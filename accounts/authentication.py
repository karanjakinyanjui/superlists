import sys

from django.contrib.auth import get_user_model

from accounts.models import Token

User = get_user_model()


class PasswordlessAuthenticationBackend:


    def authenticate(self, request, uid):
        try:
            token = Token.objects.get(uid=uid)
            user, _ = User.objects.get_or_create(email=token.email)
            return user
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        return User.objects.filter(email=email).first()
