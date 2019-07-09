from django.conf.urls import url
from .ipvs import views as ipvsViews
# from .views import article_add,upload_image,article_edit,article_index


urlpatterns = [
    url(r'^ipvs/list/$', ipvsViews.Lists.as_view()), 
    url(r'^ipvs/vip/status/(?P<id>[0-9]+)/$', ipvsViews.VipStatus.as_view()), 
    url(r'^ipvs/rs/status/(?P<id>[0-9]+)/$', ipvsViews.RsStatus.as_view()), 
    url(r'^ipvs/vip/batch/$', ipvsViews.VipBatch.as_view()), 
    url(r'^ipvs/rs/batch/$', ipvsViews.RsBatch.as_view()), 
]