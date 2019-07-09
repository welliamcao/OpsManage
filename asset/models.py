#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.models import User
from datetime import datetime

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
    mark = models.TextField(blank=True,null=True,verbose_name='资产标示')
    cabinet = models.SmallIntegerField(blank=True,null=True,verbose_name='机柜位置')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'opsmanage_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_assets", "读取资产权限"),
            ("assets_change_assets", "更改资产权限"),
            ("assets_add_assets", "添加资产权限"),
            ("assets_delete_assets", "删除资产权限"),
            ("assets_dumps_assets", "导出资产权限"),
        ) 
        verbose_name = '总资产表'  
        verbose_name_plural = '总资产表'  
    
    def get_put_zone(self):
        try:
            return Zone_Assets.objects.get(id=self.put_zone).zone_name
        except:
            return '未知'        

    def get_buy_user(self):
        try:
            return User.objects.get(id=self.buy_user).username
        except:
            return '未知'  
    
    def get_project(self):
        try:
            return Project_Assets.objects.get(id=self.project).project_name
        except:
            return '未知'         
    
    def get_service(self):
        try:
            return Service_Assets.objects.get(id=self.business).service_name
        except:
            return '未知'         
        
    def to_json(self):  
        if hasattr(self,'server_assets'):
            detail = self.server_assets.to_json()
        elif hasattr(self,'network_assets'):
            detail = self.network_assets.to_json() 
            
        json_format = {
           "id": self.id,
            "assets_type": self.assets_type,
            "name": self.name,
            "sn": self.sn,
            "buy_time": self.buy_time,
            "expire_date": self.expire_date,
            "buy_user": self.get_buy_user(),
            "management_ip": self.management_ip,
            "manufacturer": self.manufacturer,
            "provider": self.provider,
            "model": self.model,
            "status": self.status,
            "put_zone": self.get_put_zone(),
            "group": self.group,
            "project": self.get_project(),
            "host_vars": self.host_vars,
            "mark": self.mark,
            "cabinet": self.cabinet,
            "create_date": datetime.strftime(self.create_date, '%Y-%m-%d %H:%M:%S'),
            "update_date": datetime.strftime(self.update_date, '%Y-%m-%d %H:%M:%S'),
            "service": self.get_service(),
            "detail":detail,
        }
        return  json_format

class Server_Assets(models.Model): 
    assets = models.OneToOneField('Assets', on_delete=models.CASCADE) 
    ip = models.CharField(max_length=100,unique=True,blank=True,null=True) 
    hostname = models.CharField(max_length=100,blank=True,null=True)  
    username = models.CharField(max_length=100,blank=True,null=True)  
    passwd = models.CharField(max_length=100,default='root',blank=True,null=True)  
    sudo_passwd = models.CharField(max_length=100,blank=True,null=True)
    keyfile =  models.SmallIntegerField(blank=True,null=True)#FileField(upload_to = './upload/key/',blank=True,null=True,verbose_name='密钥文件')
    port = models.DecimalField(max_digits=6,decimal_places=0,default=22)
    line = models.SmallIntegerField(blank=True,null=True)
    cpu = models.CharField(max_length=100,blank=True,null=True)
    cpu_number = models.SmallIntegerField(blank=True,null=True)
    vcpu_number = models.SmallIntegerField(blank=True,null=True)
    cpu_core = models.SmallIntegerField(blank=True,null=True)
    disk_total = models.IntegerField(blank=True,null=True)
    ram_total= models.IntegerField(blank=True,null=True)
    kernel = models.CharField(max_length=100,blank=True,null=True)
    selinux = models.CharField(max_length=100,blank=True,null=True)
    swap = models.CharField(max_length=100,blank=True,null=True)
    raid = models.SmallIntegerField(blank=True,null=True)
    system = models.CharField(max_length=100,blank=True,null=True)
