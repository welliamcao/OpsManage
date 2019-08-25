#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import uuid,xlrd
from asset.models import *
from apply.models import *
from utils.logger import logger
from dao.base import DataHandle
from django.http import QueryDict
from apply.service.ipvs import IPVSRunner 
from django.db.models import Count
from mptt.templatetags.mptt_tags import cache_tree_children  

class AssetsIpvs(DataHandle):
    def __init__(self):
        super(AssetsIpvs, self).__init__()        

    def recursive_node_to_dict(self,node):
        json_format = node.to_json()
        children = [self.recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            json_format['children'] = children
        else:
            json_format['icon'] = 'fa fa-minus-square-o'        
        return json_format
        
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
    
    def business_paths_id_list(self,business):
        tree_list = []
        dataList = Business_Tree_Assets.objects.raw("""SELECT id FROM opsmanage_business_assets WHERE tree_id = {tree_id} AND  lft < {lft} AND  rght > {rght} ORDER BY lft ASC;""".format(tree_id=business.tree_id,lft=business.lft,rght=business.rght))
        for ds in dataList:
            tree_list.append(ds.id)
        tree_list.append(business.id)
        return tree_list
    
    def tree_business(self,business):
        dataList = []
        for ds in IPVS_CONFIG.objects.filter(business=business):
            dataList.append(ds.to_json())
        return dataList
    
    def tree(self):
        ipvs_business = [ ds.get("business") for ds in IPVS_CONFIG.objects.values('business').annotate(dcount=Count('business')) ]
        
        business_list = []
        
        for business in Business_Tree_Assets.objects.filter(id__in=ipvs_business):
            business_list += self.business_paths_id_list(business)
            
        business_list = list(set(business_list))
        
        business_node = Business_Tree_Assets.objects.filter(id__in=business_list)
        
        root_nodes = cache_tree_children(business_node)
        
        dataList = []
        for n in root_nodes:
            dataList.append(self.recursive_node_to_dict(n))         
        return dataList      
          

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