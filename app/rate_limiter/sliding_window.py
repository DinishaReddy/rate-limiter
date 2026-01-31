# app/rate_limiter/sliding_window.py

import time
from fastapi import HTTPException
from redis.exceptions import ConnectionError as RedisConnectionError
from app.rate_limiter.policies import RateLimitPolicy
from app.rate_limiter.scripts import SLIDING_WINDOW_LUA

class SlidingWindowLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.script = self.redis.register_script(SLIDING_WINDOW_LUA)

    def check(self, user: str, endpoint: str, policy: RateLimitPolicy) -> None:
        key = f"rl:sw:{user}:{endpoint}"
        now_ms = int(time.time() * 1000)
        window_ms = policy.window_seconds * 1000

        # Member id must be unique; using now_ms + a tiny random-ish suffix
        member_id = f"{now_ms}-{user}"

        try:
            allowed, count = self.script(
                keys=[key],
                args=[now_ms, window_ms, policy.max_requests, member_id]
            )
        except RedisConnectionError:
            raise HTTPException(status_code=503, detail="Redis unavailable")

        if int(allowed) != 1:
            raise HTTPException(
                status_code=429,
                detail=f"Too many requests (sliding window). Limit {policy.max_requests}/{policy.window_seconds}s."
            )
