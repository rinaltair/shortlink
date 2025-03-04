from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from models.user_model import UserRole

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=4, max_length=100)
    password: str = Field(..., min_length=8)
