from django.core.cache import cache
from . import redisKey


class CacheArticles:
    """
    原始数据类型 dict
    存储数据类型 bytes
    数据说明 将dict数据序列化成二进制数据，存入redis中
    """

    db = cache
    key_prefix = redisKey.CACHE_ARTICLE
    key_prefix_reading = redisKey.CACHE_ARTICLE_READING

    @classmethod
    def get(cls, article_id: id):
        key = cls.key_prefix(article_id)
        article_dict = cls.db.get(key)
        return article_dict

    @classmethod
    def set(cls, article_id: id, article_dict: dict):
        key = cls.key_prefix(article_id)
        cls.db.set(key, article_dict, cls.key_prefix.ex)

    @classmethod
    def delete(cls, article_id: id):
        key = cls.key_prefix(article_id)
        return cls.db.delete(key) == 1

    @classmethod
    def reading(cls, article_id: id):
        key = cls.key_prefix_reading(article_id)
        return cls.db.incr(key)