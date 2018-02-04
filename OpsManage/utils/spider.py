#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import chardet,requests

class Requests(object):
    def __init__(self):
        self.headers = {
                        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding":"gzip, deflate, sdch",
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
                        }
        self.iPhone = {
                       "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                       "Accept-Encoding":"gzip, deflate, sdch",
                       "Accept-Language":"zh-CN,zh;q=0.8",
                       "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
                       }
    def requestGet(self,url,headers=None):
        try:
            if headers!=None:
                request = requests.get(url,headers=headers,timeout=10,verify=False)
            else:
                head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',}
                request = requests.get(url,headers=head,timeout=10,verify=False)
            response = request.content
            encoding = chardet.detect(response).get('encoding')
            if encoding == 'ISO-8859-2': response = response.decode('gbk', 'ignore').encode('gb2312', 'ignore')
            elif encoding=='GB2312': response = response.decode('gbk', 'ignore').encode('utf-8', 'ignore')
            elif encoding=='EUC-TW': response = response.decode('gbk', 'ignore').encode('utf-8', 'ignore')
            else: response = response.decode(encoding, 'ignore').encode('utf-8', 'ignore')
        except Exception,e:
            print e
            return False
        return response
    
    def requestPost(self,url,data,headers=None):
        try:
            if headers!=None:
                response = requests.post(url,data,headers=self.headers)
            else:
                head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',}
                response = requests.post(url,data,headers=head,timeout=3)
        except Exception,e:
            print e
            return False
        return response 


class Spider(Requests):
        
    def chat(self,msg):
        apiUrl = 'http://www.tuling123.com/openapi/api'
        data = {
                'key'    : 'somekey',
                'info'   : msg,
                'userid' : 'yourid',
            }
        try:
            response = self.requestPost(apiUrl, data=data).json()
            news = response.get('list')
            url = response.get('url')
            content = ''
            if news:
                for ds in response.get('list'):
                    info = ds.get('info')
                    article = ds.get('article')
                    if info:result = info
                    elif article:result = article
                    content = result + '\n源文地址：' + ds.get('detailurl') + '\n' + content
                return response.get('text') + '\n' + content
            elif url:return response.get('text') + '\n点击查看：' + url
            else:return response.get('text')
        except Exception,e:
            msg = '**[chat]** Error: ' + str(e)
            return '报告大人：问题太难了，小的回答不上[尴尬]~' 