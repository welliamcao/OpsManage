#!/usr/bin/env python
# _#_ coding:utf-8 _*_
import json
from time import localtime, strftime

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

@login_required()
@permission_required('OpsManage.can_add_gameserver_config',login_url='/noperm/')
def gameserver_add(request):
    if request.method == "GET":
        serverList = AssetsSource().serverList()
        for i,asset in enumerate(serverList):
            sid=Server_Assets.objects.get(assets_id=serverList[i]['id']).id
            serverList[i]['sid']=sid
        return render(request,'gameserver/gs_add.html',{"user":request.user,"serverList":serverList})
    elif request.method == "POST":
        gtype = request.GET.get("type")
        if gtype=="server":
            try:
                server = Assets.objects.get(id=request.POST.get("game_server")).server_assets
            except:
                return HttpResponse(content="主机ID不存在，可能已被删除", status=404)
            try:
                GameServer_Config.objects.create(
                    name = request.POST.get("gamename"),
                    game_path = request.POST.get("game_path"),
                    gate_path = request.POST.get("gate_path"),
                    state = request.POST.get("state"),
                    ip = server
                )
            except Exception, ex:
                if (1062 in ex) and ('Duplicate' in ex[1]):ex="添加失败，游戏服已存在"
                return HttpResponse(content=ex,status=500)
            return HttpResponse(status=201)
        if gtype=="host":
            pass


@login_required()
@permission_required('OpsManage.can_read_gameserver_config',login_url='/noperm/')
def gameserver_modify(request,gid=None):
    if request.method == "GET":
        serverList = AssetsSource().serverList()
        try:
            gameserver = GameServer_Config.objects.get(id=gid)
        except :
            return HttpResponse(status=404)
        for i,gs in enumerate(serverList):
            if gs["ip"] == gameserver.ip.ip:
                gshost = serverList.pop(i)
        return render(request, 'gameserver/gs_modf.html', {"serverList":serverList, "user":request.user,
                                                           "gameserver":gameserver, "gshost":gshost})
    elif request.method =="POST":
        if not request.user.has_perm('OpsManage.can_change_gameserver_config'):
            return HttpResponse(status=403)
        else:
            try:
                server = Server_Assets.objects.get(id=request.POST.get('game_server'))
                gameserver = GameServer_Config.objects.get(id=request.POST.get("id"))
            except Exception, ex:
                return HttpResponse(content=ex,status=404)
            gameserver.name = request.POST.get("name"),
            gameserver.game_path = request.POST.get("gamepath"),
            gameserver.gate_path = request.POST.get("gatepath"),
            gameserver.state = request.POST.get("state"),
            gameserver.ip = server.ip
            try:
                gameserver.save()
            except Exception,ex:
                return HttpResponse(content="修改失败，游戏服可能已经被删除",status=404)
            try:
                gameserver.save()
            except Exception, ex:
                return HttpResponse(content=ex,status=500)
            return HttpResponse(status=202)

@login_required()
@permission_required('OpsManage.can_read_gameserver_config',login_url='/noperm/')
def gamehost_list(request):
    if request.method == "GET":
        gshost = []
        ips = GameServer_Config.objects.values_list("ip__ip",flat=True).distinct()
        totalgame = GameServer_Config.objects.all().count()
        offlinegame = GameServer_Config.objects.filter(state=False).count()
        for ip in ips:
            sid = Server_Assets.objects.get(ip=ip).id
            aid = Server_Assets.objects.get(ip=ip).assets.id
            business = Project_Assets.objects.get(id=Assets.objects.get(id=aid).business).project_name
            hostname = Server_Assets.objects.get(ip=ip).hostname
            system = Server_Assets.objects.get(ip=ip).system
            onlinegame = GameServer_Config.objects.filter(state=True,ip__ip=ip).count()
            status = Assets.objects.get(id=aid).status
            game =list(GameServer_Config.objects.filter(ip__ip=ip).values_list("name",flat=True))
            gshost.append(
                {
                    'game': ",".join(game),
                    'aid':aid,
                    'sid':sid,
                    'business':business,
                    'hostname':hostname,
                    'ip':ip,
                    'system':system,
                    'onlinegame':onlinegame,
                    'status':status,
                }
            )
        return render(request,'gameserver/gs_config.html',{"user":request.user,"totalGame":totalgame,"onlineGame":onlinegame,
                                                           "offlineGame":offlinegame,"gshost":gshost},)

