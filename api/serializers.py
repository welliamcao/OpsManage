#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from rest_framework import serializers
from asset.models import *
from databases.models import *
from deploy.models import *
from orders.models import *
from sched.models import *
from cicd.models import *
from navbar.models import * 
from wiki.models import *
from orders.models import *
from apply.models import *
from django.contrib.auth.models import Group,User
from django_celery_beat.models  import CrontabSchedule,IntervalSchedule,PeriodicTask
from rest_framework.pagination import CursorPagination

class PageConfig(CursorPagination):
    cursor_query_param  = 'offset'
    page_size = 100     #每页显示2个数据
    ordering = '-id'   #排序
    page_size_query_param = None
    max_page_size = 200

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = User
        fields = ('id','last_login','is_superuser','username',
                  'first_name','last_name','email','is_staff',
                  'is_active','date_joined')       
 

class ServiceSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    class Meta:
        model = Service_Assets
        fields = ('id','service_name','project_name','project_id')
           


class ProjectSerializer(serializers.ModelSerializer):
    service_assets = ServiceSerializer(many=True, read_only=True,required=False)
    class Meta:
        model = Project_Assets
        fields = ('id','project_name','project_owner','service_assets')   
                  

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')
          
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags_Assets
        fields = ('id','tags_name')          

class CabinetSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source='zone.zone_name', read_only=True)
    zone_id = serializers.IntegerField(source='zone.id', read_only=True)
    class Meta:
        model = Cabinet_Assets
        fields = ('id','cabinet_name','zone_name','zone_id')   

class ZoneSerializer(serializers.ModelSerializer):
    cabinet_assets = CabinetSerializer(many=True, read_only=True,required=False)
    class Meta:
        model = Zone_Assets
        fields = ('id','zone_name','zone_network','zone_local','zone_contact','zone_number','cabinet_assets')            

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line_Assets
        fields = ('id','line_name')          

class RaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid_Assets
        fields = ('id','raid_name')         

        
        
class AssetsSerializer(serializers.ModelSerializer):
    crontab_total = serializers.SerializerMethodField(read_only=True,required=False)
    database_total = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = Assets
        fields = ('id','assets_type','name','sn','buy_time','expire_date',
                  'buy_user','management_ip','manufacturer','provider','mark',
                  'model','status','put_zone','group','business','project',
                  'crontab_total','database_total',)  

    def get_crontab_total(self, obj):
        return [ cron.id for cron in obj.crontab_total.all() ]  #返回列表          
    
    def get_database_total(self,obj):
        return [ db.id for db in obj.database_total.all() ]  #返回列表          


class ServerSerializer(serializers.ModelSerializer): 
    assets = AssetsSerializer(required=False)
    class Meta:
        model = Server_Assets
        fields = ('id','ip','hostname','username','port','passwd',
                  'line','cpu','cpu_number','vcpu_number','keyfile',
                  'cpu_core','disk_total','ram_total','kernel',
                  'selinux','swap','raid','system','assets',
                  'sudo_passwd') 
    def create(self, data):
        if(data.get('assets')):
            assets_data = data.pop('assets')
            assets = Assets.objects.create(**assets_data)
        else:
            assets = Assets()
        data['assets'] = assets;
        server = Server_Assets.objects.create(**data)  
        return server 
    
class AssetsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log_Assets
        fields = ('id','assets_id','assets_user','assets_content','assets_type','create_time') 
        

class DeployPlaybookSerializer(serializers.ModelSerializer): 
    class Meta:
        model =  Deploy_Playbook
        fields = ('id','playbook_name','playbook_desc','playbook_vars',
                  'playbook_uuid','playbook_file','playbook_auth_group',
                  'playbook_auth_user')   
        
class DeployModelLogsSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Log_Deploy_Model
        fields = ('id','ans_user','ans_model','ans_args',
                  'ans_server','create_time') 

class DeployModelLogsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploy_CallBack_Model_Result
        fields = ('id','logId','content')
        
class DeployPlaybookLogsSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Log_Deploy_Playbook
        fields = ('id','ans_user','ans_name','ans_content','ans_id',
                  'ans_server','ans_content','create_time') 
        
class DeployPlaybookLogsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploy_CallBack_PlayBook_Result
        fields = ('id','logId','content') 
         
class NetworkSerializer(serializers.ModelSerializer): 
    assets = AssetsSerializer(required=False)
    class Meta:
        model = Network_Assets
        fields = ('id','ip','bandwidth','port_number','firmware',
                  'cpu','stone','configure_detail','assets',
                  'port','passwd','sudo_passwd','username')  
          
    def create(self, data):
        if(data.get('assets')):
            assets_data = data.pop('assets')
            assets = Assets.objects.create(**assets_data)
        else:
            assets = Assets()
        data['assets'] = assets;
        server = Network_Assets.objects.create(**data)  
        return server   
    

class OrderSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    modify_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    class Meta:
        model = Order_System
        fields = ('id','order_subject','order_user','order_status','order_cancel',
                  'order_type','order_level','create_time','modify_time','order_executor')
        extra_kwargs = {
                        'order_subject': {'required': False},
                        'order_user':{'required': False},
                        'order_cancel':{'required': False},
                        'order_type':{'required': False},
                        'order_executor':{'required': False},
                        }                 
        
class DataBaseServerSerializer(serializers.ModelSerializer):
    db_service = serializers.IntegerField(source='db_assets.business', read_only=True)
    db_project = serializers.IntegerField(source='db_assets.project', read_only=True)
    class Meta:
        model = DataBase_Server_Config
        fields = ('id','db_env','db_name','db_assets_id',
                  'db_user','db_port','db_mark','db_type',
                  "db_mode","db_service","db_project",
                  "db_rw")  
        
        
class CustomSQLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_High_Risk_SQL
        fields = ('id','sql')
        
class HistroySQLSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    db_host = serializers.SerializerMethodField(read_only=True,required=False)
    db_name = serializers.SerializerMethodField(read_only=True,required=False)
    db_env = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = SQL_Execute_Histroy
        fields = ('id','exe_sql','exe_user','exec_status','exe_result','db_host','db_name','create_time','db_env','exe_db',"exe_time")        
    
    def get_db_env(self,obj):
        if obj.exe_db.db_env == 'alpha':
            return "开发环境"
        
        elif obj.exe_db.db_env == 'beta':
            return "测试环境"
        
        elif obj.exe_db.db_env =="ga":
            return "生产环境"
        
        else:
            return "未知"
        
        
    def get_db_host(self,obj):
        try:
            return obj.exe_db.db_assets.server_assets.ip
        except:
            return "未知"
    
    def get_db_name(self, obj):
        try:
            return obj.exe_db.db_name   
        except:
            return "未知"        
        
class DeployInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploy_Inventory
        fields = ('id','name', 'desc','user') 
        

class DeployInventoryGroupsSerializer(serializers.ModelSerializer):
    inventory_name = serializers.CharField(source='inventory.inventory_name', read_only=True)
    inventory_id = serializers.IntegerField(source='inventory.id', read_only=True)
    class Meta:
        model = Deploy_Inventory_Groups
        fields = ('id','group_name','ext_vars','inventory_name','inventory_id')
        
class TaskCrontabSerializer(serializers.ModelSerializer):
#     timezone = timezone_field.TimeZoneField(default='Asia/Shanghai')
    class  Meta:
        model = CrontabSchedule
        fields = ('id','minute', 'hour','day_of_week','day_of_month','month_of_year') 
 
class TaskIntervalsSerializer(serializers.ModelSerializer):
    class  Meta:
        model = IntervalSchedule
        fields = ('id','every', 'period')  
               
class PeriodicTaskSerializer(serializers.ModelSerializer):
    class  Meta:
        model = PeriodicTask
        fields = ('id','name', 'task', 'kwargs','last_run_at','total_run_count',
                  'enabled','queue','crontab','interval','args','expires')  
        
class CronSerializer(serializers.ModelSerializer):
    crontab_server = serializers.CharField(source='cron_server.server_assets.ip', read_only=True)
    class  Meta:
        model = Cron_Config
        fields = ('id','cron_minute', 'cron_hour','cron_day','cron_week','cron_month',
                  'cron_user','cron_name','cron_log_path','cron_type','cron_command',
                  'crontab_server','cron_status'
                  ) 
        
class ApschedNodeSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(source='sched_server.server_assets.ip', read_only=True)
    jobs_count = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = Sched_Node
        fields = ('sched_node','port', 'token','enable','ip','jobs_count')         

    def get_jobs_count(self,obj):
        return obj.node_jobs.all().count()      
    
class ApschedNodeJobsSerializer(serializers.ModelSerializer):
    node_detail = serializers.SerializerMethodField(read_only=True,required=False)
    jobs_detail = serializers.SerializerMethodField(read_only=True,required=False)
    alert_detail = serializers.SerializerMethodField(read_only=True,required=False)
    runs = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = Sched_Job_Config
        fields = ("id","job_name","jobs_detail","node_detail","alert_detail","runs")         
    
    def get_node_detail(self,obj):
        return obj.job_node.to_json()
    
    def get_jobs_detail(self, obj):
        if obj.sched_type == "date":data = obj.to_date_json()
        elif obj.sched_type == "interval":data = obj.to_interval_json()
        else:data = obj.to_cron_json()
        return data   

    def get_runs(self,obj):
        return obj.node_jobs_log.all().count()

    def get_alert_detail(self, obj):
        return obj.to_alert_json()    
                     
                     
