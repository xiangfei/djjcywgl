#!/usr/bin/python 
from rest_framework.decorators import permission_classes

# -*- coding: utf-8 -*-

'''
Created on 2018年4月23日

@author: xiangfei
'''


from django.db import models

# Create your models here.
class Server(models.Model):

    name = models.CharField(max_length=255 )
    outterip = models.CharField(max_length=255 ,null = True)
    innerip = models.CharField(max_length=255, null = True)
    status = models.CharField(max_length=255, null = True)
    usage = models.CharField(max_length=255, null = True)
    image = models.CharField(max_length=255)
    networkband = models.CharField(max_length=255 , null = True)
    security = models.CharField(max_length=255)
    loginuser = models.CharField(max_length=255)
    loginpassword = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, null = True)
    zone = models.CharField(max_length=255, null = True)
    charging = models.CharField(max_length=255 , null = True)
    cycle = models.CharField(max_length=255)
    config = models.CharField(max_length=255 ,null = True)
    env = models.CharField(max_length=255)
    vpc = models.CharField(max_length=255)
    switch = models.CharField(max_length=255)
    useoutip = models.BooleanField(default = False)
    bandtype= models.CharField(max_length = 255 , null = True)
    serverid =  models.CharField(max_length = 255 ,unique = True)
    def __unicode__(self):
        return self.name
    
    @property
    def vpc_switch(self):
        return [self.vpc , self.switch]
    class Meta:
        db_table = 'server_server'
        permissions = (
            ('view_server', 'Can view server'),
            ('stop_server', 'Can stop server'),
            ('recover_server', 'Can recover server'),

        )
    def  concat_str(self):

        return  str(self.name) + str(self.outterip) + str(self.innerip) + str(self.status) + str(self.usage) + str(self.env) + str(self.config) + str(self.id)
    