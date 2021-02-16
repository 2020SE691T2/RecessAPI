from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
import logging
from .strcnst import ErrorMsg


class CustomUserManager(BaseUserManager):
    logger = logging.getLogger(__name__)

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, password, **validated_data):
        """
        Create and save a User with the given email and password.
        """
        email = validated_data.pop('email_address')
        CustomUserManager.logger.debug("Creating user for email %s", email)
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        CustomUserManager.logger.debug("Normalized email is %s", email)
        user = self.model(email_address=email, **validated_data)
        if 'is_staff' in validated_data.keys() and validated_data['is_staff'] == True:
            user.is_staff = True
        user.set_password(password)
        user.save()
        CustomUserManager.logger.info("Created user %s", user)
        return user

    def create_superuser(self, email, password, **validated_data):
        """
        Create and save a Super User with the given email and password.
        """
        CustomUserManager.logger.debug("Creating superuser for email %s", email)
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        CustomUserManager.logger.debug("Normalized email is %s", email)
        user = self.model(email_address=email, **validated_data)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        CustomUserManager.logger.info("Created superuser %s", user)
        return user

class ClassManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom class model manager where class id is the unique identifier.
    """
    def get_class_data(self, class_id, **extra_fields):
        """
        return a class.
        """
        ClassManager.logger.debug("Getting class data for id %s", class_id)
        if not class_id:
            raise ValueError(_(ErrorMsg.class_dne()))
        class_data = self.model(class_id=class_id, **extra_fields)
        return class_data

class ClassEnrollmentManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom class model manager where enrollment id is the unique identifier.
    """
    def get_class_enrollment_data(self, class_id, **extra_fields):
        """
        return a class.
        """
        ClassEnrollmentManager.logger.debug("Getting class enrollment data for id %s", class_id)
        if not class_id:
            raise ValueError(_(ErrorMsg.class_dne()))
        class_data = self.model(class_id=class_id, **extra_fields)
        return class_data

class ClassScheduleManager(models.Manager):
    logger = logging.getLogger(__name__)
    
    """
    Custom class model manager where class id is the unique identifier.
    """
    def get_class_schedule_data(self, class_id, **extra_fields):
        """
        return a class.
        """
        ClassScheduleManager.logger.debug("Getting class schedule data for id %s", class_id)
        if not class_id:
            raise ValueError(_(ErrorMsg.class_dne()))
        class_data = self.model(class_id=class_id, **extra_fields)
        return class_data

class AssignmentManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom assignment model manager where assignment id is the unique identifier.
    """
    def get_assignment_schedule_data(self, assignment_id, **extra_fields):
        """
        return a class.
        """
        AssignmentManager.logger.debug("Getting assignment data for id %s", assignment_id)
        if not assignment_id:
            raise ValueError(_('The assignment does not exist!'))
        assignment_data = self.model(assignment_id=assignment_id, **extra_fields)
        return assignment_data

class ClassRosterManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom class roster model manager where roster id is the unique identifier.
    """
    def get_roster_data(self, roster_id, **extra_fields):
        """
        return a class.
        """
        ClassRosterManager.logger.debug("Getting roster data for id %s", roster_id)
        if not roster_id:
            raise ValueError(_('The roster does not exist!'))
        roster_data = self.model(roster_id=roster_id, **extra_fields)
        return roster_data

class ClassRosterParticipantManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom class roster participant model manager where roster id and email address is the unique identifier.
    """
    def get_roster_participant_data(self, roster_id, email_address, **extra_fields):
        """
        return a class.
        """
        ClassRosterParticipantManager.logger.debug("Getting assignment data for id %s %s", roster_id, email_address)
        if not roster_id or not email_address:
            raise ValueError(_('The roster participant does not exist!'))
        roster_participant_data = self.model(roster_id=roster_id, email_address=email_address, **extra_fields)
        return roster_participant_data