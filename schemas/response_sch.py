from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[object]
    message: Optional[str]

class ErrorResponse(BaseModel):
    success: bool = False
    message: str