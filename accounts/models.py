from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager)
from django.db import models


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(max_length=255)


class ListUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        return ListUser.objects.create(email=email)

    def create_super_user(self, email, password):
        self.create_user(email, password)


class ListUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'

    objects = ListUserManager()

    def __str__(self):
        return f"Email: {self.email}"

    @property
    def is_staff(self):
        return self.email == 'ekkinyanjui@gmail.com'

    @property
    def is_active(self):
        return True
