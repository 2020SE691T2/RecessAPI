from unittest.mock import MagicMock
from RecessApplication.models import CustomUser

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test classes should start with 'Test'
class TestModels:
    USERNAME = "TEST_USERNAME"
    PASSWORD = "TEST_PASSWORD"

    def mock_user(self, ):
        user = CustomUser()
        user.username = TestModels.USERNAME
        user.password = TestModels.PASSWORD
        return user

    # All tests should start with 'test_'

    def test_tokens_not_empty(self):
        user = self.mock_user()
        token = user.tokens()
        refresh = token['refresh']
        access = token['access']
        assert refresh != None and refresh != ""
        assert access != None and access != ""

    def test_tokens_different(self):
        user_one = self.mock_user()
        user_two = self.mock_user()

        token_one = user_one.tokens()
        refresh_one = token_one['refresh']
        access_one = token_one['access']

        token_two = user_two.tokens()
        refresh_two = token_two['refresh']
        access_two = token_two['access']

        assert refresh_one != refresh_two
        assert access_one != access_two

    def test_tokens_change(self):
        user = self.mock_user()

        token_one = user.tokens()
        refresh_one = token_one['refresh']
        access_one = token_one['access']

        # Get new tokens
        token_two = user.tokens()
        refresh_two = token_two['refresh']
        access_two = token_two['access']

        assert refresh_one != refresh_two
        assert access_one != access_two