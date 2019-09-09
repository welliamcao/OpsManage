#!/bin/bash
DATABASE=${MYSQL_DATABASE}
USER=${MYSQL_USER}
PASSWORD=${MYSQL_PASSWORD}

count=$(mysql -h db -D ${DATABASE} -e "show tables;" -u${USER} -p${PASSWORD}|wc -l)
if [ ${count} -lt 10  ];then
     mysql -h db -D ${DATABASE} -u${USER} -p${PASSWORD} < /data/apps/opsmanage/docker/init.sql
     cd /data/apps/opsmanage/ && python manage.py loaddata docker/superuser.json
fi
echo_supervisord_conf > /etc/supervisord.conf
export PYTHONOPTIMIZE=1
cat > /etc/supervisord.conf << EOF
[unix_http_server]
file=/tmp/supervisor.sock   

[supervisord]
logfile=/data/apps/opsmanage/logs/supervisord.log 
logfile_maxbytes=50MB        
logfile_backups=10           
loglevel=info                
pidfile=/var/run/supervisord.pid 
nodaemon=false               
minfds=1024                  
minprocs=200      
           
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock

[program:celery-worker-default]
command=celery -A OpsManage worker --loglevel=info -E -Q default -n worker-default@%%h
directory=/data/apps/opsmanage
stdout_logfile=/data/apps/opsmanage/logs/celery-worker-default.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

[program:celery-worker-ansible]
command=celery -A OpsManage worker --loglevel=info -E -Q ansible -n worker-ansible@%%h
directory=/data/apps/opsmanage
stdout_logfile=/data/apps/opsmanage/logs/celery-worker-ansible.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

[program:celery-beat]
command=celery -A OpsManage  beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
directory=/data/apps/opsmanage
stdout_logfile=/data/apps/opsmanage/logs/celery-beat.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1
EOF
supervisord -c /etc/supervisord.conf
sleep 3
cd /data/apps/opsmanage/
python manage.py runserver 0.0.0.0:8000 --http_timeout=1200
