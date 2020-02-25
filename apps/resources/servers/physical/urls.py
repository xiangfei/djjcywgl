# coding=utf-8

from django.urls import path, include, re_path
from .views import *
from django.conf.urls import url


urlpatterns = [
    path('report/', ServerReportView.as_view()),
    path('list/', ServerListView.as_view()),
    path('add/', ServerAddView.as_view()),
    path('update/', ServerUpdateView.as_view()),
    url(r'^upload/$', ServersUploadView.as_view()),
    url(r'^download/$', ServersDownloadView.as_view()),
    url(r'^datadownload/$', ServersDataDownloadView.as_view()),
]
