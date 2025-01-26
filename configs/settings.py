from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()  # Load environment variables from .env file


class Settings(BaseSettings):
    DB_CONFIG: str
    shortcode_length: int = 6
    URL_BASE: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # Load values from .env file
