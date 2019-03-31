#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import uuid,time
from sched.models import Sched_Node,Sched_Job_Config,Sched_Job_Logs
from utils.logger import logger
from django.http import QueryDict
from .assets import AssetsBase
from utils.sched.rpc import sched_rpc
from django.db.models import Q
from tasks.celery_apsched import apsched_notice

class ApschedBase(object):
    def __init__(self):
        super(ApschedBase, self).__init__()  
    
    def get_nodes_count(self):
        return Sched_Node.objects.all().count()   
    
    def get_jobs_count(self):
        return Sched_Job_Config.objects.all().count()  
    
    def get_jobs_status_count(self,status=0):
        return Sched_Job_Logs.objects.filter(status=status).count()
    
    def get_jobs_status_falied(self):
        return Sched_Job_Logs.objects.filter(~Q(status=0)).count()
        
class ApschedNodeManage(AssetsBase):
    
    def __init__(self):
        super(ApschedNodeManage, self).__init__()  
    
    def schedNode(self,request):
        if request.method == 'GET':cid = request.GET.get('sched_node')
        elif request.method == 'POST':cid = request.POST.get('sched_node')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('sched_node')
        try:
            sched = Sched_Node.objects.get(sched_node=cid)
            return sched
        except Exception as ex:
            logger.warn(msg="获取计划任务节点失败: {ex}".format(ex=ex))
            return False    
    
    def get_node_jobs_by_token(self,token):
        try:
            node = Sched_Node.objects.get(token=token)
        except Exception as ex:
            logger.warn(msg="获取计划任务节点失败: {ex}".format(ex=ex))
            return []  
              
        jobsList = []
        
        if node.enable == 0: return []
        
        for job in node.node_jobs.all():
            if job.status == "running":
                if job.sched_type == "date":data = job.to_date_json()
                elif job.sched_type == "interval":data = job.to_interval_json()
                else:data = job.to_cron_json()
                jobsList.append(data)
            
        return  jobsList            
    
    def create_node(self,request):   
        assets = self.assets(request.POST.get("sched_server"))
        if assets:  
            try:
                sched = Sched_Node.objects.create(
                                            sched_server = assets,
                                            port = request.POST.get('port'),
                                            token = request.POST.get('token'),
                                            enable = request.POST.get('enable',1),
                                        )
                return sched
            except Exception as ex:
                logger.warn(msg="添加节点失败: {ex}".format(ex=ex)) 
                return  "添加节点失败: {ex}".format(ex=ex) 
        else:          
            return "节点资产不存在"
        
    def update_node(self,request):   
        node = self.schedNode(request)
        if node:
            try:
                query_params = dict()
                for ds in QueryDict(request.body).keys():
                    query_params[ds] = QueryDict(request.body).get(ds)                
                return Sched_Node.objects.filter(sched_node=node.sched_node).update(**query_params)
            except Exception as ex:
                logger.warn(msg="修改节点信息失败: {ex}".format(ex=ex))
                return str(ex)   
        else:
            return "节点不存在"  
        
    def delete_node(self,request):   
        node = self.schedNode(request)
        if node:
            try:          
                node.delete()
            except Exception as ex:
                logger.warn(msg="修改节点信息失败: {ex}".format(ex=ex))
                return str(ex)   
        else:
            return "节点不存在"   
        
class ApschedNodeJobsManage(ApschedNodeManage):
    def __init__(self):
        self.jobs_sched_field = ["second","minute","hour","week","day","day_of_week","month","start_date","end_date","run_date"]
        self.jobs_notice_field = ["notice_number","notice_interval"]
        super(ApschedNodeJobsManage, self).__init__()                
    
    
    def queryJobs(self,jobs):
        
        if jobs.sched_type == "cron":
            return jobs.to_cron_json()
        
        elif jobs.sched_type == "interval":
            return jobs.to_interval_json()
        
        elif jobs.sched_type == "date":
            return jobs.to_date_json()  
        
        else:
            return {}      
    
    def schedJobs(self,request):
        if request.method == 'GET':cid = request.GET.get('id')
        elif request.method == 'POST':cid = request.POST.get('id')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('id')
        try:
            jobs = Sched_Job_Config.objects.get(id=cid)
            return jobs
        except Exception as ex:
            logger.warn(msg="获取计划任务失败: {ex}".format(ex=ex))
            return False   
    
    def insert_jobs_logs_by_jid(self,data):
        try:
            jobs = Sched_Job_Config.objects.get(job_id=data.get("jid"))
        except Exception as ex:
            logger.warn(msg="get jobs failed: {ex}".format(ex=ex))
            return "job does not exist"
        
        try:
            data["job_id"] = jobs
            data.pop("jid")
            jobLogs = Sched_Job_Logs.objects.create(**data)
            self.judge_notice(jobs.to_alert_json(), jobLogs.to_json())
            return jobLogs.to_json()
        except Exception as ex:
            msg = "record jobs logs error {ex}".format(ex=str(ex))
            logger.warn(msg)
            return msg               
    
    def judge_notice(self,jobs,jobLogs):
        try:
            atime = int(jobs.get('atime'))
        except:
            atime = 0
        if jobs.get('is_alert') > 0 and int(time.time()) - atime > 0:
            print(jobLogs)
