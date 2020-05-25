#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from asset.models import *
from apply.models import *
from utils.logger import logger
from django.http import QueryDict
from service.apply.ipvs import IPVSRunner 
from dao.base import AppsTree

class AssetsIpvs:
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
    
    def tree_business(self,business):
        return AppsTree(Business_Tree_Assets, IPVS_CONFIG).tree_business(business)
    
    def tree(self):
        return AppsTree(Business_Tree_Assets, IPVS_CONFIG).apply_tree()
             
          

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
    
    def vip_rate(self,request):
        vip = self.get_ipvs_vip(request.get('id'))
        IPVS = IPVSRunner(vip=vip) 
        return IPVS.run('vip_rate')

    def vip_stats(self,request):
        vip = self.get_ipvs_vip(request.get('id'))
        IPVS = IPVSRunner(vip=vip) 
        return IPVS.run('vip_stats')
    
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
        
        IPVS = IPVSRunner(vip=vipList,realserver=realserver) 
        return IPVS.run('batch_modf_rs') 
        
                
    def rs_batch_delete(self,request):
        args = QueryDict(request.body).dict()  
        rs_id_list = QueryDict(request.body).getlist('rs_ids[]')
        args.pop('rs_ids[]')
        try:
            realserver = IPVS_RS_CONFIG.objects.filter(id__in=rs_id_list)
            realserver.delete()  
        except Exception as ex:
            logger.error(msg="Ipvs RealServer批量删除失败: {ex}".format(ex=ex))                   
            return "Ipvs RealServer批量删除失败: {ex}".format(ex=ex)        
     
        vipList = [ ]
        for ds in realserver:
            if ds.ipvs_vip not in vipList and int(ds.ipvs_vip.is_active) == 1:
                vipList.append(ds.ipvs_vip)
        
        IPVS = IPVSRunner(vip=vipList,realserver=realserver) 
        return IPVS.run('batch_del_rs')    

    def ns_batch_delete(self,request):
        args = QueryDict(request.body).dict()  
        rs_id_list = QueryDict(request.body).getlist('ns_ids[]')
        args.pop('ns_ids[]')
        try:
            nameserver = IPVS_NS_CONFIG.objects.filter(id__in=rs_id_list)
            nameserver.delete()  
        except Exception as ex:
            logger.error(msg="Ipvs NameServer批量删除失败: {ex}".format(ex=ex))                   
            return "Ipvs NameServer批量删除失败: {ex}".format(ex=ex)        
    
                                                                       
ASSETSIPVS = AssetsIpvs()