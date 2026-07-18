from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)

ADMIN_HEADERS = {"X-API-Key": "admin-demo-key"}
ANALYST_HEADERS = {"X-API-Key": "analyst-demo-key"}
VIEWER_HEADERS = {"X-API-Key": "viewer-demo-key"}


def test_executive_summary_admin_access():
    response = client.get("/executive/summary", headers=ADMIN_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_executive_summary_viewer_access():
    response = client.get("/executive/summary", headers=VIEWER_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_monthly_sales_viewer_access():
    response = client.get("/executive/monthly-sales", headers=VIEWER_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_top_products_analyst_access():
    response = client.get("/executive/top-products", headers=ANALYST_HEADERS)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_top_products_viewer_denied():
    response = client.get("/executive/top-products", headers=VIEWER_HEADERS)

    assert response.status_code == 403