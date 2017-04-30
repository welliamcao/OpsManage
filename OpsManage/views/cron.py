#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import os
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from OpsManage.models import Cron_Config,Server_Assets
from OpsManage.utils.ssh_tools import SSHManage
from OpsManage.utils import base
from OpsManage.tasks import recordCron
from OpsManage.models import Log_Cron_Config
from django.contrib.auth.decorators import permission_required

@login_required()
@permission_required('Opsmanage.can_add_cron_config',login_url='/noperm/') 
def cron_add(request):
    serverList = Server_Assets.objects.all()
    if request.method == "GET": 
        return render_to_response('cron/cron_add.html',{"user":request.user,"serverList":serverList},
                                  context_instance=RequestContext(request))
    elif request.method == "POST":
        cron_status = request.POST.get('cron_status',0)
        try:
            server = Server_Assets.objects.get(id=request.POST.get('cron_server'))
        except:
            return render_to_response('cron/cron_add.html',{"user":request.user,
                                                               "serverList":serverList,
                                                               "errorInfo":"主机不存在，请检查是否被删除。"},
                                  context_instance=RequestContext(request)) 
        try:
            cron = Cron_Config.objects.create(
                                       cron_minute=request.POST.get('cron_minute'),
                                       cron_hour=request.POST.get('cron_hour'),
                                       cron_day=request.POST.get('cron_day'),
                                       cron_week=request.POST.get('cron_week'),
                                       cron_month=request.POST.get('cron_month'),
                                       cron_user=request.POST.get('cron_user'),
                                       cron_name=request.POST.get('cron_name'),
                                       cron_desc=request.POST.get('cron_desc'),
                                       cron_server=server,
                                       cron_command=request.POST.get('cron_command'),
                                       cron_script=request.FILES.get('cron_script', None),
                                       cron_script_path=request.POST.get('cron_script_path',None),
                                       cron_status=cron_status,
                                       )
            recordCron.delay(cron_user=str(request.user),cron_id=cron.id,cron_name=cron.cron_name,cron_content="添加计划任务",cron_server=server.ip)
        except Exception,e:
            return render_to_response('cron/cron_add.html',{"user":request.user,
                                                               "serverList":serverList,
                                                               "errorInfo":"提交失败，错误信息："+str(e)},
                                  context_instance=RequestContext(request))    
        
        if  int(cron_status) == 1:       
            cronList = Cron_Config.objects.filter(cron_server=request.POST.get('cron_server'),
                                                  cron_user=request.POST.get('cron_user'),
                                                  cron_status=1)
            try:
                tmpFile = "/tmp/" + request.POST.get('cron_user') + '.' + base.radString(length=4)
                with open(tmpFile,"w") as f:
                    for cron in cronList:
                        f.write('#' + cron.cron_name +'\n')
                        cronStr = '{minute} {hour} {day} {week} {month} {command} \n'.format(
                                                                                              minute=cron.cron_minute,hour=cron.cron_hour,
                                                                                              day=cron.cron_day,week=cron.cron_week,
                                                                                              month=cron.cron_month,command=cron.cron_command
                                                                                              )
                        f.write(cronStr)
                if os.path.exists(tmpFile):
                    sshRbt = SSHManage(hostname=server.ip,password=server.passwd,username=server.username,port=int(server.port))
                    result = sshRbt.upload(localPath=tmpFile, remotePath='/var/spool/cron/'+request.POST.get('cron_user'))
                    sshRbt.close()
                    os.remove(tmpFile)
                    if result.get('status') != 'success':
                        return render_to_response('cron/cron_add.html',{"user":request.user,
                                                                                               "serverList":serverList,
                                                                                               "errorInfo":"任务条件数据库成功，更新远程主机Crontab失败。"},
                                                                  context_instance=RequestContext(request))                             
                         
            except Exception,e:
                try:
                    Cron_Config.objects.get(cron_name=request.POST.get('cron_name'),cron_server=server,
                                        cron_user=request.POST.get('cron_user')).delete()
                except:
                    pass
                return render_to_response('cron/cron_add.html',{"user":request.user,
                                                                   "serverList":serverList,
                                                                   "errorInfo":"错误信息:"+str(e)},
                                      context_instance=RequestContext(request))                     
        return HttpResponseRedirect('/cron_add')

