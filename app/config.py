from pydantic_settings import BaseSettings
import os
from pathlib import Path


class Settings(BaseSettings):
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Authentication
    USERNAME: str
    PASSWORD: str

    # Application settings
    APP_NAME: str

    # Path settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STATIC_DIR: Path = Path(__file__).resolve().parent / "static"
    TEMPLATES_DIR: Path = Path(__file__).resolve().parent / "templates"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Load settings from .env file
settings = Settings()
