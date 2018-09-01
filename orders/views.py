#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import json,os
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from OpsManage.models import (Project_Assets,Project_Config,Project_Number,
                              Service_Assets,DataBase_Server_Config,SQL_Audit_Control,
    Server_Assets)
from .models import Order_System,Project_Order,SQL_Audit_Order
from django.db.models import Q 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from OpsManage.utils.logger import logger
from OpsManage.utils import base
from OpsManage.utils.git import GitTools
from OpsManage.utils.svn import SvnTools
from django.contrib.auth.models import User,Group
from OpsManage.tasks.sql import sendOrderNotice
from OpsManage.utils.inception import Inception
from dao.order import Order
from dao.assets import AssetsSource
from filemanage.models import FileUpload_Audit_Order,UploadFiles,FileDownload_Audit_Order

@login_required()
@permission_required('orders.can_add_project_order',login_url='/noperm/')
def deploy_ask(request):
    deployList = Project_Config.objects.filter(project_env='uat')
    for ds in deployList:
        ds.number = Project_Number.objects.filter(project=ds)
    return render(request,'orders/deploy_list.html',{"user":request.user,"deployList":deployList}) 

@login_required()
@permission_required('orders.can_add_project_order',login_url='/noperm/')
def deploy_apply(request,pid):
    try:
        project = Project_Config.objects.get(id=pid)
        if project.project_repertory == 'git':version = GitTools()
        elif project.project_repertory == 'svn':version = SvnTools()
    except:
        return render(request,'orders/deploy_apply.html',{"user":request.user,
                                                         "errorInfo":"项目不存在，可能已经被删除."}, 
                                  )     
    if request.method == "GET":
        vList = None
        version.pull(path=project.project_repo_dir)
        if project.project_model == "branch" or project.project_repertory == 'svn':
            #获取最新版本
            bList = version.branch(path=project.project_repo_dir) 
            vList = version.log(path=project.project_repo_dir, number=50)
        elif project.project_model == "tag":
            bList = version.tag(path=project.project_repo_dir) 
        audit_group = Group.objects.get(id=project.project_audit_group)
        userList = [ u for u in audit_group.user_set.values()]
        return render(request,'orders/deploy_apply.html',{"user":request.user,"project":project,
                                                         "userList":userList,"bList":bList,"vList":vList}, 
                                  )  
    elif request.method == "POST":       
        try:      
            order = Order_System.objects.create(
                                                order_user = request.user.id,
                                                order_subject = request.POST.get('order_subject'),
                                                order_executor = request.POST.get('order_audit'),
                                                order_status = request.POST.get('order_status',2),
                                                order_level = request.POST.get('order_level'),
                                                order_type =  1,
                                            )
        except Exception,ex:
            logger.error(msg="项目部署申请失败: {ex}".format(ex=str(ex)))
            return render(request,'orders/deploy_apply.html',{"user":request.user,"errorInfo":"项目部署申请失败：%s" % str(ex)},)    
        try:
            Project_Order.objects.create(
                                         order = order,
                                         order_project = project,
                                         order_content = request.POST.get('order_content'),
                                         order_branch = request.POST.get('order_branch',None),
                                         order_comid = request.POST.get('order_comid',None),
                                         order_tag  = request.POST.get('order_tag',None)                                         
                                         )
        except Exception,ex:      
            logger.error(msg="项目部署申请失败: {ex}".format(ex=str(ex)))
            return render(request,'orders/deploy_apply.html',{"user":request.user,"errorInfo":"项目部署申请失败：%s" % str(ex)},)                 
        sendOrderNotice.delay(order_id=order.id,mask='【申请中】')
        return HttpResponseRedirect('/order/deploy/apply/{id}/'.format(id=pid))  


