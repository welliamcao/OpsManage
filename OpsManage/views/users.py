#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.decorators import permission_required
from django.db.models import Q 
from orders.models import Order_System
from OpsManage.views import assets
from django.http import QueryDict
from OpsManage.models import (Server_Assets,Service_Assets,
                                Assets,User_Server,Global_Config,
                                Project_Assets)
@login_required()
@permission_required('auth.change_user',login_url='/noperm/') 
def user_manage(request):
    if request.method == "GET":
        userList = User.objects.all()
        groupList = Group.objects.all()
        return render(request,'users/user_manage.html',{"user":request.user,"userList":userList,"groupList":groupList})    
        
        
def register(request):
    if request.method == "POST":
        if request.POST.get('password') == request.POST.get('c_password'):
            try:
                user = User.objects.filter(username=request.POST.get('username'))
                if len(user)>0:return JsonResponse({"code":500,"data":None,"msg":"注册失败，用户已经存在。"})
                else: 
                    user = User()
                    user.username = request.POST.get('username')
                    user.email = request.POST.get('email')
                    user.is_staff = 0
                    user.is_active = 0
                    user.is_superuser = 0                        
                    user.set_password(request.POST.get('password'))
                    user.save()
                    return JsonResponse({"code":200,"data":None,"msg":"用户注册成功"})
            except Exception,e:
                return JsonResponse({"code":500,"data":None,"msg":"用户注册失败"}) 
        else:return JsonResponse({"code":500,"data":None,"msg":"密码不一致，用户注册失败。"})
        
@login_required()
def user_center(request):
    if request.method == "GET": 
        serverList = []
        baseAssets = {}
        try:
            baseAssets = assets.getBaseAssets()            
            config = Global_Config.objects.get(id=1)
            if config.webssh == 1 and request.user.is_superuser:
                serverList = Assets.objects.all().order_by("-id") 
            elif config.webssh == 1:
                userServer = User_Server.objects.filter(user_id=int(request.user.id))
                serverList = []
                for s in userServer:
                    ser = Server_Assets.objects.get(id=s.server_id)
                    serverList.append(ser.assets)
        except:
            config = None     
        orderList = Order_System.objects.filter(Q(order_user=User.objects.get(username=request.user).id) | Q(order_executor=User.objects.get(username=request.user).id)).order_by("id")[0:150]  
        for order in  orderList:
            if order.order_executor == request.user.id:order.perm = 1
            order.order_user = User.objects.get(id=order.order_user).username
            order.order_executor = User.objects.get(id=order.order_executor).username
        return render(request,'users/user_center.html',{"user":request.user,"orderList":orderList,
                                                        "serverList":serverList,"baseAssets":baseAssets,
                                                        "config":config}) 
    if request.method == "POST":
        if request.POST.get('password') == request.POST.get('c_password'):
            try:
                user = User.objects.get(username=request.user)                  
                user.set_password(request.POST.get('password'))
                user.save()
                return JsonResponse({"code":200,"data":None,"msg":"密码修改成功"})
            except Exception,e:
                return JsonResponse({"code":500,"data":None,"msg":"密码修改失败：%s" % str(e)}) 
        else:return JsonResponse({"code":500,"data":None,"msg":"密码不一致，密码修改失败。"})      
           
@login_required    
@permission_required('auth.change_user',login_url='/noperm/')   
def user(request,uid):    
    if request.method == "GET":
        try:
            user = User.objects.get(id=uid)
        except Exception,e:
            return render(request,'users/user_info.html',{"user":request.user,
                                                             "errorInfo":"用户不存在，可能已经被删除."})         
        #获取用户权限列表
        userGroupList = []
        permList = Permission.objects.filter(codename__startswith="can_")
        userPermList = [ u.get('id') for u in user.user_permissions.values()]
        for ds in permList:
            if ds.id in userPermList:ds.status = 1
            else:ds.status = 0        
        #获取用户组列表
        groupList = Group.objects.all() 
        userGroupList = [ g.get('id') for g in user.groups.values()]
        for gs  in groupList:
            if gs.id in userGroupList:gs.status = 1
            else:gs.status = 0 
        serverList = Server_Assets.objects.all()
        userServerListId =  [ i.server_id for i in User_Server.objects.filter(user_id=user.id)]
        for ser in serverList:
            if ser.id in userServerListId:ser.status = 1
            else:ser.status = 0
        projectList = Project_Assets.objects.all()    
        serviceList = Service_Assets.objects.all()                      
        return render(request,'users/user_info.html',{"user":request.user,"user_info":user,
                                                          "serverList":serverList,"serviceList":serviceList,
                                                          "permList":permList,"groupList":groupList,
                                                          "projectList":projectList})
            
    elif request.method == "POST":
        try:
            user = User.objects.get(id=uid)
            User.objects.filter(id=uid).update(
                                            is_active = request.POST.get('is_active'),
                                            is_superuser = int(request.POST.get('is_superuser')),
                                            email = request.POST.get('email'), 
                                            username = request.POST.get('username')
                                            )          
            #如果权限key不存在就单做清除权限
            if request.POST.getlist('perms') is None:user.user_permissions.clear()
            else:
                userPermList = []
                for perm in user.user_permissions.values():
                    userPermList.append(perm.get('id'))
                permList = [ int(i) for i in request.POST.getlist('perms')]
                addPermList = list(set(permList).difference(set(userPermList)))
                delPermList = list(set(userPermList).difference(set(permList)))
                #添加新增的权限
                for permId in addPermList:
                    perm = Permission.objects.get(id=permId)
                    User.objects.get(id=uid).user_permissions.add(perm)
                #删除去掉的权限
                for permId in delPermList:
                    perm = Permission.objects.get(id=permId)
                    User.objects.get(id=uid).user_permissions.remove(perm) 
            #如果用户组key不存在就单做清除用户组  
            if request.POST.getlist('groups') is None:user.groups.clear()
            else:
                userGroupList = []
                for group in user.groups.values():
                    userGroupList.append(group.get('id'))
                groupList = [ int(i) for i in request.POST.getlist('groups')]
                addGroupList = list(set(groupList).difference(set(userGroupList)))
                delGroupList = list(set(userGroupList).difference(set(groupList)))
                #添加新增的用户组
                for groupId in addGroupList:
                    group = Group.objects.get(id=groupId)
                    user.groups.add(group)
                #删除去掉的用户组
                for groupId in delGroupList:
                    group = Group.objects.get(id=groupId)
                    user.groups.remove(group)
            return HttpResponseRedirect('/user/{uid}/'.format(uid=uid)) 
        except Exception,e:
            return  render(request,'users/user_info.html',{"user":request.user,"errorInfo":"用户资料修改错误：%s" % str(e)})   
            
    elif request.method == "PUT" and request.user.is_superuser:
        data = QueryDict(request.body)
        password = data.get('password')
        c_password = data.get('c_password')
        if password == c_password:
            try:
                user = User.objects.get(id=uid)                  
                user.set_password(password)
                user.save()
                return JsonResponse({"code":200,"data":None,"msg":"密码修改成功"})
            except Exception,e:
                return JsonResponse({"code":500,"data":None,"msg":"密码修改失败：%s" % str(e)}) 
        else:return JsonResponse({"code":500,"data":None,"msg":"密码不一致，密码修改失败。"})   

    
    
        
