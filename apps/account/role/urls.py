'''
Created on 2018年5月9日

@author: xiangfei
'''
from django.conf.urls import url

from .views import RolePermissionView
from .views import EditRolePermissionView

urlpatterns = [

    url(r'^role/permissionlist/$' , RolePermissionView.as_view()),
    url(r'^role/permissionedit/$' , EditRolePermissionView.as_view()),
]