from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from RecessApplication.serializers import CustomUserSerializer, GroupSerializer, ClassSerializer, ClassEnrollmentSerializer, ClassScheduleSerializer, AssignmentSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer, ClassRosterSerializer, ClassRosterParticipantSerializer
from RecessApplication.models import Class, ClassEnrollment, ClassSchedule, Assignment, CustomUser, ClassRoster, ClassRosterParticipant
from RecessApplication.permissions import IsOwner
from .cache import TeacherStudentCache
from rest_framework_simplejwt.views import TokenObtainPairView
from .zoom import ZoomProxy
import logging
import json

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
    permission_classes = (IsOwner,)
    lookup_value_regex = '[^/]+'
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "email_address"

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    zoom_proxy = ZoomProxy()

    def perform_create(self, serializer):
        instance = serializer.save()

        if not instance.meeting_link or not instance.super_link:
            data = { "topic": instance.class_name + "-" + instance.section}
            meeting_json = self.get_zoom_proxy().create_meeting(data)
            meeting = meeting_json.data

            serializer.save(meeting_link=meeting["join_url"], super_link=meeting["start_url"])
    
    def get_zoom_proxy(self):
            return ClassViewSet.zoom_proxy

class ClassEnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows class enrollments to be viewed or edited.
    """
    queryset = ClassEnrollment.objects.all()
    lookup_field = "enrollment_id"
    serializer_class = ClassEnrollmentSerializer
    logger = logging.getLogger(__name__)

    def get_queryset(self):
        user = self.request.user
        roster_participants = ClassRosterParticipant.objects.filter(email_address=user.email_address)
        roster_ids = []
        for participant in roster_participants:
            roster_ids.append(participant.roster_id)
        objects = ClassEnrollment.objects.filter(roster_id__in=user.email_address)
        ClassEnrollmentViewSet.logger.info("User: %s", user.email_address)
        return objects

class RosterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rosters to be viewed or edited.
    """
    queryset = ClassRoster.objects.all()
    serializer_class = ClassRosterSerializer
    logger = logging.getLogger(__name__)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class RosterParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rosters to be viewed or edited.
    """
    queryset = ClassRosterParticipant.objects.all()
    serializer_class = ClassRosterParticipantSerializer
    logger = logging.getLogger(__name__)

class ClassScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows class schedules to be viewed or edited.
    """
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows class schedules to be viewed or edited.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class StudentTeacherViewSet(APIView):
    """
    Returns all teachers and students in separate lists
    """

    teacher_student_cache = TeacherStudentCache()

    def get(self, format=None):
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'data': json.dumps(self.teacher_student_cache.get_data())
        }

        return Response(response)

class ZoomMeetingsView(APIView):
    """
    Interact with the Zoom Meeting API.
    """
    def __init__(self):
        self.proxy = ZoomProxy()

    def get(self, request, pk, format=None):
        return self.proxy.get_meeting(meeting_id=pk)

    def delete(self, request, pk, format=None):
        return self.proxy.delete_meeting(meeting_id=pk)

class ZoomMeetingsListView(APIView):
    """
    Interact with the Zoom Meetings API.
    """
    def __init__(self):
        self.proxy = ZoomProxy()

    def get(self, request, format=None):
        return self.proxy.list_meetings()

    def post(self, request, format=None):
        return self.proxy.create_meeting(request.data)