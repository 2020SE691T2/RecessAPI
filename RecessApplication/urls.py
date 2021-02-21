"""RecessApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from RecessApplication import views
from .api import CreateEventAPI, LoginAPI, RegistrationAPI, WeeklyScheduleAPI
from .views import ChangePasswordView
import logging
from .router import OptionalSlashRouter

router = OptionalSlashRouter()

router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'class_info', views.ClassViewSet)
router.register(r'class_enrollment', views.ClassEnrollmentViewSet)
router.register(r'class_schedule', views.ClassScheduleViewSet)
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'roster', views.RosterViewSet)
router.register(r'roster_participant', views.RosterParticipantViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    re_path(r'^admin/?', admin.site.urls),
    re_path(r'^api-auth/register/?', RegistrationAPI.as_view()),
    re_path(r'^api-auth/auth/?', LoginAPI.as_view()),
    re_path(r'^api-auth/?', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/classes/?', WeeklyScheduleAPI.as_view()),
    re_path(r'^api/create-class/?', CreateEventAPI.as_view()),
    re_path(r'^api/token/new/?', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/token/refresh/?', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^zoom/meetings/(?P<pk>[0-9]+)/?$', views.ZoomMeetingsView.as_view()),
    re_path(r'^zoom/meetings/?', views.ZoomMeetingsListView.as_view()),
    re_path(r'^api/participants/?', views.StudentTeacherViewSet.as_view())
]

static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

logger = logging.getLogger(__name__)
logger.info("----- INITIALIZATION COMPLETE -----")