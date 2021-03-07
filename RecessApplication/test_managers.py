from unittest.mock import MagicMock
from .managers import CustomUserManager
from .models import CustomUser
from .test_utilities import TestLogger
import pytest

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test events should start with 'Test'
class TestManager:

    PASSWORD = "PASSWORD"
    EMAIL_ADDRESS = "test@example.com"
    EMPTY = None

    def mock_user_manager(self):
        user_manager = CustomUserManager()
        user_manager.getLogger = MagicMock(return_value=TestLogger())
        user_manager.model = MagicMock(return_value=self.mock_user())
        return user_manager

    def mock_user(self):
        user = CustomUser()
        user.save = MagicMock(return_value=True)
        return user

    # All tests should start with 'test_'

    def test_create_user_success(self):
        manager = self.mock_user_manager()
        is_staff = False
        user = manager.create_user(password=TestManager.PASSWORD, email_address=TestManager.EMAIL_ADDRESS, is_staff=is_staff)
        assert user.is_staff == is_staff
        # Check hashing
        assert TestManager.PASSWORD != user.password

    def test_create_user_staff_success(self):
        manager = self.mock_user_manager()
        is_staff = True
        user = manager.create_user(password=TestManager.PASSWORD, email_address=TestManager.EMAIL_ADDRESS, is_staff=is_staff)
        assert user.is_staff == is_staff

    def test_create_user_failure(self):
        with pytest.raises(ValueError):
            manager = self.mock_user_manager()
            manager.create_user(password=TestManager.PASSWORD, email_address=TestManager.EMPTY)

    def test_create_superuser_staff_success(self):
        manager = self.mock_user_manager()
        user = manager.create_superuser(password=TestManager.PASSWORD, email=TestManager.EMAIL_ADDRESS)
        assert user.is_staff == True
        assert user.is_superuser == True
        # Check hashing
        assert TestManager.PASSWORD != user.password

    def test_create_superuser_failure(self):
        with pytest.raises(ValueError):
            manager = self.mock_user_manager()
            manager.create_superuser(password=TestManager.PASSWORD, email=TestManager.EMPTY)