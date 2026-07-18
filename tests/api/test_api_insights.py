from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)

ADMIN_HEADERS = {"X-API-Key": "admin-demo-key"}
ANALYST_HEADERS = {"X-API-Key": "analyst-demo-key"}
VIEWER_HEADERS = {"X-API-Key": "viewer-demo-key"}


def test_insights_executive_summary_viewer_access():
    response = client.get("/insights/executive-summary", headers=VIEWER_HEADERS)

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert "key_findings" in body["data"]
    assert "recommended_actions" in body["data"]


def test_insights_sales_performance_analyst_access():
    response = client.get("/insights/sales-performance", headers=ANALYST_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_insights_operational_risk_analyst_access():
    response = client.get("/insights/operational-risk", headers=ANALYST_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_insights_recommendations_admin_access():
    response = client.get("/insights/recommendations", headers=ADMIN_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_llm_context_admin_only_success():
    response = client.get("/insights/llm-context", headers=ADMIN_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_llm_context_viewer_denied():
    response = client.get("/insights/llm-context", headers=VIEWER_HEADERS)

    assert response.status_code == 403