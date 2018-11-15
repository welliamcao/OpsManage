#!/usr/bin/env python
# _#_ coding:utf-8 _*_
import uuid,os,json
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OpsManage.models import Server_Assets, Network_Assets
from OpsManage.data.DsRedisOps import DsRedis
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.contrib.auth.models import User,Group
from OpsManage.models import (Ansible_Playbook,Ansible_Playbook_Number,
                              Log_Ansible_Model,Log_Ansible_Playbook,
                              Ansible_CallBack_Model_Result,Service_Assets,
                              Ansible_CallBack_PlayBook_Result,Assets,
                              Ansible_Script,Project_Assets,Ansible_Inventory,
                              Ansible_Inventory_Groups,Ansible_Inventory_Groups_Server,
                              GameServer_Update_List,GameServer_Config,Log_GameServer)
from OpsManage.data.DsMySQL import AnsibleRecord
from django.contrib.auth.decorators import permission_required
from OpsManage.utils.logger import logger
from dao.assets import AssetsSource
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required()
@permission_required('OpsManage.can_read_gameserver_config',login_url='/noperm/')
def gamehost_list(request):
    gshost = []
    ips = GameServer_Config.objects.values_list("ip__ip",flat=True)
    totalgame = GameServer_Config.objects.all().count()
    onlinegame = 0
    offlinegame = GameServer_Config.objects.filter(state=False).count()
    for ip in ips:
        sid = Server_Assets.objects.get(ip=ip).id
        aid = Server_Assets.objects.get(ip=ip).assets.id
        business = Project_Assets.objects.get(id=Assets.objects.get(id=aid).business).project_name
        hostname = Server_Assets.objects.get(ip=ip).hostname
        system = Server_Assets.objects.get(ip=ip).system
        gonlinegame = GameServer_Config.objects.filter(state=True,ip__ip=ip).count()
        status = Assets.objects.get(id=aid).status
        game = list(GameServer_Config.objects.filter(ip__ip=ip).values_list("name",flat=True))
        onlinegame = onlinegame+gonlinegame
        gshost.append(
            {
                'game': game,
                'aid':aid,
                'sid':sid,
                'business':business,
                'hostname':hostname,
                'ip':ip,
                'system':system,
                'onlinegame':gonlinegame,
                'status':status,
            }
        )
    return render(request,'gameserver/gs_config.html',{"user":request.user,"totalGame":totalgame,"onlineGame":onlinegame,"offlineGame":offlinegame,"gshost":gshost},)

@login_required()
@permission_required('OpsManage.can_read_gameserver_config')
def gameserver_details(request):
    gameserver_list = GameServer_Config.objects.all()[0:300]
    if request.method == "GET" :
        #rungame = ANSRunner.run_model()
        return render(request.user,{"gs_list":gameserver_list})
    if request.method == "POST" and request.user.has_perm('OpsManage.can_change_gameserver_config'):
        pass
    if request.method == "DELETE" and request.user.has_perm('OpsManage.can_delete_gameserver_config'):
        pass


