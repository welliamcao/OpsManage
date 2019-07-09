#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from cicd.models import Project_Config,Log_Project_Config,Log_Project_Record,Project_Roles
from asset.models import Project_Assets,Service_Assets 
from utils.logger import logger
from .assets import AssetsBase
from django.http import QueryDict
from utils.deploy.git import GitTools
from utils.deploy.svn import SvnTools 
from django.contrib.auth.models import User
from utils import base
import uuid,random,json
from cicd.service.deploy import DeployRunner

class AppsCount:
    def __init__(self):
        super(AppsCount, self).__init__()  
        self.dataList = []
    
    def __get_range_day(self,maxNum=31):
        dataList = []
        count = 1
        while count < maxNum:
            dataList.append((base.changeTotimestamp(base.getDaysAgo(count,"%Y-%m-%d"),"%Y-%m-%d")))
            count = count + 1
        return dataList            
        
    def __get_all_apps(self):
        return Project_Config.objects.all()
    
    def get_apps_release_status(self,project=None):
        dataList = []
        if project:sql = """select id,count(1) as count,`status` from opsmanage_log_project_config where project_id={project} and `status` IN ("success","failed") GROUP BY `status`;""".format(project=project)  
        else:sql = """select id,count(1) as count,`status` from opsmanage_log_project_config where  `status` IN ("success","failed") GROUP BY `status`;"""
        for ds in Log_Project_Config.objects.raw(sql): 
            data = {}
            if ds.status == "success":
                data["value"] = ds.count
                data["label"] = u"成功" 
            else:
                data["value"] = ds.count
                data["label"] = u"失败"
            dataList.append(data)    
        return dataList
    
    
    def get_apps_release_type(self,project=None):
        dataList = []
        if project:sql = """select id,count(1) as count,type from opsmanage_log_project_config where project_id={project} and type IN ("deploy","rollback") GROUP BY type;""".format(project=project)  
        else:sql = """select id,count(1) as count,type from opsmanage_log_project_config where type IN ("deploy","rollback") GROUP BY type;"""
        for ds in Log_Project_Config.objects.raw(sql):
            data = {} 
            if ds.type == "deploy":
                data["label"] = u"部署" 
                data["value"] = ds.count
            else:
                data["value"] = ds.count
                data["label"] = u"回滚"
            dataList.append(data)
        return dataList        
        
    def get_apps_release_by_date(self,dateRange,project=None):
        dataList = []
        dateRange.reverse()
        for startTime in dateRange:
            endTime = startTime + 86400
            if project:
                sql = """SELECT id,IFNULL(count(0),0) as count from opsmanage_log_project_config WHERE  date_format(create_time,"%%Y%%m%%d") >= FROM_UNIXTIME({startTime},'%%Y%%m%%d') and 
                                        date_format(create_time,"%%Y%%m%%d") < FROM_UNIXTIME({endTime},'%%Y%%m%%d') and project_id={project} ;""".format(startTime=startTime,endTime=endTime,project=project)                 
            else:
                sql = """SELECT id,IFNULL(count(0),0) as count from opsmanage_log_project_config WHERE date_format(create_time,"%%Y%%m%%d") >= FROM_UNIXTIME({startTime},'%%Y%%m%%d') and 
                                        date_format(create_time,"%%Y%%m%%d") < FROM_UNIXTIME({endTime},'%%Y%%m%%d');""".format(startTime=startTime,endTime=endTime) 
            release = Log_Project_Config.objects.raw(sql)
            if  release[0].count == 0:dataList.append({"dtime":base.changeTimestampTodatetime(startTime,'%Y-%m-%d'),"value":random.randint(1, 100)})
            else:
                dataList.append({"dtime":base.changeTimestampTodatetime(startTime,'%Y-%m-%d'),"value":release[0].count})       
        return dataList   
        
    
    def all_apps_release(self):
        return self.get_apps_release_by_date(dateRange=self.__get_range_day())
    
    def all_app_release_status(self):
        return self.get_apps_release_status()

    def all_app_release_type(self):
        return self.get_apps_release_type()  
    
    def all_apps_release_count(self):
        dataList = []
        for ds in self.__get_all_apps():
            data = {}
            data["id"] = ds.id
            data["name"] = ds.project_name
            data["count"] = Log_Project_Config.objects.filter(project=ds).count()
            dataList.append(data)
        return dataList
    
    
    def get_all_apps_count(self):
        return {"releaseCount":self.all_apps_release_count(),
                "successRate":self.all_app_release_type()+self.all_app_release_status(),
                "monthCount":self.all_apps_release()
                } 
        
    def get_apps_count(self,pid):
        return {"releaseCount":[],
                "successRate":[],
                "monthCount":[]
                }  
           
        
    
