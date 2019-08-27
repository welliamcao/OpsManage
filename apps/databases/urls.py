from django.conf.urls import url
from . import views
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^config/$', views.DatabaseConfigs.as_view()), 
    url(r'^manage/$', views.DatabaseManage.as_view()), 
    url(r'^users/$', views.DatabaseUsers.as_view()), 
    url(r'^query/$', views.DatabaseQuery.as_view()), 
    url(r'^execute/histroy/$', views.DatabaseExecuteHistroy.as_view()), 
]