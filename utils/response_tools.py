#coding=utf-8

import functools
import traceback

class http_code:
    success = {"code": 200, "status": "OK"}
    fail = {"code": 999, "status": "FAIL"}
    unauth = {"code": 401, "status": "UNAUTH"}


# 接口返回状态码
class ResponseCode(object):
    success = 200  # 接口正常, 业务正常
    func_error = 600  # 接口正常, 业务异常导致没有数据
    fail = 999  # 接口正常, 业务处理出现异常被捕获
    params_error = 301  # 参数异常


# 接口方法异常捕获
def except_hold(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except:
            traceback.print_exc()
            return {'code': ResponseCode.fail, 'msg': '接口异常', 'data': {}}
    return wrapper
