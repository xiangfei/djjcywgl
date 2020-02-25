'''
Created on 2018年5月12日

@author: xiangfei
'''

REST_FRAMEWORK = {

    'EXCEPTION_HANDLER': 'utils.exception.jcgroup_exception_handler'

}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jcywgl',
        'USER': 'root',
        'PASSWORD': '1',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

PATH_ROOT = "/opt/jcywgl_file/import_files/"
EXAMPLE_ROOT = "/opt/jcywgl_file/example/"
