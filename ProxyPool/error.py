class RedisClientPOPError(Exception):
    def __str__(self):
        return repr('代理资源已耗尽')