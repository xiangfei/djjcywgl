'''
Created on 2018年5月12日

@author: xiangfei
'''
from .settings import *

REST_FRAMEWORK = {

    'EXCEPTION_HANDLER': 'utils.exception.jcgroup_exception_handler'

}

if os.name == 'nt':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'jcywgl',
            'USER': 'root',
            'PASSWORD': '123456',
            'HOST': '10.0.50.38',
            'PORT': '3306',  
            #'ENGINE': 'django.db.backends.sqlite3',
            #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'jcywgl',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
PATH_ROOT = "/Users/"
EXAMPLE_ROOT = "/Users/"
