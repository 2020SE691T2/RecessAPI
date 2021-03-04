from unittest.mock import MagicMock, ANY
from .models import CustomUser, Event
from .serializers import EventSerializer
from .views import UserViewSet, EventViewSet, ZoomMeetingsView, ZoomMeetingsListView, StudentTeacherViewSet
from .test_utilities import MockRequest
from .zoom import ZoomProxy
import json

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test events should start with 'Test'
class TestViews:

    JOIN_URL = "JOIN_URI"
    START_URL = "START_URI"
    NUM_TEACHERS = 2
    NUM_STUDENTS = 5

    def mock_userviewset(self):
        user_viewset = UserViewSet()
        user_viewset.update = MagicMock(return_value=self.mock_user())
        user_viewset.kwargs = {}
        user_viewset.kwargs[user_viewset.lookup_field] = "Test"
        return user_viewset

    def mock_classviewset(self):
        event_viewset = EventViewSet()
        EventViewSet.get_zoom_proxy = MagicMock(return_value=self.mock_zoomproxy())
        return event_viewset

    def mock_zoommeetings_view(self):
        zoom_meetings_view = ZoomMeetingsView()
        return zoom_meetings_view

    def mock_zoommeetings_listview(self):
        zoom_meetings_listview = ZoomMeetingsListView()
        return zoom_meetings_listview

    def mock_classserializer(self, exists=False):
        event_serializer = EventSerializer()
        event_serializer.save = MagicMock(return_value=self.mock_class(exists=exists))
        return event_serializer

    def mock_user(self):
        user = CustomUser()
        return user

    def mock_class(self, exists=False):
        _class = Event()
        if exists:
            _class.meeting_link = TestViews.JOIN_URL
            _class.super_link = TestViews.START_URL
        return _class

    def mock_zoomproxy(self):
        zoom_proxy = ZoomProxy()
        zoom_proxy.create_meeting = MagicMock(return_value=self.mock_zoom_response())
        return zoom_proxy

    def mock_zoom_response(self):
        response = MockRequest()
        response.data["join_url"] = TestViews.JOIN_URL
        response.data["start_url"] = TestViews.START_URL
        return response

    def mock_student_teacher_view(self):
        student_teacher_view = StudentTeacherViewSet()
        student_teacher_view.get_all_users = MagicMock(return_value=self.mock_get_students_teachers())
        return student_teacher_view

    def mock_get_students_teachers(self):
        users = []

        for index in range(TestViews.NUM_STUDENTS):
            student = CustomUser()
            student.role = 'Student'
            student.email_address = 'student@email.com'
            student.first_name = "Little"
            student.last_name = "Student" + str(index)
            users.append(student)

        for index in range(TestViews.NUM_TEACHERS):
            teacher = CustomUser()
            teacher.role = 'Teacher'
            teacher.email_address = 'teacher@email.com'
            teacher.first_name = "Mr./Mrs."
            teacher.last_name = "Teacher" + str(index)
            users.append(teacher)

        return users

    # All tests should start with 'test_'

    def test_userviewset_partial_success(self):
        user_viewset = self.mock_userviewset()
        user_viewset.partial_update(request=MockRequest(), partial=False)
        user_viewset.update.assert_called_with(ANY, partial=True)

    def test_classviewset_perform_create_success(self):
        event_viewset = self.mock_classviewset()
        event_serializer = self.mock_classserializer(exists=False)
        event_viewset.perform_create(event_serializer)
        event_viewset.get_zoom_proxy().create_meeting.assert_called()

    def test_classviewset_perform_create_already_exists(self):
        event_viewset = self.mock_classviewset()
        event_serializer = self.mock_classserializer(exists=True)
        event_viewset.perform_create(event_serializer)
        event_viewset.get_zoom_proxy().create_meeting.assert_not_called()

    def test_zoommeeting_view_proxy_exists(self):
        zoom_meetings_view = self.mock_zoommeetings_view()
        assert zoom_meetings_view.proxy != None

    def test_zoommeeting_list_view_proxy_exists(self):
        zoom_meetings_list_view = self.mock_zoommeetings_listview()
        assert zoom_meetings_list_view.proxy != None

    def test_studentteacher_view_get(self):
        student_teacher_view = self.mock_student_teacher_view()
        result = student_teacher_view.get()
        data = json.loads(result.data['data'])
        assert len(data["teachers"]) == TestViews.NUM_TEACHERS
        assert len(data["students"]) == TestViews.NUM_STUDENTS