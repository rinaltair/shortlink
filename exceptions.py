# exceptions.py
import logging
from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.authentication import AuthenticationError
from starlette.middleware.base import BaseHTTPMiddleware

from schemas.response_sch import ErrorResponse

logger = logging.getLogger(__name__)

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            content = ErrorResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                title="Internal Server Error",
                detail=str(exc),
                instance=request.url.path
            )
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(f"Error: {content.detail}")

        
            if isinstance(exc, HTTPException):
                content.type = "/errors/http"
                content.title = "HTTP Error"
                content.status = exc.status_code
                content.detail = exc.detail
                status_code = exc.status_code

            elif isinstance(exc, ValueError):
                content.type = "/errors/value"
                content.title = "Validation Error"
                content.status = status.HTTP_400_BAD_REQUEST
                content.detail = exc.errors()
                status_code = status.HTTP_400_BAD_REQUEST

            elif isinstance(exc, LookupError):
                content.type = "/errors/notFound"
                content.title = "Validation Error"
                content.status = status.HTTP_404_NOT_FOUND
                content.detail = exc.errors()
                status_code = status.HTTP_404_NOT_FOUND

            elif isinstance(exc, RequestValidationError):
                content.type = "/errors/validation"
                content.title = "Validation Error"
                content.status = status.HTTP_422_UNPROCESSABLE_ENTITY
                content.detail = exc.errors()
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            
            elif isinstance(exc, PermissionError):
                content.type = "/errors/forbidden"
                content.title = "Forbidden"
                content.status = status.HTTP_403_FORBIDDEN
                content.detail = "Forbidden"
                status_code = status.HTTP_403_FORBIDDEN

            elif isinstance(exc, AuthenticationError):
                content.type = "/errors/authentication"
                content.title = "Authentication Error"
                content.status = status.HTTP_401_UNAUTHORIZED
                content.detail = "Authentication failed"
                status_code = status.HTTP_401_UNAUTHORIZED
            # Add other exception types as needed

            cors_headers = {
                "Access-Control-Allow-Origin": request.headers.get("origin", ""),
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            }

            return JSONResponse(
                status_code=status_code,
                content=content.dict(),
                headers={
                    **cors_headers,
                    "Content-Type": "application/problem+json"
                }
            )