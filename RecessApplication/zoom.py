import json
import logging
from zoomus import ZoomClient
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

import ast

class ZoomProxy:

    user_id = None
    logger = logging.getLogger(__name__)

    INSTANT_MEETING = 1
    FIXED_MEETING = 2
    RECURRING_MEETING_UNFIXED = 3
    RECURRING_MEETING_FIXED = 8

    RECURRING_MEETING_DAILY = 1
    RECURRING_MEETING_WEEKLY = 2
    RECURRING_MEETING_MONTHLY = 3

    def __init__(self):

        self.client = ZoomClient(settings.ZOOM_KEY, settings.ZOOM_SECRET)

        # Make sure we only do this once
        if (ZoomProxy.user_id == None):
            user_list_response = self.client.user.list()
            user_list = json.loads(user_list_response.content)

            ZoomProxy.user_id = user_list['users'][0]['id']
            ZoomProxy.logger.info("Zoom User ID is %s", ZoomProxy.user_id)

    """
    meeting_type - integer
        1 - Instant meeting
        2 - Fixed meeting
        3 - Recurring meeting with no fixed time
        8 - Recurring meeting with fixed time
        We assume most of our meetings will be type '8' with occasional types '1' and '2'. Will populate some fields automatically based on this value.

    """
    def create_meeting(self, topic, meeting_type=None, start_time=None, duration=None, recurrence_type=None, weekly_days=None, end_times=None, end_date_time=None):
        if meeting_type == None:
            # Default to weekly recurring meeting
            meeting_type = ZoomProxy.RECURRING_MEETING_FIXED
        if recurrence_type == None:
            recurrence_type = ZoomProxy.RECURRING_MEETING_WEEKLY
        if weekly_days == None:
            # Default to M-F
            weekly_days = "2,3,4,5,6" # Monday thru Friday
        if end_times == None and end_date_time == None:
            # Can only use one or the other
            end_times = 50 # Maximum

        ZoomProxy.logger.info("Creating meeting for topic %s, type %s, start time %s", topic, meeting_type, start_time)

        # General scenario - no recurrence
        recurrence = None
        # Top-level settings for all meetings
        settings = {}
        settings["host_video"] = True
        settings["mute_upon_entry"] = True
        settings["auto_recording"] = "none"
        settings["join_before_host"] = False

        # Most likely scenario - Plug in default recurrence parameters
        if meeting_type == ZoomProxy.RECURRING_MEETING_FIXED or meeting_type == ZoomProxy.RECURRING_MEETING_UNFIXED:
            ZoomProxy.logger.info("Creating a recurring fixed meeting - using defaults to have a weekly meeting M-F")
            # Include recurrence settings
            recurrence = {}
            # General recurrence settings
            recurrence["type"] = recurrence_type
            recurrence["repeat_interval"] = 1 # Every week (or day or month)
            # Handle specific settings
            if (recurrence_type == ZoomProxy.RECURRING_MEETING_WEEKLY):
                recurrence["weekly_days"] = weekly_days
            if end_date_time:
                recurrence["end_date_time"] = end_date_time
            else:
                recurrence["end_times"] = end_times

        meeting_create_response = self.client.meeting.create(user_id=ZoomProxy.user_id, topic=topic, type=meeting_type, start_time=start_time, duration=duration, recurrence=recurrence, settings=settings)
        content = self.format_json_output(meeting_create_response.content)

        ZoomProxy.logger.info("Create meeting response (%s): %s", meeting_create_response.status_code, content)
        
        return Response(content, status=meeting_create_response.status_code)

    def delete_meeting(self, meeting_id):

        ZoomProxy.logger.info("Deleting meeting %s", meeting_id)
        if (meeting_id == None):
            return Response("Must provide meeting id path parameter", status=status.HTTP_400_BAD_REQUEST)

        meeting_delete_response = self.client.meeting.delete(id=meeting_id)
        content = self.format_json_output(meeting_delete_response.content)

        ZoomProxy.logger.info("Delete meeting response (%s): %s", meeting_delete_response.status_code, content)
        
        return Response(content, status=meeting_delete_response.status_code)

    def get_meeting(self, meeting_id, occurrence_id=None):
        ZoomProxy.logger.info("Getting meeting for ID %s", meeting_id)
        if (meeting_id == None):
            return Response("Must provide meeting id path parameter", status=status.HTTP_400_BAD_REQUEST)
        show_previous_occurrences = False
        meeting_get_response = self.client.meeting.get(user_id=ZoomProxy.user_id, id=meeting_id, occurrence_id=occurrence_id, show_previous_occurrences=show_previous_occurrences)
        content = self.format_json_output(meeting_get_response.content)

        ZoomProxy.logger.info("Get meeting response (%s): %s", meeting_get_response.status_code, content)
        
        return Response(content, status=meeting_get_response.status_code)

    def list_meetings(self, meeting_type="upcoming"):
        ZoomProxy.logger.info("Getting list meeting for type %s", meeting_type)
        meeting_list_response = self.client.meeting.list(user_id=ZoomProxy.user_id, type=meeting_type)
        content = self.format_json_output(meeting_list_response.content)

        ZoomProxy.logger.info("Get list meeting response (%s): %s", meeting_list_response.status_code, content)
        
        return Response(content, status=meeting_list_response.status_code)

    # Convert byte string to json dictionary for proper API display and formatting
    def format_json_output(self, byte_string):
        dict_str = byte_string.decode("UTF-8")
        # Zoom API returns lower case true and false, Python expects uppercase
        dict_str = dict_str.replace("true", "True")
        dict_str = dict_str.replace("false", "False")
        return ast.literal_eval(dict_str)
