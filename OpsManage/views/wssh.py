#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.shortcuts import render
from OpsManage.models import Assets,Server_Assets,User_Server
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def wssh(request,sid):
    
    try:
        server = Server_Assets.objects.get(id=sid)
        if request.user.is_superuser:
            serverList = Server_Assets.objects.all()
            return render(request,'webssh/webssh.html',{"user":request.user,"server":server,
                                                     "serverList":serverList})  
        else:
            user_server = User_Server.objects.get(user_id=int(request.user.id),server_id=id)
            userServer = User_Server.objects.filter(user_id=int(request.user.id))
            serverList = []
            for s in userServer:
                ser = Server_Assets.objects.get(id=s.server_id)
                serverList.append(ser)
            if user_server:
                return render(request,'webssh/webssh.html',{"user":request.user,"server":server,
                                                         "serverList":serverList}) 
    except Exception,e:
        print e
        return render(request,'webssh/webssh.html',{"user":request.user,"errorInfo":"你没有权限访问这台服务器！"})    
    