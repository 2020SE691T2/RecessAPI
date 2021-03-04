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
from .managers import CustomUserManager, EventManager, EventEnrollmentManager, EventScheduleManager, AssignmentManager, EventRosterManager, EventRosterParticipantManager

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "Password Reset Token: {}".format(reset_password_token.key)
    html_message = """\
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta name="viewport" content="width=device-width" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Reset Password</title>
        <link href="https://recess-api.herokuapp.com/static/htmlemail.css" media="all" rel="stylesheet" type="text/css" />
        </head>

        <body>

        <table class="body-wrap">
            <tr>
                <td></td>
                <td class="container" width="600">
                    <div class="content">
                        <table class="main" width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td class="content-wrap">
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td class="content-block">
                                                Please use the following token to reset your account password:
                                            </td>
                                        </tr>
                                        <tr>
                                            <td class="content-block">
                                                {}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td class="content-block">
                                                &mdash; Recess Application Team
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        <div class="footer">
                            <table width="100%">
                                <tr>
                                    <td class="aligncenter content-block">See our code <a href="https://github.com/2020SE691T2">here</a> on GitHub.</td>
                                </tr>
                            </table>
                        </div></div>
                </td>
                <td></td>
            </tr>
        </table>
        </body>
        </html>
    """.format(reset_password_token.key)
    requests.post(
		"https://api.mailgun.net/v3/sandbox95a40589397a44f78c650f4f17c9897f.mailgun.org/messages",
		auth=("api", os.environ['MAILGUN_KEY']),
		data={"from": "Recess Application Support <mailgun@sandbox95a40589397a44f78c650f4f17c9897f.mailgun.org>",
			"to": [reset_password_token.user.email_address],
			"subject": "Password Reset for Recess Application",
			"text": email_plaintext_message,
            "html": html_message})

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

class Event(models.Model):
    """
    """
    # required and unique
    event_id = models.CharField(max_length=100, blank=True, default='', primary_key=True) 
    event_name = models.CharField(max_length=100, blank=True, default='') 
    meeting_link = models.CharField(max_length=100, blank=True, default='')
    super_link = models.CharField(max_length=100, blank=True, default='')
    year = models.CharField(max_length=100, blank=True, default='')
    section = models.CharField(max_length=100, blank=True, default='')
    
    CLASSNAME_FIELD = 'event_id'
    REQUIRED_FIELDS = ['event_name', 'meeting_link', 'super_link', 'year', 'section']
    
    objects = EventManager()
    
    class Meta:
        db_table = 'events'
    
    def __str__(self):
        return str(self.event_id)

class EventEnrollment(models.Model):
    """
    """
    # required and unique
    enrollment_id = models.IntegerField(primary_key=True)
    event = models.ForeignKey(Event, related_name='enrollment', on_delete=models.CASCADE)
    roster_id = models.IntegerField()

    CLASSNAME_FIELD = 'enrollment_id'
    REQUIRED_FIELDS = ['event', 'roster_id']
    
    objects = EventEnrollmentManager()
    
    class Meta:
        db_table = 'event_enrollment'
    
    def __str__(self):
        return str(self.event_id)

class EventRoster(models.Model):
    """
    """
    roster_id = models.IntegerField(primary_key=True)
    roster_name = models.CharField(max_length=100, blank=False, default='')

    CLASSNAME_FIELD = 'roster_id'
    REQUIRED_FIELDS = ['roster_name']
    
    objects = EventRosterManager()
    
    class Meta:
        db_table = 'event_roster'
    
    def __str__(self):
        return str(self.roster_id)

class EventRosterParticipant(models.Model):
    participant_id = models.IntegerField(primary_key=True)
    roster = models.ForeignKey(EventRoster, related_name='participants', on_delete=models.CASCADE)
    email_address = models.EmailField(_('email_address'))

    CLASSNAME_FIELD = 'participant_id'
    REQUIRED_FIELDS = ['roster', 'email_address']
    
    objects = EventRosterParticipantManager()
    
    class Meta:
        unique_together = ['roster', 'email_address']
        db_table = 'event_roster_participant'
    
    def __str__(self):
        return str(self.roster_id) + " " + self.email_address

class EventSchedule(models.Model):
    """
    """
    # required and unique
    schedule_id = models.IntegerField(primary_key=True)
    event = models.ForeignKey(Event, related_name='event', on_delete=models.CASCADE)
    weekday = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    CLASSNAME_FIELD = 'schedule_id'
    REQUIRED_FIELDS = ['event', 'weekday', 'start_time', 'end_time']
    
    objects = EventScheduleManager()
    
    class Meta:
        db_table = 'event_schedule'
    
    def __str__(self):
        return str(self.event_id)

class Assignment(models.Model):
    """
    """
    # required and unique
    assignment_id = models.CharField(max_length=100, blank=True, default='', primary_key=True)
    name = models.CharField(max_length=10000, blank=True, default='')
    description = models.CharField(max_length=100000, blank=True, default='')
    assigned_date = models.DateField()
    due_date = models.DateField()
    event_id = models.CharField(max_length=100, blank=True, default='')

    ASSIGNMENTNAME_FIELD = 'assignment_id'
    REQUIRED_FIELDS = ['name', 'description', 'assigned_date', 'due_date', 'event_id']
    
    objects = AssignmentManager()
    
    class Meta:
        db_table = 'assignments'
    
    def __str__(self):
        return str(self.assignment_id)
