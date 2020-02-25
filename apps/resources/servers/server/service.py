#!/usr/bin/python 

# -*- coding: utf-8 -*-



'''
Created on 2018年4月23日

@author: xiangfei
'''

import json
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest 
from aliyunsdkecs.request.v20140526 import DescribeImagesRequest 
from aliyunsdkecs.request.v20140526 import DescribeVpcsRequest 
from aliyunsdkecs.request.v20140526 import DescribeVSwitchesRequest
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest
from aliyunsdkecs.request.v20140526 import CreateImageRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import  ModifyInstanceNetworkSpecRequest
from aliyunsdkecs.request.v20140526 import  AllocatePublicIpAddressRequest
access_key_id = "LTAImlBxMcZDgWSM"
access_key_secret = "eq1vfMXYCdEdW83kG5KIUogrd02xFw"
region_id = "cn-shanghai" 
image_owner ={'self':'自定义镜像 ','system':'系统镜像'}
#  带宽计费方式
charing = {'PayByTraffic':'按流量计费' ,'PayByBandwidth':'按带宽计费'}
# 服务器计费方式
InstanceChargeType ={'包年包月':'PrePaid','按量付费':'PayByBandwidth'}
zone ={"cn-shanghai-b":'华东2可用区B' , "cn-shanghai-a":'华东2可用区A'}
config_dict_list = [{'id':1 , 'name':'2核4G内存200G硬盘','cpu':2 , 'memory':4 ,'disk':200,'flavor':'ecs.sn1.medium'}, 
               {'id':2 , 'name':'4核8G内存200G硬盘','cpu':4 , 'memory':8 ,'disk':200,'flavor':'ecs.n4.xlarge'},
               {'id':3 , 'name':'2核16G内存200G硬盘','cpu':2 , 'memory':16 ,'disk':200,'flavor':'ecs.se1.large'}]
bandtype_dict_list = [{'id':1 , 'name':'按使用流量','value':'按使用流量'}]
charging_dict_list= [{'id':1 , 'name':'包年包月','value':'包年包月'}]
zone_dict_list= [{'id':1 , 'name':'华东2可用区B','value':'cn-shanghai-b'}]
cycle_dict_list=[{'id':1, 'name':'1个月', 'value':'1个月'}]
server_status_dict = {'Stopped':'已停止','Starting':'启动中','Running':'运行中','Stopping':'停止中'}
diskcatalog_dict = {'cloud_ssd':'cloud_ssd','cloud_efficiency':'cloud_efficiency','cloud':'cloud','ephemeral_ssd':'ephemeral_ssd'}
#有不同的type配置相同
#instance_type_dict = {'ecs.sn1.medium':'2核4G内存200硬盘','ecs.n4.xlarge':'4核8G内存200硬盘','ecs.se1.large':'2核16G内存200硬盘'}


class AliCloudService(object):

    def get_server_list(self):
        result_list= []
        server_list = self._get_server_list()
        image_map = self.get_image_map()
        vswitch_map = self.get_vswitch_map()
        securitygroup_map = self.get_securitygroup_map()
        for server in server_list:
            serverimage= image_map.get(server['ImageId'],server['ImageId'])
            privateip = ','.join(server['VpcAttributes']['PrivateIpAddress']['IpAddress'])
            serverid = server['InstanceId']
            zoneid = zone.get(server['ZoneId'])
            #流量计费
            charging= charing.get(server['InternetChargeType'])
            publicip = ','.join(server['PublicIpAddress']['IpAddress'])
            servername = server['InstanceName']
            networkband = server['InternetMaxBandwidthOut']
            bandtype = InstanceChargeType.get(server['InstanceChargeType'])
            status = server['Status']
            vpcid = server['VpcAttributes']['VpcId']
            vswitchid = vswitch_map.get(server['VpcAttributes']['VSwitchId'])
            cpu = server['Cpu']
            memory = int(server['Memory']/1024)
            instancetype = '{0}核{1}G内存200G硬盘'.format(cpu,memory)
