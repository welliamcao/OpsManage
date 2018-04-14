#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import os,xlrd,time
from django.http import JsonResponse
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from OpsManage.models import *
from django.db.models import Count
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.contrib.auth.models import Group,User
from OpsManage.tasks.assets import recordAssets
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from OpsManage.utils.logger import logger

def getBaseAssets():
    try:
        groupList = Group.objects.all()
    except:
        groupList = []
    try:
        serviceList = Service_Assets.objects.all()
    except:
        serviceList = []
    try:
        zoneList = Zone_Assets.objects.all()
    except:
        zoneList = []
    try:
        lineList = Line_Assets.objects.all()
    except:
        lineList = []
    try:
        raidList = Raid_Assets.objects.all()
    except:
        raidList = []  
    try:
        projectList = Project_Assets.objects.all()
    except:
        projectList = []          
    return {"group":groupList,"service":serviceList,"zone":zoneList,
            "line":lineList,"raid":raidList,'project':projectList}

@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_config(request):
    return render(request,'assets/assets_config.html',{"user":request.user,"baseAssets":getBaseAssets()},
                              )
    
@login_required(login_url='/login')
@permission_required('OpsManage.can_add_assets',login_url='/noperm/') 
def assets_add(request):
    if request.method == "GET":
        userList = User.objects.all()
        return render(request,'assets/assets_add.html',{"user":request.user,"baseAssets":getBaseAssets(),
                                                        'userList':userList})      
    
@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_list(request):
    userList = User.objects.all()
    assetsList = Assets.objects.all().order_by("-id") 
    for ds in assetsList:
        ds.nks = ds.networkcard_assets_set.all() 
    assetOnline = Assets.objects.filter(status=0).count()
    assetOffline = Assets.objects.filter(status=1).count()
    assetMaintain = Assets.objects.filter(status=2).count()
    assetsNumber = Assets.objects.values('assets_type').annotate(dcount=Count('assets_type'))
    return render(request,'assets/assets_list.html',{"user":request.user,"totalAssets":assetsList.count(),
                                                         "assetOnline":assetOnline,"assetOffline":assetOffline,
                                                         "assetMaintain":assetMaintain,"baseAssets":getBaseAssets(),
                                                         "assetsList":assetsList,"assetsNumber":assetsNumber,
                                                         'userList':userList},
                              )

@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_view(request,aid): 
    try:
        assets = Assets.objects.get(id=aid)
        userList = User.objects.all()
    except:
        return render(request,'404.html',{"user":request.user},
                                )  
    if assets.assets_type in ['server','vmser']:
        try:
            asset_ram = assets.ram_assets_set.all()
        except:
            asset_ram = []
        try:
            asset_disk = assets.disk_assets_set.all()
        except:
            asset_disk = []
        try:
            asset_nks = assets.networkcard_assets_set.all()
        except Exception, ex:
            asset_nks = [] 
            logger.warn(msg="获取网卡设备资产失败: {ex}".format(ex=str(ex)))
        try:
            asset_body = assets.server_assets                    
        except:
            return render(request,'assets/assets_view.html',{"user":request.user},
                            ) 
        return render(request,'assets/assets_view.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "asset_ram":asset_ram,"asset_disk":asset_disk,
                                                            "baseAssets":getBaseAssets(),'userList':userList,
                                                            "asset_nks":asset_nks},
                            )   
    else:
        try:
            asset_body = assets.network_assets
        except:
            return render(request,'assets/assets_view.html',{"user":request.user},
                            )                 
        return render(request,'assets/assets_view.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "baseAssets":getBaseAssets(),'userList':userList},
                            )  
             
