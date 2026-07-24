from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.auth_helpers import ADMIN_HEADERS, ANALYST_HEADERS, VIEWER_HEADERS


client = TestClient(app)


def test_executive_summary_admin_access():
    response = client.get("/executive/summary", headers=ADMIN_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], dict)


def test_executive_summary_viewer_access():
    response = client.get("/executive/summary", headers=VIEWER_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], dict)


def test_monthly_sales_viewer_access():
    response = client.get("/executive/monthly-sales", headers=VIEWER_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], list)


def test_top_products_analyst_access():
    response = client.get("/executive/top-products", headers=ANALYST_HEADERS)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "success"
    assert isinstance(response_data["data"], list)


def test_top_products_viewer_denied():
    response = client.get("/executive/top-products", headers=VIEWER_HEADERS)

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to access this resource"