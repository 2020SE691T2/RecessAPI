from unittest.mock import MagicMock, patch
from .api import RegistrationAPI, LoginAPI
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginUserSerializer
from .test_utilities import TestLogger, MockRequest
from rest_framework.response import Response

import ast
import datetime
import pytest

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test classes should start with 'Test'
class TestApi:

    EMAIL_ADDRESS = "email@address.com"
    PASSWORD = "secret"
    TOKEN = "1234ABCD"

    def mock_registration_api(self, is_valid):
        registration_api = RegistrationAPI()
        registration_api.get_serializer = MagicMock(return_value=self.mock_registration_serializer(is_valid=is_valid))
        registration_api.getLogger = MagicMock(return_value=TestLogger())
        registration_api.request = ""
        registration_api.format_kwarg = ""
        return registration_api

    def mock_registration_serializer(self, is_valid):
        self.registration_serializer = CustomUserSerializer()
        self.registration_serializer.is_valid = MagicMock(return_value=is_valid)
        self.registration_serializer.custom_save = MagicMock(return_value=self.mock_valid_user_response())
        return self.registration_serializer

    def mock_registration_data(self, is_staff=None, is_superuser=None):
        request = MockRequest()
        request.data['email_address'] = TestApi.EMAIL_ADDRESS
        request.data['password'] = TestApi.PASSWORD
        request.data['is_staff'] = is_staff
        request.data['is_superuser'] = is_superuser
        return request

    def mock_valid_user_response(self):
        user = CustomUser()
        user.email_address = TestApi.EMAIL_ADDRESS
        return user

    def mock_login_api(self, is_valid):
        login_api = LoginAPI()
        login_api.request = ""
        login_api.format_kwarg = ""
        login_api.get_serializer = MagicMock(return_value=self.mock_login_serializer(is_valid=is_valid))
        login_api.getLogger = MagicMock(return_value=TestLogger())
        return login_api

    def mock_login_serializer(self, is_valid):
        self.login_serializer = LoginUserSerializer()
        self.login_serializer.is_valid = MagicMock(return_value=is_valid)
        if not is_valid:
            self.login_serializer.is_valid = MagicMock(return_value=is_valid, side_effect=Exception('mocked error'))
        self.login_serializer._validated_data = [self.mock_valid_user_response(), TestApi.TOKEN]
        return self.login_serializer

    def mock_login_data(self, is_staff=None, is_superuser=None):
        request = MockRequest()
        request.data['email_address'] = TestApi.EMAIL_ADDRESS
        request.data['password'] = TestApi.PASSWORD
        return request

    # All tests should start with 'test_'

    # RegistrationAPI
    def test_registration_post_success(self):
        is_staff = True
        is_superuser = True

        registration_api = self.mock_registration_api(is_valid=True)
        registration_api.post(request=self.mock_registration_data(is_staff=is_staff, is_superuser=is_superuser))
        self.registration_serializer.custom_save.assert_called_with(password=TestApi.PASSWORD, is_staff=is_staff, is_superuser=is_superuser)

    def test_registration_post_success_staff(self):
        is_staff = True

        registration_api = self.mock_registration_api(is_valid=True)
        registration_api.post(request=self.mock_registration_data(is_staff=is_staff))
        self.registration_serializer.custom_save.assert_called_with(password=TestApi.PASSWORD, is_staff=is_staff)


    def test_registration_post_success_student(self):
        registration_api = self.mock_registration_api(is_valid=True)
        registration_api.post(request=self.mock_registration_data())
        self.registration_serializer.custom_save.assert_called_with(password=TestApi.PASSWORD)

    def test_registration_post_serializer_data_invalid(self):
        registration_api = self.mock_registration_api(is_valid=False)
        result = registration_api.post(request=self.mock_registration_data())
        assert result.data['error'] == "The data was not valid."

    # LoginAPI
    def test_login_post_success(self):
        login_api = self.mock_login_api(is_valid=True)
        result = login_api.post(request=self.mock_login_data()).data
        assert TestApi.EMAIL_ADDRESS == result['user']['email_address']
        assert TestApi.TOKEN == result['tokens']

    def test_login_post_invalid(self):
        with pytest.raises(Exception):
            login_api = self.mock_login_api(is_valid=False)
            login_api.post(request=self.mock_login_data())
