#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import uuid,json
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OpsManage.models import (Project_Assets,Server_Assets,Project_Config,
                            Project_Number,Project_Order,Log_Project_Config,
                            Service_Assets,Assets)
from OpsManage.utils.git import GitTools
from OpsManage.utils.svn import SvnTools
from OpsManage.utils import base
from OpsManage.data.DsRedisOps import DsRedis
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.contrib.auth.models import User,Group
from OpsManage.views.assets import getBaseAssets
from django.db.models import Count
from django.db.models import Q 
from OpsManage.tasks.deploy import recordProject,sendDeployNotice
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required()
@permission_required('OpsManage.can_add_project_config',login_url='/noperm/')
def deploy_add(request):
    if request.method == "GET":
        serverList = Server_Assets.objects.all()
        groupList = Group.objects.all()
        return render(request,'deploy/deploy_add.html',{"user":request.user,"groupList":groupList,
                                                        "serverList":serverList,'baseAssets':getBaseAssets()})
    elif  request.method == "POST":
        serverList = Server_Assets.objects.all()
        ipList = request.POST.getlist('server') 
        try:
            proAssets = Project_Assets.objects.get(id=request.POST.get('project_id'))
        except Exception, ex:
            return render(request,'deploy/deploy_add.html',{"user":request.user,"errorInfo":"部署服务器信息添加错误：%s" % str(ex)},)             
        try:    
            project = Project_Config.objects.create(
                                                    project = proAssets,
                                                    project_service = request.POST.get('project_service'),
                                                    project_env = request.POST.get('project_env'), 
                                                    project_repertory = request.POST.get('project_repertory'), 
                                                    project_address = request.POST.get('project_address'),
                                                    project_repo_dir = request.POST.get('project_repo_dir'),
                                                    project_remote_command = request.POST.get('project_remote_command'),
                                                    project_local_command = request.POST.get('project_local_command'),
                                                    project_dir = request.POST.get('project_dir'),
                                                    project_uuid = uuid.uuid4(),
                                                    project_exclude = request.POST.get('project_exclude','.git').rstrip(),
                                                    project_user = request.POST.get('project_user','root'),
                                                    project_model = request.POST.get('project_model'),
                                                    project_status = 0,
                                                    project_repo_user = request.POST.get('project_repo_user'),
                                                    project_repo_passwd = request.POST.get('project_repo_passwd'),
                                                    project_audit_group = request.POST.get('project_audit_group',None),
                                                    )
            recordProject.delay(project_user=str(request.user),project_id=project.id,project_name=proAssets.project_name,project_content="添加项目")
        except Exception,e:
            return render(request,'deploy/deploy_add.html',{"user":request.user,
                                                            "serverList":serverList,"errorInfo":"部署服务器信息添加错误：%s" % str(e)},)             
        if ipList:
            for sid in ipList:
                try:
                    server = Server_Assets.objects.get(id=sid)
                    Project_Number.objects.create(dir=request.POST.get('dir'),
                                                  server=server.ip,
                                                  project=project)
                except Exception,e:
                    project.delete()
                    return render(request,'deploy/deploy_add.html',{"user":request.user,
                                                                        "serverList":serverList,
                                                                        "errorInfo":"目标服务器信息添加错误：%s" % str(e)},
                                              )                     
          
        return HttpResponseRedirect('/deploy_add') 
    
