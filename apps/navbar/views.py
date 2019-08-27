#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.views.generic import View
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.contrib import auth
from dao.navbar import NavBarThirdNumber
from django.contrib.auth.mixins import LoginRequiredMixin


class NavbarList(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request,'navbar/navbar_list.html',{"user":request.user})
    
class NavbarManage(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request,'navbar/navbar_manage.html',{"user":request.user})    


class NavbarThird(LoginRequiredMixin,NavBarThirdNumber,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request,'navbar/navbar_third.html',{"user":request.user,"navbar":self.get_navbar_number(id=kwagrs.get('id'))}) 