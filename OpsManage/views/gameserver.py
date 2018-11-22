#!/usr/bin/env python
# _#_ coding:utf-8 _*_
import json
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OpsManage.data.DsRedisOps import DsRedis
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.contrib.auth.models import User,Group
from OpsManage.models import (Ansible_Playbook,Ansible_Playbook_Number,
                              Log_Ansible_Model,Log_Ansible_Playbook,
                              Ansible_CallBack_Model_Result,Service_Assets,
                              Ansible_CallBack_PlayBook_Result,Assets,
                              Ansible_Script,Project_Assets,
                              GameServer_Update_List,GameServer_Config,Log_GameServer,Server_Assets)
from OpsManage.data.DsMySQL import AnsibleRecord
from django.contrib.auth.decorators import permission_required
from OpsManage.utils.logger import logger
from dao.assets import AssetsSource
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required()
@permission_required('OpsManage.can_add_gameserver_config',login_url='/noperm/')
def gameserver_add(request):
    if request.method == "GET":
        serverList = AssetsSource().serverList()

        return render(request,'gameserver/gs_add.html',{"user":request.user,"serverList":serverList})
    elif request.method == "POST":
        try:
            server = Server_Assets.objects.get(id=request.POST.get("game_server"));
        except:
            return HttpResponse(content="主机ID不存在，可能已被删除", status=404)
        try:
            gameserver = GameServer_Config.objects.create(
                name = request.POST.get("gamename"),
                game_path = request.POST.get("game_path"),
                gate_path = request.POST.get("gate_path"),
                state = request.POST.get("state"),
                ip = server
            )
            return HttpResponse(status=201)
        except Exception, ex:
            if 1062 in ex:ex="添加失败，游戏服已存在"
            return HttpResponse(content=ex,status=500)

@login_required()
@permission_required('OpsManage.can_read_gameserver_config',login_url='/noperm/')
def gamehost_list(request):
    gshost = []
    ips = GameServer_Config.objects.values_list("ip__ip",flat=True).distinct()
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
        game =list(GameServer_Config.objects.filter(ip__ip=ip).values_list("name",flat=True))
        onlinegame = onlinegame+gonlinegame
        gshost.append(
            {
                'game': ",".join(str(game)),
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
def gameserver_details(request,id):
    gameserver_list = GameServer_Config.objects.all()
    if request.method == "GET" :

        #rungame = ANSRunner.run_model()
        gslist = gameserver_list.filter(ip__assets_id=id)
        data = []
        for gs in gslist:
            data.append({"name":gs.name,"game_path":gs.game_path,"gate_path":gs.gate_path,"state":gs.state,"gid":gs.id})
        return JsonResponse({"code": 200, "msg": "success", "data": data})
    elif request.method == "POST":
        if not request.user.has_perm('OpsManage.can_change_gameserver_config'):
            return HttpResponse(status=404)
        else:
            try:
                server = Server_Assets.objects.get(id=request.POST.get('game_server'))
            except Server_Assets.DoesNotExist:
                return HttpResponse(status=404)
            gameserver = GameServer_Config(
                name=request.POST.get("name"),
                game_path=request.POST.get("gamepath"),
                gate_path=request.POST.get("gatepath"),
                state=request.POST.get("state"),
                ip=server.ip
            )
            try:
                gameserver.save()
            except:
                return HttpResponse(status=500)
    elif request.method == "DELETE":
        if not request.user.has_perm('OpsManage.can_delete_gameserver_config'):
            return HttpResponse(status=403)
        else:
            try:
                gameserver = gameserver_list.get(id=id)
            except gameserver.DoesNotExist:
                return HttpResponse(status=404)
            gameserver.delete()
            return HttpResponse(status=200)