@login_required()
@permission_required('OpsManage.can_change_project_config',login_url='/noperm/')
def deploy_modf(request,pid): 
    try:
        project = Project_Config.objects.select_related().get(id=pid)
        tagret_server = Project_Number.objects.filter(project=project)
        serverList = [ s.server_assets for s in Assets.objects.filter(project=project.project.id) ]
    except:
        return render(request,'deploy/deploy_modf.html',{"user":request.user,
                                                         "errorInfo":"项目不存在，可能已经被删除."},
                                )     
    if request.method == "GET": 
        serviceList = Service_Assets.objects.filter(project=project.project)
        groupList = Group.objects.all()
        server = [ s.server for s in tagret_server]
        for ds in serverList:
            if ds.ip in server:ds.count = 1
            else:ds.count = 0        
        return render(request,'deploy/deploy_modf.html',
                                  {"user":request.user,"project":project,"server":tagret_server,
                                   "serverList":serverList,"groupList":groupList,"serviceList":serviceList},
                                )         
    elif  request.method == "POST":
        ipList = request.POST.getlist('server',None)
        try:      
            Project_Config.objects.filter(id=pid).update(
                                                    project_env = request.POST.get('project_env'),  
                                                    project_service = request.POST.get('project_service'),
                                                    project_repertory = request.POST.get('project_repertory'), 
                                                    project_address = request.POST.get('project_address'),
                                                    project_repo_dir = request.POST.get('project_repo_dir'),
                                                    project_remote_command = request.POST.get('project_remote_command'),
                                                    project_local_command = request.POST.get('project_local_command'),
                                                    project_dir = request.POST.get('project_dir'),
                                                    project_exclude = request.POST.get('project_exclude','.git').rstrip(),
                                                    project_user = request.POST.get('project_user'),
                                                    project_audit_group = request.POST.get('project_audit_group'),
                                                    project_repo_user = request.POST.get('project_repo_user'),
                                                    project_repo_passwd = request.POST.get('project_repo_passwd'),                                                    
                                                    )
            recordProject.delay(project_user=str(request.user),project_id=pid,project_name=project.project.project_name,project_content="修改项目")
        except Exception,e:
            return render(request,'deploy/deploy_modf.html',
                                      {"user":request.user,"errorInfo":"更新失败："+str(e)},
                                  ) 
        if ipList:
            tagret_server_list = [ s.server for s in tagret_server ]
            postServerList = []
            for sid in ipList:
                try:
                    server = Server_Assets.objects.get(id=sid) 
                    postServerList.append(server.ip) 
                    if server.ip not in tagret_server_list:     
                        Project_Number.objects.create(dir=request.POST.get('dir'),
                                                      server=server.ip,
                                                      project=project)    
                    elif server.ip in tagret_server_list and request.POST.get('dir'):
                        try:
                            Project_Number.objects.filter(project=project,server=server.ip).update(dir=request.POST.get('dir'))  
                        except Exception,e:
                            print e
                            pass                                          
                except Exception,e:
                    return render(request,'deploy/deploy_modf.html',{"user":request.user,
                                                                        "serverList":serverList,
                                                                        "errorInfo":"目标服务器信息添加错误：%s" % str(e)},
                                              ) 
            #清除目标主机 - 
            delList = list(set(tagret_server_list).difference(set(postServerList)))
            for ip in delList:
                Project_Number.objects.filter(project=project,server=ip).delete()                      
        return HttpResponseRedirect('/deploy_mod/{id}/'.format(id=pid))          
        
@login_required()
@permission_required('OpsManage.can_read_project_config',login_url='/noperm/')
def deploy_list(request):
    deployList = Project_Config.objects.all()
    for ds in deployList:
        ds.number = Project_Number.objects.filter(project=ds)
    uatProject = Project_Config.objects.filter(project_env="uat").count()
    qaProject = Project_Config.objects.filter(project_env="qa").count()
    sitProject = Project_Config.objects.filter(project_env="sit").count()
    return render(request,'deploy/deploy_list.html',{"user":request.user,"totalProject":deployList.count(),
                                                         "deployList":deployList,"uatProject":uatProject,
                                                         "qaProject":qaProject,"sitProject":sitProject},
                              )  
    
