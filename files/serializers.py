from .models import File, Folder, SharedWith
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer


class FileSerializer(serializers.ModelSerializer):
    shared_with_users = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            'id', 
            'download_url',
            'created_at', 
            'updated_at', 
            'file_name', 
            'file_type', 
            'file_size', 
            'file', 
            'owner', 
            'parent_folder',
            'shared_with_users'
        ]
        extra_kwargs = {
            'file_type': {'read_only': True},
            'file_size': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'owner': {'read_only': True},
            'file': {'write_only': True},
        }
    
    def get_shared_with_users(self, obj):
        users = SharedWith.objects.filter(file=obj).values('user')
        results = []
        for user in users:
            results.append(user['user'])
        return results

    def get_download_url(self, obj):
        return f"/api/files/{obj.id}/download"

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'folder_name', 'owner', 'parent_folder']
        extra_kwargs = {
            'owner': {'read_only': True}
        }

class ShareWithSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    file = FileSerializer(read_only=True)
    folder = FolderSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        user_to_share = get_user_model().objects.get(
            email=validated_data["email"]
        )
        
        validated_data.pop('email', None)

        return SharedWith.objects.create(
            user=user_to_share, 
            **validated_data
        )