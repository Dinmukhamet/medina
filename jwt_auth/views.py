from django.shortcuts import render
from .models import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response, decorators, permissions, status
from .serializers import *
from rest_framework.response import Response

from rest_framework.views import APIView
from hub.settings import EMAIL_HOST_USER, SECRET_KEY
from django.core.mail import BadHeaderError, send_mail
import jwt
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from jwt.exceptions import DecodeError, ExpiredSignatureError
import time
from datetime import datetime, timedelta
from .renderers import UserJSONRenderer
from utils.services import generate_token, send_email


# Create your views here.


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            confirm_password = serializer.data.get("confirm_password")
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            if new_password != confirm_password:
                return Response({"new_password": ["Passwords don't match."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            response = {
                'message': _('Password updated successfully'),
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = _("Password reset")
        from_email = EMAIL_HOST_USER
        email_to = serializer.data['email']
        try:
            user = User.objects.get(email=email_to)
        except User.DoesNotExist:
            return Response({"error": _("User with given email not found")}, status=status.HTTP_404_NOT_FOUND)
        # url = request.META['HTTP_HOST'] + \
        token = generate_token(email_to)
        url = '{}://{}{}'.format(request.scheme, request.get_host(), reverse('password_reset_confirm', args=(token.decode(),)))
        message = "Пожалуйста, перейдите на эту страницу и введите новый пароль:\n{}".format(
            url)
        send_email(subject, from_email, email_to, message, request)
        response = {'message': _(
            'Мы отправили вам инструкцию по установке нового пароля на указанный адрес электронной почты. Вы должны получить ее в ближайшее время. Если вы не получили письмо, пожалуйста, проверьте папку со спамом.')}
        return Response(response, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        token = kwargs['token']
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            email = data.get('email')
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": _("User not found.")}, status=status.HTTP_404_NOT_FOUND)
        except DecodeError:
            return Response({"error": _("Invalid token.")}, status=status.HTTP_400_BAD_REQUEST)
        except ExpiredSignatureError:
            return Response({"error": _("Token expired.")}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data.get("new_password")
        confirm_password = serializer.data.get("confirm_password")
        if new_password != confirm_password:
            return Response({"error": _("Passwords don't match.")}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": _("Your password has been changed successfully")}, status=status.HTTP_200_OK)


class ObtainTokenView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ObtainTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)