@login_required()
@permission_required('orders.can_read_sql_audit_order',login_url='/noperm/')
def db_sqlorder_audit(request):
    try:
        config = SQL_Audit_Control.objects.get(id=1)  
    except:
        return render(request,'orders/db_sqlorder_audit.html',{"user":request.user,"errinfo":"请先在数据管理-基础配置-SQL工单审核配置，做好相关配置。"})
    if request.method == "GET":
        try:
            try:
                audit_group = []
                for g in json.loads(config.audit_group):
                    audit_group.append(int(g)) 
            except:
                audit_group = []   
            userList = User.objects.filter(groups__in=audit_group)    
            dataBaseList = DataBase_Server_Config.objects.all()
            serviceList = Service_Assets.objects.all()
            projectList = Project_Assets.objects.all()
        except Exception, ex:
            logger.warn(msg="获取SQL审核配置信息失败: {ex}".format(ex=str(ex)))
        return render(request,'orders/db_sqlorder_audit.html',{"user":request.user,"dataBaseList":dataBaseList,"userList":userList,
                                                                 "serviceList":serviceList,"projectList":projectList})
    elif request.method == "POST":
        if request.POST.get('type') == 'audit':
            dbId = request.POST.get('order_db')
            if Order_System.objects.filter(order_subject=request.POST.get('order_desc'),order_type=0).count() > 0:
                return  JsonResponse({'msg':"审核失败，工单（{desc}）已经存在".format(desc=request.POST.get('order_desc')),"code":500,'data':[]})
            try:
                db = DataBase_Server_Config.objects.get(id=int(dbId))
            except Exception,ex:
                logger.error(msg="获取数据库配置信息失败: {ex}".format(ex=str(ex)))
                return JsonResponse({'msg':str(ex),"code":500,'data':[]})
            if request.POST.get('order_type') == 'online':
                try:
                    incept = Inception(
                                       host=db.db_host,name=db.db_name,
                                       user=db.db_user,passwd=db.db_passwd,
                                       port=db.db_port
                                       )
                    result = incept.checkSql(request.POST.get('order_sql'))
                    if result.get('status') == 'success':
                        count = 0
                        sList = []
                        for ds in result.get('data'):
                            if ds.get('errlevel') > 0 and ds.get('errmsg'):count = count + 1
                            sList.append({'sql':ds.get('sql'),'row':ds.get('affected_rows'),'errmsg':ds.get('errmsg')})
                        if count > 0:return JsonResponse({'msg':"审核失败，请检查SQL语句","code":500,'data':sList})
                        else:
                            mask='【已自动授权】'
                            if config.t_auto_audit == 1 and db.db_env == 'test':order_status = 8
                            elif config.p_auto_audit == 1 and db.db_env == 'prod':order_status = 8
                            else:
                                order_status = 4
                                mask='【申请中】'
                            try:
                                order_executor = User.objects.get(id=request.POST.get('order_executor'))
                                order = Order_System.objects.create(
                                                           order_user=request.user.id,
                                                           order_subject = request.POST.get('order_desc'),
                                                           order_level = 0,
                                                           order_executor = order_executor.id,
                                                           order_status = order_status,
                                                           order_type = 0
                                                           )  
                                sendOrderNotice.delay(order.id,mask)                          
                            except Exception, ex:
                                logger.error(msg="SQL审核失败: {ex}".format(ex=str(ex)))
                                return JsonResponse({'msg':str(ex),"code":500,'data':[]})
                            try:
                                SQL_Audit_Order.objects.create(
                                                               order = order,
                                                               order_db = db,   
                                                               order_type = 'online',                                                            
                                                               order_sql = request.POST.get('order_sql')
                                                               )
                            except Exception, ex:
                                logger.error(msg="SQL审核失败: {ex}".format(ex=str(ex)))
                                return JsonResponse({'msg':str(ex),"code":500,'data':[]})                               
                            return JsonResponse({'msg':"审核成功，SQL已经提交","code":200,'data':sList})
                    else:
                        return JsonResponse({'msg':result.get('errinfo'),"code":500,'data':[]}) 
                except Exception, ex:
                    return JsonResponse({'msg':str(ex),"code":200,'data':[]})     
            elif request.POST.get('order_type') == 'file':
                try:
                    order_executor = User.objects.get(id=request.POST.get('order_executor'))  
                    order = Order_System.objects.create(
                                               order_user=request.user.id,
                                               order_subject = request.POST.get('order_desc'),
                                               order_level = 0,
                                               order_executor = order_executor.id,
                                               order_status = 4,
                                               order_type = 0
                                               )                          
                except Exception, ex:
                    logger.error(msg="SQL文件审核失败: {ex}".format(ex=str(ex)))
                    return JsonResponse({'msg':str(ex),"code":500,'data':[]})                 
                try:                                  
                    SQL_Audit_Order.objects.create(
                                                    order = order,
                                                    order_db = db,
                                                    order_type = 'file',  
                                                    order_sql = request.POST.get('order_sql'),
                                                    order_file = request.FILES.get('order_file'),
                                                )  
                    sendOrderNotice.delay(order.id,mask='【申请中】')                          
                except Exception, ex:
                    logger.error(msg="SQL文件审核失败: {ex}".format(ex=str(ex)))
                    return JsonResponse({'msg':str(ex),"code":500,'data':[]})
                return JsonResponse({'msg':"SQL工单已经提交","code":200,'data':[]})  


