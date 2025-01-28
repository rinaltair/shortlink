from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import field_validator

load_dotenv()  # Load environment variables from .env file


class Settings(BaseSettings):
    DB_CONFIG: str
    shortlink_length: int = 6
    URL_BASE: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("URL_BASE")
    # Ensuring the url base always ends with "/"
    def validate_url_base(cls, value):
        if not value.endswith("/"):
            value += "/"
        return value



settings = Settings()  # Load values from .env file
