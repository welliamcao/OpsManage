from django.conf.urls import url
from . import views
# from .views import article_add,upload_image,article_edit,article_index
from django.views.static import serve


urlpatterns = [
    url(r'^deploy/apply/$', views.deploy_ask), 
    url(r'^deploy/apply/(?P<pid>[0-9]+)/$', views.deploy_apply),
    url(r'^sql/apply/$', views.db_sqlorder_audit),
    url(r'^file/upload/apply/$', views.file_upload_audit),
    url(r'^file/upload/list/(?P<page>[0-9]+)/$', views.file_upload_list),
    url(r'^file/download/apply/$', views.file_download_audit),    
    url(r'^file/download/list/(?P<page>[0-9]+)/$', views.file_download_list),
    url(r'^list/(?P<page>[0-9]+)/$', views.order_list),
    url(r'^search/$', views.order_search),
]