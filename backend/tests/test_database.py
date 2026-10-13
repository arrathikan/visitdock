"""PostgreSQL integration tests for VisitDock persistence and Appointment model."""

import uuid
from datetime import UTC, datetime, timedelta, timezone, tzinfo

import pytest
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.appointments.models import Appointment, AppointmentStatus, AppointmentType
from app.db.session import SessionLocal, get_db


def test_database_connection_established(db_session: Session) -> None:
    """Verify that a basic connection and query succeed."""
    result = db_session.execute(sa.text("SELECT 1")).scalar()
    assert result == 1


def test_appointments_table_schema_exists(db_session: Session) -> None:
    """Verify that the Alembic migration created the appointments table with expected columns."""
    inspector = sa.inspect(db_session.bind)
    tables = inspector.get_table_names()
    assert "appointments" in tables

    columns = {col["name"]: col for col in inspector.get_columns("appointments")}
    expected_columns = {
        "id",
        "patient_name",
        "appointment_at",
        "doctor",
        "appointment_type",
        "status",
        "created_at",
        "updated_at",
    }
    assert expected_columns.issubset(columns.keys())


def test_appointment_insert_and_query_in_new_session(db_session: Session) -> None:
    """Verify that an appointment can be inserted and queried in a separate session."""
    appt_time = datetime(2026, 10, 20, 9, 30, tzinfo=UTC)
    appt = Appointment(
        patient_name="Emma Wilson",
        appointment_at=appt_time,
        doctor="Dr. Maya Carter",
        appointment_type=AppointmentType.CONSULTATION,
        status=AppointmentStatus.SCHEDULED,
    )
    db_session.add(appt)
    db_session.commit()
    appt_id = appt.id

    assert isinstance(appt_id, uuid.UUID)

    # Query in a brand-new session
    with SessionLocal() as new_session:
        fetched = new_session.get(Appointment, appt_id)
        assert fetched is not None
        assert fetched.id == appt_id
        assert fetched.patient_name == "Emma Wilson"
        assert fetched.doctor == "Dr. Maya Carter"
        assert fetched.appointment_type == "consultation"
        assert fetched.status == "scheduled"
        assert fetched.created_at is not None
        assert fetched.updated_at is not None
        assert fetched.appointment_at == appt_time


def test_all_allowed_appointment_types_and_statuses_persist(db_session: Session) -> None:
    """Verify all valid appointment types and statuses can be stored successfully."""
    valid_pairs = [
        (AppointmentType.CONSULTATION, AppointmentStatus.SCHEDULED),
        (AppointmentType.FOLLOW_UP, AppointmentStatus.COMPLETED),
        (AppointmentType.CHECK_UP, AppointmentStatus.CANCELLED),
    ]

    for appt_type, status in valid_pairs:
        appt = Appointment(
            patient_name="Test Patient",
            appointment_at=datetime.now(UTC),
            doctor="Dr. Maya Carter",
            appointment_type=appt_type,
            status=status,
        )
        db_session.add(appt)
        db_session.commit()

        assert appt.id is not None
        assert appt.appointment_type == appt_type.value
        assert appt.status == status.value


def test_invalid_appointment_type_violates_check_constraint(db_session: Session) -> None:
    """Verify that inserting an invalid appointment_type triggers a database check constraint."""
    invalid_appt = Appointment(
        patient_name="Emma Wilson",
        appointment_at=datetime.now(UTC),
        doctor="Dr. Maya Carter",
        appointment_type="invalid_type",
        status=AppointmentStatus.SCHEDULED,
    )
    db_session.add(invalid_appt)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_invalid_status_violates_check_constraint(db_session: Session) -> None:
    """Verify that inserting an invalid status triggers a database check constraint."""
    invalid_appt = Appointment(
        patient_name="Emma Wilson",
        appointment_at=datetime.now(UTC),
        doctor="Dr. Maya Carter",
        appointment_type=AppointmentType.CONSULTATION,
        status="invalid_status",
    )
    db_session.add(invalid_appt)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_timezone_aware_datetime_instant_preserved(db_session: Session) -> None:
    """Verify timezone offset is correctly stored as UTC instant in TIMESTAMPTZ."""
    # 09:30 +05:30 corresponds to 04:00 UTC
    tz_plus_5_30: tzinfo = timezone(timedelta(hours=5, minutes=30))
    appt_time_local = datetime(2026, 10, 20, 9, 30, tzinfo=tz_plus_5_30)
    expected_utc = datetime(2026, 10, 20, 4, 0, tzinfo=UTC)

    appt = Appointment(
        patient_name="Noah Bennett",
        appointment_at=appt_time_local,
        doctor="Dr. Arjun Patel",
        appointment_type=AppointmentType.FOLLOW_UP,
        status=AppointmentStatus.SCHEDULED,
    )
    db_session.add(appt)
    db_session.commit()

    with SessionLocal() as new_session:
        loaded = new_session.get(Appointment, appt.id)
        assert loaded is not None
        # Loaded datetime from Postgres TIMESTAMPTZ is in UTC
        assert loaded.appointment_at == expected_utc


def test_get_db_session_lifecycle() -> None:
    """Verify get_db dependency yields a valid session and closes it cleanly."""
    gen = get_db()
    session = next(gen)
    assert isinstance(session, Session)
    assert session.is_active

    # Closing generator finishes session
    with pytest.raises(StopIteration):
        next(gen)
