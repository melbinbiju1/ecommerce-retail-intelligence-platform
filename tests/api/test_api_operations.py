from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.auth_helpers import ADMIN_HEADERS, ANALYST_HEADERS, VIEWER_HEADERS


client = TestClient(app)


def test_alert_summary_admin_access():
    response = client.get("/operations/alert-summary", headers=ADMIN_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], dict)


def test_alerts_by_type_analyst_access():
    response = client.get("/operations/alerts-by-type", headers=ANALYST_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], list)


def test_recent_alerts_limit():
    response = client.get("/operations/recent-alerts?limit=5", headers=ANALYST_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], list)
    assert len(response_data["data"]) <= 5


def test_high_risk_sellers_access():
    response = client.get("/operations/high-risk-sellers?limit=5", headers=ADMIN_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], list)
    assert len(response_data["data"]) <= 5


def test_operations_viewer_denied():
    response = client.get("/operations/alert-summary", headers=VIEWER_HEADERS)

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to access this resource"