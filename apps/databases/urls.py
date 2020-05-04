from django.conf.urls import url
from apps.databases.mysql import views
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^mysql/config/$', views.DatabaseConfigs.as_view()), 
    url(r'^mysql/manage/$', views.DatabaseManage.as_view()), 
#     url(r'^users/$', views.DatabaseUsers.as_view()), 
    url(r'^mysql/query/$', views.DatabaseQuery.as_view()), 
    url(r'^mysql/execute/histroy/$', views.DatabaseExecuteHistroy.as_view()), 
]