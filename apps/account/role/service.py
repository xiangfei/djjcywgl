#!/usr/bin/python 

# -*- coding: utf-8 -*-


'''
Created on 2018年5月9日

@author: xiangfei
'''
from apps.account.account.models import Role
from django.contrib.auth.models import Permission
from apps.account.account.models import User
from django.db import transaction

translate_dict ={'add':'增加','change':'编辑','delete':'删除',
                 'recover':'恢复','view':'查看' ,'disable':'禁用','enable':'启用',"search":'搜索'}


class RoleService(object):
    
    def __init__(self):
        
        pass

    #查看有view权限的contnenttype ,过滤系统表
    #contenttype 过滤 权限
    def get_role_permissions(self,roleid):

        result_list = []
        r = Role.objects.get(pk = roleid)
        role_permisison_list = r.permissions.all()
        possible_permission = Permission.objects.all().filter(codename__icontains = 'view')
        contenttype_list =   [ permission.content_type.id for  permission in possible_permission]
        permission_list = Permission.objects.all().filter(content_type__id__in = contenttype_list)
        temp_map = {}
        result_permission_list = []
        for permission in permission_list:
            permissionname = permission.codename
            module , permissionxx = permissionname.split('_')
            if temp_map.get(permissionxx) == None:
                temp_map[permissionxx] = []
            temp_dict_child = {}
            temp_dict_child['key'] = str(permission.id)
            temp_dict_child['title'] =  translate_dict.get(module , module)
            if  permission in role_permisison_list:
                temp_dict_child['value'] = True
                result_permission_list.append(str(permission.id))
            else:
                temp_dict_child['value'] = False
            temp_map[permissionxx].append(temp_dict_child)
        
        for key , value in temp_map.items():
            result_list.append({key:value})
        return (result_list , result_permission_list)

    def get_user_navigator_permission(self,username):
        user = User.objects.get(username = username)
        role_list = user.groups.all()
        result_list = []
        for role in role_list:
            permission_list =  role.permissions.all()
            for permission in permission_list:
                if permission.codename.find('view_')!=-1:
                    result_list.append(permission.codename)
        # 前台需要判断异常使用
        result_list.append('view_allowed')
        return result_list

    def update_role_permission(self ,roleid , permissionids):
        
        role = Role.objects.get(pk=roleid)
        permission_list = Permission.objects.filter(pk__in=permissionids)
        with transaction.atomic():
            role.permissions.clear()
            for permission in permission_list:
                role.permissions.add(permission)
        
roleservice = RoleService()