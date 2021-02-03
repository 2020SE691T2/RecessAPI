from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging
import copy

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
                "tokens": user.tokens()
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
            enrollments = self.getClassEnrollments().filter(teacher_email=user.email_address).values()
        else:
            enrollments = self.getClassEnrollments().filter(student_email=user.email_address).values()

        if not self.exists(enrollments):
            return Response({
                "error": "User is not enrolled in or teaching any classes."
            })
        
        if not (request.GET.get("year")) :     
            year = datetime.today().isocalendar()[0] # return tuple (year, week number, weekday)
        else:
            year = int(request.GET.get("year")) # https://stackoverflow.com/questions/3711349/django-and-query-string-parameters
        
        if not (request.GET.get("week")) :
            week = datetime.today().isocalendar()[1]
        else:
            week = int(request.GET.get("week"))
        
        if week >= 30:
            class_year = year
        else:
            class_year = year - 1
        
        class_ids = [ e['class_id'] for e in enrollments ]
        classes = self.getClasses().filter(class_id__in=class_ids, year=class_year).values()

        result = []
        if self.exists(classes):
            class_schedules = self.getClassSchedules().filter(class_id__in=class_ids).values()    
            
            for cs in class_schedules:
                class_item = next((cl for cl in classes if cl['class_id'] == cs['class_id']), {})
                if (not class_item) or (class_item['year'] != class_year): continue
                cs.update(class_item)
                enr_item = next((enr for enr in enrollments if enr['class_id'] == cs['class_id']), {})
                cs.update(enr_item)
                for day in self.get_weekday_name(int(cs['weekday'])):
                    cs['weekday'] = day
                    new_cs = copy.deepcopy(cs)       
                    result.append(new_cs)

        return Response({
            "schedules": result
        })
    
    def get_weekday_name(self, nday):
        result = []
        wdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if (nday == -1):
            result = wdays
        else:
            result.append(wdays[nday])
        return result

    def getClassEnrollments(self):
        return ClassEnrollment.objects

    def getClasses(self):
        return Class.objects

    def getClassSchedules(self):
        return ClassSchedule.objects

    def getLogger(self):
        return WeeklyScheduleAPI.logger

    def exists(self, obj):
        return obj.exists()
