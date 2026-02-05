from fastapi import HTTPException

from app.rate_limiter.fixed_window import FixedWindowLimiter
from app.rate_limiter.sliding_window import SlidingWindowLimiter
from app.rate_limiter.token_bucket import TokenBucketLimiter
from app.rate_limiter.leaky_bucket import LeakyBucketLimiter
from app.rate_limiter.policies import RateLimitPolicy
from app.rate_limiter.Metrics import Metrics


class LimiterSelector:
    def __init__(self, redis_client):
        self.limiters = {
            "fixed_window": FixedWindowLimiter(redis_client),
            "sliding_window": SlidingWindowLimiter(redis_client),
            "token_bucket": TokenBucketLimiter(redis_client),
            "leaky_bucket": LeakyBucketLimiter(redis_client),
        }
        self.metrics = Metrics(redis_client)

    def check(self, user: str, endpoint: str, policy: RateLimitPolicy) -> None:
        limiter = self.limiters.get(policy.algorithm)
        if limiter is None:
            raise ValueError(f"Unsupported algorithm: {policy.algorithm}")

        try:
            limiter.check(user=user, endpoint=endpoint, policy=policy)
            # ✅ request allowed
            self.metrics.record_allowed(endpoint)
        except HTTPException:
            # ✅ request blocked (429 or 503)
            self.metrics.record_blocked(endpoint)
            raise
