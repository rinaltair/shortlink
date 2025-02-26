from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware

class AsyncCleanupMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        await request.state.db.aclose()  # If using request-scoped db
        return response