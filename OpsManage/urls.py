"""Sparrow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from OpsManage.views import index,users


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index.Index.as_view()),
    url(r'^login/$', index.login),
    url(r'^logout/$', index.logout),
    url(r'^403/$', index.Permission.as_view()),
    url(r'^404/$', index.PageError.as_view()),
    url(r'^user/manage/$', users.UserManage.as_view()),
    url(r'^user/center/$', users.UserCenter.as_view()),
    url(r'^group/manage/$', users.GroupManage.as_view()),
    url(r'^api/',include('api.urls')),
    url(r'^assets/',include('asset.urls')),
    url(r'^deploy/',include('deploy.urls')),
    url(r'^db/',include('databases.urls')),
    url(r'^sched/',include('sched.urls')),
    url(r'^apps/',include('cicd.urls')),
    url(r'^nav/',include('navbar.urls')),
    url(r'^websocket/',include('websocket.urls')),
    url(r'^wiki/',include('wiki.urls')),
    url(r'^order/',include('orders.urls')),
    url(r'^apply/',include('apply.urls')),
]
