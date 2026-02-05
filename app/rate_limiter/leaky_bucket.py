# app/rate_limiter/leaky_bucket.py

import time
from fastapi import HTTPException
from redis.exceptions import ConnectionError as RedisConnectionError
from app.rate_limiter.policies import RateLimitPolicy
from app.rate_limiter.scripts import LEAKY_BUCKET_LUA

class LeakyBucketLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.script = self.redis.register_script(LEAKY_BUCKET_LUA)

    def check(self, user: str, endpoint: str, policy: RateLimitPolicy) -> None:
        key = f"rl:lb:{user}:{endpoint}"
        now_ms = int(time.time() * 1000)

        capacity = policy.max_requests
        window_ms = policy.window_seconds * 1000
        leak_rate_per_ms = capacity / window_ms

        try:
            allowed, water_level = self.script(
                keys=[key],
                args=[now_ms, capacity, leak_rate_per_ms]
            )
        except RedisConnectionError:
            raise HTTPException(status_code=503, detail="Redis unavailable")

        if int(allowed) != 1:
            raise HTTPException(
                status_code=429,
                detail=f"Too many requests (leaky bucket)."
            )
