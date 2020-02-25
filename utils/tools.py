#coding=utf-8

import uuid
import hashlib
import random

def md5(string):
    """
    md5
    upper 32 bit encryption
    """
    assert isinstance(string, str)

    hash = hashlib.md5()
    hash.update(string.encode('utf-8'))

    return hash.hexdigest().upper()


def make_uid(style=1,string=None):
    """
    根据不同风格生成uuid
    :param style:风格
    :param string:要加密的字符串
    :return:uuid
    """
    if string:
        assert isinstance(string,str)

    if style == 1:
        uid = uuid.uuid1()
    elif style == 3:
        uid = uuid.uuid3(uuid.NAMESPACE_DNS,string)
    elif style == 4:
        uid = uuid.uuid4()
    elif style == 5:
        uid = uuid.uuid5(uuid.NAMESPACE_DNS,string)
    else:
        pass

    return str(uid)

def gen_passwd():
    """
    随机生成6位数密码
    """
    code = []
    for i in range(6):
        if i == random.randint(1,5):
            code.append(str(random.randint(1,5)))
        else:
            code.append(chr(random.randint(65,90)))
    code_str = ''.join(code)
    return md5(code_str)