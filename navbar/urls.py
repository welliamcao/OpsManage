from django.conf.urls import url
from . import views
# from .views import article_add,upload_image,article_edit,article_index
from OpsManage.settings import MEDIA_ROOT
from django.views.static import serve
 
urlpatterns = [
    url(r'^list/$', views.NavbarList.as_view()),
    url(r'^manage/$', views.NavbarManage.as_view()),
    url(r'^third/(?P<id>[0-9]+)/$', views.NavbarThird.as_view()),
    url(r'^upload/(?P<path>(\S)*)',serve,{'document_root':MEDIA_ROOT+'navbar/'})
]