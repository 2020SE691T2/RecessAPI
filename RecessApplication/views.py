from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from RecessApplication.serializers import CustomUserSerializer, GroupSerializer, ClassSerializer, ClassEnrollmentSerializer, ClassScheduleSerializer, AssignmentSerializer
from RecessApplication.models import Class, ClassEnrollment, ClassSchedule, Assignment
from .zoom import ZoomProxy
import datetime

import urllib.parse

User = get_user_model()

# View overview
# CreateAPIView - POST
# ListAPIView - GET collection
# RetrieveAPIView - GET single
# DestroyAPIView - DELETE
# UpdateAPIView - PUT and POST single
# ListCreateAPIView - GET and POST
# RetrieveUpdateAPIView - GET and PUT and PATCH single
# RetrieveDestroyAPIView - GET and DELETE single
# RetrieveUpdateDestroyAPIView - GET and PUT and PATCH and DELETE single

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    lookup_value_regex = '[^/]+'
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "email_address"

    """def get_queryset(self):
        email = self.kwargs["email_address"]
        return User.objects.filter(email_address=email) # return a queryset"""

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class ClassEnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows class enrollments to be viewed or edited.
    """
    queryset = ClassEnrollment.objects.all()
    serializer_class = ClassEnrollmentSerializer

class ClassScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows class schedules to be viewed or edited.
    """
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer


class ClassScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows class schedules to be viewed or edited.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class ZoomMeetingsView(APIView):
    """
    Interact with the Zoom Meeting API.
    """
    def __init__(self):
        self.proxy = ZoomProxy()

    def get(self, request, format=None):
        meeting_id = request.query_params.get('meeting_id', None)
        print("Meeting id is ", meeting_id)
        return self.proxy.get_meeting(meeting_id=meeting_id)

    def post(self, request, format=None):
        topic = request.data.get('topic', None)
        type = request.data.get('type', None)
        start_time = request.data.get('start_time', datetime.datetime.now())
        duration = request.data.get('duration', 60)
        return self.proxy.create_meeting(topic=topic, type=type, start_time=start_time, duration=duration)

class ZoomMeetingsListView(APIView):
    """
    Interact with the Zoom Meetings API.
    """
    def __init__(self):
        self.proxy = ZoomProxy()

    def get(self, request, format=None):
        return self.proxy.list_meetings()