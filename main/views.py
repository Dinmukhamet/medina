from django.shortcuts import render
from rest_framework import generics, permissions
from .models import *
from .serializers import *

# Create your views here.
class CreateProjectView(generics.CreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [permissions.IsAuthenticated]

class ListProjectsView(generics.ListAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [permissions.AllowAny]

class RetrieveProjectView(generics.RetrieveAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer

    # TODO Custom Permission
