#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Assets(models.Model):
    assets_type_choices = (
                          ('server',u'服务器'),
                          ('vmser',u'虚拟机'),
                          ('switch',u'交换机'),
                          ('route',u'路由器'),
                          ('printer',u'打印机'),
                          ('scanner',u'扫描仪'),
                          ('firewall',u'防火墙'),
                          ('storage',u'存储设备'),
                          ('wifi',u'无线设备'),
                          )
    assets_type = models.CharField(choices=assets_type_choices,max_length=100,default='server',verbose_name='资产类型')
    name = models.CharField(max_length=100,verbose_name='资产编号',unique=True)
    sn =  models.CharField(max_length=100,verbose_name='设备序列号',blank=True,null=True)
    buy_time = models.DateField(blank=True,null=True,verbose_name='购买时间')
    expire_date = models.DateField(u'过保修期',null=True, blank=True)
    buy_user = models.SmallIntegerField(blank=True,null=True,verbose_name='购买人')
    management_ip = models.GenericIPAddressField(u'管理IP',blank=True,null=True)
    manufacturer = models.CharField(max_length=100,blank=True,null=True,verbose_name='制造商')
    provider = models.CharField(max_length=100,blank=True,null=True,verbose_name='供货商')
    model = models.CharField(max_length=100,blank=True,null=True,verbose_name='资产型号')
    status = models.SmallIntegerField(blank=True,null=True,verbose_name='状态')
    put_zone = models.SmallIntegerField(blank=True,null=True,verbose_name='放置区域')
    group = models.SmallIntegerField(blank=True,null=True,verbose_name='使用组')
    business = models.SmallIntegerField(blank=True,null=True,verbose_name='业务类型')
    project = models.SmallIntegerField(blank=True,null=True,verbose_name='项目类型')
    host_vars = models.TextField(blank=True,null=True,verbose_name='ansible主机变量')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'opsmanage_assets'
        permissions = (
            ("can_read_assets", "读取资产权限"),
            ("can_change_assets", "更改资产权限"),
            ("can_add_assets", "添加资产权限"),
            ("can_delete_assets", "删除资产权限"),
            ("can_dumps_assets", "导出资产权限"),
        ) 
        verbose_name = '总资产表'  
        verbose_name_plural = '总资产表'  


class Server_Assets(models.Model): 
    assets = models.OneToOneField('Assets') 
    ip = models.CharField(max_length=100,unique=True,blank=True,null=True)  
    hostname = models.CharField(max_length=100,blank=True,null=True)  
    username = models.CharField(max_length=100,blank=True,null=True)  
    passwd = models.CharField(max_length=100,blank=True,null=True)  
    sudo_passwd = models.CharField(max_length=100,blank=True,null=True)
    keyfile =  models.SmallIntegerField(blank=True,null=True)#FileField(upload_to = './upload/key/',blank=True,null=True,verbose_name='密钥文件')
    port = models.DecimalField(max_digits=6,decimal_places=0,blank=True,null=True)
    line = models.SmallIntegerField(blank=True,null=True)
    cpu = models.CharField(max_length=100,blank=True,null=True)
    cpu_number = models.SmallIntegerField(blank=True,null=True)
    vcpu_number = models.SmallIntegerField(blank=True,null=True)
    cpu_core = models.SmallIntegerField(blank=True,null=True)
    disk_total = models.CharField(max_length=100,blank=True,null=True)
    ram_total= models.IntegerField(blank=True,null=True)
    kernel = models.CharField(max_length=100,blank=True,null=True)
    selinux = models.CharField(max_length=100,blank=True,null=True)
    swap = models.CharField(max_length=100,blank=True,null=True)
    raid = models.SmallIntegerField(blank=True,null=True)
    system = models.CharField(max_length=100,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    '''自定义添加只读权限-系统自带了add change delete三种权限'''
    class Meta:
        db_table = 'opsmanage_server_assets'
        permissions = (
            ("can_read_server_assets", "读取服务器资产权限"),
            ("can_change_server_assets", "更改服务器资产权限"),
            ("can_add_server_assets", "添加服务器资产权限"),
            ("can_delete_server_assets", "删除服务器资产权限"),            
        )
        verbose_name = '服务器资产表'  
        verbose_name_plural = '服务器资产表' 


class Network_Assets(models.Model):
    assets = models.OneToOneField('Assets')
    bandwidth =  models.CharField(max_length=100,blank=True,null=True,verbose_name='背板带宽') 
    ip = models.CharField(unique=True,max_length=100,blank=True,null=True,verbose_name='管理ip')
    username = models.CharField(max_length=100,blank=True,null=True)
    passwd = models.CharField(max_length=100,blank=True,null=True) 
    sudo_passwd = models.CharField(max_length=100,blank=True,null=True) 
    port = models.DecimalField(max_digits=6,decimal_places=0,blank=True,null=True)    
    port_number = models.SmallIntegerField(blank=True,null=True,verbose_name='端口个数')
    firmware =  models.CharField(max_length=100,blank=True,null=True,verbose_name='固件版本')
    cpu = models.CharField(max_length=100,blank=True,null=True,verbose_name='cpu型号')
    stone = models.CharField(max_length=100,blank=True,null=True,verbose_name='内存大小')
    configure_detail = models.TextField(max_length=100,blank=True,null=True,verbose_name='配置说明')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)    
    class Meta:
        db_table = 'opsmanage_network_assets'
        permissions = (
            ("can_read_network_assets", "读取网络资产权限"),
            ("can_change_network_assets", "更改网络资产权限"),
            ("can_add_network_assets", "添加网络资产权限"),
            ("can_delete_network_assets", "删除网络资产权限"), 
        ) 
        verbose_name = '网络资产表'  
        verbose_name_plural = '网络资产表' 

    
