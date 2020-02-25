from rest_framework import serializers

from .models import User, Role 
import sequences


sequences.apps.AppConfig

class UsersSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='user_ptr_id')
    class Meta:
        model = User
        fields = ('id', 'username', 'chinese_name', 'mobile', 'is_active', 'role')
        ordering = ['id']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'role_desc')
        ordering = ['id']

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
    
