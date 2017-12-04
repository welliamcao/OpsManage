#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import os,xlrd,json
from django.http import JsonResponse
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from OpsManage.models import *
from django.db.models import Count
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.contrib.auth.models import Group
from OpsManage.tasks import recordAssets
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    return {"group":groupList,"service":serviceList,"zone":zoneList,
            "line":lineList,"raid":raidList}

@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_config(request):
    return render(request,'assets/assets_config.html',{"user":request.user,"baseAssets":getBaseAssets()},
                              )
    
@login_required(login_url='/login')
@permission_required('OpsManage.can_add_assets',login_url='/noperm/') 
def assets_add(request):
    if request.method == "GET":
        return render(request,'assets/assets_add.html',{"user":request.user,"baseAssets":getBaseAssets()},
                                  )      
    
@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_list(request):
    assetsList = Assets.objects.all().order_by("-id") 
    assetOnline = Assets.objects.filter(status=0).count()
    assetOffline = Assets.objects.filter(status=1).count()
    assetMaintain = Assets.objects.filter(status=2).count()
    assetsNumber = Assets.objects.values('assets_type').annotate(dcount=Count('assets_type'))
    return render(request,'assets/assets_list.html',{"user":request.user,"totalAssets":assetsList.count(),
                                                         "assetOnline":assetOnline,"assetOffline":assetOffline,
                                                         "assetMaintain":assetMaintain,"baseAssets":getBaseAssets(),
                                                         "assetsList":assetsList,"assetsNumber":assetsNumber},
                              )

@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_view(request,aid): 
    try:
        assets = Assets.objects.get(id=aid)
    except:
        return render(request,'404.html',{"user":request.user},
                                )  
    if assets.assets_type == 'server':
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
        except:
            return render(request,'assets/assets_view.html',{"user":request.user},
                            ) 
        return render(request,'assets/assets_view.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "asset_ram":asset_ram,"asset_disk":asset_disk,
                                                            "baseAssets":getBaseAssets()},
                            )   
    else:
        try:
            asset_body = assets.network_assets
        except:
            return render(request,'assets/assets_view.html',{"user":request.user},
                            )                 
        return render(request,'assets/assets_view.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "baseAssets":getBaseAssets()},
                            )  
             