@login_required(login_url='/login')
@permission_required('OpsManage.can_change_assets',login_url='/noperm/') 
def assets_modf(request,aid):  
    try:
        assets = Assets.objects.get(id=aid)
        userList = User.objects.all()
    except:
        return render(request,'assets/assets_modf.html',{"user":request.user},
                                )  
    if assets.assets_type in ['server','vmser']:
        try:
            asset_ram = assets.ram_assets_set.all()
        except:
            asset_ram = []
        try:
            asset_disk = assets.disk_assets_set.all()
        except:
            asset_disk = []
        try:
            asset_body = assets.server_assets                    
        except Exception ,ex:
            logger.error(msg="修改资产失败: {ex}".format(ex=str(ex)))
            return render(request,'404.html',{"user":request.user},
                            )         
        return render(request,'assets/assets_modf.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "asset_ram":asset_ram,"asset_disk":asset_disk,
                                                            "assets_data":getBaseAssets(),'userList':userList},
                            )    
    else:     
        try:
            asset_body = assets.network_assets
        except:
            return render(request,'assets/assets_modf.html',{"user":request.user},   
                                      )                                                 
        return render(request,'assets/assets_modf.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "assets_data":getBaseAssets(),'userList':userList},
                            )  
        
@login_required(login_url='/login')
@permission_required('OpsManage.can_change_server_assets',login_url='/noperm/') 
def assets_facts(request,args=None):
    if request.method == "POST" and request.user.has_perm('OpsManage.change_server_assets'):
        server_id = request.POST.get('server_id')
        genre = request.POST.get('type')
        if genre == 'setup':
            try:
                server_assets = Server_Assets.objects.get(id=request.POST.get('server_id'))
                if server_assets.keyfile == 1:resource = [{"hostname": server_assets.ip, "port": int(server_assets.port),"username": server_assets.username}] 
                else:resource = [{"hostname": server_assets.ip, "port": server_assets.port,"username": server_assets.username, "password": server_assets.passwd}]
            except Exception,ex:
                logger.error(msg="更新资产失败: {ex}".format(ex=str(ex)))
                return  JsonResponse({'msg':"数据更新失败-查询不到该主机资料~","code":502})
            ANS = ANSRunner(resource)
            ANS.run_model(host_list=[server_assets.ip],module_name='setup',module_args="")
            data = ANS.handle_cmdb_data(ANS.get_model_result())
            if data:
                for ds in data:
                    status = ds.get('status')
                    if status == 0:
                        try:
                            assets = Assets.objects.get(id=server_assets.assets_id) 
                            Assets.objects.filter(id=server_assets.assets_id).update(sn=ds.get('serial'),model=ds.get('model'),
                                                                                     manufacturer=ds.get('manufacturer'))
                        except Exception, ex:
                            logger.error(msg="获取服务器信息失败: {ex}".format(ex=str(ex)))
                            return  JsonResponse({'msg':"数据更新失败-查询不到该主机的资产信息","code":403})
                        try:
                            Server_Assets.objects.filter(id=server_id).update(cpu_number=ds.get('cpu_number'),kernel=ds.get('kernel'),
                                                                                  selinux=ds.get('selinux'),hostname=ds.get('hostname'),
                                                                                  system=ds.get('system'),cpu=ds.get('cpu'),
                                                                                  disk_total=ds.get('disk_total'),cpu_core=ds.get('cpu_core'),
                                                                                  swap=ds.get('swap'),ram_total=ds.get('ram_total'),
                                                                                  vcpu_number=ds.get('vcpu_number')
                                                                                  )
                            recordAssets.delay(user=str(request.user),content="修改服务器资产：{ip}".format(ip=server_assets.ip),type="server",id=server_assets.id)
                        except Exception, ex:
                            logger.error(msg="更新服务器信息失败: {ex}".format(ex=str(ex)))
                            return JsonResponse({'msg':"数据更新失败-写入数据失败","code":400})
                        for nk in ds.get('nks'):
                            macaddress = nk.get('macaddress')
                            count = NetworkCard_Assets.objects.filter(assets=assets,macaddress=macaddress).count()
                            if count > 0:
                                try:
                                    NetworkCard_Assets.objects.filter(assets=assets,macaddress=macaddress).update(assets=assets,device=nk.get('device'),
                                                                                                                       ip=nk.get('address'),module=nk.get('module'),
                                                                                                                       mtu=nk.get('mtu'),active=nk.get('active'))
                                except Exception, ex:
                                    logger.warn(msg="更新服务器网卡信息失败: {ex}".format(ex=str(ex)))
                            else:
                                try:
                                    NetworkCard_Assets.objects.create(assets=assets,device=nk.get('device'),
                                                                  macaddress=nk.get('macaddress'),
                                                                  ip=nk.get('address'),module=nk.get('module'),
                                                                  mtu=nk.get('mtu'),active=nk.get('active'))
                                except Exception, ex:
                                    logger.warn(msg="写入服务器网卡信息失败: {ex}".format(ex=str(ex)))
                            
                    else:
                        return JsonResponse({'msg':"数据更新失败-无法链接主机~","code":502})                    
                return JsonResponse({'msg':"数据更新成功","code":200})
            else:
                return JsonResponse({'msg':"数据更新失败-请检查Ansible配置","code":400})

        elif genre == 'crawHw':
            try:
                server_assets = Server_Assets.objects.get(id=server_id)
                assets = Assets.objects.get(id=server_assets.assets_id)
                if server_assets.keyfile == 1:resource = [{"hostname": server_assets.ip, "port": int(server_assets.port),"username": server_assets.username}] 
                else:resource = [{"hostname": server_assets.ip, "port": server_assets.port,"username": server_assets.username, "password": server_assets.passwd}]
            except Exception,e:
                logger.error(msg="更新硬件信息失败: {ex}".format(ex=ex))
                return  JsonResponse({'msg':"数据更新失败-查询不到该主机资料~","code":502})
            ANS = ANSRunner(resource)
            ANS.run_model(host_list=[server_assets.ip],module_name='crawHw',module_args="")
            data = ANS.handle_cmdb_crawHw_data(ANS.get_model_result())
            if data:
                for ds in data:
                    if ds.get('mem_info'):
                        for mem in ds.get('mem_info'):
                            if Ram_Assets.objects.filter(assets=assets,device_slot=mem.get('slot')).count() > 0:
                                try:
                                    Ram_Assets.objects.filter(assets=assets,device_slot=mem.get('slot')).update(
                                                            device_slot=mem.get('slot'),device_model=mem.get('serial'),
                                                            device_brand= mem.get('manufacturer'),device_volume=mem.get('size'),
                                                            device_status="Online"
                                                            )
        
                                except Exception, ex:
                                    return JsonResponse({'msg':"数据更新失败-写入数据失败","code":400})                        
                            else:
                                try:
                                    Ram_Assets.objects.create(device_slot=mem.get('slot'),device_model=mem.get('serial'),
                                                             device_brand= mem.get('manufacturer'),device_volume=mem.get('size'),
                                                             device_status="Online",assets=assets
                                                             )
                                    recordAssets.delay(user=str(request.user),content="修改服务器资产：{ip}".format(ip=server_assets.ip),type="server",id=server_assets.id)
                                except Exception,e:
                                    return JsonResponse({'msg':"数据更新失败-写入数据失败","code":400})
                    if ds.get('disk_info'):
                        for disk in ds.get('disk_info'):
                            if Disk_Assets.objects.filter(assets=assets,device_slot=disk.get('slot')).count() > 0:
                                try:
                                    Disk_Assets.objects.filter(assets=assets,device_slot=disk.get('slot')).update(
                                                            device_serial=disk.get('serial'),device_model=disk.get('model'),
                                                            device_brand= disk.get('manufacturer'),device_volume=disk.get('size'),
                                                            device_status="Online"
                                                             )
        
                                except Exception,e:
                                    return JsonResponse({'msg':"数据更新失败-写入数据失败","code":400})  
                            else:                           
                                try:
                                    Disk_Assets.objects.create(device_serial=disk.get('serial'),device_model=disk.get('model'),
                                                             device_brand= disk.get('manufacturer'),device_volume=disk.get('size'),
                                                             device_status="Online",assets=assets,device_slot=disk.get('slot')
                                                             )
                                    recordAssets.delay(user=str(request.user),content="修改服务器资产：{ip}".format(ip=server_assets.ip),type="server",id=server_assets.id)
                                except Exception,e:
                                    return JsonResponse({'msg':"数据更新失败-写入数据失败","code":400})                        

                return JsonResponse({'msg':"数据更新成功","code":200})
            else:
                return JsonResponse({'msg':"数据更新失败，系统可能不支持，未能获取数据","code":400})

    else:
        return JsonResponse({'msg':"您没有该项操作的权限~","code":400})