@login_required()
@permission_required('OpsManage.can_change_project_config',login_url='/noperm/')
def deploy_init(request,pid):      
    if request.method == "POST": 
        project = Project_Config.objects.select_related().get(id=pid)
        if project.project_repertory == 'git':version = GitTools()
        elif project.project_repertory == 'svn':version = SvnTools()
        version.mkdir(dir=project.project_repo_dir)
        version.mkdir(dir=project.project_dir)
        result = version.clone(url=project.project_address, dir=project.project_repo_dir, user=project.project_repo_user, passwd=project.project_repo_passwd)
        if result[0] > 0:return  JsonResponse({'msg':result[1],"code":500,'data':[]})
        else:
            Project_Config.objects.filter(id=pid).update(project_status = 1)  
            recordProject.delay(project_user=str(request.user),project_id=project.id,project_name=project.project.project_name,project_content="初始化项目")              
            return JsonResponse({'msg':"初始化成功","code":200,'data':[]})
        
@login_required()
def deploy_version(request,pid): 
    try:
        project = Project_Config.objects.select_related().get(id=pid)
        if project.project_repertory == 'git':version = GitTools()
    except:
        return render(request,'deploy/deploy_version.html',{"user":request.user,
                                                         "errorInfo":"项目不存在，可能已经被删除."}, 
                                  )      
    if request.method == "POST":
        try:
            project = Project_Config.objects.get(id=pid)
            if project.project_repertory == 'git':version = GitTools()
            elif project.project_repertory == 'svn':version = SvnTools()
        except:
            return JsonResponse({'msg':"项目资源不存在","code":403,'data':[]}) 
        if project.project_status == 0:return JsonResponse({'msg':"请先初始化项目","code":403,'data':[]}) 
        if request.POST.get('op') in ['create','delete','query','histroy']:
            if  request.POST.get('op') == 'create':
                if request.POST.get('model') == 'branch':result = version.createBranch(path=project.project_repo_dir,branchName=request.POST.get('name'))
                elif request.POST.get('model') == 'tag':result = version.createTag(path=project.project_repo_dir,tagName=request.POST.get('name'))
            elif request.POST.get('op') == 'delete':
                if request.POST.get('model') == 'branch':result = version.delBranch(path=project.project_repo_dir,branchName=request.POST.get('name'))
                elif request.POST.get('model') == 'tag':result = version.delTag(path=project.project_repo_dir,tagName=request.POST.get('name')) 
            elif request.POST.get('op') == 'query':
                if project.project_model == 'branch':
                    result = version.log(path=project.project_repo_dir,bName=request.POST.get('name'),number=50)
                    return JsonResponse({'msg':"操作成功","code":200,'data':result}) 
                else:result = version.tag(path=project.project_repo_dir)
            elif request.POST.get('op') == 'histroy':
                result = version.show(path=project.project_repo_dir,branch=request.POST.get('project_branch'),cid=request.POST.get('project_version',None))
                return JsonResponse({'msg':"操作成功","code":200,'data':"<pre> <xmp>" + result[1].replace('<br>','\n') + "</xmp></pre>"}) 
        else:return JsonResponse({'msg':"非法操作","code":500,'data':[]})
        if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})
        else:return JsonResponse({'msg':"操作成功","code":200,'data':[]})    
        
