#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
# Create your views here.

from django.shortcuts import redirect, render

def webssh(request):
    return render(request, 'websocket/ssh.html')