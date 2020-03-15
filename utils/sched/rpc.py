#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import requests, json, hashlib, time
from utils.logger import logger

class Requests(object):
    def __init__(self):
        self.headers = {
                        "Content-Type": "application/json",
                        'User-Agent':'OpsManage Sched Server',
                        }
    
    def _sig(self, content_md5, date, ak, sk):
        sha1 = hashlib.sha1(sk.encode("utf-8"))
        sha1.update(content_md5)
        sha1.update("application/json".encode("utf-8"))
        sha1.update(date)
        return "OPS-2:%s:%s" % (ak, sha1.hexdigest())

    def request(self, method, endpoint, uri, node ,body = None, cookie = None):
        url = "http://{endpoint}/api/v1/{uri}".format(endpoint=endpoint,uri=uri)
        if body:
            body = json.dumps(body).encode("utf-8")
            content_md5 = hashlib.md5(body).hexdigest()
        else:
            content_md5 = hashlib.md5(uri).hexdigest()
        date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        header = {"content-type": "application/json"}
        header['Authorization'] = self._sig(content_md5.encode("utf-8"), date.encode("utf-8"), node.ak, node.sk)
        header['Date'] = date
        try:
            r = requests.request(method, url, data=body, headers=header, cookies=cookie)
            return r.json()
        except Exception as ex:
            logger.error("request failed script exit, because {ex}".format(ex=str(ex)))
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