#     mount = models.TextField(blank=True,null=True,verbose_name='分区情况')
    create_date = models.DateTimeField(default = timezone.now)
    update_date = models.DateTimeField(auto_now_add=True)
    '''自定义添加只读权限-系统自带了add change delete三种权限'''
    class Meta:
        db_table = 'opsmanage_server_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_server", "读取服务器资产权限"),
            ("assets_change_server", "更改服务器资产权限"),
            ("assets_add_server", "添加服务器资产权限"),
            ("assets_delete_server", "删除服务器资产权限"),   
            ("assets_webssh_server", "登陆服务器资产权限"),         
        )
        verbose_name = '服务器资产表'  
        verbose_name_plural = '服务器资产表' 
    
    def get_line(self):
        try:
            return Line_Assets.objects.get(id=self.line).line_name
        except:
            return '未知'        

    def get_raid(self):
        try:
            return Raid_Assets.objects.get(id=self.raid).raid_name
        except:
            return '未知' 
        
    def to_json(self):
        json_format = {
            "id": self.id,
            "assets_id": self.assets.id,
            "ip": self.ip,
            "hostname": self.hostname,
            "username": self.username,
            "keyfile": self.keyfile,
            "line": self.get_line(),
            "cpu": self.cpu,
            "cpu_number": self.cpu_number,
            "vcpu_number": self.vcpu_number,
            "cpu_core":self.cpu_core,
            "disk_total": self.disk_total,
            "ram_total": self.ram_total,
            "kernel": self.kernel,
            "selinux": self.selinux,
            "swap": self.swap,
            "raid": self.get_raid(),
            "system": self.system,
            "create_date": datetime.strftime(self.create_date, '%Y-%m-%d %H:%M:%S'),
            "update_date": datetime.strftime(self.update_date, '%Y-%m-%d %H:%M:%S')
        }
        return  json_format

class Network_Assets(models.Model):
    assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
    bandwidth =  models.CharField(max_length=100,blank=True,null=True,verbose_name='背板带宽') 
    ip = models.CharField(unique=True,max_length=100,blank=True,null=True,verbose_name='管理ip')
    username = models.CharField(max_length=100,blank=True,null=True)
    passwd = models.CharField(max_length=100,blank=True,null=True) 
    sudo_passwd = models.CharField(max_length=100,blank=True,null=True) 
    port = models.DecimalField(max_digits=6,decimal_places=0,default=22)    
    port_number = models.SmallIntegerField(blank=True,null=True,verbose_name='端口个数')
    firmware =  models.CharField(max_length=100,blank=True,null=True,verbose_name='固件版本')
    cpu = models.CharField(max_length=100,blank=True,null=True,verbose_name='cpu型号')
    stone = models.CharField(max_length=100,blank=True,null=True,verbose_name='内存大小')
    configure_detail = models.TextField(max_length=100,blank=True,null=True,verbose_name='配置说明')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)    
    class Meta:
        db_table = 'opsmanage_network_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_network", "读取网络资产权限"),
            ("assets_change_network", "更改网络资产权限"),
            ("assets_add_network", "添加网络资产权限"),
            ("assets_delete_network", "删除网络资产权限"), 
        ) 
        verbose_name = '网络资产表'  
        verbose_name_plural = '网络资产表' 

    def to_json(self):
        json_format = {
            "id": self.id,
            "assets_id": self.assets.id,
            "bandwidth": self.bandwidth,
            "ip": self.ip,            
            "username": self.username,
            "port": self.port,
            "port_number": self.port_number,
            "firmware": self.firmware,
            "cpu": self.cpu,
            "stone": self.stone,
            "configure_detail":self.configure_detail,
            "create_date": datetime.strftime(self.create_date, '%Y-%m-%d %H:%M:%S'),
            "update_date": datetime.strftime(self.update_date, '%Y-%m-%d %H:%M:%S'),
        }
        return  json_format
    
