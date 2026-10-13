"""Browser integration and privacy regression tests."""

import pytest
from sqlalchemy.exc import OperationalError

from app.appointments.models import Appointment
from app.core.config import Settings
from app.db.session import get_db
from app.main import app


def test_allowed_cors_preflight(client):
    response = client.options("/api/v1/appointments", headers={
        "Origin": "http://localhost:3000", "Access-Control-Request-Method": "PUT",
        "Access-Control-Request-Headers": "content-type",
    })
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    rejected = client.options("/api/v1/appointments", headers={
        "Origin": "https://untrusted.example", "Access-Control-Request-Method": "POST",
    })
    assert "access-control-allow-origin" not in rejected.headers


def test_database_failure_redacted(client):
    def failed_db():
        raise OperationalError("secret SQL", {}, Exception("credential and patient"))
    original = app.dependency_overrides[get_db]
    app.dependency_overrides[get_db] = failed_db
    try:
        response = client.get("/api/v1/appointments")
        assert response.status_code == 503
        assert response.json() == {"detail": "Appointment service unavailable"}
    finally:
        app.dependency_overrides[get_db] = original


def test_repr_omits_names():
    appointment = Appointment(patient_name="Fictional Private", doctor="Fictional Doctor")
    assert "Private" not in repr(appointment)
    assert "Doctor" not in repr(appointment)


def test_invalid_timezone_rejected():
    with pytest.raises(ValueError, match="IANA"):
        Settings(CLINIC_TIMEZONE="Invalid/Zone")