@login_required(login_url='/login')
@permission_required('OpsManage.can_change_server_assets',login_url='/noperm/') 
def assets_import(request):
    if request.method == "POST":
        f = request.FILES.get('import_file')
        filename = os.path.join(os.getcwd() + '/upload/',f.name)
        if os.path.isdir(os.path.dirname(filename)) is not True:os.makedirs(os.path.dirname(filename))
        fobj = open(filename,'wb')
        for chrunk in f.chunks():
            fobj.write(chrunk)
        fobj.close()
        #读取上传的execl文件内容方法
        def getAssetsData(fname=filename):
            bk = xlrd.open_workbook(fname)
            dataList = []
            try:
                server = bk.sheet_by_name("server")
                net = bk.sheet_by_name("net")
                for i in range(1,server.nrows):
                    dataList.append(server.row_values(i)) 
                for i in range(1,net.nrows):
                    dataList.append(net.row_values(i))     
            except Exception,e:
                return []
            return dataList 
        dataList = getAssetsData(fname=filename)
        #获取服务器列表
        for data in dataList:
            assets = {
                      'assets_type':data[0],
                      'name':data[1],
                      'sn':data[2],
                      'buy_user':int(data[5]),
                      'management_ip':data[6],
                      'manufacturer':data[7],
                      'model':data[8],
                      'provider':data[9],
                      'status':int(data[10]),
                      'put_zone':int(data[11]),
                      'group':int(data[12]),
                      'project':int(data[13]),
                      'business':int(data[14]),
                      }
            if data[3]:assets['buy_time'] = xlrd.xldate.xldate_as_datetime(data[3],0)
            if data[4]:assets['expire_date'] = xlrd.xldate.xldate_as_datetime(data[4],0)
            if assets.get('assets_type') in ['vmser','server']:
                server_assets = {
                          'ip':data[15],
                          'keyfile':data[16],
                          'username':data[17],
                          'passwd':data[18],
                          'hostname':data[19],
                          'port':data[20],
                          'raid':data[21],
                          'line':data[22],
                          } 
            else:
                net_assets = {
                            'ip':data[15],
                            'bandwidth':data[16],
                            'port_number': data[17],
                            'firmware':data[18],
                            'cpu':data[19],
                            'stone':data[20],
                            'configure_detail': data[21]                              
                              }                                                  
            count = Assets.objects.filter(name=assets.get('name')).count()
            if count == 1:
                assetsObj = Assets.objects.get(name=assets.get('name'))
                Assets.objects.filter(name=assets.get('name')).update(**assets)
                try:
                    if assets.get('assets_type') in ['vmser','server']:
                        Server_Assets.objects.filter(assets=assetsObj).update(**server_assets)
                    elif assets.get('assets_type') in ['switch','route','printer','scanner','firewall','storage','wifi']:
                        Network_Assets.objects.filter(assets=assetsObj).update(**net_assets)
                except  Exception,ex:
                    print ex
            else:
                try:
                    assetsObj = Assets.objects.create(**assets)   
                except Exception, ex:
                    logger.warn(msg="批量写入资产失败: {ex}".format(ex=str(ex)))
                if assetsObj:
                    try:  
                        if assets.get('assets_type') in ['vmser','server']:
                            Server_Assets.objects.create(assets=assetsObj,**server_assets)
                        elif assets.get('assets_type') in ['switch','route','printer','scanner','firewall','storage','wifi']:
                            Network_Assets.objects.create(assets=assetsObj,**net_assets)                          
                    except Exception, ex:
                        logger.warn(msg="批量更新资产失败: {ex}".format(ex=str(ex)))
                        assetsObj.delete()
        return HttpResponseRedirect('/assets_list')


