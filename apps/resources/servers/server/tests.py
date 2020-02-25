#!/usr/bin/python 

# -*- coding: utf-8 -*-

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .views import ServerListView
from .views import ServerAddView
from .views import ServerRecoverView
from .views import ServerStopView
from .views import ServerReleaseView
from .views import ServerDictView
from .views import ServerVPCView
from .views import ServerDetailView
from .views import ServerNousageView
# Create your tests here.


class ServerTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.csrftoken = "1qaz@wsx3edc4rfv" 
    
    def test_main(self):
        self._test_001_create_server()
        self._test_002_get_server_list()
        self._test_002_02_get_nousage_server()
        self._test_003_startup_server()
        self._test_004_poweroff_server()
        self._test_005_server_detail()
        self._test_006_release_server()
        self._test_007_get_server_basicdict()
        self._test_008_get_server_vpc()
    
    def _test_001_create_server(self):
        data = {
            "bandtype":"1",
            "charging":"1",
            "comment":"333333",
            "config":"2",
            "loginpassword":"XFTEST@jcroup2.com",
            "cycle":"1",
            "image":"m-uf68o21m55wtnqlzhzez",
            "loginpassword":"XFTEST@jcroup2.com",
            "loginuser":"root",
            "name":"testxiangfeiout01-pre",
            "networkband":"5",
            "security":"sg-uf6f3z1ua4xce0y5ig8z",
            "useoutip":'true',
            "vpc_switch":["vpc-uf65ldgyqi9vuimxigpem", "vsw-uf616ikve0wf7vb8605jb"],
            "zone":"1"
            }
        request = self.factory.post('/server/add' , data ,format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view = ServerAddView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200

    def _test_002_get_server_list(self):
        request = self.factory.post('/server/list')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view  = ServerListView.as_view()
        response = view(request)
        print (response.data)
        assert response.status_code == 200

    def _test_002_02_get_nousage_server(self):
        data = {'env':'正式环境'}
        request = self.factory.post('/server/nousage' , data ,format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view = ServerNousageView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200

    def _test_003_startup_server(self):
        data = {"id": "1"}
        request = self.factory.post('/server/recover', data ,format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view  = ServerRecoverView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200

    def _test_004_poweroff_server(self):
        
        data = {"id": "1"}
        request = self.factory.post('/server/stop', data ,format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view  = ServerStopView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200
        
    def _test_005_server_detail(self):
        data = {"id": "1" }
        request = self.factory.post('/server/detail', data ,format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view  = ServerDetailView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200
        
    def _test_006_release_server(self):
        data = {"id": "1" ,"backups":"true"}
        request = self.factory.post('/server/release', data ,format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view  = ServerReleaseView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200

    def _test_007_get_server_basicdict(self):
        
        request = self.factory.get('/server/basicdict')
        view  = ServerDictView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200

    def _test_008_get_server_vpc(self):
        
        request = self.factory.get('/server/vpc')
        view  = ServerVPCView.as_view()
        response = view(request)
        print (response.data)
        assert response.data['code'] == 200