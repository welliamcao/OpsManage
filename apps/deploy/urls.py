from django.conf.urls import url
from . import views
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^model/$', views.DelolyModel.as_view()), 
    url(r'^inventory/$', views.DeployInventory.as_view()),
    url(r'^inventory/group/(?P<id>[0-9]+)/$', views.DeployInventoryGroups.as_view()),
    url(r'^scripts/$', views.DeployScripts.as_view()),
    url(r'^playbook/$', views.DeployPlaybooks.as_view()),
    url(r'^logs/$', views.DelolyLogs.as_view()),
]