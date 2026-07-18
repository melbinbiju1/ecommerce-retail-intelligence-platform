import os
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


DEMO_API_KEYS = {
    os.getenv("ADMIN_API_KEY", "admin-demo-key"): "admin",
    os.getenv("ANALYST_API_KEY", "analyst-demo-key"): "analyst",
    os.getenv("VIEWER_API_KEY", "viewer-demo-key"): "viewer",
}


def get_current_role(api_key: str | None = Depends(api_key_header)) -> str:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide X-API-Key header.",
        )

    role = DEMO_API_KEYS.get(api_key)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )

    return role


def require_roles(allowed_roles: list[str]):
    def role_checker(current_role: str = Depends(get_current_role)) -> str:
        if current_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}",
            )

        return current_role

    return role_checker