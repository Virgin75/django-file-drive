from .models import File
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file_name', 'file_type', 'file', 'owner']
        extra_kwargs = {
            'file_type': {'read_only': True},
            'owner': {'read_only': True}
        }
