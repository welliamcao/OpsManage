#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import uuid, json,time
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from dao.app import AppsManage
from utils.logger import logger
from django.http import JsonResponse
from OpsManage import settings
from django.http import HttpResponseRedirect
from dao.redisdb import DsRedis
from utils import base
from dao.assets import AssetsSource
from utils.ansible.runner import ANSRunner
from utils.base import method_decorator_adaptor
from django.contrib.auth.decorators import permission_required      
        
class Config(LoginRequiredMixin,AppsManage,View):
    login_url = '/login/'
    
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:       
            return HttpResponseRedirect('/404/')
    
    @method_decorator_adaptor(permission_required, "apps.project_read_project_config","/403/")      
    def config(self,request, *args, **kwagrs):
        return render(request, 'apps/apps_config.html',{"user":request.user,"assets":self.base(),"project_dir":settings.WORKSPACES})
    
    @method_decorator_adaptor(permission_required, "apps.project_read_project_config","/403/")  
    def info(self,request, *args, **kwagrs):
        res = self.info_apps(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"添加成功","code":200,'data':res})
    
    @method_decorator_adaptor(permission_required, "apps.project_change_project_config","/403/")      
    def init(self,request, *args, **kwagrs):
        res = self.init_apps(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':[]}) 
    
    @method_decorator_adaptor(permission_required, "apps.project_change_project_config","/403/")      
    def edit(self,request, *args, **kwagrs):
        return render(request, 'apps/apps_edit.html',{"user":request.user,"assets":self.base(),"project_dir":settings.WORKSPACES})

    @method_decorator_adaptor(permission_required, "apps.project_add_project_config","/403/")      
    def create(self,request, *args, **kwagrs):
        res = self.create_apps(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})     
        return JsonResponse({'msg':"添加成功","code":200,'data':[]}) 
    
    @method_decorator_adaptor(permission_required, "apps.project_change_project_config","/403/")  
    def update(self,request, *args, **kwagrs):
        res = self.update_apps(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})     
        return JsonResponse({'msg':"修改成功","code":200,'data':[]})         
        
    def get(self, request, *args, **kwagrs):
        return self.allowcator(sub=request.GET.get('type','config'), args=request)
    
    def post(self, request, *args, **kwagrs):
        return self.allowcator(sub=request.POST.get('type'), args=request)
    
class Lists(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request, 'apps/apps_list.html',{"user":request.user})
    
