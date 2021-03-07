from unittest.mock import MagicMock
from .test_utilities import MockResponse
from .zoom import ZoomProxy
from zoomus import ZoomClient
from rest_framework import status

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test events should start with 'Test'
class TestZoom:
    FAKE_SECRET = "SECRET"
    STATUS_SUCCESS = 200
    MEETING_ID = 1

    def mock_zoom(self):
        zoom = ZoomProxy()
        zoom.get_client = MagicMock(return_value=self.mock_zoom_client())
        return zoom

    def mock_zoom_client(self):
        client = ZoomClient(TestZoom.FAKE_SECRET, TestZoom.FAKE_SECRET)
        client.meeting.create = MagicMock(return_value=self.mock_response())
        client.meeting.delete = MagicMock(return_value=self.mock_response())
        client.meeting.get = MagicMock(return_value=self.mock_response())
        client.meeting.list = MagicMock(return_value=self.mock_response())
        return client

    def mock_response(self):
        response = MockResponse()
        response.status_code = TestZoom.STATUS_SUCCESS
        return response

    # All tests should start with 'test_'

    # ZoomProxy

    def test_init(self):
        zoom = ZoomProxy()
        assert zoom.client != None
        assert zoom.user_id != None

    def test_create_meeting_success(self):
        zoom = self.mock_zoom()
        result = zoom.create_meeting(data={})
        zoom.get_client().meeting.create.assert_called()
        assert result.status_code == TestZoom.STATUS_SUCCESS

    # TODO: Potentially add a test with more specific input and check call to create()

    def test_delete_meeting_success(self):
        zoom = self.mock_zoom()
        result = zoom.delete_meeting(meeting_id=TestZoom.MEETING_ID)
        zoom.get_client().meeting.delete.assert_called_with(id=TestZoom.MEETING_ID)
        assert result.status_code == TestZoom.STATUS_SUCCESS

    def test_delete_meeting_failure(self):
        zoom = self.mock_zoom()
        result = zoom.delete_meeting(meeting_id=None)
        zoom.get_client().meeting.delete.assert_not_called()
        assert result.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_meeting_success(self):
        zoom = self.mock_zoom()
        result = zoom.get_meeting(meeting_id=TestZoom.MEETING_ID)
        zoom.get_client().meeting.get.assert_called()
        assert result.status_code == TestZoom.STATUS_SUCCESS

    def test_get_meeting_failure(self):
        zoom = self.mock_zoom()
        result = zoom.get_meeting(meeting_id=None)
        zoom.get_client().meeting.get.assert_not_called()
        assert result.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_meeting_success(self):
        zoom = self.mock_zoom()
        result = zoom.list_meetings()
        zoom.get_client().meeting.list.assert_called()
        assert result.status_code == TestZoom.STATUS_SUCCESS

    # TODO: Somewhat more generic tests to add

    # set_meeting_defaults
        # Empty input, default output
        # Filled in input, matching output
        # Mix-n-match
    # format_json_output
        # Figure out why the delete is throwing an error
