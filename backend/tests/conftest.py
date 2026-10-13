"""Pytest fixtures and configuration for VisitDock test suite."""

from collections.abc import Generator
from pathlib import Path

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from alembic import command
from app.core.config import settings
from app.db.session import engine, get_db
from app.main import app

BACKEND_DIR = Path(__file__).resolve().parent.parent


def validate_test_database_target(app_env: str, database_url: str) -> None:
    """Validate that the test execution environment and database target are strictly isolated.

    Prevents tests from accidentally running against development or production databases,
    which could cause data loss or schema contamination.

    Raises:
        pytest.UsageError: If APP_ENV is not 'test' or database name is unsafe.
    """
    if app_env != "test":
        raise pytest.UsageError(
            f"Unsafe test environment: APP_ENV is set to '{app_env}'. "
            "Automated tests must only run with APP_ENV=test to prevent data loss."
        )

    try:
        url = make_url(database_url)
    except Exception as exc:
        raise pytest.UsageError(f"Invalid DATABASE_URL configuration: {exc}") from exc

    db_name = url.database
    if not db_name:
        raise pytest.UsageError("DATABASE_URL does not specify a target database name.")

    # Strictly reject known development, system, or production database names
    forbidden_databases = {"visitdock", "postgres", "template0", "template1", "production"}
    is_recognized_test_db = db_name.endswith("_test") or db_name.endswith("-test")

    if db_name in forbidden_databases or not is_recognized_test_db:
        raise pytest.UsageError(
            f"Unsafe target database '{db_name}'. "
            "Tests must be executed against a dedicated test database "
            "(e.g., 'visitdock_test' or ending in '_test'). Refusing to proceed."
        )


@pytest.fixture(scope="session", autouse=True)
def setup_test_database() -> Generator[None, None, None]:
    """Ensure test database target is safe and Alembic migrations are applied up to head."""
    validate_test_database_target(settings.APP_ENV, settings.DATABASE_URL)

    alembic_ini_path = BACKEND_DIR / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as exc:
        url = make_url(settings.DATABASE_URL)
        raise RuntimeError(
            f"Failed to apply migrations to test database '{url.database}'. "
            "Ensure the test database exists and is reachable.\n"
            "For local Docker PostgreSQL, create it with:\n"
            f"  docker exec -i visitdock-db-1 psql -U visitdock -d postgres "
            f"-c 'CREATE DATABASE {url.database};'\n"
            f"Original error: {exc}"
        ) from exc

    yield

    # Engine cleanup at end of test session
    engine.dispose()


@pytest.fixture
def db_session(monkeypatch: pytest.MonkeyPatch) -> Generator[Session, None, None]:
    """Provide a transaction-isolated database session with automatic rollback.

    Each test executes within an outer transaction with savepoints.
    When the test completes (success or failure), the entire outer transaction
    is rolled back, ensuring zero residual test data and eliminating destructive
    table-wide cleanup.
    """
    connection = engine.connect()
    transaction = connection.begin()

    test_sessionmaker = sessionmaker(
        bind=connection,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False,
    )

    # Monkeypatch SessionLocal so any auxiliary session created in test code shares this connection
    monkeypatch.setattr("app.db.session.SessionLocal", test_sessionmaker)
    monkeypatch.setattr("tests.test_database.SessionLocal", test_sessionmaker, raising=False)

    session = test_sessionmaker()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Provide a FastAPI TestClient bound to the transaction-isolated database session."""

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
