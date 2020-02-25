from django.shortcuts import render
from .models import ProjectRecord, ModuleRecord
from .serializers import ModuleRecordSerializer, ProjectRecordSerializer, UserSerializer, GroupSerializer
from rest_framework.pagination import PageNumberPagination
#from django.contrib.auth.models import User, Group
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filter import ProjectFilter, ModuleFilter
from wsgiref.util import FileWrapper
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
import gitlab
import os
import random
import string
from apps.account.account.models import JCGroup, User, Department, Bureau
from django.db.models import Q, F
from utils import split_tools
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.token import TokenAuthentication
from utils.permissions import check_permission , list_permission
#class UserViewSet(viewsets.ModelViewSet):
#    """
#    允许用户查看或编辑的API路径。
#    """
#    queryset = User.objects.all().order_by('-date_joined')
#    serializer_class = UserSerializer


#class GroupViewSet(viewsets.ModelViewSet):
#    """
#    允许组查看或编辑的API路径。
#    """
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer


class AllPagination(PageNumberPagination):
    #默认每页显示的个数
    page_size = 10
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'page'
    #最多能显示多少页
    max_page_size = 100


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")


def user_id_split(user_id=None):
    if user_id:
        if isinstance(user_id, str):
            if '-' in user_id:
                user_id = user_id.split('-')[1]
        return user_id
    return ''


def user_exist(user_id):
    exist = User.objects.filter(id=user_id).first()
    if exist:
        return True
    return False


def get_username(user_id):
    user = User.objects.filter(id=int(user_id)).values('username')
    if user:
        username = user[0]['username']
        return username
    return ''


#@authentication()
class ProjectViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    #authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = ProjectRecord.objects.all().order_by('id')
    pagination_class = AllPagination
    serializer_class = ProjectRecordSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ProjectFilter
    search_fields = ('project_name',)


#@authentication()
class ModuleViewset(mixins.ListModelMixin,viewsets.GenericViewSet):

    queryset = ModuleRecord.objects.all().order_by('id')
    pagination_class = AllPagination
    serializer_class = ModuleRecordSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ModuleFilter
    search_fields = ('module_name',)


datadic = {
        "module_tech": [
            {
                "title": "java",
                "value": '1'
            },
        ],
        "module_type": [
            {
                "title": "dubbo",
                "value": '1'
            },
            {
                "title": "gateway",
                "value": '2'
            },
        ]
    }


global project_data_lists
global module_data_lists


