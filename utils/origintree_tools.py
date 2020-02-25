#coding=utf-8

import pymysql
from collections import OrderedDict

from jcywgl import settings
from utils.basic_ldap import myldap
from apps.account.account.models import User, JCGroup, SubCompany, Branch, Department, Bureau
from django.db import connection
class SqlConnection(object):

    conn = None

    def __new__(self, ip=None, port=None, user=None, password=None, database=None):

        return connection

class DbOperation(object):

    def __init__(self):
        self.conn = SqlConnection()

    def data_select_all(self, sql_string):
        cursor = self.conn.cursor()
        cursor.execute(sql_string)
        return cursor.fetchall()

    def data_select_one(self, sql_string):
        cursor = self.conn.cursor()
        cursor.execute(sql_string)
        return cursor.fetchone()

    def data_run_sql(self, sql_string):
        cursor = self.conn.cursor()
        if isinstance(sql_string, list):
            for sql_str in sql_string:
                cursor.execute(sql_str)
        elif isinstance(sql_string, str):
            cursor.execute(sql_string)
        if isinstance(sql_string, (str, list)):
            try:
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()


def organize_tree_data():
    """
    拆分ldap_dn数据存入数据库
    """
    conn = DbOperation()
    source_data = conn.data_select_all('select user_ptr_id , ldap_dn from account_user as ac inner join auth_user as au on au.id = ac.user_ptr_id  where au.is_active=1')
    
    init_params = dict(
            bureau_id=10001,
            department_id=1001,
            branch_id=101,
            subcompany_id=11,
            jcgroup_id=1,
            init=True,
        )
    for user_data in source_data:
        user_id = user_data[0]
        ldap_str_list = user_data[1].split(',')
        temp_str = str(ldap_str_list[1]).split('=')[1]
        if temp_str.endswith('部'):
            branch_name = temp_str
            subcompany_name = str(ldap_str_list[2]).split('=')[1]
            jcgroup_name = str(ldap_str_list[3]).split('=')[1]
            params = dict(
                init=init_params['init'],
                user_id=user_id,
                bureau_id=init_params['bureau_id'],
                department_id=init_params['department_id'],
                branch_id=init_params['branch_id'],
                subcompany_id=init_params['subcompany_id'],
                jcgroup_id=init_params['jcgroup_id'],
                branch_name=branch_name,
                subcompany_name=subcompany_name,
                jcgroup_name=jcgroup_name
            )
            split_to_database(conn, init_params, params)
            continue
        elif temp_str.endswith('局'):
            department_name = temp_str
            branch_name = str(ldap_str_list[2]).split('=')[1]
            subcompany_name = str(ldap_str_list[3]).split('=')[1]
            jcgroup_name = str(ldap_str_list[4]).split('=')[1]
            params = dict(
                init=init_params['init'],
                user_id=user_id,
                bureau_id=init_params['bureau_id'],
                department_id=init_params['department_id'],
                branch_id=init_params['branch_id'],
                subcompany_id=init_params['subcompany_id'],
                jcgroup_id=init_params['jcgroup_id'],
                department_name=department_name,
                branch_name=branch_name,
                subcompany_name=subcompany_name,
                jcgroup_name=jcgroup_name
            )
            split_to_database(conn, init_params, params)
            continue
        elif temp_str.endswith('科') or temp_str.endswith('中心'):
            bureau_name = temp_str
            department_name = str(ldap_str_list[2]).split('=')[1]
            branch_name = str(ldap_str_list[3]).split('=')[1]
            subcompany_name = str(ldap_str_list[4]).split('=')[1]
            jcgroup_name = str(ldap_str_list[5]).split('=')[1]
            params = dict(
                init=init_params['init'],
                user_id=user_id,
                bureau_id=init_params['bureau_id'],
                department_id=init_params['department_id'],
                branch_id=init_params['branch_id'],
                subcompany_id=init_params['subcompany_id'],
                jcgroup_id=init_params['jcgroup_id'],
                bureau_name=bureau_name,
                department_name=department_name,
                branch_name=branch_name,
                subcompany_name=subcompany_name,
                jcgroup_name=jcgroup_name
            )
            split_to_database(conn, init_params, params)
            continue
        else:
            print('str split error, has no-thinking scene ------  {0}'.format(user_data[1]))
    return True