@login_required()
def deploy_run(request,pid): 
    try:
        project = Project_Config.objects.get(id=pid)
        serverList = Project_Number.objects.filter(project=project)
        if project.project_repertory == 'git':version = GitTools()
        elif project.project_repertory == 'svn':version = SvnTools()
    except:
        return render(request,'deploy/deploy_run.html',{"user":request.user,
                                                         "errorInfo":"项目不存在，可能已经被删除."}, 
                                  )     
    if request.method == "GET":
        if project.project_model == 'branch':bList = version.branch(path=project.project_repo_dir) 
        elif project.project_model == 'tag':bList = version.tag(path=project.project_repo_dir) 
        #获取最新版本
        version.pull(path=project.project_repo_dir)        
        vList = version.log(path=project.project_repo_dir, number=50)
        return render(request,'deploy/deploy_run.html',{"user":request.user,
                                                         "project":project,"serverList":serverList,
                                                         "bList":bList,"vList":vList}, 
                                  ) 
        
    elif request.method == "POST":
        if request.POST.getlist('project_server',None):
            serverList = [ Project_Number.objects.get(project=project,server=ds) for ds in request.POST.getlist('project_server') ]
            allServerList = [ ds.server  for ds in Project_Number.objects.filter(project=project) ]
            #获取项目目标服务器列表与分批部署服务器（post提交）列表的差集
            tmpServer = [ i for i in allServerList if i not in request.POST.getlist('project_server') ]
        elif request.POST.get('project_model',None) == "rollback":tmpServer = None
        else:return JsonResponse({'msg':"项目部署失败：未选择目标服务器","code":500,'data':[]}) 
        if DsRedis.OpsProject.get(redisKey=project.project_uuid+"-locked") is None:#判断该项目是否有人在部署
            #给项目部署加上锁
            DsRedis.OpsProject.set(redisKey=project.project_uuid+"-locked",value=request.user)
            DsRedis.OpsDeploy.delete(project.project_uuid)  
            if request.POST.get('project_model',None) == "rollback":
                project_content = "回滚项目"
                if project.project_model == 'branch':
                    verName = request.POST.get('project_version') 
                    trueDir = project.project_dir+project.project_env+'/'+ request.POST.get('project_version')  + '/'
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Start] Start Rollback branch:%s  vesion: %s" % (request.POST.get('project_branch'),request.POST.get('project_version')))
                elif  project.project_model == 'tag':
                    verName = request.POST.get('project_branch') 
                    trueDir = project.project_dir+project.project_env+'/'+ request.POST.get('project_branch') + '/'
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Start] Start Rollback tag:%s" % request.POST.get('project_branch'))
                #创建版本目录
                base.mkdir(dirPath=trueDir)
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Mkdir version dir: {dir} ".format(dir=trueDir))
                #创建快捷方式
                softdir = project.project_dir+project.project.project_name+'/'
                result = base.lns(spath=trueDir, dpath=softdir.rstrip('/'))
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Make softlink cmd:  ln -s  {sdir} {ddir} info: {info}".format(sdir=trueDir,ddir=softdir,info=result[1]))
                if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})    
                #获取要排除的文件 
                exclude = None
                if project.project_exclude:
                    try:
                        exclude = ''
                        for s in project.project_exclude.split(','):
                            exclude =  "--exclude='{file}'".format(file=s.replace('\r\n','').replace('\n','').strip()) + ' ' + exclude
                    except Exception,e:
                        return JsonResponse({'msg':str(e),"code":500,'data':[]})                                 
            else:
                project_content = "部署项目"
                #判断版本上线类型再切换分支到指定的分支/Tag
                if project.project_model == 'branch':
                    bName = request.POST.get('project_branch')
                    result = version.checkOut(path=project.project_repo_dir, name=bName)
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Start] Switched to branch %s" % bName)
                    #reset到指定版本
                    result = version.reset(path=project.project_repo_dir, commintId=request.POST.get('project_version'))
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Git reset to {comid} info: {info}".format(comid=request.POST.get('project_version'),info=result[1])) 
                    trueDir = project.project_dir+project.project_env+'/'+ request.POST.get('project_version')  + '/'
                    verName = bName + '_' + request.POST.get('project_version','未知')
                elif project.project_model == 'tag':
                    bName = request.POST.get('project_branch')
                    result = version.checkOut(path=project.project_repo_dir, name=bName)
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Start] Switched to tag %s" % bName)
                    trueDir = project.project_dir+project.project_env+'/'+ bName + '/'
                    verName = bName
                #创建版本目录
                base.mkdir(dirPath=trueDir)
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Mkdir version dir: {dir} ".format(dir=trueDir))
                #创建快捷方式
                softdir = project.project_dir+project.project.project_name+'/'
                result = base.lns(spath=trueDir, dpath=softdir.rstrip('/'))
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Make softlink cmd:  ln -s  {sdir} {ddir} info: {info}".format(sdir=trueDir,ddir=softdir,info=result[1]))
                if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})      
                #获取要排除的文件 
                exclude = None
                if project.project_exclude:
                    try:
                        exclude = ''
                        for s in project.project_exclude.split(','):
                            exclude =  "--exclude='{file}'".format(file=s.replace('\r\n','').replace('\n','').strip()) + ' ' + exclude
                    except Exception,e:
                        return JsonResponse({'msg':str(e),"code":500,'data':[]})                             
                #执行部署命令  - 编译型语言      
                if project.project_local_command:
                    result =  base.cmds(cmds=project.project_local_command) 
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Execute local command: {cmds} info: {info}".format(cmds=project.project_local_command,info=result[1])) 
                    if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})  
                #非编译型语言
                else:               
                    #配置rsync同步文件到本地目录
                    result = base.rsync(sourceDir=project.project_repo_dir, destDir=trueDir,exclude=exclude)
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Rsync {sDir} to {dDir} exclude {exclude}".format(sDir=project.project_repo_dir,dDir=trueDir,exclude=exclude))  
                    if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})                         
                #授权文件
                result = base.chown(user=project.project_user, path=trueDir)
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Chown {user} to {path}".format(user=project.project_user,path=trueDir)) 
                if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})        
            #调用ansible同步代码到远程服务器上           
            resource = []
            hostList = []
            for ds in serverList:
                server = Server_Assets.objects.get(ip=ds.server) 
                hostList.append(ds.server)
                data = dict()
                if server.keyfile == 1:
                    data['port'] = int(server.port)
                    data["hostname"] = server.ip
                    data["username"] = server.username
                else:
                    data["hostname"] = server.ip
                    data["port"] = int(server.port)
                    data["username"] = server.username
                    data["password"] = server.passwd
                resource.append(data)            
            if resource and hostList:
                if exclude:args = '''src={srcDir} dest={desDir} links=yes recursive=yes compress=yes delete=yes rsync_opts="{exclude}"'''.format(srcDir=softdir, desDir=ds.dir,exclude=exclude)
                else:args = '''src={srcDir} dest={desDir} links=yes recursive=yes compress=yes delete=yes'''.format(srcDir=softdir, desDir=ds.dir)
                ANS = ANSRunner(resource)
                ANS.run_model(host_list=hostList,module_name='synchronize',module_args=args)
                #精简返回的结果
                dataList = ANS.handle_model_data(ANS.get_model_result() , 'synchronize', module_args=args)
                for ds in  dataList:
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Rsync project to {host} status: {status} msg: {msg}".format(host=ds.get('ip'),
                                                                                                                                  status=ds.get('status'),
                                                                                                                                  msg=ds.get('msg')))
                    if ds.get('status') == 'failed':result = (1,ds.get('ip')+ds.get('msg'))
            #目标服务器执行后续命令
            if project.project_remote_command:
                ANS.run_model(host_list=hostList,module_name='raw',module_args=project.project_remote_command)
                #精简返回的结果
                dataList = ANS.handle_model_data(ANS.get_model_result() , 'raw', module_args=project.project_remote_command) 
                for ds in dataList:
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Running] Execute command to {host} status: {status} msg: {msg}".format(host=ds.get('ip'),
                                                                                                                                  status=ds.get('status'),
                                                                                                                                  msg=ds.get('msg')))
                    if ds.get('status') == 'failed':result = (1,"部署错误: " +ds.get('msg'))                           
            if result[0] > 0:
                DsRedis.OpsProject.delete(redisKey=project.project_uuid+"-locked")
                return JsonResponse({'msg':result[1],"code":500,'data':[]}) 
            DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Done] Deploy Success.")
            #切换版本之后取消项目部署锁
            DsRedis.OpsProject.delete(redisKey=project.project_uuid+"-locked") 
            #异步记入操作日志
