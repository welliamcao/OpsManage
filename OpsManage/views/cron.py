#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import os
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OpsManage.models import Cron_Config,Server_Assets
from OpsManage.utils.ssh_tools import SSHManage
from OpsManage.utils import base
from OpsManage.tasks.cron import recordCron
from OpsManage.models import Log_Cron_Config
from django.contrib.auth.decorators import permission_required
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dao.assets import AssetsSource

@login_required()
@permission_required('OpsManage.can_add_cron_config',login_url='/noperm/') 
def cron_add(request):
    serverList = AssetsSource().serverList()
    if request.method == "GET": 
        return render(request,'cron/cron_add.html',{"user":request.user,"serverList":serverList},
                                  )
    elif request.method == "POST":
        cron_status = request.POST.get('cron_status',0)
        try:
            server = Server_Assets.objects.get(id=request.POST.get('cron_server'))
        except:
            return render(request,'cron/cron_add.html',{"user":request.user,
                                                               "serverList":serverList,
                                                               "errorInfo":"主机不存在，请检查是否被删除。"},
                                  ) 
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
            return render(request,'cron/cron_add.html',{"user":request.user,
                                                               "serverList":serverList,
                                                               "errorInfo":"提交失败，错误信息："+str(e)},
                                  )    
        
        if  int(cron_status) == 1: 
            try:
                sList = [server.ip]
                if server.keyfile == 1:resource = [{"ip": server.ip, "port": int(server.port),"username": server.username}] 
                else:resource = [{"ip": server.ip, "port": int(server.port),"username": server.username,"password": server.passwd}]              
                ANS = ANSRunner(resource)
                if cron.cron_script:
                    src = os.getcwd() + '/' + str(cron.cron_script)
                    file_args = """src={src} dest={dest} owner={user} group={user} mode=755""".format(src=src,dest=cron.cron_script_path,user=cron.cron_user)
                    ANS.run_model(host_list=sList,module_name="copy",module_args=file_args)        
                    result = ANS.handle_model_data(ANS.get_model_result(), 'copy',file_args) 
                    if result[0].get('status') == 'failed':
                        cron.delete()
                        return render(request,'cron/cron_add.html',{"user":request.user,
                                                                   "serverList":serverList,
                                                                   "errorInfo":"错误信息:"+result[0].get('msg')}, 
                                      ) 
#                 
                cron_args = """name={name} minute='{minute}' hour='{hour}' day='{day}'
                               weekday='{weekday}' month='{month}' user='{user}' job='{job}'""".format(name=cron.cron_name,minute=cron.cron_minute,
                                                                                                    hour=cron.cron_hour,day=cron.cron_day,
                                                                                                     weekday=cron.cron_week,month=cron.cron_month,
                                                                                                     user=cron.cron_user,job=cron.cron_command
                                                                                                     )  
                ANS.run_model(host_list=sList,module_name="cron",module_args=cron_args)   
                result = ANS.handle_model_data(ANS.get_model_result(), 'cron',cron_args) 
            except Exception,e:
                return render(request,'cron/cron_add.html',{"user":request.user,
                                                                   "serverList":serverList,
                                                                   "errorInfo":"错误信息:"+str(e)}, 
                                      )     
            if result[0].get('status') == 'failed':
                cron.delete()
                return render(request,'cron/cron_add.html',{"user":request.user,
                                                                   "serverList":serverList,
                                                                   "errorInfo":"错误信息:"+result[0].get('msg').replace('\n','')}) 
        return HttpResponseRedirect('/cron_add')

@login_required()
@permission_required('OpsManage.can_read_cron_config',login_url='/noperm/') 
def cron_list(request,page):
    allCronList = Cron_Config.objects.select_related().all()[0:1000]
    paginator = Paginator(allCronList, 25)          
    try:
        cronList = paginator.page(page)
    except PageNotAnInteger:
        cronList = paginator.page(1)
    except EmptyPage:
        cronList = paginator.page(paginator.num_pages)     
    return render(request,'cron/cron_list.html',{"user":request.user,
                                                    "cronList":cronList},
                              ) 
    