class Manage(LoginRequiredMixin,AppsManage,AssetsSource,View):
    login_url = '/login/' 
    deploy_status = 'success' 
    logs_uuid = None
    deploy_config = {
                     'pull_code':u'【获取指定版本代码】',
                     'pack_code':u'【打包指定版本代码】',
                     'dep_code':u'【执行部署配置命令】',
                     'rsync_code':u'【同步指定版本代码】',
                     'cmd_code':u'【执行部署配置命令】',
                     'rollback_code':u'【回滚指定版本代码】',
                     'done':u'【当前版本代码部署完成】'
                     }
           
    
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:       
            return HttpResponseRedirect('/404/')  
    
    @method_decorator_adaptor(permission_required, "apps.project_read_project_config","/403/")  
    def viewLogs(self,request):
        result = []
        project = self.get_apps(request)
        logPaths = request.POST.get('log_path')
        if project:
            ids = []
            logPathsList = []
            for ds in project.project_number.all():
                ids.append(ds.id) 
                for path in ds.logpath.split(";"):
                    if path not in logPathsList:logPathsList.append(path)
            sList,resource = self.idSource(request.POST.get('server'))
            if logPaths and sList and logPaths in logPathsList:
                if request.POST.get('keywords'):module_args="""grep "{keywords}" {log_path}| tail -n 1000 """.format(keywords=request.POST.get('keywords'),log_path=logPaths) 
                else:module_args="""tail -n 1000 {log_path}""".format(log_path=logPaths) 
                ANS = ANSRunner(resource)
                ANS.run_model(host_list=sList, module_name='raw', module_args=module_args) 
                result = ANS.handle_model_data(ANS.get_model_result(), 'raw', module_args)   
            else:                  
                return JsonResponse({'msg':"日志文件与数据库记录不一致","code":500,'data':[]})
        else:
            return JsonResponse({'msg':"项目不存在","code":500,'data':[]})
        return JsonResponse({'msg':"日志文件与数据库记录不一致","code":200,'data':result})     
        
    def bList(self,project,version):
        if project.project_model == 'branch':
            return version.branch(path=project.project_repo_dir) 
        elif project.project_model == 'tag':
            return  version.tag(path=project.project_repo_dir) 
        else:
            return version.trunk(path=project.project_repo_dir) 
    
    def __verName(self,request,project):
        bName = request.POST.get('project_branch')
        if project.project_model == 'branch' or project.project_repertory == 'svn':
            verName = bName + '|' + request.POST.get('project_version','未知')
        elif project.project_model == 'tag':
            verName = bName
        return verName,bName
    
    def __checkOut(self,request,project,version,runIds):
        verName,bName = self.__verName(request, project)
        #判断版本上线类型再切换分支到指定的分支/Tag
        if project.project_model == 'branch' or project.project_repertory == 'svn':
            result = version.checkOut(path=project.project_repo_dir, name=bName)
            #reset到指定版本
            result = version.reset(path=project.project_repo_dir, commintId=request.POST.get('project_version'))
            trueDir = project.project_dir+project.project_env+'/'+ request.POST.get('project_version')  + '/'
            
        elif project.project_model == 'tag':
            result = version.checkOut(path=project.project_repo_dir, name=bName)
            trueDir = project.project_dir+project.project_env+'/'+ bName + '/'
        
        if result[0] > 0:self.deploy_status = 'failed'
        self.__push_msg(project,runIds, 'pull_code', self.deploy_status, result[1])     
        return (trueDir,verName,result)
    
    def __soft_dir(self,trueDir,project,runIds,code_key='pack_code'):
        #创建版本目录
        base.mkdir(dirPath=trueDir)
        #创建快捷方式
        softdir = project.project_dir+project.project_name+'/'
        result = base.lns(spath=trueDir, dpath=softdir.rstrip('/')) 
        if result[0] > 0:self.deploy_status = 'failed'
        self.__push_msg(project,runIds, code_key, self.deploy_status, result[1])         
        return (softdir,result)
        
    def __exclude(self,project):
        #获取要排除的文件 
        exclude = ''
        for s in project.project_exclude.split(','):
            exclude =  "--exclude={file}".format(file=s.replace('\r\n','').replace('\n','').strip()) + ',' + exclude
        return exclude[:-1]
    
    def __compile(self,project,version,runIds):
        #执行部署命令  - 编译型语言      
        tmpFile = '/tmp/' + uuid.uuid4().hex[0:8] + '.sh'
        with open(tmpFile, 'w') as f:  
            f.write(project.project_local_command)                      
        result =  base.cmds(cmds='dos2unix {tmpFile}'.format(tmpFile=tmpFile)) 
        if result[0] > 0:
            self.deploy_status = 'failed'
            self.__push_msg(project,runIds, 'dep_code', self.deploy_status, result[1]) 
            return result 
        result =  base.cmds(cmds='cd {project_repo_dir} && bash {tmpFile}'.format(tmpFile=tmpFile,project_repo_dir=project.project_repo_dir))
        if result[0] > 0:self.deploy_status = 'failed'
        self.__push_msg(project,runIds, 'dep_code', self.deploy_status, result[1]) 
        return result  

    def __uncompile(self,project,trueDir,exclude,runIds):
        #非编译型语言           
        #配置rsync同步文件到本地目录
        result = base.rsync(sourceDir=project.project_repo_dir, destDir=trueDir,exclude=exclude)
        if result[0] > 0:self.deploy_status = 'failed'
        self.__push_msg(project,runIds, 'pack_code', self.deploy_status, result[1]) 
        return  result    
    
    def __chown(self,project,trueDir,exclude,runIds):
        #授权文件
        result = base.chown(user=project.project_user, path=trueDir)
        self.__push_msg(project,runIds, 'rsync_code', self.deploy_status, result[1])
        if result[0] > 0:self.deploy_status = 'failed'
        self.__push_msg(project,runIds, 'rsync_code', self.deploy_status, result[1])   
        return  result      
    
    def __rsync(self,ansRbt,hostList,project,exclude,softdir,runIds):
        #调用ansible同步代码到远程服务器上        
        numbers = self.get_apps_number(project)#[0].dir
        if numbers:           
            if exclude:args = "src={srcDir} dest={desDir} links=yes recursive=yes compress=yes delete=yes rsync_opts='{exclude}'".format(srcDir=softdir, desDir=numbers[0].get("dir"),exclude=exclude)
            else:args = '''src={srcDir} dest={desDir} links=yes recursive=yes compress=yes delete=yes'''.format(srcDir=softdir, desDir=numbers[0].get("dir"))
            ansRbt.run_model(host_list=hostList,module_name='synchronize',module_args=args)
            #精简返回的结果
            dataList = ansRbt.handle_model_data(ansRbt.get_model_result() , 'synchronize', module_args=args)
            for ds in dataList:
                if ds.get('status') == 'failed':
                    self.deploy_status = 'failed'
                    self.__push_msg(project,runIds, 'rsync_code', 'failed', '<code>'+ ds.get('ip') +'</code><br>' + ds.get('msg'))
                else:
                    self.__push_msg(project,runIds, 'rsync_code', 'success', '<code>'+ ds.get('ip') +'</code><br>' + ds.get('msg'))   
            return dataList
        else:return '项目部署目标主机不存在'       
    
    def __command(self,ansRbt,hostList,project,runIds): 
        #目标服务器执行后续命令
        if project.project_remote_command:
