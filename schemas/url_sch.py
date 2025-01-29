from datetime import datetime  # Import datetime from the datetime module
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field, computed_field, model_validator

from configs.settings import settings
from utils import Shortlink

class UrlCreate(BaseModel):
    # What user can create
    title: Optional[str] = Field(None, max_length=100)
    original_url: HttpUrl
    shortlink: Optional[str] = Field(None, min_length=4, max_length=100, pattern="^[a-zA-Z0-9]*$")

    @model_validator(mode='after')
    def validate_shortlink(cls, values):
        shortlink = values.shortlink
        if shortlink is not None:  # Only validate if provided
            if len(shortlink) < 4: raise ValueError("Shortcode must be at least 4 characters")
            if not Shortlink.validate(shortlink): raise ValueError("Only letters, numbers, underscores and hyphens allowed")
        else: shortlink = None
        return values 


class UrlUpdate(BaseModel):
    # What user can update
    title: Optional[str] = Field(None, max_length=100)
    original_url: HttpUrl
    shortlink: Optional[str]
    is_active: Optional[bool] = None


class UrlResponse(BaseModel):
    # For API Response
    id: str
    title: str
    original_url: str
    shortlink: str
    clicks: int = 0
    is_active: bool
    created_at: str
    updated_at: str

    @computed_field
    def short_url(self) -> str:  # For Generating the full short url, i just need to  save the code
        return f"{settings.URL_BASE}{self.shortlink}"