@login_required()
@permission_required('OpsManage.can_change_cron_config',login_url='/noperm/') 
def cron_mod(request,cid): 
    try:
        cron = Cron_Config.objects.select_related().get(id=cid)
    except:
        return render(request,'cron/cron_modf.html',{"user":request.user,
                                                         "errorInfo":"任务不存在，可能已经被删除."},
                                )    
    if request.method == "GET": 
        return render(request,'cron/cron_modf.html',
                                  {"user":request.user,"cron":cron},
                                ) 
    elif request.method == "POST":    
        try:
            Cron_Config.objects.filter(id=cid).update(
                       cron_minute=request.POST.get('cron_minute'),
                       cron_hour=request.POST.get('cron_hour'),
                       cron_day=request.POST.get('cron_day'),
                       cron_week=request.POST.get('cron_week'),
                       cron_month=request.POST.get('cron_month'),
                       cron_user=request.POST.get('cron_user'),
                       cron_desc=request.POST.get('cron_desc'),
                       cron_command=request.POST.get('cron_command'),
                       cron_script_path=request.POST.get('cron_script_path',None),
                       cron_status=request.POST.get('cron_status'),
                                       )
            recordCron.delay(cron_user=str(request.user),cron_id=cid,cron_name=cron.cron_name,cron_content="修改计划任务",cron_server=cron.cron_server.ip)
        except Exception,e:
            return render(request,'cron/cron_modf.html',
                                      {"user":request.user,"errorInfo":"更新失败，错误信息："+str(e)},
                                  )  
        try:
            sList = [cron.cron_server.ip]
            if cron.cron_server.keyfile == 1:resource = [{"ip": cron.cron_server.ip, "port": int(cron.cron_server.port),"username": cron.cron_server.username}] 
            else:resource = [{"ip": cron.cron_server.ip, "port": int(cron.cron_server.port),
                         "username": cron.cron_server.username,"password": cron.cron_server.passwd}]    
            cron = Cron_Config.objects.get(id=cid)
            if request.FILES.get('cron_script'):
                cron.cron_script=request.FILES.get('cron_script')
                cron.save()
            ANS = ANSRunner(resource)
            if  cron.cron_status == 0:ANS.run_model(host_list=sList,module_name="cron",module_args="""name={name} state=absent""".format(name=cron.cron_name))       
            else:
                if cron.cron_script:
                    src = os.getcwd() + '/' + str(cron.cron_script)
                    file_args = """src={src} dest={dest} owner={user} group={user} mode=755""".format(src=src,dest=cron.cron_script_path,user=cron.cron_user)
                    ANS.run_model(host_list=sList,module_name="copy",module_args=file_args)  
                cron_args = """name={name} minute='{minute}' hour='{hour}' day='{day}'
                               weekday='{weekday}' month='{month}' user='{user}' job='{job}'""".format(name=cron.cron_name,minute=cron.cron_minute,
                                                                                                    hour=cron.cron_hour,day=cron.cron_day,
                                                                                                     weekday=cron.cron_week,month=cron.cron_month,
                                                                                                     user=cron.cron_user,job=cron.cron_command
                                                                                                     )                              
                ANS.run_model(host_list=sList,module_name="cron",module_args=cron_args)    
        except Exception,e:
            return render(request,'cron/cron_modf.html',{"user":request.user,"errorInfo":"错误信息:"+str(e)}, 
                                  )                     
        return HttpResponseRedirect('/cron_mod/{id}/'.format(id=cid))
    
    elif request.method == "DELETE" and request.user.has_perm('OpsManage.can_delete_cron_config'):     
        try:
            recordCron.delay(cron_user=str(request.user),cron_id=cid,cron_name=cron.cron_name,cron_content="删除计划任务",cron_server=cron.cron_server.ip)
            sList = [cron.cron_server.ip]
            if cron.cron_server.keyfile == 1:resource = [{"ip": cron.cron_server.ip, "port": int(cron.cron_server.port),"username": cron.cron_server.username}] 
            else:resource = [{"ip": cron.cron_server.ip, "port": int(cron.cron_server.port),
                         "username": cron.cron_server.username,"password": cron.cron_server.passwd}]    
            ANS = ANSRunner(resource)  
            ANS.run_model(host_list=sList,module_name="cron",module_args="""name={name} state=absent""".format(name=cron.cron_name))    
            cron.delete()      
        except Exception,e:
            return JsonResponse({'msg':'删除失败：'+str(e),"code":500,'data':[]})                
        return JsonResponse({'msg':'删除成功',"code":200,'data':[]})       
        
@login_required()
@permission_required('OpsManage.can_add_cron_config',login_url='/noperm/') 
def cron_config(request):
    serverList = Server_Assets.objects.all()
    if request.method == "GET": 
        return render(request,'cron/cron_config.html',{"user":request.user,"serverList":serverList},
                                  )    
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
                                               cron_status=request.POST.get('cron_status',0),
                                               )
                    recordCron.delay(cron_user=str(request.user),cron_id=cron.id,cron_name=cron.cron_name,cron_content="导入计划任务",cron_server=server.ip)
                    if  int(cron.cron_status) == 1: 
                        sList = [server.ip]
                        if server.keyfile == 1:resource = [{"ip": server.ip, "port": int(server.port),"username": server.username}] 
                        else:resource = [{"ip": server.ip, "port": int(server.port),"username": server.username,"password": server.passwd}]                
                        ANS = ANSRunner(resource)
                        ANS.run_model(host_list=sList,module_name="cron",module_args="""name={name} minute='{minute}' hour='{hour}' day='{day}'
                                                                                     weekday='{weekday}' month='{month}' user='{user}' job='{job}'""".format(name=cron.cron_name,minute=cron.cron_minute,
                                                                                                                                                         hour=cron.cron_hour,day=cron.cron_day,
                                                                                                                                                         weekday=cron.cron_week,month=cron.cron_month,
                                                                                                                                                         user=cron.cron_user,job=cron.cron_command
                                                                                                                                                         )
                                                                                     )                     
                except Exception,e:
                    repeatCron = cron_name + "<br>" + repeatCron 
        except:
            return JsonResponse({'msg':'数据格式不对',"code":500,'data':[]}) 
        if repeatCron:return JsonResponse({'msg':'添加失败，以下是重复内容：<br>' + repeatCron,"code":200,'data':[]}) 
        else:return JsonResponse({'msg':'添加成功',"code":200,'data':[]}) 
        
@login_required(login_url='/login')  
def cron_log(request,page):
    if request.method == "GET":
        allCronList = Log_Cron_Config.objects.all().order_by('-id')[0:1000]
        paginator = Paginator(allCronList, 25)          
        try:
            cronList = paginator.page(page)
        except PageNotAnInteger:
            cronList = paginator.page(1)
        except EmptyPage:
            cronList = paginator.page(paginator.num_pages)          
        return render(request,'cron/cron_log.html',{"user":request.user,"cronList":cronList},)