class  ProjectRecordListView(APIView):
    authentication_classes = (TokenAuthentication, )
    serializer_class = ProjectRecordSerializer
    
    @check_permission('project.view_projectrecord')
    @list_permission
    def post(self, request):
        received_json_data = json.loads(request.body)
        project_name = received_json_data.get('project_name', '')
        department_id = received_json_data.get('department_id', None)
        organizational_id = received_json_data.get('organizational_id', None)
        starttime = received_json_data.get('starttime', datetime.now() - timedelta(weeks=48))
        endtime = received_json_data.get('endtime', datetime.now())

        if str(project_name) != "" and department_id and organizational_id:
            project_data_lists = ProjectRecord.objects.filter(project_name__contains=project_name, department_id=user_id_split(department_id), organizational_id=user_id_split(organizational_id), date_joined__lte=endtime, date_joined__gte=starttime)
        elif str(project_name) != "" and department_id:
            project_data_lists = ProjectRecord.objects.filter(project_name__contains=project_name, department_id=user_id_split(department_id), date_joined__lte=endtime, date_joined__gte=starttime)
        elif str(project_name) != "" and organizational_id:
            project_data_lists = ProjectRecord.objects.filter(project_name__contains=project_name, organizational_id=user_id_split(organizational_id), date_joined__lte=endtime, date_joined__gte=starttime)
        elif str(project_name) != "":
            project_data_lists = ProjectRecord.objects.filter(project_name__contains=project_name, date_joined__lte=endtime, date_joined__gte=starttime)
        elif department_id and organizational_id:
            project_data_lists = ProjectRecord.objects.filter(department_id=user_id_split(department_id), organizational_id=user_id_split(organizational_id), date_joined__lte=endtime, date_joined__gte=starttime)
        elif department_id:
            project_data_lists = ProjectRecord.objects.filter(department_id=user_id_split(department_id), date_joined__lte=endtime, date_joined__gte=starttime)
        elif organizational_id:
            project_data_lists = ProjectRecord.objects.filter(organizational_id=user_id_split(organizational_id), date_joined__lte=endtime, date_joined__gte=starttime)
        else:
            project_data_lists = ProjectRecord.objects.filter(date_joined__lte=endtime, date_joined__gte=starttime)
  
        page_size = int(received_json_data.get('page_size'))
        page = int(received_json_data.get('page'))

        talbelen = project_data_lists.count()

        if (page - 1) * page_size >= talbelen:
            ret = {'code': 200, 'msg': '获取服务列表成功', 'data': {'msgdata': [], 'total': talbelen, 'page_size': page_size, 'current_page': page}}

            # result = json.dumps(ret, default=json_date_handler)
            return Response(ret)
        else:
            start = (page - 1) * page_size
            end = page*page_size
            if page*page_size > talbelen:
                end = talbelen
            
            project_data_list = project_data_lists[start:end]

            llist = []
            for news in project_data_list:
                try:
                    organizational_name = JCGroup.objects.filter(id=int(user_id_split(news.organizational_id))).values('jcgroup')[0]['jcgroup']
                except:
                    organizational_name = ''
                depart_id = int(user_id_split(news.department_id))
                if 0 < depart_id <= 10:
                    department_name = JCGroup.objects.filter(jcgroup_id=int(split_tools.user_id_split(depart_id))).values('jcgroup')[0]['jcgroup'] if JCGroup.objects.filter(jcgroup_id=int(split_tools.user_id_split(depart_id))).values('jcgroup') else '',
                elif 10 < depart_id <= 100:
                    department_name = ''
                elif 100 < depart_id <= 1000:
                    department_name = ''
                elif 1000 < depart_id <= 10000:
                    department_name = Department.objects.filter(department_id=int(split_tools.user_id_split(depart_id))).values('department')[0]['department'] if Department.objects.filter(department_id=int(split_tools.user_id_split(depart_id))).values('department') else '',
                else:
                    department_name = Bureau.objects.filter(bureau_id=int(split_tools.user_id_split(depart_id))).values('bureau')[0]['bureau'] if Bureau.objects.filter(bureau_id=int(split_tools.user_id_split(depart_id))).values('bureau') else '',

                llist.append({
                    'id': news.id, 
                    'project_name': news.project_name,
                    'organizational_name': organizational_name,
                    'department_name': department_name,
                    'leader_name': get_username(user_id_split(news.supervisor_id)),
                    'desc': news.desc,
                    'date_joined': news.date_joined, 'service_num': ModuleRecord.objects.filter(child_of_project__id=news.id).count()})

            ret = {'code': 200, 'msg': '获取服务列表成功', 'data': {'msgdata': llist, 'total': talbelen, 'page_size': page_size, 'current_page': page}}

            # result = json.dumps(ret, default=json_date_handler)

            return Response(ret)


