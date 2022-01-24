from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import File, Folder
from .serializers import FileSerializer, FolderSerializer
from .permissions import IsObjectOwner, IsOwnerOrIsPublic

class ListCreateFiles(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

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

        serializer.save(
            file_type=file_type, 
            file_size=file_size,
            file_name=file_name, 
            owner=user
        )

class RetrieveUpdateDestroyFile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    permissions_classes = [IsOwnerOrIsPublic]
    lookup_field = 'pk'

    

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

#TODO:Check if requester is owner of folder & files OR some has shared it with him/her
class RetrieveFilesInFolder(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

    def get_queryset(self):
        files_in_folder = File.objects.filter(
            parent_folder=self.kwargs['pk']
        )
        return files_in_folder
