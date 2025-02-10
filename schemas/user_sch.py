from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    # What user can create
    username: str = Field(None, min_length=4, max_length=100)
    email: EmailStr = Field(None, max_length=254)
    password: str = Field(None, min_length=8)


class UserUpdate(BaseModel):
    # What user can update
    username: Optional[str] = Field(None, min_length=4, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=254)
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)


class UserResponse(BaseModel):
    # For API Response
    id: str
    username: str
    email: str
    # password: str
    role: str
    is_active: bool
    created_at: str
    updated_at: str