class  ProjectRecordAddView(APIView):
    authentication_classes = (TokenAuthentication, )
    serializer_class = ProjectRecordSerializer
    
    @check_permission('project.add_projectrecord')
    def post(self, request):
        received_json_data = json.loads(request.body)
        project_name = received_json_data.get('project_name')
        project = ProjectRecord.objects.filter(project_name=project_name)
        if project:
            return Response({'code': 200, 'msg': '项目名已存在，请重新命名', 'data': ""})
        else:
            gl = gitlab.Gitlab('http://git.jc', private_token='fFZjxzWn-osXh3PHzRBs', api_version='3')
            gl.groups.create({'name': project_name, 'path': project_name})
            supervisor_id = user_id_split(str(received_json_data.get('supervisor_id')))
            organizational_id = user_id_split(str(received_json_data.get('organizational_id')))
            department_id = user_id_split(str(received_json_data.get('department_id')))
            product_manager_id = ','.join([user_id_split(str(x)) for x in received_json_data.get('product_manager_id') if user_exist(user_id_split(str(x)))])
            develop_user_id = ','.join([user_id_split(str(x)) for x in received_json_data.get('develop_user_id') if user_exist(user_id_split(str(x)))])
            ops_user_id = ','.join([user_id_split(str(x)) for x in received_json_data.get('ops_user_id') if user_exist(user_id_split(str(x)))])
            test_user_id = ','.join([user_id_split(str(x)) for x in received_json_data.get('test_user_id') if user_exist(user_id_split(str(x)))])
            other_user_id = ','.join([user_id_split(str(x)) for x in received_json_data.get('other_user_id') if user_exist(user_id_split(str(x)))])
            received_json_data['supervisor_id'] = supervisor_id
            received_json_data['product_manager_id'] = product_manager_id
            received_json_data['develop_user_id'] = develop_user_id
            received_json_data['ops_user_id'] = ops_user_id
            received_json_data['test_user_id'] = test_user_id
            received_json_data['other_user_id'] = other_user_id
            received_json_data['department_id'] = department_id
            received_json_data['organizational_id'] = organizational_id
            ProjectRecord(**received_json_data).save()

            ret = {'code': 200, 'msg': '添加服务列表成功', "data": ""}
            # result = json.dumps(ret, default=json_date_handler)

            return Response(ret)


