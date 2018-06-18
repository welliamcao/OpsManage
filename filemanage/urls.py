from django.conf.urls import url
from . import views
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^upload/run/(?P<id>[0-9]+)/$', views.file_upload_run), 
    url(r'^download/run/(?P<id>[0-9]+)/$', views.file_download_run), 
    url(r'^downloads/$', views.file_downloads), 
]