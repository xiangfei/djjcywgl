# coding=utf-8

from django.db.models import Q
from .models import EnvType, EnvFile
from .serializers import EnvTypeSerializer
from django.shortcuts import HttpResponse
from django.utils.encoding import escape_uri_path


class EnvService(object):
    """
    环境类型管理类
    """
    def __init__(self, **kwargs):
        self.search_key = kwargs.get('search_key', None)

    def env_list(self):
        if self.search_key is None:
            envs = EnvType.objects.filter().all()
        else:
            envs = EnvType.objects.filter(Q(environ_name__contains=self.search_key) | Q(desc__contains=self.search_key))
        all_envs = EnvTypeSerializer(envs, many=True).data
        return all_envs

    def env_add(self, env_name, desc, file_id):
        try:
            env_type = EnvType(environ_name=env_name,
                               desc=desc,
                               file_id=file_id,
                               )
            env_type.save()
        except:
            return False, EnvType(environ_name='', desc='', file_id=-1)
        return True, env_type

    def env_info(self, env_id):
        env = EnvType.objects.filter(id=int(env_id)).first()
        file_info = EnvFile.objects.filter(id=env.file_id).first()
        ret_info = {"env_id": env.id, "env_name": env.environ_name, "desc": env.desc,
                    "file_id": env.file_id, "file_name": file_info.file_name if file_info else '',
                    "file_url": file_info.file_url if file_info else ''}
        return ret_info

    def env_del(self, env_id):
        EnvType.objects.filter(id=int(env_id)).delete()
        return True

    def env_edit(self, env_id, env_name, desc, file_id):
        EnvType.objects.filter(id=int(env_id)).update(**{"environ_name": env_name, "desc": desc, "file_id": file_id})
        return True

    def envfile_load(self, file_path, file):
        file_url = "{0}{1}".format(file_path, file.name)
        with open(file_url, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        file_info = EnvFile(**{"file_name": file.name, "file_url": file_path})
        file_info.save()
        file_info = EnvFile.objects.filter(**{"file_name": file.name, "file_url": file_path}).first()
        return file_info.id

    def envfile_download(self, file_id):
        file_info = EnvFile.objects.filter(id=file_id).first()
        file = open(file_info.file_url + file_info.file_name, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_info.file_name))
        return response




