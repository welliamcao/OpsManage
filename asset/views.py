#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import os
from django.views.generic import View
from django.http import QueryDict
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Assets,Server_Assets,NetworkCard_Assets
from dao.assets import AssetsBase,AssetsSource
from utils.logger import logger
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from utils.base import method_decorator_adaptor
from asset.models import Network_Assets

        
class Config(LoginRequiredMixin,AssetsBase,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request, 'assets/assets_config.html',{"user":request.user,"assets":self.base()})
        
        
class AssetsManage(LoginRequiredMixin,AssetsBase,View):
    login_url = '/login/'  
    
    @method_decorator_adaptor(permission_required, "asset.assets_read_assets","/403/")   
    def get(self, request, *args, **kwagrs):
        if request.GET.get('id') and request.GET.get('model')=='edit':
            return render(request, 'assets/assets_modf.html',{"user":request.user,"assets":self.assets(id=request.GET.get('id')),"assetsBase":self.base()}) 
        elif request.GET.get('id') and request.GET.get('model')=='info':
            return JsonResponse({'msg':"主机查询成功","code":200,'data':self.info(request.GET.get('id'))})  
        return render(request, 'assets/assets_add.html',{"user":request.user,"assets":self.base()})    
                  
         
class AssetsList(LoginRequiredMixin,AssetsBase,View):
    login_url = '/login/'  
    @method_decorator_adaptor(permission_required, "asset.assets_read_assets","/403/")   
    def get(self, request, *args, **kwagrs):
        return render(request, 'assets/assets_list.html',{"user":request.user,"assets":self.base(),"assetsList":self.assetsList()})   
    
    
class AssetsTree(LoginRequiredMixin,AssetsBase,View):
    login_url = '/login/'  
    @method_decorator_adaptor(permission_required, "asset.assets_read_assets","/403/")   
    def get(self, request, *args, **kwagrs):
        return render(request, 'assets/assets_tree.html',{"user":request.user})     


class AssetsServer(LoginRequiredMixin,AssetsBase,View):
    login_url = '/login/'
    def post(self, request, *args, **kwagrs):
        return JsonResponse({'msg':"主机查询成功","code":200,'data':self.allowcator(request.POST.get('query'), request.POST.get('id'),request)})  
         
    
    
class AssetsModf(LoginRequiredMixin,AssetsSource,View):
    login_url = '/login/'  
        
    def post(self, request, *args, **kwagrs):
        fList,sList = self.allowcator(request.POST.get('model'),request)
        if fList:return JsonResponse({'msg':fList,"code":400})               
        return JsonResponse({"code":200,"msg":"资产更新成功","data":[]})   
    
