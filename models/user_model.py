from sqlmodel import SQLModel, Field, Relationship
from sqlmodel import Field
from typing import Optional

from .base_model import Base


class UserBase(SQLModel):
    # Base Model is where user can tinkered with
    username: Optional[str] = Field(default=None, unique=True, nullable=False)
    email: Optional[str] = Field(default=None, unique=True, nullable=False)
    # password: Optional[str] = Field(default=None, min_length=8)           # Not needed for now


class UserFull(UserBase, Base):
    # Manage by the systems, like relationship
    role: Optional[str] = Field(default=None)
    password_hash: Optional[str] = Field(default=None, nullable=False)


class User(UserFull, table=True):
    pass
