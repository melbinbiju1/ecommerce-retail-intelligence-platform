from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.auth_helpers import ADMIN_HEADERS, ANALYST_HEADERS, VIEWER_HEADERS


client = TestClient(app)


def test_missing_token_denied():
    response = client.get("/executive/summary")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_invalid_bearer_token_denied():
    response = client.get(
        "/executive/summary",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired authentication token"


def test_admin_allowed_for_protected_endpoint():
    response = client.get(
        "/operations/risk-summary",
        headers=ADMIN_HEADERS,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"


def test_viewer_allowed_for_limited_endpoint():
    response = client.get(
        "/executive/monthly-sales",
        headers=VIEWER_HEADERS,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"


def test_viewer_denied_for_operations_endpoint():
    response = client.get(
        "/operations/risk-summary",
        headers=VIEWER_HEADERS,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to access this resource"


def test_analyst_allowed_for_operations_endpoint():
    response = client.get(
        "/operations/risk-summary",
        headers=ANALYST_HEADERS,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"


def test_viewer_denied_for_admin_only_endpoint():
    response = client.get(
        "/insights/llm-context",
        headers=VIEWER_HEADERS,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"