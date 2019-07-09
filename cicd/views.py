#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import os
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from dao.cicd import AppsManage
from django.http import HttpResponseRedirect,JsonResponse,StreamingHttpResponse
from OpsManage import settings
from utils import base
from dao.assets import AssetsSource
from utils.ansible.runner import ANSRunner
from utils.base import method_decorator_adaptor
from django.contrib.auth.decorators import permission_required      
from .service.deploy import DeployRunner
        
class Config(LoginRequiredMixin,AppsManage,View):
    login_url = '/login/'
    
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:       
            return HttpResponseRedirect('/404/')
    
    @method_decorator_adaptor(permission_required, "cicd.project_read_project_config","/403/")      
    def config(self,request, *args, **kwagrs):
        return render(request, 'cicd/cicd_config.html',{"user":request.user,"assets":self.base(),"project_dir":settings.WORKSPACES})
    
    @method_decorator_adaptor(permission_required, "cicd.project_read_project_config","/403/")  
    def info(self,request, *args, **kwagrs):
        res = self.info_apps(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"添加成功","code":200,'data':res})
    
    @method_decorator_adaptor(permission_required, "cicd.project_change_project_config","/403/")      
    def init(self,request, *args, **kwagrs):
        res = self.init_apps(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':[]}) 
    
    @method_decorator_adaptor(permission_required, "cicd.project_change_project_config","/403/")      
    def edit(self,request, *args, **kwagrs):
        return render(request, 'cicd/cicd_edit.html',{"user":request.user,"assets":self.base(),"project_dir":settings.WORKSPACES})

    @method_decorator_adaptor(permission_required, "cicd.project_add_project_config","/403/")      
    def create(self,request, *args, **kwagrs):
        res = self.create_apps(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})     
        return JsonResponse({'msg':"添加成功","code":200,'data':[]}) 
    
    @method_decorator_adaptor(permission_required, "cicd.project_change_project_config","/403/")  
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
        return render(request, 'cicd/cicd_list.html',{"user":request.user})
    
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
    
    @method_decorator_adaptor(permission_required, "cicd.project_read_project_config","/403/")  
    def viewLogs(self,request):
        result = []
        project = self.get_apps(request)
        logPaths = request.POST.get('log_path')
        if project:
            logPathsList = []
            for path in project.project_logpath.split(";"):
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
             
    def status(self,request, *args, **kwagrs):
        project = self.get_apps(request)
        if project:
            #获取最新版本      
            apps = DeployRunner(apps_id=project.id)                  
            return render(request, 'cicd/cicd_status.html',{"user":request.user,'project':project,
                                                            'project_data':{
                                                                            'type':project.project_model,
                                                                            'bList':apps.list_branch(),
                                                                            'tList': apps.list_tag(),
                                                                            'number':self.get_apps_number(project),                                                                
                                                                }})
        else:
            return HttpResponseRedirect('/404/') 

    def query_repo(self,request):   
        project = self.get_apps(request) 
        if project:    
            apps = DeployRunner(apps_id=project.id) 
            apps.init_apps()  
            if project.project_model == 'branch':                
                result = apps.list_commits(branch=request.GET.get('name'))
                return JsonResponse({'msg':"操作成功","code":200,'data':result}) 
            else:
                result = apps.list_tag()    
                return JsonResponse({'msg':"操作成功","code":200,'data':result})
        else:
            return JsonResponse({'msg':"项目不存在","code":500,'data':[]})
        
    def refresh_branch(self,request):
        project = self.get_apps(request) 
        if project:    
            apps = DeployRunner(apps_id=project.id) 
            apps.init_apps() 
            result = apps.list_branch()   
            return JsonResponse({'msg':"操作成功","code":200,'data':result})
        else:
            return JsonResponse({'msg':"项目不存在","code":500,'data':[]}) 

    def refresh_commit(self,request):
        project = self.get_apps(request) 
        if project:    
            apps = DeployRunner(apps_id=project.id) 
            apps.init_apps() 
            result = apps.list_commits(branch=request.GET.get('name'))   
            return JsonResponse({'msg':"操作成功","code":200,'data':result})
        else:
            return JsonResponse({'msg':"项目不存在","code":500,'data':[]})
    
    def refresh_tag(self,request):
        project = self.get_apps(request) 
        if project:    
            apps = DeployRunner(apps_id=project.id) 
            apps.init_apps() 
            result = apps.list_tag()   
            return JsonResponse({'msg':"操作成功","code":200,'data':result})
        else:
            return JsonResponse({'msg':"项目不存在","code":500,'data':[]})
    
    def download_package(self,request):  
        project = self.get_apps(request)
        task = self.get_task(request)
        if project and task:    
            response = StreamingHttpResponse(base.file_iterator(task.package))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{file_name}'.format(file_name=os.path.basename(task.package))
            return response
        else:
            return JsonResponse({'msg':"项目或者任务不存在","code":500,'data':[]})        
                           
    
    @method_decorator_adaptor(permission_required, "cicd.project_change_project_config","/403/")  
    def create_branch(self,request):  
        version,project = self.apps_type(request)
        if project.project_model == 'branch':
            result = version.createBranch(path=project.project_repo_dir,branchName=request.POST.get('name'))
        elif request.project_model == 'tag':
            result = version.createTag(path=project.project_repo_dir,tagName=request.POST.get('name'))
        if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})
        else:return JsonResponse({'msg':"操作成功","code":200,'data':[]})   
    
    @method_decorator_adaptor(permission_required, "cicd.project_delete_project_config","/403/")     
    def delete_branch(self,request): 
        version,project = self.apps_type(request)
        if project.project_model == 'branch':result = version.delBranch(path=project.project_repo_dir,branchName=request.POST.get('name'))
        elif project.project_model == 'tag':result = version.delTag(path=project.project_repo_dir,tagName=request.POST.get('name'))                                  
        if result[0] > 0:return JsonResponse({'msg':result[1],"code":500,'data':[]})
        else:return JsonResponse({'msg':"操作成功","code":200,'data':[]}) 

        
    def histroy(self,request):
        version,project = self.apps_type(request)       
        result = version.show(path=project.project_repo_dir,branch=request.GET.get('project_branch'),cid=request.POST.get('project_version',None))
        return JsonResponse({'msg':"操作成功","code":200,'data':"<pre> <xmp>" + result[1].replace('<br>','\n') + "</xmp></pre>"})              
            
    def get(self, request, *args, **kwagrs):
        return self.allowcator(sub=request.GET.get('type','status'), args=request)    
    
    def post(self,request, *args, **kwagrs):
        return self.allowcator(sub=request.POST.get('type'), args=request)   