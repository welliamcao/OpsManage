#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from rest_framework import serializers
from OpsManage.models import *
from wiki.models import *
from orders.models import *
from filemanage.models import *
from django.contrib.auth.models import Group,User


class UserSerializer(serializers.ModelSerializer):
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
        fields = ('id','project_name','service_assets')   
                  

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')
          
class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone_Assets
        fields = ('id','zone_name','zone_network','zone_contact','zone_number')         

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line_Assets
        fields = ('id','line_name')          

class RaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid_Assets
        fields = ('id','raid_name')         
        
# class AssetStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Assets_Satus
#         fields = ('id','status_name') 
        
class CronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cron_Config
        fields = ('id','cron_minute','cron_hour','cron_day',
                  'cron_week','cron_month','cron_user',
                  'cron_name','cron_desc','cron_server',
                  'cron_command','cron_script','cron_status') 
        

class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = ('id','assets_type','name','sn','buy_time','expire_date',
                  'buy_user','management_ip','manufacturer','provider',
                  'model','status','put_zone','group','business','project')  
                

class AssetsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log_Assets
        fields = ('id','assets_id','assets_user','assets_content','assets_type','create_time') 
        

class ProjectConfigSerializer(serializers.ModelSerializer): 
    project_number = serializers.StringRelatedField(many=True)
    class Meta:
        model = Project_Config
        fields = ('id','project_env','project_name','project_local_command',
                  'project_repo_dir','project_dir','project_exclude',
                  "project_type",'project_address','project_repertory',
                  'project_status','project_remote_command','project_user',
                  'project_uuid','project_number')   

class DeployLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log_Project_Config
        fields = ('id','project_id','project_user','project_name',
                  'project_content','project_branch','create_time') 

class AnbiblePlaybookSerializer(serializers.ModelSerializer): 
    server_number = serializers.StringRelatedField(many=True)
    class Meta:
        model =  Ansible_Playbook
        fields = ('id','playbook_name','playbook_desc','playbook_vars',
                  'playbook_uuid','playbook_file','playbook_auth_group',
                  'playbook_auth_user','server_number')   
        
class AnsibleModelLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log_Ansible_Model
        fields = ('id','ans_user','ans_model','ans_args',
                  'ans_server','create_time') 
        
class AnsiblePlaybookLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log_Ansible_Playbook
        fields = ('id','ans_user','ans_name','ans_content','ans_id',
                  'ans_server','ans_content','create_time') 

class CronLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log_Cron_Config
        fields = ('id','cron_id','cron_user','cron_name','cron_content',
                  'cron_server','create_time') 

class ServerSerializer(serializers.ModelSerializer): 
    assets = AssetsSerializer(required=False)
#     keyfile = serializers.FileField(max_length=None, use_url=True)
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
    
class DeployOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Order
        fields = ('id','order_project','order_subject','order_content',
                  'order_branch','order_comid','order_tag','order_audit',
                  'order_status','order_level','order_cancel','create_time',
                  'order_user')   
        
class InceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inception_Server_Config
        fields = ('id','db_name','db_host','db_user','db_passwd','db_port',
                  'db_backup_host','db_backup_user','db_backup_port',
                  'db_backup_passwd')   

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_System
        fields = ('id','order_subject','order_status','order_cancel','order_level')         
        
class DataBaseServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBase_Server_Config
        fields = ('id','db_env','db_name','db_host','db_user',
                  'db_passwd','db_port','db_mark','db_service',
                  'db_group','db_project','db_type',"db_mode")  
        
        
class CustomSQLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_High_Risk_SQL
        fields = ('id','sql')
        
class HistroySQLSerializer(serializers.ModelSerializer):
    class Meta:
        model = SQL_Execute_Histroy
        fields = ('id','exe_sql','exe_user','exec_status','exe_result')
        
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


class UploadFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFiles
        fields = ('file_path', 'file_type')  
        
class UploadFilesOrderSerializer(serializers.ModelSerializer):
    files = UploadFilesSerializer(many=True)
    class Meta:
        model = FileUpload_Audit_Order
        fields = ('id', 'dest_path', 'dest_server',
                  'chown_user','chown_rwx','files')  
        
class DownloadFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDownload_Audit_Order
        fields = ('id','order_content', 'dest_server','dest_path') 
        
class AnsibleInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ansible_Inventory
        fields = ('id','name', 'desc','user') 