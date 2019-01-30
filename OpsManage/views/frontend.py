#!/usr/bin/env python
# _#_ coding:utf-8 _*_
import sys
from os import path
import json
from django.core.files.base import ContentFile
from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from OpsManage.models import FrontEndConfig,Global_Config
from OpsManage.tasks.cdn import commitcdn
from OpsManage.utils.cdnrefresh_v2_1 import Cdn
from OpsManage.utils.logger import logger

@login_required(login_url='/login')
@permission_required('OpsManage.can_exec_cdncommit',login_url='/noperm/')
def config(request):
    if request.method == "GET":
        myconfig = FrontEndConfig.objects.get(userof=request.user)
        if myconfig.cdnsecretid == None:
            cdnsecretid = ""
        else:cdnsecretid = myconfig.cdnsecretid
        if myconfig.sourcename == None:
            sourcename = ""
        else:sourcename = myconfig.sourcename
        if myconfig.chinacacheuser == None:
            chinacacheuser = ""
        else:chinacacheuser = myconfig.chinacacheuser
        return render(request,"frontend/config.html",{"user":request.user,"id":myconfig.id,"cdnsecretid":cdnsecretid,"sourcename":sourcename,"chinacacheuser":chinacacheuser})
    if request.method == "POST":
        try:
            myconfig = FrontEndConfig.objects.get(id=request.POST.get("id"))
        except Exception:
            return render(request, "frontend/config.html",{"user": request.user})
        if not request.user == myconfig.userof:
            return render(request, "frontend/config.html",{"user": request.user, "errorInfo": "非法操作，无配置权限"})
        else:
            myconfig.cdnsecretid = request.POST.get("cdnsecretid")
            myconfig.sourcename = request.POST.get("sourcename")
            myconfig.chinacacheuser = request.POST.get("chinacacheuser")
            sourcepasswd = request.POST.get("sourcepasswd")
            cdnsecretkey = request.POST.get("cdnsecretkey")
            chinacachepassword = request.POST.get("chinacachepassword")
            if len(sourcepasswd):myconfig.sourcepasswd = sourcepasswd
            if len(cdnsecretkey):myconfig.cdnsecretkey = cdnsecretkey
            if len(chinacachepassword):myconfig.chinacachepassword = chinacachepassword
            try:
                myconfig.save()
            except Exception,ex:
                return HttpResponse(status=500, content=ex)
            return HttpResponse(status=200, content="succeeded")

@login_required(login_url='/login')
@permission_required('OpsManage.can_exec_cdncommit',login_url='/noperm/')
def cdn(request):
    if request.method == "GET":
        flist=[]
        myconfig,created = FrontEndConfig.objects.get_or_create(userof=request.user)
        if not created:
            try:
                for f in myconfig.frontendlist.readlines():
                    f = f.replace("\n","")
                    if len(f):
                        flist.append(f)
            except Exception:
                flist = ""
        else:flist = ""
        return render(request,'frontend/cdn.html',{"user":request.user,"frontendlist":flist})
    if request.method == "POST":
            frontendlist = request.POST.get("editordata").replace("\r","")
            myconfig = FrontEndConfig.objects.get(userof=request.user)
            try:
                with open(myconfig.frontendlist.path, "w") as f:
                    f.write(frontendlist)
            except Exception:
                myconfig.frontendlist.save(request.user.username + ".list", ContentFile(frontendlist))
                return HttpResponse(status=201)
            return HttpResponse(status=201)

