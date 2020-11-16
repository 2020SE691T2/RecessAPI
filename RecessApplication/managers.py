from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
import logging


class CustomUserManager(BaseUserManager):
    logger = logging.getLogger(__name__)

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        CustomUserManager.logger.debug("Creating user for email %s", email)
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email_address=email, **extra_fields)
        user.set_password(password)
        user.save()
        CustomUserManager.logger.info("Created user %s", user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a Super User with the given email and password.
        """
        CustomUserManager.logger.debug("Creating superuser for email %s", email)
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email_address=email, **extra_fields)
        user.set_password(password)
        user.save()
        CustomUserManager.logger.info("Created superuser %s", user)
        return user

class ClassManager():
    logger = logging.getLogger(__name__)

    """
    Custom class model manager where class id is the unique identifiers
    for authentication instead of usernames.
    """
    def get_class_data(self, class_id, **extra_fields):
        """
        return a class.
        """
        ClassManager.logger.debug("Getting class data for id %s", class_id)
        if not class_id:
            raise ValueError(_('The class does not exist!'))
        class_data = self.model(class_id=class_id, **extra_fields)
        return class_data

class ClassEnrollmentManager():
    logger = logging.getLogger(__name__)

    """
    Custom class model manager where class id is the unique identifiers
    for authentication instead of usernames.
    """
    def get_class_enrollment_data(self, class_id, **extra_fields):
        """
        return a class.
        """
        ClassEnrollmentManager.logger.debug("Getting class enrollment data for id %s", class_id)
        if not class_id:
            raise ValueError(_('The class does not exist!'))
        class_data = self.model(class_id=class_id, **extra_fields)
        return class_data

class ClassScheduleManager():
    logger = logging.getLogger(__name__)
    
    """
    Custom class model manager where class id is the unique identifiers
    for authentication instead of usernames.
    """
    def get_class_schedule_data(self, class_id, **extra_fields):
        """
        return a class.
        """
        ClassScheduleManager.logger.debug("Getting class schedule data for id %s", class_id)
        if not class_id:
            raise ValueError(_('The class does not exist!'))
        class_data = self.model(class_id=class_id, **extra_fields)
        return class_data

class AssignmentManager():
    logger = logging.getLogger(__name__)

    """
    Custom assignment model manager where assignment id is the unique identifiers
    for authentication instead of usernames.
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