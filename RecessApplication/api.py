from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging

from .serializers import CustomUserSerializer, LoginUserSerializer, ClassScheduleSerializer

class RegistrationAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
    logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs): # need all args for registering a user
        RegistrationAPI.logger.info("Getting information for %s", request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Add the special fields not invluded in the CustomUser Model
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

class LoginAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer
    logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs):
        LoginAPI.logger.info("Logging in %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = serializer.validated_data
        LoginAPI.logger.info("Logged in as user %s", user)
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "tokens": tokens
        })

class WeeklyScheduleAPI(generics.GenericAPIView):
    logger = logging.getLogger(__name__)

    def get(self, request):
        WeeklyScheduleAPI.logger.info("Request Info: %s", dir(self.request))
        WeeklyScheduleAPI.logger.info("Request Auth: %s", self.request.auth)
        WeeklyScheduleAPI.logger.info("Request User: %s", self.request.user)
        return Response({
            "user": "test",
        })
