from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class AsyncCleanupMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if hasattr(request.state, 'db'):
            await request.state.db.close()  # Close the database connection
        return response