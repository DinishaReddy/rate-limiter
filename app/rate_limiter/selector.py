from app.rate_limiter.fixed_window import FixedWindowLimiter
from app.rate_limiter.policies import RateLimitPolicy


class LimiterSelector:
    """
    Chooses the correct limiter based on policy.algorithm
    """

    def __init__(self, redis_client):
        # We create the limiter objects once and reuse them
        self.limiters = {
            "fixed_window": FixedWindowLimiter(redis_client)
        }

    def check(self, user: str, endpoint: str, policy: RateLimitPolicy) -> None:
        algo_name = policy.algorithm

        limiter = self.limiters.get(algo_name)

        if limiter is None:
            # If someone sets algorithm to something we don't support yet
            raise ValueError(f"Unsupported algorithm: {algo_name}")

        limiter.check(user=user, endpoint=endpoint, policy=policy)
