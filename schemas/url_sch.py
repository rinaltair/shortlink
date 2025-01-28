import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field, computed_field, field_validator

from configs.settings import settings


class UrlCreate(BaseModel):
    # What user can create
    title: Optional[str] = Field(None, max_length=100)
    original_url: HttpUrl
    shortlink: Optional[str] = Field(None, min_length=8, max_length=100, pattern="^[a-zA-Z0-9]*$")

    @field_validator("shortlink")
    def validate_shortlink(cls, value):
        if value:  # Only validate if provided
            if len(value) < 4: raise ValueError("Shortcode must be at least 4 characters")
            if not value.isalnum() and '_' not in value and '-' not in value:
                raise ValueError("Only letters, numbers, underscores and hyphens allowed")
        return value


class UrlUpdate(BaseModel):
    # What user can update
    title: Optional[str] = Field(None, max_length=100)
    original_url: HttpUrl
    shortlink: Optional[str]
    is_active: Optional[bool] = None


class UrlResponse(BaseModel):
    # For API Response
    id: UUID
    title: str
    original_url: str
    shortlink: str
    clicks: int = 0
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @computed_field
    def short_url(self) -> str:  # For Generating the full short url, i just need to  save the code
        return f"{settings.URL_BASE}/{self.shortlink}"
