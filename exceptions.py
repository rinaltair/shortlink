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
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorResponse(message=exc.detail).dict()
            )
        except ValueError as exc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ErrorResponse(message=str(exc)).dict()
            )
        except LookupError as exc:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResponse(message=str(exc)).dict()
            )
        except RequestValidationError as exc:
            first_error_msg = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ErrorResponse(message=first_error_msg).dict()
            )
        except PermissionError as exc:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=ErrorResponse(message=str(exc)).dict()
            )
        except AuthenticationError as exc:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=ErrorResponse(message="Authentication failed").dict()
            )
        except Exception as exc:
            logger.error(f"An unexpected error occurred: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ErrorResponse(message="Internal Server Error").dict()
            )
