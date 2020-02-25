from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.


class EnvType(models.Model):
    """
    用户表
    """
    class Meta:
        db_table = "envir_type"

    id = models.AutoField(primary_key=True)
    environ_name = models.CharField(max_length=255, null=False, unique=True, db_index=True)
    desc = models.CharField(max_length=255, null=True)
    file_id = models.IntegerField(unique=True, null=True)

    def __repr__(self):
        return '<Env %r>' % (self.environ_name)

    def __str__(self):
        return self.environ_name


class EnvFile(models.Model):
    """
    脚本文件表
    """
    class Meta:
        db_table = "envir_envfile"
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255, null=False, unique=True, db_index=True)
    file_url = models.CharField(max_length=255, null=True)

