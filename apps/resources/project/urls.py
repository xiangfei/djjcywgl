# coding=utf-8

from django.urls import path, include, re_path
from .views import *
from django.conf.urls import url

urlpatterns = [
    url('module/list/', ModulerecordListView.as_view()),
    url('module/add/', ModulerecordAddView.as_view()),
    url('module/info/', ModulerecordInfoView.as_view()),
    url('module/update/', ModulerecordUpdateView.as_view()),
    url('module/delete/', ModulerecordDeleteView.as_view()),
    url('project/list/', ProjectRecordListView.as_view()),
    url('project/add/', ProjectRecordAddView.as_view()),
    url('project/info/', ProjectRecordInfoView.as_view()),
    url('project/update/', ProjectRecordUpdateView.as_view()),
    url('module/file_download/(\w+)/$', module_file_download, name='module_file_download'),
]
