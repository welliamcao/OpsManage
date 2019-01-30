from django.conf.urls import url
from . import views
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^cron/$', views.CronManage.as_view()), 
    url(r'^celery/$', views.CeleryManage.as_view()), 
]