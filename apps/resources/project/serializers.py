from django.contrib.auth.models import User, Group
from .models import ProjectRecord, ModuleRecord
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProjectRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectRecord
        fields = '__all__'


class ModuleRecordSerializer(serializers.ModelSerializer):
    child_of_project = ProjectRecordSerializer()

    class Meta:
        model = ModuleRecord
        fields = '__all__'