@login_required()
@permission_required('Opsmanage.can_read_config',login_url='/noperm/') 
def cron_list(request):
    cronList = Cron_Config.objects.select_related().all()
    return render_to_response('cron/cron_list.html',{"user":request.user,
                                                    "cronList":cronList},
                              context_instance=RequestContext(request)) 
    
@login_required()
@permission_required('Opsmanage.can_change_cron_config',login_url='/noperm/') 
def cron_mod(request,cid): 
    try:
        cron = Cron_Config.objects.select_related().get(id=cid)
    except:
        return render_to_response('cron/cron_modf.html',{"user":request.user,
                                                         "errorInfo":"任务不存在，可能已经被删除."},
                                context_instance=RequestContext(request))    
    if request.method == "GET": 
        return render_to_response('cron/cron_modf.html',
                                  {"user":request.user,"cron":cron},
                                context_instance=RequestContext(request)) 
    elif request.method == "POST":        
        try:
            Cron_Config.objects.filter(id=cid).update(
                       cron_minute=request.POST.get('cron_minute'),
                       cron_hour=request.POST.get('cron_hour'),
                       cron_day=request.POST.get('cron_day'),
                       cron_week=request.POST.get('cron_week'),
                       cron_month=request.POST.get('cron_month'),
                       cron_user=request.POST.get('cron_user'),
                       cron_name=request.POST.get('cron_name'),
                       cron_desc=request.POST.get('cron_desc'),
                       cron_command=request.POST.get('cron_command'),
                       cron_script=request.FILES.get('cron_script', None),
                       cron_script_path=request.POST.get('cron_script_path',None),
                       cron_status=request.POST.get('cron_status'),
                                       )
            recordCron.delay(cron_user=str(request.user),cron_id=cid,cron_name=cron.cron_name,cron_content="修改计划任务",cron_server=cron.cron_server.ip)
        except Exception,e:
            return render_to_response('cron/cron_modf.html',
                                      {"user":request.user,"errorInfo":"更新失败，错误信息："+str(e)},
                                  context_instance=RequestContext(request))     
        #获取改主机所有激活的计划任务
        cronList = Cron_Config.objects.filter(cron_server=cron.cron_server, cron_status=1,
                                              cron_user=request.POST.get('cron_user'),
                                             )         
        try:
            tmpFile = "/tmp/"  + request.POST.get('cron_user') + '.' + base.radString(length=4)
            with open(tmpFile,"w") as f:
                for cron in cronList:
                    f.write('#' + cron.cron_name +'\n')
                    cronStr = '{minute} {hour} {day} {week} {month} {command} \n'.format(
                                                                                          minute=cron.cron_minute,hour=cron.cron_hour,
                                                                                          day=cron.cron_day,week=cron.cron_week,
                                                                                          month=cron.cron_month,command=cron.cron_command
                                                                                          )
                    f.write(cronStr)
            if os.path.exists(tmpFile):
                sshRbt = SSHManage(hostname=cron.cron_server.ip,password=cron.cron_server.passwd,
                                   username=cron.cron_server.username,port=int(cron.cron_server.port))
                result = sshRbt.upload(localPath=tmpFile, remotePath='/var/spool/cron/'+request.POST.get('cron_user'))
                sshRbt.close()                
                os.remove(tmpFile)
                if result.get('status') != 'success':
                    return render_to_response('cron/cron_add.html',{"user":request.user,"errorInfo":"任务条件数据库成功，更新远程主机Crontab失败。"},
                                                              context_instance=RequestContext(request))                             
        except Exception,e:
            return render_to_response('cron/cron_add.html',{"user":request.user,"errorInfo":"错误信息:"+str(e)},)           
        return HttpResponseRedirect('/cron_mod/{id}/'.format(id=cid))
    
    elif request.method == "DELETE":
        try:
            recordCron.delay(cron_user=str(request.user),cron_id=cid,cron_name=cron.cron_name,cron_content="删除计划任务",cron_server=cron.cron_server.ip)
            cron.delete()
        except Exception,e:
            return JsonResponse({'msg':'删除失败：'+str(e),"code":500,'data':[]})          
        #获取改主机所有激活的计划任务
        cronList = Cron_Config.objects.filter(cron_server=cron.cron_server, cron_status=1,
                                              cron_user=cron.cron_user,
                                             )  
        try:
            tmpFile = "/tmp/"  + cron.cron_user + '.' + base.radString(length=4)
            with open(tmpFile,"w") as f:
                for cron in cronList:
                    f.write('#' + cron.cron_name +'\n')
                    cronStr = '{minute} {hour} {day} {week} {month} {command} \n'.format(
                                                                                          minute=cron.cron_minute,hour=cron.cron_hour,
                                                                                          day=cron.cron_day,week=cron.cron_week,
                                                                                          month=cron.cron_month,command=cron.cron_command
                                                                                          )
                    f.write(cronStr)
            if os.path.exists(tmpFile):
                sshRbt = SSHManage(hostname=cron.cron_server.ip,password=cron.cron_server.passwd,
                                   username=cron.cron_server.username,port=int(cron.cron_server.port))
                result = sshRbt.upload(localPath=tmpFile, remotePath='/var/spool/cron/'+cron.cron_user)
                sshRbt.close()                  
                os.remove(tmpFile)
                if result.get('status') != 'success':                   
                    return JsonResponse({'msg':'删除成功',"code":200,'data':[]})                           
        except Exception,e:
            return JsonResponse({'msg':'删除失败：'+str(e),"code":500,'data':[]})        
        return JsonResponse({'msg':'删除成功',"code":200,'data':[]})       
        
