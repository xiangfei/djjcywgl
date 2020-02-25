#!/usr/bin/python 
from rest_framework.exceptions import APIException

# -*- coding: utf-8 -*-


'''
Created on 2018年5月9日

@author: xiangfei
'''
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RoleSerializer , EditRoleSerializer
from .service import roleservice
from utils.permissions import check_permission
from utils.token import TokenAuthentication
        
class RolePermissionView(APIView):
    authentication_classes = (TokenAuthentication, )
    serializer_class = RoleSerializer
    
    @check_permission('account.view_permission')
    def post(self, request):
        
        serializer = RoleSerializer(data = request.data)
        if serializer.is_valid():
            result_list , result_permission_list = serializer.get_role_permission()
            return Response({"code":200  ,"data":result_list ,"msg":"success" ,'permission_list':result_permission_list })
        return Response({'code':500,'msg':serializer.errors})
    
    
class EditRolePermissionView(APIView):
    authentication_classes = (TokenAuthentication, )
    
    @check_permission('account.change_permission')
    def post(self, request):
        
        serializer = EditRoleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.update_role_permission()

            return Response({"code":200  ,"msg":"success"})

        return Response({'code':500,'msg':serializer.errors})