@login_required()
@permission_required('orders.can_read_order_system',login_url='/noperm/')
def order_list(request,page):
    if request.method == "GET":
        if request.user.is_superuser:
            orderList = Order_System.objects.all().order_by("-id")[0:1000]
        else:
            orderList = Order_System.objects.filter(Q(order_user=request.user.id) | Q(order_executor=request.user.id)).order_by("-id")[0:1000]
        for ds in orderList:
            try:
                if ds.order_executor == request.user.id:ds.perm = 1
                ds.order_user = User.objects.get(id=ds.order_user).username
                ds.order_executor = User.objects.get(id=ds.order_executor).username 
                if ds.order_type  == 1:
                    ds.order_url = '/deploy_order/status/{id}/'.format(id=ds.id)
                    ds.order_content = ds.project_order.order_content
                elif ds.order_type  == 0:
                    ds.order_url = '/db/sql/order/run/{id}/'.format(id=ds.id)
                    if ds.sql_audit_order.order_type == 'file' and ds.sql_audit_order.order_file:
                        filePath = os.getcwd() + '/upload/' + str(ds.sql_audit_order.order_file)
                        with open(filePath, 'r') as f:
                            ds.order_content = f.read(1000)   
                    else:ds.order_content = ds.sql_audit_order.order_sql  
                elif ds.order_type  == 2:
                    ds.order_url = '/file/upload/run/{id}/'.format(id=ds.id)
                    ds.order_content = ds.fileupload_audit_order.order_content  
                elif ds.order_type  == 3:
                    ds.order_url = '/file/download/run/{id}/'.format(id=ds.id)
                    ds.order_content = ds.filedownload_audit_order.order_content                    
                else:ds.order_content = '未知'
            except Exception, ex:
                logger.warn(msg="获取审核SQL[{id}]错误: {ex}".format(id=ds.id,ex=str(ex)))
        orderRbt = Order()       
        #工单类型总计
        orderType =  orderRbt.countOrderType()                 
        #用户列表
        usernameList = orderRbt.getUserNameList()     
        #分页信息
        paginator = Paginator(orderList, 25)          
        try:
            orderList = paginator.page(page)
        except PageNotAnInteger:
            orderList = paginator.page(1)
        except EmptyPage:
            orderList = paginator.page(paginator.num_pages)      
        return render(request,'orders/order_list.html',{"user":request.user,"orderList":orderList,
                                                        "orderType":orderType,"monthDataList":orderRbt.getMonthOrderCount(),
                                                        "codeDataList":orderRbt.getOrderCount(type=1, day=7),"usernameList":usernameList,
                                                        "sqlDataList":orderRbt.getOrderCount(type=0, day=7),
                                                        "statusList":Order().getOrderStatusCount()},
                                  )    
        
        
