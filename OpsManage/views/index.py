#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.views.generic import View
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin

class Index(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request,'base.html',{"user":request.user})



def login(request):
    if request.session.get('username') is not None:
        return HttpResponseRedirect('/',{"user":request.user})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = auth.authenticate(username=username,password=password)
        if user and user.is_active:
            auth.login(request,user)
            request.session['username'] = username
            return HttpResponseRedirect('/',{"user":request.user})
        else:
            if request.method == "POST":
                return render(request,'login.html',{"login_error_info":"用户名或者密码错误","username":username},)  
            else:
                return render(request,'login.html') 
            
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')   




class Permission(View):
    def get(self, request, *args, **kwagrs):     
        return render(request,'403.html',{"user":request.user})

    def put(self, request, *args, **kwagrs):  
        return JsonResponse({'msg':"你没有权限操作此项","code":403,'data':[]})
    
    def post(self, request, *args, **kwagrs):     
        return JsonResponse({'msg':"你没有权限操作此项","code":403,'data':[]})
    
    def delete(self, request, *args, **kwagrs):     
        return JsonResponse({'msg':"你没有权限操作此项","code":403,'data':[]})
    
class PageError(View):
    def get(self, request, *args, **kwagrs):     
        return render(request,'404.html',{"user":request.user})    
    
    def put(self, request, *args, **kwagrs):  
        return JsonResponse({'msg':"你访问的地址不存在","code":404,'data':[]})
    
    def post(self, request, *args, **kwagrs):     
        return JsonResponse({'msg':"你访问的地址不存在","code":404,'data':[]})
    
    def delete(self, request, *args, **kwagrs):     
        return JsonResponse({'msg':"你访问的地址不存在","code":404,'data':[]})    