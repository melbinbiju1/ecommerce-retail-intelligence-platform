import os

from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_jwt_login_admin_success(monkeypatch):
    monkeypatch.setenv("JWT_ADMIN_USERNAME", "admin")
    monkeypatch.setenv("JWT_ADMIN_PASSWORD", "admin-test-password")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-jwt-secret")

    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin-test-password",
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"
    assert response_data["role"] == "admin"
    assert response_data["expires_in_minutes"] > 0


def test_jwt_login_invalid_password(monkeypatch):
    monkeypatch.setenv("JWT_ADMIN_USERNAME", "admin")
    monkeypatch.setenv("JWT_ADMIN_PASSWORD", "admin-test-password")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-jwt-secret")

    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_auth_me_with_valid_token(monkeypatch):
    monkeypatch.setenv("JWT_ADMIN_USERNAME", "admin")
    monkeypatch.setenv("JWT_ADMIN_PASSWORD", "admin-test-password")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-jwt-secret")

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin-test-password",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "admin"
    assert response.json()["role"] == "admin"


def test_protected_endpoint_without_token_returns_401():
    response = client.get("/executive/summary")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_viewer_cannot_access_operations(monkeypatch):
    monkeypatch.setenv("JWT_VIEWER_USERNAME", "viewer")
    monkeypatch.setenv("JWT_VIEWER_PASSWORD", "viewer-test-password")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-jwt-secret")

    login_response = client.post(
        "/auth/login",
        data={
            "username": "viewer",
            "password": "viewer-test-password",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/operations/alert-summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to access this resource"