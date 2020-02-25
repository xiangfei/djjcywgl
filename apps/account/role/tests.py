#!/usr/bin/python 

# -*- coding: utf-8 -*-

from django.test import TestCase
from rest_framework.test import APIRequestFactory


from .views import RolePermissionView
from .views import EditRolePermissionView
# Create your tests here.


class PermissionTestCase(TestCase):
    fixtures = ['role.yaml']
    def setUp(self):
        
        self.factory = APIRequestFactory()
        self.csrftoken = "1qaz@wsx3edc4rfv" 
    
#     def test_main(self):
#         self._test_001_create_server()
#         self._test_002_get_server_list()
    
    def test_001_get_role_permission(self):
        data = {

            "role_id":"1"
            }
        
        
        request = self.factory.post('role/role/permissionlist' , data ,format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view  = RolePermissionView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200
        
    
    def test_002_assigin_role_permission(self):
         
        data = {
 
            "role_id":"1",
            "permission_ids":[1,2,3]
        }
 
        request = self.factory.post('role/role/permissionedit' , data ,format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view  = EditRolePermissionView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200



