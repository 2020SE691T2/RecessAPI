from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import CustomUserManager, ClassManager, ClassEnrollmentManager, ClassScheduleManager, AssignmentManager

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email_address]
    )

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
    year = models.CharField(max_length=100, blank=True, default='')
    section = models.CharField(max_length=100, blank=True, default='')
    
    CLASSNAME_FIELD = 'class_id'
    REQUIRED_FIELDS = ['class_name', 'meeting_link', 'year', 'section']
    
    objects = ClassManager()
    
    class Meta:
        db_table = 'classes'
    
    def __str__(self):
        return self.class_id

class ClassEnrollment(models.Model):
    """
    """
    # required and unique
    enrollment_id = models.IntegerField(primary_key=True)
    class_id = models.CharField(max_length=100, blank=False, editable=False)
    teacher_email = models.EmailField(_('email_address')) 
    student_email = models.EmailField(_('email_address')) 

    CLASSNAME_FIELD = 'class_id'
    REQUIRED_FIELDS = ['teacher_email', 'student_email']
    
    objects = ClassEnrollmentManager()
    
    class Meta:
        db_table = 'class_enrollment'
    
    def __str__(self):
        return self.class_id

class ClassSchedule(models.Model):
    """
    """
    # required and unique
    schedule_id = models.IntegerField(primary_key=True)
    class_id = models.CharField(max_length=100, blank=True, default='')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    CLASSNAME_FIELD = 'class_id'
    REQUIRED_FIELDS = ['date', 'start_time', 'end_time']
    
    objects = ClassScheduleManager()
    
    class Meta:
        db_table = 'class_schedule'
    
    def __str__(self):
        return self.class_id

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
        return self.assignment_id