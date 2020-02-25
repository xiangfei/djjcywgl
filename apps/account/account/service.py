# coding=utf-8

from django.db.models import Q

from .models import User, Department, Role, RoleAuthority, Branch, DataDicName, DataDicContent
from apps.resources.servers.physical.models import Asset
from apps.resources.project.models import ModuleRecord
from utils.tools import gen_passwd
from utils.basic_ldap import myldap
from utils import origintree_tools, split_tools
from .serializers import RoleSerializer, UsersSerializer
from rest_framework.authtoken.models import Token


class AccountService(object):
    """
    用户管理类
    """

    def __init__(self, **kwargs):
        self.username = kwargs.get('username') or '-1'
        self.chinese_name = kwargs.get('chinese_name') or '-1'
        self.user_id = kwargs.get('user_id') or -1
        user = User.objects.filter(Q(id=self.user_id) | Q(username__contains=self.username) | Q(chinese_name__contains=self.chinese_name))
        if user:
            user = user[0]
            self.user_id = user.id
            self.username = user.username
            self.chinese_name = user.chinese_name

    def is_user_exist(self):
        """
        用户是否存在，用户名唯一
        """
        return True if self.user_id >= 0 else False

    def ldap_auth(self, password):
        """
        认证ldap
        """
        return myldap.auth(self.username, password)

    def comm_auth(self, password):
        """
        系统用户认证
        """
        return User.objects.filter(username=self.username, password=password).first()

    def raw_auth(self,password):
        return User.objects.filter(username=self.username, password=password).first()

    def login(self, password):
        """
        用户登录
        """
        if self.ldap_auth(password) or self.comm_auth(password) or self.raw_auth(password):
            valid_user = User.objects.filter(id=self.user_id, is_active=1).first()
            if not valid_user:
                return False, '', '用户已被禁用'
            user_obj = User.objects.get(id=self.user_id)
            try:
                token = Token.objects.get(user=user_obj)
                token.delete()
            except Token.DoesNotExist:
                pass
            token = Token.objects.create(user=user_obj)

            return True, token.key , '登录成功'
        else:
            return False, '', '用户名或密码错误'

    def list_user(self, username, department_id):
        """
        用户列表
        """
        role_instance = RolesService()
        node_type = ""
        if department_id:
            node_type = str(department_id).split('-')[0]
            department_id = split_tools.user_id_split(str(department_id))
        if username and department_id:
            branch_ids = [x.branch_id for x in Branch.objects.filter(jcgroup_id=department_id).all()]
            users = User.objects.filter(Q(chinese_name__contains=username), Q(department_id=department_id) | Q(bureau_id=department_id) | Q(branch_id__in=branch_ids))
        elif username:
            users = User.objects.filter(Q(chinese_name__contains=username))
        elif department_id:
            if node_type == '1':
                branch_ids = [x.branch_id for x in Branch.objects.filter(jcgroup_id=department_id).all()]
                users = User.objects.filter(Q(department_id=department_id) | Q(bureau_id=department_id) | Q(branch_id__in=branch_ids))
            else:
                users = User.objects.filter(Q(department_id=department_id) | Q(bureau_id=department_id))
        else:
            users = User.objects.filter().all()

        all_users = UsersSerializer(users, many=True).data
        all_users = [split_tools.dict_key_instead(user, {'user_id': 'id', 'user_name': 'chinese_name', 'ldap_name': 'username', 'status': 'is_active', 'role_name': 'role'}) for user in all_users]
        for user in all_users:
            user['status'] = True if user['status'] else False
            role_str = user['role_name']
            user['role_name'] = []
            for role_id in role_str.split(','):
                role_name = role_instance.get_roles_name(role_id)
                if role_name:
                    user['role_name'].append(role_name.name)
        return True, all_users

    def update_user(self, data):
        """
        更新用户
        """
        try:
            user = User.objects.filter(id=self.user_id).update(**data)
            user = User.objects.get(id=self.user_id)
        except:
            user = User(id=-1)
            return False, user
        return True, user

    def save_user(self, data):
        """
        保存用户
        """
        user = User(username=data.get('username'),
                    password=gen_passwd(),
                    email=data.get('email'),
                    mobile=data.get('mobile'),
                    chinese_name=data.get('chinese_name'),
                    ldap_dn=data.get('ldap_dn'),
                    )
        user.save()
        return True, user

    def get_tree_data(self, tree_id, person_flag):
        """
        获取组织树数据
        :param tree_id:
        :param person_flag:
        :return:
        bureau_id=10001,
        department_id=1001,
        branch_id=101,
        subcompany_id=11,
        jcgroup_id=1,
        """
        tree_id_select = int(split_tools.user_id_split(str(tree_id)))
        if 0 < tree_id_select <= 10:
            temp_data = origintree_tools.tree_id_data(tree_id, person_flag)
        elif 10 < tree_id_select <= 100:
            temp_data = []
        elif 100 < tree_id_select <= 1000:
            temp_data = []
        elif 1000 < tree_id_select <= 10000:
            temp_data = origintree_tools.tree_id_data(tree_id, person_flag)
        else:
            temp_data = origintree_tools.tree_id_data(tree_id, person_flag)
        return temp_data

