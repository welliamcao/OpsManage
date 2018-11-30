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
def gameserver_modify(request,gid=None):
    if request.method == "GET":
        serverList = AssetsSource().serverList()
        try:
            gameserver = GameServer_Config.objects.get(id=gid)
        except :
            return HttpResponse(status=404)
        for gs in serverList:
            if gs["ip"] == gameserver.ip.ip:
                gshost = gs
        return render(request, 'gameserver/gs_modf.html', {"serverList":serverList, "user":request.user, "gameserver":gameserver, "gshost":gshost})
    elif request.method =="POST":
        if not request.user.has_perm('OpsManage.can_change_gameserver_config'):
            return HttpResponse(status=403)
        else:
            try:
                server = Server_Assets.objects.get(id=request.POST.get('game_server'))
            except Exception, ex:
                return HttpResponse(content=ex,status=404)
            gameserver = GameServer_Config(
                name=request.POST.get("name"),
                game_path=request.POST.get("gamepath"),
                gate_path=request.POST.get("gatepath"),
                state=request.POST.get("state"),
                ip=server.ip
            )
            try:
                gameserver.save
            except Exception, ex:
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
    elif request.method == "DELETE":
        if not request.user.has_perm('OpsManage.can_delete_gameserver_config'):
            return HttpResponse(content="没有权限，请联系管理员",status=403)
        else:
            try:
                gameserver = gameserver_list.get(id=id)
            except gameserver.DoesNotExist:
                return HttpResponse(content="ID不存在，游戏服可能已被删除，",status=404)
            gameserver.delete()
            return HttpResponse(status=200)

@login_required()
def gamehost_facts(request):
    if request.method == "POST" and request.user.has_perm('OpsManage.can_change_gameserver_config'):
        try:
            server_assets = Server_Assets.objects.get(id=request.POST.get("server_id"))
            if server_assets.keyfile == 1:
                resource = [{"ip": server_assets.ip, "port": int(server_assets.port), "username": server_assets.username,
                             "sudo_passwd": server_assets.sudo_passwd}]
            else:
                resource = [{"ip": server_assets.ip, "port": server_assets.port, "username": server_assets.username,
                             "password": server_assets.passwd, "sudo_passwd": server_assets.sudo_passwd}]
        except Exception,ex:
            return HttpResponse(status=404)
        filter = "old|OLD|Old|lost|下线"
        ANS = ANSRunner(resource)
        ANS.run_model(host_list=[server_assets.ip], module_name='raw',
                      module_args="find /data -type f Gate* |grep -v '{0}'|xargs -I {{}} dirname {{}}".format(filter))
        Gatedata = ANS.handle_model_data(ANS.get_model_result(),"raw")
        ANS.run_model(host_list=[server_assets.ip], module_name='raw',
                      module_args="find /data -type f Game* |grep -v '{0}'|xargs -I {{}} dirname {{}}".format(filter))
        Gamedata = ANS.handle_model_data(ANS.get_model_result(),"raw")
        if Gatedata:
            for gate in Gatedata:
                Gatelist = gate.get("msg").split("<br>")
        if Gamedata:
            for game in Gamedata:
                Gamelist = game.get("msg").split("<br>")
        for gate in Gatelist:
            for game in Gamelist:
                gamename = game.split("/")[1]
                if gate.split("/")[1] == gamename:
                    try:
                        GameServer_Config.objects.create(
                            name=gamename,
                            gate_path=gate,
                            game_path=game,
                            ip=server_assets
                        )
                    except Exception,ex:
                        return HttpResponse(status=500)
    else:return HttpResponse(status=403)