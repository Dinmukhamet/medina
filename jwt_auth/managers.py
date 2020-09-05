from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, first_name, last_name, role, password=None):
        """Create and return a `User` with an email, username and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, first_name, last_name, email, role, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, first_name, last_name, role, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user