@login_required    
@permission_required('auth.change_group',login_url='/noperm/')           
def group(request,gid):    
    if request.method == "GET":
        try:
            group = Group.objects.get(id=gid)
        except:
            return render(request,'users/group_info.html',{"user":request.user,
                                                             "errorInfo":"用户不存在，可能已经被删除."}, 
                                      ) 
        permList = Permission.objects.filter(codename__startswith="can_") 
        groupPerm = [ p.get('id') for p in group.permissions.values()]
        try:
            for ds in permList:
                if ds.id in groupPerm:ds.status = 1
                else:ds.status = 0
            return render(request,'users/group_info.html',{"user":request.user,"permList":permList,"group":group},) 
        except Exception,e: 
            return render(request,'users/group_info.html',
                                      {"user":request.user,"errorInfo":"用户组资料修改错误：%s" % str(e)}, 
                                      )  
    elif request.method == "POST":
        try:
            group = Group.objects.get(id=gid)
            Group.objects.filter(id=gid).update(
                                            name = request.POST.get('name')
                                            )            
            #如果权限key不存在就单做清除权限
            if request.POST.getlist('perms') is None:group.permissions.clear()
            else:
                userPermList = []
                for perm in group.permissions.values():
                    userPermList.append(perm.get('id'))
                permList = [ int(i) for i in request.POST.getlist('perms')]
                addPermList = list(set(permList).difference(set(userPermList)))
                delPermList = list(set(userPermList).difference(set(permList)))
                #添加新增的权限
                for permId in addPermList:
                    perm = Permission.objects.get(id=permId)
                    Group.objects.get(id=gid).permissions.add(perm)
                #删除去掉的权限
                for permId in delPermList:
                    perm = Permission.objects.get(id=permId)
                    Group.objects.get(id=gid).permissions.remove(perm) 
            return HttpResponseRedirect('/group/{gid}/'.format(gid=gid)) 
        except Exception,e:
            return render(request,'users/user_info.html',{"user":request.user,"errorInfo":"用户资料修改错误：%s" % str(e)})         

@login_required       
def user_server(request,uid):  
    try:
        user = User.objects.get(id=uid)
    except Exception,e:
        return JsonResponse({"code":500,"data":None,"msg":"主机分配失败：%s" % str(e)})
    if request.method == "POST":
        sList = []
        
        if request.POST.get('server_model') in ['service','group','custom']:
            if request.POST.get('server_model') == 'custom':
                serverList = request.POST.getlist('webssh_server')
                for server in serverList:
                    try:
                        sList.append(Server_Assets.objects.get(id=server))
                    except:
                        pass
            elif request.POST.get('server_model') == 'group':
                serverList = Assets.objects.filter(group=request.POST.get('webssh_group'))
                for server in serverList:
                    sList.append(server.server_assets)  
            elif request.POST.get('server_model') == 'service':
                serverList = Assets.objects.filter(business=request.POST.get('webssh_service'))
                for server in serverList:
                    sList.append(server.server_assets)
        try:
            serverList = [ i.id for i in sList ]
            userServer =  User_Server.objects.filter(user_id=user.id)
            userServerList = []
            for s in userServer:
                userServerList.append(s.server_id)
            addServerList =  list(set(serverList).difference(set(userServerList)))
            delServerList = list(set(userServerList).difference(set(serverList)))
            #添加新增的主机
            for s in addServerList:
                User_Server.objects.create(user_id=user.id,server_id=s)
            #删除去掉的主机
            for s in delServerList:
                User_Server.objects.get(user_id=user.id,server_id=s).delete()
        except Exception,e:
            return JsonResponse({"code":500,"data":None,"msg":"主机分配失败：%s" % str(e)})  
        return JsonResponse({"code":200,"data":None,"msg":"主机分配成功"}) 