@login_required()
@permission_required('OpsManage.can_read_gameserver_config')
def gameserver_details(request,id):
    gameserver_list = GameServer_Config.objects.all()
    if request.method == "GET" :

        #rungame = ANSRunner.run_model()
        gslist = gameserver_list.filter(ip=id)
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
@permission_required('OpsManage.can_change_gameserver_config')
def gamehost_facts(request):
    def synchost(id,filter="old|OLD|Old|lost|下线"):
        datalist=[]
        try:
            server_assets = Server_Assets.objects.get(id=id)
            if server_assets.keyfile == 1:
                resource = [{"ip": server_assets.ip, "port": int(server_assets.port), "username": server_assets.username,
                             "sudo_passwd": server_assets.sudo_passwd}]
            else:
                resource = [{"ip": server_assets.ip, "port": server_assets.port, "username": server_assets.username,
                             "password": server_assets.passwd, "sudo_passwd": server_assets.sudo_passwd}]
        except Exception,ex:
            return  "获取资产信息失败,ErrorString:"+str(ex)
        ANS = ANSRunner(resource)
        ANS.run_model(host_list=[server_assets.ip], module_name='raw',
                      module_args="find /data -type f -name 'Gate*' |grep -vE '{0}'|xargs -I {{}} dirname {{}}".format(filter))
        Gatedata = ANS.handle_model_data(ANS.get_model_result(),"raw")
        ANS.run_model(host_list=[server_assets.ip], module_name='raw',
                      module_args="find /data -type f -name 'Game*' |grep -vE '{0}'|xargs -I {{}} dirname {{}}".format(filter))
        Gamedata = ANS.handle_model_data(ANS.get_model_result(),"raw")
        if Gatedata:
            for gate in Gatedata:
                Gatewaylist = gate.get("msg").split("<br>")
        if Gamedata:
            for game in Gamedata:
                Gameserverlist = game.get("msg").split("<br>")
        for gate in Gatewaylist:
            gatename = gate.split("/")
            if len(gatename)>3:
                for game in Gameserverlist:
                    gamename = game.split("/")
                    if len(gamename)>3:
                        if gatename[2] == gamename[2]:
                            datalist.append(
                                {"name": gamename[2], "gate_path": gate, "game_path": game}
                            )
        return datalist,server_assets
    if request.method == "PUT":
        gamelist,server_assets=synchost(id=request.POST.get("server_id"))
        for game in gamelist:
            try:
                GameServer_Config.objects.update_or_create(ip=server_assets,**game)
            except Exception,ex:
                return JsonResponse({'msg': ex, "code": 500})
        return JsonResponse({'msg': "同步成功", "code": 201})

    if request.method=="GET":
        try:
            gamelist,server_assets = synchost(id=request.GET.get("server_id"))
        except Exception,ex:
            if isinstance(gamelist, str): return JsonResponse({'msg': gamelist, "code": 500})
        for i,game in enumerate(gamelist):
            gamelist[i][0]=game["name"]
            gamelist[i][1] = game["gate_path"]
            gamelist[i][2] = game["game_path"]
        if isinstance(gamelist, list):return JsonResponse({'msg': json.dumps(gamelist), "code": 200})
        if isinstance(gamelist, str):return JsonResponse({'msg': gamelist, "code": 404})



@login_required()
@permission_required('OpsManage.can_add_gsupdate_list',login_url='/noperm/')
def reupdate(request):
    if request.method == "GET":
        ids=list(GameServer_Update_List.objects.values_list("listid",flat=True))
        if ids:
            ids.sort()
            listid= ids[len(ids)-1]+1
        else:listid=0
        return render(request,'gameserver/reupdate.html',{"user":request.user,"ListID":listid})



def showfile(request):
    if request.method == "POST":
        Gastat = []
        gameserver = GameServer_Config.objects.get(id=int(request.POST.get("gid")))
        gamehost = gameserver.ip
        if gamehost.keyfile == 1:
            resource = [
                {"ip": gamehost.ip, "port": int(gamehost.port), "username": gamehost.username,
                 "sudo_passwd": gamehost.sudo_passwd}]
        else:
            resource = [{"ip": gamehost.ip, "port": gamehost.port, "username": gamehost.username,
                         "password": gamehost.passwd, "sudo_passwd": gamehost.sudo_passwd}]
        if request.POST.get("ptype") == "gateway":
            path=gameserver.gate_path
            keyword="Gate"
        elif request.POST.get("ptype") == "gameserver":
            keyword = "Game"
            path=gameserver.game_path
        ANS = ANSRunner(resource)
        ANS.run_model(host_list=[gamehost.ip], module_name='raw',
                      module_args="cd {0} && find ./ -maxdepth 1 -type f |grep {1}|xargs -I {{}} stat -c '%n,%Y,%s' {{}}".format(path,keyword))
        predata = ANS.handle_model_data(ANS.get_model_result(),"raw")
        if predata:
            for x in predata:
                datalist = x.get("msg").split("<br>")
                for filedata in datalist:
                    filestat = filedata.split(",")
                    if len(filestat)==3:
                        stat = dict(zip(["name","mtime","size"],filestat))
                        stat["size"]='%.2fM'%(float(stat["size"])/1024/1024)
                        stat["name"]=stat["name"].strip("./")
                        stat["mtime"]=strftime("%Y-%m-%d %H:%M:%S",localtime(int(stat["mtime"])))
                        Gastat.append(stat)
        return JsonResponse({"code": 200, "msg": "success", "data": Gastat})

def uplist_modify(request):
    if request.method == "GET":
        data = []
        gameupdate = {}
        updateobj = GameServer_Update_List.objects.all()
        for alist in updateobj:
            data.append({"listid":alist.listid,"oderid":alist.orderid,"type":alist.type,"souce":alist.sourceip,"target":alist.targetip,
                         "soucepath":alist.souce_path,"targetpath":alist.target_path,"ocudate":alist.ocudate})