@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_search(request): 
    AssetFieldsList = [ n.name for n in Assets._meta.fields ]
    ServerAssetFieldsList = [ n.name for n in Server_Assets._meta.fields ]
    if request.method == "GET":
        manufacturerList = [  m.manufacturer for m in Assets.objects.raw('SELECT id,manufacturer from opsmanage_assets WHERE  manufacturer is not null GROUP BY manufacturer')]
        modelList = [  m.model for m in Assets.objects.raw('SELECT id,model from opsmanage_assets WHERE model is not null  GROUP BY model')]
        providerList = [  m.provider for m in Assets.objects.raw('SELECT id,provider from opsmanage_assets WHERE provider is not null GROUP BY provider')]
        cpuList = [  a.cpu for a in Assets.objects.raw('SELECT id,cpu from opsmanage_server_assets WHERE cpu is not null GROUP BY cpu')]
        buyUserList = User.objects.all()
        selinuxList = [  m.selinux for m in Assets.objects.raw('SELECT id,selinux from opsmanage_server_assets WHERE selinux is not null GROUP BY selinux')]
        systemList = [  m.system for m in Assets.objects.raw('SELECT id,system from opsmanage_server_assets WHERE system is not null GROUP BY system')]    
        kernelList = [  m.kernel for m in Assets.objects.raw('SELECT id,kernel from opsmanage_server_assets WHERE kernel is not null GROUP BY kernel')]   
        return render(request,'assets/assets_search.html',{"user":request.user,"baseAssets":getBaseAssets(),
                                                               "manufacturerList":manufacturerList,"modelList":modelList,
                                                               "providerList":providerList,"cpuList":cpuList,
                                                               "buyUserList":buyUserList,"selinuxList":selinuxList,
                                                               "systemList":systemList,'kernelList':kernelList,
                                                             },
                                  ) 
    elif request.method == "POST":  
        AssetIntersection = list(set(request.POST.keys()).intersection(set(AssetFieldsList)))
        ServerAssetIntersection = list(set(request.POST.keys()).intersection(set(ServerAssetFieldsList)))
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
                data['disk_total__gte'] = int(disk_total[0])*1024
                data['disk_total__lte'] = int(disk_total[1])*1024
            except:
                pass       
            try:
                ram_total = request.POST.get('ram_total').split('-')
                data.pop('ram_total')
                data['ram_total__gte'] = int(ram_total[0])
                data['ram_total__lte'] = int(ram_total[1])
            except:
                pass 
            

        if data.has_key('ip'):
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
                
        baseAssets = getBaseAssets()
        dataList = []
        for a in assetsList:
            assets_id = '''<td class="text-center"><input type="checkbox" value="{aid}" name="ckbox"/></td>'''.format(aid=a.id)
            if a.assets_type == "server":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">服务器</button></td>'''
            elif a.assets_type == "vmser":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">虚拟机</button></td>'''                   
            elif a.assets_type == "switch":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">交换机</button></td>'''                                
            elif a.assets_type == "route":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">路由器</button></td>'''                                          
            elif a.assets_type == "printer":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">打印机</button></td>'''
            elif a.assets_type == "scanner":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">扫描仪</button></td>'''                                             
            elif a.assets_type == "firewall":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">防火墙</button></td>'''                                           
            elif a.assets_type == "storage":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">存储设备</button></td>'''
            elif a.assets_type == "wifi":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">无线设备</button></td>''' 
            nks = ''
            if a.management_ip:
                liTags = ''
                for ns in a.networkcard_assets_set.all():
                    if ns.ip != 'unkown' and ns.ip !=  a.management_ip:
                        liTag = '''<li><span class="label label-success">内</span>:<code>{address}</code></li>'''.format(address=ns.ip) 
                        liTags = liTags + liTag
                nks = '''<ul class="list-unstyled">
                            <li><span class="label label-danger">外</span>:<code>{management_ip}</code></li>
                            {liTags}
                        </ul>'''.format(management_ip=a.management_ip,liTags=liTags)
            elif a.server_assets.ip:
                liTags = ''
                for ns in a.networkcard_assets_set.all():
                    if ns.ip != 'unkown' and ns.ip !=  a.server_assets.ip:
                        liTag = '''<li><span class="label label-success">内</span>:<code>{address}</code></li>'''.format(address=ns.ip) 
                        liTags = liTags + liTag
                nks = '''<ul class="list-unstyled">
                            <li><span class="label label-danger">外</span>:<code>{server_ip}</code></li>
                            {liTags}
                        </ul>'''.format(server_ip=a.server_assets.ip,liTags=liTags)
            management_ip = '''<td class="text-center">{ip}</td>'''.format(ip=nks)  
            name = '''<td class="text-center">{name}</td>'''.format(name=a.name)      
            model = '''<td class="text-center">{model}</td>'''.format(model=a.model)  
            for p in baseAssets.get('project'):
                if p.id == a.project:project = '''<td class="text-center">{project}</td>'''.format(project=p.project_name)                                      
            for s in baseAssets.get('service'):
                if s.id == a.business:service = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">{service}</button></td>'''.format(service=s.service_name)
            if a.status == 0:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-success">已上线</button></td>'''
            elif a.status == 1:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-primary">已下线</button></td>'''
            elif a.status == 2:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-warning">维修中</button></td>'''
            elif a.status == 3:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-info">已入库</button></td>'''
            elif a.status == 4:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-default">未使用</button></td>'''
            if a.buy_time:buy_time = '''<td class="text-center">{buy_time}</td>'''.format(buy_time=a.buy_time)
            else:buy_time = '''<td class="text-center">{buy_time}</td>'''.format(buy_time=str(a.create_date)[0:10])
            group ='''<td class="text-center">{groupname}</td>'''.format(groupname=Group.objects.get(id=a.group).name)
            for z in baseAssets.get('zone'):
                if z.id == a.put_zone:put_zone = '''<td class="text-center">{zone_name}</td>'''.format(zone_name=z.zone_name)
