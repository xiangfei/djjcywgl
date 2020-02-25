from utils.response_tools import ResponseCode, except_hold
from .service import EnvService
from .serializers import EnvTypeSerializer
from django.conf import settings


@except_hold
def func_env_list(s_key, page, p_size):
    all_envs = EnvService(search_key=s_key).env_list()

    result_data = {"msgdata": all_envs[(page - 1) * p_size: page * p_size], "current_page": page, "page_size": p_size, "total": len(all_envs)}
    return {'code': ResponseCode.success, 'msg': "获取环境类型列表成功", 'data': result_data}


@except_hold
def func_env_add(e_name, desc, f_id):
    flag, new_env = EnvService().env_add(e_name, desc, f_id)

    if flag:
        return {'code': ResponseCode.success, 'msg': "环境类型新增成功", 'data': EnvTypeSerializer(new_env).data}
    else:
        return {'code': ResponseCode.fail, 'msg': "环境类型新增失败", 'data': EnvTypeSerializer(new_env).data}


@except_hold
def func_env_info(e_id):
    if e_id is None:
        return {'code': ResponseCode.params_error, 'msg': "请传入正确的环境id", 'data': ""}
    env_info = EnvService().env_info(e_id)
    return {'code': ResponseCode.success, 'msg': "环境类型信息获取成功", 'data': env_info}


@except_hold
def func_env_del(e_id):
    if e_id is None:
        return {'code': ResponseCode.params_error, 'msg': "请传入正确的环境id", 'data': ""}
    EnvService().env_del(e_id)
    return {'code': ResponseCode.success, 'msg': "环境类型删除成功", 'data': ""}


@except_hold
def func_env_edit(e_id, e_name, desc, f_id):
    if e_id is None:
        return {'code': ResponseCode.params_error, 'msg': "请传入正确的环境id", 'data': ""}
    EnvService().env_edit(e_id, e_name, desc, f_id)
    return {'code': ResponseCode.success, 'msg': "环境类型编辑成功", 'data': ""}

@except_hold
def func_env_upload(file):
    file_id = EnvService().envfile_load(settings.PATH_ROOT, file)
    return {'code': ResponseCode.success, 'msg': "环境类型脚本上传成功", 'data': file_id}


@except_hold
def func_env_download(f_id):
    return EnvService().envfile_download(f_id)


