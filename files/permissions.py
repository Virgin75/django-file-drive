from rest_framework import permissions
from django.conf import settings

class IsObjectOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of files or folders to retrieve it.
    """
    message = 'You must be owner of this object.'

    def has_object_permission(self, request, view, obj):
        user = self.request.user
        owner = obj.owner
        return user == owner