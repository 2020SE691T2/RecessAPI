from unittest.mock import MagicMock, patch
from .api import RegistrationAPI, LoginAPI, WeeklyScheduleAPI
from .managers import ClassEnrollmentManager, ClassManager, ClassScheduleManager
from .models import CustomUser, ClassEnrollment, Class, ClassSchedule
from .serializers import CustomUserSerializer, LoginUserSerializer
from .test_utilities import TestLogger, MockRequest
from rest_framework.response import Response
from datetime import datetime
from django.db.models.query import QuerySet

import ast
import datetime
import pytest

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# Mock class
class MockWeeklyScheduleAPI(WeeklyScheduleAPI):
    def exists(self, obj):
        return len(obj) > 0

# All test classes should start with 'Test'
class TestApi:

    EMAIL_ADDRESS = "email@address.com"
    EMAIL_ADDRESS = "fake@address.com"
    NOT_A_PASSW0RD = "secret"
    TOKEN = "1234ABCD"
    NUM_DAILY_CLASSES=1
    NUM_WEEKLY_CLASSES=5
    # Nominal testing year
    SCHEDULED_YEAR=2020
    # Year to use for testing 'early' week entries
    EARLY_YEAR=SCHEDULED_YEAR-1
    # Should have no entries
    BAD_YEAR=1980
    # Early weeks are for previous years
    EARLY_WEEK=2
    # Late weeks are for designated years
    LATE_WEEK=50

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
        request.data['password'] = TestApi.NOT_A_PASSW0RD
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
        request.data['password'] = TestApi.NOT_A_PASSW0RD
        return request

    # All tests should start with 'test_'

    # RegistrationAPI
    def test_registration_post_success(self):
        is_staff = True
        is_superuser = True

        registration_api = self.mock_registration_api(is_valid=True)
        registration_api.post(request=self.mock_registration_data(is_staff=is_staff, is_superuser=is_superuser))
        self.registration_serializer.custom_save.assert_called_with(password=TestApi.NOT_A_PASSW0RD, is_staff=is_staff, is_superuser=is_superuser)

    def test_registration_post_success_staff(self):
        is_staff = True

        registration_api = self.mock_registration_api(is_valid=True)
        registration_api.post(request=self.mock_registration_data(is_staff=is_staff))
        self.registration_serializer.custom_save.assert_called_with(password=TestApi.NOT_A_PASSW0RD, is_staff=is_staff)


    def test_registration_post_success_student(self):
        registration_api = self.mock_registration_api(is_valid=True)
        registration_api.post(request=self.mock_registration_data())
        self.registration_serializer.custom_save.assert_called_with(password=TestApi.NOT_A_PASSW0RD)

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

    # WeeklyScheduleAPI
    def mock_schedule_request(self, year, week, is_staff=True):
        request = MockRequest()
        request.user.is_staff = is_staff
        request.data['year'] = year
        request.data['week'] = week
        return request

    def mock_schedule_api(self, has_enrollments=True):
        schedule_api = MockWeeklyScheduleAPI()
        schedule_api.getClassEnrollments = MagicMock(return_value=self.mock_enrollment_data(has_enrollments))
        schedule_api.getClasses = MagicMock(return_value=self.mock_class_data())
        schedule_api.getClassSchedules = MagicMock(return_value=self.mock_class_schedule_data())
        schedule_api.enrollments_exists = MagicMock()
        return schedule_api

    def mock_enrollment_data(self, has_enrollments):
        result = ClassEnrollmentManager()

        data = []
        max_class_id=0
        for index in range(TestApi.NUM_DAILY_CLASSES + TestApi.NUM_WEEKLY_CLASSES):
            next = {}
            next['enrollment_id'] = index + 10
            next['class_id'] = index
            next['student_email'] = "student@email.fake"
            next['teacher_email'] = "teacher@email.fake"
            data.append(next)
        max_class_id = TestApi.NUM_DAILY_CLASSES + TestApi.NUM_WEEKLY_CLASSES

        for index in range(TestApi.NUM_DAILY_CLASSES):
            next = {}
            next['enrollment_id'] = max_class_id + index + 10
            next['class_id'] = max_class_id + index
            next['student_email'] = "student@email.fake"
            next['teacher_email'] = "teacher@email.fake"
            data.append(next)

        queryset = QuerySet()
        result.filter = MagicMock(return_value=queryset)
        
        if has_enrollments:
            queryset.values = MagicMock(return_value=data)
        else:
            queryset.values = MagicMock(return_value=[])

        return result

    def mock_class_data(self):
        result = ClassManager()

        data = []
        max_class_id=0
        # Make a 'class' for each class designated
        for index in range(TestApi.NUM_DAILY_CLASSES + TestApi.NUM_WEEKLY_CLASSES):
            next = {}
            next['class_id'] = index
            next['class_name'] = "Class " + str(index)
            next['meeting_link'] = "https://www.google.fake"
            next['section'] = "fake"
            next['year'] = TestApi.SCHEDULED_YEAR
            data.append(next)
            max_class_id=index
        max_class_id = max_class_id + 1

        # Make a 'class' for each daily designated class for previous year
        for index in range(TestApi.NUM_DAILY_CLASSES):
            next = {}
            next['class_id'] = index + max_class_id
            next['class_name'] = "Class " + str(index + max_class_id)
            next['meeting_link'] = "https://www.google.fake"
            next['section'] = "fake"
            next['year'] = TestApi.EARLY_YEAR
            data.append(next)

        queryset = QuerySet()
        result.filter = MagicMock(return_value=queryset)
        queryset.values = MagicMock(return_value=data)

        return result

    def mock_class_schedule_data(self):
        result = ClassScheduleManager()

        data = []

        # Make a 'class' for each class designated (weekly)
        max_previous=0
        for index in range(TestApi.NUM_WEEKLY_CLASSES):
            start_hour = (6 + index*2) % 20
            stop_hour = start_hour+1

            next = {}
            next['class_id'] = index
            next['schedule_id'] = index + 20
            next['weekday'] = index % 5
            next['start_time'] = str(datetime.time(hour=start_hour, minute=0, second=0))
            next['end_time'] = str(datetime.time(hour=stop_hour, minute=0, second=0))
            data.append(next)
            max_previous = index
        max_previous = max_previous + 1

        # Make a 'class' for each class designated (daily)
        for index in range(TestApi.NUM_DAILY_CLASSES):
            daily_index = index + max_previous
            start_hour = (6 + daily_index*2) % 20
            stop_hour = start_hour+1

            next = {}
            next['class_id'] = daily_index
            next['schedule_id'] = daily_index + 20
            next['weekday'] = -1
            next['start_time'] = str(datetime.time(hour=start_hour, minute=0, second=0))
            next['end_time'] = str(datetime.time(hour=stop_hour, minute=0, second=0))
            data.append(next)
        max_previous = max_previous + TestApi.NUM_DAILY_CLASSES

        # Make a 'class' for each daily designated class for previous year
        for index in range(TestApi.NUM_DAILY_CLASSES):
            daily_index = index + max_previous
            start_hour = (6 + daily_index*2) % 20
            stop_hour = start_hour+1

            next = {}
            next['class_id'] = daily_index
            next['schedule_id'] = daily_index + 20
            next['weekday'] = -1
            next['start_time'] = str(datetime.time(hour=start_hour, minute=0, second=0))
            next['end_time'] = str(datetime.time(hour=stop_hour, minute=0, second=0))
            data.append(next)

        queryset = QuerySet()
        result.filter = MagicMock(return_value=queryset)
        queryset.values = MagicMock(return_value=data)

        return result

    def test_schedule_success(self):
        request = self.mock_schedule_request(year=TestApi.SCHEDULED_YEAR, week=TestApi.LATE_WEEK)
        schedule_api = self.mock_schedule_api()
        result = schedule_api.get(request)
        assert len(result.data['schedules']) == TestApi.NUM_WEEKLY_CLASSES + TestApi.NUM_DAILY_CLASSES * 5

    def test_schedule_success_user(self):
        request = self.mock_schedule_request(is_staff=False, year=TestApi.SCHEDULED_YEAR, week=TestApi.LATE_WEEK)
        schedule_api = self.mock_schedule_api()
        result = schedule_api.get(request)
        assert len(result.data['schedules']) == TestApi.NUM_WEEKLY_CLASSES + TestApi.NUM_DAILY_CLASSES * 5

    def test_schedule_empty_year(self):
        request = self.mock_schedule_request(year=TestApi.BAD_YEAR, week=TestApi.LATE_WEEK)
        schedule_api = self.mock_schedule_api()
        result = schedule_api.get(request)
        assert len(result.data['schedules']) == 0

    def test_schedule_success_early(self):
        request = self.mock_schedule_request(year=TestApi.SCHEDULED_YEAR, week=TestApi.EARLY_WEEK)
        schedule_api = self.mock_schedule_api()
        result = schedule_api.get(request)
        assert len(result.data['schedules']) == TestApi.NUM_DAILY_CLASSES * 5

    def test_schedule_failure_enrollments(self):
        request = self.mock_schedule_request(year=TestApi.SCHEDULED_YEAR, week=TestApi.EARLY_WEEK)
        schedule_api = self.mock_schedule_api(has_enrollments=False)
        result = schedule_api.get(request)
        assert len(result.data['error']) > 0
        assert "not enrolled" in result.data['error']