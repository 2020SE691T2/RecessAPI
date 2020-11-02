import json
from zoomus import ZoomClient
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class ZoomProxy:

    user_id = None

    def __init__(self):

        self.client = ZoomClient(settings.ZOOM_KEY, settings.ZOOM_SECRET)

        if (ZoomProxy.user_id == None):
            user_list_response = self.client.user.list()
            user_list = json.loads(user_list_response.content)

            # Trying to set it directly ['users][0]['id'] was throwing an error
            # There should only be a single 'users' at the moment
            # Simply grab the first in the list and exit
            #for user in user_list['users']:
            ZoomProxy.user_id = user_list['users'][0]['id']

        print('User ID is', ZoomProxy.user_id)

    """
    meeting_type - integer
        1 - Instant meeting
        2 - Fixed meeting
        3 - Recurring meeting with no fixed time
        8 - Recurring meeting with fixed time
    """
    def create_meeting(self, topic, meeting_type, start_time=None, duration=None):
        meeting_create_response = self.client.meeting.create(user_id=ZoomProxy.user_id, topic=topic, type=meeting_type, start_time=start_time, duration=duration)
        print("You are here")
        print("Type is ", meeting_type)
        print("Start time is ", start_time)
        date_string = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        print("That formatted is ", date_string)
        print(meeting_create_response.content)
        print(meeting_create_response.content, meeting_create_response.status_code)
        
        return Response(meeting_create_response.content, status=meeting_create_response.status_code)

    def get_meeting(self, meeting_id):
        if (meeting_id == None):
            return Response("Must provide meeting id query parameter", status=status.HTTP_400_BAD_REQUEST)
        meeting_get_response = self.client.meeting.get(user_id=ZoomProxy.user_id, id=meeting_id)
        print("You are trying to get a meeting")
        print(meeting_get_response.content)
        print(meeting_get_response.status_code)
        
        return Response(meeting_get_response.content, status=meeting_get_response.status_code)

    def list_meetings(self, type="upcoming"):
        meeting_list_response = self.client.meeting.list(user_id=ZoomProxy.user_id, type=type)
        print("You are trying to list meetings")
        print(meeting_list_response.content)
        print(meeting_list_response.status_code)
        
        return Response(meeting_list_response.content, status=meeting_list_response.status_code)