#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import uuid,os
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OpsManage.models import (Project_Assets,Server_Assets,Project_Config,
                            Project_Number,Log_Project_Config,Service_Assets,Assets)
from OpsManage.utils.git import GitTools
from OpsManage.utils.svn import SvnTools
from OpsManage.utils import base
from OpsManage.data.DsRedisOps import DsRedis
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.contrib.auth.models import User,Group
from OpsManage.views.assets import getBaseAssets
from orders.models import Order_System
from OpsManage.tasks.deploy import recordProject
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from OpsManage.utils.logger import logger
from OpsManage import settings
from dao.assets import AssetsSource

@login_required()
@permission_required('OpsManage.can_add_project_config',login_url='/noperm/')
def deploy_add(request):
    if request.method == "GET":
#         serverList = Server_Assets.objects.all()
        groupList = Group.objects.all()
        return render(request,'deploy/deploy_add.html',{"user":request.user,"groupList":groupList,
                                                        'baseAssets':getBaseAssets(),
                                                        "project_dir":settings.WORKSPACES})
    elif  request.method == "POST":
#         serverList = Server_Assets.objects.all()
        ipList = request.POST.get('server') 
        try:
            proAssets = Project_Assets.objects.get(id=request.POST.get('project_id'))
        except Exception, ex:   
            return JsonResponse({'msg':"部署项目添加失败".format(ex=ex),"code":500,'data':[]})     
        try: 
            project = Project_Config.objects.create(
                                                    project = proAssets,
                                                    project_service = request.POST.get('project_service'),
                                                    project_type = request.POST.get('project_type'),
                                                    project_env = request.POST.get('project_env'), 
                                                    project_name = request.POST.get('project_name'), 
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
            recordProject.delay(project_user=str(request.user),project_id=project.id,project_name=project.project_name,project_content="添加项目")
        except Exception, ex:
            logger.error(msg="部署项目添加失败: {ex}".format(ex=ex))
            return JsonResponse({'msg':"部署项目添加失败: {ex}".format(ex=ex),"code":500,'data':[]})           
        if ipList:
            for sid in ipList.split(','):
                try:
                    assets = Assets.objects.get(id=sid)
                    if hasattr(assets,'server_assets'):
                        Project_Number.objects.create(dir=request.POST.get('dir'),server=assets.server_assets.ip,project=project)
                except Exception, ex:
                    project.delete()
                    logger.error(msg="部署项目添加失败: {ex}".format(ex=ex))
                    return JsonResponse({'msg':"部署项目添加失败: {ex}".format(ex=ex),"code":500,'data':[]})            
    return JsonResponse({'msg':"部署项目添加成功","code":200,'data':[]})
    
@login_required()
@permission_required('OpsManage.can_change_project_config',login_url='/noperm/')
def deploy_modf(request,pid): 
    try:
        project = Project_Config.objects.select_related().get(id=pid)
        tagret_server = Project_Number.objects.filter(project=project)
    except Exception, ex:
        logger.error(msg="修改项目失败: {ex}".format(ex=ex))
        return render(request,'deploy/deploy_modf.html',{"user":request.user,
                                                         "errorInfo":"修改项目失败: {ex}".format(ex=ex)},
                                )  
    if request.method == "GET": 
        serverList = AssetsSource().serverList()
        serviceList = Service_Assets.objects.filter(project=project.project)
        groupList = Group.objects.all()
        server = [ s.server for s in tagret_server]
        for ds in serverList:
            if ds.get('ip') in server:ds['count'] = 1
            else:ds['count'] = 0        
        return render(request,'deploy/deploy_modf.html',{"user":request.user,"project":project,"server":tagret_server,
                                                         "serverList":serverList,"groupList":groupList,"serviceList":serviceList},)         
    elif  request.method == "POST":
        ipList = request.POST.get('server',None)
        try:      
            Project_Config.objects.filter(id=pid).update(
                                                    project_env = request.POST.get('project_env'),  
                                                    project_type = request.POST.get('project_type'),                                                    
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
                                                    project_model = request.POST.get('project_model'),                                                
                                                    )
            recordProject.delay(project_user=str(request.user),project_id=pid,project_name=project.project_name,project_content="修改项目")
        except Exception,ex:
            logger.error(msg="部署项目修改失败: {ex}".format(ex=ex))
            return JsonResponse({'msg':"部署项目修改失败: {ex}".format(ex=ex),"code":500,'data':[]}) 
        if ipList:
            tagret_server_list = [ s.server for s in tagret_server ]
            postServerList = []
            for sid in ipList.split(','):
                try:
                    assets = Assets.objects.get(id=sid)
                    if hasattr(assets,'server_assets'):
                        postServerList.append(assets.server_assets.ip) 
                        if assets.server_assets.ip not in tagret_server_list:     
                            Project_Number.objects.create(dir=request.POST.get('dir'),
                                                          server=assets.server_assets.ip,
                                                          project=project)    
                        elif assets.server_assets.ip in tagret_server_list and request.POST.get('dir'):
                            try:
                                Project_Number.objects.filter(project=project,server=assets.server_assets.ip).update(dir=request.POST.get('dir'))  
                            except Exception,e:
                                logger.warn(msg="部署项目修改目标服务器失败: {ex}".format(ex=ex))                                         
                except Exception,ex:
                    logger.error(msg="部署项目修改失败: {ex}".format(ex=ex))
                    return JsonResponse({'msg':"部署项目修改失败: {ex}".format(ex=ex),"code":500,'data':[]}) 
            #清除目标主机 - 
            delList = list(set(tagret_server_list).difference(set(postServerList)))
            for ip in delList:
                Project_Number.objects.filter(project=project,server=ip).delete()                      
    return JsonResponse({'msg':"部署项目修改成功","code":200,'data':[]})         
        
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
        if project.project_type == 'compile':version.mkdir(dir=project.project_dir)
        result = version.clone(url=project.project_address, dir=project.project_repo_dir, user=project.project_repo_user, passwd=project.project_repo_passwd)
        if result[0] > 0:return  JsonResponse({'msg':result[1],"code":500,'data':[]})
        else:
            Project_Config.objects.filter(id=pid).update(project_status = 1)  
            recordProject.delay(project_user=str(request.user),project_id=project.id,project_name=project.project_name,project_content="初始化项目")              
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
                    version.checkOut(path=project.project_repo_dir, name=request.GET.get('name'))
                    version.pull(path=project.project_repo_dir)                     
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
    except Exception ,ex:
        logger.error(msg="项目部署失败: {ex}".format(ex=ex))
        return render(request,'deploy/deploy_run.html',{"user":request.user,
                                                         "errorInfo":"项目部署失败: {ex}".format(ex=ex)}, 
                                  )     
    if request.method == "GET":
        if project.project_model == 'branch':bList = version.branch(path=project.project_repo_dir) 
        elif project.project_model == 'tag':bList = version.tag(path=project.project_repo_dir) 
        else:bList = version.trunk(path=project.project_repo_dir) 
        if project.project_env == 'uat':
            return render(request,'deploy/deploy_run.html',{"user":request.user,
                                                             "project":project,"serverList":serverList,
                                                             "errorInfo":"正式环境代码部署，请走工单审批流程"}, 
                                      )                    
        #获取最新版本
        version.pull(path=project.project_repo_dir)        
        vList = version.log(path=project.project_repo_dir, number=50) 
        return render(request,'deploy/deploy_run.html',{"user":request.user,
                                                         "project":project,"serverList":serverList,
                                                         "bList":bList,"vList":vList,}, 
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
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Start Rollback branch:%s  vesion: %s" % (request.POST.get('project_branch'),request.POST.get('project_version')))
                elif  project.project_model == 'tag':
                    verName = request.POST.get('project_branch') 
                    trueDir = project.project_dir+project.project_env+'/'+ request.POST.get('project_branch') + '/'
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Start Rollback tag:%s" % request.POST.get('project_branch'))
                #创建版本目录
                base.mkdir(dirPath=trueDir)
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Mkdir version dir: {dir} ".format(dir=trueDir))
                #创建快捷方式
                softdir = project.project_dir+project.project_name+'/'
                result = base.lns(spath=trueDir, dpath=softdir.rstrip('/'))
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Make softlink cmd:  ln -s  {sdir} {ddir} info: {info}".format(sdir=trueDir,ddir=softdir,info=result[1]))
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
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL start get code on server]") 
                project_content = "部署项目"
                #判断版本上线类型再切换分支到指定的分支/Tag
                if project.project_model == 'branch' or project.project_repertory == 'svn':
                    bName = request.POST.get('project_branch')
                    result = version.checkOut(path=project.project_repo_dir, name=bName)
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Switched to branch %s" % bName)
                    #reset到指定版本
                    result = version.reset(path=project.project_repo_dir, commintId=request.POST.get('project_version'))
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Git reset to {comid} info: {info}".format(comid=request.POST.get('project_version'),info=result[1])) 
                    trueDir = project.project_dir+project.project_env+'/'+ request.POST.get('project_version')  + '/'
                    verName = bName + '_' + request.POST.get('project_version','未知')
                elif project.project_model == 'tag':
                    bName = request.POST.get('project_branch')
                    result = version.checkOut(path=project.project_repo_dir, name=bName)
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Switched to tag %s" % bName)
                    trueDir = project.project_dir+project.project_env+'/'+ bName + '/'
                    verName = bName
                #创建版本目录
                base.mkdir(dirPath=trueDir)
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Mkdir version dir: {dir} ".format(dir=trueDir))
                #创建快捷方式
                softdir = project.project_dir+project.project_name+'/'
                result = base.lns(spath=trueDir, dpath=softdir.rstrip('/'))
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[PULL] Make softlink cmd:  ln -s  {sdir} {ddir} info: {info}".format(sdir=trueDir,ddir=softdir,info=result[1]))
                if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})      
                #获取要排除的文件 
                exclude = None
                if project.project_exclude:
                    try:
                        exclude = ''
                        for s in project.project_exclude.split(','):
                            exclude =  "--exclude={file}".format(file=s.replace('\r\n','').replace('\n','').strip()) + ' ' + exclude
                    except Exception,e:
                        return JsonResponse({'msg':str(e),"code":500,'data':[]})                             
                #执行部署命令  - 编译型语言      
                if project.project_local_command and project.project_type == 'compile':
                    tmpFile = '/tmp/' + uuid.uuid4().hex[0:8] + '.sh'
                    with open(tmpFile, 'w') as f:  
                        f.write(project.project_local_command)                      
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[DEPLOY start deploy project]")
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[DEPLOY] try to converting deploy scripts file {tmpFile}".format(tmpFile=tmpFile))
                    result =  base.cmds(cmds='dos2unix {tmpFile}'.format(tmpFile=tmpFile)) 
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[DEPLOY] {cmds} info: {info}".format(cmds='dos2unix {tmpFile}'.format(tmpFile=tmpFile),info=result[1])) 
                    result =  base.cmds(cmds='cd {project_repo_dir} && bash {tmpFile}'.format(tmpFile=tmpFile,project_repo_dir=project.project_repo_dir)) 
                    os.remove(tmpFile)
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[DEPLOY] Execute deploy scripts: {cmds} <br>{info}".format(cmds='bash {tmpFile}'.format(tmpFile=tmpFile),info=result[1].replace('\n','<br>'))) 
                    if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})  
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Pack start package project]")   
                #非编译型语言
                else:            
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Pack start package project]")   
                    #配置rsync同步文件到本地目录
                    result = base.rsync(sourceDir=project.project_repo_dir, destDir=trueDir,exclude=exclude)
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Pack] Rsync {sDir} to {dDir} exclude {exclude}".format(sDir=project.project_repo_dir,dDir=trueDir,exclude=exclude))  
                    if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})                         
                #授权文件
                result = base.chown(user=project.project_user, path=trueDir)
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[Pack] Chown {user} to {path}".format(user=project.project_user,path=trueDir)) 
                if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})        
            #调用ansible同步代码到远程服务器上           
            resource = []
            hostList = []
            for ds in serverList:
                server = Server_Assets.objects.get(ip=ds.server) 
                hostList.append(ds.server)
                data = dict()
                if server.keyfile == 0:data["password"] = server.passwd
                data["ip"] = server.ip
                data["port"] = int(server.port)
                data["username"] = server.username                    
                data["sudo_passwd"] = server.sudo_passwd
                resource.append(data)    
            DsRedis.OpsDeploy.lpush(project.project_uuid, data="[RSYNC start rsync project to remote server]")             
            if resource and hostList:
                if exclude:args = "src={srcDir} dest={desDir} links=yes recursive=yes compress=yes delete=yes rsync_opts='{exclude}'".format(srcDir=softdir, desDir=ds.dir,exclude=exclude.replace(' ',',')[:-1])
                else:args = '''src={srcDir} dest={desDir} links=yes recursive=yes compress=yes delete=yes'''.format(srcDir=softdir, desDir=ds.dir)
                ANS = ANSRunner(resource)
                ANS.run_model(host_list=hostList,module_name='synchronize',module_args=args)
                #精简返回的结果
                dataList = ANS.handle_model_data(ANS.get_model_result() , 'synchronize', module_args=args)
                for ds in  dataList:
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[RSYNC] Rsync project to {host} status: {status} msg: {msg}".format(host=ds.get('ip'),
                                                                                                                                  status=ds.get('status'),
                                                                                                                                  msg=ds.get('msg')))
                    if ds.get('status') == 'failed':result = (1,ds.get('ip')+ds.get('msg'))
            #目标服务器执行后续命令
            if project.project_remote_command:
                DsRedis.OpsDeploy.lpush(project.project_uuid, data="[CMD start run command to remote server]") 
                ANS.run_model(host_list=hostList,module_name='raw',module_args=project.project_remote_command)
                #精简返回的结果
                dataList = ANS.handle_model_data(ANS.get_model_result() , 'raw', module_args=project.project_remote_command) 
                for ds in dataList:
                    DsRedis.OpsDeploy.lpush(project.project_uuid, data="[CMD] Execute command to {host} status: {status} msg: {msg}".format(host=ds.get('ip'),
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
                                project_name=project.project_name,project_content=project_content,
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
@permission_required('orders.can_add_project_order',login_url='/noperm/')
def deploy_order_status(request,pid):
    if request.method == "GET":
        try:
            order= Order_System.objects.get(id=pid)
            order.order_user = User.objects.get(id=order.order_user).username
            serverList = Project_Number.objects.filter(project=order.project_order.order_project)
            if order.order_user == str(request.user):order.order_perm = 'pass'
        except Exception ,ex:
            logger.error(msg="获取代码部署工单失败: {ex}".format(ex=ex))
            return render(request,'orders/deploy_apply.html',{"user":request.user,
                                                "errorInfo":"获取代码部署工单失败: {ex}".format(ex=ex)}, 
                                              )             
        return render(request,'deploy/deploy_order_status.html',{"user":request.user,"order":order,"serverList":serverList},) 
    
    
@login_required()
@permission_required('orders.can_add_project_order',login_url='/noperm/')
def deploy_order_rollback(request,pid):
    if request.method == "GET":
        order= Order_System.objects.get(id=pid)
        order.order_user = User.objects.get(id=order.order_user).username
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
        for ds in allProjectList:
            try:
                ds.project = Project_Config.objects.get(id=ds.project_id)
            except Exception,ex:
                logger.info(msg="项目id: {ex}可能已经被删除了".format(ex=ex))
        paginator = Paginator(allProjectList, 25)          
        try:
            projectList = paginator.page(page)
        except PageNotAnInteger:
            projectList = paginator.page(1)
        except EmptyPage:
            projectList = paginator.page(paginator.num_pages)        
        return render(request,'deploy/deploy_log.html',{"user":request.user,"projectList":projectList},
                                  )    