class Disk_Assets(models.Model):      
    assets = models.ForeignKey('Assets')
    device_volume =  models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘容量') 
    device_status =  models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘状态')
    device_model = models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘型号')
    device_brand = models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘生产商')
    device_serial =  models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘序列号')
    device_slot = models.SmallIntegerField(blank=True,null=True,verbose_name='硬盘插槽')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)   
    class Meta:
        db_table = 'opsmanage_disk_assets'
        permissions = (
            ("can_read_disk_assets", "读取磁盘资产权限"),
            ("can_change_disk_assets", "更改磁盘资产权限"),
            ("can_add_disk_assets", "添加磁盘资产权限"),
            ("can_delete_disk_assets", "删除磁盘资产权限"),             
        ) 
        unique_together = (("assets", "device_slot"))
        verbose_name = '磁盘资产表'  
        verbose_name_plural = '磁盘资产表'  

class Ram_Assets(models.Model):   
    assets = models.ForeignKey('Assets')
    device_model = models.CharField(max_length=100,blank=True,null=True,verbose_name='内存型号')
    device_volume =  models.CharField(max_length=100,blank=True,null=True,verbose_name='内存容量') 
    device_brand = models.CharField(max_length=100,blank=True,null=True,verbose_name='内存生产商')
    device_slot = models.SmallIntegerField(blank=True,null=True,verbose_name='内存插槽')
    device_status = models.CharField(max_length=100,blank=True,null=True,verbose_name='内存状态')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)    
    class Meta:
        db_table = 'opsmanage_ram_assets'
        permissions = (
            ("can_read_ram_assets", "读取内存资产权限"),
            ("can_change_ram_assets", "更改内存资产权限"),
            ("can_add_ram_assets", "添加内存资产权限"),
            ("can_delete_ram_assets", "删除内存资产权限"),             
        ) 
        unique_together = (("assets", "device_slot"))
        verbose_name = '内存资产表'  
        verbose_name_plural = '内存资产表'         
        
class NetworkCard_Assets(models.Model):   
    assets = models.ForeignKey('Assets')
    device =  models.CharField(max_length=20,blank=True,null=True)
    macaddress = models.CharField(u'MAC',max_length=64,blank=True,null=True)
    ip = models.GenericIPAddressField(u'IP', blank=True,null=True)
    module = models.CharField(max_length=50,blank=True,null=True)
    mtu = models.CharField(max_length=50,blank=True,null=True)
    active = models.SmallIntegerField(blank=True,null=True,verbose_name='是否在线')
    class Meta:
        db_table = 'opsmanage_networkcard_assets'
        verbose_name = '服务器网卡资产表'  
        verbose_name_plural = '服务器网卡资产表'  
        unique_together = (("assets", "macaddress"))       
        
class Project_Assets(models.Model):
    '''产品线资产表'''
    project_name = models.CharField(max_length=100,unique=True) 
    class Meta:
        db_table = 'opsmanage_project_assets'
        permissions = (
            ("can_read_project_assets", "读取产品线权限"),
            ("can_change_project_assets", "更改产品线权限"),
            ("can_add_project_assets", "添加产品线权限"),
            ("can_delete_project_assets", "删除产品线权限"),              
        )  
        verbose_name = '项目资产表'  
        verbose_name_plural = '项目资产表' 
              
    
