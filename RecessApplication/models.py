from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

from .managers import CustomUserManager, CustomClassManager

class CustomUser(AbstractBaseUser):
    last_login = None

    # required and unique       
    email_address = models.EmailField(_('email_address'), primary_key=True) 
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

class CustomClass(models.Model):
    """
    """
    # required and unique
    class_id = models.CharField(max_length=100, blank=True, default='', primary_key=True) 
    class_name = models.CharField(max_length=100, blank=True, default='') 
    meeting_link = models.CharField(max_length=100, blank=True, default='')
    year = models.CharField(max_length=100, blank=True, default='')
    section = models.CharField(max_length=100, blank=True, default='')
    
    CLASSNAME_FIELD = 'class_id'
    REQUIRED_FIELDS = ['class_name', 'meeting_link', 'year', 'section']
    
    objects = CustomClassManager()
    
    class Meta:
        db_table = 'classes'
    
    def __str__(self):
        return self.class_id
