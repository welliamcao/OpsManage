#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import uuid,os,json
from django.http import QueryDict
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from asset.models import Assets,Project_Assets,Service_Assets
from deploy.models import *
from utils.ansible_api_v2 import ANSRunner
from dao.dispos import DeployScript,DeployPlaybook
from dao.redisdb import DsRedis
from django.contrib.auth.decorators import permission_required
from utils.logger import logger
from dao.assets import AssetsBase,AssetsSource
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.base import method_decorator_adaptor,cmds


class DelolyModel(LoginRequiredMixin,AssetsSource,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request, 'deploy/deploy_model.html',{"user":request.user})  
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_exec_deploy_model","/403/")  
    def post(self, request, *args, **kwagrs):
            sList,resource = self.allowcator(request.POST.get('server_model'), request)
            if len(request.POST.get('custom_model')) > 0:model_name = request.POST.get('custom_model')
            else:model_name = request.POST.get('deploy_model',None)
            if len(sList) > 0:
                redisKey = request.POST.get('ans_uuid')
#                 logId = DeployRecord.Model.insert(user=str(request.user),ans_model=model_name,ans_server=','.join(sList),ans_args=request.POST.get('ansible_args',None))
                DsRedis.OpsAnsibleModel.delete(redisKey)
                DsRedis.OpsAnsibleModel.lpush(redisKey, "[Start] Ansible Model: {model}  ARGS:{args}".format(model=model_name,args=request.POST.get('deploy_args',"None")))
                if request.POST.get('deploy_debug') == 'on':ANS = ANSRunner(resource,redisKey,verbosity=4)
                else:ANS = ANSRunner(hosts=resource,redisKey=redisKey)
                if request.POST.get('server_model') == 'inventory_groups':sList = ",".join(resource.keys())
                ANS.run_model(host_list=sList,module_name=model_name,module_args=request.POST.get('deploy_args',""))
                DsRedis.OpsAnsibleModel.lpush(redisKey, "[Done] Ansible Done.")
                return JsonResponse({'msg':"操作成功","code":200,'data':[]})
            else:
                return JsonResponse({'msg':"操作失败，未选择主机或者该分组没有成员","code":500,'data':[]})
   
    

class DeployRun(LoginRequiredMixin,View):
    login_url = '/login/'
    def post(self, request, *args, **kwagrs):
        redisKey = request.POST.get('ans_uuid')       
        msg = DsRedis.OpsAnsibleModel.rpop(redisKey)
        if msg:return JsonResponse({'msg':msg.decode("utf-8") ,"code":200,'data':[]}) 
        else:return JsonResponse({'msg':None,"code":200,'data':[]})
        
class DeployInventory(LoginRequiredMixin,AssetsBase,View):        
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request, 'deploy/deploy_inventory.html',{"user":request.user,"assets":self.base()})
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_add_deploy_inventory","/403/") 
    def post(self, request, *args, **kwagrs):
        try:
            Deploy_Inventory.objects.create(name=request.POST.get('inventory_name'),
                                             desc=request.POST.get('inventory_desc'),
                                             user=request.user.id)
        except Exception as ex:
            logger.error(msg="添加动态资产失败: {ex}".format(ex=str(ex)))
            return JsonResponse({'msg':"添加动态资产失败: {ex}".format(ex=ex),"code":500,'data':[]})    
        return JsonResponse({'msg':"添加成功","code":200,'data':[]})      
    
    
