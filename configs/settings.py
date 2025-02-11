from typing import List

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

load_dotenv()  # Load environment variables from .env file


class BaseConfig:
    """ .env file configuration class."""
    env_file = ".env"
    env_file_encoding = "utf-8"


class Settings(BaseSettings):
    """Application settings class."""
    DB_CONFIG: str
    shortlink_length: int = 6
    URL_BASE: str
    RESTRICTED_SHORTLINK: List[str] = ['api', 'auth']

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @field_validator("URL_BASE")
    # Ensuring the url base always ends with "/"
    def validate_url_base(cls, value):
        if not value.endswith("/"):
            value += "/"
        return value

    class Config(BaseConfig): pass


settings = Settings()  # Load values from .env file
