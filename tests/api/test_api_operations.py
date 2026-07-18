from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)

ADMIN_HEADERS = {"X-API-Key": "admin-demo-key"}
ANALYST_HEADERS = {"X-API-Key": "analyst-demo-key"}
VIEWER_HEADERS = {"X-API-Key": "viewer-demo-key"}


def test_alert_summary_admin_access():
    response = client.get("/operations/alert-summary", headers=ADMIN_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_alerts_by_type_analyst_access():
    response = client.get("/operations/alerts-by-type", headers=ANALYST_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_recent_alerts_limit():
    response = client.get("/operations/recent-alerts?limit=5", headers=ANALYST_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) <= 5


def test_high_risk_sellers_access():
    response = client.get("/operations/high-risk-sellers?limit=5", headers=ADMIN_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_operations_viewer_denied():
    response = client.get("/operations/alert-summary", headers=VIEWER_HEADERS)

    assert response.status_code == 403