class DeployInventoryGroups(LoginRequiredMixin,View):      
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        try:
            inventoryGroups = Deploy_Inventory_Groups.objects.get(id=kwagrs.get('id'))
            assetsIds =  [ ds.server for ds in Deploy_Inventory_Groups_Server.objects.filter(groups=inventoryGroups)]
        except Exception as ex:
            return JsonResponse({'msg':"查询动态资产组失败: {ex}".format(ex=ex),"code":500,'data':[]})
        dataList = []                            
        for assets in Assets.objects.all():
            if assets.id in assetsIds:seletcd = 1
            else:seletcd = 0
            try:
                project = Project_Assets.objects.get(id=assets.project).project_name
            except Exception as ex:
                project = '未知'
                logger.warn(msg="查询主机项目信息失败: {ex}".format(ex=str(ex)))  
            try:
                service = Service_Assets.objects.get(id=assets.business).service_name
            except Exception as ex:
                service = '未知' 
                logger.warn(msg="查询主机应用信息失败: {ex}".format(ex=str(ex)))             
            if hasattr(assets,'server_assets'):
                try:
                    dataList.append({"id":assets.id,"ip":assets.server_assets.ip,"project":project,"service":service,"seletcd":seletcd})                       
                except Exception as ex:
                    logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id,ex=ex))                    
            elif hasattr(assets,'network_assets'):
                try:
                    dataList.append({"id":assets.id,"ip":assets.network_assets.ip,"project":project,"service":service,"seletcd":seletcd})                       
                except Exception as ex:
                    logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id,ex=ex))                
        return JsonResponse({'msg':"动态资产组查询成功","code":200,'data':dataList,"vars":json.dumps(inventoryGroups.ext_vars)}) 
     
    @method_decorator_adaptor(permission_required, "deploy.deploy_change_deploy_inventory","/403/") 
    def put(self, request, *args, **kwagrs):
        try:
            inventoryGroups = Deploy_Inventory_Groups.objects.get(id=kwagrs.get('id'))
            assetsIds =  [ ds.server for ds in Deploy_Inventory_Groups_Server.objects.filter(groups=inventoryGroups)]
        except Exception as ex:
            return JsonResponse({'msg':"删除动态资产组失败: {ex}".format(ex=ex),"code":500,'data':[]})      
        try:   
            newAssetsIds = [ int(s) for s in QueryDict(request.body).getlist('sList[]') ]
        except Exception as ex:
            logger.warn(msg="资产组主机成员修改失败: {ex}".format(ex=str(ex)))  
        delsList = list(set(assetsIds).difference(set(newAssetsIds)))
        for aid in newAssetsIds:
            if aid not in assetsIds:
                try:
                    Deploy_Inventory_Groups_Server.objects.create(groups=inventoryGroups,server=aid)
                except Exception as ex:
                    logger.warn(msg="资产组主机成员修改失败: {ex}".format(ex=str(ex))) 
                    return JsonResponse({'msg':"资产组主机成员修改失败: {ex}".format(ex=str(ex)),"code":500,'data':[]})                 
        for did in delsList:
            try:
                server = Deploy_Inventory_Groups_Server.objects.get(groups=inventoryGroups,server=did)
                server.delete()
            except Exception as ex:
                logger.warn(msg="资产组主机成员修改失败: {ex}".format(ex=str(ex))) 
                return JsonResponse({'msg':"资产组主机成员修改失败: {ex}".format(ex=str(ex)),"code":500,'data':[]}) 
        try:                    
            inventoryGroups.ext_vars = json.dumps(eval(QueryDict(request.body).get('ext_vars')))
            inventoryGroups.save()
        except Exception as ex:
            logger.warn(msg="资产组变量修改失败: {ex}".format(ex=str(ex))) 
            return JsonResponse({'msg':"资产组变量修改失败: {ex}".format(ex=str(ex)),"code":500,'data':[]})   
        return JsonResponse({'msg':"资产组信息已更新","code":200,'data':[]})  
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_delete_deploy_inventory","/403/")  
    def delete(self, request, *args, **kwagrs):  
        try:
            inventoryGroups = Deploy_Inventory_Groups.objects.get(id=kwagrs.get('id'))
        except Exception as ex:
            return JsonResponse({'msg':"删除动态资产组失败: {ex}".format(ex=ex),"code":500,'data':[]})   
        inventoryGroups.delete()
        return JsonResponse({'msg':"资产删除成功","code":200,'data':[]})   
    
    
class DeployScripts(LoginRequiredMixin,DeployScript,View):        
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_read_deploy_script","/403/")       
    def get(self, request, *args, **kwagrs):
        if request.GET.get('sid'):
            return JsonResponse({'msg':"数据获取成功","code":200,'data':self.script(request.GET.get('sid'))})
        return render(request, 'deploy/deploy_scripts.html',{"user":request.user,"scriptList":self.scriptList()}) 
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_add_deploy_script","/403/")   
    def post(self, request, *args, **kwagrs):
        res = self.createScript(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"保存成功","code":200,'data':[]})   
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_change_deploy_script","/403/") 
    def put(self, request, *args, **kwagrs):
        res = self.updateScript(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':[]})     

    @method_decorator_adaptor(permission_required, "deploy.deploy_delete_deploy_script","/403/") 
    def delete(self,request, *args, **kwagrs):
        res = self.deleteScript(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"删除成功","code":200,'data':[]})                

