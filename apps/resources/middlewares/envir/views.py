from utils.token import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .func import (
    func_env_list, func_env_add, func_env_info,
    func_env_del, func_env_edit, func_env_upload,
    func_env_download,
)

# Create your views here.


class EnvListView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        search_key = request.data.get('env_key', None)
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 20)
        ret = func_env_list(search_key, page, page_size)
        return Response(ret)


class EnvAddView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        env_name = request.data.get('env_name', '')
        desc = request.data.get('desc', '')
        file_id = request.data.get('file_id', '')
        ret = func_env_add(env_name, desc, file_id)
        return Response(ret)


class EnvInfoView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        env_id = request.data.get('env_id', '')
        ret = func_env_info(env_id)
        return Response(ret)


class EnvDeleteView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        env_id = request.data.get('env_id', '')
        ret = func_env_del(env_id)
        return Response(ret)


class EnvEditView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        env_id = request.data.get('env_id', '')
        env_name = request.data.get('env_name', '')
        desc = request.data.get('desc', '')
        file_id = request.data.get('file_id', '')
        ret = func_env_edit(env_id, env_name, desc, file_id)
        return Response(ret)


class EnvUploadView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        File = request.FILES.get("file", None)
        ret = func_env_upload(File)
        return Response(ret)


class EnvDownloadView(APIView):
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        file_id = request.query_params.get('file_id')
        ret = func_env_download(file_id)
        return ret
