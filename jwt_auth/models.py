from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from .managers import UserManager
# Create your models here.


class User(AbstractUser):
    user_manager = UserManager()
    username = None
    first_name = models.CharField(
        max_length=100, null=True, verbose_name=_('First name'), help_text=_(
            'Required. 100 characters or fewer. Type your first name.'))
    last_name = models.CharField(
        max_length=100, null=True, verbose_name=_('Last name'), help_text=_(
            'Required. 100 characters or fewer. Type your last name.'))
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    role = models.ForeignKey("main.UserRoles", verbose_name=_("Role"), on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-id']
        verbose_name = _('User')
        verbose_name_plural = _('Users')