#                 else:put_zone = '''<td class="text-center">未知</td>'''
            try:
                if a.assets_type in ["server","vmser"]:
                    assets_type_div = '''
                                        <div class="btn-group">                
                                           <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                                                  <font class="glyphicon glyphicon-refresh"></font>
                                               <span class="caret"></span>
                                           </button>                                                                                            
                                             <ul class="dropdown-menu" role="menu">
                                                  <li>
                                                      <a href="javascript:" onclick='assetsUpdate(this,{server_assets_id},"{server_assets_ip}","setup")'>更新主体信息</a>
                                                  </li>        
                                                  <li>
                                                      <a href="javascript:" onclick='assetsUpdate(this,{server_assets_id},"{server_assets_ip}","crawHw")'>更新内存硬盘</a>
                                                  </li>                                         
                                             </ul>
                                        </div>'''.format(server_assets_id=a.server_assets.id,server_assets_ip=a.server_assets.ip)           
                else:
                    assets_type_div = ''' <div class="btn-group">                
                           <button type="button" class="btn btn-success dropdown-toggle disabled" data-toggle="dropdown">
                                  <font class="glyphicon glyphicon-refresh"></font>
                               <span class="caret"></span>
                           </button>                                                                                            
                        </div>'''         
            except:
                pass             
            opt = '''
                <td class="text-center">
                     <a href="/assets_view/{id}" style="text-decoration:none;"><button  type="button" class="btn btn-default"><abbr title="查看详细信息"><i class="glyphicon glyphicon-info-sign"></i></abbr></button></a>
                     {assets_type_div}
                     <a href="/assets_mod/{id}" style="text-decoration:none;"><button  type="button" class="btn btn-default"><abbr title="修改资料"><i class="glyphicon glyphicon-edit"></button></i></abbr></a>
                     <button  type="button" class="btn btn-default" onclick="deleteAssets(this,{id})"><i class="glyphicon glyphicon-trash"></i></button>
                 </td>'''.format(id=a.id,assets_type_div=assets_type_div)
            dataList.append([assets_id,assets_type,management_ip,name,model,put_zone,project,service,group,buy_time,status,opt])                                                                                                                                                                                          
        return JsonResponse({'msg':"数据查询成功","code":200,'data':dataList,'count':0})     
    
