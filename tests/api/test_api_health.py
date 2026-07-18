from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "E-Commerce Retail Intelligence API"


def test_health_endpoint():
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json()["database_connected"] is True


def test_system_status_endpoint():
    response = client.get("/health/status")

    assert response.status_code == 200
    assert "checked_objects" in response.json()