import inspect
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
    
    def allowcator(self, sub, args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            return {}

mysql_service = MySQLMgrApi()