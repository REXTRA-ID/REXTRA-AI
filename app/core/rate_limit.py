import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# Get Redis URL from environment, fallback to localhost for local dev
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
# Use database 3 for rate limiting to avoid conflicts
rate_limit_redis_url = REDIS_URL.replace("/0", "/3") if "/0" in REDIS_URL else f"{REDIS_URL}/3"

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
    storage_uri=rate_limit_redis_url
)

def rate_limit_exceeded_handler(request, exc):
    return {
        "error": "rate_limit_exceeded",
        "message": "Too many requests. Please try again later."
    }