"""API integration tests for creating and listing appointments."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.appointments.models import Appointment, AppointmentStatus, AppointmentType


def test_create_appointment_success(client: TestClient, db_session: Session) -> None:
    """Verify that a valid appointment returns HTTP 201 and persists to PostgreSQL."""
    payload = {
        "patient_name": "  Emma Wilson  ",
        "appointment_at": "2026-10-20T09:30:00+05:30",
        "doctor": "  Dr. Maya Carter  ",
        "appointment_type": "consultation",
        "status": "scheduled",
    }
    response = client.post("/api/v1/appointments", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert uuid.UUID(data["id"])
    assert data["patient_name"] == "Emma Wilson"
    assert data["doctor"] == "Dr. Maya Carter"
    assert data["appointment_at"] == "2026-10-20T04:00:00Z"
    assert data["appointment_type"] == "consultation"
    assert data["status"] == "scheduled"
    assert data["created_at"].endswith("Z")
    assert data["updated_at"].endswith("Z")

    # Verify persistence directly from the isolated test session
    persisted = db_session.get(Appointment, uuid.UUID(data["id"]))
    assert persisted is not None
    assert persisted.patient_name == "Emma Wilson"
    assert persisted.doctor == "Dr. Maya Carter"
    assert persisted.appointment_type == "consultation"
    assert persisted.status == "scheduled"
    assert persisted.appointment_at == datetime(2026, 10, 20, 4, 0, tzinfo=UTC)


@pytest.mark.parametrize("whitespace_name", ["", "   ", "\t\n  "])
def test_create_appointment_whitespace_names_rejected(
    client: TestClient, whitespace_name: str
) -> None:
    """Verify whitespace-only patient and doctor names return HTTP 422."""
    payload_patient = {
        "patient_name": whitespace_name,
        "appointment_at": "2026-10-20T09:30:00Z",
        "doctor": "Dr. Maya Carter",
        "appointment_type": "consultation",
        "status": "scheduled",
    }
    res1 = client.post("/api/v1/appointments", json=payload_patient)
    assert res1.status_code == 422

    payload_doctor = {
        "patient_name": "Emma Wilson",
        "appointment_at": "2026-10-20T09:30:00Z",
        "doctor": whitespace_name,
        "appointment_type": "consultation",
        "status": "scheduled",
    }
    res2 = client.post("/api/v1/appointments", json=payload_doctor)
    assert res2.status_code == 422


@pytest.mark.parametrize(
    "missing_field",
    ["patient_name", "appointment_at", "doctor", "appointment_type", "status"],
)
def test_create_appointment_missing_required_fields(
    client: TestClient, missing_field: str
) -> None:
    """Verify missing required fields return HTTP 422."""
    payload = {
        "patient_name": "Emma Wilson",
        "appointment_at": "2026-10-20T09:30:00Z",
        "doctor": "Dr. Maya Carter",
        "appointment_type": "consultation",
        "status": "scheduled",
    }
    del payload[missing_field]
    response = client.post("/api/v1/appointments", json=payload)
    assert response.status_code == 422


def test_create_appointment_invalid_enums_rejected(client: TestClient) -> None:
    """Verify invalid appointment_type and status values return HTTP 422."""
    base_payload = {
        "patient_name": "Emma Wilson",
        "appointment_at": "2026-10-20T09:30:00Z",
        "doctor": "Dr. Maya Carter",
        "appointment_type": "consultation",
        "status": "scheduled",
    }

    res1 = client.post(
        "/api/v1/appointments",
        json={**base_payload, "appointment_type": "invalid_type"},
    )
    assert res1.status_code == 422

    res2 = client.post(
        "/api/v1/appointments",
        json={**base_payload, "status": "invalid_status"},
    )
    assert res2.status_code == 422


@pytest.mark.parametrize(
    "invalid_dt",
    [
        "2026-10-20T09:30:00",  # naive datetime without offset
        "2026-10-20",  # date only
        "invalid-date-string",
        "",
    ],
)
def test_create_appointment_naive_or_malformed_datetime_rejected(
    client: TestClient, invalid_dt: str
) -> None:
    """Verify offset-less or malformed datetime strings return HTTP 422."""
    payload = {
        "patient_name": "Emma Wilson",
        "appointment_at": invalid_dt,
        "doctor": "Dr. Maya Carter",
        "appointment_type": "consultation",
        "status": "scheduled",
    }
    response = client.post("/api/v1/appointments", json=payload)
    assert response.status_code == 422


def test_create_appointment_overlong_names_rejected(client: TestClient) -> None:
    """Verify names exceeding 150 characters are rejected with HTTP 422."""
    payload = {
        "patient_name": "A" * 151,
        "appointment_at": "2026-10-20T09:30:00Z",
        "doctor": "Dr. Maya Carter",
        "appointment_type": "consultation",
        "status": "scheduled",
    }
    res1 = client.post("/api/v1/appointments", json=payload)
    assert res1.status_code == 422

    payload["patient_name"] = "Emma Wilson"
    payload["doctor"] = "D" * 151
    res2 = client.post("/api/v1/appointments", json=payload)
    assert res2.status_code == 422


@pytest.mark.parametrize("extra_key", ["id", "created_at", "updated_at", "role", "unknown"])
def test_create_appointment_extra_fields_rejected(client: TestClient, extra_key: str) -> None:
    """Verify unexpected client-supplied fields are rejected with HTTP 422."""
    payload = {
        "patient_name": "Emma Wilson",
        "appointment_at": "2026-10-20T09:30:00Z",
        "doctor": "Dr. Maya Carter",
        "appointment_type": "consultation",
        "status": "scheduled",
        extra_key: "forbidden_value",
    }
    response = client.post("/api/v1/appointments", json=payload)
    assert response.status_code == 422


def test_create_appointment_preserves_utc_instant(
    client: TestClient, db_session: Session
) -> None:
    """Verify timezone offset (09:30 +05:30) is accurately preserved as 04:00 UTC."""
    payload = {
        "patient_name": "Noah Bennett",
        "appointment_at": "2026-10-20T09:30:00+05:30",
        "doctor": "Dr. Arjun Patel",
        "appointment_type": "follow_up",
        "status": "scheduled",
    }
    response = client.post("/api/v1/appointments", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["appointment_at"] == "2026-10-20T04:00:00Z"

    persisted = db_session.get(Appointment, uuid.UUID(data["id"]))
    assert persisted is not None
    assert persisted.appointment_at == datetime(2026, 10, 20, 4, 0, tzinfo=UTC)


# --- LIST ENDPOINT TESTS ---


def test_list_appointments_empty_database(client: TestClient) -> None:
    """Verify GET /api/v1/appointments returns empty items and 0 total when no records exist."""
    response = client.get("/api/v1/appointments")
    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
    }


def test_list_appointments_default_pagination(client: TestClient, db_session: Session) -> None:
    """Verify default pagination returns items with page=1 and page_size=20."""
    now = datetime.now(UTC)
    for i in range(3):
        appt = Appointment(
            patient_name=f"Patient {i}",
            appointment_at=now + timedelta(hours=i),
            doctor="Dr. Carter",
            appointment_type=AppointmentType.CONSULTATION,
            status=AppointmentStatus.SCHEDULED,
        )
        db_session.add(appt)
    db_session.commit()

    response = client.get("/api/v1/appointments")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert len(data["items"]) == 3


def test_list_appointments_custom_pagination(client: TestClient, db_session: Session) -> None:
    """Verify custom page and page_size parameters paginate records accurately."""
    base_time = datetime(2026, 11, 1, 9, 0, tzinfo=UTC)
    for i in range(5):
        appt = Appointment(
            patient_name=f"Patient {i}",
            appointment_at=base_time + timedelta(hours=i),
            doctor="Dr. Carter",
            appointment_type=AppointmentType.CONSULTATION,
            status=AppointmentStatus.SCHEDULED,
        )
        db_session.add(appt)
    db_session.commit()

    # Request page 2 with page_size 2 (should return items 2 and 3)
    response = client.get("/api/v1/appointments?page=2&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert len(data["items"]) == 2
    assert data["items"][0]["patient_name"] == "Patient 2"
    assert data["items"][1]["patient_name"] == "Patient 3"


def test_list_appointments_deterministic_sorting(
    client: TestClient, db_session: Session
) -> None:
    """Verify appointments are sorted by appointment_at ASC deterministically."""
    t1 = datetime(2026, 12, 1, 10, 0, tzinfo=UTC)
    t2 = datetime(2026, 12, 2, 10, 0, tzinfo=UTC)
    t3 = datetime(2026, 12, 3, 10, 0, tzinfo=UTC)

    # Insert out of chronological order
    for t, name in [(t3, "Third"), (t1, "First"), (t2, "Second")]:
        db_session.add(
            Appointment(
                patient_name=name,
                appointment_at=t,
                doctor="Dr. Carter",
                appointment_type=AppointmentType.CONSULTATION,
                status=AppointmentStatus.SCHEDULED,
            )
        )
    db_session.commit()

    response = client.get("/api/v1/appointments")
    assert response.status_code == 200
    names = [item["patient_name"] for item in response.json()["items"]]
    assert names == ["First", "Second", "Third"]


def test_list_appointments_same_timestamp_sorted_by_id(
    client: TestClient, db_session: Session
) -> None:
    """Verify appointments at the exact same timestamp are tie-broken stably by id ASC."""
    same_time = datetime(2026, 10, 20, 9, 30, tzinfo=UTC)
    appts = [
        Appointment(
            patient_name=f"Patient {i}",
            appointment_at=same_time,
            doctor="Dr. Carter",
            appointment_type=AppointmentType.CONSULTATION,
            status=AppointmentStatus.SCHEDULED,
        )
        for i in range(4)
    ]
    db_session.add_all(appts)
    db_session.commit()

    response = client.get("/api/v1/appointments")
    assert response.status_code == 200
    items = response.json()["items"]
    ids = [item["id"] for item in items]
    assert ids == sorted(ids)


def test_list_appointments_out_of_range_page(client: TestClient, db_session: Session) -> None:
    """Verify that requesting a page beyond available records returns items: [] without error."""
    db_session.add(
        Appointment(
            patient_name="Lone Patient",
            appointment_at=datetime.now(UTC),
            doctor="Dr. Carter",
            appointment_type=AppointmentType.CONSULTATION,
            status=AppointmentStatus.SCHEDULED,
        )
    )
    db_session.commit()

    response = client.get("/api/v1/appointments?page=10&page_size=20")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 1
    assert data["page"] == 10
    assert data["page_size"] == 20


@pytest.mark.parametrize(
    ("page", "page_size"),
    [
        (0, 20),
        (-1, 20),
        (1, 0),
        (1, -5),
        (1, 101),  # Exceeds max 100
    ],
)
def test_list_appointments_invalid_pagination_rejected(
    client: TestClient, page: int, page_size: int
) -> None:
    """Verify invalid pagination query parameters return HTTP 422."""
    response = client.get(f"/api/v1/appointments?page={page}&page_size={page_size}")
    assert response.status_code == 422


def test_list_appointments_max_page_size_allowed(client: TestClient) -> None:
    """Verify page_size=100 is accepted as the maximum allowed page size."""
    response = client.get("/api/v1/appointments?page=1&page_size=100")
    assert response.status_code == 200
    assert response.json()["page_size"] == 100
