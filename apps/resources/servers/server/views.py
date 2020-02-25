#!/usr/bin/python 
# -*- coding: utf-8 -*-


from rest_framework.views import APIView
from rest_framework.response import Response
from .service import alicloudservice
from .models import Server
from .serializers import ServerDetailSerializer, ServerListSerializer , ServerNoUsageSerializer ,ServerAddSerializer
from .serializers import ServerStopSerializer 
from .serializers import ServerRecoverSerializer
from .serializers import ServerReleaseSerializer
from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework import   status
from jcywgl.settings import   ALICLOUD_ACTION
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from .service import config_dict_list
from .service import bandtype_dict_list
from .service import charging_dict_list
from .service import zone_dict_list
from .service import cycle_dict_list
from .service import server_status_dict
#from .token import TokenAuthentication

from utils.permissions import check_permission , list_permission
from utils.token import TokenAuthentication
from utils.paginators import ServerPagination
from utils.filters import PostSearchFilter

class ServerDictView(APIView):


    def get(self,request):

        
        ret = {'code':200,'msg':None,'data':None}
        security_dict_list = alicloudservice.get_securitygroup_list()
        image_dict_list = alicloudservice.get_image_list("self")
        ret['data'] = [{'bandtype':bandtype_dict_list,'zone':zone_dict_list,
                       'charging':charging_dict_list,'cycle':cycle_dict_list,
                       'config':config_dict_list,'security':security_dict_list,
                       'image':image_dict_list}]
        return Response(ret)


class ServerVPCView(APIView):
    
    def get(self,request):
        ret_data = alicloudservice.get_vpc_vswitch_list()
        ret = {'code':200,'msg':None,'data':ret_data}
        return Response(ret)


class ServerDetailView(APIView):
    
    authentication_classes = (TokenAuthentication, )
    
    @check_permission('server.view_server')
    def post(self,request):
        
        serializer =  ServerDetailSerializer(data = request.data)
        if serializer.is_valid():
            dserializer = serializer.get_server_detail()
            ret = {'code':200,'msg':None,'data':dserializer.data}
            return Response(ret)
        return Response({'code':500,'msg':serializer.errors})



class ServerNousageView(APIView):
    
    def post(self,request):
        
        
        serializer = ServerNoUsageSerializer(data = request.data)
        if serializer.is_valid():
            nousageserializer = serializer.list_no_usage_server()
            ret = {'code':200,'msg':None,'data':nousageserializer.data}
            return Response(ret)
        return Response({'code':500,'msg':serializer.errors})



class  ServerListView(ListModelMixin, GenericAPIView):


    queryset = Server.objects.all()
    serializer_class = ServerListSerializer
    #数据测试需要request.data 组装
    filter_backends = (PostSearchFilter,)
    search_fields = ('name' , 'outterip' ,'innerip' , 'status' ,'usage','env','config','id')
    pagination_class = ServerPagination
    authentication_classes = (TokenAuthentication, )
    
    @check_permission('server.view_server')
    @list_permission
    def post(self , request):
        
        return self.list(request)

class ServerAddView(APIView):

    authentication_classes = (TokenAuthentication, )
    @check_permission('server.add_server')
    def post(self , request):

        pserializer = ServerAddSerializer(data=request.data)
        if pserializer.is_valid():
            pserializer.save()
            return Response({'code':200,'msg':None,'data':pserializer.data})

        return Response({'code':500,'msg':pserializer.errors})

#启动机器
class ServerRecoverView(APIView):


    authentication_classes = (TokenAuthentication, )
    serializer_class = ServerRecoverSerializer
    @check_permission('server.recover_server')
    def post(self,request):
        
        serializer = ServerRecoverSerializer(data = request.data)
        if serializer.is_valid():
            serializer.server_recover(ALICLOUD_ACTION)
            ret = {'code':200,'msg':'success'}
            return Response(ret)
        return Response({'code':500 , 'msg': serializer.errors}) 



#删除机器
class ServerReleaseView(APIView):

    authentication_classes = (TokenAuthentication, )
    serializer_class = ServerReleaseSerializer
    @check_permission('server.delete_server')
    def post(self,request):
        serializer = ServerReleaseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.server_release(ALICLOUD_ACTION)
            ret = {'code':200,'msg':'success'}
            return Response(ret)
        return Response({'code':500 , 'msg': serializer.errors}) 





class ServerStopView(APIView):
    
    authentication_classes = (TokenAuthentication, )
    serializer_class = ServerStopSerializer
    @check_permission('server.stop_server')
    def post(self,request):
        serializer = ServerStopSerializer(data = request.data)
        if serializer.is_valid():
            serializer.stop_server(ALICLOUD_ACTION)
            ret = {'code':200,'msg':'success'}
            return Response(ret)
        return Response({'code':500 , 'msg': serializer.errors}) 
        

#临时同步
class ServerSyncView(APIView):
    
    authentication_classes = (TokenAuthentication, )
    
    def get(self , request):
        
        server_list = alicloudservice.get_server_list()
        for server in server_list:
            
            s = Server()
            s.name = server['name']
            s.outterip = server['publicip']
            s.innerip = server['privateip']
            s.status = server_status_dict.get(server['status'])
            s.security = server['securitygroup']
            s.image = server['serverimage']
            s.bandtype = server['bandtype']
            s.networkband = server['networkband']
            s.config = server['config']
            s.zone = server['zone']
            s.vpc = server['vpcid']
            s.switch = server['vswitchid']
            s.charging  = server['charging']
            s.cycle = server['cycle']
            s.loginuser = 'root'
            s.loginpassword = '123456unused'
            s.serverid = server['serverid']
            if s.switch.find("预发")!=-1:
                s.env ='预发环境'
            else:
                s.env = '正式环境'
            s.save()
            
            
        return Response()
        
