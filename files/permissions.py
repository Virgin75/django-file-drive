from rest_framework import permissions
from django.conf import settings

class IsObjectOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of files or folders to retrieve it.
    """
    message = 'You must be owner of this object.'

    def has_object_permission(self, request, view, obj):
        print('aaa')
        user = request.user
        owner = obj.owner
        return user == owner

class IsOwnerOrIsPublic(permissions.BasePermission):
    """
    Object-level permission to only allow owners of files 
    or any users (if file is set to public) to retrieve it.
    > Only owner of file can edit it or delete it.
    """
    message = 'You must either be owner of this object OR the object must be public to perform this action.'

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            user = request.user
            owner = obj.owner
            print(owner, user)

            if user == owner or obj.is_public:
                return True
        
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            user = request.user
            owner = obj.owner

            if user == owner:
                return True

