from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

def safe_get_remote_address(request):
    return (request.client.host if request.client else "test") or "test"

limiter = Limiter(key_func=safe_get_remote_address)

def _rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )
