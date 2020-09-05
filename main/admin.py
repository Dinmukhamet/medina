from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserRoles)
class UserRolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    fieldsets = (
        (None, {
            "fields": (
                'name',
            ),
        }),
    )

class UserToProjectsInline(admin.StackedInline):
    model = UserToProjects
    extra = 0


class ProjectsDocumentsInline(admin.StackedInline):
    model = ProjectsDocuments
    extra = 0


class ProjectsImagesInline(admin.StackedInline):
    model = ProjectsImages
    extra = 0


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'project_type',
        'date_start',
        'date_end',
    )
    list_display_links = ('id', 'name')
    fieldsets = (
        (None, {
            "fields": (
                'name',
                'project_type',
                'date_start',
                'date_end'
            ),
        }),
    )
    inlines = [
        UserToProjectsInline, 
        ProjectsDocumentsInline,
        ProjectsImagesInline
    ]
    

    