#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from django.contrib.auth.models import User,Group,Permission,ContentType
from utils.logger import logger
from django.http import QueryDict
from dao.base import DataHandle
from dao.assets import AssetsBase
from asset.models import User_Server

class PermsManage(DataHandle):
    def __init__(self):
        super(PermsManage, self).__init__() 
    
    def get_apps(self):
        dataList = []
        for ds in ContentType.objects.all():
            dataList.append({"label":ds.app_label,"content_type":ds.id,"apps_name":ds.name})
        return dataList    
    
    def perms(self,content_type):
        perms = []
        for ds in Permission.objects.filter(content_type=content_type):
            perms.append(self.convert_to_dict(ds)) 
        return perms       
    
    def get_perms(self): 
        permsList = []
        for ds in self.get_apps():             
            if ds.get("label") in ["auth","contenttypes","admin","sessions"] or ds.get("label").startswith("django"):continue
            for ps in self.perms(content_type=ds.get("content_type")):
                ps["apps_name"] = ds.get("apps_name")
                permsList.append(ps)
        return permsList     
        
class UsersManage(PermsManage,AssetsBase):
    def __init__(self):
        super(UsersManage, self).__init__() 

    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="UsersManage没有{sub}方法".format(sub=sub))       
            return "参数错误"
        
    def get_user(self,request):
        if request.method == 'GET':cid = request.GET.get('id')
        elif request.method == 'POST':cid = request.POST.get('id')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('id')
        try:
            user = User.objects.get(id=cid)
            return user
        except Exception as ex:
            logger.warn(msg="获取用户信息失败: {ex}".format(ex=ex))
            return False      
        
    def register(self,request):
        if request.POST.get('password') == request.POST.get('c_password'):
            try:
                user = User.objects.filter(username=request.POST.get('username'))
                if len(user)>0:return "注册失败，用户已经存在。"
                else: 
                    user = User()
                    user.username = request.POST.get('username')
                    user.email = request.POST.get('email')
                    user.is_staff = 0
                    user.is_active = request.POST.get('is_active')
                    user.is_superuser = request.POST.get('is_superuser')                       
                    user.set_password(request.POST.get('password'))
                    user.save()
                    return True
            except Exception as ex:
                return ex
        else:"密码不一致，用户注册失败。"
            
    def modf_user(self,request):
        try: 
            users = User.objects.filter(id=request.POST.get('id')).update(
                                                is_active = request.POST.get('is_active'),
                                                is_superuser = int(request.POST.get('is_superuser')),
                                                email = request.POST.get('email'), 
                                                username = request.POST.get('username')
                                            )    
            return users
        except Exception as ex:
            return ex    
        
    def change_passwd(self,request):  
        user = self.get_user(request)
        if user is False:return "用户不存在"
                
        if user.id != request.user.id and request.user.is_superuser is False:return "您无权操作此项"  
             
        elif user.id == request.user.id or request.user.is_superuser:
            if request.POST.get('password') == request.POST.get('c_password'):
                try:                 
                    user.set_password(request.POST.get('password'))
                    user.save()
                    return True
                except Exception as ex:
                    return "密码修改失败：%s" % str(ex) 
                 
        return "修改密码失败"

        
    def modf_user_group(self,request):
        user = self.get_user(request)
        if user:
            userGroupList = []
            for group in user.groups.values():
                userGroupList.append(group.get('id'))
            groupList = [ int(i) for i in request.POST.getlist('groups[]')]
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
        else:
            return "用户不存在"    
    
    def modf_user_perm(self,request):
        user = self.get_user(request)
        if user:
            userPermList = []
            for perm in user.user_permissions.values():
                userPermList.append(perm.get('id'))
            permList = [ int(i) for i in request.POST.getlist('perms[]')]
            addPermList = list(set(permList).difference(set(userPermList)))
            delPermList = list(set(userPermList).difference(set(permList)))
            #添加新增的权限
            for permId in addPermList:
                perm = Permission.objects.get(id=permId)
                user.user_permissions.add(perm)
            #删除去掉的权限
            for permId in delPermList:
                perm = Permission.objects.get(id=permId)
                user.user_permissions.remove(perm) 
        else:
            return "用户不存在"         
    
    def get_users(self,request=None):
        userList = []
        for ds in User.objects.all() :           
            data = self.convert_to_dict(ds)
            data.pop('password')
            userList.append(data)
        return userList   
      
    def get_groups(self,request=None):
        dataList = []
        for ds in Group.objects.all(): 
            dataList.append(self.convert_to_dict(ds))
        return dataList
    
    def get_user_group(self,request):       
        user = self.get_user(request)
        if user:
            groupList = self.get_groups()
            userGroupList = [ g.get('id') for g in user.groups.values()]
            for gs  in groupList:
                if gs["id"] in userGroupList:gs["status"] = 1
                else:gs["status"] = 0
            return groupList
        else:
            return "用户不存在"
        
    def get_user_perms(self,request):  
        user = self.get_user(request)
        if user:
            permsList = self.get_perms()
            userPermsList =  [ p.get('id') for p in user.user_permissions.values()]
            for ps in permsList:
                if ps["id"] in userPermsList:ps["status"] = 1
                else:ps["status"] = 0
            return permsList
        else:
            return "用户不存在"
    
    def get_user_assets(self,request):
        userAssetsList = []
        user = self.get_user(request)
        if user and request.user.is_superuser:
            if request.user.id == user.id:
                for ds in self.query(self.assetsList()):
                    userAssetsList.append(ds)            
            elif request.user.id != user.id:
                assets_list =[ ds.assets for ds in User_Server.objects.filter(user=user) ]
                for ds in self.query(assets_list):
                    userAssetsList.append(ds)            
        else:
            assets_list =[ ds.assets for ds in User_Server.objects.filter(user=request.user) ]
            for ds in self.query(assets_list):
                userAssetsList.append(ds)
        return userAssetsList

    def modf_user_assets(self,request):
        user = self.get_user(request)
        if user:
            userAssetsList = []
            for asset in User_Server.objects.filter(user=user):
                userAssetsList.append(asset.assets.id)
            assetsList = [ int(i) for i in request.POST.getlist('assets[]')]
            addAssetsList = list(set(assetsList).difference(set(userAssetsList)))
            delAssetsList = list(set(userAssetsList).difference(set(assetsList)))
            #添加新增的资产
            for aId in addAssetsList:
                assets = self.assets(aId)
                if assets:
                    try:
                        User_Server.objects.create(assets=assets,user=user)
                    except Exception as ex:
                        return str(ex)
                else:
                    return "资产不存在"
            #删除去掉的资产
            for aId in delAssetsList:
                assets = self.assets(aId)
                if assets:
                    try:
                        User_Server.objects.filter(assets=assets,user=user).delete()
                    except Exception as ex:
                        return str(ex)
                else:
                    return "资产不存在"
        else:
            return "用户不存在"         
    
        
