#!/usr/bin/python 

# -*- coding: utf-8 -*-

'''
Created on 2018年5月9日

@author: xiangfei
'''


from rest_framework import serializers
from apps.account.account.models import Role
from .service import roleservice


class RoleSerializer(serializers.ModelSerializer):
    
    role_id = serializers.IntegerField(required=True)

    def get_role_permission(self ):
        role_id = self.initial_data['role_id']
        return roleservice.get_role_permissions(role_id)
    
    class Meta:
        model = Role
        
        fields = ('role_id',)
        
        
class EditRoleSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(required=True)
    permission_ids = serializers.ListField(required=True)
    
    def update_role_permission(self):
        role_id = self.initial_data['role_id']
        permission_ids = self.initial_data['permission_ids']
        return roleservice.update_role_permission(role_id, permission_ids)

    class Meta:
        model = Role
        
        fields = ('role_id', 'permission_ids')
