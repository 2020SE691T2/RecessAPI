import requests
import os
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import CustomUserManager, ClassManager, ClassEnrollmentManager, ClassScheduleManager, AssignmentManager, ClassRosterManager, ClassRosterParticipantManager

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "Password Reset Token: {}".format(reset_password_token.key)
    requests.post(
		"https://api.mailgun.net/v3/sandbox95a40589397a44f78c650f4f17c9897f.mailgun.org/messages",
		auth=("api", os.environ['MAILGUN_KEY']),
		data={"from": "Recess Application Support <mailgun@sandbox95a40589397a44f78c650f4f17c9897f.mailgun.org>",
			"to": [reset_password_token.user.email_address],
			"subject": "Password Reset for Recess Application",
			"text": email_plaintext_message})

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
    photo = models.CharField(max_length=1000000, blank=True, default='')
    is_staff = models.BooleanField(blank=True, default=False)
    is_superuser = models.BooleanField(blank=True, default=False)
    
    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['first_name', 'last_name','preferred_name','physical_id_num','dob','role','is_staff','is_superuser','photo']

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email_address

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }

class Class(models.Model):
    """
    """
    # required and unique
    class_id = models.CharField(max_length=100, blank=True, default='', primary_key=True) 
    class_name = models.CharField(max_length=100, blank=True, default='') 
    meeting_link = models.CharField(max_length=100, blank=True, default='')
    super_link = models.CharField(max_length=100, blank=True, default='')
    year = models.CharField(max_length=100, blank=True, default='')
    section = models.CharField(max_length=100, blank=True, default='')
    
    CLASSNAME_FIELD = 'class_id'
    REQUIRED_FIELDS = ['class_name', 'meeting_link', 'super_link', 'year', 'section']
    
    objects = ClassManager()
    
    class Meta:
        db_table = 'classes'
    
    def __str__(self):
        return str(self.class_id)

class ClassEnrollment(models.Model):
    """
    """
    # required and unique
    enrollment_id = models.IntegerField(primary_key=True)
    class_id = models.CharField(max_length=100, blank=False, editable=False)
    roster_id = models.IntegerField()

    CLASSNAME_FIELD = 'enrollment_id'
    REQUIRED_FIELDS = ['class_id', 'roster_id']
    
    objects = ClassEnrollmentManager()
    
    class Meta:
        db_table = 'class_enrollment'
    
    def __str__(self):
        return str(self.class_id)

class ClassRoster(models.Model):
    """
    """
    roster_id = models.IntegerField(primary_key=True)
    roster_name = models.CharField(max_length=100, blank=False, editable=False)

    CLASSNAME_FIELD = 'roster_id'
    REQUIRED_FIELDS = ['roster_name']
    
    objects = ClassRosterManager()
    
    class Meta:
        db_table = 'class_roster'
    
    def __str__(self):
        return str(self.roster_id)

class ClassRosterParticipant(models.Model):
    roster_id = models.ForeignKey(ClassRoster, related_name='roster', on_delete=models.CASCADE)
    email_address = models.EmailField(_('email_address'))

    CLASSNAME_FIELD = 'roster_id'
    REQUIRED_FIELDS = ['email_address']
    
    objects = ClassRosterParticipantManager()
    
    class Meta:
        unique_together = ['roster_id', 'email_address']
        db_table = 'class_roster_participant'
    
    def __str__(self):
        return str(self.roster_id) + " " + self.email_address

class ClassSchedule(models.Model):
    """
    """
    # required and unique
    schedule_id = models.IntegerField(primary_key=True)
    class_id = models.CharField(max_length=100, blank=True, default='')
    weekday = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    CLASSNAME_FIELD = 'class_id'
    REQUIRED_FIELDS = ['weekday', 'start_time', 'end_time']
    
    objects = ClassScheduleManager()
    
    class Meta:
        db_table = 'class_schedule'
    
    def __str__(self):
        return str(self.class_id)

class Assignment(models.Model):
    """
    """
    # required and unique
    assignment_id = models.CharField(max_length=100, blank=True, default='', primary_key=True)
    name = models.CharField(max_length=10000, blank=True, default='')
    description = models.CharField(max_length=100000, blank=True, default='')
    assigned_date = models.DateField()
    due_date = models.DateField()
    class_id = models.CharField(max_length=100, blank=True, default='')

    ASSIGNMENTNAME_FIELD = 'assignment_id'
    REQUIRED_FIELDS = ['name', 'description', 'assigned_date', 'due_date', 'class_id']
    
    objects = AssignmentManager()
    
    class Meta:
        db_table = 'assignments'
    
    def __str__(self):
        return str(self.assignment_id)