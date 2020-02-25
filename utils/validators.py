#!/usr/bin/python 
# -*- coding: utf-8 -*-



'''
Created on 2018年5月2日

@author: xiangfei
'''
import re

from rest_framework import serializers


def validate_servername(value):
    regex = re.compile(r'^\w+\d+-(pro|pre|test)$')
    if not regex.match(value):
        raise serializers.ValidationError('server name must be like ^\w+\d+-(pro|pre|test)$')
    if len(value) > 50:
        raise serializers.ValidationError('server name length > 50')
    print ('kkkkkkkk')


def validate_serversn(value):
    regex = re.compile(r'^\w+\d+$')
    if not regex.match(value):
        raise serializers.ValidationError('serversn must be like ^\w+\d+$')
    if len(value) > 50:
        raise serializers.ValidationError('serversn length > 50')


def validate_password(value):
    regex = re.compile('^(?![a-zA-Z0-9]+$)(?![^a-zA-Z/D]+$)(?![^0-9/D]+$).{8,30}$')
    if not regex.match(value):
        raise serializers.ValidationError('同时包含大小写,特殊字符8到30位')


def validate_comment(value):
    regex = re.compile(r'^(https://|http://)')
    if regex.match(value):
        raise serializers.ValidationError('comment cannot begin with http:// or https://')
    if len(value) >256 or len(value) <2:
        raise serializers.ValidationError('comment length >2 and <256')
