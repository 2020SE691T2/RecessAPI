from rest_framework.permissions import BasePermission,SAFE_METHODS
import logging

class IsOwner(BasePermission):
    logger = logging.getLogger(__name__)

    def has_object_permission(self, request, view, obj):
        IsOwner.logger.info('IsOwner Request User: %s', request.user)
        IsOwner.logger.info('IsOwner View: %s', view)
        IsOwner.logger.info('IsOwner Object: %s', obj)
        return obj==request.user

class IsSuperUser(BasePermission):
    # To be implemented later
    logger = logging.getLogger(__name__)

    def has_object_permission(self, request, view, obj):
        return False
