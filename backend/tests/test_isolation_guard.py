"""Regression tests for test database isolation safeguards."""

from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from app.appointments.models import Appointment, AppointmentStatus, AppointmentType
from tests.conftest import validate_test_database_target


@pytest.mark.parametrize("invalid_env", ["development", "production", "staging", ""])
def test_validate_target_rejects_non_test_env(invalid_env: str) -> None:
    """Verify that APP_ENV != 'test' raises a UsageError with actionable guidance."""
    with pytest.raises(pytest.UsageError, match="Unsafe test environment"):
        validate_test_database_target(
            invalid_env,
            "postgresql+psycopg://visitdock:secret@localhost:5433/visitdock_test",
        )


@pytest.mark.parametrize(
    "unsafe_url",
    [
        "postgresql+psycopg://visitdock:secret@localhost:5433/visitdock",
        "postgresql+psycopg://visitdock:secret@localhost:5433/postgres",
        "postgresql+psycopg://visitdock:secret@localhost:5433/production",
        "postgresql+psycopg://visitdock:secret@localhost:5433/visitdock_dev",
        "postgresql+psycopg://visitdock:secret@localhost:5433/myapp",
    ],
)
def test_validate_target_rejects_unsafe_database_names(unsafe_url: str) -> None:
    """Verify that targeting non-test databases raises a UsageError."""
    with pytest.raises(pytest.UsageError, match="Unsafe target database"):
        validate_test_database_target("test", unsafe_url)


def test_validate_target_rejects_missing_database_name() -> None:
    """Verify that an empty or missing database name raises a UsageError."""
    with pytest.raises(pytest.UsageError, match="does not specify a target database"):
        validate_test_database_target(
            "test",
            "postgresql+psycopg://visitdock:secret@localhost:5433/",
        )


@pytest.mark.parametrize(
    "valid_url",
    [
        "postgresql+psycopg://visitdock:secret@localhost:5433/visitdock_test",
        "postgresql+psycopg://visitdock:secret@localhost:5433/myapp_test",
        "postgresql+psycopg://visitdock:secret@localhost:5433/ci-test",
    ],
)
def test_validate_target_accepts_valid_test_databases(valid_url: str) -> None:
    """Verify that valid test configurations pass validation cleanly."""
    validate_test_database_target("test", valid_url)


def test_session_isolation_rolls_back_created_records(db_session: Session) -> None:
    """Verify records created during a test exist inside the test session."""
    appt = Appointment(
        patient_name="Isolation Check Patient",
        appointment_at=datetime.now(UTC),
        doctor="Dr. Isolation Check",
        appointment_type=AppointmentType.CHECK_UP,
        status=AppointmentStatus.SCHEDULED,
    )
    db_session.add(appt)
    db_session.commit()

    assert appt.id is not None
    loaded = db_session.get(Appointment, appt.id)
    assert loaded is not None


def test_session_isolation_verified_no_residual_data(db_session: Session) -> None:
    """Verify that previous test's committed records were rolled back and do not exist."""
    count = (
        db_session.query(Appointment)
        .filter(Appointment.patient_name == "Isolation Check Patient")
        .count()
    )
    assert count == 0
