"""OpsManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
from django.contrib import admin
from OpsManage.views import (index,assets,cron,deploy,
                             ansible,users,wssh,task,
                             database,elfinder)
from OpsManage.views.elfinder import finder
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^$',index.index),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',index.login),  
    url(r'^logout',index.logout), 
    url(r'^config',index.config), 
    url(r'^noperm',index.noperm), 
    url(r'^assets_config',assets.assets_config), 
    url(r'^assets_add',assets.assets_add), 
    url(r'^assets_list',assets.assets_list), 
    url(r'^assets_mod/(?P<aid>[0-9]+)/$',assets.assets_modf), 
    url(r'^assets_view/(?P<aid>[0-9]+)/$',assets.assets_view),
    url(r'^assets_facts',assets.assets_facts),
    url(r'^assets_log/(?P<page>[0-9]+)/$',assets.assets_log),
    url(r'^assets_import/',assets.assets_import),
    url(r'^assets_search/',assets.assets_search),
    url(r'^assets_server/',assets.assets_server),
    url(r'^assets/batch/update/',assets.assets_update),
    url(r'^assets/batch/delete/',assets.assets_delete),
    url(r'^assets/batch/dumps/',assets.assets_dumps),    
    url(r'^assets/groups/(?P<id>[0-9]+)/$',assets.assets_groups),
    url(r'^cron_add',cron.cron_add),
    url(r'^cron_list/(?P<page>[0-9]+)/$',cron.cron_list),
    url(r'^cron_config',cron.cron_config),
    url(r'^cron_log/(?P<page>[0-9]+)/$',cron.cron_log),
    url(r'^cron_mod/(?P<cid>[0-9]+)/$',cron.cron_mod),
    url(r'^deploy_add',deploy.deploy_add),
    url(r'^deploy_list',deploy.deploy_list),
    url(r'^deploy_log/(?P<page>[0-9]+)/$',deploy.deploy_log),
    url(r'^deploy_mod/(?P<pid>[0-9]+)/$',deploy.deploy_modf),
    url(r'^deploy_init/(?P<pid>[0-9]+)/$',deploy.deploy_init),
    url(r'^deploy_version/(?P<pid>[0-9]+)/$',deploy.deploy_version),    
    url(r'^deploy_run/(?P<pid>[0-9]+)/$',deploy.deploy_run),
    url(r'^deploy_result/(?P<pid>[0-9]+)/$',deploy.deploy_result),
    url(r'^deploy_order/status/(?P<pid>[0-9]+)/$',deploy.deploy_order_status),
    url(r'^deploy_order/rollback/(?P<pid>[0-9]+)/$',deploy.deploy_order_rollback),
    url(r'^deploy_manage/(?P<pid>[0-9]+)/$',deploy.deploy_manage),
    url(r'^apps/$',ansible.apps_list),
    url(r'^apps/model/$',ansible.apps_model),
    url(r'^apps/script/online/$',ansible.apps_script_online),
    url(r'^apps/script/list/$',ansible.apps_script_list),
    url(r'^apps/script/file/(?P<pid>[0-9]+)/$',ansible.apps_script_file),
    url(r'^apps/script/run/(?P<pid>[0-9]+)/$',ansible.apps_script_online_run),
    url(r'^apps/run/$',ansible.ansible_run),
    url(r'^apps/log/$',ansible.ansible_log),
    url(r'^apps/log/(?P<model>[a-z]+)/(?P<id>[0-9]+)/$',ansible.ansible_log_view),
    url(r'^apps/playbook/upload/$',ansible.apps_upload),
    url(r'^apps/playbook/online/$',ansible.apps_online),
    url(r'^apps/playbook/file/(?P<pid>[0-9]+)/$',ansible.apps_playbook_file),  
    url(r'^apps/playbook/run/(?P<pid>[0-9]+)/$',ansible.apps_playbook_run),    
    url(r'^apps/playbook/modf/(?P<pid>[0-9]+)/$',ansible.apps_playbook_modf),   
    url(r'^apps/playbook/online/modf/(?P<pid>[0-9]+)/$',ansible.apps_playbook_online_modf),
    url(r'^apps/inventory/$',ansible.ansible_inventory), 
    url(r'^apps/inventory/modf/(?P<id>[0-9]+)/$',ansible.ansible_inventory_modf), 
    url(r'^apps/inventory/groups/(?P<id>[0-9]+)/$',ansible.ansible_inventory_groups),    
    url(r'^apps/inventory/groups/server/(?P<id>[0-9]+)/$',ansible.ansible_inventory_groups_server),
    url(r'^db/config/$',database.db_config), 
    url(r'^db/sql/control/$',database.db_sql_control), 
    url(r'^db/sql/order/run/(?P<id>[0-9]+)/$',database.db_sqlorder_run),
    url(r'^db/sql/order/osc/(?P<id>[0-9]+)/$',database.db_sqlorder_osc),
    url(r'^db/sql/ops/$',database.db_ops),
    url(r'^db/sql/dumps/$',database.db_sql_dumps),
    url(r'^db/sql/logs/(?P<page>[0-9]+)/$',database.db_sql_logs),
    url(r'^task_model/$',task.task_model),
    url(r'^task_view/$',task.task_view),
    url(r'^task_search/$',task.task_search),
    url(r'^users/manage$',users.user_manage),
    url(r'^register/',users.register),
    url(r'^user/(?P<uid>[0-9]+)/$',users.user),
    url(r'^user/center/$',users.user_center),
    url(r'^user/server/(?P<uid>[0-9]+)/$',users.user_server),
    url(r'^group/(?P<gid>[0-9]+)/$',users.group),
    url(r'^webssh/(?P<sid>[0-9]+)/$',wssh.wssh),
    url(r'^roles/',elfinder.finder),
    url(r'^elfinder/',include('elfinder.urls')),
    url(r'^wiki/',include('wiki.urls')),
    url(r'^order/',include('orders.urls')),
    url(r'^api/',include('api.urls')),
    url(r'^file/',include('filemanage.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