#             apsched_notice.apply_async(**{"jobs":jobs,"jobslog":jobLogs})
                
    def create_jobs(self,request):   
        node = self.schedNode(request)
        if node:  
            if node.enable == 0: return "创建任务失败，节点已下线"
            try:
                sched_jobs = Sched_Job_Config.objects.create(
                                            job_node = node,
                                            job_id = uuid.uuid4(),
                                            job_name = request.POST.get('job_name'),
                                            second = request.POST.get('second'),
                                            minute = request.POST.get('minute'),
                                            hour = request.POST.get('hour'),
                                            week = request.POST.get('week'),
                                            day = request.POST.get('day'),
                                            day_of_week = request.POST.get('day_of_week'),
                                            month = request.POST.get('month'),
                                            job_command = request.POST.get('job_command'),
                                            start_date = request.POST.get('start_date'),
                                            end_date = request.POST.get('end_date'),
                                            run_date = request.POST.get('run_date'),
                                            sched_type = request.POST.get('sched_type'),
                                            status = request.POST.get('status',"remove"),
                                            is_alert = request.POST.get('is_alert'),
                                            notice_type =  request.POST.get('notice_type'),
                                            notice_interval =  request.POST.get('notice_interval',3600),
                                            notice_trigger = request.POST.get('notice_interval',0),
                                            notice_number = request.POST.get('notice_number'),
                                        )
                return sched_jobs
            except Exception as ex:
                logger.error(msg="添加任务失败: {ex}".format(ex=ex)) 
                return  "添加任务失败: {ex}".format(ex=ex) 
        else:          
            return "节点资产不存在，任务添加失败"
           
    def update_jobs(self,request):   
        jobs = self.schedJobs(request)
        if jobs: 
            if jobs.job_node.enable == 0: return "更新任务失败，节点已下线"       
            try:
                query_params = dict()
                if "status" in QueryDict(request.body).keys():
                    for ds in QueryDict(request.body).keys():
                        query_params[ds] = QueryDict(request.body).get(ds) 
                        
                elif "is_alert" in QueryDict(request.body).keys():
                    for ds in QueryDict(request.body).keys():
                        query_params[ds] = QueryDict(request.body).get(ds)                     
                else:     
                    for keys in self.jobs_sched_field:
                        if keys in QueryDict(request.body).keys():
                            query_params[keys] = QueryDict(request.body).get(keys) 
                        else:
                            query_params[keys] = None
                Sched_Job_Config.objects.filter(id=jobs.id).update(**query_params)
            except Exception as ex:
                logger.error(msg="修改任务失败: {ex}".format(ex=ex)) 
                return  "修改任务失败: {ex}".format(ex=ex) 
            
            jobs = Sched_Job_Config.objects.get(id=jobs.id)
            
            if query_params.get("status") == "running": 
                return self.rpc_update_jobs(jobs,"add")
            
            elif query_params.get("status") == "remove": 
                return self.rpc_update_jobs(jobs,"remove")    
                    
            if jobs.status == "running" and "is_alert" not in QueryDict(request.body).keys():
                return self.rpc_update_jobs(jobs,"edit")
        else:          
            return "任务不存在，任务修改失败"     
    
    def delete_jobs(self,request):   
        jobs = self.schedJobs(request)
        if jobs:       
            try:
                self.rpc_update_jobs(jobs,"remove")   
                jobs.delete()
            except Exception as ex:
                logger.error(msg="删除任务失败: {ex}".format(ex=ex)) 
                return  "删除任务失败: {ex}".format(ex=ex)   
        else:          
            return "任务不存在，任务删除失败"       
    
      
    def rpc_update_jobs(self,jobs,uri):
        data = self.queryJobs(jobs)                
        result = sched_rpc.post(url="http://{ip}:{port}/api/v1/{uri}".format(ip=jobs.job_node.sched_server.server_assets.ip,
                                                                                port=jobs.job_node.port,uri=uri),
                                                                                data=data,token=jobs.job_node.token)
        jobs.status = "stopped"
        if isinstance(result, str):
            jobs.save()                     
            return "更新节点任务失败:{result}".format(result=result)                  
        else:           
            if result.get("code") == 200:
                return jobs
            else:
                jobs.save()
                return result.get("msg")       
