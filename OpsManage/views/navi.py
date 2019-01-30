#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.forms import model_to_dict
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OpsManage.models import SiteNavigation

@login_required(login_url='/login')
def edit(request,id):
    if request.method == "GET":
        data = model_to_dict(SiteNavigation.objects.get(id=id))
        return JsonResponse({"code": 200, "msg": "success", "data":data})
    if request.method == "POST":
        mynavi = SiteNavigation.objects.filter(userof=request.user)
        navi = mynavi.get(id=id)
        navi.url = request.POST.get("url")
        navi.sitename = request.POST.get("sitename")
        navi.description = request.POST.get("description")
        try:
            navi.save()
            return HttpResponse(status=201)
        except Exception,ex:
            return HttpResponse(content=ex,status=500)

@login_required(login_url='/login')
def delete(request,id):
    mynavi = SiteNavigation.objects.filter(userof=request.user)
    try:
        navi = mynavi.get(id=id)
        navi.delete()
        return HttpResponse(status=204)
    except:
        return HttpResponse(content="删除失败，导航可能已不存在",status=404)

@login_required(login_url='/login')
def add(request):
    if request.method == "POST":
        try:
            SiteNavigation.objects.create(
                sitename=request.POST.get("sitename"),
                url=request.POST.get("url"),
                description=request.POST.get("description"),
                userof=request.user
            )
            return HttpResponse(status=201)
        except Exception,ex:
            return HttpResponse(status=500,content=ex)