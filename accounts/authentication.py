import sys
from accounts.models import ListUser, Token


class PasswordlessAuthenticationBackend(object):

    def authenticate(self, request, uid):
        try:
            token = Token.objects.get(uid=uid)
            user, created = ListUser.objects.get_or_create(email=token.email)
            token.delete()
            return user
        except Token.DoesNotExist:
            print('No token found', file=sys.stderr)
            return None

    def get_user(self, pk):
        user = ListUser.objects.get(pk=pk)
        print(f"Email: {user.email}", file=sys.stderr)
        return user