@login_required(login_url='/login')
@permission_required('OpsManage.can_exec_cdncommit',login_url='/noperm/')
def refresh_or_prehot(request):
    cdntype = request.GET.get("type")
    try:
        keyconfig = int(Global_Config.objects.get(id=1).apikey)
    except Exception:
        keyconfig = 1
    if request.method == "POST":
        try:
            if keyconfig:
                myconfig = FrontEndConfig.objects.filter(cdnsecretid__isnull=False,cdnsecretkey__isnull=False).get(userof=request.user)
                cdnsecretid = str(myconfig.cdnsecretid)
                cdnsecretkey = str(myconfig.cdnsecretkey)
            else:
                globalconfig = FrontEndConfig.objects.filter(cdnsecretid__isnull=False,cdnsecretkey__isnull=False).get(userof__is_superuser=1)
                cdnsecretid = str(globalconfig.cdnsecretid)
                cdnsecretkey = str(globalconfig.cdnsecretkey)
        except Exception,ex:
            return HttpResponse(content="APIkey未配置",status=404)
        if cdntype=="refresh":
            urllist = []
            dirlist = []
            urlslist = json.loads(request.POST.get("urlslist"))
            for x in urlslist:
                if x.endswith("/"):
                    dirlist.append(x)
                else:
                    urllist.append(x)
            if len(urllist):
                for i in range(len(urllist)):
                    urllist.insert(i*2,"--urls")
                try:
                    commitcdn.delay(['RefreshCdnUrl', '-u', cdnsecretid, '-p',
                                     cdnsecretkey] + urllist)
                except Exception, ex:
                    return HttpResponse(content=ex, status=500)
            if len(dirlist):
                for i in range(len(dirlist)):
                    dirlist.insert(i*2,"--dirs")
                try:
                    commitcdn.delay(['RefreshCdnDir', '-u', cdnsecretid, '-p',
                                     cdnsecretkey] + dirlist)
                except Exception, ex:
                    return HttpResponse(content=ex, status=500)
            return HttpResponse(status=200)
        if cdntype=="prehot":
            urlslist =json.loads(request.POST.get("urlslist"))
            if len(urlslist):
                for i in range(len(urlslist)):
                    urlslist.insert(i*2,"--urls")
                try:
                    commitcdn.delay(['CdnPusherV2', '-u', cdnsecretid, '-p',
                                     cdnsecretkey] + urlslist)
                except Exception, ex:
                    return HttpResponse(content=ex, status=500)
            return HttpResponse(status=200)

@login_required(login_url='/login')
@permission_required('OpsManage.can_exec_cdncommit',login_url='/noperm/')
def queryrecord(request):
    try:
        keyconfig = int(Global_Config.objects.get(id=1).apikey)
    except Exception:
        keyconfig = 1
    try:
        if keyconfig:
            myconfig = FrontEndConfig.objects.filter(cdnsecretid__isnull=False, cdnsecretkey__isnull=False).get(
                userof=request.user)
            cdnsecretid = str(myconfig.cdnsecretid)
            cdnsecretkey = str(myconfig.cdnsecretkey)
        else:
            globalconfig = FrontEndConfig.objects.filter(cdnsecretid__isnull=False, cdnsecretkey__isnull=False).get(
                userof__is_superuser=1)
            cdnsecretid = str(globalconfig.cdnsecretid)
            cdnsecretkey = str(globalconfig.cdnsecretkey)
    except Exception, ex:
        return HttpResponse(content="APIkey未配置", status=404)
    if request.method == "GET":
        return render(request, 'frontend/cdnrecord.html', {"user": request.user})
    if request.method == "POST":
        recordtype = request.GET.get("type")
        if recordtype == "refresh":
            startTime = request.POST.get("startTime")
            endTime = request.POST.get("endTime")
            try:
                cdn = Cdn()
                rt = cdn.parse_args(['GetCdnRefreshLog', '-u', cdnsecretid, '-p',
                                 cdnsecretkey,'--startDate',startTime,'--endDate',endTime])
            except Exception, ex:
                return HttpResponse(content=ex, status=500)
            try:
                records = json.dumps(rt)
            except Exception,ex:
                logger.warn(msg="api没有返回json对象:{ex}".format(ex=rt))
            return JsonResponse(records,safe=False)
        if recordtype == "prehot":
            startTime = request.POST.get("startTime")
            endTime = request.POST.get("endTime")
            try:
                cdn = Cdn()
                rt = cdn.parse_args(['GetPushLogs', '-u', cdnsecretid, '-p',
                                 cdnsecretkey,'--startDate',startTime,'--endDate',endTime])
            except Exception, ex:
                return HttpResponse(content=ex, status=500)
            return HttpResponse(content=rt, status=200)

