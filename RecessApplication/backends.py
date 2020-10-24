from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user, need to add check_password for authentication realistically
        user = self.get_user(username)
        pwd_valid = password == user.password
        print(f'Authenticating {username}, user={user}, pwd_valid={pwd_valid}')
        if user and pwd_valid:
            return user
        return None
    
    def get_user(self, email_address):
        try:
            return User.objects.get(email_address=email_address)
        except User.DoesNotExist:
            return None

        