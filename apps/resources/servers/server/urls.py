#!/usr/bin/python 
# -*- coding: utf-8 -*-


'''
Created on 2018年4月23日

@author: xiangfei
'''

from django.conf.urls import url
from .views import ServerDictView 
from .views import ServerDetailView
from .views import ServerVPCView
from .views import ServerNousageView
from .views import ServerSyncView
from .views import ServerListView
from .views import ServerRecoverView
from .views import ServerReleaseView
from .views import ServerStopView
from .views import ServerAddView

urlpatterns = [
    url(r'^basicdict/$', ServerDictView.as_view()),
    url(r'^vpc/$', ServerVPCView.as_view()),
    url(r'^detail/$', ServerDetailView.as_view()),
    url(r'^sync/$', ServerSyncView.as_view()),
    url(r'^list/$', ServerListView.as_view()),
    url(r'^nousage/$', ServerNousageView.as_view()),
    url(r'^recover/$', ServerRecoverView.as_view()),
    url(r'^release/$', ServerReleaseView.as_view()),
    url(r'^stop/$', ServerStopView.as_view()),
    url(r'^add/$', ServerAddView.as_view()),
]