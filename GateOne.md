## 安装配置GateOne
本文用来介绍OpsManage结合Gateone实现Webssh功能


## 下载GateOne：
 * （方式一）网盘地址：[https://pan.baidu.com/s/1i5tcEvb](https://pan.baidu.com/s/1i5tcEvb)
 * （方式二）Github地址：[https://github.com/liftoff/GateOne](https://github.com/liftoff/GateOne)


## 安装GateOne
```
# cd gateone
# python setup.py install
```

## 配置GateOne
一、生成api_key
```
# cd /etc/gateone/conf.d
# gateone --new_api_key
# vim 10server.conf
```
修改origins的值，改成下面一样
```
"origins": ["*"],
```
配置api认证方式
```
# vim 20authentication.conf
把"auth": "none" 修改为 "auth": "api",
```
查看key与secret
```
# cat 30api_keys.conf
{
    "*": {
        "gateone": {
            "api_keys": {
                "NTA3ZGY5Y2VjZjg3NGRhOGI3YjE3NTZmMjViNzRhNjY3O": "ZjFkMzFjNzk0MjI4NGYwYmJlMDM5MjFkOGJmMTEwMmFlO"
            }
        }
    }
}
```
启动GateOne
```
# /etc/init.d/gateone start
```
## 配置OpsManage
一、修改settings.py配置文件
```
# cd /path/OpsManage/OpsManage
# vim settings.py
修改GateOne配置
'''GateOne Setting'''
GATEONE_SERVER = 'https://192.168.88.233'   ##改成GateOne运行的地址
GATEONE_API_URL = 'http://192.168.88.233:8000'  #改成OpsManage运行的地址
GATEONE_KEY = 'NTA3ZGY5Y2VjZjg3NGRhOGI3YjE3NTZmMjViNzRhNjY3O' #对应30api_keys.conf的key
GATEONE_SECRET = 'ZjFkMzFjNzk0MjI4NGYwYmJlMDM5MjFkOGJmMTEwMmFlO' #对应30api_keys.conf的secret

```
二、安装OpsManage
>  参照OpsManage的[readme.md](https://github.com/welliamcao/OpsManage/blob/beta/README.md)进行安装

三、开启WebSSH功能
> 全局配置 -> 开启WebSSH
