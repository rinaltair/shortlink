from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from sqlalchemy import Text

from .model import Base


class UrlBase(SQLModel):
    title: Optional[str] = Field(default=None, nullable=True)
    original_url: str = Field(index=True, sa_type=Text, max_length=1048)
    shortened_url: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)

    # visits: Optional["VisitModel"] = Relationship(back_populates="url")


class UrlFull(UrlBase, Base):
    pass


class Url(UrlFull, table=True):
    pass