class ProjectRecordInfoView(APIView):
    authentication_classes = (TokenAuthentication, )
    serializer_class = ProjectRecordSerializer
    
    @check_permission('project.view_projectrecord')
    def post(self, request):
        received_json_data = json.loads(request.body)
        project_id = int(received_json_data.get('id', '0'))
        project_dic = {}
        project_obj = ProjectRecord.objects.filter(id=project_id).first()
        if not project_obj:
            return Response({'code': 200, 'msg': '没有查询到该项目', "data": "" })
        user_id = -1 if str(project_obj.supervisor_id).strip() == "" else project_obj.supervisor_id
        organ_id = -1 if str(project_obj.organizational_id).strip() == "" else project_obj.organizational_id
        depart_id = -1 if str(project_obj.department_id).strip() == "" else project_obj.department_id
        supervisor_name = User.objects.filter(id=int(split_tools.user_id_split(user_id))).values('username')[0]['username'] if User.objects.filter(id=int(split_tools.user_id_split(user_id))).values('username') else ''
        organizational_name = JCGroup.objects.filter(id=int(split_tools.user_id_split(organ_id))).values('jcgroup')[0]['jcgroup'] if JCGroup.objects.filter(id=int(split_tools.user_id_split(organ_id))).values('jcgroup') else '',
        departm_id = int(split_tools.user_id_split(depart_id))
        if 0 < departm_id <= 10:
            department_name = JCGroup.objects.filter(jcgroup_id=int(split_tools.user_id_split(departm_id))).values('jcgroup')[0]['jcgroup'] if JCGroup.objects.filter(jcgroup_id=int(split_tools.user_id_split(departm_id))).values('jcgroup') else '',
        elif 10 < departm_id <= 100:
            department_name = ''
        elif 100 < departm_id <= 1000:
            department_name = ''
        elif 1000 < departm_id <= 10000:
            department_name = Department.objects.filter(department_id=int(split_tools.user_id_split(departm_id))).values('department')[0]['department'] if Department.objects.filter(department_id=int(split_tools.user_id_split(departm_id))).values('department') else '',
        else:
            department_name = Bureau.objects.filter(bureau_id=int(split_tools.user_id_split(departm_id))).values('bureau')[0]['bureau'] if Bureau.objects.filter(bureau_id=int(split_tools.user_id_split(departm_id))).values('bureau') else '',

        dict1 = {}
        product_manager = project_obj.product_manager_id.split(',')
        userlist = []
        product_manager_ids = []
        for i in product_manager:
            if i.strip() == "":
                continue
            username = get_username(int(i))
            if username:
                userlist.append(username)
                product_manager_ids.append(i)
        dict1['product_manager_name'] = userlist

        develop_user_ids = []
        develop_user = project_obj.develop_user_id.split(',')
        userlist = []
        for i in develop_user:
            if i.strip() == "":
                continue
            username = get_username(int(i))
            if username:
                userlist.append(username)
                develop_user_ids.append(i)
        dict1['develop_user_name'] = userlist

        ops_user_ids = []
        ops_user = project_obj.ops_user_id.split(',')
        userlist = []
        for i in ops_user:
            if i.strip() == "":
                continue
            username = get_username(int(i))
            if username:
                userlist.append(username)
                ops_user_ids.append(i)
        dict1['ops_user_name'] = userlist

        test_user = project_obj.test_user_id.split(',')
        test_user_ids = []
        userlist = []
        for i in test_user:
            if i.strip() == "":
                continue
            username = get_username(int(i))
            if username:
                userlist.append(username)
                test_user_ids.append(i)
        dict1['test_user_name'] = userlist

        other_user = project_obj.other_user_id.split(',')
        other_user_ids = []
        userlist = []
        for i in other_user:
            if i.strip() == "":
                continue
            username = get_username(int(i))
            if username:
                userlist.append(username)
                other_user_ids.append(i)
        dict1['other_user_name'] = userlist

        project_info = {'id': project_obj.id, 'project_name': project_obj.project_name,
                        'organizational_id': '1-' + str(project_obj.organizational_id),
                        'department_id': '2-' + str(project_obj.department_id) if int(project_obj.department_id) > 10 else '1-' + str(project_obj.department_id),
                        'supervisor_id': '3-' + str(project_obj.supervisor_id),
                        'organizational_name': organizational_name,
                        'department_name': department_name,
                        'supervisor_name': supervisor_name,
                        'product_manager_name': dict1.get('product_manager_name'),
                        'product_manager_id': ['3-' + str(x) for x in product_manager_ids],
                        'develop_user_name': dict1.get('develop_user_name'),
                        'develop_user_id': ['3-' + str(x) for x in develop_user_ids],
                        'ops_user_name': dict1.get('ops_user_name'),
                        'ops_user_id': ['3-' + str(x) for x in ops_user_ids],
                        'test_user_name': dict1.get('test_user_name'),
                        'test_user_id': ['3-' + str(x) for x in test_user_ids],
                        'other_user_name': dict1.get('other_user_name'),
                        'other_user_id': ['3-' + str(x) for x in other_user_ids],
                        'desc': project_obj.desc,
                        'online_time': project_obj.online_time,
                        'service_num': project_obj.service_num,}

        module_obj = ModuleRecord.objects.filter(child_of_project__id=project_id)
        module_info = []
        for i in module_obj:
            module_info.append({'module_name': i.module_name, 'module_version': i.version_num})
        version_info = [{"version_num": " ",  "online_time": " "}]
        project_dic['basic_info'] = project_info
        project_dic['module_info'] = module_info
        project_dic['version_info'] = version_info

        ret = {'code': 200, 'msg': '获取服务详情成功', 'data': project_dic}

        # result = json.dumps(ret, default=json_date_handler)

        return Response(ret)


class ModulerecordUpdateView(APIView):

    authentication_classes = (TokenAuthentication, )
    serializer_class = ModuleRecordSerializer
    
    @check_permission('project.change_modulerecord')
    def post(self, request):

        received_json_data = json.loads(request.body)
        module_id = received_json_data.get('id')

        ModuleRecord.objects.filter(id=module_id).update(**received_json_data, date_updated=datetime.now())
 
        ret = {'code': 200, 'msg': '更新项目成功', 'data': ''}
        # result = json.dumps(ret, default=json_date_handler)
    
        return Response(ret)