class ApschedNodeJobsLogsSerializer(serializers.ModelSerializer):
    runtime = serializers.SerializerMethodField(read_only=True,required=False)
    jobname = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = Sched_Job_Logs
        fields = ("id","status","stime","etime","cmd","result","runtime","jobname") 
    
    def get_jobname(self,obj):
        return obj.job_id.job_name 
          
    def get_runtime(self,obj):
        try:
            return obj.etime - obj.stime
        except:
            return 0                            
         
        
class AppsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='project.project_name', read_only=True)
    class  Meta:
        model = Project_Config
        fields = ('id','project_env', 'project_name','project_type','project_local_command','project_repo_dir',
                  'project_exclude','project_address','project_uuid','project_repo_user','project_repo_passwd',
                  'project_repertory','project_status','project_remote_command','project_user','project_model',
                  'project_service','product_name',"project_pre_remote_command") 

class AppsRolesSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Project_Roles    
        fields = ('id','project', 'user','role') 
           
class AppsLogsSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    project_env = serializers.CharField(source='project.project_env', read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    package = serializers.SerializerMethodField(read_only=True,required=False)
    git_version = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = Log_Project_Config
        fields = ('id', 'project_name','username','package','status','project_env','create_time','type','task_id','git_version') 
        
    def get_package(self,obj):
        try:
            return obj.package.split("/")[-1]
        except:
            return "未知"  
          
    def get_git_version(self,obj):
        try:
            if obj.project.project_model == "branch":
                return "分支: " + obj.branch + ' 版本: ' + obj.commit_id[0:10]
            else:
                return "标签: " + obj.tag
        except:
            return "未知"              
        
class AppsLogsRecordSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class  Meta:
        model = Log_Project_Record
        fields = ('id', 'key','msg','title','status','task_id','create_time')        
         

        
class NavTypeNumberSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='nav_type.type_name', read_only=True)
    nav_type_id = serializers.IntegerField(source='nav_type.id', read_only=True)
    class Meta:
        model = Nav_Type_Number
        fields = ('id','nav_name','nav_desc','type_name','nav_type_id','nav_url','nav_img')
           


class NavTypeSerializer(serializers.ModelSerializer):
    nav_type_number = NavTypeNumberSerializer(many=True, read_only=True,required=False)
    class Meta:
        model = Nav_Type
        fields = ('id','type_name','nav_type_number')

class NavThirdNumberSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='nav_third.type_name', read_only=True)
    nav_third_id = serializers.IntegerField(source='nav_third.id', read_only=True)
    class Meta:
        model = Nav_Third_Number
        fields = ('id','nav_name',"type_name",'url','nav_third_id','height','width')
           


class NavThirdSerializer(serializers.ModelSerializer):
    nav_third_number = NavThirdNumberSerializer(many=True, read_only=True,required=False)
    class Meta:
        model = Nav_Third
        fields = ('id','type_name','icon','nav_third_number')
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name')
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')    
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','content','category','author')   
        
class OrdersNoticeConfigSerializer(serializers.ModelSerializer):                        
    class Meta:
        model = Order_Notice_Config
        fields = ('id','order_type','grant_group','mode','number')     
           
class IPVSSerializer(serializers.ModelSerializer):
    sip = serializers.CharField(source='ipvs_assets.server_assets.ip', read_only=True)
    rs_count = serializers.SerializerMethodField(read_only=True,required=False)
    rs_list = serializers.SerializerMethodField(read_only=True,required=False)
    project = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = IPVS_CONFIG
        fields = ('id','vip','port','scheduler','sip','rs_count','persistence','protocol','line','desc','is_active','ipvs_assets','project','rs_list')         
    
        extra_kwargs = {
                        'ipvs_assets': {'required': False},
                        'vip':{'required': False},
                        'port':{'required': False},
                        'scheduler':{'required': False},                   
                        }       
    
    def get_project(self,obj):
        return obj.project()
    
    def get_rs_count(self,obj):
        return obj.ipvs_rs.all().count()  
    
    def get_rs_list(self,obj):
        return [ x.to_json() for x in obj.ipvs_rs.all() ]     
    
class IPVSRealServerSerializer(serializers.ModelSerializer):
    sip = serializers.CharField(source='rs_assets.server_assets.ip', read_only=True)
    vip_detail = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = IPVS_RS_CONFIG
        fields = ('id','ipvs_fw_ip','forword','weight','sip','ipvs_vip','rs_assets','is_active','vip_detail')         
        extra_kwargs = {
                        'rs_assets': {'required': False},
                        'ipvs_fw_ip':{'required': False},
                        'ipvs_vip':{'required': False},
                        'forword':{'required': False},
                        }       
    
    def get_vip_detail(self,obj):
        return obj.ipvs_vip.to_json() 

class IPVSNanmeServerSerializer(serializers.ModelSerializer):
    vip = serializers.CharField(source='ipvs_vip.vip', read_only=True)
    class  Meta:
        model = IPVS_NS_CONFIG
        fields = ('id','nameserver','desc','ipvs_vip','vip')         
        extra_kwargs = {
                        'ipvs_vip':{'required': False},
                        }       
    
  