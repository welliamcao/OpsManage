#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import uuid,xlrd
from asset.models import *
from apply.models import *
from django.contrib.auth.models import User,Group
from utils.logger import logger
from dao.base import DataHandle
from django.http import QueryDict
from apply.service.ipvs import IPVSRunner 

  

class AssetsIpvs(DataHandle):
    def __init__(self):
        super(AssetsIpvs, self).__init__()        
        
    def assets(self):
        dataList,aList = [],[]
        for ds in IPVS_RS_CONFIG.objects.all():
            try:
                if ds.rs_assets.id not in aList:
                    dataList.append(ds.to_assets())
                    aList.append(ds.rs_assets.id)
            except Exception as ex:
                logger.error("获取ipvs 资产失败: {msg}".format(msg=str(ex)))
                continue
        return dataList

    def allowcator(self,sub,args,request=None):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args,request)
        else:
            logger.error(msg="AssetsIpvs没有{sub}方法".format(sub=sub))       
            return []         
    
    def tree(self,tree=None):
        dataList = []
        for ds in IPVS_CONFIG.objects.raw("""SELECT t1.id,t2.project,count(t2.project) as pcount from opsmanage_ipvs_config as t1,opsmanage_assets as t2 WHERE t1.ipvs_assets_id = t2.id GROUP BY t2.project;"""):
            data = dict()
            try:
                project = Project_Assets.objects.get(id=ds.project)
                data["text"] = "{name} ({num})".format(name=str(project.project_name),num=str(ds.pcount))
            except Exception as ex:
                logger.error("获取ipvs tree项目失败: {msg}".format(msg=str(ex)))
                continue
            data["id"] = ds.id + 10000
            data["state"] = {"opened" : 'true' }
            data["icon"] = "fa fa-database"
            data["children"] = [] 
            for svr in Service_Assets.objects.filter(project=project):
                sData = {}
                for ds in IPVS_CONFIG.objects.raw("""SELECT t2.id,count(t2.business) as scount from opsmanage_ipvs_config as t1,opsmanage_assets as t2 WHERE t1.ipvs_assets_id = t2.id and t2.business={sid} GROUP BY t2.business;""".format(sid=svr.id)):
                    sData["id"] = svr.id + 20000
                    sData["text"] = "{name} ({num})".format(name=str(svr.service_name),num=str(ds.scount))
                    sData["icon"] =  "fa fa-circle-o"
                    data["children"].append(sData)
            dataList.append(data)
        return dataList   
    
    def service(self,service=0):
        dataList = []
        for ds in IPVS_CONFIG.objects.raw("""SELECT t1.*  from opsmanage_ipvs_config as t1,opsmanage_assets as t2 WHERE t1.ipvs_assets_id = t2.id and t2.business={service};""".format(service=service)):
            data = ds.to_json()
            data["rs_list"] = [ x.to_json() for x in ds.ipvs_rs.all() ]
            data["rs_count"] = len(data["rs_list"])
            dataList.append(data)
        return {"next":None,"previous":None,"results":dataList}       

class IVPSManage():
    def __init__(self):
        super(IVPSManage, self).__init__() 
    
    def get_ipvs_vip(self,id):
        try:
            return IPVS_CONFIG.objects.get(id=id)
        except Exception as ex:
            logger.error(msg="Ipvs VIP查询失败：{ex}".format(ex=ex))       
    
    def get_ipvs_rs(self,id):
        try:
            return IPVS_RS_CONFIG.objects.get(id=id)
        except Exception as ex:
            logger.error(msg="Ipvs RealServer查询失败: {ex}".format(ex=ex)) 
    
    def vip_status(self,request):
#         is_active = 0
        vip = self.get_ipvs_vip(QueryDict(request.body).get('id'))
        if vip:
            try:
                vip.is_active = QueryDict(request.body).get('is_active')
                vip.save()
            except Exception as ex:
                return "vip状态更新失败: {ex}".format(ex=ex)

            IPVS = IPVSRunner(vip=vip)   
            
            if int(vip.is_active) == 0:
#                 is_active = 1
                result = IPVS.run('del_vip') 
            else:
                result = IPVS.run('add_vip')  
                
            if result: 
#                 vip.is_active = is_active
#                 vip.save()                
                return str(result)
        else:
            return "vip不存在可能已被删除"

    def rs_status(self,request):
        realserver = self.get_ipvs_rs(QueryDict(request.body).get('id'))
        if realserver:
            try:
                realserver.is_active = QueryDict(request.body).get('is_active')
                realserver.save()
            except Exception as ex:
                return "realserver状态更新失败: {ex}".format(ex=ex)

            IPVS = IPVSRunner(vip=realserver.ipvs_vip,realserver=realserver) 
            
            if int(realserver.is_active) == 0:
                result = IPVS.run('del_rs') 
            else:
                result = IPVS.run('add_rs')  
                
            if result:            
                return str(result)
        else:
            return "realserver不存在可能已被删除"
    
    def vip_batch_modf(self,request):
        args = QueryDict(request.body).dict()
        vip_id_list = QueryDict(request.body).getlist('ipvs_vip')
        args.pop('ipvs_vip')
        try:
            IPVS_CONFIG.objects.filter(id__in=vip_id_list).update(**args)
        except Exception as ex:
            logger.error(msg="Ipvs VIP批量修改失败： {ex}".format(ex=ex))   
            return "Ipvs VIP批量修改失: {ex}".format(ex=ex)
                
    def rs_batch_modf(self,request):
        args = QueryDict(request.body).dict()
        rs_id_list = QueryDict(request.body).getlist('rs_ids')
        args.pop('rs_ids')
        try:
            realserver = IPVS_RS_CONFIG.objects.filter(id__in=rs_id_list)
            realserver.update(**args)   
        except Exception as ex:
            logger.error(msg="Ipvs RealServer批量修改失败: {ex}".format(ex=ex))                   
            return "Ipvs RealServer批量修改失败: {ex}".format(ex=ex)
        
        vipList = [ ]
        for ds in realserver:
            if ds.ipvs_vip not in vipList and int(ds.ipvs_vip.is_active) == 1:
                vipList.append(ds.ipvs_vip)
#             
        IPVS = IPVSRunner(vip=vipList,realserver=realserver) 
        IPVS.run('batch_modf_rs') 
#          
#         cmds = ''
#          
#         for ds in realserver:
#             if int(ds.is_active) == 1:cmds = cmds + ';' +ds.modf_realsever()
#              
#         if len(cmds) > 0:
#             result = IPVS.run('batch_modf_rs',cmds)  
#                      
#             if result:            
#                 return str(result)        
        
                
    def rs_batch_delete(self,request):
        args = QueryDict(request.body).dict()  
        rs_id_list = QueryDict(request.body).getlist('rs_ids[]')
        args.pop('rs_ids[]')
        try:
            IPVS_RS_CONFIG.objects.filter(id__in=rs_id_list).delete() 
        except Exception as ex:
            logger.error(msg="Ipvs RealServer批量删除失败: {ex}".format(ex=ex))                   
            return "Ipvs RealServer批量删除失败: {ex}".format(ex=ex)        
                                                                      
ASSETSIPVS = AssetsIpvs()