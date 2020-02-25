#!/usr/bin/python 

# -*- coding: utf-8 -*-
'''
Created on 2018年4月23日

@author: xiangfei
'''

from rest_framework import serializers
from .models import Server
from django.db import transaction
from .service import alicloudservice
from .service import config_dict_list , cycle_dict_list , zone_dict_list ,charging_dict_list , bandtype_dict_list ,diskcatalog_dict, server_status_dict
from jcywgl.settings import  ALICLOUD_ACTION
import uuid
from utils.validators import validate_servername , validate_comment , validate_password


class ServerDetailSerializer(serializers.ModelSerializer):
    id =  serializers.IntegerField()
    name = serializers.CharField(required = False)
    image = serializers.CharField(required = False)
    vpc = serializers.CharField(required = False)
    env = serializers.CharField(required = False)
    cycle = serializers.CharField(required = False)
    switch = serializers.CharField(required = False)
    security = serializers.CharField(required = False)
 
    def get_server_detail(self):
        
        serverid = self.initial_data['id']
        server = Server.objects.get(pk = serverid)
        return ServerDetailSerializer(server)

    class Meta:
        model = Server
        fields = ('name', 'outterip', 'innerip' ,'status','usage' ,'image' 
                  , 'networkband','security','switch'
                  ,'comment','zone','charging','cycle','config','env' ,'id','vpc'
                  )

class ServerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = ('name', 'outterip', 'innerip' ,'status','usage' ,'id' ,'env' ,'config','id'
                  )



class ServerNoUsageSerializer(serializers.ModelSerializer):

    env  = serializers.HiddenField(default  = '123')

    class Meta:
        model = Server
        fields = ('outterip', 'innerip' ,'id' ,'env')
        
    def list_no_usage_server(self):
        
        env = self.initial_data['env']
        search_server_list = Server.objects.all().filter(env = env).filter(usage__isnull=True)
        return ServerNoUsageSerializer(search_server_list, many = True)


class ServerAddSerializer(serializers.ModelSerializer):
    env = serializers.CharField(required=False)
    serverid = serializers.CharField(required=False)
    networkband = serializers.CharField(required=False)
    bandtype = serializers.CharField(required=False)
    comment = serializers.CharField(required = False , validators = [validate_comment])
    name = serializers.CharField(validators = [validate_servername])
    loginpassword = serializers.CharField(validators = [validate_password])
    vpc_switch = serializers.ListField(max_length = 2 , min_length = 2)
    
    def create(self, validated_data):
        vpc_switch = validated_data.pop('vpc_switch')
        validated_data['switch'] = vpc_switch[-1]
        validated_data['vpc'] = vpc_switch[0]
        cycleid = 1
        disksize = 200
        image_map = alicloudservice.get_image_map()
        security_map = alicloudservice.get_securitygroup_map()
        switch_map = alicloudservice.get_vswitch_map()
        imageid =  validated_data['image']
        validated_data['image']  =image_map.get(imageid)
        securityid = validated_data['security']
        validated_data['security'] =security_map.get(securityid)
        if validated_data['switch'].find("预发")!=-1:
            env = '预发环境'
        else:
            env = '正式环境'
            
        switchid  =  validated_data['switch']
        validated_data['switch'] = switch_map.get(switchid)
        for config in config_dict_list:
            if int(config['id']) == int(validated_data['config']):
                validated_data['config'] = config['name']
                flavor = config['flavor']
                disksize  = config['disk']
                break
        for cycle in cycle_dict_list:
            if int(cycle['id']) == int(validated_data['cycle']):
                validated_data['cycle'] = cycle['name']
                cycleid = cycle['id']
                break
        for zone in zone_dict_list:
            if int(zone['id']) == int(validated_data['zone']):
                validated_data['zone'] = zone['name']
                break
        for charging in charging_dict_list:
            if int(charging['id']) == int(validated_data['charging']):
                validated_data['charging'] = charging['name']
                break
        for bandtype in bandtype_dict_list:
            if validated_data.get('bandtype'):
                if int(validated_data.get('bandtype'))== bandtype['id']:
                    validated_data['bandtype'] = bandtype['name']
        
        servername = validated_data['name']
        password = validated_data['loginpassword']
        period = cycleid
        hostname = servername
        diskcatalog = diskcatalog_dict.get('cloud_efficiency')
        bandsize =  int(validated_data.get('networkband',0) )
        useoutip =  validated_data['useoutip']
        with transaction.atomic():
            if ALICLOUD_ACTION:
                server_status = alicloudservice.create_server(servername, imageid, securityid, password,
                                                                      flavor, period, switchid, hostname, diskcatalog, 
                                                                      disksize, bandsize , useoutip = useoutip)
                serverid = server_status['serverid']
                outterip = server_status['publicip']
                innerip = server_status['privateip']
                status = server_status_dict.get(server_status['status'])
            else:
                serverid = uuid.uuid4().hex
                outterip = "127.0.0.1"
                innerip = "127.0.0.1"
                status = '已停止'
            return Server.objects.create( serverid = serverid,
                                   env = env ,outterip =outterip ,innerip = innerip,status = status
                                   , **validated_data)


    class Meta:
        model = Server
        fields = ('vpc_switch','bandtype','useoutip','config','cycle','charging','zone','comment','loginpassword','loginuser',
                  'security','networkband','image','usage','name' ,'env','serverid'
                  )
        
        
class ServerReleaseSerializer(serializers.ModelSerializer):
    
    id =  serializers.IntegerField()
    backups = serializers.BooleanField(default = False)
    def  server_release(self , delete_instance = False):
        serverid = self.initial_data['id']
        backups = self.initial_data['backups']
        server = Server.objects.get(pk = serverid)
        if server.status !="已停止":
            raise Exception("只能释放已停止的服务器")
        if delete_instance:
            
            if backups:
                alicloudservice.convert_server_to_image(server.name, server.serverid)
            alicloudservice.terminal_server(server.serverid)
        server.delete()
    class Meta:
        model = Server
        fields = ('id', 'backups')
        
class ServerRecoverSerializer(serializers.ModelSerializer):
    id =  serializers.IntegerField()
    
    def server_recover(self ,recover_instance = False):
        serverid = self.initial_data['id']
        server = Server.objects.get(pk = serverid)
        if server.status !="已停止":
            raise Exception("只能恢复已经停止的服务器")
        server.status = server_status_dict.get('Running')
        if recover_instance:
            alicloudservice.startup_server(server.serverid)
        server.save()
    class Meta:
        model = Server
        fields = ('id',)
        
class ServerStopSerializer(serializers.ModelSerializer):
    id =  serializers.IntegerField()
    
    def stop_server(self , stop_instance = False):
        serverid = self.initial_data['id']
        server = Server.objects.get(pk = serverid)
        if server.status !="运行中":
            raise Exception("只能停止正在运行的服务器")
        server.status = server_status_dict.get('Stopped')
        if stop_instance:
            alicloudservice.stop_server(server.serverid)
        server.save()
    class Meta:
        model = Server
        fields = ('id',)