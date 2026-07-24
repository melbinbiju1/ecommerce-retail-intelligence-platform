from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.auth_helpers import ADMIN_HEADERS, ANALYST_HEADERS, VIEWER_HEADERS


client = TestClient(app)


def test_insights_executive_summary_viewer_access():
    response = client.get("/insights/executive-summary", headers=VIEWER_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], dict)


def test_insights_sales_performance_analyst_access():
    response = client.get("/insights/sales-performance", headers=ANALYST_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], dict)


def test_insights_operational_risk_analyst_access():
    response = client.get("/insights/operational-risk", headers=ANALYST_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], dict)


def test_insights_recommendations_admin_access():
    response = client.get("/insights/recommendations", headers=ADMIN_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], dict)


def test_llm_context_admin_only_success():
    response = client.get("/insights/llm-context", headers=ADMIN_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], dict)


def test_llm_context_viewer_denied():
    response = client.get("/insights/llm-context", headers=VIEWER_HEADERS)

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"