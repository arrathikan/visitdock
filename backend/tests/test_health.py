from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_200() -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_json_payload() -> None:
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_check_content_type() -> None:
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]


def test_nonexistent_route_returns_404() -> None:
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404


def test_openapi_schema_available() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "VisitDock API"
    assert schema["info"]["version"] == "0.1.0"
