from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[object]
    message: Optional[str]

class ErrorResponse(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: str = ""