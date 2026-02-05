from fastapi import APIRouter
from app.core.redis_client import get_redis_client

router = APIRouter()

redis = get_redis_client()

@router.get("/metrics")
def metrics():
    allowed = redis.get("metrics:allowed") or 0
    blocked = redis.get("metrics:blocked") or 0

    return {
        "allowed_requests": int(allowed),
        "blocked_requests": int(blocked),
    }
