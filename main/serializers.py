from rest_framework import serializers
from .models import *

class UserToProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserToProjects
        fields = [
            'id',
            'user',
            'role'
        ]

class DocumentsToProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectsDocuments
        fields = [
            'datafile'
        ]

class ImageToProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectsImages
        fields = [
            'image'
        ]

class ProjectsSerializer(serializers.ModelSerializer):
    users = UserToProjectsSerializer(many=True)
    documents = DocumentsToProjectsSerializer(many=True)
    images = ImageToProjectsSerializer(many=True)

    class Meta:
        model = Projects
        fields = [
            'id', 
            'name', 
            'project_type',
            'date_start',
            'date_end',
            'users',
            'documents',
            'images'
        ]
    
    def create(self, validated_data):
        users = validated_data.pop('users')
        documents = validated_data.pop('documents')
        images = validated_data.pop('images')
        project = Projects.objects.create(**validated_data)
        for user in users:
            u = UserToProjects.objects.create(project=project, **user)
        for document in documents:
            d = ProjectsDocuments.objects.create(project=project, **document)
        for image in images:
            i = ProjectsImages.objects.create(project=project, **image)
        return project