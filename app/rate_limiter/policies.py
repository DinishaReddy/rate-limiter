from dataclasses import dataclass

@dataclass(frozen=True) # freeze to make it immutable
class RateLimitPolicy:
    max_requests: int
    window_seconds: int
    algorithm: str  # e.g., "fixed_window", later "token_bucket"

# Here POLICIES is a variable name
POLICIES = {
    "/login":   RateLimitPolicy(max_requests=5,  window_seconds=60, algorithm="sliding_window"),
    "/data":    RateLimitPolicy(max_requests=60, window_seconds=60, algorithm="token_bucket"),
    "/analyze": RateLimitPolicy(max_requests=10, window_seconds=60, algorithm="leaky_bucket"),
}
DEFAULT_POLICY = RateLimitPolicy(max_requests=30, window_seconds=60, algorithm="fixed_window")
