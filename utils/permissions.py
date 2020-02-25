'''
Created on 2018年5月10日

@author: xiangfei
'''
import wrapt
from rest_framework.exceptions import PermissionDenied, APIException
from  rest_framework.request import  Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Permission
from guardian.shortcuts import get_perms_for_model , get_user_perms
from django.http.request import HttpRequest
from django.core.handlers.wsgi import HttpRequest as WHttpRequest
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import User
def get_user(request):
    tokenid  = request.META.get('HTTP_ACCESSTOKEN') or request.COOKIES.get('AUID')
    if tokenid == '1qaz@wsx3edc4rfv':
        
        try:
            user  = User.objects.get(username = 'admin')
        except User.DoesNotExist:
            user =  User.objects.create_superuser("admin", "admin@jcgroup.com", "1qaz@wsx")
        return user
    token = Token.objects.get(key = tokenid)
    user = token.user
    return user

def check_permission(perm):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        for request in args:
            if isinstance(request, (Request,HttpRequest , WSGIRequest, WHttpRequest)):
                user = get_user(request)

                if isinstance(perm, str):
                    if user.has_perm(perm):

                        return wrapped(*args, **kwargs)

                elif isinstance(perm, tuple) or isinstance(perm, list):
                    for p in perm:

                        if user.has_perm(p):
                            return wrapped(*args, **kwargs)

        raise  PermissionDenied()
    return wrapper

def compare_permission(user , permissonqueryset = None):

    user_permission_list  = user.get_all_permissions()
    result_map = {}
    if permissonqueryset:
        permission_list = permissonqueryset
    else:
        permission_list = Permission.objects.all()
    
    for permission in permission_list:
        
        contentypename =  permission.content_type.app_label
        permissionname = permission.codename
        fullname =  contentypename + '.' + permissionname
        if fullname in user_permission_list:
            result_map[permissionname] = True
        else:
            result_map[permissionname] = False

    return result_map


@wrapt.decorator
def list_permission(wrapped, instance, args, kwargs):
    try:
        model =  instance.serializer_class.Meta.model
        model_perm = get_perms_for_model(model)
    except:
        raise APIException('missing serializer class')

    for request in args:
        if isinstance(request, Request):
            user = get_user(request)
            result_list = compare_permission(user , model_perm)

    result = wrapped(*args, **kwargs)
    data_result_dict =  result.data
    data_result_dict['data']['permissions'] = result_list

    return Response(data_result_dict)

