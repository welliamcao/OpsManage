# -*- coding=utf-8 -*-
'''
应用基类（每次应用启动时，都必须调用基类的初始化方法）
@author: welliam.cao<303350019@qq.com> 
@version:1.0 2017年4月12日
'''
import redis, os
from redis.exceptions import  ConnectionError, RedisError
from django.conf import settings
from django.db import connection
from collections import namedtuple
from datetime import datetime,date
from libs.secret.aescipher import AESCipher
from django.db import models
from mptt.templatetags.mptt_tags import cache_tree_children
from django.db.models import Count

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class DataHandle(object):
    def __init__(self):
        super(DataHandle,self).__init__()  
            
    def saveScript(self,content,filePath):
        if os.path.isdir(os.path.dirname(filePath)) is not True:os.makedirs(os.path.dirname(filePath))#判断文件存放的目录是否存在，不存在就创建
        with open(filePath, 'w') as f:
            f.write(content) 
        return filePath    
    
    def change(self,args):
        try:
            return int(args)
        except:
            return  0

    def convert_to_dict(self,model):      
        for fieldName in model._meta.get_fields():
            try:
                fieldValue = getattr(model,fieldName.name)
                if type(fieldValue) is date or type(fieldValue) is datetime:
                    fieldValue = datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                setattr(model, fieldName.name, fieldValue)    
            except Exception as ex:
                pass
        data = {}
        data.update(model.__dict__)
        data.pop("_state", None)
        data.pop("script_file",None)
        data.pop("cron_script",None)
        data.pop("_cron_server_cache",None)
        data.pop("playbook_file",None)
        data.pop('_assets_cache',None)
        data.pop('sudo_passwd',None)
        data.pop('passwd',None)  
        data.pop('codename',None)  
        data.pop('content_type_id',None)  
        data.pop('_project_cache',None)
        data.pop('_network_assets_cache',None)
        data.pop('_server_assets_cache',None)            
        return data
    
    def convert_to_dicts(self,models):
        obj_arr = []        
        for obj in models:
            for fieldName in obj._meta.get_fields():
                try:
                    fieldValue = getattr(obj,fieldName.name)
                    if type(fieldValue) is date or type(fieldValue) is datetime:
                        fieldValue = datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                    setattr(obj, fieldName.name, fieldValue)    
                except Exception as ex:
                    pass
            data = {}
            data.update(obj.__dict__)
            data.pop("_state", None)
            data.pop("script_file",None)
            obj_arr.append(dict)
        return obj_arr    

class DjangoCustomCursors(object):
    def __init__(self):
        super(DjangoCustomCursors, self).__init__()
        self.cursor = connection.cursor()
        
        
    def dictfetchall(self):
        columns = [col[0] for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]
    
    def namedtuplefetchall(self):
        desc = self.cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in self.cursor.fetchall()]
            
    def execute(self,sql):   
        self.cursor.execute(sql)  
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()           

class APBase(object):
    REDSI_POOL = 10000
    @staticmethod
    def getRedisConnection(db):
        '''根据数据源标识获取Redis连接池'''
        if db==APBase.REDSI_POOL:
            args = settings.REDSI_KWARGS_LPUSH
            if settings.REDSI_LPUSH_POOL == None:
                settings.REDSI_LPUSH_POOL = redis.ConnectionPool(host=args.get('host'), port=args.get('port'), db=args.get('db'),password=args.get('password'))
            pools = settings.REDSI_LPUSH_POOL  
        connection = redis.Redis(connection_pool=pools)
        return connection

   


class AESCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        if 'prefix' in kwargs:
            self.prefix = kwargs['prefix']
            del kwargs['prefix']
        else:
            self.prefix = "aes:::"
        self.cipher = AESCipher(settings.SECRET_KEY)
        super(AESCharField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(AESCharField, self).deconstruct()
        if self.prefix != "aes:::":
            kwargs['prefix'] = self.prefix
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        if value.startswith(self.prefix):
            value = value[len(self.prefix):]
            value = self.cipher.decrypt(value)
        return value

    def to_python(self, value):
        if value is None:
            return value
        elif value.startswith(self.prefix):
            value = value[len(self.prefix):]
            value = self.cipher.decrypt(value)
        return value

    def get_prep_value(self, value):
        if isinstance(value, str) or isinstance(value, bytes):
            value = self.cipher.encrypt(value)
            value = self.prefix + value.decode('utf-8')
        elif value is not None:
            raise TypeError(str(value) + " is not a valid value for AESCharField")
        return value

class AppsTree:
    def __init__(self,business_tree, apps, apps_user=None, apps_db=None, request=None):
        self.business_tree = business_tree
        self.apps = apps
        self.apps_user = apps_user
        self.apps_db = apps_db
        self.request = request
        
    def _query_user_db_server(self):
        if self.request.user.is_superuser:
            dbList = self.apps.objects.all()      
        else: 
            user_db_list = [ ud.db for ud in self.apps_user.objects.filter(user=self.request.user.id) ]

            dbLists = [ ds.db_server for ds in self.apps_db.objects.filter(id__in=user_db_list) ]

            dbList = list(dict.fromkeys(dbLists)) #去除重复
            
        return dbList

    def _recursive_node_to_dict(self, node, request, user_db_server_list):
        json_format = node.to_json()
        children = [self._recursive_node_to_dict(c, request, user_db_server_list) for c in node.get_children()]
        if children:
            json_format['children'] = children
        else:
            json_format['icon'] = 'fa fa-minus-square-o'
        
        #获取业务树下面的数据库服务器    
        if json_format["last_node"] == 1: 
            db_children = []    
            for ds in self.apps.objects.filter(id__in=user_db_server_list, db_business=json_format["id"], db_rw__in=self.request.query_params.getlist('db_rw')):  
                data = ds.to_tree()
                data["user_id"] = self.request.user.id
                db_children.append(data)
            json_format['children'] = db_children
            json_format["icon"] = "fa fa-plus-square"
            json_format["last_node"] = 0
            
        return json_format

    def recursive_node_to_dict(self,node):
        json_format = node.to_json()
        children = [self.recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            json_format['children'] = children
        else:
            json_format['icon'] = 'fa fa-minus-square-o'        
        return json_format
    
    def _business_paths_id_list(self,business):
        tree_list = []
        
        dataList = self.business_tree.objects.raw("""SELECT id FROM opsmanage_business_assets WHERE tree_id = {tree_id} AND  lft < {lft} AND  rght > {rght} ORDER BY lft ASC;""".format(tree_id=business.tree_id,lft=business.lft,rght=business.rght))
        
        for ds in dataList:
            tree_list.append(ds.id)
            
        tree_list.append(business.id)
        
        return tree_list
       
    def db_tree(self):
        
        user_db_server_list =  [ ds.id for ds in self._query_user_db_server() ] 
        
        if self.request.user.is_superuser:
            user_business = [ ds.get("db_business") for ds in self.apps.objects.values('db_business').annotate(dcount=Count('db_business')) ] 
                     
        else:    
            user_business = [ ds.get("db_business") for ds in self.apps.objects.filter(id__in=user_db_server_list).values('db_business').annotate(dcount=Count('db_business')) ]

        business_list = []

        for business in self.business_tree.objects.filter(id__in=user_business):
            
            business_list += self._business_paths_id_list(business)
            
        business_list = list(set(business_list))
        
        business_node = self.business_tree.objects.filter(id__in=business_list)
        
        root_nodes = cache_tree_children(business_node)
        
        dataList = []
        
        for n in root_nodes:
            
            dataList.append(self._recursive_node_to_dict(n, self.request, user_db_server_list))   
                  
        return dataList    
    
    def tree_business(self,business):
        dataList = []
        for ds in self.apps.objects.filter(business=business):
            dataList.append(ds.to_json())
        return dataList
    
    def apply_tree(self):
        apply_business = [ ds.get("business") for ds in self.apps.objects.values('business').annotate(dcount=Count('business')) ]
        
        business_list = []
        
        for business in self.business_tree.objects.filter(id__in=apply_business):
            business_list += self._business_paths_id_list(business)
            
        business_list = list(set(business_list))
        
        business_node = self.business_tree.objects.filter(id__in=business_list)
        
        root_nodes = cache_tree_children(business_node)
        
        dataList = []
        for n in root_nodes:
            dataList.append(self.recursive_node_to_dict(n))         
        return dataList      
          
            
if __name__=='__main__':   
    pass