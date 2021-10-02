#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json, datetime, os, time, signal
from asset.models import Tags_Assets, Tags_Server_Assets, Server_Assets
from apply.models import APPLY_CENTER_CONFIG, ApplyTasksModel, Apply_Tasks_Result
from utils.logger import logger
from django.http import QueryDict
from OpsManage.settings import _deploy_tasks
from dao.assets import AssetsSource
from utils.base import makeToken
from django.db.models import Count

class ApplyConfigManage(object):
    def __init__(self):
        super(ApplyConfigManage, self).__init__()    

    def get_apply(self, apply_id):
        try:
            apply = APPLY_CENTER_CONFIG.objects.get(id=apply_id)
            return apply.to_json()
        except Exception as ex:
            return str(ex)        
         
    def create_apply(self, request): 
        if request.POST.get('apply_payload'):
            try:
                payload = json.loads(request.POST.get('apply_payload'))
            except Exception as ex:
                return "the data is not in JSON format: {ex}".format(ex=ex)    
               
        try:
            apply = APPLY_CENTER_CONFIG.objects.create(
                                        apply_name=request.POST.get('apply_name'),
                                        apply_desc=request.POST.get('apply_desc'),
                                        apply_icon=request.FILES.get('apply_icon'),
                                        apply_type=request.POST.get('apply_type'),
                                        apply_playbook=request.POST.get('apply_playbook'),
                                        apply_payload=payload
                                        )
            return apply.to_json()
        except Exception as ex:
            return str(ex)
    
    def update_apply(self, request):  
        
        try:
            payload =  json.loads(QueryDict(request.body).get('apply_id'))
        except Exception as ex:
            return "the data is not in JSON format: {ex}".format(ex=ex)         
        
        try:   
            apply = APPLY_CENTER_CONFIG.objects.get(id=QueryDict(request.body).get('apply_id'))
        except Exception as ex:
            return "更新应用失败: {ex}".format(ex=ex)
        
        try:
            APPLY_CENTER_CONFIG.objects.filter(id=apply.id).update(
                                            apply_name=request.get('apply_name'),
                                            apply_desc=request.get('apply_desc'),
                                            apply_icon=request.get('apply_icon'),
                                            apply_type=request.get('apply_type'),
                                            apply_playbook=request.get('apply_playbook'),
                                            apply_payload=payload
                                            )
        except Exception as ex:
            logger.error(msg="更新应用失败: {ex}".format(ex=str(ex)))
            return "更新应用失败: {ex}".format(ex=str(ex))
        return True 
    
    
    def delete_apply(self, request):  
               
        try:   
            apply = APPLY_CENTER_CONFIG.objects.get(id=QueryDict(request.body).get('apply_id'))
        except Exception as ex:
            return "更新应用失败: {ex}".format(ex=ex)
        
        try:
            apply.delete()
        except Exception as ex:
            logger.error(msg="删除应用失败: {ex}".format(ex=str(ex)))
            return "删除应用失败: {ex}".format(ex=str(ex))
        return True    
    
        
    

class ApplyTaskManager(object):
    def __init__(self):
        super(ApplyTaskManager, self).__init__()
                
        
    def add_deploy_task(self, request,  deploy_task):
        try:
            task = ApplyTasksModel.objects.create(user=request.id, task_id=deploy_task.get('task_id'),
                                              task_per=0, status='ready', deploy_type='playbook',
                                              extra_vars=deploy_task.get('extra_vars')
                                              )
            return task.to_json()
        except Exception as ex:
            logger.error(str(ex))
            return False

        
    def update_deploy_task_status(self, task_id, status=None):
        try:            
            return ApplyTasksModel.objects.filter(task_id=task_id).update(status=status)            
        except Exception as ex:
            logger.error(str(ex))
            return False


    def if_deploy_task_exists(self, task_id):
        task = ApplyTasksModel.objects.get(task_id=task_id)
        return True if task else False

    def get_deploy_task_status(self, task_id):
        try:            
            return ApplyTasksModel.objects.get(task_id=task_id).to_json()        
        except Exception as ex:
            logger.error(str(ex))
            return False

    def stop_deploy_task(self, task_id):
