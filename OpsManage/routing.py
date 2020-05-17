#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from websocket.consumers import webterminal
from deploy.consumers import AnsibleModel,AnsibleScript,AnsiblePlaybook
from apply.consumers import IpvsVipStatus
from cicd.consumers import AppsDeploy
from databases.mysql.consumers import MySQLWebTerminal
from databases.redis.consumers import RedisWebTerminal
from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            re_path(r'ssh/(?P<id>[0-9]+)/(?P<group_name>.*)/', webterminal),
            re_path(r'ansible/model/(?P<group_name>.*)/', AnsibleModel),
            re_path(r'ansible/script/(?P<group_name>.*)/', AnsibleScript),
            re_path(r'ansible/playbook/(?P<group_name>.*)/', AnsiblePlaybook),
            re_path(r'apps/deploy/(?P<id>[0-9]+)/(?P<group_name>.*)/', AppsDeploy),
            re_path(r'ipvs/stats/(?P<id>[0-9]+)/(?P<group_name>.*)/', IpvsVipStatus),
            re_path(r'mysql/terminal/(?P<id>[0-9]+)/(?P<group_name>.*)/', MySQLWebTerminal),
            re_path(r'redis/terminal/(?P<id>[0-9]+)/(?P<group_name>.*)/', RedisWebTerminal),
        ]),
    ),
})