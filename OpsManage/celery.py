# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os,django
from celery import Celery,platforms
from django.conf import settings
from kombu import Queue,Exchange
from OpsManage.settings import config

platforms.C_FORCE_ROOT = True
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpsManage.settings')
django.setup()
app = Celery('OpsManage')


''' celery config '''



CELERY_QUEUES=(
                Queue('default', exchange=Exchange('default', type='direct'), routing_key='for_default'),
                Queue('ansible', exchange=Exchange('ansible', type='direct'), routing_key='for_ansible'),
            )               
CELERY_TASK_ROUTES = {
                'celery_sql.*':{'queue':'default','routing_key':'for_default'},
                'celery_assets.*':{'queue':'default','routing_key':'for_default'},
                'celery_cron.*':{'queue':'default','routing_key':'for_default'},
                'celery_sched.*':{'queue':'default','routing_key':'for_default'},
                'celery_apsched.*':{'queue':'default','routing_key':'for_default'},
                'celery_deploy.AnsibleScripts':{'queue':'ansible','routing_key':'for_ansible'},
                'celery_deploy.AnsiblePlayBook':{'queue':'ansible','routing_key':'for_ansible'},
                }   

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'

app.conf.update( 
                CELERY_BROKER_URL = 'amqp://'+ config.get('amqp', 'user') +':'+ config.get('amqp', 'password') +'@' + config.get('amqp', 'host') + ":" + config.get('amqp', 'port') + '//', 
                CELERY_RESULT_BACKEND ='django-db',              
                CELERY_TIMEZONE= 'Asia/Shanghai',
                CELERY_ENABLE_UTC= True,
                CELERYBEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler',
                CELERY_TASK_RESULT_EXPIRES=60 * 60 * 24,
                CELERYD_MAX_TASKS_PER_CHILD=40,
                CELERY_TRACK_STARTED=True,
                CELERY_TASK_SERIALIZER= 'json',
                CELERY_RESULT_SERIALIZER= 'json',
                CELERY_ACCEPT_CONTENT= ['json'],
                )
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)



