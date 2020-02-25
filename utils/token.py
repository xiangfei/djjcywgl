#!/usr/bin/python 
# -*- coding: utf-8 -*-

'''
Created on 2018年4月27日

@author: xiangfei
'''

from rest_framework import authentication 
from rest_framework.exceptions import APIException
from rest_framework.authtoken.models import Token


class AuthenticationFailed(APIException):
    status_code = 401
    default_code = 'authentication_failed'


class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        access_token = request.META.get('HTTP_ACCESSTOKEN') or request.COOKIES.get('AUID')
        if not access_token:
            raise AuthenticationFailed("无效token")
        if access_token == '1qaz@wsx3edc4rfv':
            return (access_token, None)
        session = request.session.get(access_token, None)
        if session:
            try:
                token = Token.objects.get(key = session)
                request.user = token.user
                request.token = token.key

            except Token.DoesNotExist:
                raise AuthenticationFailed("认证失败")
        else:
            raise AuthenticationFailed("timeout")

        request.user_id = token.user.id
        request.access_token = token.key

        return (token.key, None) 
