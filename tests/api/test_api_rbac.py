from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_missing_api_key_denied_for_protected_endpoint():
    response = client.get("/executive/summary")

    assert response.status_code == 401


def test_invalid_api_key_denied():
    response = client.get(
        "/executive/summary",
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 403


def test_public_health_endpoint_without_api_key():
    response = client.get("/health/")

    assert response.status_code == 200


def test_viewer_allowed_for_limited_endpoint():
    response = client.get(
        "/executive/monthly-sales",
        headers={"X-API-Key": "viewer-demo-key"},
    )

    assert response.status_code == 200


def test_viewer_denied_for_operations_endpoint():
    response = client.get(
        "/operations/risk-summary",
        headers={"X-API-Key": "viewer-demo-key"},
    )

    assert response.status_code == 403