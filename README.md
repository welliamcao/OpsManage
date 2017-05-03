## OpsManage是什么？
一款代码部署、应用部署、计划任务、设备资产管理平台。

## 开发语言与框架：
 * 编程语言：Python2.7 + HTML + JScripts
 * 前端Web框架：Bootstrap
 * 后端Web框架：Django
 * 后端Task框架：Celery + Redis

## OpsManage环境要求
 * 编程语言：Python 2.7
 * 操作系统：CentOS 6+
 * Ansible版本：2.0 + 
 * 部署平台及节点服务器：Rsync 3+

## 安装环境配置
一、安装Python
```
# yum install zlib zlib-devel readline-devel sqlite-devel bzip2-devel openssl-devel gdbm-devel libdbi-devel ncurses-libs kernel-devel libxslt-devel libffi-devel python-devel mysql-devel zlib-devel mysql-server sshpass -y
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
# pip install ansible==2.2.2
# pip install redis
# pip install supervisor
# pip install redis
# pip install MySQL-python
# pip install DBUtils
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
bind 你的服务器ip地址
```
```
# cd ../
# mv redis-3.2.8 /usr/local/redis
# /usr/local/redis/src/redis-server /usr/local/redis/redis.conf
```
六、配置MySQL
```
# vim /etc/my.cnf
[mysqld]
default-character-set = utf8
character_set_server = utf8
添加以上字段
```
```
# mysql -uroot -p
mysql> create database opsmanage;
mysql> grant all privileges on opsmanage.* to root@'%' identified by 'password';
mysql>\q
# /etc/init.d/mysqld restart
```
七、配置OpsManage
```
# cd /path/OpsManage/OpsManage
# vim settings.py
BROKER_URL =  redis://192.168.1.233:6379/3 #修改成自己的配置
REDSI_KWARGS_LPUSH = {"host":'192.168.1.233','port':6379,'db':3} #修改成自己的配置
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
     ‘/yourpath/OpsManage/OpsManage/static/',	#修改成自己的配置
    )
TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR,'mysite\templates'),
    ‘/yourpath/OpsManage/OpsManage/templates/',	#修改成自己的配置
)
```
八、生成数据表与管理员账户
```
# cd /yourpath/OpsManage/
# python manage.py migrate
# python manage.py createsuperuser
```
九、启动部署平台
```
# cd /yourpath/OpsManage/
# python manage.py runserver ip:8000
```
十、配置证书认证
```
# ssh-keygen -t  rsa
# ssh-copy-id -i ~/.ssh/id_rsa.pub  root@ipaddress
```
十一、配置Celery异步任务系统
```
# echo_supervisord_conf > /etc/supervisord.conf
# vim /etc/supervisord.conf
最后添加
[program:celery-worker]
command=/usr/bin/python manage.py celery worker --loglevel=info -E -c 2
directory=/yourpath/OpsManage
stdout_logfile=/var/log/celery-worker.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1
启动celery
# /usr/local/bin/supervisord -c /etc/supervisord.conf
# supervisorctl status
```
Ansible部署功能：
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/ansible.gif)

代码部署：
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/project.gif)

资产管理：
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/assets.gif)

计划任务管理：
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/crontab.gif)

全局配置：
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/config.gif)

用户管理：
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/user.gif)
