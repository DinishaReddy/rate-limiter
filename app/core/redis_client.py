import os
import redis

def get_redis_client() -> redis.Redis:
    """
    Local: uses REDIS_HOST + REDIS_PORT (defaults to localhost:6379)
    Render: uses REDIS_URL (provided by Render Redis service)
    """
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        return redis.Redis.from_url(redis_url, decode_responses=True)

    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    return redis.Redis(host=host, port=port, decode_responses=True)