class ProjectRecordUpdateView(APIView):
    authentication_classes = (TokenAuthentication, )
    serializer_class = ProjectRecordSerializer
    
    @check_permission('project.change_projectrecord')
    def post(self, request):
        received_json_data = json.loads(request.body)
        project_id = received_json_data.get('id')

        received_json_data['department_id'] = split_tools.user_id_split(received_json_data.get("department_id", ""))
        received_json_data['supervisor_id'] = split_tools.user_id_split(received_json_data.get("supervisor_id", ""))
        received_json_data['product_manager_id'] = split_tools.project_userid_split(received_json_data.get("product_manager_id", []))
        received_json_data['ops_user_id'] = split_tools.project_userid_split(received_json_data.get("ops_user_id", []))
        received_json_data['develop_user_id'] = split_tools.project_userid_split(received_json_data.get("develop_user_id", []))
        received_json_data['test_user_id'] = split_tools.project_userid_split(received_json_data.get("test_user_id", []))
        received_json_data['other_user_id'] = split_tools.project_userid_split(received_json_data.get("other_user_id", []))

        ProjectRecord.objects.filter(id=project_id).update(**received_json_data, date_updated=datetime.now())

        ret = {'code': 200, 'msg': '更新项目成功', 'data': ''}
        # result = json.dumps(ret, default=json_date_handler)
    
        return Response(ret)


class ModulerecordAddView(APIView):

    authentication_classes = (TokenAuthentication, )
    serializer_class = ModuleRecordSerializer
    
    @check_permission('project.add_modulerecord')
    def post(self, request):

        received_json_data = json.loads(request.body)
        module_name = received_json_data.get('module_name')
        module = ModuleRecord.objects.filter(module_name=module_name)
        if module:
            return Response({'code': 500, 'msg': '服务名已存在，请重新命名', "data": ""})
        else:
            project_id = received_json_data.get('project_id')
            project = ProjectRecord.objects.get(id=int(project_id))
            received_json_data.pop('project_id')
            received_json_data['is_public'] = received_json_data.pop('publicservice')
            project_name = project.project_name
            gl = gitlab.Gitlab('http://git.jc', private_token='fFZjxzWn-osXh3PHzRBs', api_version='3')
            group_id = gl.groups.list(search=project_name)[0].id
            module_git = gl.projects.create({'name': module_name, 'namespace_id': group_id})
            received_json_data['git_url'] = module_git.web_url
            project_type = received_json_data.get('module_type')
            cmd = 'cd {0}/script/jcwf/ && python2 project_gen_args.py {1} {2} {3}'.format(os.getcwd(), project_name, module_name, project_type)
            result = os.system(cmd)
            if 0 == result:
                file_name = project_name + '-' + module_name + '.zip'
                files_dir = ''.join(random.sample(string.ascii_lowercase, 8))
                received_json_data['file_name'] = file_name
                received_json_data['files_dir'] = files_dir

                ModuleRecord(**received_json_data, child_of_project=project).save()

            ret = {'code': 200, 'msg': '添加服务成功', 'data': ''}
            # result = json.dumps(ret, default=json_date_handler)
    
            return Response(ret)


def module_file_download(request, random_str):
    #file_path, file_name = '', ''
    import json
    FileUploadDir = '/home/djjcywgl/jcywgl'
    if request.method == "POST":
        file_path = "%s/downloads" % (FileUploadDir, )
        received_json_data = json.loads(request.body)
        file_name = received_json_data['file_name']
        zip_file_name = "%s/%s" % (file_path, file_name)
        wrapper = FileWrapper(open(zip_file_name, 'rb'))
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=%s' % (urlquote(zip_file_name))

        return response



class ModulerecordInfoView(APIView):

    authentication_classes = (TokenAuthentication, )
    serializer_class = ModuleRecordSerializer
    
    @check_permission('project.view_modulerecord')
    def post(self, request):
#         user_id = request.user
        received_json_data = json.loads(request.body)
        module_id = received_json_data.get('id')
        module_obj = ModuleRecord.objects.get(id=module_id)
        module_info = {'id': module_obj.id, 'module_name': module_obj.module_name, 'module_tech': module_obj.module_tech, 'logs_path': module_obj.logs_path, 'module_path': module_obj.module_path, 'port': module_obj.port,  'module_type': module_obj.module_type, 'desc': module_obj.desc, 'status': module_obj.status, 'git_url': module_obj.git_url, 'version_num': module_obj.version_num,
                       'publicservice': module_obj.is_public,
                       'supervisor': get_username(user_id_split(ProjectRecord.objects.filter(modulerecord__id__contains=module_id).values('supervisor_id')[0]['supervisor_id'])),
                       }

        ret = {'code': 200, 'msg': '获取服务详情成功', 'data': module_info}
        # result = json.dumps(ret, default=json_date_handler)

        return Response(ret)


