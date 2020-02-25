#!/usr/bin/python 
# -*- coding: utf-8 -*-


'''
Created on 2018年5月2日

@author: xiangfei
'''
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import InvalidPage
from django.utils import six
from rest_framework.exceptions import NotFound
from rest_framework.pagination import _positive_int
#默认get查询方式，post不起作用
class CommonPagination(PageNumberPagination):
    #默认每页显示的个数
    page_size = 10
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'page'
    #最多能显示多少页
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
            'page_size':self.page_size,
            'count': self.page.paginator.count,
            'data': data
        })


#PageNu
class ServerPagination(PageNumberPagination):
    
    
    #默认每页显示的个数
    page_size = 10
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'current_page'



    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.data[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size
    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.data.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    
    def get_paginated_response(self, data):
        total = self.page.paginator.count
        page_size = self.request.data.get(self.page_size_query_param, self.page_size)
        current_page = self.request.data.get(self.page_query_param , 1)
        ret = {'code':200,'msg':None,'data':{'msg':data,'total':total,'page_size':page_size,'current_page': current_page }}
        return Response(ret)


class NewServerPagination(ServerPagination):

    def get_paginated_response(self, data):
        total = self.page.paginator.count
        page_size = self.request.data.get(self.page_size_query_param, self.page_size)
        current_page = self.request.data.get(self.page_query_param , 1)
        ret = {'code': 200, 'msg': None, 'data': {'msgdata': data, }, 'total': total, 'page_size':page_size, 'current_page': current_page}
        return Response(ret)