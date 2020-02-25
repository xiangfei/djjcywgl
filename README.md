django 框架版的 jcywgl

django框架安装步骤

安装一个venv环境

1.查看python版本

先安装python3(同时pip3已安装)

2.pip3  install  virtualenv  

pip3 install virtualenv virtualenvwrapper

3.创建项目文件夹    

mkdir  djjcywgl

cd djjcywgl

4.virtualenv -p python3 djvenv --no-pip --no-setuptools --no-wheel --no-site-packages   #不使用系统包

5.进入虚拟环境
source djvenv/bin/activate

deactivate 

yum install gcc libffi-devel python-devel openssl-devel -y

需要自己安装pip /setuptools

wget --no-check-certificate  https://pypi.python.org/packages/source/p/pip/pip-8.0.2.tar.gz#md5=3a73c4188f8dbad6a1e6f6d44d117eeb

tar -zxvf pip-8.0.2.tar.gz

cd pip-8.0.2

python3 setup.py build

python3 setup.py install

wget --no-check-certificate  https://pypi.python.org/packages/source/s/setuptools/setuptools-19.6.tar.gz#md5=c607dd118eae682c44ed146367a17e26

tar -zxvf setuptools-19.6.tar.gz

cd setuptools-19.6.tar.gz

python3 setup.py build

python3 setup.py install


项目创建步骤

6.安装django框架所需包

pip3 install -r requirements.txt

7、8、9、10(直接从gitlab clone/pull代码即可)

7.创建工程(直接从gitlab clone/pull代码即可)

django-admin.py startproject jcywgl

8.创建app(直接从gitlab clone/pull代码即可)

cd jcywgl

python manage.py startapp account

python manage.py startapp resources

python manage.py startapp tasks

10.修改settting.py，将app加入到INSTALLED_APPS(直接从gitlab clone/pull代码即可)

11.修改数据库

default': { 'ENGINE': 'django.db.backends.mysql'
        'NAME': 'jcywgl',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',                  
    }

12.python manage.py makemigrations

13.python manage.py migrate

14.python manage.py runserver 0.0.0.0:8000