class Service_Assets(models.Model):
    '''业务分组表'''
    project = models.ForeignKey('Project_Assets',related_name='service_assets', on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100) 
    
    class Meta:
        db_table = 'opsmanage_service_assets'
        permissions = (
            ("can_read_service_assets", "读取业务资产权限"),
            ("can_change_service_assets", "更改业务资产权限"),
            ("can_add_service_assets", "添加业务资产权限"),
            ("can_delete_service_assets", "删除业务资产权限"),              
        )  
        unique_together = (("project", "service_name"))
        verbose_name = '业务分组表'  
        verbose_name_plural = '业务分组表'  
                  

class Zone_Assets(models.Model):  
    zone_name = models.CharField(max_length=100,unique=True) 
    zone_contact = models.CharField(max_length=100,blank=True,null=True,verbose_name='机房联系人')
    zone_number = models.CharField(max_length=100,blank=True,null=True,verbose_name='联系人号码')
    zone_network = models.CharField(max_length=100,blank=True,null=True,verbose_name='机房网段')
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_zone_assets'
        permissions = (
            ("can_read_zone_assets", "读取机房资产权限"),
            ("can_change_zone_assets", "更改机房资产权限"),
            ("can_add_zone_assets", "添加机房资产权限"),
            ("can_delete_zone_assets", "删除机房资产权限"),             
        )  
        verbose_name = '机房资产表'  
        verbose_name_plural = '机房资产表'         
                
class Line_Assets(models.Model):   
    line_name = models.CharField(max_length=100,unique=True)     
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_line_assets'
        permissions = (
            ("can_read_line_assets", "读取出口线路资产权限"),
            ("can_change_line_assetss", "更改出口线路资产权限"),
            ("can_add_line_assets", "添加出口线路资产权限"),
            ("can_delete_line_assets", "删除出口线路资产权限"),             
        )
        verbose_name = '出口线路资产表'  
        verbose_name_plural = '出口线路资产表' 
        
class Raid_Assets(models.Model):   
    raid_name = models.CharField(max_length=100,unique=True)    
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_raid_assets'
        permissions = (
            ("can_read_raid_assets", "读取Raid资产权限"),
            ("can_change_raid_assets", "更改Raid资产权限"),
            ("can_add_raid_assets", "添加Raid资产权限"),
            ("can_delete_raid_assets", "删除Raid资产权限"),             
        )
        verbose_name = 'Raid资产表'  
        verbose_name_plural = 'Raid资产表' 

