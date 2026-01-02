from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        key = request.headers.get("x-api-key") or request.query_params.get("api_key")
        if key != self.api_key:
            raise HTTPException(status_code=401, detail="Unauthorized")
        response = await call_next(request)
        return response
