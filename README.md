## OpsManage是什么？
一款代码部署、应用部署、计划任务、设备资产管理平台。

**开源协议**：[GNU General Public License v2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

**开源声明**：欢迎大家star或者fork我的开源项目，如果大家在自己的项目里面需要引用该项目代码，请在项目里面申明协议和版权信息。
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
 * MySQL版本：5.1-5.6

## OpsManage功能说明
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/opsmanage.png)

## Docker构建OpsManage
[传送门](https://github.com/welliamcao/OpsManage/wiki/Docker%E6%9E%84%E5%BB%BAOpsManage)

## Demo地址
[传送门](http://47.75.140.140:8896)
```
用户:demo 密码：demo
正在开发v3.0，demo环境暂时关闭.
```
## QQ交流群
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/qq_group.png)

## 安装环境配置(基于 CentOS7 )
一、安装依赖
```
# yum -y update
# yum -y install epel-release
# yum -y install zlib zlib-devel readline-devel bzip2-devel openssl-devel gdbm-devel libdbi-devel ncurses-libs kernel-devel libxslt-devel libffi-devel python-devel zlib-devel sshpass gcc git mariadb-devel
```
二、安装pip
```
# yum -y install python-pip
```

三、安装模块
```
# cd /mnt/
# git clone https://github.com/welliamcao/OpsManage.git
# cd /mnt/OpsManage/
# pip install -r requirements.txt  #注意，如果出现错误不要跳过，请根据错误信息尝试解决
```

四、安装Redis
```
# yum -y insatall redis
# systemctl enable redis
# systemctl start redis
```

五、安装MySQL
```
# yum -y install mariadb mariadb-devel mariadb-server
# systemctl enabled mysql.service
# systemctl start mysql.service
# mysql -uroot  # 初始密码为空
> create database opsmanage DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
> grant all privileges on opsmanage.* to opsmanage@'127.0.0.1' identified by 'weakPassword';
> quit
```
六、配置OpsManage
```
# cd /mnt/OpsManage/OpsManage
# vim settings.py
BROKER_URL =  redis://127.0.0.1:6379/3  # 如果redis在其他的服务器，请修改成自己的配置，格式是redis://[:password]@host:port/db
REDSI_KWARGS_LPUSH = {"host":'127.0.0.1','port':6379,'db':3}  # 如果redis在其他的服务器，请修改
SECRET_KEY = 'kd8f&jx1h^1m-uldfdo3d#10d9mbc-ijjz!tozusy@aw#h+875'  # 请随意输入随机字符串（推荐字符大于等于 50位）
DEBUG = False  # 生成环境推荐关闭，需要通过 nginx 代理访问
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'opsmanage',
        'USER':'opsmanage',	 # 修改成自己的配置
        'PASSWORD':'weakPassword',	# 修改成自己的配置
        'HOST':'127.0.0.1',  # 修改成自己的配置
        'PORT': 3306
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["/mnt/OpsManage/OpsManage/static/",'/mnt/OpsManage/OpsManage/templates/'],  # 如果安装路径不是/mnt，请修改成自己的路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
STATICFILES_DIRS = (
     '/mnt/OpsManage/OpsManage/static/',	# 如果安装路径不是/mnt，请修改成自己的路径
    )
TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR,'mysite\templates'),
    '/mnt/OpsManage/OpsManage/templates/',	# 如果安装路径不是/mnt，请修改成自己的路径
)
SFTP_CONF = {
             'port':22,
             'username':'root',
             'password':'welliam',
             'timeout':30
             }  # 请修改成有权限连接到OpsManage服务器的用户

```
七、生成数据表与管理员账户
```
# cd /mnt/OpsManage/
# python manage.py makemigrations OpsManage
# python manage.py makemigrations wiki
# python manage.py makemigrations orders
# python manage.py makemigrations filemanage
# python manage.py migrate
# python manage.py createsuperuser
```
八、启动部署平台
```
# cd /mnt/OpsManage/
# python manage.py runserver 0.0.0.0:8000  # 如果8000端口被其他端口占用，请修改成其他的端口
```
九、设置Nginx代理 (新开一个终端)
```
# yum -y install nginx
# vi /etc/nginx/nginx.conf
修改下面
server {
        listen       80 default_server;  # 对外端口
        listen       [::]:80 default_server;
        server_name  _;  # 如果有域名就修改成自己的域名
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
            proxy_pass http://localhost:8000;  # 如果OpsManage端口不是8000，请修改
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /static/ {
            root /mnt/OpsManage/OpsManage/;  # 静态资源，如果修改安装目录，此处需要修改
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
```
启动Nginx
```
# systemctl enable nginx
# firewall-cmd --zone=public --add-port=80/tcp --permanent  # 如果端口不是80，请修改
# firewall-cmd --reload
# setsebool -P httpd_can_network_connect 1  # selinux放行nginx
# systemctl start nginx
```
十、配置证书认证
```
# ssh-keygen -t  rsa
# ssh-copy-id -i ~/.ssh/id_rsa.pub  root@ipaddress
```
十一、配置Celery异步任务系统
```
# yum -y install supervisor
# systemctl enable supervisord
# echo_supervisord_conf > /etc/supervisord.conf
# export PYTHONOPTIMIZE=1
# vim /etc/supervisord.conf
最后添加
[program:celery-worker-default]
command=/usr/bin/python manage.py celery worker --loglevel=info -E -Q default
directory=/mnt/OpsManage
stdout_logfile=/var/log/celery-worker-default.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

[program:celery-worker-ansible]
command=/usr/bin/python manage.py celery worker --loglevel=info -E -Q ansible
directory=/mnt/OpsManage
stdout_logfile=/var/log/celery-worker-ansible.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

[program:celery-beat]
command=/usr/bin/python manage.py celery beat
directory=/mnt/OpsManage
stdout_logfile=/var/log/celery-beat.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

[program:celery-cam]
command=/usr/bin/python manage.py celerycam
directory=/mnt/OpsManage
stdout_logfile=/var/log/celery-celerycam.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

启动celery
# /usr/local/bin/supervisord -c /etc/supervisord.conf
# supervisorctl status #要检查是否都是running状态
```

十二、SQL审核
```
自行安装Inception与SQLadvisor，SQLadvisor可执行文件请放在OpsManage服务器/usr/bin/sqladvisor路径
```

## 提供帮助

如果您觉得OpsManage对您有所帮助，可以通过下列方式进行捐赠，谢谢！

![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/donate.png)

## 部分功能截图:
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