class AssetsSearch(LoginRequiredMixin,AssetsBase,View):
    login_url = '/login/'  
    AssetFieldsList = [ n.name for n in Assets._meta.fields ]
    ServerAssetFieldsList = [ n.name for n in Server_Assets._meta.fields ]
    
    def get(self, request, *args, **kwagrs):
        return render(request, 'assets/assets_search.html',{"user":request.user,"assets":self.base()})
    
    def post(self, request, *args, **kwagrs):
        AssetIntersection = list(set(request.POST.keys()).intersection(set(self.AssetFieldsList)))
        ServerAssetIntersection = list(set(request.POST.keys()).intersection(set(self.ServerAssetFieldsList)))
        assetsList = []
        data = dict()
        #格式化查询条件
        for (k,v)  in request.POST.items() :
            if v is not None and v != u'':
                data[k] = v 

        if list(set(['buy_time' , 'expire_date' , 'vcpu_number',
                     'cpu_core','cpu_number','ram_total',
                     'swap','disk_total']).intersection(set(request.POST.keys()))):
            try:
                buy_time = request.POST.get('buy_time').split('-')
                data.pop('buy_time')
                data['buy_time__gte'] = buy_time[0] + '-01-01'
                data['buy_time__lte'] = buy_time[1] + '-01-01'
            except:
                pass
            try:
                expire_date = request.POST.get('expire_date').split('-')
                data.pop('expire_date')
                data['expire_date__gte'] = expire_date[0] + '-01-01'
                data['expire_date__lte'] = expire_date[1] + '-01-01'
            except:
                pass
            try:
                vcpu_number = request.POST.get('vcpu_number').split('-')
                data.pop('vcpu_number')
                data['vcpu_number__gte'] = int(vcpu_number[0])
                data['vcpu_number__lte'] = int(vcpu_number[1])
            except:
                pass  
            try:
                cpu_number = request.POST.get('cpu_number').split('-')
                data.pop('cpu_number')
                data['cpu_number__gte'] = int(cpu_number[0])
                data['cpu_number__lte'] = int(cpu_number[1])
            except:
                pass  
            try:
                cpu_core = request.POST.get('cpu_core').split('-')
                data.pop('cpu_core')
                data['cpu_core__gte'] = int(cpu_core[0])
                data['cpu_core__lte'] = int(cpu_core[1])
            except:
                pass  
            try:
                swap = request.POST.get('swap').split('-')
                data.pop('swap')
                data['swap__gte'] = int(swap[0])
                data['swap__lte'] = int(swap[1])
            except:
                pass   
            try:
                disk_total = request.POST.get('disk_total').split('-')
                data.pop('disk_total')
                data['disk_total__gte'] = int(disk_total[0])
                data['disk_total__lte'] = int(disk_total[1])
            except:
                pass       
            try:
                ram_total = request.POST.get('ram_total').split('-')
                data.pop('ram_total')
                data['ram_total__gte'] = int(ram_total[0])
                data['ram_total__lte'] = int(ram_total[1])
            except:
                pass 

        if set(["ip"]).issubset(data):
            for ds in NetworkCard_Assets.objects.filter(ip=data.get('ip')):
                if ds.assets not in assetsList:assetsList.append(ds.assets) 
  
        else:                                                     
            if len(AssetIntersection) > 0 and len(ServerAssetIntersection) > 0:
                assetsData = dict()
                for a in AssetIntersection:
                    for k in data.keys():
                        if k.find(a) != -1:
                            assetsData[k] = data[k]
                            data.pop(k)
                serverList = [ a.assets_id for a in Server_Assets.objects.filter(**data) ]
                assetsData['id__in'] = serverList
                assetsList.extend(Assets.objects.filter(**assetsData))             
                
            elif len(AssetIntersection) > 0 and len(ServerAssetIntersection) == 0:
                assetsList.extend(Assets.objects.filter(**data)) 
                
            elif len(AssetIntersection) == 0 and len(ServerAssetIntersection) > 0:
                for ds in Server_Assets.objects.filter(**data):
                    if ds.assets not in assetsList:assetsList.append(ds.assets)
                
        baseAssets = self.base()
        dataList = []
        for a in assetsList:
            if hasattr(a,'server_assets'):
                sip = a.server_assets.ip
            elif hasattr(a,'network_assets'):
                sip = a.network_assets.ip
            else:
                sip = '未知'
            management_ip = '''{ip}'''.format(ip=sip)  
            try:  
                system = a.server_assets.system
            except:
                system =  '无数据'   
            try:  
                kernel = a.server_assets.kernel
            except:
                kernel =  '无数据'   
            try:  
                vcpu_number = a.server_assets.vcpu_number
            except:
                vcpu_number =  '无数据'                   
            try:
                ram_total = str(a.server_assets.ram_total) + 'GB' 
            except:
                ram_total = '无数据'
            try:
                disk_total = str(a.server_assets.disk_total) + 'GB' 
            except:
                disk_total = '无数据'                
            for p in baseAssets.get('projectList'):
                if p.id == a.project:project = '''{project}'''.format(project=p.project_name)                                      
            for s in baseAssets.get('serviceList'):
                if s.id == a.business:service = '''{service}'''.format(service=s.service_name)
            for z in baseAssets.get('zoneList'):
                if z.id == a.put_zone:put_zone = '''{zone_name}'''.format(zone_name=z.zone_name)      
            opt = ''' <div class="btn-group btn-group-sm">                
                    <button type="button" name="btn-assets-alter" value="{id}" class="btn btn-default" aria-label="Center Align"><a href="/assets/manage/?id={id}&model=edit" target="view_window"><span class="glyphicon glyphicon-check" aria-hidden="true"></span></a>
                    </button>
                    <button type="button" name="btn-assets-info" value="{id}" class="btn btn-default" aria-label="Right Align" data-toggle="modal" data-target=".bs-example-modal-info"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>
                    </button>
                    <button type="button" name="btn-assets-update" value="{id}" class="btn btn-default" aria-label="Right Align"><span class="glyphicon glyphicon-refresh" aria-hidden="true"></span>
                    </button>
                    <button type="button" name="btn-assets-hw" value="{id}" class="btn btn-default" aria-label="Right Align"><span class="fa fa-hdd-o" aria-hidden="true"></span>
                    </button>                    
                    <button type="button" name="btn-assets-delete" value="{id}" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
                    </button></div>
                 '''.format(id=a.id)
            dataList.append(
                             {"详情":'',
                             '全选':'<input type="checkbox" class="flat" value="{id}" name="table_records"/>'.format(id=a.id),
                             '资产ID':a.id,
                             '所属项目':project,
                             '应用类型':service,                             
                             'IP地址':management_ip,
                             '操作系统':system,
                             '内核版本':kernel,                             
                             'CPU':vcpu_number,
                             '内存(GB)':ram_total,
                             '硬盘(GB)':disk_total,
                             '放置区域':put_zone,
                             '操作':opt}
                             )                                                                                                                                                                                          
        return JsonResponse({'msg':"数据查询成功","code":200,'data':dataList,'count':0})   
    
