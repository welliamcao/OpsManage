## OpsManage是什么？
一款代码部署、应用部署、计划任务、设备资产管理平台。

**开源协议**：[GNU General Public License v2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

**开源声明**：欢迎大家star或者fork我的开源项目，如果大家在自己的项目里面需要引用该项目代码，请在项目里面申明协议和版权信息。
## 开发语言与框架：
 * 编程语言：Python3.6 + HTML + JScripts
 * 前端Web框架：Bootstrap
 * 后端Web框架：Django
 * 后端Task框架：Celery + Redis

## OpsManage环境要求
 * 编程语言：Python 3.6
 * 操作系统：CentOS 6+
 * Ansible版本：2.6 + 
 * 部署平台及节点服务器：Rsync 3+
 * MySQL版本：5.1-5.6

## OpsManage功能说明
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/opsmanage.png)

## QQ交流群
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/qq_group.png)

## 安装环境配置
一、安装Python
```
# yum install zlib zlib-devel readline-devel sqlite-devel bzip2-devel openssl-devel gdbm-devel libdbi-devel ncurses-libs kernel-devel libxslt-devel libffi-devel python-devel zlib-devel openldap-devel sshpass gcc git -y
# yum install http://www.percona.com/downloads/percona-release/redhat/0.1-6/percona-release-0.1-6.noarch.rpm
# yum install Percona-Server-server-56 install Percona-Server-devel-56
# wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz  #CentOS 7不用安装python2.7
# tar -xzvf Python-3.6.6.tgz
# cd Python-3.6.6
# ./configure --prefix=/usr/local/python3
# make all
# make install
# make clean
# make distclean  
# ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```


二、安装模块
```
# cd /mnt/
# git clone -b v3 https://github.com/welliamcao/OpsManage.git
# cd /mnt/OpsManage/
# pip3 install -r requirements.txt  #CentOS 7使用pip3
```

三、安装Redis
```
# wget http://download.redis.io/releases/redis-3.2.8.tar.gz
# tar -xzvf redis-3.2.8.tar.gz
# cd redis-3.2.8
# make
# make install
# vim redis.conf
```
修改以下配置（不要配置认证）
```
daemonize yes
loglevel warning
logfile "/var/log/redis.log"
bind 你的服务器ip地址
例如： bind 127.0.0.1 192.168.88.201
```
```
# cd ../
# mv redis-3.2.8 /usr/local/redis
# /usr/local/redis/src/redis-server /usr/local/redis/redis.conf
```
四、安装MySQL
```
# vim /etc/my.cnf
[mysqld]
character_set_server = utf8
添加以上字段
# /etc/init.d/mysqld restart     	#centos 6
# systemctl start mysql.service 	#centos 7
# mysql -uroot -p  				#初始密码为空，直接回车就行
mysql> create database opsmanage DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
mysql> grant all privileges on opsmanage.* to root@'%' identified by 'password';
mysql>\q
```
五、配置OpsManage
```
# cd /mnt/OpsManage/conf
# vim opsmanage.ini
根据自己的情况修改配置

```
六、生成数据表与管理员账户
```
# cd /mnt/OpsManage/
# /usr/local/python3/bin/python3 manage.py makemigrations wiki
# /usr/local/python3/bin/python3 manage.py makemigrations orders
# /usr/local/python3/bin/python3 manage.py makemigrations filemanage
# /usr/local/python3/bin/python3 manage.py makemigrations navbar
# /usr/local/python3/bin/python3 manage.py makemigrations databases
# /usr/local/python3/bin/python3 manage.py makemigrations asset
# /usr/local/python3/bin/python3 manage.py makemigrations deploy
# /usr/local/python3/bin/python3 manage.py makemigrations cicd
# /usr/local/python3/bin/python3 manage.py makemigrations sched
# /usr/local/python3/bin/python3 manage.py makemigrations apply
# /usr/local/python3/bin/python3 manage.py migrate
# /usr/local/python3/bin/python3 manage.py createsuperuser  #创建管理员账户与密码
```
```
# 如果出现错误ImportError: cannot import name 'LDAPError'
pip3 uninstall python-ldap
pip3 install --upgrade python-ldap
```
九、启动部署平台
```
# cd /mnt/OpsManage/
# /usr/local/python3/bin/python3 manage.py runserver 0.0.0.0:8000
```


十、使用OpsManage分布式任务调度功能，不使用的话可以不进行下面的步骤
```
# mkdir -p /usr/local/opsched
# cp /mnt/OpsManage/opsched/* /usr/local/opsched/
# vim /usr/local/opsched/sched.conf 
# 注意修改里面secret跟ops_address的值，修改成自己的配置
# /usr/local/opsched/opsched -f /usr/local/opsched/sched.conf -a check      #检查配置看看有没有报错
# /usr/local/opsched/opsched -f /usr/local/opsched/sched.conf -a runserver  #正式运行 
```



