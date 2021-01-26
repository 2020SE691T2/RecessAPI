from unittest.mock import MagicMock, ANY
from .models import CustomUser, Class
from .serializers import ClassSerializer
from .views import UserViewSet, ClassViewSet, ZoomMeetingsView, ZoomMeetingsListView
from .test_utilities import MockRequest
from .zoom import ZoomProxy

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test classes should start with 'Test'
class TestViews:

    JOIN_URL = "JOIN_URI"
    START_URL = "START_URI"

    def mock_userviewset(self):
        user_viewset = UserViewSet()
        user_viewset.update = MagicMock(return_value=self.mock_user())
        user_viewset.kwargs = {}
        user_viewset.kwargs[user_viewset.lookup_field] = "Test"
        return user_viewset

    def mock_classviewset(self):
        class_viewset = ClassViewSet()
        ClassViewSet.get_zoom_proxy = MagicMock(return_value=self.mock_zoomproxy())
        return class_viewset

    def mock_zoommeetings_view(self):
        zoom_meetings_view = ZoomMeetingsView()
        return zoom_meetings_view

    def mock_zoommeetings_listview(self):
        zoom_meetings_listview = ZoomMeetingsListView()
        return zoom_meetings_listview

    def mock_classserializer(self, exists=False):
        class_serializer = ClassSerializer()
        class_serializer.save = MagicMock(return_value=self.mock_class(exists=exists))
        return class_serializer

    def mock_user(self):
        user = CustomUser()
        return user

    def mock_class(self, exists=False):
        _class = Class()
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

    # All tests should start with 'test_'

    def test_userviewset_partial_success(self):
        user_viewset = self.mock_userviewset()
        user_viewset.partial_update(request=MockRequest(), partial=False)
        user_viewset.update.assert_called_with(ANY, partial=True)

    def test_classviewset_perform_create_success(self):
        class_viewset = self.mock_classviewset()
        class_serializer = self.mock_classserializer(exists=False)
        class_viewset.perform_create(class_serializer)
        class_viewset.get_zoom_proxy().create_meeting.assert_called()

    def test_classviewset_perform_create_already_exists(self):
        class_viewset = self.mock_classviewset()
        class_serializer = self.mock_classserializer(exists=True)
        class_viewset.perform_create(class_serializer)
        class_viewset.get_zoom_proxy().create_meeting.assert_not_called()

    def test_zoommeeting_view_proxy_exists(self):
        zoom_meetings_view = self.mock_zoommeetings_view()
        assert zoom_meetings_view.proxy != None

    def test_zoommeeting_list_view_proxy_exists(self):
        zoom_meetings_list_view = self.mock_zoommeetings_listview()
        assert zoom_meetings_list_view.proxy != None

