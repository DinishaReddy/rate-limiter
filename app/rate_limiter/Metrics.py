class Metrics:
    def __init__(self, redis_client):
        self.redis = redis_client

    def record_allowed(self, endpoint: str):
        self.redis.incr("metrics:allowed")
        self.redis.incr(f"metrics:endpoint:{endpoint}")

    def record_blocked(self, endpoint: str):
        self.redis.incr("metrics:blocked")
        self.redis.incr(f"metrics:endpoint:{endpoint}")
