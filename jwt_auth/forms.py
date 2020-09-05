from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_staff = True
        user.is_active = True
        user.save()
        return user