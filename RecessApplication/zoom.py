import json
import logging
from zoomus import ZoomClient
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import datetime

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

    def get_client(self):
        return self.client

    """
    meeting_type - integer
        1 - Instant meeting
        2 - Fixed meeting
        3 - Recurring meeting with no fixed time
        8 - Recurring meeting with fixed time
        We assume most of our meetings will be type '8' with occasional types '1' and '2'. Will populate some fields automatically based on this value.

    """
    def create_meeting(self, data):

        defaults = self.set_meeting_defaults(data)
        topic = defaults["topic"]
        meeting_type = defaults["meeting_type"]
        start_time = defaults["start_time"]
        duration = defaults["duration"]
        recurrence_type = defaults["recurrence_type"]
        weekly_days = defaults["weekly_days"]
        end_time = defaults["end_time"]
        end_date_time = defaults["end_date_time"]

        if meeting_type == None:
            # Default to weekly recurring meeting
            meeting_type = ZoomProxy.RECURRING_MEETING_FIXED
        if recurrence_type == None:
            recurrence_type = ZoomProxy.RECURRING_MEETING_WEEKLY
        if weekly_days == None:
            # Default to M-F
            weekly_days = "2,3,4,5,6" # Monday thru Friday

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
            if end_time:
                recurrence["end_time"] = end_time
            else:
                recurrence["end_date_time"] = end_date_time

        meeting_create_response = self.get_client().meeting.create(user_id=ZoomProxy.user_id, topic=topic, type=meeting_type, start_time=start_time, duration=duration, recurrence=recurrence, settings=settings)
        content = self.format_json_output(meeting_create_response.content)

        ZoomProxy.logger.info("Create meeting response (%s): %s", meeting_create_response.status_code, content)
        
        return Response(content, status=meeting_create_response.status_code)

    def set_meeting_defaults(self, data):
        defaults = {}
        defaults["topic"] = data.get('topic', None)
        defaults["meeting_type"] = data.get('meeting_type', None)
        defaults["start_time"] = data.get('start_time', datetime.datetime.now() + datetime.timedelta(days=7))
        defaults["duration"] = data.get('duration', 60)
        defaults["recurrence_type"] = data.get('recurrence_type', None)
        defaults["weekly_days"] = data.get('weekly_days', None)
        defaults["end_time"] = data.get('end_time', None)
        defaults["end_date_time"] = data.get('end_date_time', self.default_end_datetime(data.get('year')))
        return defaults

    def delete_meeting(self, meeting_id):

        ZoomProxy.logger.info("Deleting meeting %s", meeting_id)
        if (meeting_id == None):
            return Response("Must provide meeting id path parameter", status=status.HTTP_400_BAD_REQUEST)

        meeting_delete_response = self.get_client().meeting.delete(id=meeting_id)
        content = self.format_json_output(meeting_delete_response.content)

        ZoomProxy.logger.info("Delete meeting response (%s): %s", meeting_delete_response.status_code, content)
        
        return Response(content, status=meeting_delete_response.status_code)

    def get_meeting(self, meeting_id, occurrence_id=None):
        ZoomProxy.logger.info("Getting meeting for ID %s", meeting_id)
        if (meeting_id == None):
            return Response("Must provide meeting id path parameter", status=status.HTTP_400_BAD_REQUEST)
        show_previous_occurrences = False
        meeting_get_response = self.get_client().meeting.get(user_id=ZoomProxy.user_id, id=meeting_id, occurrence_id=occurrence_id, show_previous_occurrences=show_previous_occurrences)
        content = self.format_json_output(meeting_get_response.content)

        ZoomProxy.logger.info("Get meeting response (%s): %s", meeting_get_response.status_code, content)
        
        return Response(content, status=meeting_get_response.status_code)

    def list_meetings(self, meeting_type="upcoming"):
        ZoomProxy.logger.info("Getting list meeting for type %s", meeting_type)
        meeting_list_response = self.get_client().meeting.list(user_id=ZoomProxy.user_id, type=meeting_type)
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

    def default_end_datetime(self, year):
        # Default to current year
        if year is None:
            now = datetime.datetime.now()
            year = now.year
            # For early months of the year, use the previous year
            # e.g. in January the year is 2021 but the school year is 2020
            if (now.month < 6):
                year = year - 1

        result = {}
        result[2019] = datetime.datetime(2020, 6, 1)
        result[2020] = datetime.datetime(2021, 6, 1)
        result[2021] = datetime.datetime(2022, 6, 1)

        return result[int(year)]
