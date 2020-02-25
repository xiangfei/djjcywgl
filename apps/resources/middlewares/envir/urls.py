"""jcywgl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import (
    EnvListView, EnvAddView, EnvInfoView,
    EnvDeleteView, EnvEditView, EnvUploadView,
    EnvDownloadView,
)


urlpatterns = [
    url(r'^search/$', EnvListView.as_view()),
    url(r'^add/$', EnvAddView.as_view()),
    url(r'^info/$', EnvInfoView.as_view()),
    url(r'^delete/$', EnvDeleteView.as_view()),
    url(r'^edit/$', EnvEditView.as_view()),
    url(r'^upload/$', EnvUploadView.as_view()),
    url(r'^download/$', EnvDownloadView.as_view()),
]
