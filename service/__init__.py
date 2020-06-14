import inspect, time
from service.mysql import mysql_base, mysql_pxc, mysql_status, mysql_variables, mysql_innodb_status, mysql_replication, mysql_innodb_trx
from service.redis import redis_base, redis_memory, redis_commandstats, redis_status
       
class MySQLMgrApi:
    def __init__(self):
        super(MySQLMgrApi,self).__init__() 
        
    def __get_module_classes(self, module):
        classes = []
        clsmembers = inspect.getmembers(module, inspect.isclass)
        for (name, cls) in clsmembers:
            classes.append(cls)
        return classes
    
    def __format_to_json(self, data):
        format_data = dict()
        if data[0] > 0: 
            for i in data[1]:
                format_data[i[0].lower()] = i[1]
        return format_data
        
    def status(self, dbServer):
        dataList = []
        json_data = self.__format_to_json(mysql_base.MySQLBase(dbServer).execute("show global status"))
        for cls in self.__get_module_classes(mysql_status):
            if hasattr(cls,'key_name'):
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value(json_data) 
                data["metric"] = cls.metric
                data["desc"] = cls.__doc__
                data["level"] = cls.level
                dataList.append(data)
        return dataList
    
    def pxc(self, dbServer):
        dataList = []
        json_data = self.__format_to_json(mysql_base.MySQLBase(dbServer).execute("show global status"))
        for cls in self.__get_module_classes(mysql_pxc):
            if hasattr(cls,'key_name'):
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value(json_data) 
                data["metric"] = cls.metric
                data["desc"] = cls.__doc__
                data["level"] = cls.level
                dataList.append(data)
        return dataList    

    def varibles(self, dbServer):
        dataList = []
        json_data = self.__format_to_json(mysql_base.MySQLBase(dbServer).execute("show global variables"))
        for cls in self.__get_module_classes(mysql_variables):
            if hasattr(cls,'key_name'):
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value(json_data) 
                data["desc"] = cls.__doc__
                dataList.append(data)
        return dataList 
    
    def innodb_status(self, dbServer):
        dataList = []
        json_data = self.__format_to_json(mysql_base.MySQLBase(dbServer).execute("show global status"))
        for cls in self.__get_module_classes(mysql_innodb_status):
            if hasattr(cls,'key_name') and cls.key_name:
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value(json_data) 
                data["metric"] = cls.metric
                data["desc"] = cls.__doc__
                data["level"] = cls.level
                dataList.append(data)
        return dataList     

    def replication(self, dbServer):
        dataList = []
        for cls in self.__get_module_classes(mysql_replication):
            if hasattr(cls,'key_name'):
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value() 
                data["desc"] = cls.__doc__
                dataList.append(data)
        return dataList 
    
    def innodb_locked_trx(self, dbServer):
        return mysql_innodb_trx.MySQLInnodbTrx(dbServer).get_locked_trx()
 
    def innodb_block_trx(self, dbServer):
        return mysql_innodb_trx.MySQLInnodbTrx(dbServer).get_block_trx()         
    
    def processlist(self, dbServer):
        return mysql_base.MySQLBase(dbServer).get_processlists()
    
    def status_per(self, dbServer, second=1):            
        before_status = self.status(dbServer)
        time.sleep(second)
        current_status = self.status(dbServer)
        dataList = []
        for i in range(0, len(current_status)):
            current_value = current_status[i].get('value')
            if not isinstance(current_value, float):
                per_value = int(current_value) - int(before_status[i].get('value'))
                dataList.append({
                                    "name":current_status[i].get("name"),
                                    "value":per_value,
                                    "metric":current_status[i].get("metric"),
                                    "desc":current_status[i].get("desc"),
                                    "level":current_status[i].get("level"),                               
                                })
            else:
                dataList.append(current_status[i])
        return dataList   
    
    def allowcator(self, sub, args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            return {}

class RedisMgrApi:
    def __init__(self):
        super(RedisMgrApi,self).__init__() 
        
    
    def __get_module_classes(self, module):
        classes = []
        clsmembers = inspect.getmembers(module, inspect.isclass)
        for (name, cls) in clsmembers:
            classes.append(cls)
        return classes

    def allowcator(self, sub, args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            return {}
        
    def memory(self, dbServer):    
        dataList = []
        info_data = redis_base.RedisBase(dbServer).get_info(section='Memory')
        for cls in self.__get_module_classes(redis_memory):
            if hasattr(cls,'key_name') and cls.key_name:
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value(info_data) 
                data["metric"] = cls.metric
                data["desc"] = cls.__doc__
                data["level"] = cls.level
                dataList.append(data)
        return dataList     

    def cmd(self, dbServer):    
        dataList = []
        info_data = redis_base.RedisBase(dbServer).get_info(section='Commandstats')
        for cls in self.__get_module_classes(redis_commandstats):
            if hasattr(cls,'key_name') and cls.key_name:
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value(info_data)
                data["metric"] = cls.metric
                data["desc"] = cls.__doc__
                data["level"] = cls.level
                dataList.append(data)
        return dataList  

    def stats(self, dbServer):    
        dataList = []
        info_data = redis_base.RedisBase(dbServer).get_info(section='Stats')
        for cls in self.__get_module_classes(redis_status):
            if hasattr(cls,'key_name') and cls.key_name:
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value(info_data)
                data["metric"] = cls.metric
                data["desc"] = cls.__doc__
                data["level"] = cls.level
                dataList.append(data)
        return dataList     
          
    
mysql_service = MySQLMgrApi()
redis_service = RedisMgrApi()