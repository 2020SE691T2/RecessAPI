from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from RecessApplication.serializers import CustomUserSerializer, GroupSerializer, ClassSerializer, ClassEnrollmentSerializer, ClassScheduleSerializer, AssignmentSerializer
from RecessApplication.models import Class, ClassEnrollment, ClassSchedule, Assignment

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
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

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