@login_required()
@permission_required('Opsmanage.can_add_cron_config',login_url='/noperm/') 
def cron_config(request):
    serverList = Server_Assets.objects.all()
    if request.method == "GET": 
        return render_to_response('cron/cron_config.html',{"user":request.user,"serverList":serverList},
                                  context_instance=RequestContext(request))    
    elif request.method == "POST": 
        try:
            server = Server_Assets.objects.get(id=request.POST.get('cron_server'))
        except:
            return JsonResponse({'msg':"主机资源不存在","code":500,'data':[]})  
        try:
            repeatCron = ""
            for ds in request.POST.get('cron_data').split('\n'):
                cron = ds.split('|')
                cron_name = cron[0]
                cron_time = cron[1]
                cron_data = cron_time.split(' ',5)
                try:
                    cron = Cron_Config.objects.create(
                                               cron_minute=cron_data[0],
                                               cron_hour=cron_data[1],
                                               cron_day=cron_data[2],
                                               cron_week=cron_data[3],
                                               cron_month=cron_data[4],
                                               cron_user=request.POST.get('cron_user'),
                                               cron_name=cron_name,
                                               cron_desc=cron_name,
                                               cron_server=server,
                                               cron_command=cron_data[5],
                                               cron_script=request.FILES.get('file', None),
                                               cron_status=request.POST.get('cron_user',0),
                                               )
                    recordCron.delay(cron_user=str(request.user),cron_id=cron.id,cron_name=cron.cron_name,cron_content="导入计划任务",cron_server=server.ip)
                except:
                    repeatCron = cron_name + "<br>" + repeatCron
        except:
            return JsonResponse({'msg':'数据格式不对',"code":500,'data':[]}) 
        if repeatCron:return JsonResponse({'msg':'添加成功，以下是重复内容：<br>' + repeatCron,"code":200,'data':[]}) 
        else:return JsonResponse({'msg':'添加成功',"code":200,'data':[]}) 
        
@login_required(login_url='/login')  
def cron_log(request):
    if request.method == "GET":
        cronList = Log_Cron_Config.objects.all().order_by('-id')[0:120]
        return render_to_response('cron/cron_log.html',{"user":request.user,"cronList":cronList},
                                  context_instance=RequestContext(request))