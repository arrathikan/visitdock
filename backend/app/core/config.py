"""Application configuration settings using Pydantic Settings."""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory for backend (where .env may optionally reside)
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """VisitDock backend application settings.

    Environment variables take precedence over values loaded from backend/.env.
    """

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: Literal["development", "test", "production"] = "development"
    DATABASE_URL: str = (
        "postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock"
    )
    CLINIC_TIMEZONE: str = "UTC"
    CORS_ORIGINS: str = "http://localhost:3000"


settings = Settings()
