from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from RecessApplication.models import CustomUser, Class, ClassEnrollment, ClassSchedule, Assignment, ClassRoster, ClassRosterParticipant
from django.contrib.auth import authenticate
from django.db.models import Max

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email_address', 'first_name', 'last_name', 'preferred_name', 'physical_id_num', 'dob','role', 'photo', 'is_staff', 'is_superuser']
        read_only_fields = ['is_staff', 'is_superuser']
        write_only_fields = ['password']

    def create(self, validated_data):
        print(validated_data)
        return CustomUser.objects.create_user(validated_data.pop('password'), **validated_data)

    def create_superuser(self, validated_data):
        return CustomUser.objects.create_superuser(validated_data.pop('password'), **validated_data)
        
    def custom_save(self, **kwargs):
        # These asserts are included in the built-in save() function in Django, we should keep them in our custom save function.
        assert hasattr(self, '_errors'), ('You must call `.is_valid()` before calling `.save()`.')
        assert not self.errors, ('You cannot call `.save()` on a serializer with invalid data.')
        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. ")

        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, ('`update()` did not return an object instance.')
        elif 'is_superuser' in self.validated_data.keys() and self.validated_data['is_superuser'] == True:
            self.instance = self.create_superuser(validated_data)
            assert self.instance is not None, ('`create_superuser()` did not return an object instance.')
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, ('`create()` did not return an object instance.')

        return self.instance

class LoginUserSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get('email_address', ''), password=data.get('password', ''))
        if user and user.is_active:
            return user, user.tokens()
        raise exceptions.AuthenticationFailed(f'Unable to log in with provided credentials.')

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass
        else:
            request_data = json.loads(request.body)
            email_address = request_data.get("email_address")
            profile_has_expired = False
            try:
                user = CustomUser.objects.get(email_address=email_address)
            except CustomUser.DoesNotExist:
                profile_has_expired = True
            else:
                profile_has_expired = dt.date.today() > profile.expires_on
            finally:
                if profile_has_expired:
                    error_message = "This profile has expired"
                    error_name = "expired_profile"
                    raise exceptions.AuthenticationFailed(error_message, error_name)
        return super().validate(attrs)

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ClassEnrollmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClassEnrollment
        fields = ['enrollment_id', 'event_id', 'roster_id']

class ClassScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = ['event_id', 'schedule_id', 'weekday', 'start_time', 'end_time']

class ClassSerializer(serializers.HyperlinkedModelSerializer):
    class_schedule = ClassScheduleSerializer(source='event', many=True, read_only=True, required=False)
    class_enrollment = ClassEnrollmentSerializer(source='enrollment', many=True, read_only=True, required=False)
    
    class Meta:
        model = Class
        fields = ['event_id', 'class_name', 'meeting_link', 'year', 'section', 'class_schedule', 'class_enrollment']
        read_only_fields = ['event_id']
        lookup_field = 'event_id'
        

class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assignment
        fields = ['assignment_id', 'name', 'description', 'assigned_date', 'due_date', 'event_id']

class ClassRosterParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRosterParticipant
        fields = ['roster_id', 'email_address']

class ClassRosterSerializer(serializers.ModelSerializer):
    participants = ClassRosterParticipantSerializer(many=True)
    
    class Meta:
        model = ClassRoster
        fields = ['roster_id', 'roster_name', 'participants']
        read_only_fields = ['roster_id']
    
    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        roster_id = ClassRoster.objects.aggregate(Max('roster_id'))['roster_id__max']
        
        if roster_id is None:
            roster_id = 0
        roster_id = roster_id + 1
        
        roster = ClassRoster.objects.create(roster_id=roster_id, **validated_data)
        participant_id = ClassRosterParticipant.objects.aggregate(Max('participant_id'))['participant_id__max']
        if participant_id is None:
            participant_id = 0
        
        for participant in participants_data:
            participant_id = participant_id + 1
            ClassRosterParticipant.objects.create(participant_id=participant_id, roster_id=roster_id, **participant)
        return roster