@login_required()
@permission_required('orders.can_read_order_system',login_url='/noperm/')
def order_search(request):        
    if request.method == "GET":
        userList = User.objects.all()       
        return render(request,'orders/order_search.html',{"user":request.user,
                                                          "userList":userList},
                                  )   
    elif request.method == "POST":
        dataList = []
        data = dict()
        #格式化查询条件
        for (k,v)  in request.POST.items() :
            if v is not None and v != u'' :
                data[k] = v 
        for ds in Order_System.objects.filter(**data).order_by("-id")[0:1000]:
            order_id = '''<td class="text-center">{sqlid}</td>'''.format(sqlid=ds.id)
            order_user = '''<td class="text-center">{order_user}</td>'''.format(order_user=User.objects.get(id=ds.order_user).username)
            if ds.order_type == 1:
                order_url =  '/deploy_order/status/{id}/'.format(id=ds.id)
                order_type = '<td class="text-center"><span class="label label-success">代码部署</span></td>'
                order_content = '<td class="text-center"><a href="{order_url}">{content}</a></td>'.format(order_url=order_url,content = ds.project_order.order_content[0:10])
            elif ds.order_type == 0:
                order_url = '/db/sql/order/run/{id}/'.format(id=ds.id)
                order_type = '<td class="text-center"><span class="label label-info">SQL更新</span></td>'
                if ds.sql_audit_order.order_type == 'file' and ds.sql_audit_order.order_file:
                    filePath = os.getcwd() + '/upload/' + str(ds.sql_audit_order.order_file)
                    with open(filePath, 'r') as f:
                        ds.sql_audit_order.order_sql = f.read(100)                     
                order_content = '''<td class="text-center"><a href="{order_url}" target="_blank" class="tooltip-test" 
                                        data-toggle="tooltip" title="{content}">{abr_content}</a></td>'''.format(order_url=order_url,content = ds.sql_audit_order.order_sql,
                                                                                                                 abr_content=ds.sql_audit_order.order_sql[0:50])
            elif ds.order_type == 2:
                order_url =  '/file/upload/run/{id}/'.format(id=ds.id)
                order_type = '<td class="text-center"><span class="label label-warning">文件分发</span></td>'
                order_content = '<td class="text-center"><a href="{order_url}">{content}</a></td>'.format(order_url=order_url,content = ds.fileupload_audit_order.order_content[0:10]) 
            elif ds.order_type == 3:
                order_url =  '/file/download/run/{id}/'.format(id=ds.id)
                order_type = '<td class="text-center"><span class="label label-danger">文件下载</span></td>'
                order_content = '<td class="text-center"><a href="{order_url}">{content}</a></td>'.format(order_url=order_url,content = ds.filedownload_audit_order.order_content[0:10])                                                        
            order_subject = '<td class="text-center">{order_subject}</td>'.format(order_subject=ds.order_subject)          
            order_executor = '''<td class="text-center">{order_executor}</td>'''.format(order_executor=User.objects.get(id=ds.order_executor).username)
            order_createTime = '''<td class="text-center">{order_createTime}</td>'''.format(order_createTime=ds.create_time)                      
            if ds.order_status == 1:span = '<span class="label label-info">已拒绝</span>'
            elif ds.order_status == 2:span = '<span class="label label-success">审核中</span>'
            elif ds.order_status == 3:span = '<span class="label label-danger">已部署</span>'  
            elif ds.order_status == 4:span = '<span class="label label-default">待授权</span>'   
            elif ds.order_status == 5:span = '<span class="label label-success">已执行</span>'  
            elif ds.order_status == 6:span = '<span class="label label-danger">已回滚</span>'      
            elif ds.order_status == 7:span = '<span class="label label-danger">已撤回</span>'    
            elif ds.order_status == 8:span = '<span class="label label-success">已授权</span>'                                                                                         
            else: span = '<span class="label label-warning">已失败</span>'        
            order_status = '''<td class="text-center">{span}</td>'''.format(span=span)
            if request.user.is_superuser:
                aTag = '<a href="{order_url}" target="_blank"><button  type="button" class="btn btn-default"><abbr title="执行SQL"><i class="fa fa-play-circle-o"></i></button></a>'.format(order_url=order_url,ds_id=ds.id)    
                if ds.order_status == 4:
                    buttonTag1 = """<button  type="button" class="btn btn-default"><abbr title="授权"><i class="fa fa-check"  onclick="updateSqlOrderStatus(this,{ds_id},'auth')"></i></button>""".format(ds_id=ds.id)
                else:
                    buttonTag1 = """<button  type="button" class="btn btn-default disabled"><abbr title="授权"><i class="fa fa-check"></i></button>"""                                           
                if ds.order_status == 7:
                    buttonTag2 = """<button  type="button" class="btn btn-default disabled"><abbr title="取消"><i class="fa fa-times "></i></button>"""                         
                else:
                    buttonTag2 = """<button  type="button" class="btn btn-default"><abbr title="取消"><i class="fa fa-times "  onclick="updateSqlOrderStatus(this,{ds_id},'disable')"></i></button>""".format(ds_id=ds.id)                                                         
                buttonTag3 = """<button  type="button" class="btn btn-default"><abbr title="删除"><i class="glyphicon glyphicon-trash"  onclick="deleteSqlOrder(this,{ds_id})"></i></button>""".format(ds_id=ds.id)  
                buttons = aTag + buttonTag1 + buttonTag2 + buttonTag3
            else:              
                if ds.order_executor == request.user.id:
                    aTag = '<a href="{order_url}" target="_blank"><button  type="button" class="btn btn-default"><abbr title="执行SQL"><i class="fa fa-play-circle-o"></i></button></a>'.format(order_url=order_url,ds_id=ds.id)     
                    if ds.order_status == 4:
                        buttonTag1 = """<button  type="button" class="btn btn-default"><abbr title="授权"><i class="fa fa-check"  onclick="updateSqlOrderStatus(this,{ds_id},'auth')"></i></button>""".format(ds_id=ds.id)
                    else:
                        buttonTag1 = """<button  type="button" class="btn btn-default disabled"><abbr title="授权"><i class="fa fa-check"></i></button>"""  
                    if ds.order_status == 7:
                        buttonTag2 = """<button  type="button" class="btn btn-default disabled"><abbr title="取消"><i class="fa fa-times "></i></button>"""                          
                    else:
                        buttonTag2 = """<button  type="button" class="btn btn-default"><abbr title="取消"><i class="fa fa-times "  onclick="updateSqlOrderStatus(this,{ds_id},'disable')"></i></button>""".format(ds_id=ds.id)                                                     
                else:
                    aTag = """<button  type="button" class="btn btn-default disabled"><abbr title="执行SQL"><i class="fa fa-play-circle-o"></i></button>"""  
                    buttonTag1 = """<button  type="button" class="btn btn-default disabled"><abbr title="授权"><i class="fa fa-check" ></i></button>"""  
                    buttonTag2 = """<button  type="button" class="btn btn-default disabled"><abbr title="取消"><i class="fa fa-times "></i></button>"""
                buttons = aTag + buttonTag1 + buttonTag2
            order_op = '''<td class="text-center">{buttons}</td>'''.format(buttons=buttons)
            dataList.append([order_id ,order_type,order_user,order_subject,order_content,order_executor,order_createTime,order_status,order_op])
        return JsonResponse({'msg':"数据查询成功","code":200,'data':dataList,'count':0})         
    
    
