from rest_framework import permissions
from django.conf import settings
from .models import SharedWith

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

class IsAllowedToAccessObject(permissions.BasePermission):
    """
    Object-level permission to allow people that have been
    shared access to a file or a folder to access it.
    """
    def has_object_permission(self, request, view, obj):
        user_requesting_access = request.user

        if(type(obj).__name__ == 'File'):
            file_shared_with = SharedWith.objects.filter(file=obj)
            for person in file_shared_with:
                if person.user == user_requesting_access:
                    return True
        
        if(type(obj).__name__ == 'Folder'):
            folder_shared_with = SharedWith.objects.filter(folder=obj)
            for person in folder_shared_with:
                if person.user == user_requesting_access:
                    return True
        
        return False