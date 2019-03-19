#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import requests,json
from utils.logger import logger

class Requests(object):
    def __init__(self):
        self.headers = {
                        "Content-Type": "application/json",
                        'User-Agent':'OpsManage Sched Server',
                        }
    def get(self,url,headers=None):
        try:
            if headers!=None:
                response = requests.get(url,headers=headers,timeout=10,verify=False)
            else:
                head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',}
                response = requests.get(url,headers=head,timeout=10,verify=False)
            return response.json()
        except Exception as ex:
            logger.error("Get {url} failed {ex}".format(url=url,ex=str(ex)))
            return False
    
    def post(self,url,data,token):
        try:
            self.headers["Authorization"] = "OpsSched {token}".format(token=token)
            response = requests.post(url,json.dumps(data),headers=self.headers,timeout=3)
            return response.json()
        except Exception as ex:
            logger.error("Post {url} with {args} failed {ex}, agent return {content}.".format(url=url,args=data,ex=str(ex)),content=response.content)
            return str(ex)
    
sched_rpc = Requests()

if __name__ == '__main__': 
    data = {
            "status": "running",
            "sched": {
                "seconds": 5,
            },
            "cmd": "date",
            "type": "interval",
            "id": "550be34b-0b67-469c-a7cb-e81fa27a3f32"
        }
    res = sched_rpc.post("http://192.168.1.234:12345/api/v1/edit", json.dumps(data), "7d74d9e8762c4ed7a04fd34cb6de2822")
    print(res.content)