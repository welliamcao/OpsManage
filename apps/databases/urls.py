from django.conf.urls import url
from apps.databases.mysql import views as mysql_views
from apps.databases.redis import views as redis_views
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^mysql/config/$', mysql_views.DatabaseConfigView.as_view()), 
    url(r'^mysql/manage/$', mysql_views.DatabaseManageView.as_view()), 
    url(r'^mysql/query/$', mysql_views.DatabaseQueryView.as_view()), 
    url(r'^mysql/execute/history/$', mysql_views.DatabaseExecuteHistoryView.as_view()), 
    url(r'^redis/config/$', redis_views.RedisConfigView.as_view()), 
    url(r'^redis/manage/$', redis_views.RedisManageView.as_view()), 
    url(r'^redis/execute/history/$', redis_views.RedisExecuteHistoryView.as_view()),     
]