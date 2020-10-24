from django.contrib.auth.models import User, Group
from rest_framework import serializers
from RecessApplication.models import CustomUser
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'preferred_name', 'password', 'physical_id_num', 'dob','role', 'email_address']

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        print(f'User = {user}')
        if user and user.is_active:
            return user
        raise serializers.ValidationError(f'Unable to log in with provided credentials. user={user}, data={data}')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']