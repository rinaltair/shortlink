from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from sqlalchemy import Text

from .base_model import Base


class UrlBase(SQLModel): # Base Model is only for user submitted data
    title: Optional[str] = Field(default=None, nullable=True)
    original_url: str = Field(index=True, sa_type=Text, max_length=1048)
    short_code: str = Field(index=True, unique=True)
    clicks : int = Field(default=0)


class UrlFull(UrlBase, Base): # The rest of the model
    is_active: bool = Field(default=True)
    pass


class Url(UrlFull, table=True):
    pass
