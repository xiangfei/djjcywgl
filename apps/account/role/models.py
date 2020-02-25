#!/usr/bin/python 

# -*- coding: utf-8 -*-

'''
Created on 2018年5月9日

@author: xiangfei
'''
# from django.db import models
# from guardian.admin import GuardedModelAdmin
# from django.contrib import admin
# from django.contrib.auth.models import ContentType
# class Navigator(models.Model):
#     name = models.CharField(max_length=255)
#     parentid = models.ForeignKey("self" , null =True , on_delete= models.SET_NULL ,related_name= 'children')
#     contenttype = models.ForeignKey(ContentType , null =True , on_delete= models.SET_NULL)
#     def __str__(self):
#         return self.name
#     class Meta:
#         db_table = "account_navigator"
#         
#     def get_all_children(self, include_self=True):
#         r = []
#         if include_self:
#             r.append(self)
#         for c in Navigator.objects.filter(parentid=self):
#             _r = c.get_all_children(include_self=True)
#             if 0 < len(_r):
#                 r.extend(_r)
#         return r
# 
# 
# admin.site.register(Navigator, GuardedModelAdmin)
# 
# 
# from mptt.models import MPTTModel, TreeForeignKey
# class TreeView(MPTTModel):
#     name = models.CharField(max_length=50, unique=True)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
# 
#     class MPTTMeta:
#         order_insertion_by = ['name']
# 
# 
# admin.site.register(TreeView, GuardedModelAdmin)