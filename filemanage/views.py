#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import json,uuid,os
from django.shortcuts import render
from OpsManage.data.DsRedisOps import DsRedis
from OpsManage.utils.ansible_api_v2 import ANSRunner
from django.http import JsonResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from orders.models import Order_System
from OpsManage.utils import base
from dao.assets import AssetsSource
from filemanage.models import FileUpload_Audit_Order,UploadFiles

@login_required()
@permission_required('filemanage.can_add_fileupload_audit_order',login_url='/noperm/')
def file_upload_run(request,id):
    if request.method == "GET":
        uploadfilesList = []
        try:
            order = Order_System.objects.get(id=id,order_type=2)
        except Exception,ex:
            return render(request,'filemanage/file_upload_run.html',{"user":request.user,"errInfo":ex})
        order.fileupload_audit_order.dest_server = json.loads(order.fileupload_audit_order.dest_server)
        for ds in UploadFiles.objects.filter(file_order=order.fileupload_audit_order):
            ds.file_path = str(ds.file_path).replace('file/upload/','')
            uploadfilesList.append(ds)
        return render(request,'filemanage/file_upload_run.html',{"user":request.user,"order":order,
                                                                 "uploadfilesList":uploadfilesList,
                                                                 "ans_uuid":uuid.uuid4()}) 
    elif request.method == "POST":
        try:
            order = Order_System.objects.get(id=id,order_type=2)
        except Exception,ex:
            return JsonResponse({'msg':ex,"code":500,'data':[]})  
        if request.user.is_superuser or request.user.id in [order.order_executor,order.order_user]:
            sList,resource = AssetsSource().queryAssetsByIp(ipList=request.POST.getlist('dest_server'))
            if len(sList) > 0 and order.order_status == 8:
                redisKey = request.POST.get('ans_uuid')
                DsRedis.OpsAnsibleModel.delete(redisKey)
                ANS = ANSRunner(resource,redisKey)       
                DsRedis.OpsAnsibleModel.lpush(redisKey, "[Start] file distribution".format(model='copy',args=request.POST.get('ansible_args',"None")))     
                for files in request.POST.getlist('file_path'):
                    file = UploadFiles.objects.get(id=files)     
                    filePath = os.getcwd() + '/upload/' + str(file.file_path)        
                    module_args = "src={src} dest={dest} mode={chown_rwx} owner={chown_user} group={chown_user} backup={backup}".format(src=filePath,backup=request.POST.get('backup','yes'),
                                                                                                                                   dest=order.fileupload_audit_order.dest_path,
                                                                                                                                   chown_user=order.fileupload_audit_order.chown_user,
                                                                                                                                   chown_rwx=order.fileupload_audit_order.chown_rwx
                                                                                                               )
                    ANS.run_model(host_list=sList,module_name='copy',module_args=module_args)
                DsRedis.OpsAnsibleModel.lpush(redisKey, "[Done] Ansible Done.")
                return JsonResponse({'msg':"操作成功","code":200,'data':[]})
            else:
                return JsonResponse({'msg':"操作失败，未选择主机或者该分组没有成员","code":500,'data':[]})
        else:
            return JsonResponse({'msg':"操作失败，您没有权限进行操作","code":500,'data':[]})
    else:
        return JsonResponse({'msg':"操作失败，不支持的操作类型","code":500,'data':[]})   
    
    
@login_required()
@permission_required('filemanage.can_add_fileupload_audit_order',login_url='/noperm/')
def file_download_run(request,id):
    if request.method == "GET":
        try:
            order = Order_System.objects.get(id=id,order_type=3)
        except Exception,ex:
            return render(request,'filemanage/file_download_run.html',{"user":request.user,"errInfo":ex})
        order.filedownload_audit_order.dest_server = json.loads(order.filedownload_audit_order.dest_server)
        return render(request,'filemanage/file_download_run.html',{"user":request.user,"order":order,
                                                                 "ans_uuid":uuid.uuid4()}) 
    elif request.method == "POST":
        try:
            order = Order_System.objects.get(id=id,order_type=3)
        except Exception,ex:
            return JsonResponse({'msg':ex,"code":500,'data':[]})  
        if request.user.is_superuser or request.user.id in [order.order_executor,order.order_user]:
            sList,resource = AssetsSource().queryAssetsByIp(ipList=request.POST.getlist('dest_server'))
            dataList = []
            if len(sList) > 0 and order.order_status == 8:
                ANS = ANSRunner(resource)                
                module_args = "paths={dest}".format( dest=order.filedownload_audit_order.dest_path)
                ANS.run_model(host_list=sList,module_name='find',module_args=module_args)
                filesData = json.loads(ANS.get_model_result())
                for k,v in filesData.get('success').items():
                    for ds in v.get('files'):
                        data = {}
                        data["id"] = order.id
                        data['host'] = k
                        data['path'] = ds.get('path')
                        data['size'] = ds.get('size')/1024/1024
                        data['islnk'] = ds.get('islnk')
                        dataList.append(data)
                return JsonResponse({'msg':"操作成功","code":200,'data':dataList})
            else:
                return JsonResponse({'msg':"操作失败，未选择主机或者该分组没有成员","code":500,'data':[]})
        else:
            return JsonResponse({'msg':"操作失败，您没有权限进行操作","code":500,'data':[]})
    else:
        return JsonResponse({'msg':"操作失败，不支持的操作类型","code":500,'data':[]})            


@login_required()
@permission_required('filemanage.can_add_fileupload_audit_order',login_url='/noperm/')
def file_downloads(request):
    if request.method == "POST":
        try:
            order = Order_System.objects.get(id=request.POST.get('id',0),order_type=3)
        except Exception,ex:
            return JsonResponse({'msg':ex,"code":500,'data':[]})
        if request.user.is_superuser or request.user.id in [order.order_executor,order.order_user]:
            sList,resource = AssetsSource().queryAssetsByIp(ipList=request.POST.getlist('dest_server'))
            if len(sList) > 0 and order.order_status == 8:
                ANS = ANSRunner(resource)           
                dest = os.getcwd() + '/upload/file/download/' 
                module_args = "src={src} dest={dest}".format(src=request.POST.get('path'),dest=dest)
                ANS.run_model(host_list=sList,module_name='fetch',module_args=module_args)
                filesData = json.loads(ANS.get_model_result())
                filePath = filesData.get('success').get(request.POST.get('dest_server')).get('dest')
                if filePath:
                    response = StreamingHttpResponse(base.file_iterator(filePath))
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = 'attachment; filename="{file_name}'.format(file_name=os.path.basename(filePath))
                    return response    
            else:
                return JsonResponse({'msg':"操作失败，未选择主机或者该分组没有成员","code":500,'data':[]})                                  
        else:
            return JsonResponse({'msg':"操作失败，您没有权限进行操作","code":500,'data':[]})
    else:
        return JsonResponse({'msg':"操作失败，不支持的操作类型","code":500,'data':[]})          