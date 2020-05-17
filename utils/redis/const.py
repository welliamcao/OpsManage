#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
CMD_PERMISSIONS = {
    "APPEND": {
        "desc": "追加一个值到key上"
    }, 
    "AUTH": {
        "desc": "验证服务器命令"
    }, 
    "BGREWRITEAOF": {
        "desc": "异步重写追加文件命令"
    }, 
    "BGSAVE": {
        "desc": "异步保存数据集到磁盘上"
    }, 
    "BITCOUNT": {
        "desc": "统计字符串指定起始位置的字节数"
    }, 
    "BITFIELD": {
        "desc": "Perform arbitrary bitfield integer operations on strings"
    }, 
    "BITOP": {
        "desc": "Perform bitwise operations between strings"
    }, 
    "BITPOS": {
        "desc": "Find first bit set or clear in a string"
    }, 
    "BLPOP": {
        "desc": "删除，并获得该列表中的第一元素，或阻塞，直到有一个可用"
    }, 
    "BRPOP": {
        "desc": "删除，并获得该列表中的最后一个元素，或阻塞，直到有一个可用"
    }, 
    "BRPOPLPUSH": {
        "desc": "弹出一个列表的值，将它推到另一个列表，并返回它;或阻塞，直到有一个可用"
    }, 
    "BZPOPMAX": {
        "desc": "Remove and return the member with the highest score from one or more sorted sets, or block until one is available"
    }, 
    "BZPOPMIN": {
        "desc": "Remove and return the member with the lowest score from one or more sorted sets, or block until one is available"
    }, 
    "CLIENT": {
        "desc": "客户端相关命令"
    }, 
    "CLUSTER": {
        "desc": "CLUSTER相关命令"
    },     
    "COMMAND": {
        "desc": "Get array of Redis command details"
    },
    "CONFIG": {
        "desc": "获取配置参数相关命令"
    }, 
    "DBSIZE": {
        "desc": "返回当前数据库里面的keys数量"
    }, 
    "DEBUG": {
        "desc": "获取一个key的debug信息"
    },  
    "DECR": {
        "desc": "整数原子减1"
    }, 
    "DECRBY": {
        "desc": "原子减指定的整数"
    }, 
    "DEL": {
        "desc": "删除指定的key（一个或多个）"
    }, 
    "DISCARD": {
        "desc": "丢弃所有 MULTI 之后发的命令"
    }, 
    "DUMP": {
        "desc": "导出key的值"
    }, 
    "ECHO": {
        "desc": "回显输入的字符串"
    }, 
    "EVAL": {
        "desc": "在服务器端执行 LUA 脚本"
    }, 
    "EVALSHA": {
        "desc": "在服务器端执行 LUA 脚本"
    }, 
    "EXEC": {
        "desc": "执行所有 MULTI 之后发的命令"
    }, 
    "EXISTS": {
        "desc": "查询一个key是否存在"
    }, 
    "EXPIRE": {
        "desc": "设置一个key的过期的秒数"
    }, 
    "EXPIREAT": {
        "desc": "设置一个UNIX时间戳的过期时间"
    }, 
    "FLUSHALL": {
        "desc": "清空所有数据库命令"
    }, 
    "FLUSHDB": {
        "desc": "清空当前的数据库命令"
    }, 
    "GEOADD": {
        "desc": "添加一个或多个地理空间位置到sorted set"
    }, 
    "GEODIST": {
        "desc": "返回两个地理空间之间的距离"
    }, 
    "GEOHASH": {
        "desc": "返回一个标准的地理空间的Geohash字符串"
    }, 
    "GEOPOS": {
        "desc": "返回地理空间的经纬度"
    }, 
    "GEORADIUS": {
        "desc": "查询指定半径内所有的地理空间元素的集合。"
    }, 
    "GEORADIUSBYMEMBER": {
        "desc": "查询指定半径内匹配到的最大距离的一个地理空间元素。"
    }, 
    "GET": {
        "desc": "返回key的value"
    }, 
    "GETBIT": {
        "desc": "返回位的值存储在关键的字符串值的偏移量。"
    }, 
    "GETRANGE": {
        "desc": "获取存储在key上的值的一个子字符串"
    }, 
    "GETSET": {
        "desc": "设置一个key的value，并获取设置前的值"
    }, 
    "HDEL": {
        "desc": "删除一个或多个Hash的field"
    }, 
    "HEXISTS": {
        "desc": "判断field是否存在于hash中"
    }, 
    "HGET": {
        "desc": "获取hash中field的值"
    }, 
    "HGETALL": {
        "desc": "从hash中读取全部的域和值"
    }, 
    "HINCRBY": {
        "desc": "将hash中指定域的值增加给定的数字"
    }, 
    "HINCRBYFLOAT": {
        "desc": "将hash中指定域的值增加给定的浮点数"
    }, 
    "HKEYS": {
        "desc": "获取hash的所有字段"
    }, 
    "HLEN": {
        "desc": "获取hash里所有字段的数量"
    }, 
    "HMGET": {
        "desc": "获取hash里面指定字段的值"
    }, 
    "HMSET": {
        "desc": "设置hash字段值"
    }, 
    "HSCAN": {
        "desc": "迭代hash里面的元素"
    }, 
    "HSET": {
        "desc": "设置hash里面一个字段的值"
    }, 
    "HSETNX": {
        "desc": "设置hash的一个字段，只有当这个字段不存在时有效"
    }, 
    "HSTRLEN": {
        "desc": "获取hash里面指定field的长度"
    }, 
    "HVALS": {
        "desc": "获得hash的所有值"
    }, 
    "INCR": {
        "desc": "执行原子加1操作"
    }, 
    "INCRBY": {
        "desc": "执行原子增加一个整数"
    }, 
    "INCRBYFLOAT": {
        "desc": "执行原子增加一个浮点数"
    }, 
    "INFO": {
        "desc": "获得服务器的详细信息"
    }, 
    "KEYS": {
        "desc": "查找所有匹配给定的模式的键"
    }, 
    "LASTSAVE": {
        "desc": "获得最后一次同步磁盘的时间"
    }, 
    "LINDEX": {
        "desc": "获取一个元素，通过其索引列表"
    }, 
    "LINSERT": {
        "desc": "在列表中的另一个元素之前或之后插入一个元素"
    }, 
    "LLEN": {
        "desc": "获得队列(List)的长度"
    }, 
    "LPOP": {
        "desc": "从队列的左边出队一个元素"
    }, 
    "LPUSH": {
        "desc": "从队列的左边入队一个或多个元素"
    }, 
    "LPUSHX": {
        "desc": "当队列存在时，从队到左边入队一个元素"
    }, 
    "LRANGE": {
        "desc": "从列表中获取指定返回的元素"
    }, 
    "LREM": {
        "desc": "从列表中删除元素"
    }, 
    "LSET": {
        "desc": "设置队列里面一个元素的值"
    }, 
    "LTRIM": {
        "desc": "修剪到指定范围内的清单"
    }, 
    "MGET": {
        "desc": "获得所有key的值"
    }, 
    "MIGRATE": {
        "desc": "原子性的将key从redis的一个实例移到另一个实例"
    }, 
    "MONITOR": {
        "desc": "实时监控服务器"
    }, 
    "MOVE": {
        "desc": "移动一个key到另一个数据库"
    }, 
    "MSET": {
        "desc": "设置多个key value"
    }, 
    "MSETNX": {
        "desc": "设置多个key value,仅当key存在时"
    }, 
    "MULTI": {
        "desc": "标记一个事务块开始"
    }, 
    "OBJECT": {
        "desc": "检查内部的再分配对象"
    }, 
    "PERSIST": {
        "desc": "移除key的过期时间"
    }, 
    "PEXPIRE": {
        "desc": "设置key的有效时间以毫秒为单位"
    }, 
    "PEXPIREAT": {
        "desc": "设置key的到期UNIX时间戳以毫秒为单位"
    }, 
    "PFADD": {
        "desc": "将指定元素添加到HyperLogLog"
    }, 
    "PFCOUNT": {
        "desc": "Return the approximated cardinality of the set(s) observed by the HyperLogLog at key(s)."
    }, 
    "PFMERGE": {
        "desc": "Merge N different HyperLogLogs into a single one."
    }, 
    "PING": {
        "desc": "Ping 服务器"
    }, 
    "PSETEX": {
        "desc": "Set the value and expiration in milliseconds of a key"
    }, 
    "PSUBSCRIBE": {
        "desc": "Listen for messages published to channels matching the given patterns"
    }, 
    "PTTL": {
        "desc": "获取key的有效毫秒数"
    }, 
    "PUBLISH": {
        "desc": "发布一条消息到频道"
    }, 
    "PUBSUB": {
        "desc": "Inspect the state of the Pub/Sub subsystem"
    }, 
    "PUNSUBSCRIBE": {
        "desc": "停止发布到匹配给定模式的渠道的消息听"
    }, 
    "QUIT": {
        "desc": "关闭连接，退出"
    }, 
    "RANDOMKEY": {
        "desc": "返回一个随机的key"
    }, 
    "READONLY": {
        "desc": "Enables read queries for a connection to a cluster slave node"
    }, 
    "READWRITE": {
        "desc": "Disables read queries for a connection to a cluster slave node"
    }, 
    "RENAME": {
        "desc": "将一个key重命名"
    }, 
    "RENAMENX": {
        "desc": "重命名一个key,新的key必须是不存在的key"
    }, 
    "REPLICAOF": {
        "desc": "Make the server a replica of another instance, or promote it as master."
    }, 
    "RESTORE": {
        "desc": "Create a key using the provided serialized value, previously obtained using DUMP."
    }, 
    "ROLE": {
        "desc": "Return the role of the instance in the context of replication"
    }, 
    "RPOP": {
        "desc": "从队列的右边出队一个元"
    }, 
    "RPOPLPUSH": {
        "desc": "删除列表中的最后一个元素，将其追加到另一个列表"
    }, 
    "RPUSH": {
        "desc": "从队列的右边入队一个元素"
    }, 
    "RPUSHX": {
        "desc": "从队列的右边入队一个元素，仅队列存在时有效"
    }, 
    "SADD": {
        "desc": "添加一个或者多个元素到集合(set)里"
    }, 
    "SAVE": {
        "desc": "同步数据到磁盘上"
    }, 
    "SCAN": {
        "desc": "增量迭代key"
    }, 
    "SCARD": {
        "desc": "获取集合里面的元素数量"
    },
    "SDIFF": {
        "desc": "获得队列不存在的元素"
    }, 
    "SDIFFSTORE": {
        "desc": "获得队列不存在的元素，并存储在一个关键的结果集"
    }, 
    "SELECT": {
        "desc": "选择新数据库"
    }, 
    "SET": {
        "desc": "设置一个key的value值"
    }, 
    "SETBIT": {
        "desc": "Sets or clears the bit at offset in the string value stored at key"
    }, 
    "SETEX": {
        "desc": "设置key-value并设置过期时间（单位：秒）"
    }, 
    "SETNX": {
        "desc": "设置的一个关键的价值，只有当该键不存在"
    }, 
    "SETRANGE": {
        "desc": "Overwrite part of a string at key starting at the specified offset"
    }, 
    "SHUTDOWN": {
        "desc": "关闭服务"
    }, 
    "SINTER": {
        "desc": "获得两个集合的交集"
    }, 
    "SINTERSTORE": {
        "desc": "获得两个集合的交集，并存储在一个关键的结果集"
    }, 
    "SISMEMBER": {
        "desc": "确定一个给定的值是一个集合的成员"
    }, 
    "SLAVEOF": {
        "desc": "指定当前服务器的主服务器"
    }, 
    "SLOWLOG": {
        "desc": "管理再分配的慢查询日志"
    }, 
    "SMEMBERS": {
        "desc": "获取集合里面的所有元素"
    }, 
    "SMOVE": {
        "desc": "移动集合里面的一个元素到另一个集合"
    }, 
    "SORT": {
        "desc": "对队列、集合、有序集合排序"
    }, 
    "SPOP": {
        "desc": "删除并获取一个集合里面的元素"
    }, 
    "SRANDMEMBER": {
        "desc": "从集合里面随机获取一个元素"
    }, 
    "SREM": {
        "desc": "从集合里删除一个或多个元素"
    }, 
    "SSCAN": {
        "desc": "迭代set里面的元素"
    }, 
    "STRLEN": {
        "desc": "获取指定key值的长度"
    }, 
    "SUBSCRIBE": {
        "desc": "监听频道发布的消息"
    }, 
    "SUNION": {
        "desc": "添加多个set元素"
    }, 
    "SUNIONSTORE": {
        "desc": "合并set元素，并将结果存入新的set里面"
    },
    "SYNC": {
        "desc": "用于复制的内部命令"
    }, 
    "TIME": {
        "desc": "返回当前服务器时间"
    }, 
    "TOUCH": {
        "desc": "Alters the last access time of a key(s). Returns the number of existing keys specified."
    }, 
    "TTL": {
        "desc": "获取key的有效时间（单位：秒）"
    }, 
    "TYPE": {
        "desc": "获取key的存储类型"
    }, 
    "UNLINK": {
        "desc": "Delete a key asynchronously in another thread. Otherwise it is just as DEL, but non blocking."
    },
    "ZADD": {
        "desc": "添加到有序set的一个或多个成员，或更新的分数，如果它已经存在"
    }, 
    "ZCARD": {
        "desc": "获取一个排序的集合中的成员数量"
    }, 
    "ZCOUNT": {
        "desc": "返回分数范围内的成员数量"
    }, 
    "ZINCRBY": {
        "desc": "增量的一名成员在排序设置的评分"
    }, 
    "ZINTERSTORE": {
        "desc": "相交多个排序集，导致排序的设置存储在一个新的关键"
    }, 
    "ZLEXCOUNT": {
        "desc": "返回成员之间的成员数量"
    }, 
    "ZPOPMAX": {
        "desc": "Remove and return members with the highest scores in a sorted set"
    }, 
    "ZPOPMIN": {
        "desc": "Remove and return members with the lowest scores in a sorted set"
    }, 
    "ZRANGE": {
        "desc": "根据指定的index返回，返回sorted set的成员列表"
    }, 
    "ZRANGEBYLEX": {
        "desc": "返回指定成员区间内的成员，按字典正序排列, 分数必须相同。"
    }, 
    "ZRANGEBYSCORE": {
        "desc": "返回有序集合中指定分数区间内的成员，分数由低到高排序。"
    }, 
    "ZRANK": {
        "desc": "确定在排序集合成员的索引"
    }, 
    "ZREM": {
        "desc": "从排序的集合中删除一个或多个成员"
    }, 
    "ZREMRANGEBYLEX": {
        "desc": "删除名称按字典由低到高排序成员之间所有成员。"
    }, 
    "ZREMRANGEBYRANK": {
        "desc": "在排序设置的所有成员在给定的索引中删除"
    }, 
    "ZREMRANGEBYSCORE": {
        "desc": "删除一个排序的设置在给定的分数所有成员"
    }, 
    "ZREVRANGE": {
        "desc": "在排序的设置返回的成员范围，通过索引，下令从分数高到低"
    }, 
    "ZREVRANGEBYLEX": {
        "desc": "返回指定成员区间内的成员，按字典倒序排列, 分数必须相同"
    }, 
    "ZREVRANGEBYSCORE": {
        "desc": "返回有序集合中指定分数区间内的成员，分数由高到低排序。"
    }, 
    "ZREVRANK": {
        "desc": "确定指数在排序集的成员，下令从分数高到低"
    }, 
    "ZSCAN": {
        "desc": "迭代sorted sets里面的元素"
    }, 
    "ZSCORE": {
        "desc": "获取成员在排序设置相关的比分"
    }, 
    "ZUNIONSTORE": {
        "desc": "添加多个排序集和导致排序的设置存储在一个新的关键"
    }
}
