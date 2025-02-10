from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, Column
from sqlmodel import SQLModel as _SQLModel
from stringcase import snakecase

from utils.datetime import DateTime  # Ensure this import is correct

class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)

class Base(SQLModel):
    class Config:
        arbitrary_types_allowed = True
        # table = False  # Critical for inheritance

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False,)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False, sa_column_kwargs={"onupdate": datetime.utcnow})