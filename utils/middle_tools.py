from django.utils.deprecation import MiddlewareMixin

class RequestHandle(MiddlewareMixin):

    def init(self):
        pass

    def process_request(self, request):
        if str(request.path_info).endswith('/'):
            pass
        else:
            request.path_info = request.path + '/'
        return None

