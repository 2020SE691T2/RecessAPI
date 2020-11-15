from django.contrib.auth.models import User, Group
from rest_framework import serializers
from RecessApplication.models import CustomUser, Class, ClassEnrollment, ClassSchedule, Assignment
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email_address', 'first_name', 'last_name', 'preferred_name', 'password', 'physical_id_num', 'dob','role', 'photo', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginUserSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email_address'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError(f'Unable to log in with provided credentials. user={user}, data={data}')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Class
        fields = ['class_id', 'class_name', 'meeting_link', 'year', 'section']

class ClassEnrollmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClassEnrollment
        fields = ['class_id', 'teacher_email', 'student_email']

class ClassScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = ['class_id', 'date', 'start_time', 'end_time']

class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assignment
        fields = ['assignment_id', 'name', 'description', 'assigned_date', 'due_date', 'class_id']