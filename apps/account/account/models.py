from django.db import models
from django.contrib.auth.models import User as AuUser
from django.contrib.auth.models import Group
from guardian.admin import GuardedModelAdmin
from django.contrib import admin
from rest_framework.authtoken.models import Token
# from sequences import get_next_value


class JCGroup(models.Model):
    """
    集团表
    """
    class Meta:
        db_table = "account_jcgroup"
    id = models.AutoField(primary_key=True )
    jcgroup = models.CharField(max_length=32, unique=True, null=False)
    jcgroup_id = models.IntegerField(unique=True, null=False, default=-1)

    def __unicode__(self):
        return self.jcgroup


admin.site.register(JCGroup, GuardedModelAdmin)


class SubCompany(models.Model):
    """
    集团下属分支表
    """
    class Meta:
        db_table = "account_subcompany"
    id = models.AutoField(primary_key=True )
    subcompany = models.CharField(max_length=32, unique=False, null=False)
    subcompany_id = models.IntegerField(unique=True, null=False, default=-1)
    jcgroup_id = models.IntegerField(unique=False, null=True)

    def __unicode__(self):
        return self.subcompany


admin.site.register(SubCompany, GuardedModelAdmin)


class Branch(models.Model):
    """
    部门表
    """
    class Meta:
        db_table = "account_branch"
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length=32, unique=False, null=False)
    branch_id = models.IntegerField(unique=True, null=False, default=-1)
    subcompany_id = models.IntegerField(unique=False, null=True)
    jcgroup_id = models.IntegerField(unique=False, null=True)

    def __unicode__(self):
        return self.branch
    
    
admin.site.register(Branch, GuardedModelAdmin)


class Department(models.Model):
    """
    局表
    """
    class Meta:
        db_table = "account_department"
    id = models.AutoField(primary_key=True )
    department = models.CharField(max_length=32, unique=False, null=False)
    department_id = models.IntegerField(unique=True, null=False, default=-1)
    branch_id = models.IntegerField(unique=False, null=True)
    subcompany_id = models.IntegerField(unique=False, null=True)
    jcgroup_id = models.IntegerField(unique=False, null=True)

    def __unicode__(self):
        return self.department


admin.site.register(Department, GuardedModelAdmin)


class Bureau(models.Model):
    """
    科室表
    """
    class Meta:
        db_table = "account_bureau"
    id = models.AutoField(primary_key=True)
    bureau = models.CharField(max_length=32, unique=False, null=False)
    bureau_id = models.IntegerField(unique=True, null=False, default=-1)
    department_id = models.IntegerField(unique=False, null=True)
    branch_id = models.IntegerField(unique=False, null=True)
    subcompany_id = models.IntegerField(unique=False, null=True)
    jcgroup_id = models.IntegerField(unique=False, null=True)

    def __unicode__(self):
        return self.bureau


admin.site.register(Bureau, GuardedModelAdmin)


class Role(Group):
    desc = models.CharField(max_length=32, null=True)
    role_desc = models.CharField(max_length=120, null=True)
    author_id = models.CharField(max_length=64, unique=False, null=True)
    used_author_id = models.CharField(max_length=64, unique=False, null=True)

    class Meta:
        db_table = "account_role"
        permissions = (
            ('view_role', 'Can view role'),
            ('view_permission', 'Can view permission'),
            ('change_permission', 'Can change permission'),
        
        )
    def to_json(self):
        return {'role_id': self.id,
                'role_name': self.name,
                'desc': self.role_desc,
                }


class RoleAuthority(models.Model):
    """
    角色权限表
    """
    class Meta:
        db_table = "account_authority"
    id = models.AutoField(primary_key=True)
    role_authority = models.CharField(max_length=32, unique=True, null=False)
    

admin.site.register(Role, GuardedModelAdmin)


class User(AuUser):
    chinese_name = models.CharField(max_length=32, null=True)
    mobile = models.CharField(max_length=32, null=True)
    ldap_dn = models.CharField(max_length=120, null=True)
    date_updated = models.DateTimeField(null=True, auto_now=True)
    department_id = models.IntegerField(null=False, default=-1)
    bureau_id = models.IntegerField(null=False, default=-1)
    branch_id = models.IntegerField(null=False, default=-1)

    class Meta:
        db_table = "account_user"
        permissions = (
            ('view_user', 'Can view user'),
            ('sync_user', 'Can sync user'),
            ('enable_user', 'Can enable user'),
            ('disable_user', 'Can disable user'),
            ('search_user', 'Can search user'),
        )
    def to_json(self):
        return {'user_id': str(self.id),
                'ldap_name': self.username,
                'user_name': self.chinese_name,
                'mobile': self.mobile or '',
                'status': True if self.is_active else False
                }

admin.site.register(User, GuardedModelAdmin)


# class UserToken(Token):
#     token_time = models.DateTimeField(auto_now_add=True)
#     
#     def to_json(self):
#         return {
#             "user_id": self.user.id,
#             "access_token": self.key,
#             "token_time": self.token_time,
#         }
# 
# 
# admin.site.register(UserToken, GuardedModelAdmin)




from django.contrib.auth.models import Permission
 
admin.site.register(Permission , GuardedModelAdmin)

class DataDicName(models.Model):
    name = models.CharField(max_length=128, blank=True, null=False)
    aliasname = models.CharField(max_length=128, blank=True, null=False)

    class Meta:
        db_table = "data_dic_name"


class DataDicContent(models.Model):
    content = models.CharField(max_length=1024, blank=True, null=False)
    name = models.ForeignKey(DataDicName, on_delete=models.CASCADE, related_name='datadiccontent')

    class Meta:
        db_table = "data_dic_content"


# class TaskLog(models.Model):
#     StartTime = models.DateTimeField(auto_now_add=True)
#     TaskType = models.CharField(max_length=1024, blank=True, null=False)
#     User = models.ForeignKey('User', on_delete=models.DO_NOTHING)
#     TaskContent = models.TextField()
#
#     class Meta:
#         db_table = "task_log"


"""
TaskLog表

StartTime = models.DateTimeField(auto_now_add=True)
TaskType = models.CharField(max_length=1024, blank=True, null=False)
User = models.ForeignKey('Users')
TaskContent = models.TextField()(待确定)

DataDicName表
name = models.CharField(max_length=128, blank=True, null=False)
DataDicContent表
Content = models.CharField(max_length=1024, blank=True, null=False)
name = models.ForeignKey(DataDicName, on_delete=models.CASCADE)

"""




