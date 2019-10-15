#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.models import User
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey




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
    assets_type_dicts = {
        "printer": "打印机",
        "scanner": "扫描仪",
        "firewall": "防火墙",
        "route": "路由器",
        "wifi": "无线设备",
        "storage": "存储设备",
        "server": "服务器",
        "switch": "交换机",
        "vmser": "虚拟机"
    }
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
    status = models.SmallIntegerField(default=0,blank=True,null=True,verbose_name='状态')
    put_zone = models.SmallIntegerField(blank=True,null=True,verbose_name='放置区域')
    group = models.SmallIntegerField(blank=True,null=True,verbose_name='使用组')
#     business = models.SmallIntegerField(blank=True,null=True,verbose_name='业务类型')
    project = models.SmallIntegerField(blank=True,null=True,verbose_name='项目类型')
    host_vars = models.TextField(blank=True,null=True,verbose_name='ansible主机变量')
    mark = models.TextField(blank=True,null=True,verbose_name='资产标示')
    cabinet = models.SmallIntegerField(blank=True,null=True,verbose_name='机柜位置')
    business_tree = models.ManyToManyField('Business_Tree_Assets',blank=True)
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
        verbose_name = '资产管理'  
        verbose_name_plural = '总资产表'  
    
 
    def get_put_zone(self):
        try:
            return Idc_Assets.objects.get(id=self.put_zone).idc_name
        except:
            return '未知'        

    def get_buy_user(self):
        try:
            return User.objects.get(id=self.buy_user).username
        except:
            return '未知'  
                    
    def to_json(self):  
        if hasattr(self,'server_assets'):
            detail = self.server_assets.to_json()
        elif hasattr(self,'network_assets'):
            detail = self.network_assets.to_json() 
            
        json_format = {
           "id": self.id,
            "assets_type": self.assets_type_dicts[self.assets_type],
            "name": self.name,
            "sn": self.sn,
            "buy_time": self.buy_time,
            "expire_date": self.expire_date,
#             "business":[ ds.id for ds in self.business_tree.all() ],
            "buy_user": self.get_buy_user(),
            "management_ip": self.management_ip,
            "manufacturer": self.manufacturer,
            "provider": self.provider,
            "model": self.model,
            "status": self.status,
            "put_zone": self.get_put_zone(),
            "group": self.group,
            "host_vars": self.host_vars,
            "mark": self.mark,
            "cabinet": self.cabinet,
            "create_date": datetime.strftime(self.create_date, '%Y-%m-%d %H:%M:%S'),
            "update_date": datetime.strftime(self.update_date, '%Y-%m-%d %H:%M:%S'),
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
    keyfile_path = models.CharField(max_length=100,blank=True,null=True)
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
        verbose_name = '资产管理' 
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
        verbose_name = '资产管理' 
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
        verbose_name = '资产管理' 
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
        verbose_name = '资产管理'  
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
        verbose_name = '资产管理'  
        verbose_name_plural = '服务器网卡资产表'  
        unique_together = (("assets", "macaddress"))    
                    
class Business_Env_Assets(models.Model):
    '''业务环境资产表'''
    name = models.CharField(default="测试环境",max_length=100,unique=True) 
    class Meta:
        db_table = 'opsmanage_business_env_assets'
        default_permissions = ()
        verbose_name = '资产管理'  
        verbose_name_plural = '业务环境类型表'


class Business_Tree_Assets(MPTTModel):
    text = models.CharField(verbose_name='节点名称', max_length=100)
    env = models.SmallIntegerField(blank=True,null=True,verbose_name='项目环境')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, verbose_name='上级业务', null=True, blank=True,db_index=True ,related_name='children')
    manage = models.SmallIntegerField(blank=True,null=True,verbose_name='项目负责人')
    group = models.CharField(blank=True,null=True,max_length=100,verbose_name='所属部门')   
    desc = models.CharField(blank=True,null=True,max_length=200) 

    class Meta:
        db_table = 'opsmanage_business_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_business", "读取业务资产权限"),
            ("assets_change_business", "编辑业务资产权限"),
            ("assets_add_business", "添加业务资产权限"),
            ("assets_delete_business", "删除业务资产权限"),              
        )  
        verbose_name = '资产管理'  
        verbose_name_plural = '业务节点资产表' 

    def __unicode__(self):
        return self.text
               

    def business_env(self):
        try:
            env = Business_Env_Assets.objects.get(id=self.get_root().env).name
        except Exception as ex:
            env = "未知"        
        return env
    
    def node_path(self):
        self.paths = ''
        if not self.parent:
            self.paths = self.text
        else:
            dataList = Business_Tree_Assets.objects.raw("""SELECT id,text as path FROM opsmanage_business_assets WHERE tree_id = {tree_id} AND  lft < {lft} AND  rght > {rght} ORDER BY lft DESC;""".format(tree_id=self.tree_id,lft=self.lft,rght=self.rght))
            for ds in dataList:
                self.paths = ds.path + '/' + self.paths
            self.paths = self.paths  + self.text
        return  self.paths
    
    def last_node(self):
        if self.is_leaf_node():
            return 1
        else:
            return 0
    
    def icon(self):
        icon =  "fa fa-tree"  
        if self.parent: 
            icon = "fa fa-plus-square" 
        if self.is_leaf_node():
            return 'fa fa-minus-square-o' 
        return icon           

    def to_json(self):
        if self.parent: 
            parentId = self.parent.id
        else:
            parentId = 0      
        json_format = {
            "id":self.id,
            "text":self.text,
            "icon":self.icon(),
            "level":self.level,
            "manage":self.manage,
            "group":self.group,
            "desc":self.desc,
            "tree_id":self.tree_id,
            "lft":self.lft,
            "rght":self.rght,
            "paths":self.node_path(),
            "last_node":self.last_node(),
            "parentId": parentId,                  
        }
        return json_format        
        