class Disk_Assets(models.Model):      
    assets = models.ForeignKey('Assets', on_delete=models.CASCADE)
    device_volume =  models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘容量') 
    device_status =  models.SmallIntegerField(blank=True,null=True,verbose_name='硬盘状态')
    device_model = models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘型号')
    device_brand = models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘生产商')
    device_serial =  models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘序列号')
    device_slot = models.SmallIntegerField(blank=True,null=True,verbose_name='硬盘插槽')
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now_add=True)   
    class Meta:
        db_table = 'opsmanage_disk_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_disk", "读取磁盘资产权限"),
            ("assets_change_disk", "更改磁盘资产权限"),
            ("assets_add_disk", "添加磁盘资产权限"),
            ("assets_delete_disk", "删除磁盘资产权限"),             
        ) 
        unique_together = (("assets", "device_slot"))
        verbose_name = '磁盘资产表'  
        verbose_name_plural = '磁盘资产表'  

class Ram_Assets(models.Model):   
    assets = models.ForeignKey('Assets', on_delete=models.CASCADE)
    device_model = models.CharField(max_length=100,blank=True,null=True,verbose_name='内存型号')
    device_volume =  models.CharField(max_length=100,blank=True,null=True,verbose_name='内存容量')  
    device_brand = models.CharField(max_length=100,blank=True,null=True,verbose_name='内存生产商')
    device_slot = models.SmallIntegerField(blank=True,null=True,verbose_name='内存插槽')
    device_status = models.SmallIntegerField(blank=True,null=True,verbose_name='内存状态')
    create_date = models.DateTimeField(default = timezone.now)
    update_date = models.DateTimeField(auto_now_add=True)    
    class Meta:
        db_table = 'opsmanage_ram_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_ram", "读取内存资产权限"),
            ("assets_change_ram", "更改内存资产权限"),
            ("assets_add_ram", "添加内存资产权限"),
            ("assets_delete_ram", "删除内存资产权限"),             
        ) 
        unique_together = (("assets", "device_slot"))
        verbose_name = '内存资产表'  
        verbose_name_plural = '内存资产表'         
        
class NetworkCard_Assets(models.Model):   
    assets = models.ForeignKey('Assets', on_delete=models.CASCADE)
    device =  models.CharField(max_length=20,blank=True,null=True)
    macaddress = models.CharField(u'MAC',max_length=64,blank=True,null=True)
    ip = models.GenericIPAddressField(u'IP', blank=True,null=True)
    module = models.CharField(max_length=50,blank=True,null=True)
    mtu = models.CharField(max_length=50,blank=True,null=True)
    active = models.SmallIntegerField(blank=True,null=True,verbose_name='是否在线')
    class Meta:
        db_table = 'opsmanage_networkcard_assets'
        default_permissions = ()
        verbose_name = '服务器网卡资产表'  
        verbose_name_plural = '服务器网卡资产表'  
        unique_together = (("assets", "macaddress"))    
                    
        
class Project_Assets(models.Model):
    '''产品线资产表'''
    project_name = models.CharField(max_length=100,unique=True) 
    project_owner = models.SmallIntegerField(blank=True,null=True,verbose_name='项目负责人')
    class Meta:
        db_table = 'opsmanage_project_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_project", "读取产品线权限"),
            ("assets_change_project", "更改产品线权限"),
            ("assets_add_project", "添加产品线权限"),
            ("assets_delete_project", "删除产品线权限"),              
        )  
        verbose_name = '项目资产表'  
        verbose_name_plural = '项目资产表' 
              
    
class Service_Assets(models.Model):
    '''业务分组表'''
    project = models.ForeignKey('Project_Assets',related_name='service_assets', on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100) 
    
    class Meta:
        db_table = 'opsmanage_service_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_service", "读取业务资产权限"),
            ("assets_change_service", "更改业务资产权限"),
            ("assets_add_service", "添加业务资产权限"),
            ("assets_delete_service", "删除业务资产权限"),              
        )  
        unique_together = (("project", "service_name"))
        verbose_name = '业务分组表'  
        verbose_name_plural = '业务分组表'  
        
        