class GroupManageBase(PermsManage):
    
    def __init__(self):
        super(GroupManageBase, self).__init__()
    
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="GroupManage没有{sub}方法".format(sub=sub))       
            return "参数错误"
        
    def get_group(self,request):
        if request.method == 'GET':cid = request.GET.get('id')
        elif request.method == 'POST':cid = request.POST.get('id')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('id')
        try:
            user = Group.objects.get(id=cid)
            return user
        except Exception as ex:
            logger.warn(msg="获取用户信息失败: {ex}".format(ex=ex))
            return False 
    
    def get_groups(self,request=None):
        dataList = []
        for ds in Group.objects.all(): 
            dataList.append(self.convert_to_dict(ds))
        return dataList    
    
    def get_group_users(self,request):
        group = self.get_group(request)
        if group:        
            userList = []
            for ds in group.user_set.all():           
                data = self.convert_to_dict(ds)
                data.pop('password')
                userList.append(data)
            return userList
        else:
            return "用户组不存在" 
           
    def get_group_perms(self,request):  
        group = self.get_group(request)
        if group:
            permsList = self.get_perms()
            groupPermsList =  [ g.get('id') for g in group.permissions.values()]
            for ps in permsList:
                if ps["id"] in groupPermsList:ps["status"] = 1
                else:ps["status"] = 0
            return permsList
        else:
            return "用户组不存在"         
    
    def modf_group_users(self,request):
        group = self.get_group(request)
        if group:
            userList = [ int(i) for i in request.POST.getlist('users[]')]
            groupUsersList = []
            for user in group.user_set.all():
                groupUsersList.append(user.id)
            addUsersList = list(set(userList).difference(set(groupUsersList)))
            delUsersList = list(set(groupUsersList).difference(set(userList)))
            #添加新增的用户
            for uid in addUsersList:
                user = User.objects.get(id=uid)
                group.user_set.add(user)
            #删除去掉的用户
            for uid in delUsersList:
                user = User.objects.get(id=uid)
                group.user_set.remove(user)
        else:
            return "用户不存在"   
                            
    def modf_group_perm(self,request):
        group = self.get_group(request)
        if group:
            userPermList = []
            for perm in group.permissions.values():
                userPermList.append(perm.get('id'))
            permList = [ int(i) for i in request.POST.getlist('perms[]')]
            addPermList = list(set(permList).difference(set(userPermList)))
            delPermList = list(set(userPermList).difference(set(permList)))
            #添加新增的权限
            for permId in addPermList:
                perm = Permission.objects.get(id=permId)
                Group.objects.get(id=request.POST.get('id')).permissions.add(perm)
            #删除去掉的权限
            for permId in delPermList:
                perm = Permission.objects.get(id=permId)
                Group.objects.get(id=request.POST.get('id')).permissions.remove(perm) 
        else:
            return "用户不存在"         