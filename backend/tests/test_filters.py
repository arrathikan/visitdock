"""Search and local calendar boundaries against real PostgreSQL."""

import pytest

from app.core.config import settings
from tests.test_appointment_details import BASE, PAYLOAD


def seed(client):
    for name, doctor, at, status in [
        ("Fictional Rowan", "Dr. Fictional Avery", "2026-10-19T18:29:59Z", "scheduled"),
        ("Fictional Robin", "Dr. Fictional Sage", "2026-10-19T18:30:00Z", "completed"),
        ("Fictional 100%_", "Dr. Fictional Avery", "2026-10-20T18:29:59Z", "scheduled"),
        ("Fictional End", "Dr. Fictional Avery", "2026-10-20T18:30:00Z", "scheduled"),
    ]:
        assert client.post(BASE, json={**PAYLOAD, "patient_name": name, "doctor": doctor,
                                     "appointment_at": at, "status": status}).status_code == 201


@pytest.mark.parametrize("params,total", [
    ({"search": "rOwAn"}, 1), ({"search": "  SAGE  "}, 1),
    ({"doctor": " dr. fictional AVERY "}, 3), ({"status": "completed"}, 1),
    ({"search": "%_"}, 1), ({"search": "unknown"}, 0),
    ({"doctor": "unknown"}, 0), ({"search": "fictional", "status": "completed",
                                  "doctor": "Dr. Fictional Sage"}, 1),
    ({"search": "Rowan", "status": "completed"}, 0),
    ({"search": " "}, 4),
])
def test_filters(client, params, total):
    seed(client)
    response = client.get(BASE, params=params)
    assert response.status_code == 200
    assert response.json()["total"] == total
    assert len(response.json()["items"]) == total


def test_colombo_boundaries_and_filtered_pagination(client, monkeypatch):
    monkeypatch.setattr(settings, "CLINIC_TIMEZONE", "Asia/Colombo")
    seed(client)
    response = client.get(BASE, params={"date": "2026-10-20", "page_size": 1, "page": 2})
    assert response.json()["total"] == 2
    assert response.json()["items"][0]["patient_name"] == "Fictional 100%_"


@pytest.mark.parametrize("day,start,end", [
    ("2026-03-08", "2026-03-08T05:00:00Z", "2026-03-09T04:00:00Z"),
    ("2026-11-01", "2026-11-01T04:00:00Z", "2026-11-02T05:00:00Z"),
])
def test_dst_days(client, monkeypatch, day, start, end):
    monkeypatch.setattr(settings, "CLINIC_TIMEZONE", "America/New_York")
    for at in [start, end]:
        client.post(BASE, json={**PAYLOAD, "appointment_at": at})
    data = client.get(BASE, params={"date": day}).json()
    assert data["total"] == 1
    assert data["items"][0]["appointment_at"] == start


@pytest.mark.parametrize("params", [
    {"date": "nonsense"}, {"date": "2026-02-30"}, {"date": "9999-12-31"},
    {"status": "unknown"}, {"search": "x" * 151}, {"doctor": "x" * 151},
])
def test_invalid_filters(client, params):
    assert client.get(BASE, params=params).status_code == 422
