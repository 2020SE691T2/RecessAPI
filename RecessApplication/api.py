from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from .serializers import CustomUserSerializer, LoginUserSerializer

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs): # need all args for registering a user
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
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = serializer.validated_data
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "tokens": tokens
        })