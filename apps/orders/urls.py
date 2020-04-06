from django.conf.urls import url
from . import views
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^apply/$', views.OrderApply.as_view()), 
    url(r'^list/$', views.OrderLists.as_view()), 
    url(r'^sql/handle/$', views.OrderSQLHandle.as_view()),
    url(r'^fileupload/handle/$', views.OrderFileUploadHandle.as_view()),
    url(r'^filedownload/handle/$', views.OrderFileDwonloadHandle.as_view()),
    url(r'^service/handle/$', views.OrderServiceHandle.as_view()),
    url(r'^progress/$', views.Progress.as_view()),
]