from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging

from .serializers import CustomUserSerializer, LoginUserSerializer, ClassScheduleSerializer, ClassEnrollmentSerializer
from .models import ClassEnrollment, ClassSchedule, Class

class RegistrationAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
    logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs): # need all args for registering a user
        self.getLogger().info("Getting information for %s", request.data)
        serializer = self.get_serializer(data=request.data)
        # Don't raise exception since we're responding with an error Response
        if serializer.is_valid(raise_exception=False):
            # Add the special fields not included in the CustomUser Model
            special_fields = {'password': request.data['password']}
            if 'is_staff' in request.data.keys() and request.data['is_staff'] == True:
                special_fields['is_staff'] = True
            if 'is_superuser' in request.data.keys() and request.data['is_superuser'] == True:
                special_fields['is_superuser'] = True
            user = serializer.custom_save( **special_fields )
            return Response({
                "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            })
        return Response({
            "error": "The data was not valid."
        })

    def getLogger(self):
        return RegistrationAPI.logger

class LoginAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer
    logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs):
        self.getLogger().info("Logging in %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = serializer.validated_data
        self.getLogger().info("Logged in as user %s", user)
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "tokens": tokens
        })

    def getLogger(self):
        return LoginAPI.logger

class WeeklyScheduleAPI(generics.GenericAPIView):
    logger = logging.getLogger(__name__)
    serializer_class = ClassEnrollmentSerializer

    def get(self, request):
        user = request.user
        if user.is_staff:
            enrollments = ClassEnrollment.objects.filter(teacher_email=user.email_address).values()
        else:
            enrollments = ClassEnrollment.objects.filter(student_email=user.email_address).values()
        
        if not enrollments.exists():
            return Response({
                "error": "User is not enrolled in or teaching any classes."
            })
        
        class_ids = [ e['class_id'] for e in enrollments ]
        classes = Class.objects.filter(class_id__in=class_ids).values()
        class_schedules = ClassSchedule.objects.filter(class_id__in=class_ids).values()
        
        for schedule in class_schedules:
            schedule['start_time'] = datetime(schedule['date'].year, schedule['date'].month, schedule['date'].day, schedule['start_time'])
            schedule['end_time'] = datetime(schedule['date'].year, schedule['date'].month, schedule['date'].day, schedule['end_time'])

        for cs in class_schedules:
            class_item = next((cl for cl in classes if cl['class_id'] == cs['class_id']), {})
            cs.update(class_item)
            enr_item = next((enr for enr in enrollments if enr['class_id'] == cs['class_id']), {})
            cs.update(enr_item)

        return Response({
            "schedules": class_schedules
        })
