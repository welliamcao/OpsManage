#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from django.contrib.auth.models import Permission,ContentType
from account.models import User,Role,Structure
from utils.logger import logger
from django.http import QueryDict, Http404
from dao.base import DataHandle
from dao.assets import AssetsBase
from asset.models import User_Server,Assets
from django.db.models import Q

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
        except User.DoesNotExist:
            raise Http404     
                
    def change_passwd(self, request):  
        user = self.get_user(request)

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

    def modf_user_profile(self, request):  
        user = self.get_user(request)
        
        if user.id != request.user.id and request.user.is_superuser is False:return "您无权操作此项"  
             
        elif user.id == request.user.id or request.user.is_superuser:
            try:                 
                user.email = request.POST.get('email')
                user.mobile = request.POST.get('mobile')
                user.name = request.POST.get('name')
                user.save()
                return True
            except Exception as ex:
                return "配置信息修改失败：%s" % str(ex) 
                 
        return "配置信息修改失败"        
            
    def modf_user_role(self,request):
        user = self.get_user(request)
        
        userRoleList = []
        for role in user.roles.all():
            userRoleList.append(role.id)
        roleList = [ int(i) for i in request.POST.getlist('roles[]')]
        addroleList = list(set(roleList).difference(set(userRoleList)))
        delroleList = list(set(userRoleList).difference(set(roleList)))
        #添加新增的角色
        for roleId in addroleList:
            role = Role.objects.get(id=roleId)
            user.roles.add(role)
        #删除去掉的角色
        for roleId in delroleList:
            role = Role.objects.get(id=roleId)
            user.roles.remove(role)   
    
    def modf_user_perm(self,request):
        user = self.get_user(request)

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
    
    def get_users(self,request=None):
        userList = []
        for ds in User.objects.all() :           
            userList.append(ds.to_json())
        return userList   
      
    def get_roles(self,request=None):
        dataList = []
        for ds in Role.objects.all(): 
            dataList.append(ds.to_json())
        return dataList
    
    def get_user_role(self,request):       
        user = self.get_user(request)

        roleList = self.get_roles()
        userRoleList = [ g.get('id') for g in user.roles.values()]
        for gs  in roleList:
            if gs["id"] in userRoleList:gs["status"] = 1
            else:gs["status"] = 0
        return roleList
        
    def get_user_perms(self,request):  
        user = self.get_user(request)

        permsList = self.get_perms()
        userPermsList =  [ p.get('id') for p in user.user_permissions.values()]
        for ps in permsList:
            if ps["id"] in userPermsList:ps["status"] = 1
            else:ps["status"] = 0
        return permsList
    
    def get_user_assets(self,request):
        userAssetsList = []
        user = self.get_user(request)
        if request.user.is_superuser:
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
    
    def get_user_superior(self,user):
        dataList, uidList = [], []
        if user.superior and user.superior.id != user.id:
            uidList.append(user.superior.id)
            dataList.append(user.superior.to_json())
            
        for ds in user.department.values():
            manage_user = User.objects.get(id=ds.get("manage"))
            if manage_user.id not in uidList and manage_user.id != user.id:
                uidList.append(manage_user.id)
                dataList.append(manage_user.to_json()) 
        return dataList
    
        
class RolesManage(PermsManage):  
    
    def __init__(self):
        super(RolesManage, self).__init__()     
    
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="RolesManage没有{sub}方法".format(sub=sub))       
            return "参数错误"
        
    def get_role(self,request):
        if request.method == 'GET':cid = request.GET.get('id')
        elif request.method == 'POST':cid = request.POST.get('id')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('id')
        try:
            user = Role.objects.get(id=cid)
            return user
        except Role.DoesNotExist:
            raise Http404  
    
    def get_roles(self):
        dataList = []
        for ds in Role.objects.all(): 
            dataList.append(ds.to_json())
        return dataList    
    
    def get_role_users(self,request):
        role = self.get_role(request)    
        userList = []
        for ds in User.objects.filter(roles=role):           
            userList.append(ds.to_json())
        return userList

           
    def get_role_perms(self,request):  
        role = self.get_role(request)
        permsList = self.get_perms()
        groupPermsList =  [ g.id for g in role.permissions.all()]
        for ps in permsList:
            if ps["id"] in groupPermsList:ps["status"] = 1
            else:ps["status"] = 0
        return permsList        
    
    def modf_role_users(self,request):
        role = self.get_role(request)
        userList = [ int(i) for i in request.POST.getlist('users[]')]
        
        roleUsersList = []
        for user in User.objects.filter(roles=role):
            roleUsersList.append(user.id)
            
        addUsersList = list(set(userList).difference(set(roleUsersList)))
        delUsersList = list(set(roleUsersList).difference(set(userList)))
        
        #添加新增的用户
        for uid in addUsersList:
            try:
                User.objects.get(id=uid).roles.add(role)
            except Exception as ex:
                logger.warn(msg="删除用户组失败: {ex}".format(ex=ex))
            
        #删除去掉的用户
        for uid in delUsersList:
            try:
                User.objects.get(id=uid).roles.remove(role)
            except Exception as ex:
                logger.warn(msg="删除用户组失败: {ex}".format(ex=ex))  
                            
    def modf_role_perm(self,request):
        role = self.get_role(request)

        userPermList = []
        for perm in role.permissions.all():
            userPermList.append(perm.id)
        permList = [ int(i) for i in request.POST.getlist('perms[]')]
        addPermList = list(set(permList).difference(set(userPermList)))
        delPermList = list(set(userPermList).difference(set(permList)))
        #添加新增的权限
        for permId in addPermList:
            perm = Permission.objects.get(id=permId)
            Role.objects.get(id=request.POST.get('id')).permissions.add(perm)
        #删除去掉的权限
        for permId in delPermList:
            perm = Permission.objects.get(id=permId)
            Role.objects.get(id=request.POST.get('id')).permissions.remove(perm) 

class StructureManage(object):
    def __init__(self):
        super(StructureManage, self).__init__()  
        
    def get_node_json_user(self,structure):
        dataList = []
        for ds in structure.user_set.all():
            dataList.append(ds.to_json())
        return dataList
    
    def get_assets(self,structure):
        return structure.user_set.all()
    
    def get_all_sub_node(self,structures):
        dicts = []
        for ds in structures:
            if ds.last_node() > 0:dicts.append(ds.to_json())
        return dicts
    
    def get_nodes_all_children(self,tree_id,lft,rght):
        return Structure.objects.filter(tree_id=tree_id,lft__gt=lft,rght__lt=rght)

    def get_node_unallocated_json_member(self,structure):
        dataList = []
        for ds in User.objects.filter(~Q(department=structure)):
            dataList.append(ds.to_json())  
        return dataList 
    
    def get_node_unallocated_json_assets(self,structure):
        dataList = []
        for ds in Assets.objects.filter(~Q(department_tree=structure)):
            dataList.append(ds.to_json())  
        return dataList 