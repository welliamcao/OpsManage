from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/manage/$', views.UserManage.as_view()),
    url(r'^user/center/$', views.UserCenter.as_view()),
    url(r'^role/manage/$', views.RoleManage.as_view()),
]