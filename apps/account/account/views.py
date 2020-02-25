from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from utils.token import TokenAuthentication
from .serializers import UsersSerializer
from .serializers import RoleSerializer
from .func import (
    func_login, func_user_list,
    func_data_sync, func_tree_data, func_user_status,
    func_role_list, func_role_add, func_role_info,
    func_role_info_edit, func_role_delete, func_author_availables,
    func_author_edit, func_role_users, func_roleusers_edit,
    func_dic_search, func_dic_edit, func_dic_add,
    func_dic_del, func_dic_list
)

# Create your views here.

from utils.permissions import check_permission ,list_permission
class LoginView(APIView):
    """用户登录管理"""
    def post(self, request):
        username = str(request.data['userName'])
        password = str(request.data['password'])
        ret = func_login(username, password)
        try:
            token = ret['data']['accessToken']
            request.session[token] = token
            request.session.set_expiry(3600)
        except:
            pass
        return Response(ret)


class LogoutView(APIView):
    """用户登出管理"""
    authentication_classes = (TokenAuthentication,)

    def post(self, request):

        try:
            token = request.token
            request.session[token] = None
            ret ={'code': 200, 'msg': '登出成功 ', 'data': ""}
        except:
            ret ={'code': 500, 'msg': '登出失败', 'data': ""}
        return Response(ret)


class UserListView(ListModelMixin, GenericAPIView):
    """获取用户列表以及用户查询"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = UsersSerializer

    @check_permission('account.view_user')
    @list_permission
    def post(self, request):
        username = request.data.get('username', None)
        department_id = request.data.get('department_id', None)
        page = int(request.data.get('page', 1))
        page_size = int(request.data.get('page_size', 20))
        user_status = request.data.get('user_status', '0')
        ret = func_user_list(username, department_id, page, page_size)
        return Response(ret)


class UserDataSyncView(APIView):
    """同步用户数据"""
    authentication_classes = (TokenAuthentication,)
 
    @check_permission('account.sync_user')
    def post(self, request):
        ret = func_data_sync()
        return Response(ret)


class UserTreeDataView(APIView):
    """获取组织树数据"""
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        tree_id = request.data.get('id', '1-1')
        if str(tree_id).strip() == "":
            tree_id = '1-1'
        person_flag = request.data.get('withPerson', False)
        ret = func_tree_data(tree_id, person_flag)
        return Response(ret)


class UserStatusModifyView(APIView):
    """修改用户状态"""
    authentication_classes = (TokenAuthentication, )

    @check_permission(['account.enable_user','account.disable_user'])
    def post(self, request):
        user_id = request.data.get('user_id', None)
        status_code = request.data.get('status', True)
        ret = func_user_status(user_id, status_code)
        return Response(ret)


class RoleListView(APIView):
    """获取角色列表"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = RoleSerializer
    @check_permission('account.view_role')
    @list_permission
    def post(self, request):
        role_name = request.data.get('role_name', '')
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 20)
        ret = func_role_list(role_name, page, page_size)
        return Response(ret)


class RoleAddView(APIView):
    """新增角色"""
    authentication_classes = (TokenAuthentication, )

    @check_permission('account.add_role')
    def post(self, request):
        role_name = request.data.get('role_name')
        role_desc = request.data.get('role_desc', "")
        ret = func_role_add(role_name, role_desc)
        return Response(ret)


class RoleInfoView(APIView):
    """获取角色信息"""
    authentication_classes = (TokenAuthentication, )

    @check_permission('account.view_role')
    def post(self, request):
        role_id = request.data.get('role_id', '')
        ret = func_role_info(role_id)
        return Response(ret)


class RoleEditInfoView(APIView):
    """编辑角色信息"""
    authentication_classes = (TokenAuthentication, )

    @check_permission('account.change_role')
    def post(self, request):
        role_id = request.data.get('role_id', '')
        role_name = request.data.get('role_name', '')
        role_desc = request.data.get('desc', '')
        ret = func_role_info_edit(role_id, role_name, role_desc)
        return Response(ret)


class RoleDeleteView(APIView):
    """删除角色"""
    authentication_classes = (TokenAuthentication, )

    @check_permission('account.delete_role')
    def post(self, request):
        role_id = request.data.get('role_id', '')
        ret = func_role_delete(role_id)
        return Response(ret)


class AuthorAvailableView(APIView):
    """查询角色可用权限"""
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        role_id = request.data.get('role_id', '')
        ret = func_author_availables(role_id)
        return Response(ret)


class AuthorEditView(APIView):
    """编辑角色权限"""
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        role_id = request.data.get('role_id', '')
        authority_ids = request.data.get('authority_ids', [])
        ret = func_author_edit(role_id, authority_ids)
        return Response(ret)


class RoleUsersView(APIView):
    """获取角色当前用户"""
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        role_id = request.data.get('role_id', '')
        ret = func_role_users(role_id)
        return Response(ret)


class RoleUsersEditView(APIView):
    """编辑角色当前用户"""
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        role_id = request.data.get('role_id', '')
        user_ids = request.data.get('user_ids', [])
        ret = func_roleusers_edit(role_id, user_ids)
        return Response(ret)


class DataDictionaryEditView(APIView):
    """获取数据字典"""
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        # result = {
        #     "module_tech": [
        #         {
        #             "title": "java",
        #             "value": '1'
        #         },
        #     ],
        #     "module_type": [
        #         {
        #             "title": "dubbo",
        #             "value": '1'
        #         },
        #     ]
        # }

        ret = func_dic_search()
        return Response(ret)

    def post(self, request):
        dic_id = request.data.get('dic_id', '')
        dic_name = request.data.get('dic_name', '')
        dic_content = request.data.get('dic_content', [])
        alias_name = request.data.get('alias_name', '')
        ret = func_dic_edit(dic_id, dic_name, dic_content, alias_name)
        return Response(ret)


class DataDictionaryAddView(APIView):
    """增加数据字典"""
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        dic_name = request.data.get('dic_name', '')
        dic_content = request.data.get('dic_content', [])
        alias_name = request.data.get('alias_name', '')
        ret = func_dic_add(dic_name, dic_content, alias_name)
        return Response(ret)


class DataDictionaryDelView(APIView):
    """删除数据字典"""
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        dic_id = request.data.get('dic_id', '')
        ret = func_dic_del(dic_id)
        return Response(ret)


class DataDictionarysView(APIView):
    """获取数据字典列表"""
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        search_key = request.data.get('search_key', '')
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 20)
        ret = func_dic_list(search_key, page, page_size)
        return Response(ret)
