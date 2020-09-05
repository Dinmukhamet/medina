from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import CreateUserForm
# Register your models here.



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    add_fieldsets = [
        (None, {
            'fields':
                [
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'role',
                    'is_superuser',
                    'groups'
                ]
        })
    ]
    list_display = ('id', 'email', 'first_name', 'last_name',
                    'is_superuser', 'is_staff', 'role')
    list_display_links = ('id', 'email')
    fieldsets = (
        (None, {
            "fields": (
                'email',
                'password',
                'is_superuser',
                'role',
                'groups'
            ),
        }),
        (_('Personal info'), {
            "fields": (
                'first_name',
                'last_name',
            )
        }),
        (_('Dates'), {
            'fields': (
                'last_login',
                'date_joined'
            )
        })
    )
    ordering = ('-id', 'email')

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            if not obj:
                return [(None, {
                        'fields':
                            [
                                'first_name',
                                'last_name',
                                'password1',
                                'password2',
                            ]
                        })
                        ]
            return [(None, {'fields': ('first_name', 'last_name')}), ]
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(is_superuser=True)

admin.site.site_url = None