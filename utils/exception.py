'''
Created on 2018年5月3日

@author: xiangfei
'''

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
import traceback


def jcgroup_exception_handler(exc, context):

    traceback.print_exc()
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

        return Response({'code':response.status_code , 'msg': exc.detail ,'data':None})

    else:
        
        if isinstance(exc, Exception):
            return Response({'code': 500 , 'msg': APIException(exc).detail ,'data':None})

        
        