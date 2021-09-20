#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.base import method_decorator_adaptor

class ApplicationCenter(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request, 'apply/center/apply_center.html',{"user":request.user})   