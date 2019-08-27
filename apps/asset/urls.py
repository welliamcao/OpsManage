from django.conf.urls import url
from . import views
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^config/$', views.Config.as_view()), 
    url(r'^manage/$', views.AssetsManage.as_view()), 
    url(r'^list/$', views.AssetsList.as_view()), 
    url(r'^modf/(?P<id>[0-9]+)/$', views.AssetsModf.as_view()), 
    url(r'^search/$', views.AssetsSearch.as_view()), 
    url(r'^batch/$', views.AssetsBatch.as_view()), 
    url(r'^server/query/$', views.AssetsServer.as_view()), 
    url(r'^tree/$', views.AssetsTree.as_view()), 
    url(r'^import/$', views.AssetsImport.as_view()), 
]