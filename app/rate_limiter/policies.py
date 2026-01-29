from dataclasses import dataclass

@dataclass(frozen=True) # freeze to make it immutable
class RateLimitPolicy:
    max_requests: int
    window_seconds: int
    algorithm: str  # e.g., "fixed_window", later "token_bucket"

# Here POLICIES is a variable name
POLICIES: dict[str, RateLimitPolicy] = {
    # strict endpoint (auth/login usually needs stricter limits)
    "/login": RateLimitPolicy(max_requests=5, window_seconds=60, algorithm="fixed_window"),

    # normal API reads
    "/data": RateLimitPolicy(max_requests=60, window_seconds=60, algorithm="fixed_window"),

    # a heavier endpoint (expensive work)
    "/analyze": RateLimitPolicy(max_requests=10, window_seconds=60, algorithm="fixed_window"),
}
# Default policy if no specific endpoint is matched
DEFAULT_POLICY = RateLimitPolicy(max_requests=30, window_seconds=60, algorithm="fixed_window")