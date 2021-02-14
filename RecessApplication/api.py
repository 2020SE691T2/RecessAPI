from datetime import datetime
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from .permissions import IsStaffPermission
from rest_framework.response import Response
import logging
import copy
from .zoom import ZoomProxy
from datetime import time

from .serializers import CustomUserSerializer, LoginUserSerializer, ClassSerializer, ClassScheduleSerializer, ClassEnrollmentSerializer
from .models import ClassEnrollment, ClassSchedule, Class

class CreateEventAPI(generics.GenericAPIView):
    permission_classes = (IsStaffPermission, )
    logger = logging.getLogger(__name__)
    zoom_proxy = ZoomProxy()
    
    def convertDatetime(self, time_obj):        
        return datetime.fromisoformat('2021-01-01T' + time_obj + ':00').time()

    def getNextClassId(self):
        '''
        return the 'next' id from ids of type class_id in the database
        '''
        return Class.objects.all().aggregate(Max('class_id'))['class_id__max'] + 1
    
    def getNextScheduleId(self):
        '''
        return the 'next' id from ids of type schedule_id in the database
        '''
        return ClassSchedule.objects.all().aggregate(Max('schedule_id'))['schedule_id__max'] + 1
    
    def post(self, request, *args, **kwargs):
        next_class_id = self.getNextClassId()
        class_data = self.saveClass(request.data, next_class_id)
        class_schedules = self.saveClassSchedule(request.data, next_class_id)
        if not (class_data and class_schedules):
            return Response({
                "error": "The data was not valid."
            })
        return Response({
                "class_id": next_class_id
            })
    
    def saveClass(self, data, next_class_id):
        args = {
                'class_id' : next_class_id,
                'class_name' : data['class_name'],
                'year' : data['year'],
                'section' : data.get('section',1)
                }
        serializer = ClassSerializer(data=args)
        if serializer.is_valid(raise_exception=True):
            cl = serializer.save()
            return cl
        return False
    
    def saveClassSchedule(self, data, next_class_id):
        cl = []
        for day in data['days']:
            args = {
                    'class_id' : next_class_id,
                    'schedule_id' : self.getNextScheduleId(),
                    'weekday' : day,
                    'start_time' : self.convertDatetime(data['start']),
                    'end_time' : self.convertDatetime(data['end'])
                    }
            serializer = ClassScheduleSerializer(data=args)
            if serializer.is_valid(raise_exception=True):
                cl.append(serializer.save())
            else:
                return False
        return cl

    def getLogger(self):
        return CreateEventAPI.logger

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
