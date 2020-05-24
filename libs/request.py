# -*- coding=utf-8 -*-
'''
@author: welliam<303350019@qq.com> 
@version:1.0 2020年05月24日
'''
import requests, chardet, hashlib, time, json
from requests.auth import HTTPDigestAuth
from utils.logger import logger

class Requests(object):
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }

    def _sig(self, content_md5, date, ak, sk):
        sha1 = hashlib.sha1(sk.encode("utf-8"))
        sha1.update(content_md5)
        sha1.update("application/json".encode("utf-8"))
        sha1.update(date)
        return "OPS-2:%s:%s" % (ak, sha1.hexdigest())

    def _sig_auth(self, method, endpoint, uri, node ,body = None, cookie = None):
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
            logger.error("request failed script exit, because {ex}".format(ex=ex.__str__()))
            return ex.__str__()
                        
    def Get(self,url,headers=None):
        '''发送HTTP请求，并返回响应的内容。'''
        if headers == None:
            try:
                request = requests.get(url,headers=self.headers,timeout=5)
            except Exception as ex:
                return ex.__str__()
        else:
            try:
                request = requests.get(url,headers=headers,timeout=5)
            except Exception as ex:
                return ex.__str__()
        response = request.content
        encoding = chardet.detect(response).get('encoding')
        if encoding == 'ISO-8859-2': response = response.decode('gbk', 'ignore').encode('gb2312', 'ignore')
        elif encoding=='GB2312': response = response.decode('gbk', 'ignore').encode('utf-8', 'ignore')
        else: response = response.decode(encoding, 'ignore').encode('utf-8', 'ignore')
        return request.status_code, response
    
    def Post(self,url, data):
        try:
            request = requests.post(url, data,headers=self.headers,timeout=5)
            response = request.content          
        except Exception as ex:
            return ex.__str__()   
        return request.status_code, response
        
    @staticmethod
    def BaiscAuth(url,username,password):
        '''DigestAuth类型页面'''
        try:
            response = requests.get(url, auth=HTTPDigestAuth(username, password))
        except Exception as ex:
            return ex.__str__()
        response = response.content   
        return response
    
    def StatusCode(self,url,headers=None):
        '''发送HTTP请求，并返回响应的状态码。'''
        if headers == None:
            try:
                request = requests.get(url,headers=self.headers,timeout=5)
            except Exception as ex:
                return ex.__str__()
        else:
            try:
                request = requests.get(url,headers=headers,timeout=5)
            except Exception as ex:
                return ex.__str__()
        response = request.status_code
        return response
    
http_request = Requests()    