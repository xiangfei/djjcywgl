# Create your views here.
#coding=utf-8

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Asset
from .filter import AssetFilter
from .serializers import AssetSerializer, AssetAddSerializer, AssetAllSerializer, AssetUpdateSerializer, AssetNotOnLineSerializer, AssetPhysicalSerializer
from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework import status
from jcywgl.settings import DEBUG
from django.core.mail import EmailMessage
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from utils.token import TokenAuthentication
from utils.paginators import ServerPagination, NewServerPagination
from utils.filters import PostSearchFilter, POSTDjangoFilterBackend
import operator
from .service import record_log, excel_upload, data_download
from django.shortcuts import HttpResponse
from django.utils.encoding import escape_uri_path
from datetime import datetime, timedelta
import time
from django.conf import settings
from utils.response_tools import ResponseCode
from .serializers import dic_search, get_dictdata, get_dictvalue, ENV_NODE
import json

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.126.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'jcgrouptest@126.com'
EMAIL_HOST_PASSWORD = 'JC@group'
DEFAULT_FROM_EMAIL = 'jcgroup'


def mails(subject, message, from_email='jcgrouptest@126.com', recipient_list=['H000011@jcgroup.com.cn']):

    msg = EmailMessage(subject, message, from_email, recipient_list)
    msg.content_subtype = "html"
    msg.send()


class ServerListView(ListModelMixin, GenericAPIView):

    authentication_classes = (TokenAuthentication,)

    queryset = Asset.objects.all().order_by('id')
    serializer_class = AssetAllSerializer
    pagination_class = NewServerPagination
    filter_backends = (PostSearchFilter, POSTDjangoFilterBackend)
    filter_class = AssetFilter
    search_fields = ("manageip", "switchip", "hostuser", "svrname", "svrip", "svrsn",
                     "eqsname", "svrfirstusetime", "svrstoptime", "svrofftime", "strdescription",)

    def post(self, request):
        serverid = request.data['svrenv']
        if serverid == '0':
            self.queryset = Asset.objects.all()
            self.serializer_class = AssetAllSerializer
        elif serverid == '1':
            self.queryset = Asset.objects.filter(onoffline=False).filter(svrchangenid__isnull=True)
            self.serializer_class = AssetAllSerializer
        elif serverid == '2':
            self.queryset = Asset.objects.filter(onoffline=True).filter(svrchangenid__isnull=True)
            self.serializer_class = AssetAllSerializer
        elif serverid == '3' or serverid == '4' or serverid == '5' or serverid == '6' or serverid == '7':
            evnname = ENV_NODE[serverid]
            serverenvid = get_dictvalue(evnname)
            self.queryset = Asset.objects.filter(svrchangenid=str(serverenvid))
            self.serializer_class = AssetAllSerializer
        elif serverid == '8':
            evnname = ENV_NODE[serverid]
            serverenvid = get_dictvalue(evnname)
            self.queryset = Asset.objects.filter(svrabandon=True).filter(svrchangenid=str(serverenvid))
            self.serializer_class = AssetAllSerializer
        elif serverid == '9':
            evnname = ENV_NODE[serverid]
            serverenvid = get_dictvalue(evnname)
            self.queryset = Asset.objects.filter(svrabandon=False).filter(svrchangenid=str(serverenvid))
            self.serializer_class = AssetAllSerializer
        else:
            return Response({'code': 500, 'msg': 'error', 'data': 'svrenv error'})
        return self.list(request)


class ServerAddView(APIView):

    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        assetsn = request.data['svrsn']
        try:
            asset = Asset.objects.get(svrsn=assetsn)
        except:
            asset = ''
        if asset:
            return Response({'code': 500, 'msg': 'same sn'})

        pserializer = AssetAddSerializer(data=request.data)
        if pserializer.is_valid():
            pserializer.save()
            return Response({'code': 200, 'msg': None, 'data': pserializer.data})

        return Response({'code': 500, 'msg': pserializer.errors})