class RolesService(object):
    """
    角色管理
    """

    @staticmethod
    def add_role(role_name, role_desc):
        """
        新增角色
        """
        try:
            role = Role(name=role_name, role_desc=role_desc)
            role.save()
        except:
            role = Role.objects.filter(name=role_name).first()
            return False, role.to_json()
        return True, role.to_json()

    def get_roles(self, role_name):
        """
        查询所有角色信息
        """
        if role_name == "":
            roles = Role.objects.all()
        else:
            # roles = Role.objects.filter(Role.role.like("{0}%".format(role_name))).all()
            roles = Role.objects.filter(name__contains=role_name)
        roles_list = RoleSerializer(roles, many=True).data
        roles_list = [split_tools.dict_key_instead(role, {'role_id': 'id', 'role_name': 'name', 'desc': 'role_desc'}) for role in roles_list]

        if roles:
            return roles_list
        else:
            return []

    def get_roles_name(self, role_id):
        role = Role.objects.filter(id=role_id).first()
        if role:
            return role.role
        return None

    def get_role_info(self, role_id):
        """
        查询当前角色信息
        """
        role = Role.objects.filter(id=role_id).first()
        if role:
            return role.to_json()
        else:
            return {}

    def update_role_info(self, role_id, role_name, role_desc):
        """
        更新角色信息
        """
        try:
            role = Role.objects.filter(id=role_id).update(**{"id": role_id, "name": role_name, "role_desc": role_desc})
            role = Role.objects.filter(id=role_id).first()
        except:
            return False, {}
        return True, role.to_json() if role else {}

    def del_role_info(self, role_id):
        """
        删除当前角色信息
        """
        try:
            role = Role.objects.filter(id=role_id).first()
            role_rn = Role.objects.filter(id=role_id).delete()
            if role:
                return True, role.to_json() if role_rn else {}
            else:
                return True, {}
        except:
            return False, {}

    def get_role_authoritys(self, role_id):
        """
        查询当前角色权限
        """
        role = Role.objects.filter(id=role_id).first()

        role_author_ids = role.author_id.split(',') if role.author_id else []
        role_used_ids = role.used_author_id.split(',') if role.used_author_id else []
        selected_ids = [str(x).strip() for x in role_used_ids]
        authors = []
        for author_id in role_author_ids:
            authority_id = str(author_id).strip()
            role_author = RoleAuthority.objects.filter(id=int(authority_id)).first()
            author_id_item = {
                "authority_id": authority_id,
                "authority_name": role_author.role_authority if role_author else "",
                "is_selected": True if authority_id in selected_ids else False,
                "authority_content": ""
            }
            authors.append(author_id_item)

        if role:
            return authors
        else:
            return []

    def update_role_authors(self, role_id, role_authors):
        """
        编辑角色权限
        """
        role_authors = ','.join([str(x) for x in role_authors])
        role = Role.objects.filter(id=role_id).first()
        role_author_id = ""
        if role:
            Role.objects.filter(id=role_id).update(**{"used_author_id": role_authors})
            try:
                role_author_id = Role.objects.filter(id=role_id).first().used_author_id
            except:
                role_author_id = ""
        if role_author_id == role_authors:
            return True
        else:
            return False

    def role_users_data(self, role_id):
        """
        查看当前角色所属用户
        """
        try:
            user_ids = []
            role = Role.objects.filter(id=role_id).first()
            users = role.user_set.all()
            for user in users:
                roles = [str(x.id).strip() for x in user.groups.all()]
                if str(role_id) in roles:
                    user = User.objects.get(pk = user.id)
                    user_info = user.to_json()
                    user_info.update({"user_id": "3-" + str(user_info["user_id"])})
                    user_ids.append(user_info)

            result_dict = {
                "role_id": role_id,
                "role_name": role.name,
                "user_ids": user_ids
            }
            return True, result_dict
        except Exception as e:
            print(e)
            return False, {}

    def role_users_edit(self, role_id, user_ids):
        """
        编辑当前角色所属用户
        """
        try:
            role = Role.objects.get(pk = role_id)
            role.user_set.clear()
            for user_id in user_ids:
                userinfo = User.objects.filter(id=int(user_id)).first()
                userinfo.groups.add(role)
                
            return True
        except Exception as e:
            print(e)
            return False