#             if request.POST.get('project_version'):bName = request.POST.get('project_version') 
            recordProject.delay(project_user=str(request.user),project_id=project.id,
                                project_name=project.project.project_name,project_content=project_content,
                                project_branch=verName)          
            return JsonResponse({'msg':"项目部署成功","code":200,'data':tmpServer}) 
        else:
            return JsonResponse({'msg':"项目部署失败：{user}正在部署改项目，请稍后再提交部署。".format(user=DsRedis.OpsProject.get(redisKey=project.project_uuid+"-locked")),"code":500,'data':[]}) 
                        
@login_required()
def deploy_result(request,pid):
    if request.method == "POST":
        msg = DsRedis.OpsDeploy.rpop(request.POST.get('project_uuid'))
        if msg:return JsonResponse({'msg':msg,"code":200,'data':[]}) 
        else:return JsonResponse({'msg':None,"code":200,'data':[]})
        
@login_required()
@permission_required('OpsManage.can_add_project_order',login_url='/noperm/')
def deploy_ask(request,pid):
    try:
        project = Project_Config.objects.get(id=pid)
        if project.project_repertory == 'git':version = GitTools()
        elif project.project_repertory == 'svn':version = SvnTools()
    except:
        return render(request,'deploy/deploy_ask.html',{"user":request.user,
                                                         "errorInfo":"项目不存在，可能已经被删除."}, 
                                  )     
    if request.method == "GET":
        vList = None
        version.pull(path=project.project_repo_dir)
        if project.project_model == 'branch':
            #获取最新版本
            bList = version.branch(path=project.project_repo_dir) 
            vList = version.log(path=project.project_repo_dir, number=50)
        elif project.project_model == 'tag':
            bList = version.tag(path=project.project_repo_dir) 
        audit_group = Group.objects.get(id=project.project_audit_group)
        userList = [ u.get('username') for u in audit_group.user_set.values()]
        return render(request,'deploy/deploy_ask.html',{"user":request.user,"project":project,
                                                         "userList":userList,"bList":bList,"vList":vList}, 
                                  )  
    elif request.method == "POST":       
        try:      
            order = Project_Order.objects.create(
                                                    order_user = request.user,
                                                    order_project = project, 
                                                    order_subject = request.POST.get('order_subject'),
                                                    order_audit = request.POST.get('order_audit'),
                                                    order_status = request.POST.get('order_status',2),
                                                    order_level = request.POST.get('order_level'),
                                                    order_content = request.POST.get('order_content'),
                                                    order_branch = request.POST.get('order_branch',None),
                                                    order_comid = request.POST.get('order_comid',None),
                                                    order_tag  = request.POST.get('order_tag',None)
                                                    )
            sendDeployNotice.delay(order_id=order.id,mask='【申请中】')
        except Exception,e:
            return render(request,'deploy/deploy_ask.html',{"user":request.user,"errorInfo":"项目部署申请失败：%s" % str(e)},
                                      )   
        return HttpResponseRedirect('/deploy_ask/{id}/'.format(id=pid))   
    
    
