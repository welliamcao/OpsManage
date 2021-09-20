#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

class ApplicationTasks(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request, 'apply/tasks/apply_tasks.html',{"user":request.user})   