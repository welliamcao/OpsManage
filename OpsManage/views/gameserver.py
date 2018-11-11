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
@permission_required()
def gameserver_list(request,page):
    if request.method == "GET":
        gameserverconfig = GameServer_Config.objects.select_related().all()[0:100]
        pageinter = Paginator(gameserverconfig,10)
        try:
            gs_list = pageinter.page(page)
        except PageNotAnInteger:
            gs_list = pageinter.page(1)
        except EmptyPage:
            gs_list = pageinter.page(pageinter.num_pages)

        return render(request,'gameserver/gs_config.html',{"user":request.user,"gs_list":gs_list})
    if request.method == "POST":
        request.POST.get()
