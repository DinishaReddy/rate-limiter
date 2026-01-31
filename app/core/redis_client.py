import redis
from app.core.config import REDIS_HOST, REDIS_PORT

# this function initializes and returns a Redis client instance, configured to connect to the Redis server, it returns an object that can be used to interact with Redis
def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True # whenever the redis return bytes, it will decode to strings
    )
