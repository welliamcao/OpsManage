#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from OpsManage.models import *
from django.db.models import Count
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.contrib.auth.models import Group
from OpsManage.tasks import recordAssets
from django.contrib.auth.decorators import permission_required

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
    return render_to_response('assets/assets_config.html',{"user":request.user,"baseAssets":getBaseAssets()},
                              context_instance=RequestContext(request))
    
@login_required(login_url='/login')
@permission_required('OpsManage.can_add_assets',login_url='/noperm/') 
def assets_add(request):
    if request.method == "GET":
        return render_to_response('assets/assets_add.html',{"user":request.user,"baseAssets":getBaseAssets()},
                                  context_instance=RequestContext(request))      
    
@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_list(request):
    assetsList = Assets.objects.all().order_by("-id") 
    assetOnline = Assets.objects.filter(status=0).count()
    assetOffline = Assets.objects.filter(status=1).count()
    assetMaintain = Assets.objects.filter(status=2).count()
    assetsNumber = Assets.objects.values('assets_type').annotate(dcount=Count('assets_type'))
    return render_to_response('assets/assets_list.html',{"user":request.user,"totalAssets":assetsList.count(),
                                                         "assetOnline":assetOnline,"assetOffline":assetOffline,
                                                         "assetMaintain":assetMaintain,"baseAssets":getBaseAssets(),
                                                         "assetsList":assetsList,"assetsNumber":assetsNumber},
                              context_instance=RequestContext(request))

@login_required(login_url='/login')
@permission_required('OpsManage.can_read_assets',login_url='/noperm/') 
def assets_view(request,aid): 
    try:
        assets = Assets.objects.get(id=aid)
    except:
        return render_to_response('404.html',{"user":request.user},
                                context_instance=RequestContext(request))  
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
            return render_to_response('assets/assets_view.html',{"user":request.user},
                            context_instance=RequestContext(request)) 
        return render_to_response('assets/assets_view.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "asset_ram":asset_ram,"asset_disk":asset_disk,
                                                            "baseAssets":getBaseAssets()},
                            context_instance=RequestContext(request))   
    else:
        try:
            asset_body = assets.network_assets
        except:
            return render_to_response('assets/assets_view.html',{"user":request.user},
                            context_instance=RequestContext(request))                 
        return render_to_response('assets/assets_view.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "baseAssets":getBaseAssets()},
                            context_instance=RequestContext(request))  
             
@login_required(login_url='/login')
@permission_required('OpsManage.can_change_assets',login_url='/noperm/') 
def assets_modf(request,aid):  
    try:
        assets = Assets.objects.get(id=aid)
    except:
        return render_to_response('assets/assets_modf.html',{"user":request.user},
                                context_instance=RequestContext(request))  
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
            return render_to_response('404.html',{"user":request.user},
                            context_instance=RequestContext(request))         
        return render_to_response('assets/assets_modf.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "asset_ram":asset_ram,"asset_disk":asset_disk,
                                                            "assets_data":getBaseAssets()},
                            context_instance=RequestContext(request))    
    else:     
        try:
            asset_body = assets.network_assets
        except:
            return render_to_response('assets/assets_modf.html',{"user":request.user},   
                                      context_instance=RequestContext(request))                                                 
        return render_to_response('assets/assets_modf.html',{"user":request.user,"asset_type":assets.assets_type,
                                                            "asset_main":assets,"asset_body":asset_body,
                                                            "assets_data":getBaseAssets()},
                            context_instance=RequestContext(request))  
        
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
def assets_log(request):
    if request.method == "GET":
        assetsList = Log_Assets.objects.all().order_by('-id')[0:120]
        return render_to_response('assets/assets_log.html',{"user":request.user,"assetsList":assetsList},
                                  context_instance=RequestContext(request))