##OpsManage是什么？
一款代码部署、应用部署、计划任务、设备资产管理平台。

##开发语言与框架：
 * 编程语言：Python2.7 + HTML + JScripts
 * 前端Web框架：Bootstrap
 * 后端Web框架：Django
 * 后端Task框架：Celery + Redis

##OpsManage环境要求
 * 编程语言：Python 2.7
 * 操作系统：CentOS 6+

##安装环境配置
一、安装Python
```
# yum install zlib zlib-devel readline-devel sqlite-devel bzip2-devel openssl-devel gdbm-devel libdbi-devel ncurses-libs kernel-devel libxslt-devel libffi-devel python-devel mysql-devel zlib-devel mysql-server -y
# wget http://mirrors.sohu.com/python/2.7.12/Python-2.7.12.tgz
# tar -xzvf Python-2.7.12.tgz
# cd Python-2.7.12
# ./configure
# make all
# make install
# make clean
# make distclean 
# mv /usr/bin/python /usr/bin/python2.6.6  
# ln -s /usr/local/bin/python2.7 /usr/bin/python 
# vi /usr/bin/yum  
将文件头部的
#!/usr/bin/python

改成
#!/usr/bin/python2.6.6
```
二、安装easy_install
```
# wget --no-check-certificate  https://pypi.python.org/packages/f7/94/eee867605a99ac113c4108534ad7c292ed48bf1d06dfe7b63daa51e49987/setuptools-28.0.0.tar.gz#md5=9b23df90e1510c7353a5cf07873dcd22
# tar -xzvf setuptools-28.0.0.tar.gz
# cd setuptools-28.0.0
# python  setup.py  install
```

三、安装pip
```
# wget --no-check-certificate https://github.com/pypa/pip/archive/1.5.5.tar.gz -O pip-1.5.5.tar.gz
# tar -xzvf pip-1.5.5.tar.gz
# cd pip-1.5.5/
# python setup.py install
```

四、安装模块
```
# pip install django==1.8.17
# pip install Celery 
# pip install django-celery 
# pip install celery-with-redis
# pip install djangorestframework
# pip install paramiko
# pip install ansible
# pip install redis
# pip install libvirt-python
# pip install supervisor
# pip install redis
# pip install MySQL-python
# pip install DBUtils
# pip install APScheduler-3.3.0
# pip install libvirt-python
# pip install pymongo==2.7.1
```
五、安装Redis
```
# wget http://download.redis.io/releases/redis-3.2.8.tar.gz
# tar -xzvf redis-3.2.8.tar.gz
# cd redis-3.2.8
# make
# make install
# vim redis.conf
```
修改以下配置
```
daemonize yes
loglevel warning
logfile "/var/log/redis.log"
```
```
# cd ../
# mv redis-3.2.8 /usr/local/redis
```
六、配置MySQL
```
# vim /etc/my.cnf
[mysqld]
default-character-set = utf8
character_set_server = utf8
添加以上字段

# mysql -uroot -p
mysql> create database opsmanage;
mysql> grant all privileges on opsmanage.* to root@'%' identified by 'welliam';
mysql>\q

# /etc/init.d/mysqld restart
```
七、配置OpsManage
```
# cd /path/OpsManage/OpsManage
# vim settings.py
BROKER_URL =  #修改成自己的配置
REDSI_KWARGS_LPUSH = #修改成自己的配置
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'opsmanage',
        'USER':'root',		#修改成自己的配置
        'PASSWORD':'welliam',	#修改成自己的配置
        'HOST':'192.168.1.233'  #修改成自己的配置
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
STATICFILES_DIRS = (
     ‘/path/OpsManage/OpsManage/static/',	#修改成自己的配置
    )
TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR,'mysite\templates'),
    ‘/path/OpsManage/OpsManage/templates/',	#修改成自己的配置
)

# cd ../
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver 192.168.1.233:8000
```
