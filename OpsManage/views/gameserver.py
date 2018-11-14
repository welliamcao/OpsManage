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
@permission_required('OpsManage.can_change_gameserver_config',login_url='/noperm/')
def gameserver_list(request):
    gshost = []
    gameserverconfig = GameServer_Config.objects.select_related().all()[0:300]
    ips = GameServer_Config.objects.values_list("ip",flat=True).distinct()
    for ip in ips:
        aid = Assets.objects.get(ip=ip).id
        sid = Server_Assets.objects.get(ip=ip).id
        business = Assets.objects.get(ip=ip).business
        hostname = Server_Assets.objects.get(ip=ip).hostname
        system = Server_Assets.objects.get(ip=ip).system
        onlinegame = GameServer_Config.objects.filter(state=True,ip=ip).count()
        status = Assets.objects.get(ip=ip).status
        game = GameServer_Config.objects.filter(ip=ip).values_list("name",flat=True)
        gshost.append(
            {
                "aid":aid,
                "sid":sid,
                "business":business,
                "hostname":hostname,
                "ip":ip,
                "system":system,
                "onlinegame":onlinegame,
                "game":game,
                "status":status,
            }
        )
    return render(request,'gameserver/gs_config.html',{"user":request.user,"gshost":gshost})
def gamehost_facts(){

}