@login_required()
def deploy_order(request,page):
    if request.method == "GET":
        allOrderList = Project_Order.objects.filter(Q(order_user=User.objects.get(username=request.user)) |
                                                 Q(order_audit=User.objects.get(username=request.user))).order_by("-id")[0:1000]
        totalOrder = Project_Order.objects.all().count()
        doneOrder = Project_Order.objects.filter(order_status=3).count()
        authOrder = Project_Order.objects.filter(order_status=2).count()
        rejectOrder = Project_Order.objects.filter(order_status=1).count()
        deploy_nmuber = Project_Order.objects.values('order_user').annotate(dcount=Count('order_user'))
        deploy_project =  Project_Order.objects.values('order_project').annotate(dcount=Count('order_project'))
        paginator = Paginator(allOrderList, 25)          
        try:
            orderList = paginator.page(page)
        except PageNotAnInteger:
            orderList = paginator.page(1)
        except EmptyPage:
            orderList = paginator.page(paginator.num_pages)        
        for ds in deploy_project:
            ds['order_project'] = Project_Config.objects.get(id=ds.get('order_project')).project.project_name
        return render(request,'deploy/deploy_order.html',{"user":request.user,"orderList":orderList,
                                                              "totalOrder":totalOrder,"doneOrder":doneOrder,
                                                              "authOrder":authOrder,"rejectOrder":rejectOrder,
                                                              "deploy_nmuber":deploy_nmuber,"deploy_project":deploy_project},
                                  ) 
    elif request.method == "POST" and request.user.has_perm('OpsManage.can_add_project_order'):  
        if request.POST.get('model') in ['disable','auth','finish']:
            try:     
                Project_Order.objects.filter(id=request.POST.get('id')).update(
                                order_status = request.POST.get('order_status'),
                                order_cancel = request.POST.get('order_cancel',None),
                            )
                if request.POST.get('model') == 'auth':
                    sendDeployNotice.delay(order_id=request.POST.get('id'),mask='【已授权】')
                elif request.POST.get('model') == 'finish':
                    sendDeployNotice.delay(order_id=request.POST.get('id'),mask='【已部署】')
                elif request.POST.get('model') == 'disable':
                    sendDeployNotice.delay(order_id=request.POST.get('id'),mask='【已取消】')                   
            except Exception,e:
                return JsonResponse({'msg':"操作失败："+str(e),"code":500,'data':[]}) 
            return JsonResponse({'msg':"操作成功","code":200,'data':[]})                
        else:return JsonResponse({'msg':"非法操作","code":500,'data':[]})
    else:return JsonResponse({'msg':"您无权操作此项","code":500,'data':[]})
        
