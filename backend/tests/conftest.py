"""Pytest fixtures for VisitDock test suite."""

from collections.abc import Generator
from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import delete
from sqlalchemy.orm import Session

from alembic import command
from app.appointments.models import Appointment
from app.core.config import settings
from app.db.session import SessionLocal, engine

BACKEND_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session", autouse=True)
def setup_test_database() -> Generator[None, None, None]:
    """Ensure Alembic migrations are applied up to head for the active test database."""
    alembic_ini_path = BACKEND_DIR / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    # Run migrations up to head
    command.upgrade(alembic_cfg, "head")

    yield

    # Engine cleanup at end of test session
    engine.dispose()


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Provide an isolated database session with automatic teardown cleanup."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        # Clean up any records inserted during testing to maintain test isolation
        with SessionLocal() as cleanup_session:
            cleanup_session.execute(delete(Appointment))
            cleanup_session.commit()
