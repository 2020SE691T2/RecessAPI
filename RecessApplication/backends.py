from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
import logging

class UserBackend(BaseBackend):    
    logger = logging.getLogger(__name__)
    User = get_user_model()

    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user, need to add check_password for authentication realistically
        user = self.get_user(username)
        pwd_valid = password == user.password
        UserBackend.logger.info('Authenticating %s, user=%s, pwd_valid=%s', username, user, pwd_valid)
        if user and pwd_valid:
            return user
        return None
    
    def get_user(self, email_address):
        try:
            return UserBackend.User.objects.get(email_address=email_address)
        except UserBackend.User.DoesNotExist:
            UserBackend.logger.error("Could not find user for email address: %s", email_address)
            return None