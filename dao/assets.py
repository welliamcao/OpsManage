#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from OpsManage.models import Assets,Server_Assets,Network_Assets
from OpsManage.utils.logger import logger

class AssetsSource(object):
    def __init__(self):
        super(AssetsSource,self).__init__()
    
    def serverList(self):
        serverList = []
        for assets in Assets.objects.filter(assets_type__in=["server","vmser","switch","route"]):
            if hasattr(assets,'server_assets'):
                serverList.append({"id":assets.id,"ip":assets.server_assets.ip})
            elif hasattr(assets,'network_assets'):
                serverList.append({"id":assets.id,"ip":assets.network_assets.ip})
        return  serverList   
    
    def queryAssetsByIp(self,ipList):
        sList = []
        resource = []          
        for ip in ipList:
            server = Server_Assets.objects.filter(ip=ip).count()
            network = Network_Assets.objects.filter(ip=ip).count()
            if server > 0:
                try:
                    server_assets = Server_Assets.objects.get(ip=ip)
                    sList.append(server_assets.ip)
                    if server_assets.keyfile == 1:resource.append({"hostname": server_assets.ip, 
                                                                   "port": int(server_assets.port),
                                                                   "username": server_assets.username,
                                                                   "sudo_passwd": server_assets.sudo_passwd})
                    else:resource.append({"hostname": server_assets.ip, 
                                          "port": int(server_assets.port),
                                          "username": server_assets.username,
                                          "password": server_assets.passwd,
                                          "sudo_passwd": server_assets.sudo_passwd})                    
                except Exception, ex:
                    logger.warn(msg="server_id:{assets}, error:{ex}".format(assets=server_assets.id,ex=ex))
            elif network > 0:
                try:    
                    network_assets = Network_Assets.objects.get(ip=ip)
                    sList.append(network_assets.ip)
                    resource.append({"hostname": network_assets.ip, 
                                     "port": int(network_assets.port),
                                     "username": network_assets.username,
                                     "password": network_assets.passwd,
                                     "sudo_passwd": network_assets.sudo_passwd,
                                     "connection":'local'
                                     }) 
                except Exception, ex:
                    logger.warn(msg="network_id:{assets}, error:{ex}".format(assets=server_assets.id,ex=ex))   
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
            if hasattr(assets,'server_assets'):
                try:
                    sList.append(assets.server_assets.ip)
                    if assets.server_assets.keyfile == 1:resource.append({"hostname": assets.server_assets.ip,
                                                                          "port": int(assets.server_assets.port),
                                                                          "username": assets.server_assets.username,
                                                                          "sudo_passwd": assets.server_assets.sudo_passwd})
                    else:resource.append({"hostname": assets.server_assets.ip, 
                                          "port": int(assets.server_assets.port),
                                          "username": assets.server_assets.username,
                                          "password": assets.server_assets.passwd,
                                          "sudo_passwd": assets.server_assets.sudo_passwd}) 
                except Exception, ex:
                    logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id,ex=ex))                    
            elif hasattr(assets,'network_assets'):
                try:
                    sList.append(assets.network_assets.ip)
                    resource.append({"hostname": assets.network_assets.ip, 
                                     "port": int(assets.network_assets.port),
                                     "username": assets.network_assets.username,
                                     "password": assets.network_assets.passwd,
                                     "sudo_passwd": assets.network_assets.sudo_passwd,
                                     "connection":'local'
                                     }) 
                except Exception, ex:
                    logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id,ex=ex))                    

        return sList, resource