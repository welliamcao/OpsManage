#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
SQL_PERMISSIONS = {
   "CREATE_USER":{
       "desc":"DDL-创建用户"
   },
   "CREATE_DATABASE":{
       "desc":"DDL-创建数据库"
   },
   "CREATE_TABLE":{
       "desc":"DDL-创建表权限"
    },
   "CREATE_VIEW":{
       "desc":"DDL-创建视图"
   },
   "CREATE_INDEX":{
       "desc":"DDL-创建索引"
   },
   "CREATE_EVENT":{
       "desc":"DDL-创建事件"
   },
   "CREATE_TRIGGER":{
       "desc":"DDL-创建触发器"
   },
   "CREATE_PROCEDURE":{
       "desc":"DDL-创建存储过程"
   },
   "CREATE_FUNCTION":{
       "desc":"DDL-创建自定义函数"
   },
   "DROP_TABLE":{
       "desc":"DDL-删除表"
   },
   "ALTER_TABLE":{
       "desc":"DDL-修改表"
   }, 
   "DESTRIBE":{
       "desc":"DDL-查看表结构"
   },   
   "SHOW_CREATE":{
       "desc":"DDL-查看表结构"
   },   
   "RENAME_TABLE":{
       "desc":"DDL-重命名表"
   },  
   "TRUNCATE_TABLE":{
       "desc":"DDL-清空表"
   },     
   
      
   "INSERT_INTO":{
       "desc":"DML-写入数据"
   },    
   "UPDATE":{
       "desc":"DML-更新数据"
   },
   "DELETE_FROM":{
       "desc":"DML-删除数据"
   },
   "SELECT":{
       "desc":"DQL-查询数据"
   },
   "EXPLAIN":{
       "desc":"DQL-数据分析"
   },
   
   
   "SHOW_TABLES":{
       "desc":"SHOW-显示当前数据库中所有表"
   },
   "SHOW_INDEX":{
       "desc":"SHOW-显示表的索引"
   },
   "SHOW_STATUS":{
       "desc":"SHOW-显示系统状态"
   },
   "SHOW_VARIABLES":{
       "desc":"SHOW-显示系统变量"
   },
   "SHOW_PROCESSLIST":{
       "desc":"SHOW-显示系统进程"
   },
   "SHOW_ENGINES":{
       "desc":"SHOW-显示系统存储引擎"
   },
   "SHOW_INNODB":{
       "desc":"SHOW-显示INNODB存储引擎"
   },
   "SHOW_LOGS":{
       "desc":"SHOW-显示存储引擎的日志"
   },
   "SHOW_WARNINGS":{
       "desc":"SHOW-显示警告"
   },
   "SHOW_ERRORS":{
       "desc":"SHOW-显示错误"
   }
     
}

#
SQL_DICT_HTML = """<html>
    <meta charset="utf-8">
    <title> {{db_name}}数据库  表结构字典</title>
    <style>
        body,td,th {font-family:"微软雅黑"; font-size:12px;}  
        table,h1,p{width:960px;margin:0px auto;}
        table { border-collapse:collapse;border:1px solid #CCC;background:#C0C0C0; }  
        table caption{text-align:left; background-color:#fff; line-height:2em; font-size:14px; font-weight:bold; }  
        table th{text-align:left; font-weight:bold;height:26px; line-height:26px; font-size:12px; border:1px solid #CCC;padding-left:5px;}  
        table td{height:20px; font-size:12px; border:1px solid #CCC;background-color:#fff;padding-left:5px; word-break:break-all;}  
    </style>
    <body>
    <h1 style="text-align:center;">{{host}}:{{port}} <code>{{ db_name }}</code> 数据字典 (共 {{ total_tables }} 个表)</h1>
    <p style="text-align:center;margin:20px auto;"><strong>生成时间：</strong>{{ export_time }}</p>
    {{ dict_data }}
    </body>
    </html>
    """