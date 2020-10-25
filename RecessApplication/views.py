from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from RecessApplication.serializers import CustomUserSerializer, GroupSerializer, CustomClassSerializer
from RecessApplication.models import CustomClass

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
    queryset = CustomClass.objects.all()
    serializer_class = CustomClassSerializer
