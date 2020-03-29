from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^cron/$', views.CronManage.as_view()), 
    url(r'^celery/$', views.CeleryManage.as_view()), 
    url(r'^apsched/$', views.ApsManage.as_view()), 
    url(r'^apsched/node/$', views.ApsNodeManage.as_view()), 
    url(r'^apsched/node/jobs/$', views.ApsNodeJobsManage.as_view()), 
]