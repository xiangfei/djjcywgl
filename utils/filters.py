#!/usr/bin/python 
# -*- coding: utf-8 -*-


'''
Created on 2018年5月2日

@author: xiangfei
'''
from rest_framework.filters import SearchFilter
from  django_filters.rest_framework import  DjangoFilterBackend
from django.template import loader
class PostSearchFilter(SearchFilter):
    
    search_param = 'search_text'
    
    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.data.get(self.search_param, '')
        return params.replace(',', ' ').split()
    
class POSTDjangoFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)

        if filter_class:
            return filter_class(request.data, queryset=queryset, request=request).qs

        return queryset

    def to_html(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)
        if not filter_class:
            return None
        filter_instance = filter_class(request.data, queryset=queryset, request=request)

        template = loader.get_template(self.template)
        context = {
            'filter': filter_instance
        }

        return template.render(context, request)