class ModulerecordDeleteView(APIView):

    authentication_classes = (TokenAuthentication, )
    serializer_class = ModuleRecordSerializer
    
    @check_permission('project.delete_modulerecord')
    def post(self, request):
        received_json_data = json.loads(request.body)
        module_id = received_json_data.get('id')
        module_status = received_json_data.get('status')

        ModuleRecord.objects.filter(id=module_id).update(status=0 if module_status else 1, date_updated=datetime.now())

        ret = {'code': 200, 'msg': '服务状态成功', 'data': ''}
        # result = json.dumps(ret, default=json_date_handler)

        return Response(ret)


class ModulerecordListView(APIView):
    authentication_classes = (TokenAuthentication, )
    serializer_class = ModuleRecordSerializer
    
    @check_permission('project.view_modulerecord')
    @list_permission
    def post(self, request):
        received_json_data = json.loads(request.body)
        module_name = received_json_data.get('module_name', '')
        is_public = received_json_data.get('publicservice', None)
        child_of_project = received_json_data.get('project_id', None)
        starttime = received_json_data.get('starttime', datetime.now() - timedelta(weeks=48))
        endtime = received_json_data.get('endtime', datetime.now())

        if str(module_name).strip() != "" and is_public is not None:
            module_data_lists = ModuleRecord.objects.filter(module_name__contains=module_name, is_public=1 if is_public else 0, date_joined__lte=endtime, date_joined__gte=starttime)
        elif str(module_name).strip() != "":
            module_data_lists = ModuleRecord.objects.filter(module_name__contains=module_name, date_joined__lte=endtime, date_joined__gte=starttime)
        elif is_public is not None:
            module_data_lists = ModuleRecord.objects.filter(is_public=1 if is_public else 0, date_joined__lte=endtime, date_joined__gte=starttime)
        elif child_of_project:
            module_data_lists = ModuleRecord.objects.filter(child_of_project=child_of_project, date_joined__lte=endtime, date_joined__gte=starttime)
        else:
            module_data_lists = ModuleRecord.objects.filter(date_joined__lte=endtime, date_joined__gte=starttime)

        page_size = int(received_json_data.get('page_size'))
        page = int(received_json_data.get('page'))

        talbelen = module_data_lists.count()

        if (page - 1) * page_size >= talbelen:
            return Response({'code': 200, 'msg': 'no match data', 'data': {"msgdata": [], "current_page": page, "page_size": page_size, "total": talbelen}})
        else:
            start = (page - 1) * page_size
            end = page*page_size
            if page*page_size > talbelen:
                end = talbelen

            module_data_list = module_data_lists[start:end]

            llist = []
            for module_obj in module_data_list:
                llist.append({'id': module_obj.id, 
                    'project_name': ProjectRecord.objects.filter(id=module_obj.child_of_project.id).values('project_name')[0]['project_name'] ,
                    'date_joined': module_obj.date_joined, 'module_name': module_obj.module_name, 
                    'module_tech': datadic['module_tech'][0]['title'], 'logs_path': module_obj.logs_path, 'module_path': module_obj.module_path, 'port': module_obj.port,  'module_type': datadic['module_type'][0]['title'], 'desc': module_obj.desc, 'status': module_obj.status, 'git_url': module_obj.git_url, 'version_num': module_obj.version_num,
                    'file_name': module_obj.file_name, 'files_dir': module_obj.files_dir, })

            ret = {'code': 200, 'msg': '获取服务列表成功', 'data': {'msgdata': llist, 'total': talbelen, 'page_size': page_size, 'current_page': page}}

            # result = json.dumps(ret, default=json_date_handler)

            return Response(ret)
