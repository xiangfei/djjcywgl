
#coding=utf-8

from django.db import models

#项目列表
class ProjectRecord(models.Model):

    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=128, null=False)
    organizational_id = models.CharField(max_length=64, blank=True, null=True)
    department_id = models.CharField(max_length=64, blank=True, null=True)
    supervisor_id = models.CharField(max_length=256,verbose_name=u"负责人id", blank=True, null=True)
    product_manager_id = models.CharField(max_length=256, verbose_name=u"产品经理ID", blank=True, null=True)
    develop_user_id = models.CharField(max_length=256, verbose_name=u"开发ID", blank=True, null=True)
    ops_user_id = models.CharField(max_length=256, verbose_name=u"运维ID", blank=True, null=True)
    test_user_id = models.CharField(max_length=256, verbose_name=u"测试ID",  blank=True, null=True)
    other_user_id = models.CharField(max_length=256, verbose_name=u"其它ID", blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    online_time = models.CharField(max_length=64, null=True)
    service_num = models.CharField(max_length=64, null=True)

    def __unicode__(self):
        return self.project_name
    
    class Meta:

        permissions = (
            ('view_projectrecord', 'Can view projectrecord'),
            ('view_projectmodule', 'Can view projectmodule'),
        )


#服务列表
class ModuleRecord(models.Model):

    id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=128, null=False)
    module_tech = models.CharField(max_length=128, null=True)
    logs_path = models.CharField(max_length=64, blank=True, null=True)
    module_path = models.CharField(max_length=64, blank=True, null=True)
    port = models.CharField(max_length=64, blank=True, null=True)
    supervisor_id = models.CharField(max_length=64, blank=True, null=True)
    module_type = models.CharField(max_length=64, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, null=False)
    is_public = models.BooleanField(default=False, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    git_url = models.CharField(max_length=256, null=True)
    version_num = models.CharField(max_length=256, null=True)
    file_name = models.CharField(max_length=256, blank=True, null=True)
    files_dir = models.CharField(max_length=256, blank=True, null=True)
    child_of_project = models.ForeignKey(ProjectRecord, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.module_name

    class Meta:
        permissions = (
            ('view_modulerecord', 'Can view modulerecord'),
            ('stop_modulerecord', 'Can stop modulerecord'),
        )