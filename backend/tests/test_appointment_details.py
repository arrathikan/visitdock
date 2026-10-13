"""Database-backed details, replacement and deletion regressions."""

from uuid import uuid4

import pytest

BASE = "/api/v1/appointments"
PAYLOAD = {
    "patient_name": "Fictional Rowan",
    "doctor": "Dr. Fictional Avery",
    "appointment_at": "2026-10-20T09:30:00+05:30",
    "appointment_type": "consultation",
    "status": "scheduled",
}


def test_crud_and_identical_put_timestamp(client):
    original = client.post(BASE, json=PAYLOAD).json()
    url = f"{BASE}/{original['id']}"
    assert client.get(url).json() == original
    replacement = {
        **PAYLOAD, "patient_name": "  Fictional Robin  ", "doctor": "Dr. Fictional Sage",
        "appointment_at": "2026-10-21T12:00:00Z",
        "appointment_type": "follow_up", "status": "completed",
    }
    response = client.put(url, json=replacement)
    assert response.status_code == 200
    updated = response.json()
    assert updated["patient_name"] == "Fictional Robin"
    assert updated["doctor"] == replacement["doctor"]
    assert updated["appointment_at"] == replacement["appointment_at"]
    assert updated["status"] == "completed"
    assert updated["appointment_type"] == "follow_up"
    assert updated["created_at"] == original["created_at"]
    assert updated["updated_at"] > original["updated_at"]
    assert client.get(url).json() == updated
    identical = client.put(url, json=replacement).json()
    assert identical["updated_at"] > updated["updated_at"]
    deleted = client.delete(url)
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(url).status_code == 404
    assert client.delete(url).status_code == 404
    assert client.get(BASE).json()["total"] == 0


@pytest.mark.parametrize("method", ["get", "put", "delete"])
@pytest.mark.parametrize("identifier,expected", [("malformed", 422), (str(uuid4()), 404)])
def test_details_missing_and_invalid_ids(client, method, identifier, expected):
    kwargs = {"json": PAYLOAD} if method == "put" else {}
    response = getattr(client, method)(f"{BASE}/{identifier}", **kwargs)
    assert response.status_code == expected
    if expected == 404:
        assert response.json() == {"detail": "Appointment not found"}


@pytest.mark.parametrize("field,value", [
    ("patient_name", " "), ("doctor", "D" * 151), ("status", "unknown"),
    ("appointment_type", "unknown"), ("appointment_at", "2026-10-20T09:30:00"),
    ("id", "client-controlled"),
])
def test_invalid_replacement_preserves_record(client, field, value):
    original = client.post(BASE, json=PAYLOAD).json()
    url = f"{BASE}/{original['id']}"
    assert client.put(url, json={**PAYLOAD, field: value}).status_code == 422
    assert client.get(url).json() == original


@pytest.mark.parametrize("field", list(PAYLOAD))
def test_put_requires_all_fields(client, field):
    original = client.post(BASE, json=PAYLOAD).json()
    replacement = dict(PAYLOAD)
    del replacement[field]
    assert client.put(f"{BASE}/{original['id']}", json=replacement).status_code == 422