@login_required(login_url='/login')  
def assets_log(request,page):
    if request.method == "GET":
        allAssetsList = Log_Assets.objects.all().order_by('-id')[0:1000]
        paginator = Paginator(allAssetsList, 25)          
        try:
            assetsList = paginator.page(page)
        except PageNotAnInteger:
            assetsList = paginator.page(1)
        except EmptyPage:
            assetsList = paginator.page(paginator.num_pages)        
        return render(request,'assets/assets_log.html',{"user":request.user,"assetsList":assetsList})
    
    
@login_required(login_url='/login')
@permission_required('OpsManage.can_change_assets',login_url='/noperm/')
def assets_batch(request):
    if request.method == "POST":
        fList = []
        sList = []
        resource = []
        serList = []
        if request.POST.get('model') == 'update':
            for ast in request.POST.getlist('assetsIds[]'):
                try:
                    assets = Assets.objects.get(id=int(ast))
                except Exception, ex:
                    logger.warn(msg="批量更新获取资产失败: {ex}".format(ex=str(ex)))
                    continue
                if assets.assets_type in ['vmser','server']:
                    try:
                        server_assets = Server_Assets.objects.get(assets=assets)
                    except Exception, ex:
                        logger.warn(msg="批量更新获取服务器资产失败: {ex}".format(ex=str(ex)))
                        if server_assets.ip not in fList:fList.append(server_assets.ip) 
                        continue
                    serList.append(server_assets.ip)
                    if server_assets.keyfile == 1:resource.append({"hostname": server_assets.ip, "port": int(server_assets.port),"username": server_assets.username})
                    else:resource.append({"hostname": server_assets.ip, "port": server_assets.port,"username": server_assets.username, "password": server_assets.passwd})                    
            ANS = ANSRunner(resource)
            ANS.run_model(host_list=serList,module_name='setup',module_args="")
            data = ANS.handle_cmdb_data(ANS.get_model_result())    
            if data:
                for ds in data:
                    status = ds.get('status')
                    sip = ds.get('ip') 
                    if status == 0:
                        assets = Server_Assets.objects.get(ip=ds.get('ip')).assets
                        assets.model = ds.get('model')
                        assets.save()
                        try:
                            Server_Assets.objects.filter(ip=ds.get('ip')).update(cpu_number=ds.get('cpu_number'),kernel=ds.get('kernel'),
                                                                                  selinux=ds.get('selinux'),hostname=ds.get('hostname'),
                                                                                  system=ds.get('system'),cpu=ds.get('cpu'),
                                                                                  disk_total=ds.get('disk_total'),cpu_core=ds.get('cpu_core'),
                                                                                  swap=ds.get('swap'),ram_total=ds.get('ram_total'),
                                                                                  vcpu_number=ds.get('vcpu_number')
                                                                                  )
                            if sip not in sList:sList.append(sip)
                        except Exception:
                            if sip not in fList:fList.append(sip) 
                        for nk in ds.get('nks'):
                            macaddress = nk.get('macaddress')
                            count = NetworkCard_Assets.objects.filter(assets=assets,macaddress=macaddress).count()
                            if count > 0:
                                try:
                                    NetworkCard_Assets.objects.filter(assets=assets,macaddress=macaddress).update(assets=assets,device=nk.get('device'),
                                                                                                                       ip=nk.get('address'),module=nk.get('module'),
                                                                                                                       mtu=nk.get('mtu'),active=nk.get('active'))
                                except Exception, ex:
                                    logger.warn(msg="批量更新更新服务器网卡资产失败: {ex}".format(ex=str(ex)))
                            else:
                                try:
                                    NetworkCard_Assets.objects.create(assets=assets,device=nk.get('device'),
                                                                  macaddress=nk.get('macaddress'),
                                                                  ip=nk.get('address'),module=nk.get('module'),
                                                                  mtu=nk.get('mtu'),active=nk.get('active'))
                                except Exception, ex:
                                    logger.warn(msg="批量更新写入服务器网卡资产失败: {ex}".format(ex=str(ex)))                         
                    else:
                        if sip not in fList:fList.append(sip) 
                                                         
            if sList:
                return JsonResponse({'msg':"数据更新成功","code":200,'data':{"success":sList,"failed":fList}}) 
            else:return JsonResponse({'msg':"数据更新失败","code":500,'data':{"success":sList,"failed":fList}}) 
            
        elif request.POST.get('model') == 'delete':
            for ast in request.POST.getlist('assetsIds[]'):
                try:
                    assets = Assets.objects.get(id=int(ast))
                except Exception, ex:
                    print ex
                    continue
                if assets.assets_type in ['vmser','server']:
                    try:
                        server_assets = Server_Assets.objects.get(assets=assets)
                    except Exception, ex:
                        fList.append(assets.management_ip)
                        assets.delete() 
                        continue   
                    sList.append(server_assets.ip)
                    server_assets.delete()                    
                else:
                    try:
                        net_assets = Network_Assets.objects.get(assets=assets)
                    except Exception, ex:
                        fList.append(assets.management_ip)
                        assets.delete() 
                        continue  
                    sList.append(assets.management_ip)
                    net_assets.delete()                    
                assets.delete()                                    
            return JsonResponse({'msg':"数据更新成功","code":200,'data':{"success":sList,"failed":fList}}) 
        else:
            return JsonResponse({'msg':"操作失败","code":500,'data':"不支持的操作"})    
        
