# This module sets up rate limiting for the API using the slowapi library. It defines a limiter with a default limit of 100 requests per minute and a custom handler for when the rate limit is exceeded, returning a 429 status code with a JSON response.

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def _rate_limit_exceeded_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )