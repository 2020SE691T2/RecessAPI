from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser):
    last_login = None

    # required and unique       
    email_address = models.EmailField(_('email address'), unique=True) 
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    preferred_name = models.CharField(max_length=100, blank=True, default='')
    physical_id_num = models.CharField(max_length=100, blank=True, default='')
    dob = models.DateField(auto_now_add=False)
    role = models.CharField(max_length=100, blank=True, default='')

    # Password included already...
    #password = models.CharField(max_length=100, blank=True, default='')

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['first_name', 'last_name','preferred_name','physical_id_num','dob','role']

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email_address