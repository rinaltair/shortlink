from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from models.user_model import UserRole

class UserCreate(BaseModel):
    # What user can create
    username: str = Field(..., min_length=4, max_length=100)
    email: EmailStr = Field(..., max_length=254)
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    # What user can update
    username: Optional[str] = Field(None, min_length=4, max_length=100)
    email: Optional[str] = Field(None, max_length=254)
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)


class UserResponse(BaseModel):
    # For API Response
    id: str
    username: str
    email: str
    # password: str
    role: UserRole
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        user_enum_values = True
