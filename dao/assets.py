#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import ast
from OpsManage.models import Assets,Server_Assets,Network_Assets,Ansible_Inventory,Project_Assets,Service_Assets
from OpsManage.utils.logger import logger

class AssetsSource(object):
    def __init__(self):
        super(AssetsSource,self).__init__()
    
    def serverList(self):
        serverList = []
        for assets in Assets.objects.filter(assets_type__in=["server","vmser","switch","route"]):
            try:
                service =  Service_Assets.objects.get(id=assets.business).service_name
            except:
                service = '未知'
            try:
                project =  Project_Assets.objects.get(id=assets.project).project_name
            except:
                project = '未知'                
            if hasattr(assets,'server_assets'):
                serverList.append({"id":assets.id,"ip":assets.server_assets.ip,'project':project,'service':service})
            elif hasattr(assets,'network_assets'):
                serverList.append({"id":assets.id,"ip":assets.network_assets.ip,'project':project,'service':service})
        return  serverList   
    
    def queryAssetsByIp(self,ipList):
        sList = []
        resource = []          
        for ip in ipList:
            data = {}
            server = Server_Assets.objects.filter(ip=ip).count()
            network = Network_Assets.objects.filter(ip=ip).count()
            if server > 0:
                try:
                    server_assets = Server_Assets.objects.get(ip=ip)
                    sList.append(server_assets.ip)
                    data["ip"] = server_assets.ip
                    data["port"] = int(server_assets.port)
                    data["username"] = server_assets.username
                    data["sudo_passwd"] = server_assets.sudo_passwd
                    if server_assets.keyfile != 1:data["password"] =  server_assets.passwd                   
                except Exception, ex:
                    logger.warn(msg="server_id:{assets}, error:{ex}".format(assets=server_assets.id,ex=ex))
                if server_assets.assets.host_vars:
                    try:                         
                        for k,v in ast.literal_eval(server_assets.assets.host_vars).items():
                            if k not in ["ip", "port", "username", "password","ip"]:data[k] = v 
                    except Exception,ex:
                        logger.warn(msg="资产: {assets},转换host_vars失败:{ex}".format(assets=server_assets.assets.id,ex=ex))                                                
            elif network > 0:
                try:    
                    network_assets = Network_Assets.objects.get(ip=ip)
                    sList.append(network_assets.ip)
                    data["ip"] = network_assets.ip
                    data["port"] = int(network_assets.port)
                    data["password"] = network_assets.passwd,
                    data["username"] = network_assets.username
                    data["sudo_passwd"] = network_assets.sudo_passwd
                    data["connection"] = 'local'
                except Exception, ex:
                    logger.warn(msg="network_id:{assets}, error:{ex}".format(assets=server_assets.id,ex=ex))  
                if network_assets.assets.host_vars:
                    try:                         
                        for k,v in ast.literal_eval(network_assets.assets.host_vars).items():
                            if k not in ["ip", "port", "username", "password","ip"]:data[k] = v 
                    except Exception,ex:
                        logger.warn(msg="资产: {assets},转换host_vars失败:{ex}".format(assets=network_assets.assets.id,ex=ex))              
            resource.append(data)
        return  sList, resource           
        
    def custom(self,serverList):
        assetsList = []
        for server in serverList:
            try:
                assetsList.append(Assets.objects.select_related().get(id=server))
            except:
                pass
        return self.source(assetsList)
    
    def group(self,group):
        assetsList = Assets.objects.select_related().filter(group=group,assets_type__in=["server","vmser","switch","route"])
        return self.source(assetsList)
                
    def service(self,business):
        assetsList = Assets.objects.select_related().filter(business=business,assets_type__in=["server","vmser","switch","route"])
        return self.source(assetsList)
                
    def source(self,assetsList):    
        sList = []
        resource = []                            
        for assets in assetsList:
            data = {}
            if hasattr(assets,'server_assets'):
                try:
                    sList.append(assets.server_assets.ip)
                    data["ip"] = assets.server_assets.ip
                    data["port"] = int(assets.server_assets.port)
                    data["username"] = assets.server_assets.username
                    data["sudo_passwd"] = assets.server_assets.sudo_passwd
                    if assets.server_assets.keyfile == 0:data["password"] =  assets.server_assets.passwd                         
                except Exception, ex:
                    logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id,ex=ex))                    
            elif hasattr(assets,'network_assets'):
                try:
                    sList.append(assets.network_assets.ip)
                    data["ip"] = assets.network_assets.ip
                    data["port"] = int(assets.network_assets.port)
                    data["password"] = assets.network_assets.passwd,
                    data["username"] = assets.network_assets.username
                    data["sudo_passwd"] = assets.network_assets.sudo_passwd
                    data["connection"] = 'local'
                except Exception, ex:
                    logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id,ex=ex))   
            if assets.host_vars:
                try:                         
                    for k,v in ast.literal_eval(assets.host_vars).items():
                        if k not in ["ip", "port", "username", "password","ip"]:data[k] = v
                except Exception,ex:
                    logger.warn(msg="资产: {assets},转换host_vars失败:{ex}".format(assets=assets.id,ex=ex)) 
            resource.append(data)
        return sList, resource
    
    def inventory(self,inventory):
        sList = []
        resource = {} 
        groups = ''
        try:
            inventory = Ansible_Inventory.objects.get(id=inventory)
        except Exception, ex: 
            logger.warn(msg="资产组查询失败：{id}".format(id=inventory,ex=ex))
        for ds in inventory.inventory_group.all():
            resource[ds.group_name] = {}
            hosts = []
            for ser in ds.inventory_group_server.all():
                assets =  Assets.objects.get(id=ser.server)
                data = {}
                if hasattr(assets,'server_assets'):
                    try:
                        serverIp = assets.server_assets.ip
                        data["ip"] = serverIp
                        data["port"] = int(assets.server_assets.port)
                        data["username"] = assets.server_assets.username
                        data["sudo_passwd"] = assets.server_assets.sudo_passwd                        
                        if assets.server_assets.keyfile != 1:data["password"] =  assets.server_assets.passwd
                    except Exception, ex:
                        logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id,ex=ex))                     
                elif hasattr(assets,'network_assets'):                 
                    try:
                        serverIp = assets.network_assets.ip
                        data["ip"] = serverIp
                        data["port"] = int(assets.network_assets.port)
                        data["password"] = assets.network_assets.passwd,
                        data["username"] = assets.network_assets.username
                        data["sudo_passwd"] = assets.network_assets.sudo_passwd
                        data["connection"] = 'local'
                    except Exception, ex:
                        logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id,ex=ex))
                if assets.host_vars:
                    try:                         
                        for k,v in ast.literal_eval(assets.host_vars).items():
                            if k not in ["ip", "port", "username", "password","ip"]:data[k] = v
                    except Exception,ex:
                        logger.warn(msg="资产: {assets},转换host_vars失败:{ex}".format(assets=assets.id,ex=ex))                        
                if serverIp not in sList:sList.append(serverIp)
                hosts.append(data)
            resource[ds.group_name]['hosts'] = hosts 
            groups +=  ds.group_name + ','
            try:
                if ds.ext_vars:resource[ds.group_name]['vars'] = ast.literal_eval(ds.ext_vars)  
            except Exception,ex: 
                logger.warn(msg="资产组变量转换失败: {id} {ex}".format(id=inventory,ex=ex))
                resource[ds.group_name]['vars'] = None
        return sList, resource,groups       