@login_required()
@permission_required('filemanage.can_read_fileupload_audit_order',login_url='/noperm/')
def file_upload_list(request,page):
    if request.method == "GET":
        if request.user.is_superuser:
            uploadList = Order_System.objects.filter(order_type=2).order_by("-id")[0:1000]
        else:
            uploadList = Order_System.objects.filter(Q(order_user=request.user.id) | Q(order_executor=request.user.id),order_type=2).order_by("-id")[0:1000]
        #分页信息
        paginator = Paginator(uploadList, 25)         
        try:
            uploadList = paginator.page(page)
        except PageNotAnInteger:
            uploadList = paginator.page(1)
        except EmptyPage:
            uploadList = paginator.page(paginator.num_pages)                     
        userList = User.objects.filter(is_superuser=1)    
        serverList = AssetsSource().serverList()#Server_Assets.objects.all()
        serviceList = Service_Assets.objects.all()
        projectList = Project_Assets.objects.all()
        groupList = Group.objects.all()
        return render(request,'filemanage/file_upload_list.html',{"user":request.user,"serverList":serverList,"userList":userList,
                                                                 "serviceList":serviceList,"projectList":projectList,
                                                                 "groupList":groupList,"uploadList":uploadList})    

   
@login_required()
@permission_required('filemanage.can_read_fileupload_audit_order',login_url='/noperm/')
def file_upload_audit(request):
    if request.method == "POST":  
        try:
            order = Order_System.objects.create(order_type=2,
                                                order_subject=request.POST.get('order_subject'),
                                                order_executor=request.POST.get('order_executor'),
                                                order_status=4,
                                                order_level=0,
                                                order_user=request.user.id,
                                                )
        except Exception, ex:
            logger.error(msg="文件上传失败: {ex}".format(ex=ex))
            return JsonResponse({'msg':"文件上传失败: {ex}".format(ex=ex),"code":500}) 
        if  request.POST.get('server_model') == 'service':
            serverList = AssetsSource().service(business=request.POST.get('service'))[0]
        elif request.POST.get('server_model') == 'group':
            serverList = AssetsSource().group(group=request.POST.get('group'))[0]
        elif request.POST.get('server_model') == 'custom':
            serverList = AssetsSource().custom(serverList=request.POST.get('server').split(','))[0]
        else:
            return JsonResponse({'msg':"参数不正确","code":500}) 
        try:
            upload = FileUpload_Audit_Order.objects.create(
                                                           order = order,
                                                           dest_path=request.POST.get('dest_path'),
                                                           dest_server=json.dumps(serverList),
                                                           chown_user=request.POST.get('chown_user'),
                                                           chown_rwx=request.POST.get('chown_rwx'),
                                                           order_content=request.POST.get('order_content'),
                                                           )
        except Exception, ex:
            order.delete()
            logger.error(msg="文件上传失败: {ex}".format(ex=ex))
            return JsonResponse({'msg':"文件上传失败: {ex}".format(ex=ex),"code":500})
                 
        for files in request.FILES.getlist('order_files[]'): 
            try:
                upFile = UploadFiles.objects.create(file_order=upload,file_path=files)
                filePath = os.getcwd() + '/upload/' + str(upFile.file_path)
                upFile.file_type = base.getFileType(filePath)
                upFile.save()
            except Exception,ex:
                order.delete()
                upload.delete()
                logger.error(msg="文件上传失败: {ex}".format(ex=ex))
                return JsonResponse({'msg':"文件上传失败: {ex}".format(ex=ex),"code":500}) 
         
    return JsonResponse({'msg':"文件上传成功","code":200,'data':[],'count':0})    


