import os 
import redis


class RedisClient:
    _intance = None

    def __new__(cls, *args, **kwargs):
        if not cls._intance:
            cls._intance = super(RedisClient, cls).__new__(cls, *args, **kwargs)
            cls._intance._redis_client = cls._intance._connect_to_redis 
        return cls._intance
    
    @staticmethod
    def _load_config():
        return {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', 6379)),
            'decode_responses': True
        }
    
    @classmethod
    def _connect_to_redis(cls):
        config = cls._load_config()
        redis_client = redis.StrictRedis(**config)
        return redis_client
    

    @classmethod
    def get(cls):
        return cls._redis_client