class Log_Assets(models.Model): 
    assets_id = models.IntegerField(verbose_name='资产类型id',blank=True,null=True,default=None)
    assets_user = models.CharField(max_length=50,verbose_name='操作用户',default=None)
    assets_content = models.CharField(max_length=100,verbose_name='名称',default=None)
    assets_type = models.CharField(max_length=50,default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'opsmanage_log_assets'
        verbose_name = '项目配置操作记录表'  
        verbose_name_plural = '项目配置操作记录表' 
         

class Project_Config(models.Model):  
    project_repertory_choices = (
                          ('git',u'git'),
                          ('svn',u'svn'),
                          )   
    deploy_model_choices =  (
                          ('branch',u'branch'),
                          ('tag',u'tag'),
                          )  
    project = models.ForeignKey('Project_Assets',related_name='project_config', on_delete=models.CASCADE) 
    project_env = models.CharField(max_length=50,verbose_name='项目环境',default=None)
    project_name =  models.CharField(max_length=100,verbose_name='项目名称',default=None)
    project_service = models.SmallIntegerField(verbose_name='业务类型')
    project_type = models.CharField(max_length=10,verbose_name='编译类型')
    project_local_command = models.TextField(blank=True,null=True,verbose_name='部署服务器要执行的命令',default=None)
    project_repo_dir = models.CharField(max_length=100,verbose_name='本地仓库目录',default=None)
    project_dir = models.CharField(max_length=100,verbose_name='代码目录',default=None)
    project_exclude = models.TextField(blank=True,null=True,verbose_name='排除文件',default=None)
    project_address = models.CharField(max_length=100,verbose_name='版本仓库地址',default=None)
    project_uuid = models.CharField(max_length=50,verbose_name='唯一id')
    project_repo_user = models.CharField(max_length=50,verbose_name='仓库用户名',blank=True,null=True)
    project_repo_passwd = models.CharField(max_length=50,verbose_name='仓库密码',blank=True,null=True)
    project_repertory = models.CharField(choices=project_repertory_choices,max_length=10,verbose_name='仓库类型',default=None)
    project_status = models.SmallIntegerField(verbose_name='是否激活',blank=True,null=True,default=None)
    project_remote_command = models.TextField(blank=True,null=True,verbose_name='部署之后执行的命令',default=None)
    project_user = models.CharField(max_length=50,verbose_name='项目文件宿主',default=None) 
    project_model = models.CharField(choices=deploy_model_choices,max_length=10,verbose_name='上线类型',default=None)
    project_audit_group = models.SmallIntegerField(verbose_name='项目授权组',blank=True,null=True,default=None)
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_project_config'
        permissions = (
            ("can_read_project_config", "读取项目部署权限"),
            ("can_change_project_config", "更改项目部署权限"),
            ("can_add_project_config", "添加项目部署权限"),
            ("can_delete_project_config", "删除项目部署权限"),               
        )
        unique_together = (("project_env", "project","project_name"))
        verbose_name = '项目管理表'  
        verbose_name_plural = '项目管理表'  

class Log_Project_Config(models.Model):
    project_id = models.IntegerField(verbose_name='项目id',blank=True,null=True,default=None)
    project_user = models.CharField(max_length=50,verbose_name='操作用户',default=None)
    project_name = models.CharField(max_length=100,verbose_name='名称',default=None)
    project_content = models.CharField(max_length=100,default=None)
    project_branch = models.CharField(max_length=100,default=None,blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'opsmanage_log_project_config'
        verbose_name = '项目配置操作记录表'  
        verbose_name_plural = '项目配置操作记录表'                
        
class Project_Number(models.Model):
    project = models.ForeignKey('Project_Config',related_name='project_number', on_delete=models.CASCADE)
    server =  models.CharField(max_length=100,verbose_name='服务器IP',default=None)
    dir =  models.CharField(max_length=100,verbose_name='项目目录',default=None)
    class Meta:
        db_table = 'opsmanage_project_number'
        unique_together = (("project", "server"))
        verbose_name = '项目成员表'  
        verbose_name_plural = '项目成员表' 
        
    def __unicode__(self):
        return '%s,%s' % ( self.server,self.dir)         
        
      
                        
        
class Cron_Config(models.Model): 
    cron_server = models.ForeignKey('Server_Assets') 
    cron_minute = models.CharField(max_length=10,verbose_name='分',default=None)
    cron_hour = models.CharField(max_length=10,verbose_name='时',default=None)
    cron_day = models.CharField(max_length=10,verbose_name='天',default=None)
    cron_week = models.CharField(max_length=10,verbose_name='周',default=None)
    cron_month = models.CharField(max_length=10,verbose_name='月',default=None)
    cron_user = models.CharField(max_length=50,verbose_name='任务用户',default=None)
    cron_name = models.CharField(max_length=100,verbose_name='任务名称',default=None)
    cron_desc = models.CharField(max_length=200,blank=True,null=True,verbose_name='任务描述',default=None)
    cron_command = models.CharField(max_length=200,verbose_name='任务参数',default=None)
    cron_script = models.FileField(upload_to = './cron/',blank=True,null=True,verbose_name='脚本路径',default=None)
    cron_script_path =  models.CharField(max_length=100,blank=True,null=True,verbose_name='脚本路径',default=None)
    cron_status = models.SmallIntegerField(verbose_name='任务状态',default=None)
    class Meta:
        db_table = 'opsmanage_cron_config'
        permissions = (
            ("can_read_cron_config", "读取任务配置权限"),
            ("can_change_cron_config", "更改任务配置权限"),
            ("can_add_cron_config", "添加任务配置权限"),
            ("can_delete_cron_config", "删除任务配置权限"),            
        )
        verbose_name = '任务配置表'  
        verbose_name_plural = '任务配置表' 
        unique_together = (("cron_name", "cron_server","cron_user"))
        
class Log_Cron_Config(models.Model): 
    cron_id = models.IntegerField(verbose_name='id',blank=True,null=True,default=None)
    cron_user = models.CharField(max_length=50,verbose_name='操作用户',default=None)
    cron_name = models.CharField(max_length=100,verbose_name='名称',default=None)
    cron_content = models.CharField(max_length=100,default=None)
    cron_server = models.CharField(max_length=100,default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'opsmanage_log_cron_config'
        verbose_name = '任务配置操作记录表'  
        verbose_name_plural = '任务配置操作记录表'
        
class Log_Ansible_Model(models.Model): 
    ans_user = models.CharField(max_length=50,verbose_name='使用用户',default=None)
    ans_model = models.CharField(max_length=100,verbose_name='模块名称',default=None)
    ans_args = models.CharField(max_length=500,blank=True,null=True,verbose_name='模块参数',default=None)
    ans_server = models.TextField(verbose_name='服务器',default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'opsmanage_log_ansible_model'
        permissions = (
            ("can_read_log_ansible_model", "读取Ansible模块执行记录权限"),
            ("can_change_log_ansible_model", "更改Ansible模块执行记录权限"),
            ("can_add_log_ansible_model", "添加Ansible模块执行记录权限"),
            ("can_delete_log_ansible_model", "删除Ansible模块执行记录权限"),         
        )
        verbose_name = 'Ansible模块执行记录表'  
        verbose_name_plural = 'Ansible模块执行记录表' 
        
class Ansible_Playbook(models.Model): 
    type = (
             ('service',u'service'),
             ('group',u'group'),
             ('custom',u'custom'),
             )    
    playbook_name = models.CharField(max_length=50,verbose_name='剧本名称',unique=True)
    playbook_desc = models.CharField(max_length=200,verbose_name='功能描述',blank=True,null=True)
    playbook_vars = models.TextField(verbose_name='模块参数',blank=True,null=True)
    playbook_uuid = models.CharField(max_length=50,verbose_name='唯一id')
    playbook_server_model = models.CharField(choices=type,verbose_name='服务器选择类型',max_length=10,blank=True,null=True)
    playbook_server_value = models.SmallIntegerField(verbose_name='服务器选择类型值',blank=True,null=True)
    playbook_file = models.FileField(upload_to = './playbook/',verbose_name='剧本路径')
    playbook_auth_group = models.SmallIntegerField(verbose_name='授权组',blank=True,null=True)
    playbook_auth_user = models.SmallIntegerField(verbose_name='授权用户',blank=True,null=True,)
    playbook_type = models.SmallIntegerField(verbose_name='剧本类型',blank=True,null=True,default=0)
    class Meta:
        db_table = 'opsmanage_ansible_playbook'
        permissions = (
            ("can_read_ansible_playbook", "读取Ansible剧本权限"),
            ("can_change_ansible_playbook", "更改Ansible剧本权限"),
            ("can_add_ansible_playbook", "添加Ansible剧本权限"),
            ("can_delete_ansible_playbook", "删除Ansible剧本权限"),        
            ("can_exec_ansible_playbook", "执行Ansible剧本权限"),       
        )
        verbose_name = 'Ansible剧本配置表'  
        verbose_name_plural = 'Ansible剧本配置表' 
        
        
class Ansible_Script(models.Model): 
    script_name = models.CharField(max_length=50,verbose_name='脚本名称',unique=True)
    script_uuid = models.CharField(max_length=50,verbose_name='唯一id')
    script_server = models.TextField(max_length=200,verbose_name='目标机器',blank=True,null=True)
    script_file = models.FileField(upload_to = './script/',verbose_name='脚本路径')
    script_service = models.SmallIntegerField(verbose_name='授权业务',blank=True,null=True)
    script_group = models.SmallIntegerField(verbose_name='授权组',blank=True,null=True)
    script_type = models.CharField(max_length=50,verbose_name='脚本类型',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_ansible_script'
        permissions = (
            ("can_read_ansible_script", "读取Ansible脚本权限"),
            ("can_change_ansible_script", "更改Ansible脚本权限"),
            ("can_add_ansible_script", "添加Ansible脚本权限"),
            ("can_delete_ansible_script", "删除Ansible脚本权限"),   
            ("can_exec_ansible_script", "执行Ansible脚本权限"),    
            ("can_exec_ansible_model", "执行Ansible模块权限"),      
            ("can_read_ansible_model", "读取Ansible模块权限"),   
        )
        verbose_name = 'Ansible脚本配置表'  
        verbose_name_plural = 'Ansible脚本配置表'         

        

class Log_Ansible_Playbook(models.Model): 
    ans_id = models.IntegerField(verbose_name='id',blank=True,null=True,default=None)
    ans_user = models.CharField(max_length=50,verbose_name='使用用户',default=None)
    ans_name = models.CharField(max_length=100,verbose_name='模块名称',default=None)
    ans_content = models.CharField(max_length=100,default=None)
    ans_server = models.TextField(verbose_name='服务器',default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'opsmanage_log_ansible_playbook'
        permissions = (
            ("can_read_log_ansible_playbook", "读取Ansible剧本执行记录权限"),
            ("can_change_log_ansible_playbook", "更改Ansible剧本执行记录权限"),
            ("can_add_log_ansible_playbook", "添加Ansible剧本执行记录权限"),
            ("can_delete_log_ansible_playbook", "删除Ansible剧本执行记录权限"),
        )
        verbose_name = 'Ansible剧本操作记录表'  
        verbose_name_plural = 'Ansible剧本操作记录表' 

class Ansible_Playbook_Number(models.Model):
    playbook = models.ForeignKey('Ansible_Playbook',related_name='server_number', on_delete=models.CASCADE)
    playbook_server = models.CharField(max_length=100,verbose_name='目标服务器',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_ansible_playbook_number'
        permissions = (
            ("can_read_ansible_playbook_number", "读取Ansible剧本成员权限"),
            ("can_change_ansible_playbook_number", "更改Ansible剧本成员权限"),
            ("can_add_ansible_playbook_number", "添加Ansible剧本成员权限"),
            ("can_delete_ansible_playbook_number", "删除Ansible剧本成员权限"),             
        )
        verbose_name = 'Ansible剧本成员表'  
        verbose_name_plural = 'Ansible剧本成员表'
    def __unicode__(self):
        return '%s' % ( self.playbook_server)    
    
class Ansible_Inventory(models.Model):    
    name = models.CharField(max_length=200,unique=True,verbose_name='资产名称')
    desc = models.CharField(max_length=200,verbose_name='功能描述')
    user =  models.SmallIntegerField(verbose_name='创建人')
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='创建时间') 
    class Meta:
        db_table = 'opsmanage_ansible_inventory'
        permissions = (
            ("can_read_ansible_inventory", "读取Ansible资产权限"),
            ("can_change_ansible_inventory", "更改Ansible资产权限"),
            ("can_add_ansible_inventory", "添加Ansible资产权限"),
            ("can_delete_ansible_inventory", "删除Ansible资产权限"),             
        )
        verbose_name = 'Ansible资产表'  
        verbose_name_plural = 'Ansible资产表'

# class Log_Ansible_Inventory(models.Model): 
#     ans_user = models.CharField(max_length=50,verbose_name='使用用户',default=None)
#     ans_content = models.CharField(max_length=500,default=None)
#     create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='操作时间')
#     class Meta:
#         db_table = 'opsmanage_log_ansible_inventory'

class Ansible_Inventory_Groups(models.Model):    
    inventory = models.ForeignKey('Ansible_Inventory',related_name='inventory_group', on_delete=models.CASCADE)
    group_name =  models.CharField(max_length=100,verbose_name='group name')
    ext_vars = models.TextField(verbose_name='组外部变量',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_ansible_inventory_groups'
        verbose_name = 'Ansible资产成员表'  
        verbose_name_plural = 'Ansible资产成员表'
        unique_together = (("inventory", "group_name"))

class Ansible_Inventory_Groups_Server(models.Model):
    groups = models.ForeignKey('Ansible_Inventory_Groups',related_name='inventory_group_server', on_delete=models.CASCADE)
    server = models.SmallIntegerField(verbose_name='服务器')
    class Meta:
        db_table = 'opsmanage_ansible_inventory_groups_servers'
        unique_together = (("groups", "server"))
    
class Global_Config(models.Model):
    ansible_model = models.SmallIntegerField(verbose_name='是否开启ansible模块操作记录',blank=True,null=True)
    ansible_playbook = models.SmallIntegerField(verbose_name='是否开启ansible剧本操作记录',blank=True,null=True)
    cron = models.SmallIntegerField(verbose_name='是否开启计划任务操作记录',blank=True,null=True)
    project = models.SmallIntegerField(verbose_name='是否开启项目操作记录',blank=True,null=True)
    assets = models.SmallIntegerField(verbose_name='是否开启资产操作记录',blank=True,null=True)
    server = models.SmallIntegerField(verbose_name='是否开启服务器命令记录',blank=True,null=True)
    email = models.SmallIntegerField(verbose_name='是否开启邮件通知',blank=True,null=True)
    webssh = models.SmallIntegerField(verbose_name='是否开启WebSSH',blank=True,null=True)
    sql = models.SmallIntegerField(verbose_name='是否开启SQL更新通知',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_global_config'
    
class Email_Config(models.Model):
    site = models.CharField(max_length=100,verbose_name='部署站点')
    host = models.CharField(max_length=100,verbose_name='邮件发送服务器')
    port = models.SmallIntegerField(verbose_name='邮件发送服务器端口')
    user = models.CharField(max_length=100,verbose_name='发送用户账户')
    passwd = models.CharField(max_length=100,verbose_name='发送用户密码')
    subject = models.CharField(max_length=100,verbose_name='发送邮件主题标识',default=u'[OPS]')
    cc_user = models.TextField(verbose_name='抄送用户列表',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_email_config'
    
class Server_Command_Record(models.Model): 
    user = models.CharField(max_length=50,verbose_name='远程用户')
    server = models.CharField(max_length=50,verbose_name='服务器IP')
    client = models.CharField(max_length=50,verbose_name='客户机IP',blank=True,null=True)
    command = models.TextField(verbose_name='历史命令',blank=True,null=True)
    etime = models.CharField(max_length=50,verbose_name='命令执行时间',unique=True)
    class Meta:
        db_table = 'opsmanage_server_command_record'
        permissions = (
            ("can_read_server_command_record", "读取服务器操作日志权限"),
            ("can_change_server_command_record", "更改服务器操作日志权限"),
            ("can_add_server_command_record", "添加服务器操作日志权限"),
            ("can_delete_server_command_record", "删除服务器操作日志权限"),              
        )
        verbose_name = '服务器操作日志表'  
        verbose_name_plural = '服务器操作日志表' 
        
class Ansible_CallBack_Model_Result(models.Model):
    logId = models.ForeignKey('Log_Ansible_Model')
    content = models.TextField(verbose_name='输出内容',blank=True,null=True)
    
class Ansible_CallBack_PlayBook_Result(models.Model):
    logId = models.ForeignKey('Log_Ansible_Playbook')
    content = models.TextField(verbose_name='输出内容',blank=True,null=True)
    
class User_Server(models.Model):
    server_id = models.SmallIntegerField(verbose_name='服务器资产id')
    user_id = models.SmallIntegerField(verbose_name='用户id')
    class Meta:
        db_table = 'opsmanage_user_server'
        permissions = (
            ("can_read_user_server", "读取用户服务器表权限"),
            ("can_change_user_server", "更改用户服务器表权限"),
            ("can_add_user_server", "添加用户服务器表权限"),
            ("can_delete_user_server", "删除用户服务器表权限"),              
        )
        unique_together = (("server_id", "user_id"))
        verbose_name = '用户服务器表'  
        verbose_name_plural = '用户服务器表'
        
    

class Inception_Server_Config(models.Model):   
    db_name = models.CharField(max_length=100,verbose_name='数据库名',blank=True,null=True)
    db_host = models.CharField(max_length=100,verbose_name='数据库地址')
    db_user = models.CharField(max_length=100,verbose_name='用户',blank=True,null=True)
    db_passwd = models.CharField(max_length=100,verbose_name='密码',blank=True,null=True)
    db_backup_host = models.CharField(max_length=100,verbose_name='备份数据库地址')
    db_backup_user = models.CharField(max_length=100,verbose_name='备份数据库账户')
    db_backup_passwd = models.CharField(max_length=100,verbose_name='备份数据库密码')
    db_backup_port = models.SmallIntegerField(verbose_name='备份数据库端口')
    db_port = models.SmallIntegerField(verbose_name='端口')
    class Meta:
        db_table = 'opsmanage_inception_server_config'
        permissions = (
            ("can_read_inception_server_config", "读取inception信息表权限"),
            ("can_change_inception_server_config", "更改inception信息表权限"),
            ("can_add_inception_server_config", "添加inception信息表权限"),
            ("can_delete_inception_server_config", "删除inception信息表权限"),              
        )
        verbose_name = 'inception信息表'  
        verbose_name_plural = 'inception信息表'        

class DataBase_Server_Config(models.Model):
    env_type = (
                ('test',u'测试环境'),
                ('prod',u'生产环境'),
                )
    mode = (
            ('1',u'单例'),
            ('2',u'主从'),
            ('3',u'pxc'),
            )    
    db_env = models.CharField(choices=env_type,max_length=10,verbose_name='环境类型',default=None)
    db_type = models.CharField(max_length=10,verbose_name='数据库类型',default=None)
    db_name = models.CharField(max_length=100,verbose_name='数据库名',blank=True,null=True)
    db_host = models.CharField(max_length=100,verbose_name='数据库地址')
    db_mode = models.SmallIntegerField(choices=mode,verbose_name='架构类型',default=1)
    db_user = models.CharField(max_length=100,verbose_name='用户')
    db_passwd = models.CharField(max_length=100,verbose_name='密码')
    db_port = models.IntegerField(verbose_name='端口')
    db_group = models.SmallIntegerField(verbose_name='使用组')
    db_service = models.SmallIntegerField(verbose_name='业务类型')
    db_project = models.SmallIntegerField(verbose_name='所属项目')
    db_mark =  models.CharField(max_length=100,verbose_name='标识',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_database_server_config'
        permissions = (
            ("can_read_database_server_config", "读取数据库信息表权限"),
            ("can_change_database_server_config", "更改数据库信息表权限"),
            ("can_add_database_server_config", "添加数据库信息表权限"),
            ("can_delete_database_server_config", "删除数据库信息表权限"),              
        )
        unique_together = (("db_port", "db_host","db_env","db_name"))
        verbose_name = '数据库信息表'  
        verbose_name_plural = '数据库信息表'
  

    


class SQL_Execute_Histroy(models.Model):
    exe_user = models.CharField(max_length= 100,verbose_name='执行人')
    exe_db = models.ForeignKey('DataBase_Server_Config',verbose_name='数据库id')
    exe_sql =  models.TextField(verbose_name='执行的SQL内容') 
    exec_status = models.SmallIntegerField(blank=True,null=True,verbose_name='执行状态')
    exe_result = models.TextField(blank=True,null=True,verbose_name='执行结果') 
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')  
    class Meta:
        db_table = 'opsmanage_sql_execute_histroy'
        permissions = (
            ("can_read_sql_execute_histroy", "读取SQL执行历史表权限"),
            ("can_change_sql_execute_histroy", "更改SQL执行历史表权限"),
            ("can_add_sql_execute_histroy", "添加SQL执行历史表权限"),
            ("can_delete_sql_execute_histroy", "删除SQL执行历史表权限"),              
        )
        verbose_name = 'SQL执行历史记录表'  
        verbose_name_plural = 'SQL执行历史记录表'     
        
class Custom_High_Risk_SQL(models.Model):
    sql = models.CharField(max_length=200,unique=True,verbose_name='SQL内容') 
    class Meta:
        db_table = 'opsmanage_custom_high_risk_sql'
        permissions = (
            ("can_read_custom_high_risk_sql", "读取高危SQL表权限"),
            ("can_change_custom_high_risk_sql", "更改高危SQL表权限"),
            ("can_add_custom_high_risk_sql", "添加高危SQL表权限"),
            ("can_delete_custom_high_risk_sql", "删除高危SQL表权限"),              
        )
        verbose_name = '自定义高危SQL表'  
        verbose_name_plural = '自定义高危SQL表' 
        
        
class SQL_Audit_Control(models.Model):
    t_auto_audit = models.SmallIntegerField(blank=True,null=True,verbose_name='测试环境自动授权')
    t_backup_sql = models.SmallIntegerField(blank=True,null=True,verbose_name='测试环境自动备份SQL')
    t_email = models.SmallIntegerField(blank=True,null=True,verbose_name='测试环境开启邮件通知')
    p_auto_audit = models.SmallIntegerField(blank=True,null=True,verbose_name='正式环境自动授权')
    p_backup_sql = models.SmallIntegerField(blank=True,null=True,verbose_name='正式环境自动备份SQL')
    p_email = models.SmallIntegerField(blank=True,null=True,verbose_name='正式环境开启邮件通知')
    audit_group = models.CharField(max_length=100,blank=True,null=True,verbose_name='审核组')
    class Meta:
        db_table = 'opsmanage_sql_audit_control'
        permissions = (
            ("can_read_sql_audit_control", "读取SQL审核配置表权限"),
            ("can_change_sql_audit_control", "更改SQL审核配置表权限"),
            ("can_add_sql_audit_control", "添加SQL审核配置权限"),
            ("can_delete_sql_audit_control", "删除SQL审核配置权限"),              
        )
        verbose_name = 'SQL审核配置'  
        verbose_name_plural = 'SQL审核配置' 