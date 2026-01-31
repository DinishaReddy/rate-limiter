from fastapi import APIRouter, Header, Request

from app.core.redis_client import get_redis_client
from app.rate_limiter.policies import POLICIES, DEFAULT_POLICY, RateLimitPolicy
from app.rate_limiter.selector import LimiterSelector

router = APIRouter()

redis_client = get_redis_client()
limiter = LimiterSelector(redis_client)


def get_policy_for_path(path: str) -> RateLimitPolicy:
    return POLICIES.get(path, DEFAULT_POLICY)


@router.get("/login")
def login(request: Request,x_user_id: str = Header(default="anonymous")):
    path = request.url.path
    policy = get_policy_for_path(path)
    limiter.check(user=x_user_id, endpoint=path, policy=policy)
    return {"message": "login endpoint allowed ✅"}


@router.get("/data")
def data(request: Request,x_user_id: str = Header(default="anonymous")):
    path = request.url.path
    policy = get_policy_for_path(path)
    limiter.check(user=x_user_id, endpoint=path, policy=policy)
    return {"message": "data endpoint allowed ✅"}


@router.get("/analyze")
def analyze(request: Request,x_user_id: str = Header(default="anonymous")):
    path = request.url.path
    policy = get_policy_for_path(path)
    limiter.check(user=x_user_id, endpoint=path, policy=policy)
    return {"message": "analyze endpoint allowed ✅"}