def split_to_database(conn, init_params, params):
    id_dict = data_to_database(conn, **params)
    init_params['bureau_id'] = id_dict.get('bureau_id')
    init_params['department_id'] = id_dict.get('department_id')
    init_params['branch_id'] = id_dict.get('branch_id')
    init_params['subcompany_id'] = id_dict.get('subcompany_id')
    init_params['jcgroup_id'] = id_dict.get('jcgroup_id')
    init_params['init'] = id_dict.get('flag')


def data_to_database(sqlconn, **kwargs):
    user_id = kwargs.get('user_id')
    init = kwargs.get('init', True)
    jcgroup = kwargs.get('jcgroup_name', None)
    subcompany = kwargs.get('subcompany_name', None)
    branch = kwargs.get('branch_name', None)
    department = kwargs.get('department_name', None)
    bureau = kwargs.get('bureau_name', None)
    kv_dict = None
    if bureau:
        kv_dict = OrderedDict(jcgroup=jcgroup, subcompany=subcompany, branch=branch, department=department, bureau=bureau)
    elif department:
        kv_dict = OrderedDict(jcgroup=jcgroup, subcompany=subcompany, branch=branch, department=department)
    elif branch:
        kv_dict = OrderedDict(jcgroup=jcgroup, subcompany=subcompany, branch=branch)
    elif subcompany:
        kv_dict = OrderedDict(jcgroup=jcgroup, subcompany=subcompany)
    return_dict = {}
    will_insert_value = []
    table_list = ['jcgroup', 'subcompany', 'branch', 'department', 'bureau']
    relate_k = None
    relate_v = None
    if init:
        return_dict['flag'] = False
    for k, v in kv_dict.items():
        if v:
            if k == 'jcgroup':
                now_jcgroup_id = sqlconn.data_select_one('select {0}_id from account_{0} where {0} = "{1}"'.format(k, v))
            else:
                now_jcgroup_id = sqlconn.data_select_one('select {0}_id from account_{0} where {0} = "{1}" and {2}_id = {3}'.format(k, v, relate_k, relate_v))
            if now_jcgroup_id:
                return_dict['{0}_id'.format(k)] = kwargs.get('{0}_id'.format(k))
                if now_jcgroup_id[0] != return_dict['{0}_id'.format(k)]:
                    return_dict['{0}_id'.format(k)] = now_jcgroup_id[0]
                will_insert_value.append(return_dict['{0}_id'.format(k)])
            else:
                if not init:
                    try:
                        last_number = sqlconn.data_select_one('select {0}_id from account_{0} order by {0}_id desc'.format(k))[0]
                        return_dict['{0}_id'.format(k)] = last_number + 1
                    except Exception as e:
                        print(e)
                        return_dict['{0}_id'.format(k)] = kwargs.get('{0}_id'.format(k)) + 1
                else:
                    return_dict['{0}_id'.format(k)] = kwargs.get('{0}_id'.format(k))
                will_insert_value.append(return_dict['{0}_id'.format(k)])
                if k == 'jcgroup':
                    sqlconn.data_run_sql('insert into account_{0} ({0}, {0}_id) values ("{1}", {2})'.format(k, v, return_dict.get('{0}_id'.format(k))))
                else:
                    curr_pos = table_list.index(k)
                    columns_str_list = ', '.join(['{0}_id'.format(x) for x in table_list[0: curr_pos + 1]])
                    values_str = ', '.join([str(x) for x in will_insert_value[0: curr_pos + 1]])
                    sqlconn.data_run_sql('insert into account_{0} ({0}, {2}) values ("{1}", {3})'.format(k, v, columns_str_list, values_str))
            relate_k = k
            relate_v = return_dict['{0}_id'.format(k)]

    sqlconn.data_run_sql('update account_user set department_id = {0}, bureau_id = {1}, branch_id = {2} where user_ptr_id = {3}'.format(return_dict.get('department_id') if return_dict.get('department_id') else -1, return_dict.get('bureau_id') if return_dict.get('bureau_id') else -1, return_dict.get('branch_id') if return_dict.get('branch_id') else -1, user_id))
    return return_dict

