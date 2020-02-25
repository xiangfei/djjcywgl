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

from django.urls import path, include 
from rest_framework import routers
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_jwt_token),
    path('account/', include('apps.account.account.urls')),
    path('middlewares/', include('apps.resources.middlewares.urls')),
    path('resources/', include('apps.resources.project.urls')),
    path('role/', include('apps.account.role.urls')),
    path('server/', include('apps.resources.servers.server.urls')),
    path('cmdb/', include('apps.resources.servers.physical.urls')),
]


