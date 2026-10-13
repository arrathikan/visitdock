"""Application configuration settings using Pydantic Settings."""

from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import field_validator
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

    @field_validator("CLINIC_TIMEZONE")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError("CLINIC_TIMEZONE must be an IANA timezone") from None
        return value


settings = Settings()
