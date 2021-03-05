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

class EventManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom event model manager where class id is the unique identifier.
    """
    def get_event_data(self, event_id, **extra_fields):
        """
        return an event.
        """
        EventManager.logger.debug("Getting event data for id %s", event_id)
        if not event_id:
            raise ValueError(_(ErrorMsg.event_dne()))
        event_data = self.model(event_id=event_id, **extra_fields)
        return event_data

class EventEnrollmentManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom event model manager where enrollment id is the unique identifier.
    """
    def get_event_enrollment_data(self, event_id, **extra_fields):
        """
        return an event.
        """
        EventEnrollmentManager.logger.debug("Getting class enrollment data for id %s", event_id)
        if not event_id:
            raise ValueError(_(ErrorMsg.event_dne()))
        event_data = self.model(event_id=event_id, **extra_fields)
        return event_data

class EventScheduleManager(models.Manager):
    logger = logging.getLogger(__name__)
    
    """
    Custom event model manager where event id is the unique identifier.
    """
    def get_event_schedule_data(self, event_id, **extra_fields):
        """
        return an event.
        """
        EventScheduleManager.logger.debug("Getting event schedule data for id %s", event_id)
        if not event_id:
            raise ValueError(_(ErrorMsg.event_dne()))
        event_data = self.model(event_id=event_id, **extra_fields)
        return event_data

class AssignmentManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom assignment model manager where assignment id is the unique identifier.
    """
    def get_assignment_schedule_data(self, assignment_id, **extra_fields):
        """
        return an assignment.
        """
        AssignmentManager.logger.debug("Getting assignment data for id %s", assignment_id)
        if not assignment_id:
            raise ValueError(_('The assignment does not exist!'))
        assignment_data = self.model(assignment_id=assignment_id, **extra_fields)
        return assignment_data

class EventRosterManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom event roster model manager where roster id is the unique identifier.
    """
    def get_roster_data(self, roster_id, **extra_fields):
        """
        return an event roster.
        """
        EventRosterManager.logger.debug("Getting roster data for id %s", roster_id)
        if not roster_id:
            raise ValueError(_('The roster does not exist!'))
        roster_data = self.model(roster_id=roster_id, **extra_fields)
        return roster_data

class EventRosterParticipantManager(models.Manager):
    logger = logging.getLogger(__name__)

    """
    Custom event roster participant model manager where roster id and email address is the unique identifier.
    """
    def get_roster_participant_data(self, roster_id, email_address, **extra_fields):
        """
        return a roster participant.
        """
        EventRosterParticipantManager.logger.debug("Getting roster participant data for id %s %s", roster_id, email_address)
        if not roster_id or not email_address:
            raise ValueError(_('The roster participant does not exist!'))
        roster_participant_data = self.model(roster_id=roster_id, email_address=email_address, **extra_fields)
        return roster_participant_data