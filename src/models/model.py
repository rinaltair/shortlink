from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field
from sqlmodel import SQLModel as _SQLModel
from stringcase import snakecase

from utils.datetime import Datetime


class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)


class Base(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime | None = Field(default_factory=datetime.now, sa_column=Column(Datetime, nullable=False))
    updated_at: datetime | None = Field(default=None,
                                        sa_column=Column(Datetime, nullable=False, onupdate=datetime.utcnow))
