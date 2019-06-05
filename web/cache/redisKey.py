class RedisKey:
    """RedisKey类对象"""

    def __init__(self, prefix, ex=None):
        self.prefix = prefix
        self.ex = ex

    def __call__(self, *args, **kwargs):
        return self.prefix % args


# 定义业务缓存Key
CACHE_USER_INFO = RedisKey(prefix='user:%d', ex=20 * 60)
CACHE_ARTICLE = RedisKey(prefix='article:%d', ex=20 * 60)
CACHE_ARTICLES = RedisKey(prefix='articles:%s', ex=24 * 60 * 60)
