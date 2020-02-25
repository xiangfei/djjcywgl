import json
from .service import (
    AccountService, User, origintree_tools, myldap,
    RolesService, DicService
)
from utils.response_tools import ResponseCode, except_hold
from utils.split_tools import user_id_split

from apps.account.role.service import roleservice

@except_hold
def func_login(u_name, p_word):
    account_service = AccountService(username=u_name)

    if account_service.is_user_exist():
        flag, access_token, msg = account_service.login(p_word)
        if flag:
            return {'code': ResponseCode.success, 'msg': msg, 'data':
                {'accessToken': access_token, "user_name": account_service.chinese_name,
                 "time_out": 3600, "profile_photo": "", "user_id": str(account_service.user_id),
                 "permissions":roleservice.get_user_navigator_permission(u_name)
                 }}
        else:
            return {'code': ResponseCode.success, 'msg': msg, 'data': {}}
    else:
        return {'code': ResponseCode.func_error, 'msg': '用户不存在', 'data': {}}


@except_hold
def func_user_list(u_name, dep_id, page, p_size):
    flag, all_users = AccountService(chinese_name=u_name).list_user(u_name, dep_id)

    result_data = {"msgdata": all_users[(page - 1) * p_size: page * p_size], "current_page": page, "page_size": p_size, "total": len(all_users)}
    return {'code': ResponseCode.success, 'msg': "获取用户列表成功", 'data': result_data}


@except_hold
def func_data_sync():
    result_flag, run_flag = celery_sync()

    if result_flag and run_flag:
        return {'code': ResponseCode.success, 'msg': "用户数据同步成功", 'data': ""}
    elif result_flag and not run_flag:
        return {'code': ResponseCode.success, 'msg': "用户数据拉取成功，组织树同步失败", 'data': ""}
    else:
        return {'code': ResponseCode.fail, 'msg': "用户数据同步失败", 'data': ""}


def celery_sync():
    all_users = User.objects.all()
    result_flag, result = ldap_to_database()
    try:
        run_flag = origintree_tools.organize_tree_data()
        for user in all_users:
            origintree_tools.sync_ldap_database(user, result)
    except Exception as e:
        run_flag = False
        print('sync error ', e)
    return result_flag, run_flag


def ldap_to_database():
    groups = 'OU=信息技术部,OU=正大道,OU=金诚集团,ou=gold-finance,dc=gold-finance,dc=local'
    filter = '(objectclass=user)'
    attributes = {
        'sAMAccountName': 'username',
        'mail': 'email',
        'mobile': 'mobile',
        'cn': 'chinese_name'
    }

    flag, result = myldap.ldap_search(groups, filter, attributes.keys())
    ldap_user_list = []
    if flag:
        dp_list = []
        for item in result:
            user = json.loads(item.entry_to_json())
            dn = user.get('dn')
            ou_list = dn.split(',OU=')
            if len(ou_list) == 6:
                dp_list.append(ou_list[1])
            elif len(ou_list) == 7:
                dp_list.append(ou_list[2])
            else:
                pass
            params = {'ldap_dn': dn}
            for k, v in attributes.items():
                params[v] = user.get('attributes').get(k)[0] if user.get('attributes').get(k) else ''
                if params[v] == "null":
                    params[v] = ""
            username = params.get('username')
            account = AccountService(username=username)
            ldap_user_list.append(username)
            if account.is_user_exist():
                flag, user = account.update_user(params)
                print('{0} is updated success'.format(username))
            else:
                flag, user = account.save_user(params)
                print('{0} is saved success'.format(username))
    else:
        print("Please check, ldap is error")
    return flag, ldap_user_list


@except_hold
def func_tree_data(t_id, p_flag):
    tree_data = AccountService().get_tree_data(t_id, p_flag)
    return {'code': ResponseCode.success, 'msg': "组织树数据获取成功", 'data': tree_data}


@except_hold
def func_user_status(u_id, u_status):
    if u_id is None:
        return {'code': ResponseCode.params_error, 'msg': "请传入正确的用户id", 'data': ""}
    status_msg = '启用' if u_status else '禁用'
    account = AccountService(user_id=int(u_id))
    flag, user_object = account.update_user({"is_active": 1 if u_status else 0})
    if flag:
        return {'code': ResponseCode.success, 'msg': "用户账号{0}成功".format(status_msg), 'data': {"user_id": str(user_object.id)}}
    else:
        return {'code': ResponseCode.func_error, 'msg': "用户账号{0}失败".format(status_msg), 'data': {}}


@except_hold
def func_role_list(r_name, page, p_size):
    all_result = RolesService().get_roles(r_name)

    result_data = {"msgdata": all_result[(page - 1) * p_size: page * p_size], "current_page": page, "page_size": p_size, "total": len(all_result)}
    return {'code': ResponseCode.success, 'msg': "角色搜索成功", 'data': result_data}


