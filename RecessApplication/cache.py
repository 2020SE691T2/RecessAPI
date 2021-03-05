from .models import CustomUser
import logging

class TeacherStudentCache():
    data = {}
    logger = logging.getLogger(__name__)

    def initialize(self):

        if not TeacherStudentCache.data:
            TeacherStudentCache.data = {}
            TeacherStudentCache.data['teachers'] = []
            TeacherStudentCache.data['students'] = []

            users = self.get_all_users()

            for user in users:
                self.add_user(user)

        self.logger.info("Cache initialized")

    def add_user(self, user):
        if user.role.lower() == 'teacher':
            TeacherStudentCache.data['teachers'].append(self.encode_user(user))
        elif user.role.lower() == 'student':
            TeacherStudentCache.data['students'].append(self.encode_user(user))

    def encode_user(self, user):
        data = {}
        data["emailaddress"] = user.email_address
        data["firstname"] = user.first_name
        data["lastname"] = user.last_name
        return data

    def get_all_users(self):
        users = CustomUser.objects.all()
        return list(users)

    def get_data(self):
        return TeacherStudentCache.data