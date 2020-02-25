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
    LoginView, LogoutView, UserListView,
    UserDataSyncView, UserTreeDataView,
    UserStatusModifyView, RoleListView,
    RoleAddView, RoleInfoView, RoleEditInfoView,
    RoleDeleteView, AuthorAvailableView,
    AuthorEditView, RoleUsersView, RoleUsersEditView,
    DataDictionaryEditView, DataDictionaryAddView,
    DataDictionaryDelView, DataDictionarysView,
)

urlpatterns = [
    url(r'^user/login/$', LoginView.as_view()),
    url(r'^user/logout/$', LogoutView.as_view()),
    url(r'^user/search/$', UserListView.as_view()),
    url(r'^user/sync/$', UserDataSyncView.as_view()),
    url(r'^user/organizetree/$', UserTreeDataView.as_view()),
    url(r'^user/setstatus/$', UserStatusModifyView.as_view()),
    url(r'^role/search/$', RoleListView.as_view()),
    url(r'^role/add/$', RoleAddView.as_view()),
    url(r'^role/roleinfo/$', RoleInfoView.as_view()),
    url(r'^role/edit/$', RoleEditInfoView.as_view()),
    url(r'^role/delete/$', RoleDeleteView.as_view()),
    url(r'^role/authorinfos/$', AuthorAvailableView.as_view()),
    url(r'^role/authoredit/$', AuthorEditView.as_view()),
    url(r'^role/userinfos/$', RoleUsersView.as_view()),
    url(r'^role/usersedit/$', RoleUsersEditView.as_view()),
    url(r'^user/data_dictionary/$', DataDictionaryEditView.as_view()),
    url(r'^user/adddictionary/$', DataDictionaryAddView.as_view()),
    url(r'^user/deldictionary/$', DataDictionaryDelView.as_view()),
    url(r'^user/dictionarys/$', DataDictionarysView.as_view()),
]