class Zone_Assets(models.Model):  
    zone_name = models.CharField(max_length=100,unique=True) 
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_zone_assets'
        default_permissions = ()
        permissions = (
            ("assets_read_zone", "读取区域机房权限"),
            ("assets_change_zone", "更改区域机房权限"),
            ("assets_add_zone", "添加区域机房权限"),
            ("assets_delete_zone", "删除区域机房权限"),             
        )  
        verbose_name = '资产管理'  
        verbose_name_plural = '区域资产表'     

class Idc_Assets(models.Model):
    zone = models.ForeignKey('Zone_Assets',related_name='idc_assets',on_delete=models.CASCADE)
    idc_name = models.CharField(max_length=32, verbose_name=u'机房名称')
    idc_bandwidth = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name=u'机房带宽')
    idc_linkman = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name=u'联系人')
    idc_phone = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name=u'联系电话')
    idc_address = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name=u"机房地址")
    idc_network = models.TextField(blank=True, null=True, default='', verbose_name=u"IP地址段")
    update_time = models.DateField(auto_now=True, null=True)
    idc_operator = models.CharField(max_length=32, blank=True, default='', null=True, verbose_name=u"运营商")
    idc_desc = models.CharField(max_length=128, blank=True, default='', null=True, verbose_name=u"备注")
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_idc_assets'
        default_permissions = ()
        verbose_name = '资产管理'  
        verbose_name_plural = '机房资产表'         
        
class Cabinet_Assets(models.Model):  
    idc = models.ForeignKey('Idc_Assets',related_name='cabinet_assets', on_delete=models.CASCADE)
    cabinet_name = models.CharField(max_length=100,blank=True,null=True,verbose_name='机柜名称')
    '''自定义权限'''
    class Meta:
        unique_together = (("idc", "cabinet_name"))
        default_permissions = ()
        db_table = 'opsmanage_cabinet_assets'
        verbose_name = '资产管理' 
        verbose_name_plural = '机柜资产表'              

class Idle_Assets(models.Model):  
    idc = models.ForeignKey('Idc_Assets',related_name='idle_assets', on_delete=models.CASCADE)
    idle_name = models.CharField(max_length=100,verbose_name='名称')
    idle_number = models.SmallIntegerField(verbose_name='剩余个数')
    idle_user = models.SmallIntegerField(verbose_name='记录人员')
    idle_desc = models.CharField(max_length=128, blank=True, default='', null=True, verbose_name=u"备注")
    update_time = models.DateTimeField(auto_now=True,blank=True,null=True,verbose_name='修改时间') 
    '''自定义权限'''
    class Meta:
        unique_together = (("idc", "idle_name"))
        default_permissions = ()
        db_table = 'opsmanage_idle_assets'
        verbose_name = '资产管理' 
        verbose_name_plural = '闲置资产表'    
    
    def get_username(self):
        try:
            return User.objects.get(id=self.idle_user).username
        except:
            return "未知"
                
class Line_Assets(models.Model):   
    line_name = models.CharField(max_length=100,unique=True)  
    line_price = models.CharField(max_length=20,blank=True, default='', null=True,verbose_name=u"价格")   
    update_time = models.DateTimeField(auto_now=True,blank=True,null=True,verbose_name='修改时间') 
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
        verbose_name = '资产管理'  
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
        verbose_name = '资产管理'  
        verbose_name_plural = 'Raid资产表' 
  
        
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
            ("assets_read_tree", "读取资产树权限"),            
        )        
        verbose_name = '资产管理' 
        verbose_name_plural = '资产标签表' 
        
class Tags_Server_Assets(models.Model): 
    aid = models.ForeignKey('Assets',related_name='assets', on_delete=models.CASCADE)
    tid = models.ForeignKey('Tags_Assets',related_name='tag_assets', on_delete=models.CASCADE)
    class Meta:
        unique_together = (("aid", "tid"))
        db_table = 'opsmanage_tags_server'
        default_permissions = ()
        verbose_name = '资产管理'  
        verbose_name_plural = '资产标签对应表'     
        
        
class User_Server(models.Model):
    assets = models.ForeignKey('Assets',related_name='user_assets', on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='用户', on_delete=models.CASCADE)
    class Meta:
        db_table = 'opsmanage_user_assets'
        default_permissions = ()   
        unique_together = (("assets", "user"))
        verbose_name = '资产管理'  
        verbose_name_plural = '用户资产表'                         