@login_required()
@permission_required('OpsManage.can_add_project_order',login_url='/noperm/')
def deploy_order_status(request,pid):
    if request.method == "GET":
        try:
            order= Project_Order.objects.get(id=pid)
            serverList = Project_Number.objects.filter(project=order.order_project)
            if order.order_audit == str(request.user):order.order_perm = 'pass'
        except:
            return render(request,'deploy/deploy_ask.html',{"user":request.user,
                                                "errorInfo":"工单不存在，可能已经被删除."}, 
                                              )             
        return render(request,'deploy/deploy_order_status.html',{"user":request.user,"order":order,"serverList":serverList},
                                  ) 
    
    
@login_required()
@permission_required('OpsManage.can_add_project_order',login_url='/noperm/')
def deploy_order_rollback(request,pid):
    if request.method == "GET":
        order= Project_Order.objects.get(id=pid)
        return render(request,'deploy/deploy_order_rollback.html',{"user":request.user,"order":order},) 
    
    
@login_required()
def deploy_manage(request,pid):
    try:
        project = Project_Config.objects.get(id=pid)
        if project.project_repertory == 'git':version = GitTools()
        elif project.project_repertory == 'svn':version = SvnTools()
    except:
        return render(request,'deploy/deploy_manage.html',{"user":request.user,
                                                         "errorInfo":"项目不存在，可能已经被删除."}, 
                                  ) 
    if request.method == "GET":
        #获取最新版本
        version.pull(path=project.project_repo_dir)
        if project.project_model == 'branch':bList = version.branch(path=project.project_repo_dir) 
        elif project.project_model == 'tag':bList = version.tag(path=project.project_repo_dir) 
        vList = version.log(path=project.project_repo_dir, number=50)
        return render(request,'deploy/deploy_manage.html',{"user":request.user,
                                                         "project":project,
                                                         "bList":bList,"vList":vList}, 
                                  )
        
@login_required(login_url='/login')  
def deploy_log(request,page):
    if request.method == "GET":
        allProjectList = Log_Project_Config.objects.all().order_by('-id')[0:1000]
        paginator = Paginator(allProjectList, 25)          
        try:
            projectList = paginator.page(page)
        except PageNotAnInteger:
            projectList = paginator.page(1)
        except EmptyPage:
            projectList = paginator.page(paginator.num_pages)        
        return render(request,'deploy/deploy_log.html',{"user":request.user,"projectList":projectList},
                                  )    