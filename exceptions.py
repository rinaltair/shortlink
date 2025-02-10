from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from schemas.response_sch import ErrorResponse


async def http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.detail
        ).dict()
    )


async def value(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            message=str(exc)
        ).dict()
    )


async def lookup(request: Request, exc: LookupError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(
            message=str(exc)
        ).dict()
    )


async def generic(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            message="Internal Server Error"
        ).dict()
    )


async def request(request: Request, exc: RequestValidationError):
    print(exc.errors())
    first_error_msg = exc.errors()[0]["msg"] if exc.errors() else "Validation Error"
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            message=first_error_msg,
        ).dict()
    )