class DicService(object):

    def __init__(self, **kwargs):
        self.dic_id = int(kwargs.get('dic_id')) if kwargs.get('dic_id') else None

    def dic_edit(self, dic_name, dic_contents, alias_name):
        current_dic_name = DataDicName.objects.filter(id=self.dic_id).first()
        will_del_contents = DataDicContent.objects.filter(name_id=self.dic_id).all()
        in_use = None
        for del_content in will_del_contents:
            content = del_content.content
            if current_dic_name.aliasname in ['module_type', 'module_tech']:
                in_use = ModuleRecord.objects.filter(Q(module_type=content) | Q(module_tech=content))
            else:
                in_use = Asset.objects.filter(Q(tdtnamenid=content) | Q(idcnamenid=content) | Q(sfwnamenid=content) |
                                              Q(sfwnamenid=content) | Q(svrchangenid=content))
            if not in_use and del_content.content not in dic_contents:
                DataDicContent.objects.filter(id=del_content.id).first().delete()
        if alias_name:
            DataDicName.objects.filter(id=self.dic_id).update(**{"name": dic_name, "aliasname": alias_name})
        else:
            DataDicName.objects.filter(id=self.dic_id).update(**{"name": dic_name})
        dic_name_obj = DataDicName.objects.filter(id=self.dic_id).first()

        # DataDicContent.objects.filter(name_id=self.dic_id).all().delete()
        for dic_content in dic_contents:
            content_info_obj = DataDicContent.objects.filter(content=dic_content, name_id=dic_name_obj.id)
            if not content_info_obj:
                content_info = DataDicContent(content=dic_content, name=dic_name_obj)
                content_info.save()
        if in_use:
            return False
        return True

    def dic_add(self, dic_name, dic_contents, alias_name):
        dic_name_obj = DataDicName.objects.filter(name=dic_name).first()
        if not dic_name_obj:
            dic_name_obj = DataDicName(name=dic_name, aliasname=alias_name)
            dic_name_obj.save()
            dic_name_obj = DataDicName.objects.filter(name=dic_name, aliasname=alias_name).first()
        for dic_content in dic_contents:
            content_info_obj = DataDicContent.objects.filter(content=dic_content, name_id=dic_name_obj.id)
            if not content_info_obj:
                content_info = DataDicContent(content=dic_content, name=dic_name_obj)
                content_info.save()
        return dic_name_obj.id

    def dic_search(self):
        ret_dict = {}
        dicnames = DataDicName.objects.all()
        for dicname in dicnames:
            values = []
            diccontents = DataDicContent.objects.filter(name_id=dicname.id).all()
            for diccontent in diccontents:
                values.append({"title": diccontent.content, "value": diccontent.id})
            ret_dict[dicname.aliasname] = values
        return ret_dict

    def dic_del(self):
        will_del_contents = DataDicContent.objects.filter(name_id=self.dic_id).all()
        in_use = None
        for del_content in will_del_contents:
            in_use = Asset.objects.filter(Q(tdtnamenid=del_content) | Q(idcnamenid=del_content) | Q(sfwnamenid=del_content) |
                                          Q(sfwnamenid=del_content) | Q(svrchangenid=del_content))
        if not in_use:
            DataDicContent.objects.filter(name_id=self.dic_id).all().delete()
            DataDicName.objects.filter(id=self.dic_id).delete()
            return True
        else:
            return False

    def dic_list(self, search_key):
        dicnames = DataDicName.objects.all() if str(search_key).strip() == '' else DataDicName.objects.filter(name__contains=search_key)
        diclist = []
        for dicname in dicnames:
            diccontents = DataDicContent.objects.filter(name_id=dicname.id).all()
            diclist.append({"dic_id": dicname.id, "dic_name": dicname.name, "dic_aliasname": dicname.aliasname, "dic_content": [x.content for x in diccontents]})
        return diclist