#             instancetype = instance_type_dict.get(server['InstanceType'])
#            securitygroup= ','.join(server['SecurityGroupIds']['SecurityGroupId'])
            securitygroup= ','.join([securitygroup_map[sgid] for sgid in server['SecurityGroupIds']['SecurityGroupId']])
            result_list.append({'name':servername,'networkband':networkband,
                                'publicip':publicip,'privateip':privateip ,'zone':zoneid,
                                'charging':charging,'bandtype':bandtype, 'status': status,
                                'securitygroup':securitygroup,'config':instancetype,
                                'cycle': 1,'serverid':serverid,'serverimage':serverimage,
                                'vpcid':vpcid,'vswitchid':vswitchid ,'serverid':serverid})
        return result_list
    
    def _get_server_list(self , page_number = 1):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_PageSize(100)
        request.set_PageNumber(page_number)
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        total_count = json_result['TotalCount']
        page_size = json_result['PageSize']
        page_number = json_result['PageNumber']
        server_list = json_result['Instances']['Instance']
    
        if page_number * page_size >= total_count:
            return server_list
        else:
            page_number = page_number + 1
            return server_list + self._get_server_list(page_number)
    
    
    
    def get_server_status_by_serverid(self,serverid):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_InstanceIds([serverid])
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        instance_list = json_result['Instances']['Instance']
        for  instance in instance_list:
            if instance['InstanceId'] != serverid:
                raise Exception(' cannot find instance in alicloud')
            try:
                publicip = ','.join(instance['PublicIpAddress']['IpAddress'])
            except:
                publicip = ''
            try:
                privateip = ','.join(instance['VpcAttributes']['PrivateIpAddress']['IpAddress'])
            except:
                privateip = ''
            return {"status":instance['Status'],"publicip":publicip  ,"privateip":privateip ,'serverid':serverid}

    def get_server_type_list(self):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        return json_result
    
    '''
    @param period: 购买周期  
    @param flavor: 服务器规格 
    @param disksize 单位G
    @param diskcatalog:   ,cloud_efficiency 高效云盘, cloud ,云盘 cloud_ssd：SSD 云盘, ephemeral_ssd：本地 SSD 盘
    @param bandsize:  单位mbps ,出公网带宽
    '''
    def create_server(self,servername, imageid , securitygroupid ,password , flavor, period ,vswitchid ,hostname,diskcatalog,disksize ,bandsize,  useoutip =False, instancechargetype = 'PrePaid'):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_ImageId(imageid)
        request.set_InstanceName(servername)
        request.set_SecurityGroupId(securitygroupid)
        request.set_InstanceType(flavor)
        request.set_Password(password)
        request.set_VSwitchId(vswitchid)
        request.set_HostName(hostname)
        request.set_Period(period)
#         request.set_InstanceType()
        request.set_SystemDiskSize(disksize)
        request.set_SystemDiskCategory(diskcatalog)
        # 是否自动续费
        request.set_AutoRenew(True)
        # 自动续费1个月
        request.set_AutoRenewPeriod(1)

        request.set_InternetMaxBandwidthOut(bandsize)
        request.set_InstanceChargeType(instancechargetype)
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        serverid = json_result['InstanceId']
        i = 0
        while i < 600:
            serverstatus = self.get_server_status_by_serverid(serverid)
            if serverstatus['status'] == 'Running':
                break
            if serverstatus['status'] == 'Stopped':
                break
            time.sleep(1)
            i = i + 1
        if  i == 600:
            raise Exception('create instance timeout')
        if useoutip:
            print ("xxxxxxxxxx")
            self.allocate_public_ip(serverid)
            time.sleep(2)
