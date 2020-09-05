from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Projects(models.Model):
    PROJECT_TYPE_CHOICES = [
        (1, _("Inner")),
        (2, _("Social")),
        (3, _("Commercial"))
    ]

    name = models.CharField(_("Project's name"), max_length=100)
    date_start = models.DateField(_("Start of the project"), auto_now=False, auto_now_add=False)
    date_end = models.DateField(_("End of the project"), auto_now=False, auto_now_add=False)
    project_type = models.IntegerField(_("Type of the project"), choices=PROJECT_TYPE_CHOICES)
    description = models.TextField(_("Description"))
    product_owner = models.CharField(_("Product Owner"), max_length=100)

    class Meta:
        ordering = ['-id']
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name

def upload_location(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    return '{}.{}'.format(instance.project.name, extension)

class ProjectsDocuments(models.Model):
    project = models.ForeignKey(Projects, verbose_name=_("Project"), on_delete=models.CASCADE, related_name='documents')
    datafile = models.FileField(_("File"), upload_to=upload_location)

class ProjectsImages(models.Model):
    project = models.ForeignKey(Projects, verbose_name=_("Project"), on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_("Image"), upload_to=upload_location, height_field=None, width_field=None, max_length=None)

class UserRoles(models.Model):
    name = models.CharField(_("Role Name"), max_length=50)

    class Meta:
        ordering = ['-id']
        verbose_name = _("User Role")
        verbose_name_plural = _("User Roles")
    
    def __str__(self):
        return self.name

class UserToProjects(models.Model):
    project = models.ForeignKey(Projects, verbose_name=_("Project"), related_name="users", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("jwt_auth.User", verbose_name=_("User"), related_name="projects", on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(UserRoles, verbose_name=_("Role of the user"), on_delete=models.SET_NULL, null=True)

    @property
    def user_name(self):
        return self.user.email
    
    @property
    def role_name(self):
        return self.role.name