@login_required()
@permission_required('filemanage.can_read_filedownload_audit_order',login_url='/noperm/')
def file_download_list(request,page):
    if request.method == "GET":
        if request.user.is_superuser:
            uploadList = Order_System.objects.filter(order_type=3).order_by("-id")[0:1000]
        else:
            uploadList = Order_System.objects.filter(Q(order_user=request.user.id) | Q(order_executor=request.user.id),order_type=3).order_by("-id")[0:1000]
        #分页信息
        paginator = Paginator(uploadList, 25)         
        try:
            uploadList = paginator.page(page)
        except PageNotAnInteger:
            uploadList = paginator.page(1)
        except EmptyPage:
            uploadList = paginator.page(paginator.num_pages)                     
        userList = User.objects.filter(is_superuser=1)    
        serverList = AssetsSource().serverList()#Server_Assets.objects.all()
        serviceList = Service_Assets.objects.all()
        projectList = Project_Assets.objects.all()
        groupList = Group.objects.all()
        return render(request,'filemanage/file_download_list.html',{"user":request.user,"serverList":serverList,"userList":userList,
                                                                 "serviceList":serviceList,"projectList":projectList,
                                                                 "groupList":groupList,"uploadList":uploadList}) 
        
@login_required()
@permission_required('filemanage.can_add_filedownload_audit_order',login_url='/noperm/')
def file_download_audit(request):
    if request.method == "POST":  
        try:
            order = Order_System.objects.create(order_type=3,
                                                order_subject=request.POST.get('order_subject'),
                                                order_executor=request.POST.get('order_executor'),
                                                order_status=4,
                                                order_level=0,
                                                order_user=request.user.id,
                                                )
        except Exception, ex:
            logger.error(msg="文件下载申请失败: {ex}".format(ex=ex))
            return JsonResponse({'msg':"文件下载申请失败: {ex}".format(ex=ex),"code":500}) 
        if  request.POST.get('server_model') == 'service':
            serverList = AssetsSource().service(business=request.POST.get('service'))[0]
        elif request.POST.get('server_model') == 'group':
            serverList = AssetsSource().group(group=request.POST.get('group'))[0]
        elif request.POST.get('server_model') == 'custom':
            serverList = AssetsSource().custom(serverList=request.POST.get('server').split(','))[0]
        else:
            return JsonResponse({'msg':"参数不正确","code":500}) 
        try:
            FileDownload_Audit_Order.objects.create(
                                                    order = order,
                                                    dest_path=request.POST.get('dest_path'),
                                                    dest_server=json.dumps(serverList),
                                                    order_content=request.POST.get('order_content'),
                                                    )
        except Exception, ex:
            order.delete()
            logger.error(msg="文件下载申请失败: {ex}".format(ex=ex))
            return JsonResponse({'msg':"文件下载申请失败: {ex}".format(ex=ex),"code":500})                         
    return JsonResponse({'msg':"文件下载申请成功","code":200,'data':[],'count':0})         