def tree_id_data(tree_id, people):
    if tree_id == '1-1':
        return _get_all_tree_data(people)
    else:
        data_with_id = []
        select_item = {}
        selected = False
        for one_item in _get_all_tree_data(people):
            if one_item.get("id", '1-1') == tree_id:
                # one_item.update({"id": str(one_item.get('id'))})
                select_item = dict(one_item)
                break
            else:
                for two_item in one_item.get("children", []):
                    if two_item.get("id", '1-1') == tree_id:
                        # two_item.update({"id": str(two_item.get('id'))})
                        select_item = dict(two_item)
                        selected = True
                        break
                    else:
                        for three_item in two_item.get("children", []):
                            if three_item.get("id", '1-1') == tree_id:
                                # three_item.update({"id": str(three_item.get('id'))})
                                select_item = dict(three_item)
                                selected = True
                                break
                    if selected:
                        break
                if selected:
                    break
        data_with_id.append(select_item)
        return data_with_id


def _get_all_tree_data(people):
    all_tree_data = []
    temp_jc_data = JCGroup.objects.all()
    for jc_item in temp_jc_data:
        jc_path = jc_item.jcgroup
        jc_child = []
        temp_dep_data = Department.objects.filter(jcgroup_id=jc_item.jcgroup_id).all()
        for dep_item in temp_dep_data:
            dep_path = jc_path + "/" + dep_item.department
            dep_child = []
            temp_bur_data = Bureau.objects.filter(department_id=dep_item.department_id).all()
            for bur_item in temp_bur_data:
                bur_path = dep_path + "/" + bur_item.bureau
                people_child = []
                if people:
                    temp_peo_data = User.objects.filter(is_active=1, bureau_id=bur_item.bureau_id).all()
                    for peo_item in temp_peo_data:
                        peo_path = bur_path + "/" + peo_item.chinese_name
                        peo_dict = {
                            "id": '3-' + str(peo_item.id),
                            "pid": '2-' + str(bur_item.bureau_id),
                            "fullName": peo_item.chinese_name,
                            "fullPath": peo_path,
                            "abbrName": peo_item.chinese_name,
                            "nodeType": 3,
                        }
                        people_child.append(peo_dict)
                bur_dict = {
                    "id": '2-' + str(bur_item.bureau_id),
                    "pid": '2-' + str(dep_item.department_id),
                    "fullName": bur_item.bureau,
                    "fullPath": bur_path,
                    "abbrName": bur_item.bureau,
                    "nodeType": 2,
                    "children": people_child
                }
                dep_child.append(bur_dict)
            dep_dict = {
                "id": '2-' + str(dep_item.department_id),
                "pid": '1-' + str(jc_item.jcgroup_id),
                "fullName": dep_item.department,
                "fullPath": dep_path,
                "abbrName": dep_item.department,
                "nodeType": 2,
                "children": dep_child
            }
            jc_child.append(dep_dict)
        jc_dict = {
            "id": '1-' + str(jc_item.jcgroup_id),
            "pid": "",
            "fullName": jc_item.jcgroup,
            "fullPath": jc_item.jcgroup,
            "abbrName": jc_item.jcgroup,
            "nodeType": 1,
            "children": jc_child

        }
        all_tree_data.append(jc_dict)

    return all_tree_data


def sync_ldap_database(user, result):
    username = user.username if getattr(user, 'username', None) else '-1'
    if username not in result:
        user.delete()
        print('username({0}) is not in ldap, has been deleted'.format(user.chinese_name))
