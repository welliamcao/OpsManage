import inspect, time
from . import mysql_base, mysql_pxc, mysql_status, mysql_variables, mysql_innodb_status, mysql_replication, mysql_innodb_trx
       
class MySQLMgrApi:
    def __init__(self):
        super(MySQLMgrApi,self).__init__() 
        
    
    def __get_module_classes(self, module):
        classes = []
        clsmembers = inspect.getmembers(module, inspect.isclass)
        for (name, cls) in clsmembers:
            classes.append(cls)
        return classes
    
    
    def status(self, dbServer):
        dataList = []
        for cls in self.__get_module_classes(mysql_status):
            if hasattr(cls,'key_name'):
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value() 
                data["metric"] = cls.metric
                data["desc"] = cls.__doc__
                data["level"] = cls.level
                dataList.append(data)
        return dataList
    
    def pxc(self, dbServer):
        dataList = []
        for cls in self.__get_module_classes(mysql_pxc):
            if hasattr(cls,'key_name'):
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value() 
                data["metric"] = cls.metric
                data["desc"] = cls.__doc__
                data["level"] = cls.level
                dataList.append(data)
        return dataList    

    def varibles(self, dbServer):
        dataList = []
        for cls in self.__get_module_classes(mysql_variables):
            if hasattr(cls,'key_name'):
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value() 
                data["desc"] = cls.__doc__
                dataList.append(data)
        return dataList 
    
    def innodb_status(self, dbServer):
        dataList = []
        for cls in self.__get_module_classes(mysql_innodb_status):
            if hasattr(cls,'key_name') and cls.key_name:
                data = {}
                data["name"] = cls.key_name
                data["value"] = cls(dbServer).get_value() 
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

mysql_service = MySQLMgrApi()