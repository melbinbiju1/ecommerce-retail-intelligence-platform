from src.api.jwt_auth import create_access_token


def create_test_token(username: str, role: str) -> str:
    """
    Creates a JWT token for API tests.

    The tests use JWT Bearer authentication instead of API keys.
    """
    return create_access_token(
        data={
            "sub": username,
            "role": role,
        }
    )


def auth_headers_for_role(role: str) -> dict:
    """
    Returns Authorization headers for a given test role.
    """
    token = create_test_token(
        username=f"{role}_test_user",
        role=role,
    )

    return {
        "Authorization": f"Bearer {token}",
    }


ADMIN_HEADERS = auth_headers_for_role("admin")
ANALYST_HEADERS = auth_headers_for_role("analyst")
VIEWER_HEADERS = auth_headers_for_role("viewer")