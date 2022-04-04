from ast import keyword
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from collections import namedtuple


from rest_framework import generics, views, mixins, response, status
from rest_framework.permissions import IsAuthenticated

from config.settings import CORS_ALLOWED_ORIGINS
from .models import File, Folder, SharedWith
from users.models import CustomUser
from .serializers import FileSerializer, FolderSerializer, ShareWithSerializer, FolderWithContentSerializer, SearchResultsSerializer
from .permissions import IsObjectOwner, IsOwnerOrIsPublic, IsAllowedToAccessObject, CanWriteToFolderObject
from .tasks import generate_thumbnail

class ListCreateFiles(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, CanWriteToFolderObject]

    def get_queryset(self):
        user = self.request.user
        queryset = File.objects.filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        # Get file type/size & save it to db
        file = self.request.data.get("file")
        file_type = file.content_type
        file_size = file.size / 1000000
        file_name = file._get_name()

        # Get current user & set him/her as file owner
        user = self.request.user

        # If no parent folder is defined, set root as parent folder
        if self.request.data.get("parent_folder") is None:
            parent_folder = Folder.objects.get(root_folder=True, owner=user)
            file_obj = serializer.save(
            file_type=file_type, 
            file_size=file_size,
            file_name=file_name,
            parent_folder=parent_folder,
            owner=user
        )
        else:
            file_obj = serializer.save(
                file_type=file_type, 
                file_size=file_size,
                file_name=file_name,
                owner=user
            )

        #Celery task to generate the thumbnail
        generate_thumbnail.delay(
            file_obj.file.name, 
            file_obj.id,
            file_obj.file_type
            )

class DownloadFile(views.APIView):
    permission_classes = [IsOwnerOrIsPublic|IsAllowedToAccessObject]

    def get_queryset(self):
        id = self.kwargs['pk']
        file = File.objects.filter(id=id)
        return file
    
    def get(self, request, pk, format=None):
        """
        Download the file.
        """
        file = File.objects.get(id=pk)
        self.check_object_permissions(request, file)
        res = HttpResponse(status=200)
        res['Access-Control-Allow-Origin'] = '*'
        res['Content-Type'] = ''
        res["Content-Disposition"] = f"attachment; filename={file.file_name}"
        res['X-Accel-Redirect'] = f"/protected/{file.file.name[8:]}"
        return res

class RetrieveUpdateDestroyFile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    permission_classes = [IsOwnerOrIsPublic|IsAllowedToAccessObject]
    lookup_field = 'pk'


class ShareFile(
    generics.GenericAPIView, 
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
    ):
    permission_classes = [IsObjectOwner]
    serializer_class = ShareWithSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except IntegrityError:
            content = {'error': 'This file has already been shared with this user.'}
            return response.Response(content, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            content = {'error': 'This user does not exist.'}
            return response.Response(content, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        file_pk = self.kwargs.get("pk")
        file = get_object_or_404(File, id=file_pk)
        self.check_object_permissions(self.request, file)
        serializer.save(file=file)
        
    def destroy(self, request, *args, **kwargs):
        file_pk = self.kwargs.get("pk")
        file = get_object_or_404(File, id=file_pk)
        self.check_object_permissions(request, file)
        user_with_access = get_user_model().objects.get(
            email=request.data['email']
        )
        instance = SharedWith.objects.get(file=file, user=user_with_access)
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)



class ShareFolder(
    generics.GenericAPIView, 
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
    ):
    permission_classes = [IsObjectOwner]
    serializer_class = ShareWithSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except IntegrityError:
            content = {'error': 'This folder has already been shared with this user.'}
            return response.Response(content, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            content = {'error': 'This user does not exist.'}
            return response.Response(content, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        folder_pk = self.kwargs.get("pk")
        folder = get_object_or_404(Folder, id=folder_pk)
        self.check_object_permissions(self.request, folder)
        serializer.save(folder=folder)
    
    def destroy(self, request, *args, **kwargs):
        folder_pk = self.kwargs.get("pk")
        folder = get_object_or_404(Folder, id=folder_pk)
        self.check_object_permissions(request, folder)
        user_with_access = get_user_model().objects.get(
            email=request.data['email']
        )
        instance = SharedWith.objects.get(folder=folder, user=user_with_access)
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ListContentSharedWithMe(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShareWithSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = SharedWith.objects.filter(user=user)
        return queryset


class ListCreateFolders(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Folder.objects.filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        # Get current user & set him/her as file owner
        user = self.request.user
        serializer.save(owner=user)

class RetrieveUpdateDestroyFolder(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = [IsObjectOwner|IsAllowedToAccessObject]
    lookup_field = 'pk'

    #Override destroy to prevent deletion of root folder
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.root_folder == False:
            self.perform_destroy(instance)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response({'error': 'root folder cannot be deleted'})


class RetrieveContentInFolder(generics.RetrieveAPIView):
    serializer_class = FolderWithContentSerializer
    permission_classes = [IsObjectOwner|IsAllowedToAccessObject]
    lookup_field = 'pk'
    queryset = Folder.objects.all()


class SearchFilesAndFolders(generics.ListAPIView):
    serializer_class = SearchResultsSerializer
    queryset = File.objects.all()

    def list(self, request):
        user = self.request.user
        file_queryset = File.objects.filter(owner=user)
        folder_queryset = Folder.objects.filter(owner=user)
        keyword = request.query_params.get('keyword')

        serializer = self.get_serializer({'files': file_queryset, 'folders': folder_queryset})

        if keyword:
            file_queryset = file_queryset.filter(file_name__icontains=keyword)
            folder_queryset = folder_queryset.filter(folder_name__icontains=keyword)
            serializer = self.get_serializer({'files': file_queryset, 'folders': folder_queryset})

        return response.Response(serializer.data)

