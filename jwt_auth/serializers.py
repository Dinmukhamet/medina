from .models import *
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from utils.services import generate_token, special_match
from django.utils.translation import ugettext_lazy as _
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
import re
from hub.settings import SECRET_KEY



class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        first_name = data['first_name']
        last_name = data['last_name']

        if not special_match(first_name):
            raise serializers.ValidationError(
                _("You have to write a valid first name. Don't use any characters other than letters of the alphabet.")
            )

        if not special_match(last_name):
            raise serializers.ValidationError(
                _("You have to write a valid last name. Don't use any characters other than letters of the alphabet.")
            )
        return data

    def create(self, validated_data):
        email = validated_data["email"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        role = validated_data["role"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if (email and User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})
        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(email=email,
                    first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'new_password',
            'confirm_password'
        ]


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'email',
        ]


class ObtainTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email is None:
            raise serializers.ValidationError(
                _("An email address is required to log in.")
            )

        if password is None:
            raise serializers.ValidationError(
                _("A password is required to log in.")
            )

        validate_email(email)
        user = User.objects.filter(email=email)
        if not user.exists():
            raise serializers.ValidationError(
                _("A user with given email not found.")
            )

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                _("Authentication failed with specified credentials")
            )

        return {
            'email': email,
            'token': generate_token(email).decode('utf-8')
        }


class RefreshTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    def validate(self, data):
        token = data.get('token')

        if token is None:
            raise serializers.ValidationError(
                _("Token not found")
            )
        try:
            data = jwt.decode(token, SECRET_KEY, verify=False,
                              algorithms=['HS256'])
        except DecodeError:
            raise serializers.ValidationError(
                _("Invalid token")
            )

        try:
            user = User.objects.get(email=data.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError(
                _("User not found")
            )

        return {
            'token': generate_token(user.email).decode('utf-8')
        }