@except_hold
def func_role_add(r_name, r_desc):
    if str(r_name).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入角色名称", 'data': ""}

    flag, role_data = RolesService().add_role(r_name, r_desc)

    if flag:
        return {'code': ResponseCode.success, 'msg': "角色新增成功", 'data': role_data}
    else:
        return {'code': ResponseCode.func_error, 'msg': "角色新增失败, 已存在该角色", 'data': role_data}


@except_hold
def func_role_info(r_id):
    if str(r_id).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入正确的角色id", 'data': ""}
    role_data = RolesService().get_role_info(r_id)
    return {'code': ResponseCode.success, 'msg': "角色信息获取成功", 'data': role_data}


@except_hold
def func_role_info_edit(r_id, r_name, r_desc):
    if str(r_id).strip() == '' or str(r_name).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入角色id和角色名称", 'data': ""}
    flag, role_data = RolesService().update_role_info(r_id, r_name, r_desc)

    if flag:
        return {'code': ResponseCode.success, 'msg': "角色信息编辑成功", 'data': role_data}
    else:
        return {'code': ResponseCode.func_error, 'msg': "角色编辑失败, 已存在该角色", 'data': ""}


@except_hold
def func_role_delete(r_id):
    if str(r_id).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入角色id", 'data': ""}

    flag, role_data = RolesService().del_role_info(int(r_id))

    if flag:
        return {'code': ResponseCode.success, 'msg': "角色信息删除成功", 'data': role_data}
    else:
        return {'code': ResponseCode.func_error, 'msg': "角色信息删除失败", 'data': ""}


@except_hold
def func_author_availables(r_id):
    if str(r_id).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入角色id", 'data': ""}

    role_data = RolesService().get_role_authoritys(r_id)
    return {'code': ResponseCode.success, 'msg': "角色授权项获取成功", 'data': role_data}


@except_hold
def func_author_edit(r_id, author_ids):
    if str(r_id).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入角色id", 'data': ""}
    flag = RolesService().update_role_authors(r_id, author_ids)

    if flag:
        return {'code': ResponseCode.success, 'msg': "角色权限编辑成功", 'data': ""}
    else:
        return {'code': ResponseCode.func_error, 'msg': "角色权限编辑失败", 'data': ""}


@except_hold
def func_role_users(r_id):
    if str(r_id).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入角色id", 'data': ""}
    flag, role_data = RolesService().role_users_data(r_id)

    if flag:
        return {'code': ResponseCode.success, 'msg': "获取角色用户数据成功", 'data': role_data}
    else:
        return {'code': ResponseCode.func_error, 'msg': "获取角色用户数据失败", 'data': ""}


@except_hold
def func_roleusers_edit(r_id, u_ids):
    if str(r_id).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入角色id", 'data': ""}
    user_ids = [user_id_split(str(x)) for x in u_ids]

    flag = RolesService().role_users_edit(r_id, user_ids)

    if flag:
        return {'code': ResponseCode.success, 'msg': "编辑角色用户成功", 'data': ""}
    else:
        return {'code': ResponseCode.func_error, 'msg': "编辑角色用户失败", 'data': ""}


@except_hold
def func_dic_edit(d_id, d_name, d_content, a_name):
    if str(d_id).strip() == '' or len(d_content) <= 0:
        return {'code': ResponseCode.params_error, 'msg': "请输入正确参数", 'data': ""}
    flag = DicService(dic_id=d_id).dic_edit(d_name, d_content, a_name)
    if flag:
        return {'code': ResponseCode.success, 'msg': "数据字典编辑成功", 'data': ""}
    else:
        return {'code': ResponseCode.func_error, 'msg': "数据字典处于使用中，不能删除", 'data': ""}


@except_hold
def func_dic_add(d_name, d_content, a_name):
    if str(a_name).strip() == '' or len(d_content) <= 0:
        return {'code': ResponseCode.params_error, 'msg': "请输入正确参数", 'data': ""}
    ret_id = DicService().dic_add(d_name, d_content, a_name)
    return {'code': ResponseCode.success, 'msg': "数据字典新增成功", 'data': ret_id}


@except_hold
def func_dic_search():
    ret_data = DicService().dic_search()
    return {'code': ResponseCode.success, 'msg': "数据字典查询成功", 'data': ret_data}


@except_hold
def func_dic_del(d_id):
    if str(d_id).strip() == '':
        return {'code': ResponseCode.params_error, 'msg': "请输入正确参数", 'data': ""}
    flag = DicService(dic_id=int(d_id)).dic_del()
    if flag:
        return {'code': ResponseCode.success, 'msg': "数据字典删除成功", 'data': ""}
    else:
        return {'code': ResponseCode.success, 'msg': "数据字典处于使用中，不能删除", 'data': ""}


@except_hold
def func_dic_list(s_key, page, p_size):
    page = int(page)
    p_size = int(p_size)
    dic_list = DicService().dic_list(s_key)
    result_data = {"msgdata": dic_list[(page - 1) * p_size: page * p_size], "current_page": page, "page_size": p_size, "total": len(dic_list)}
    return {'code': ResponseCode.success, 'msg': "数据字典列表获取成功", 'data': result_data}





