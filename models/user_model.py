from sqlmodel import SQLModel, Field, Relationship
from sqlmodel import Field
from typing import Optional, TYPE_CHECKING

from .base_model import Base


if TYPE_CHECKING:
    from .url_model import Url

# class UserRole(str, Enum):
#     user = "user"
#     admin = "admin"
#     moderator = "moderator"

class UserBase(SQLModel):
    # Base Model is where user can tinkered with
    username: Optional[str] = Field(default=None, unique=True, nullable=False)
    email: Optional[str] = Field(default=None, unique=True, nullable=False)
    # password: Optional[str] = Field(default=None, min_length=8)           # Not needed for now


class UserFull(UserBase, Base):
    # Manage by the systems, like relationship
    role: Optional[str] = Field(default=None, nullable=True)
    password_hash: Optional[str] = Field(default=None, nullable=False)
    is_active: Optional[bool] = Field(default=True, nullable=False)


class User(UserFull, table=True):
    urls: list['Url'] = Relationship(back_populates="user")