#             DsRedis.OpsDeploy.lpush(project.project_uuid, data="[CMD start run command to remote server]") 
            ansRbt.run_model(host_list=hostList,module_name='raw',module_args=project.project_remote_command)
            #精简返回的结果
            dataList = ansRbt.handle_model_data(ansRbt.get_model_result() , 'raw', module_args=project.project_remote_command) 
            for ds in dataList:
                if ds.get('status') == 'failed':
                    self.deploy_status = 'failed'
                    self.__push_msg(project,runIds, 'cmd_code', 'failed', '<code>'+ ds.get('ip') +'</code><br>' + ds.get('msg'))  
                else:
                    self.__push_msg(project,runIds, 'cmd_code', 'success', '<code>'+ ds.get('ip') +'</code><br>' + ds.get('msg'))                                 
            return dataList 
        else:return '远程命令不存在'         
    
    def __push_msg(self,project,runIds,key,status,result): 
        DsRedis.OpsDeploy.lpush(runIds, 
                                data= json.dumps({
                                        'key':key,
                                        'msg':result,
                                        'status':status,
                                        'user':str(self.request.user),
                                        'ctime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                       })
                                ) 
        #取消项目部署锁
        if key == 'done' and status == 'failed':DsRedis.OpsProject.delete(redisKey=project.project_uuid+"-locked") 
        self.create_apps_log_record(key=key, msg=result, title=self.deploy_config.get(key,'unkonw'), uuid=self.logs_uuid, status=status)
        
    def status(self,request, *args, **kwagrs):
        version,project = self.apps_type(request)
        if project and version:
            #获取最新版本      
            vList = version.log(path=project.project_repo_dir, number=50)                                
            return render(request, 'apps/apps_status.html',{"user":request.user,'project':project,
                                                            'project_data':{
                                                                            'type':project.project_model,
                                                                            'bList':self.bList(project, version),
                                                                            'vList':vList,
                                                                            'number':self.get_number(project),                                                                
                                                                }})
        else:return HttpResponseRedirect('/404/') 
     
    @method_decorator_adaptor(permission_required, "apps.project_change_project_config","/403/")  
    def rollback(self,request):
        version,project = self.apps_type(request)
        runIds = request.POST.get('ans_uuid')
        if self.check_role(request, project):
            if project and runIds:
                if DsRedis.OpsProject.get(redisKey=project.project_uuid+"-locked") is None:#判断该项目是否有人在部署
                    #给项目部署加上锁
                    DsRedis.OpsProject.set(redisKey=project.project_uuid+"-locked",value=request.user)            
                    DsRedis.OpsProject.delete(redisKey=project.project_uuid)
                    try:
                        hostList, resource = self.idSourceList(ids=[ a.server for a in project.project_number.all() ])  
                    except Exception as ex:
                        DsRedis.OpsProject.delete(redisKey=project.project_uuid+"-locked")
                        return JsonResponse({'msg':"项目部署失败: {ex}".format(ex=ex),"code":500,'data':[]}) 
                    if hostList and resource: 
                        self.logs_uuid = uuid.uuid4().hex                          
                        ansRbt = ANSRunner(resource)   
                        trueDir = project.project_dir+project.project_env+'/'+ request.POST.get('project_version').split('|')[-1]  + '/'
                        softdir,result = self.__soft_dir(trueDir, project, runIds, 'rollback_code')    
                        verName,bName = self.__verName(request, project)           
                        logs = self.create_apps_log(project, verName, str(self.request.user), self.logs_uuid, request.POST.get('desc','未知'),"failed","rollback")                           
                        if result[0] > 0:  
                            self.__push_msg(project, runIds, 'done', 'failed', result[1])
                            return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]}) 
                        exclude = self.__exclude(project)  
                        result = self.__rsync(ansRbt, hostList, project, exclude, softdir, runIds)
                        if isinstance(result, str):
                            self.__push_msg(project, runIds, 'done', 'failed', result)
                            return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]})  
                        result = self.__command(ansRbt, hostList, project, runIds)
                        if isinstance(result, str):
                            self.__push_msg(project, runIds, 'done', 'failed', result)
                            return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]})  
                        self.__push_msg(project, runIds, 'done', 'success', '【当前版本代码部署完成】')
                        self.update_apps_log(logs,self.deploy_status)
                        DsRedis.OpsProject.delete(redisKey=project.project_uuid+"-locked")  
                        return JsonResponse({'msg':"项目部署完成","code":200,'data':[]})
                else:
                    return JsonResponse({'msg':"项目部署失败：{user}正在部署改项目，请稍后再提交部署。".format(user=str(DsRedis.OpsProject.get(redisKey=project.project_uuid+"-locked").decode("utf-8"))),"code":500,'data':[]})
            else:
                return JsonResponse({'msg':"项目部署失败: 项目不存在.","code":405,'data':[]})  
        else:                            
            return JsonResponse({'msg':"您无权操作此项","code":500,'data':[]})
                                                 
        
    @method_decorator_adaptor(permission_required, "apps.project_change_project_config","/403/")  
    def deploy(self,request):
        version,project = self.apps_type(request)
        runIds = request.POST.get('ans_uuid')
        if self.check_role(request, project):
            if project and runIds:
                if DsRedis.OpsProject.get(redisKey=project.project_uuid+"-locked") is None:#判断该项目是否有人在部署
                    #给项目部署加上锁
                    DsRedis.OpsProject.set(redisKey=project.project_uuid+"-locked",value=request.user)            
                    DsRedis.OpsProject.delete(redisKey=project.project_uuid)
                    try:
                        hostList, resource = self.idSourceList(ids=[ int(a) for a in request.POST.getlist('server')])  
                    except Exception as ex:
                        DsRedis.OpsProject.delete(redisKey=project.project_uuid+"-locked")
                        return JsonResponse({'msg':"项目部署失败: {ex}".format(ex=ex),"code":500,'data':[]}) 
                    if hostList and resource: 
                        self.logs_uuid = uuid.uuid4().hex                          
                        ansRbt = ANSRunner(resource)
                        trueDir,verName,result = self.__checkOut(request, project, version, runIds)  
                        if result[0] > 0:
                            self.__push_msg(project, runIds, 'done', 'failed', result[1])
                            return JsonResponse({'msg':"项目部署失败:{result}".format(result=result[1]),"code":500,'data':[]}) 
                        logs = self.create_apps_log(project, verName, str(self.request.user), self.logs_uuid, request.POST.get('desc','未知'))            
                        exclude = self.__exclude(project) 
                        if project.project_local_command and project.project_type == 'compile':
                            softdir,result = self.__soft_dir(trueDir, project, runIds, 'dep_code')
                            if result[0] > 0:
                                self.__push_msg(project, runIds, 'done', 'failed', result[1])
                                return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]})                         
                            result = self.__compile(project, version, runIds)
                        else:
                            softdir,result = self.__soft_dir(trueDir, project, runIds)
                            if result[0] > 0:
                                self.__push_msg(project, runIds, 'done', 'failed', result[1])
                                return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]})                        
                            result = self.__uncompile(project, trueDir, exclude, runIds)  
                        if result[0] > 0:
                            self.__push_msg(project, runIds, 'done', 'failed', result[1])
                            return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]})          
                        result = self.__chown(project, trueDir, exclude, runIds)                
                        if  result[0] > 0:
                            self.__push_msg(project, runIds, 'done', 'failed', result[1])
                            return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]})                      
                        result = self.__rsync(ansRbt, hostList, project, exclude, softdir, runIds)
                        if isinstance(result, str):
                            self.__push_msg(project, runIds, 'done', 'failed', result)
                            return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]})  
                        result = self.__command(ansRbt, hostList, project, runIds)
                        if isinstance(result, str):
                            self.__push_msg(project, runIds, 'done', 'failed', result)
                            return JsonResponse({'msg':"项目部署失败:{result}".format(result=result),"code":500,'data':[]})  
                        self.__push_msg(project, runIds, 'done', 'success', '【当前版本代码部署完成】')
                        self.update_apps_log(logs,self.deploy_status)
                        DsRedis.OpsProject.delete(redisKey=project.project_uuid+"-locked") 
                        return JsonResponse({'msg':"项目部署完成","code":200,'data':[]})
                    else:
                        DsRedis.OpsProject.delete(redisKey=project.project_uuid+"-locked")
                        return JsonResponse({'msg':"项目部署失败: 主机资产查询不到.","code":500,'data':[]}) 
                else:
                    return JsonResponse({'msg':"项目部署失败：{user}正在部署改项目，请稍后再提交部署。".format(user=str(DsRedis.OpsProject.get(redisKey=project.project_uuid+"-locked").decode("utf-8"))),"code":500,'data':[]})
            else:
                return JsonResponse({'msg':"项目部署失败: 项目不存在.","code":405,'data':[]}) 
        else:                            
            return JsonResponse({'msg':"您无权操作此项","code":500,'data':[]})                    
    
    @method_decorator_adaptor(permission_required, "apps.project_change_project_config","/403/")  
    def create_branch(self,request):  
        version,project = self.apps_type(request)
        if project.project_model == 'branch':
            result = version.createBranch(path=project.project_repo_dir,branchName=request.POST.get('name'))
        elif request.project_model == 'tag':
            result = version.createTag(path=project.project_repo_dir,tagName=request.POST.get('name'))
        if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})
        else:return JsonResponse({'msg':"操作成功","code":200,'data':[]})   
    
    @method_decorator_adaptor(permission_required, "apps.project_delete_project_config","/403/")     
    def delete_branch(self,request): 
        version,project = self.apps_type(request)
        if project.project_model == 'branch':result = version.delBranch(path=project.project_repo_dir,branchName=request.POST.get('name'))
        elif project.project_model == 'tag':result = version.delTag(path=project.project_repo_dir,tagName=request.POST.get('name'))                                  
        if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})
        else:return JsonResponse({'msg':"操作成功","code":200,'data':[]}) 
    
    def query_repo(self,request):   
        version,project = self.apps_type(request)        
        if project.project_model == 'branch':
            version.checkOut(path=project.project_repo_dir, name=request.GET.get('name'))
            version.pull(path=project.project_repo_dir)   
            result = version.log(path=project.project_repo_dir,bName=request.GET.get('name'),number=50)
            return JsonResponse({'msg':"操作成功","code":200,'data':result}) 
        else:result = version.tag(path=project.project_repo_dir)     
        if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})
        else:return JsonResponse({'msg':"操作成功","code":200,'data':[]}) 
        
    def histroy(self,request):
        version,project = self.apps_type(request)       
        result = version.show(path=project.project_repo_dir,branch=request.GET.get('project_branch'),cid=request.POST.get('project_version',None))
        return JsonResponse({'msg':"操作成功","code":200,'data':"<pre> <xmp>" + result[1].replace('<br>','\n') + "</xmp></pre>"})        
    
    def result(self,request):
        msg = DsRedis.OpsDeploy.rpop(request.POST.get('ans_uuid'))
        if msg:return JsonResponse({'msg':str(msg.decode("utf-8")),"code":200,'data':[]}) 
        else:return JsonResponse({'msg':None,"code":200,'data':[]})        
            
    def get(self, request, *args, **kwagrs):
        return self.allowcator(sub=request.GET.get('type','status'), args=request)    
    
    def post(self,request, *args, **kwagrs):
        return self.allowcator(sub=request.POST.get('type'), args=request)   