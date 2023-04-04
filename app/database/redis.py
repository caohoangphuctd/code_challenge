import redis.asyncio as redis

from app.config import config


redis_setting = config.redis_config

pool = redis.ConnectionPool(
    host=redis_setting.redis_host,
    port=redis_setting.redis_port
)

RedisSession = redis.Redis(
    connection_pool=pool
)
