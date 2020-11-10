from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
import logging

from .serializers import CustomUserSerializer, LoginUserSerializer

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs): # need all args for registering a user
        RegistrationAPI.logger.info("Getting information for %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        RegistrationAPI.logger.info("Created user %s", user)
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs):
        LoginAPI.logger.info("Logging in %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        LoginAPI.logger.info("Logged in as user %s", user)
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
        })