class AssetsBatch(LoginRequiredMixin,AssetsSource,View):  
    login_url = '/login/'  
    fList = []
    sList = []    
    
    @method_decorator_adaptor(permission_required, "asset.assets_change_assets","/403/")     
    def post(self, request, *args, **kwagrs):
        fList,sList = self.allowcator(request.POST.get('model'),request)                     
        if sList:
            return JsonResponse({'msg':"数据更新成功","code":200,'data':{"success":sList,"failed":fList}}) 
        else:return JsonResponse({'msg':fList,"code":500,'data':{"success":sList,"failed":fList}})     
    
    @method_decorator_adaptor(permission_required, "asset.assets_delete_assets","/403/")     
    def delete(self, request, *args, **kwagrs):
        for ast in QueryDict(request.body).getlist('assetsIds[]'):
            try:
                assets = Assets.objects.get(id=int(ast))
            except Exception as ex:
                logger.error(msg="删除资产失败: {ex}".format(ex=ex))
                continue
            if assets.assets_type in ['vmser','server']:
                try:
                    server_assets = Server_Assets.objects.get(assets=assets)
                except Exception as ex:
                    self.fList.append(assets.management_ip)
                    assets.delete() 
                    continue   
                self.sList.append(server_assets.ip)
                server_assets.delete()                    
            else:
                try:
                    net_assets = NetworkCard_Assets.objects.get(assets=assets)
                except Exception as ex:
                    self.fList.append(assets.management_ip)
                    assets.delete() 
                    continue  
                self.sList.append(assets.management_ip)
                net_assets.delete()                    
            assets.delete()                                    
        return JsonResponse({'msg':"数据删除成功","code":200,'data':{"success":self.sList,"failed":self.fList}})             
    
class AssetsImport(LoginRequiredMixin,AssetsBase,View):       
    login_url = '/login/' 
    
    @method_decorator_adaptor(permission_required, "asset.assets_add_assets","/403/")   
    def post(self, request, *args, **kwagrs):
        f = request.FILES.get('import_file')
        filename = os.path.join(os.getcwd() + '/upload/',f.name)
        if os.path.isdir(os.path.dirname(filename)) is not True:os.makedirs(os.path.dirname(filename))
        fobj = open(filename,'wb')
        for chrunk in f.chunks():
            fobj.write(chrunk)
        fobj.close()
        res = self.import_assets(filename)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return HttpResponseRedirect('/user/center/')       