from celery import task
from .func import celery_sync


@task(name='account.tasks.func_name')    #appname为当前app注册的名字
def func_name():
    print('start sync ldap data')
    celery_sync()
    print('end sync ldap data')