class AppsManage(AssetsBase):
    def __init__(self):
        super(AppsManage, self).__init__() 

           
    def get_apps(self,request):
        if request.method == 'GET':cid = request.GET.get('id')
        elif request.method == 'POST':cid = request.POST.get('id')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('id')
        else:cid = request.get('id')
        try:
            deploy = Project_Config.objects.get(id=cid)
            return deploy
        except Exception as ex:
            logger.warn(msg="获取部署项目失败: {ex}".format(ex=ex))
            return False

    def get_task(self,request):
        if request.method == 'GET':cid = request.GET.get('tasks_id')
        elif request.method == 'POST':cid = request.POST.get('tasks_id')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('tasks_id')
        else:cid = request.get('tasks_id')
        try:
            task = Log_Project_Config.objects.get(id=cid)
            return task
        except Exception as ex:
            logger.warn(msg="获取部署项目任务失败: {ex}".format(ex=ex))
            return False
        
    def apps_type(self,request):
        project = self.get_apps(request)
        if project:
            if project.project_repertory == 'git':
                return GitTools(),project
            elif project.project_repertory == 'svn':
                return  SvnTools(),project
        return (None,None)
    
    def get_apps_number(self,project):
        numbers = []
        try:
            for ds in json.loads(project.project_servers):
                data = {}
                data["id"] = ds
                try:                    
                    data["ip"] = self.assets(ds).server_assets.ip
                except Exception as ex:
                    data["ip"] = "未知"
                numbers.append(data)
        except Exception as ex:
            logger.warn(msg="查询项目部署成员失败: {ex}".format(ex=ex)) 
            return False
        return numbers
    
    def info_apps(self,request):
        project = self.get_apps(request)
        if project:
            data = self.convert_to_dict(project)
            data['project_id'] = Project_Assets.objects.get(id=data['project_id']).project_name
            data['service_name'] = Service_Assets.objects.get(id=data['project_service']).service_name
            data['number'] = self.get_apps_number(project)
            data['roles'] = self.get_role(project)
            data["project_servers"] = json.loads(project.project_servers)
            return data
        return '项目不存在'        
    
         
    def init_apps(self,request):
        project = self.get_apps(request)
        if project:
            if project.project_status == 1:return '项目已经初始化过'  
            DeployRunner(apps_id=project.id).init_apps()   
            project.project_status = 1
            project.save()
            return project
        return '项目不存在'
    
    def create_apps(self,request):
        try:
            project = Project_Assets.objects.get(id=request.POST.get('project_id'))
        except Exception as ex:
            logger.warn(msg="查询项目失败: {ex}".format(ex=ex))            
        try:
            apps = Project_Config.objects.create(
                                                project = project,
                                                project_service = request.POST.get('project_service'),
                                                project_type = request.POST.get('project_type'),
                                                project_env = request.POST.get('project_env'), 
                                                project_name = request.POST.get('project_name'), 
                                                project_is_include = request.POST.get('project_is_include'), 
                                                project_repertory = request.POST.get('project_repertory'), 
                                                project_address = request.POST.get('project_address'),
                                                project_repo_dir = request.POST.get('project_repo_dir'),
                                                project_remote_command = request.POST.get('project_remote_command'),
                                                project_pre_remote_command = request.POST.get('project_pre_remote_command'),
                                                project_local_command = request.POST.get('project_local_command'),
                                                project_dir = request.POST.get('project_dir'),
                                                project_uuid = uuid.uuid4(),
                                                project_exclude = request.POST.get('project_exclude','.git').rstrip(),
                                                project_user = request.POST.get('project_user','root'),
                                                project_model = request.POST.get('project_model'),
                                                project_status = 0,
                                                project_repo_user = request.POST.get('project_repo_user'),
                                                project_repo_passwd = request.POST.get('project_repo_passwd'),
                                                project_servers = json.dumps(request.POST.get('project_servers').split(',')),
                                                project_target_root = request.POST.get('project_target_root'),
                                                project_logpath = request.POST.get('project_logpath'),
                                            )           
        except Exception as ex:
            logger.warn(msg="添加项目部署失败: {ex}".format(ex=ex)) 
            return "添加项目部署失败: {ex}".format(ex=ex)
        return  apps
        
    
    def update_apps(self,request):
        project = self.get_apps(request)
        if project:    
            try:
                project.project_env = request.POST.get('project_env')
                project.project_type = request.POST.get('project_type')
                project.project_repertory = request.POST.get('project_repertory')
                project.project_address = request.POST.get('project_address')
                project.project_remote_command = request.POST.get('project_remote_command')
                project.project_pre_remote_command = request.POST.get('project_pre_remote_command')
                project.project_local_command = request.POST.get('project_local_command')
                project.project_model = request.POST.get('project_model')
                project.project_dir = request.POST.get('project_dir')
                project.project_user = request.POST.get('project_user')
                project.project_is_include = request.POST.get('project_is_include')
                project.project_exclude = request.POST.get('project_exclude')
                project.project_repo_user = request.POST.get('project_repo_user')
                project.project_repo_passwd = request.POST.get('project_repo_passwd')
                project.project_servers = json.dumps(request.POST.get('project_servers').split(','))
                project.project_target_root = request.POST.get('project_target_root')
                project.project_logpath = request.POST.get('project_logpath')               
                project.save()
            except Exception as ex:
                logger.warn(msg="修改项目部署失败: {ex}".format(ex=ex)) 
                return "修改项目部署失败: {ex}".format(ex=ex) 
        return project
   
    def create_apps_log(self,project,version,user,uuid,content,status='failed',type="deploy"):
        try:
            logs = Log_Project_Config.objects.create(
                                          project=project,
                                          user = user,
                                          version = version,
                                          status = status,
                                          uuid = uuid, 
                                          type = type,
                                          content = content                                         
                                          ) 
        except Exception as ex:
            logger.error(msg="记录项目部署日志记录失败: {ex}".format(ex=ex))
            return False
        return logs   

    def update_apps_log(self,logs,status):
        try:
            logs.status = status
            logs.save()
        except Exception as ex:
            logger.error(msg="更新项目部署日志记录失败: {ex}".format(ex=ex))
            return False
        return logs     
    
    def create_app_deploy_record(self,project,username,servers,version,task_id,status="未完成",type="deploy",branch=None,tag=None,package=None):
        try:
            return Log_Project_Config.objects.create(
                                                project = project,
                                                username = username,
                                                commit_id = version,
                                                servers = servers,
                                                branch = branch,
                                                tag = tag,
                                                status = status,
                                                type = type,
                                                task_id = task_id,
                                                package = package,
                                                )  
        except Exception as ex:
            logger.error(msg="记录项目部署日志记录失败: {ex}".format(ex=ex))
            return False           
    
    def create_app_deploy_details_record(self, key, msg, title, task_id, status):   
        try:
            Log_Project_Record.objects.create(
                                          key=key,
                                          msg = msg,
                                          title = title,
                                          status = status,
                                          task_id = task_id,                                          
                                          ) 
        except Exception as ex:
            logger.error(msg="记录项目部署详细日志记录失败: {ex}".format(ex=ex))
            return False     
        
    def get_role(self,project):     
        role_list = []  
        for rl in  project.project_roles.all():           
            role = self.convert_to_dict(rl)
            try:
                user = User.objects.get(id=role['user'])
                role['username'] = user.username
                role['email'] = user.email
            except Exception as ex:
                role['username'] = "未知"
                role['email'] = "未知"                
                logger.warn(msg="获取项目角色管理成员失败: {ex}".format(ex=ex))
            role_list.append(role)   
        return  role_list    
    
    def get_number(self,project): 
        number_list = [] 
        for num in project.project_number.all():
            number = self.convert_to_dict(num)
            try:
                number['ip'] = self.assets(num.server).server_assets.ip
            except Exception as ex:
                logger.warn(msg="获取项目成员主机信息失败: {ex}".format(ex=ex))
            number_list.append(number) 
        return  number_list    
    
    def check_role(self,request,project,role='manage'):
        try:
            return Project_Roles.objects.get(project=project,user=request.user.id,role=role)
        except Exception as ex:
            return False