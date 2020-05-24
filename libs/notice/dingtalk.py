#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json
from utils.logger import logger
from .base import NotcieBase
from libs.request import http_request

class DtalkNotice(NotcieBase):
    
    def __init__(self):
        super(DtalkNotice, self).__init__()
    
    def send(self,**kwargs):
        payload = {'msgtype': 'text', 'text': {'content': kwargs.get("content")}}
        status_code, respone = http_request.Post(url=kwargs.get("url"), data=json.dumps(payload))
        if status_code != 200:
            logger.error("[send dingtalk msg failed] %s" % respone)
            return False
        return True