from uuid import uuid4

from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


def gen_uuid():
    return uuid4().hex


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default=gen_uuid, max_length=40)
