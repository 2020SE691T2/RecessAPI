from unittest.mock import MagicMock
from RecessApplication.backends import UserBackend
from RecessApplication.models import CustomUser

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test events should start with 'Test'
class TestBackend:
    USERNAME = "TEST_USERNAME"
    PASSWORD = "TEST_PASSWORD"
    INVALID_PASSWORD = "NOT_PASSWORD"

    def mock_user_backend(self, is_user=True):
        user_backend = UserBackend()
        user_backend.get_user = MagicMock(return_value=self.mock_user(is_user=is_user))
        return user_backend

    def mock_user(self, is_user=True):
        user = CustomUser()
        user.username = TestBackend.USERNAME
        if is_user:
            user.password = TestBackend.PASSWORD
        else:
            user.password = TestBackend.INVALID_PASSWORD
        return user

    # All tests should start with 'test_'
    def test_authenticate_success(self):
        user_backend = self.mock_user_backend()
        result = user_backend.authenticate(request=None, password=TestBackend.PASSWORD)
        assert result == self.mock_user()

    def test_authenticate_wrong_password(self):
        user_backend = self.mock_user_backend()
        result = user_backend.authenticate(request=None, password=TestBackend.INVALID_PASSWORD)
        assert result == None

    def test_authenticate_wrong_username(self):
        user_backend = self.mock_user_backend(is_user=False)
        result = user_backend.authenticate(request=None, password=TestBackend.PASSWORD)
        assert result == None
