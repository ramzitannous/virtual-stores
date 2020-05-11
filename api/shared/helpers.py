from settings.base import get_env
from redis import Redis

redis = Redis(host=get_env("REDIS_HOST"), port=get_env("REDIS_PORT"))


def put_value(key, val, timeout=None):
    redis.set(key, val, timeout)


def get_value(key, default_val=None):
    if bool(redis.exists(key)):
        return redis.get(key)
    else:
        return default_val


def remove_value(key):
    redis.delete(key)