#         deploy_task_info = _deploy_tasks.get(task_id)
#         if deploy_task_info:
#             task_process = deploy_task_info['process']
#             task_process._kill_childs()  #先杀掉子进程
#             task_process.terminate()     #再杀掉ansible主进程
#             if task_process.is_alive():  #判断进程是否存活，如果还存活就调用os模块，强制杀掉
#                 os.kill(task_process.pid, signal.SIGKILL)
#             logger.info("try to terminate task {task_name}, task_pid:{pid}".format(task_name=task_process.name, pid=task_process.pid))
#             time.sleep(1.5) #sleep 1.5秒之后再判断一次
#             if task_process.is_alive():
#                 raise Exception("terminate task {task_name} process failed, task_id:{task_id} , process_pid:{pid}".format(task_name=task_process.name,task_id=task_id, pid=task_process.pid))            
#             del _deploy_tasks[task_id]
        return self.update_deploy_task_status(task_id, status='stop')   
        
    def get_ready_deploy_task(self, seconds):
        update_time = (datetime.datetime.now()-datetime.timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S")
        try:            
            return ApplyTasksModel.objects.filter(status__in=['ready','running'],update_time__gte=update_time).order_by("-id")[:100]          
        except Exception as ex:
            logger.error(str(ex))
            return str(ex)    
        
    def get_not_ready_deploy_task(self, seconds):
        update_time = (datetime.datetime.now()-datetime.timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S")
        try:            
            return ApplyTasksModel.objects.filter(status__in=['stop','failed','finished','expired'],update_time__gte=update_time).order_by("-id")[:100]         
        except Exception as ex:
            logger.error(str(ex))
            return str(ex)       

class ApplyTaskManage(ApplyConfigManage):
    def __init__(self):
        super(ApplyTaskManage, self).__init__()    
    
    
    def is_has_illegal_asset(self, assets, host_payload):
        """判断传入的IP是否有不是CMDB里面的资产"""
        if isinstance(host_payload, dict):
            ip_list = []
            for k,v in host_payload.items():
                for host in host_payload.get(k).get('hosts'):
                    ip = host.get('ip')
                    if ip not in ip_list:
                        ip_list.append(ip)
                             
            sList, source = assets.queryAssetsByIp(ip_list)
            
            if  host_payload != sList:
                return "the CMDB system does not exist for IP"  
                              
        
        elif isinstance(host_payload, list):  
            
            sList, source = assets.queryAssetsByIp(host_payload)
            
            if  host_payload != sList:
                return "the CMDB system does not exist for IP"  
            
        else:
            return "unrecognized type for host field"
        
        del source               
        return sList
    
    def get_task_count(self):
        dataList = []
        for ds in ApplyTasksModel.task_status:
            data = {}
            status = ds[0]
            data["name"] = status
            data["count"] = ApplyTasksModel.objects.filter(status=status).count()
            dataList.append(data)
        dataList.append({"name":"total","count":ApplyTasksModel.objects.all().count()})
        return dataList  
        
    def get_task_id(self,token):
        return ApplyTasksModel.objects.filter(task_id=token,status__in=["ready","running"]).count()

   
    def create_task(self, request): 
        
        if len(_deploy_tasks.keys()) > 10: #有误报可能
            return "deploy task queue is full, waiting for other tasks finish"
        
        try:
            apply = APPLY_CENTER_CONFIG.objects.get(id=request.POST.get('apply_id'))
        except Exception as ex:
            logger.error(str(ex))
            return str(ex)
        
        try:
            apply_hosts =  json.loads(request.POST.get('apply_hosts'))
        except Exception as ex:
            return "the hosts is not in JSON format: {ex}".format(ex=ex)         
        
        host_payload = apply_hosts.get('hosts')
        if len(host_payload) == 0: return "the hosts ip is null"
        
        assets = AssetsSource()
        
        host_list = self.is_has_illegal_asset(assets, host_payload)
        if isinstance(host_list, str):
            return host_list
        
        else:
            if not request.user.is_superuser:
                sList, resource = assets.source(assets.query_user_assets(request,[])) 
                if list(set(host_list).difference(set(sList))) > 0:
                    return "unauthorized assets"     
        del assets
        
        if request.POST.get('apply_payload'):
            try:
                extra_vars =  json.loads(request.POST.get('apply_payload'))
            except Exception as ex:
                return "the payload is not in JSON format: {ex}".format(ex=ex) 
            apply_hosts['extra_vars'] = extra_vars           
        else:
            apply_hosts['extra_vars'] = {}
        
        if os.path.exists(apply.apply_playbook):
            apply_hosts['playbook_path'] = apply.apply_playbook
        else:
            return "{apply_playbook} is not exists".format(apply_playbook=apply.apply_playbook) 
        
        task_id = makeToken(str(datetime.datetime.now()).encode("utf-8"))
        task_count = self.get_task_id(task_id)
        if task_count > 0: 
            return "the task on this host is not finished yet"
        else:
            try:
                return ApplyTasksModel.objects.create(
                                            user=request.user.id,
                                            apply_id=request.POST.get('apply_id'),
                                            task_id=task_id,
                                            task_per=0,
                                            status='ready',
                                            deploy_type='playbook',
                                            payload=json.dumps(apply_hosts)
                                            )
            except Exception as ex:
                return str(ex)   
            
    def get_task_detail(self, task_id):
        data = {}
        stats_msg_list,error_msg_list,lastest_msg_list,task_name_list,err_task_msg_list,stats_task_msg_list,lastest_task_msg_list = [],[],[],[],[],[],[]
        task_deatail = Apply_Tasks_Result.objects.filter(logId=task_id)
        for ds in task_deatail:
            if ds.task_type == 'msg':
                error_msg_list.append(ds.to_json())
                if ds.task_name not in task_name_list:
                    task_name_list.append(ds.task_name)
                
            elif ds.task_type == 'stats':
                stats_msg_list.append(ds.to_json())
                
            elif ds.task_type == 'banner':
                lastest_msg_list.append(ds.to_json())
                  
        if  lastest_msg_list:
            lastest_task_msg_list.append({
                "create_time":lastest_msg_list[-1].get('create_time'),
                "task_name": lastest_msg_list[-1].get("task_name"),
                "task_msg": lastest_msg_list[-1].get('task_msg')      
                })
                     
        stats_msg = ''
        stats_data = {}
        for ds in stats_msg_list:
            stats_data["task_name"] = ds.get("task_name")
            stats_msg = ds.get('task_msg') + '\n' +  stats_msg
            stats_data["create_time"] = ds.get('create_time')
            
        stats_data["task_msg"] =  stats_msg  
        stats_task_msg_list.append(stats_data)
                              
        for ds in task_name_list:
            err_data = {}
            err_data["task_name"] = ds
            err_msg = ''
            for ts in error_msg_list: 
                if ts.get('task_name') == ds:
                    err_msg = err_msg + '\n' + ts.get('task_msg')
                    err_data["create_time"] = ts.get('create_time')
            err_data["task_msg"] = err_msg
            err_task_msg_list.append(err_data)
                          
        data['stats_msg'] = stats_task_msg_list
        data['error_msg'] = err_task_msg_list 
        data['lastest_msg'] = lastest_task_msg_list
        return data
    
    def get_assets_by_ip(self, ipList):
        return [ x.assets for x in Server_Assets.objects.filter(ip__in=ipList) ]
            
    
    def sync_task_to_tags_assets(self, task):
        if task.status != 'finished':
            return "the task is not completed."
        
        assets = AssetsSource()
        
        payload = json.loads(task.payload)
        host_list = self.is_has_illegal_asset(assets,payload.get('hosts'))
        if isinstance(host_list, str):
            return host_list 
        
        del assets
        apply = self.get_apply(task.apply_id)
        if isinstance(apply, str):
            return apply      
        
        assets_list = self.get_assets_by_ip(host_list)
        if len(assets_list)  > 0:  
            try:
                tags_asset = Tags_Assets.objects.get(tags_name=apply.get('apply_name'))
            except:
                try:
                    tags_asset = Tags_Assets.objects.create(tags_name=apply.get('apply_name'))
                except Exception as ex:
                    return str(ex)
            
            for ast in assets_list:
                Tags_Server_Assets.objects.update_or_create(aid=ast, tid=tags_asset)

        else:
            return "No assets can be marked"
                    
        return assets_list
    
    def stop_task(self, task):
        task_manager = ApplyTaskManager()
        return task_manager.stop_deploy_task(task.task_id)
        