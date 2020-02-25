#coding=utf-8

from django.db import models
from apps.resources.servers.server.models import Server
from datetime import datetime
from apps.account.account.models import User


class Asset(models.Model):

    manageip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"管理IP/宿主机IP")
    switchip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"接入交换机IP")
    hostuser = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"登录名")
    hostpassword = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"登陆密码")
    svrname = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"主机名")
    svrip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"IP")
    svrsn = models.CharField(max_length=128, blank=True, null=False, verbose_name=u"SN编号")
    tdtnamenid = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"服务器型号id")
    idcnamenid = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"机房号id")
    iopnamenid = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"机柜号id")
    eqsname = models.BooleanField(default=True, verbose_name="机器状态(正常/异常)")
    svrfirstusetime = models.DateField("购入时间", blank=True, null=True)
    svrstoptime = models.DateField("报废时间", blank=True, null=True)
    svrofftime = models.DateField("下线时间", blank=True, null=True)
    sfwnamenid = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"操作系统id")
    strdescription = models.TextField(blank=True, null=True, verbose_name=u"设备描述")
    svrchangenid = models.CharField(max_length=256, blank=True, null=True, verbose_name=u"环境状态id")
    laststatus = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"上次状态")
    svrabandon = models.BooleanField(default=False, verbose_name=u"报修/报废")
    errcontent = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"异常内容")
    errtime = models.DateTimeField(u"异常时间", auto_now_add=True, blank=True, null=True)
    onoffline = models.BooleanField(default=False, verbose_name=u"物理机/未上线")
    # server = models.OneToOneField(Server, on_delete=models.CASCADE,)

    def __unicode__(self):
        return self.svrname

    class Meta:
        permissions = (
            ('view_asset', 'Can view asset'),
        )


class TaskLog(models.Model):
    # serverid = models.IntegerField(unique=False, null=True)
    serverid = models.ForeignKey(Asset, on_delete=models.CASCADE)
    starttime = models.DateTimeField(auto_now_add=True)
    origin_status = models.CharField(max_length=128, unique=False, null=True)
    changed_status = models.CharField(max_length=128, unique=False, null=True)
    user_name = models.CharField(max_length=128, unique=False, null=True)

    class Meta:
        db_table = "task_log"