#默认按照流量
#             self.modify_public_network(serverid, 'PayByTraffic')
        return self.get_server_status_by_serverid(serverid)

    '''
    @param NetworkChargeType: PayByBandwidth：按固定带宽计费 PayByTraffic：按使用流量计费
    @param InternetMaxBandwidthOut 出外网流量
    
    '''
    def modify_public_network(self ,InstanceId   ,NetworkChargeType = 'PayByTraffic' ):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = ModifyInstanceNetworkSpecRequest.ModifyInstanceNetworkSpecRequest()
        request.set_InstanceId(InstanceId)
        request.set_NetworkChargeType(NetworkChargeType)
        response = client.do_action_with_exception(request)
        print (response)
        return response
    def allocate_public_ip(self, instanceid ):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
        request.set_InstanceId(instanceid)
        response = client.do_action_with_exception(request)
        print (response)
        return response
    #关机
    def stop_server(self,serverid):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_InstanceId(serverid)
        response = client.do_action_with_exception(request)
        i = 0
        while i < 600:
            serverstatus = self.get_server_status_by_serverid(serverid)
            if serverstatus['status'] == 'Stopped':
                break
            time.sleep(1)
            i = i + 1
        if  i == 600:
            raise Exception('stop timeout')
        return response
    #删除
    def terminal_server(self,serverid):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = DeleteInstanceRequest.DeleteInstanceRequest()
        request.set_InstanceId(serverid)
        response = client.do_action_with_exception(request)
        return response

    def convert_server_to_image(self,servername ,serverid):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request =CreateImageRequest.CreateImageRequest()
        request.set_InstanceId(serverid)
        request.set_ImageName(servername)
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        imageid = json_result['ImageId']
        i = 0 
        while i < 600:
            client = AcsClient(access_key_id, access_key_secret,region_id)
            request = DescribeImagesRequest.DescribeImagesRequest()
            request.set_ImageId = (imageid)
            response = client.do_action_with_exception(request)
            json_result = json.loads(response)
            image_list = json_result['Images']['Image']
            print (image_list)
            if len(image_list) <= 1:
                break
            time.sleep(1)
            i =i + 1
    
        raise Exception('convert to image timeout')
        
        
    def startup_server(self,serverid):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request =StartInstanceRequest.StartInstanceRequest()
        request.set_InstanceId(serverid)
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        i = 0
        
        while i < 600:
            serverstatus = self.get_server_status_by_serverid(serverid)
            if serverstatus['status'] == 'Running':
                break
            time.sleep(1)
            i = i + 1
        if  i == 600:
            raise Exception('startup timeout plesae check')
        return json_result['RequestId']
    def get_vpc_vswitch_list(self):
        
        switch_list = self._get_vswitch_list()
        result_data = {}
        result_list = []
        
        for switch in switch_list:
            switchname = switch['VSwitchName']
            switchid = switch['VSwitchId']
            vpcid = switch['VpcId']
            if result_data.get(vpcid) == None:
                result_data[vpcid] = []
                
            result_data[vpcid].append({'switchname':switchname,'switchid':switchid})
        for key,value_dict in result_data.items():
            value_list = []
            for value in value_dict:
                if value['switchname'].find("云盘")!=-1 or value['switchname'].find("默认")!=-1:
                    continue
                value_list.append({'label':value['switchname'],'value':value['switchid']})
            result_list.append({"id":key,"label":key,"value":key,'children':value_list})
        return result_list
    
    def get_vswitch_map(self):
        vswitch_map = {}
        switch_list = self._get_vswitch_list()
        for switch in switch_list:
            switchname = switch['VSwitchName']
            switchid = switch['VSwitchId']
            vswitch_map[switchid] = switchname
            
        return vswitch_map

    def _get_vswitch_list(self):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        switch_list = json_result['VSwitches']['VSwitch']
        return switch_list
    
    def get_vpc_list(self):

        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        vpc_list = json_result['Vpcs']['Vpc']
        result_data = []
        for vpc in vpc_list:
            vpcname= vpc['VpcName']
            cidr = vpc['CidrBlock']
            status = vpc['Status']
            routerid = vpc['VRouterId']
            vpcid = vpc['VpcId']
            result_data.append({'vpcid':vpcid , 'vpcname':vpcname,'cidr':cidr,'status':status,'router':routerid })
        return result_data
    
    '''
    @type owner: str  value  self or system
    '''
    def get_image_list(self ,owner = None):
        
        image_list = self._get_image_list(owner)
        result_list = []
        for image in image_list:
            imageid = image['ImageId']
            imagename = image['ImageName']
            owner = image['ImageOwnerAlias']
            result_list.append({'id':imageid,'name':imagename,'value':imagename,'owner':owner})
        return result_list
    
    def get_image_map(self):
        
        image_list = self._get_image_list()
        result_map = {}
        for image in image_list:
            imageid = image['ImageId']
            imagename = image['ImageName']
            result_map[imageid] = imagename
        return result_map
    
    def _get_image_list(self, owner= None , page_number = 1):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = DescribeImagesRequest.DescribeImagesRequest()
        if owner:
            request.set_ImageOwnerAlias(owner)
        request.set_PageSize(100)
        request.set_PageNumber(page_number)
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        total_count = json_result['TotalCount']
        page_size = json_result['PageSize']
        page_number = json_result['PageNumber']
        image_list = json_result['Images']['Image']
        if page_number * page_size >= total_count:
            return image_list
        else:
            page_number = page_number + 1
            return image_list + self._get_image_list(owner,page_number)


    def get_securitygroup_list(self):

        result_list = []
        securitygroup_list = self._get_security_list()
        for securitygroup in securitygroup_list:
            securitygroupid = securitygroup['SecurityGroupId']
            securitygroupname= securitygroup['SecurityGroupName']
            vpcid = securitygroup['VpcId']
            result_list.append({'id':securitygroupid,'name':securitygroupname,'vpcid':vpcid,'value':securitygroupname})
        return result_list

    def get_securitygroup_map(self):
        result_map = {}
        securitygroup_list = self._get_security_list()
        for securitygroup in securitygroup_list:
            securitygroupid = securitygroup['SecurityGroupId']
            securitygroupname= securitygroup['SecurityGroupName']
            result_map[securitygroupid] = securitygroupname
        return result_map
    
    def _get_security_list(self):
        client = AcsClient(access_key_id, access_key_secret,region_id)
        request = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
        response = client.do_action_with_exception(request)
        json_result = json.loads(response)
        securitygroup_list = json_result['SecurityGroups']['SecurityGroup']
        return securitygroup_list


    
alicloudservice = AliCloudService()
if __name__ =='__main__':
    alicloudservice.allocate_public_ip("i-uf67ws1gukb1hkgp7utm")
#     alicloudservice.get_server_status_by_serverid("i-uf6c75kyx5u9b4u81mz8")
#     print (alicloudservice.get_server_status_by_serverid("i-uf6c75kyx5u9b4u81mz8"))