class Zone_Assets(models.Model):  
    zone_name = models.CharField(max_length=100,unique=True) 
    zone_contact = models.CharField(max_length=100,blank=True,null=True,verbose_name='机房联系人')
    zone_number = models.CharField(max_length=100,blank=True,null=True,verbose_name='联系人号码')
    zone_local = models.CharField(max_length=200,blank=True,null=True,verbose_name='机房地理位置')
    zone_network = models.CharField(max_length=100,blank=True,null=True,verbose_name='机房网段')
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_zone_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_zone", "读取机房资产权限"),
            ("assets_change_zone", "更改机房资产权限"),
            ("assets_add_zone", "添加机房资产权限"),
            ("assets_delete_zone", "删除机房资产权限"),             
        )  
        verbose_name = '机房资产表'  
        verbose_name_plural = '机房资产表'     
        
class Cabinet_Assets(models.Model):  
    zone = models.ForeignKey('Zone_Assets',related_name='cabinet_assets', on_delete=models.CASCADE)
    cabinet_name = models.CharField(max_length=100,blank=True,null=True,verbose_name='机柜名称')
    '''自定义权限'''
    class Meta:
        unique_together = (("zone", "cabinet_name"))
        default_permissions = ()
        db_table = 'opsmanage_cabinet_assets'
        verbose_name = '机柜资产表'  
        verbose_name_plural = '机柜资产表'              
                
class Line_Assets(models.Model):   
    line_name = models.CharField(max_length=100,unique=True)     
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_line_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_line", "读取出口线路资产权限"),
            ("assets_change_line", "更改出口线路资产权限"),
            ("assets_add_line", "添加出口线路资产权限"),
            ("assets_delete_line", "删除出口线路资产权限"),             
        )
        verbose_name = '出口线路资产表'  
        verbose_name_plural = '出口线路资产表' 
        
class Raid_Assets(models.Model):   
    raid_name = models.CharField(max_length=100,unique=True)    
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_raid_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_raid", "读取Raid资产权限"),
            ("assets_change_raid", "更改Raid资产权限"),
            ("assets_add_raid", "添加Raid资产权限"),
            ("assets_delete_raid", "删除Raid资产权限"),             
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
        default_permissions = ()
        verbose_name = '项目配置操作记录表'  
        verbose_name_plural = '项目配置操作记录表'      
        
class Tags_Assets(models.Model): 
    tags_name = models.CharField(unique=True,max_length=100,verbose_name='名称',default=None)
    class Meta:
        db_table = 'opsmanage_tags_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_tags", "读取标签资产权限"),
            ("assets_change_tags", "更改标签资产权限"),
            ("assets_add_tags", "添加标签资产权限"),
            ("assets_delete_tags", "删除标签资产权限"),  
            ("assets_read_tree", "读取资产数权限"),            
        )        
        verbose_name = '资产标签表'  
        verbose_name_plural = '资产标签表' 
        
class Tags_Server_Assets(models.Model): 
    aid = models.ForeignKey('Assets',related_name='assets', on_delete=models.CASCADE)
    tid = models.ForeignKey('Tags_Assets',related_name='tag_assets', on_delete=models.CASCADE)
    class Meta:
        unique_together = (("aid", "tid"))
        db_table = 'opsmanage_tags_server'
        default_permissions = ()
        verbose_name = '资产标签对应表'  
        verbose_name_plural = '资产标签对应表'     
        
        
class User_Server(models.Model):
    assets = models.ForeignKey('Assets',related_name='user_assets', on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='用户', on_delete=models.CASCADE)
    class Meta:
        db_table = 'opsmanage_user_assets'
        default_permissions = ()
        permissions = (
            ("assets_add_user", "添加用户权限"),
            ("assets_change_user", "修改用户权限"),
            ("assets_delete_user", "删除用户权限"),  
            ("assets_read_user", "读取用户权限"),            
        )         
        unique_together = (("assets", "user"))
        verbose_name = '用户资产表'  
        verbose_name_plural = '用户资产表'                           