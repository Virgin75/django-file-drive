from .models import File, Folder
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file_name', 'file_type', 'file', 'owner', 'parent_folder']
        extra_kwargs = {
            'file_type': {'read_only': True},
            'owner': {'read_only': True}
        }

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'folder_name', 'owner', 'parent_folder']
        extra_kwargs = {
            'owner': {'read_only': True}
        }
