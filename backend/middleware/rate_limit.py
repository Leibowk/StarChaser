from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address, default_limits=["50/minute"])

def register_rate_limiter(app: FastAPI):
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request, exc):
        return JSONResponse(
            status_code=429,
            content={"message": "Too many requests, slow down!"}
        )
