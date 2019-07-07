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
    key_prefix_reading_key = redisKey.CACHE_ARTICLE_READING_KEY

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
    def get_reading(cls, article_id: id):
        key = cls.key_prefix_reading(article_id)
        number = cls.db.get(key)
        return (number, 0)[number is None]

    @classmethod
    def reading(cls, article_id: id, count: int):
        key = cls.key_prefix_reading(article_id)
        try:
            return cls.db.incr(key)
        except ValueError:
            return cls.db.set(key, count)

    @classmethod
    def get_reading_key(cls, article_id: id, user_id: id, reading_ip: str):
        key = cls.key_prefix_reading_key(article_id, user_id, reading_ip)
        value = cls.db.get(key)
        return (value, 0)[value is None]

    @classmethod
    def set_reading_key(cls, article_id: id, user_id: id, reading_ip: str):
        key = cls.key_prefix_reading_key(article_id, user_id, reading_ip)
        cls.db.set(key, 1, cls.key_prefix_reading_key.ex)