def chinacache_qcloudcdn(request):
    try:
        myconfig = FrontEndConfig.objects.filter(cdnsecretid__isnull=False, cdnsecretkey__isnull=False).get(
            userof__is_superuser=1)
        cdnsecretid = str(myconfig.cdnsecretid)
        cdnsecretkey = str(myconfig.cdnsecretkey)
    except Exception, ex:
        return HttpResponse(content="APIkey未配置", status=404,charset='gb2312')
    if request.method == "GET":
        cdn = Cdn()
        user = request.GET.get('user')
        pswd = request.GET.get('pswd')
        if user != None and pswd != None:
            confirm = FrontEndConfig.objects.filter(chinacacheuser=user,
                                                    chinacachepassword=pswd).count()
        else:confirm=0
        if confirm:
            urlslist = request.GET.get("urls")
            dirslist = request.GET.get("dirs")
            if urlslist is not None:
                urlslist = urlslist.splitlines()
                for i in range(len(urlslist)):
                    urlslist.insert(i * 2, "--urls")
                try:
                    rt = cdn.parse_args(['RefreshCdnUrl', '-u', cdnsecretid, '-p',
                                     cdnsecretkey] + urlslist)
                    urlsucesscont = rt.get('count')
                except Exception, ex:
                    content = '<xml version="1.0" encoding="utf-8" ?>\r\n' \
                              '<result>failed</result>'
                    response = HttpResponse(content=content,content_type='text/html',status=500,charset='gb2312')
                    response.__setitem__('whatsup','content="error"')
                    return response
            else:urlsucesscont = 0
            if dirslist is not None:
                dirslist = dirslist.splitlines()
                for i in range(len(dirslist)):
                    dirslist.insert(i * 2, "--dirs")
                try:
                    rt = cdn.parse_args(['RefreshCdnDir', '-u', cdnsecretid, '-p',
                                     cdnsecretkey] + dirslist)
                    dirsucesscont = rt.get('count')
                except Exception, ex:
                    content = '<xml version="1.0" encoding="utf-8" ?>\r\n' \
                              '<result>failed</result>'
                    response = HttpResponse(content=content, content_type='text/html', status=500,charset='gb2312')
                    response.__setitem__('whatsup', 'content="error"')
                    return response
            else:dirsucesscont = 0

            content = '<xml version="1.0" encoding="utf-8" ?>\r\n' \
                      '<result>\r\n' \
                        '<url>'+str(urlsucesscont)+'</url>\r\n' \
                        '<dir>'+str(dirsucesscont)+'</dir>\r\n' \
                      '</result>'
            response = HttpResponse(content=content, content_type='text/html', status=200,charset='gb2312')
            response.__setitem__('whatsup', 'content="succeed"')
            return response

        else:
            return HttpResponse(content="NO_USER_EXISTS",status=403,charset='gb2312')

    if request.method == "HEAD":
        user = request.GET.get('user')
        pswd = request.GET.get('pswd')
        if user != None and pswd != None:
            confirm = FrontEndConfig.objects.filter(chinacacheuser=user,
                                                    chinacachepassword=pswd).count()
        else:confirm=0
        if confirm:
            cdn = Cdn()
            urlslist = request.GET.get("urls")
            dirslist = request.GET.get("dirs")
            if urlslist is not None:
                urlslist = urlslist.splitlines()
                for i in range(len(urlslist)):
                    urlslist.insert(i * 2, "--urls")
                try:
                    rt = cdn.parse_args(['RefreshCdnUrl', '-u', cdnsecretid, '-p',
                                         cdnsecretkey] + urlslist)
                    urlcount = rt.get('count')
                except Exception, ex:
                    response = HttpResponse(status=500,charset='gb2312')
                    response.__setitem__('whatsup', 'content="error"')
                    return response
            else:urlcount = 0

            if dirslist is not None:
                dirslist = dirslist.splitlines()
                for i in range(len(dirslist)):
                    dirslist.insert(i * 2, "--dirs")
                try:
                    rt = cdn.parse_args(['RefreshCdnDir', '-u', cdnsecretid, '-p',
                                         cdnsecretkey] + dirslist)
                    dircount = rt.get('count')
                except Exception, ex:
                    response = HttpResponse(status=500,charset='gb2312')
                    response.__setitem__('whatsup', 'content="error"')
                    return response
            else:dircount = 0
            if (urlcount + dircount) > 0:
                response = HttpResponse(status=200,charset='gb2312')
                response.__setitem__('whatsup', 'content="succeed"')
                return response
            else:
                response = HttpResponse(status=500,charset='gb2312')
                response.__setitem__('whatsup', 'content="error"')
                return response

        else:
            return HttpResponse(status=403)