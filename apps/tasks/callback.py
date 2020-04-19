#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import json, traceback
from utils.logger import logger
from celery.app.task import Task

class CallbackTask(Task):

    def __init__(self):
        super(CallbackTask, self).__init__()

    def on_success(self, retval, task_id, args, kwargs):
        try:
            logger.info('[task_id] %s, finished successfully.' % (task_id))
        except Exception as ex:
            logger.error(traceback.format_exc())

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        try:
            logger.info(('Task {0} raised exception: {1!r}\n{2!r}'.format(
                    task_id, exc, einfo.traceback)))
        except Exception as ex:
            logger.error(traceback.format_exc())