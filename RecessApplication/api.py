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

from .serializers import CustomUserSerializer, LoginUserSerializer, EventSerializer, EventScheduleSerializer, EventEnrollmentSerializer
from .models import EventEnrollment, EventSchedule, Event, EventRosterParticipant


class CreateEventAPI(generics.GenericAPIView):
    
    permission_classes = (IsStaffPermission, )
    logger = logging.getLogger(__name__)
    zoom_proxy = ZoomProxy()
    
    def convertDatetime(self, time_obj):        
        return datetime.fromisoformat('2021-01-01T' + time_obj + ':00')

    def getNextEventId(self):
        '''
        return the 'next' id from ids of type event_id in the database
        '''
        return Event.objects.all().aggregate(Max('event_id'))['event_id__max'] + 1
    
    def getNextScheduleId(self):
        '''
        return the 'next' id from ids of type schedule_id in the database
        '''
        return EventSchedule.objects.all().aggregate(Max('schedule_id'))['schedule_id__max'] + 1
    
    def post(self, request, *args, **kwargs):
        next_event_id = self.getNextEventId()
        event_data = self.saveEvent(request.data, next_event_id)
        if not (event_data):
            return Response({
                "error": "The data was not valid."
            })
        self.saveEventSchedule(request.data, next_event_id)
        return Response({
                "event_id": next_event_id
            })
    
    def saveEvent(self, data, next_event_id):

        week_days = ""
        for i in range(0, len(data['days'])):
            if i != 0 :
                week_days += ", "
            week_days += str(int(data['days'][i]) + 2)
        start = self.convertDatetime(data['start'])
        end = self.convertDatetime(data['end'])
        zoom_data = {
            'topic': data['event_name'],
            'meeting_type': 8,
            'start_time': start,
            'duration': (end - start).total_seconds() / 1000 / 60,
            'weekly_days': week_days
        }
        meeting_json = self.zoom_proxy.create_meeting(zoom_data)
        meeting = meeting_json.data
        args = {
            'event_id' : next_event_id,
            'event_name' : data['event_name'],
            'year' : data['year'],
            'section' : data.get('section',1),
            'meeting_link' : meeting["join_url"],
            'super_link' : meeting["start_url"],
        }
        serializer = EventSerializer(data=args)
        if serializer.is_valid(raise_exception=True):
            return serializer.save()
        return False
    
    def saveEventSchedule(self, data, next_event_id):
        start_time=self.convertDatetime(data['start']).time()
        end_time=self.convertDatetime(data['end']).time()
        for day in data['days']:
            EventSchedule.objects.create(schedule_id=self.getNextScheduleId(), 
                                         event_id=next_event_id, 
                                         weekday=day, 
                                         start_time=start_time,
                                         end_time=end_time)
        return

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
    serializer_class = EventEnrollmentSerializer
    
    def get(self, request):
        user = request.user
        participants = self.getRosterParticipants().filter(email_address=user.email_address).values()

        roster_ids = set()
        for participant in participants: 
            roster_ids.add(participant["roster_id"])    
        enrollments = self.getEventEnrollments().filter(roster_id__in=roster_ids).values()

        if not self.exists(enrollments):
            return Response({
                "error": "User is not enrolled in or teaching any events."
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
            event_year = year
        else:
            event_year = year - 1
        
        event_ids = [ e['event_id'] for e in enrollments ]
        events = self.getEventes().filter(event_id__in=event_ids, year=event_year).values()

        result = []
        if self.exists(events):
            event_schedules = self.getEventSchedules().filter(event_id__in=event_ids).values()    
            
            for cs in event_schedules:
                event_item = next((cl for cl in events if cl['event_id'] == cs['event_id']), {})
                if (not event_item) or (event_item['year'] != event_year): continue
                cs.update(event_item)
                enr_item = next((enr for enr in enrollments if enr['event_id'] == cs['event_id']), {})
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

    def getRosterParticipants(self):
        return EventRosterParticipant.objects

    def getEventEnrollments(self):
        return EventEnrollment.objects

    def getEventes(self):
        return Event.objects
    
    def getEventSchedules(self):
        return EventSchedule.objects

    def getLogger(self):
        return WeeklyScheduleAPI.logger

    def exists(self, obj):
        return obj.exists()
