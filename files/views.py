from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import File, Folder
from .serializers import FileSerializer, FolderSerializer

class ListCreateFiles(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = File.objects.filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        # Get file type & save it to db
        file = self.request.data.get("file")
        file_type = file.content_type

        # Get current user & set him/her as file owner
        user = self.request.user

        serializer.save(file_type=file_type, owner=user)

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
