#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import time, hmac, hashlib, json
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from OpsManage.models import Server_Assets,User_Server
from django.conf import settings
  

@login_required(login_url='/login')
def webssh(request,id):
    try:
        server = Server_Assets.objects.get(id=id)
        if request.user.is_superuser:
            serverList = Server_Assets.objects.all()
            return render_to_response('webssh/webssh.html',{"user":request.user,"server":server,
                                                     "serverList":serverList},
                                  context_instance=RequestContext(request))  
        else:
            user_server = User_Server.objects.get(user_id=int(request.user.id),server_id=id)
            userServer = User_Server.objects.filter(user_id=int(request.user.id))
            serverList = []
            for s in userServer:
                ser = Server_Assets.objects.get(id=s.server_id)
                serverList.append(ser)
            if user_server:
                return render_to_response('webssh/webssh.html',{"user":request.user,"server":server,
                                                         "serverList":serverList},
                                      context_instance=RequestContext(request))                 
    except Exception,e:
        print e
        return render_to_response('webssh/webssh.html',{"user":request.user,"errorInfo":"你没有权限访问这台服务器！"},
                                  context_instance=RequestContext(request))        

@login_required(login_url='/login')
def websshFrame(request,id):
    try:
        server = Server_Assets.objects.get(id=id)
        if request.user.is_superuser:
            return render_to_response('webssh/websshFrame.html',{"user":request.user,"server":server},
                                  context_instance=RequestContext(request))  
        else:
            user_server = User_Server.objects.get(user_id=int(request.user.id),server_id=id)
            if user_server:
                return render_to_response('webssh/websshFrame.html',{"user":request.user,"server":server},
                                      context_instance=RequestContext(request))                 
    except Exception,e:
        return render_to_response('webssh/websshFrame.html',{"user":request.user,"errorInfo":"你没有权限访问这台服务器！"},
                                  context_instance=RequestContext(request)) 
  

@login_required(login_url='/login')
def generate_gate_one_auth_obj(request):  
    user = request.user.username      
    authobj = {  
        'api_key': settings.GATEONE_KEY,  
        'upn': user,  
        'timestamp': str(int(time.time() * 1000)),  
        'signature_method': 'HMAC-SHA1',  
        'api_version': '1.0'  
    }  
    my_hash = hmac.new(settings.GATEONE_SECRET, digestmod=hashlib.sha1)   
    my_hash.update(authobj['api_key'] + authobj['upn'] + authobj['timestamp'])   
    authobj['signature'] = my_hash.hexdigest()  
    auth_info_and_server = {"url": settings.GATEONE_SERVER, "auth": authobj}  
    valid_json_auth_info = json.dumps(auth_info_and_server) 
    return HttpResponse(valid_json_auth_info)  