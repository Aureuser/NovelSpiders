import redis
from ProxyPool.setting import HOST,PORT,PASSWORD,TABLE_NAME
from ProxyPool.error import RedisClientPOPError

class RedisClient():
    '''
    该类用于连接redis数据库
    并提供数据库的操作接口
    '''

    def __init__(self):
        if PASSWORD:
            self.conn = redis.Redis(host=HOST,port=PORT,password=PASSWORD)
        else:
            self.conn = redis.Redis(host=HOST,port=PORT)

    def pop(self):
        try:
            return self.conn.rpop(TABLE_NAME).decode('utf-8')
        except RedisClientPOPError as e:
            # 返回代理资源耗尽异常
            return None

    def count(self):
        # 返回代理资源数
        return int(self.conn.llen(TABLE_NAME))

    def flush(self):
        # 清空代理资源
        self.conn.flushall()

    def get(self, count=1):
        """
        get proxies from redis
        """
        proxies = self.conn.lrange(TABLE_NAME, 0, count - 1)
        self.conn.ltrim(TABLE_NAME, count, -1)
        return proxies

    def put(self, proxy):
        """
        add proxy to right top
        """
        self.conn.rpush(TABLE_NAME, proxy)