@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/')
def assets_server(request):
    if request.method == "POST":
        if request.POST.get('query') in ['service','project','group']:
            dataList = []
            if request.POST.get('query') == 'service':
                for ser in Assets.objects.filter(business=request.POST.get('id')):
                    dataList.append({"id":ser.server_assets.id,"ip":ser.server_assets.ip})
            elif request.POST.get('query') == 'group':
                for ser in Assets.objects.filter(group=request.POST.get('id')):
                    dataList.append({"id":ser.server_assets.id,"ip":ser.server_assets.ip})                
            return JsonResponse({'msg':"主机查询成功","code":200,'data':dataList})  
        else:JsonResponse({'msg':"不支持的操作","code":500,'data':[]})  
    else:
        return JsonResponse({'msg':"操作失败","code":500,'data':"不支持的操作"})    
    
    
@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/')    
def assets_groups(request,id):
    try:
        project = Project_Assets.objects.get(id=id)
    except Project_Assets.DoesNotExist:
        return render(request,'assets/assets_groups.html',{"user":request.user,"errorInfo":"项目不存在"})
    serviceList = Service_Assets.objects.filter(project=project)
    for ds in serviceList:
        dataList = []
        for ser in Assets.objects.select_related().filter(business=ds.id):
            if ser.server_assets.ram_total: ser.server_assets.ram_total =  str(int(ser.server_assets.ram_total) / 1024) + 'GB'
            else:ser.server_assets.ram_total = '0GB'
            if ser.server_assets.disk_total: 
                disk_total =  int(ser.server_assets.disk_total) / 1024 / 1024
                if disk_total > 1:ser.server_assets.disk_total = str(int(ser.server_assets.disk_total) / 1024 / 1024) + 'TB'
                else:ser.server_assets.disk_total =  str(int(ser.server_assets.disk_total) / 1024) +  'GB'
            else:ser.server_assets.disk_total = '0GB'
            dataList.append(ser)
            ds.host = dataList
    totalServer = Assets.objects.filter(project=id).count()
    return render(request,'assets/assets_groups.html',{"user":request.user,"project":project,
                                                       "serviceList":serviceList,"totalServer":totalServer})    
    