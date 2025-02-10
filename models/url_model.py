from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from sqlalchemy import Text

from .base_model import Base

class UrlBase(SQLModel):
    # Base Model is where user can tinkered with
    title: Optional[str] = Field(default=None, nullable=True)
    original_url: str = Field(index=True, sa_type=Text, max_length=1048)
    shortlink: str = Field(index=True, unique=True)
    clicks: int = Field(default=0)

class UrlFull(UrlBase, Base):
    # Manage by the systems, like relationship
    is_active: bool = Field(default=True)

class Url(UrlFull, table=True):
    pass