@login_required(login_url='/login')
@permission_required('OpsManage.can_change_assets',login_url='/noperm/') 
def assets_modf(request,aid):  
    try:
        assets = Assets.objects.get(id=aid)
    except:
        return render(request,'assets/assets_modf.html',{"user":request.user},
                                )  
    if assets.assets_type == 'server':
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
        except:
            return render(request,'404.html',{"user":request.user},
                            )         
        return render(request,'assets/assets_modf.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "asset_ram":asset_ram,"asset_disk":asset_disk,
                                                            "assets_data":getBaseAssets()},
                            )    
    else:     
        try:
            asset_body = assets.network_assets
        except:
            return render(request,'assets/assets_modf.html',{"user":request.user},   
                                      )                                                 
        return render(request,'assets/assets_modf.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "assets_data":getBaseAssets()},
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
                if server_assets.keyfile == 1:resource = [{"hostname": server_assets.ip, "port": int(server_assets.port)}] 
                else:resource = [{"hostname": server_assets.ip, "port": server_assets.port,"username": server_assets.username, "password": server_assets.passwd}]
            except Exception,e:
                return  JsonResponse({'msg':"数据更新失败-查询不到该主机资料~","code":502})
            ANS = ANSRunner(resource)
            ANS.run_model(host_list=[server_assets.ip],module_name='setup',module_args="")
            data = ANS.handle_cmdb_data(ANS.get_model_result())
            if data:
                for ds in data:
                    status = ds.get('status')
                    if status == 0:
                        try:
                            Assets.objects.filter(id=server_assets.assets_id).update(sn=ds.get('serial'),model=ds.get('model'),
                                                                                     manufacturer=ds.get('manufacturer'))
                        except Exception,e:
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
                        except Exception,e:
                            print e
                            return JsonResponse({'msg':"数据更新失败-写入数据失败","code":400})
                    else:
                        return JsonResponse({'msg':"数据更新失败-无法链接主机~","code":502})                    
                return JsonResponse({'msg':"数据更新成功","code":200})
            else:
                return JsonResponse({'msg':"数据更新失败-请检查Ansible配置","code":400})

        elif genre == 'crawHw':
            try:
                server_assets = Server_Assets.objects.get(id=server_id)
                assets = Assets.objects.get(id=server_assets.assets_id)
                if server_assets.keyfile == 1:resource = [{"hostname": server_assets.ip, "port": int(server_assets.port)}] 
                else:resource = [{"hostname": server_assets.ip, "port": server_assets.port,"username": server_assets.username, "password": server_assets.passwd}]
            except Exception,e:
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
        
                                except Exception,e:
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
                print e
                return []
            return dataList 
        dataList = getAssetsData(fname=filename)
        #获取服务器列表
        for s in dataList:
            try:
                count = Assets.objects.filter(name=s[1]).count()
                if count == 1:
                    assets = Assets.objects.get(name=s[1])
                    Assets.objects.filter(name=s[1]).update(
                                                            assets_type = s[0],
                                                            sn = s[2],
                                                            buy_time = xlrd.xldate.xldate_as_datetime(s[3],0),
                                                            expire_date = xlrd.xldate.xldate_as_datetime(s[4],0),
                                                            buy_user = s[5],
                                                            management_ip = s[6],
                                                            manufacturer = s[7],
                                                            model = s[8],
                                                            provider = s[9],
                                                            status = s[10],
                                                            put_zone = s[11],
                                                            group = s[12],
                                                            business = s[13]
                                                            )
                    if s[0] == 'server':
                        Server_Assets.objects.filter(assets=assets).update(
                                                                           ip = s[14],
                                                                           keyfile = s[15],
                                                                           username = s[16],
                                                                           passwd = str(s[17]),
                                                                           hostname = s[18],
                                                                           port = s[19],
                                                                           raid = s[20],
                                                                           line = s[21],
                                                                           )
                    elif s[0] in ['switch','route','printer','scanner','firewall','storage','wifi']:
                        Network_Assets.objects.filter(assets=assets).update(
                                                                            ip = s[14],
                                                                            bandwidth = s[15],
                                                                            port_number = s[16],
                                                                            firmware = s[17],
                                                                            cpu = s[18],
                                                                            stone = s[19],
                                                                            configure_detail = s[20]
                                                                            )
                else:
                    assets = Assets.objects.create(
                                                    assets_type = s[0],
                                                    name = s[1],
                                                    sn = s[2],
                                                    buy_time = xlrd.xldate.xldate_as_datetime(s[3],0),
                                                    expire_date = xlrd.xldate.xldate_as_datetime(s[4],0),
                                                    buy_user = s[5],
                                                    management_ip = s[6],
                                                    manufacturer = s[7],
                                                    model = s[8],
                                                    provider = s[9],
                                                    status = s[10],
                                                    put_zone = s[11],
                                                    group = s[12],
                                                    business = s[13]
                                                    )     
                    if s[0] == 'server':
                        Server_Assets.objects.create(
                                                        assets=assets,
                                                        ip = s[14],
                                                        keyfile = s[15],
                                                        username = s[16],
                                                        passwd = str(s[17]),
                                                        hostname = s[18],
                                                        port = s[19],
                                                        raid = s[20],
                                                        line = s[21],
                                                    )
                    elif s[0] in ['switch','route','printer','scanner','firewall','storage','wifi']:
                        Network_Assets.objects.create(
                                                        assets=assets,
                                                        ip = s[14],
                                                        bandwidth = s[15],
                                                        port_number = s[16],
                                                        firmware = s[17],
                                                        cpu = s[18],
                                                        stone = s[19],
                                                        configure_detail = s[20]
                                                     )                                           
            except Exception,e:
                print e
                pass
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
        buyUserList = [  m.buy_user for m in Assets.objects.raw('SELECT id,buy_user from opsmanage_assets WHERE buy_user is not null GROUP BY buy_user')]
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
        data = dict()
        #格式化查询条件
        for (k,v)  in request.POST.items() :
            if v is not None and v != u'' :
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
        server = False                                                                               
        if len(AssetIntersection) > 0 and len(ServerAssetIntersection) > 0:
            assetsData = dict()
            for a in AssetIntersection:
                for k in data.keys():
                    if k.find(a) != -1:
                        assetsData[k] = data[k]
                        data.pop(k)
            serverList = [ a.assets_id for a in Server_Assets.objects.filter(**data) ]
            assetsData['id__in'] = serverList
            serverList = Assets.objects.filter(**assetsData)             

            
        elif len(AssetIntersection) > 0 and len(ServerAssetIntersection) == 0:
            serverList = Assets.objects.filter(**data) 
            
        elif len(AssetIntersection) == 0 and len(ServerAssetIntersection) > 0:
            server = True
            serverList = Server_Assets.objects.filter(**data) 
        baseAssets = getBaseAssets()
        dataList = []
        for a in serverList:
            if server:a = a.assets
            if a.assets_type == "server":
                assets_type = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">服务器</button></td>'''
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
            management_ip = '''<td class="text-center">{ip}</td>'''.format(ip=a.management_ip)   
            name = '''<td class="text-center">{name}</td>'''.format(name=a.name)      
            model = '''<td class="text-center">{model}</td>'''.format(model=a.model)                                        
            for s in baseAssets.get('service'):
                if s.id == a.business:service = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">{service}</button></td>'''.format(service=s.service_name)
#                 else:service = '''<td class="text-center"><button  type="button" class="btn btn-default disabled">未知</button></td>'''
            if a.status == 0:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-success">已上线</button></td>'''
            elif a.status == 1:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-primary">已下线</button></td>'''
            elif a.status == 2:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-warning">维修中</button></td>'''
            elif a.status == 3:status = '''<td class="text-center"><button  type="button" class="btn btn-outline btn-info">已入库</button></td>'''
            elif a.status == 4:status = '''<td class="text-center">button  type="button" class="btn btn-outline btn-default">未使用</button></td>'''
            buy_user = '''<td class="text-center">{buy_user}</td>'''.format(buy_user=a.buy_user)
            buy_time ='''<td class="text-center">{buy_time}</td>'''.format(buy_time=a.buy_time)
            for z in baseAssets.get('zone'):
                if z.id == a.put_zone:put_zone = '''<td class="text-center">{zone_name}</td>'''.format(zone_name=z.zone_name)
#                 else:put_zone = '''<td class="text-center">未知</td>'''
            try:
                if a.assets_type == "server":
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
            dataList.append([assets_type,management_ip,name,model,put_zone,buy_user,buy_time,service,status,opt])                                                                                                                                                                                          
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
        return render(request,'assets/assets_log.html',{"user":request.user,"assetsList":assetsList},
                                  )