from rest_framework import serializers

from .models import EnvType, EnvFile


class EnvTypeSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(source='id')
    env_name = serializers.CharField(source='environ_name')

    class Meta:
        model = EnvType
        fields = ('env_name', 'desc', 'env_id', 'file_id')
        ordering = ['env_id']


class EnvFileSerializer(serializers.ModelSerializer):
    file_id = serializers.IntegerField(source='id')

    class Meta:
        model = EnvFile
        fields = ('file_id', 'file_name', 'file_url')
        ordering = ['file_id']
