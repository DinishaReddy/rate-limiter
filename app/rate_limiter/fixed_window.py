from fastapi import HTTPException
from redis.exceptions import ConnectionError as RedisConnectionError

from app.rate_limiter.policies import RateLimitPolicy


class FixedWindowLimiter:
    def __init__(self, redis_client):
        # this stores the redis client instance, which is used to interact with Redis
        self.redis = redis_client

    def check(self, user: str, endpoint: str, policy: RateLimitPolicy) -> None:
        """
        Fixed Window rate limiting using Redis.

        Rule example: 5 requests per 60 seconds
        - Redis key holds the current count in the current window
        - Redis key expires after window_seconds (auto reset)
        """

        # 1) Build a unique key per user + endpoint
        key = f"rate_limit:{user}:{endpoint}"

        try:
            # 2) Increase the counter by 1
            current_count = self.redis.incr(key)

            # 3) If this is the first request in the window, set expiration
            if current_count == 1:
                self.redis.expire(key, policy.window_seconds)

        except RedisConnectionError:
            # Redis is down → better to return 503 than crash with 500
            raise HTTPException(
                status_code=503,
                detail="Rate limiter storage (Redis) is unavailable. Try again later."
            )

        # 4) If user exceeded policy → block
        if current_count > policy.max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Too many requests. Limit is {policy.max_requests} per {policy.window_seconds}s."
            )