class DeployScriptsRun(LoginRequiredMixin,AssetsSource,DeployScript,View):        
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_exec_deploy_script","/403/") 
    def post(self, request, *args, **kwagrs):  
        sList,resource = self.allowcator(request.POST.get('server_model'), request)                                                
        if len(sList) > 0 and request.POST.get('script_file'):             
            filePath = self.saveScript(content=request.POST.get('script_file'),filePath='/tmp/script-{ram}'.format(ram=uuid.uuid4().hex[0:8]))
            redisKey = request.POST.get('ans_uuid')
            DsRedis.OpsAnsibleModel.delete(redisKey)
            DsRedis.OpsAnsibleModel.lpush(redisKey, "[Start] Ansible Model: {model}  Script:{filePath} {args}".format(model='script',filePath=filePath,args=request.POST.get('script_args')))
            if request.POST.get('deploy_debug') == 'on':ANS = ANSRunner(resource,redisKey,verbosity=4)
            else:ANS = ANSRunner(hosts=resource,redisKey=redisKey)
            if request.POST.get('server_model') == 'inventory_groups':sList = ",".join(resource.keys())
            ANS.run_model(host_list=sList,module_name='script',module_args="{filePath} {args}".format(filePath=filePath,args=request.POST.get('script_args')))
            DsRedis.OpsAnsibleModel.lpush(redisKey, "[Done] Ansible Done.")
            try:
                os.remove(filePath)
            except Exception as ex:
                logger.warn(msg="删除文件失败: {ex}".format(ex=ex))             
            return JsonResponse({'msg':"执行成功","code":200,'data':[]})   
        else:
            return JsonResponse({'msg':"操作失败，未选择主机或者该分组没有成员","code":500,'data':[]})   
        
class DeployPlaybooks(LoginRequiredMixin,DeployPlaybook,View):        
    login_url = '/login/'   
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_read_deploy_playbook","/403/")
    def get(self, request, *args, **kwagrs):
        if request.GET.get('pid'):
            return JsonResponse({'msg':"数据获取成功","code":200,'data':self.playbook(request.GET.get('pid'))})
        return render(request, 'deploy/deploy_playbook.html',{"user":request.user,"playbookList":self.playbookList()}) 
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_add_deploy_playbook","/403/")  
    def post(self, request, *args, **kwagrs):
        res = self.createPlaybook(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"保存成功","code":200,'data':[]})     
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_change_deploy_playbook","/403/")
    def put(self, request, *args, **kwagrs):
        res = self.updatePlaybook(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':[]})     
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_delete_deploy_playbook","/403/")
    def delete(self,request, *args, **kwagrs):
        res = self.deletePlaybook(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"删除成功","code":200,'data':[]})   
    
    
class DeployPlaybookRun(LoginRequiredMixin,AssetsSource,DeployPlaybook,View):        
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_exec_deploy_playbook","/403/")
    def post(self, request, *args, **kwagrs):
        try:
            playbook = Deploy_Playbook.objects.get(id=request.POST.get('playbook_id'))
        except Exception as ex:
            return JsonResponse({'msg':ex,"code":500,'data':[]})
        sList,resource = self.allowcator(playbook.playbook_type, request)                                              
        playbook_file = os.getcwd()  + str(playbook.playbook_file)                 
        if playbook.playbook_vars:playbook_vars = playbook.playbook_vars
        else:playbook_vars = request.POST.get('playbook_vars')
        try:
            if len(playbook_vars) == 0:playbook_vars=dict()
            else:playbook_vars = json.loads(playbook_vars)
            playbook_vars['host'] = sList    
        except Exception as ex:
            return JsonResponse({'msg':"{ex}".format(ex=ex),"code":500,'data':[]})
        logId = None#
        #执行ansible playbook
        if request.POST.get('server_model') == 'inventory_groups':sList = ",".join(resource.keys())
        ANS = ANSRunner(hosts=resource,redisKey=request.POST.get('ans_uuid'),logId=logId)                  
        ANS.run_playbook(host_list=sList, playbook_path=playbook_file,extra_vars=playbook_vars)
        DsRedis.OpsAnsiblePlayBook.lpush(request.POST.get('ans_uuid'), "[Done] Ansible Done.")
        #切换版本之后取消项目部署锁
#         DsRedis.OpsAnsiblePlayBookLock.delete(redisKey=playbook.playbook_uuid+'-locked') 
        return JsonResponse({'msg':"操作成功","code":200,'data':[],"statPer":[]})              