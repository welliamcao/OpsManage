from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import BaseRunserverCommand
# from service.apply.tasks import startup_apply_tasks
from service.apply.tasks import ApplyTaskManagerThread
from utils.logger import logger
from OpsManage.settings import _deploy_tasks, config

max_tasks = int(config.get('apply', 'max_task'))
max_expire_sec = int(config.get('apply', 'max_expire_sec'))

class Command(BaseRunserverCommand):
    def handle(self, *args, **options):
        logger.info('----------------------- startup deploy task -----------------------')
        task_thread = ApplyTaskManagerThread(max_tasks, max_expire_sec)
        task_thread.daemon = False
        task_thread.start()