class ServerUpdateView(APIView):

    authentication_classes = (TokenAuthentication,)

    @record_log('physical')
    def post(self, request):
        assetid = request.data['id']
        print (request.data)

        try:
            status = request.data['status']
        except:
            status = ''
        try:
            svrabandon = request.data['svrabandon']
        except:
            svrabandon = ''
        try:
            onoffline = request.data['onoffline']
        except:
            onoffline = ''
        if status:
            if request.data['status'] == '下线':
                serverenvid = get_dictvalue('下线')
                request.data['svrchangenid'] = serverenvid
            elif request.data['status'] == '初始化':
                request.data['svrchangenid'] = None
                request.data['onoffline'] = True
        elif svrabandon:
            request.data['svrabandon'] = 1
            serverenvid = get_dictvalue('报修')
            request.data['svrchangenid'] = serverenvid
        elif svrabandon is False:
            request.data['svrabandon'] = 0
            serverenvid = get_dictvalue('报废')
            request.data['svrchangenid'] = serverenvid
            request.data['svrstoptime'] = time.strftime("%Y-%m-%d")
        elif onoffline:
            request.data['onoffline'] = 1
        elif onoffline is False:
            request.data['onoffline'] = 0

        asset = Asset.objects.get(id=assetid)
        pserializer = AssetUpdateSerializer(asset, data=request.data)
        if pserializer.is_valid():
            pserializer.save()
            return Response({'code': 200, 'msg': 'success', 'data': 'update success'})

        return Response({'code': 500, 'msg': pserializer.errors, 'data': 'update success'})


class ServerReportView(APIView):

    def post(self, request):
        svrsn = request.data['svrsn']
        try:
            asset = Asset.objects.get(svrsn=svrsn)
        except:
            asset = ''
        if asset:
            received_json_data = request.data
            asset_find = Asset.objects.filter(svrsn=svrsn).values('svrsn', 'svrip', 'svrname')[0]
            result = operator.eq(received_json_data, asset_find)
            if result:
                Asset.objects.filter(svrsn=svrsn).update(eqsname=1)
            else:
                err = []
                for key, value in received_json_data.items():
                    if value != asset_find[key]:
                        err.append(key)
                Asset.objects.filter(svrsn=svrsn).update(eqsname=0, errcontent=" ".join(err), errtime=datetime.now())
        elif not asset:
            mails("服务器未被添加", "有服务器未被添加，服务器sn: %s" % (svrsn))

        ret = {'code': 200, 'msg': 'success', 'data': 'report sn success'}
        return Response(ret)


class ServersUploadView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        path_root = settings.PATH_ROOT
        Files = request.FILES.getlist("file", None)
        file_type = request.POST.get('file_type', '0')
        if Files is None:
            return Response({'code': ResponseCode.fail, 'msg': "请选择要上传的文件", 'data': ""})
        else:
            if len(Files) > 5 or len(Files) <= 0:
                return Response({'code': ResponseCode.fail, 'msg': "请上传1至5个文件", 'data': ""})
            ret = excel_upload(file_type, Files, path_root)
            return Response(ret)


class ServersDownloadView(APIView):
    # authentication_classes = (TokenAuthentication, )

    def get(self, request):
        data_type = request.query_params.get('file_type', '0')
        file_name = '物理机导入表格模板.xlsx' if data_type == '0' else '虚拟机导入表格模板.xlsx'
        file = open(settings.EXAMPLE_ROOT + file_name, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))

        return response


class ServersDataDownloadView(APIView):
    # authentication_classes = (TokenAuthentication, )

    def get(self, request):
        data_type = request.query_params.get('file_type', '0')
        file_name = '物理机数据下载.xlsx' if data_type == '0' else '虚拟机数据下载.xlsx'
        file = data_download(data_type, settings.PATH_ROOT)
        # file = open(settings.PATH_ROOT + file_name, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))
        # response['Content-Disposition'] = 'attachment; filename="file_name"'.encode('utf-8')

        return response
