from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from RecessApplication.serializers import CustomUserSerializer, GroupSerializer, CustomClassSerializer
from RecessApplication.models import CustomClass

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
    queryset = CustomClass.objects.all()
    serializer_class = CustomClassSerializer
