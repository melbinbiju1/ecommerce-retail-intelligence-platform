from fastapi import Depends, HTTPException, status

from src.api.jwt_auth import get_current_user


ROLE_PERMISSIONS = {
    "admin": {
        "executive": True,
        "operations": True,
        "insights": True,
        "admin": True,
    },
    "analyst": {
        "executive": True,
        "operations": True,
        "insights": True,
        "admin": False,
    },
    "viewer": {
        "executive": True,
        "operations": False,
        "insights": False,
        "admin": False,
    },
}


def require_permission(permission_name: str):
    """
    FastAPI dependency factory for role-based permission checks.

    Authentication is handled by JWT Bearer token validation.
    Authorization is handled by checking the user's role against the
    permission map above.
    """

    def permission_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")

        if user_role not in ROLE_PERMISSIONS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unknown user role",
            )

        has_permission = ROLE_PERMISSIONS[user_role].get(permission_name, False)

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return permission_checker


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Requires the current JWT user to have the admin role.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


def require_executive_access(
    current_user: dict = Depends(require_permission("executive")),
) -> dict:
    """
    Allows users with executive analytics access.
    """
    return current_user


def require_operations_access(
    current_user: dict = Depends(require_permission("operations")),
) -> dict:
    """
    Allows users with operational analytics access.
    """
    return current_user


def require_insights_access(
    current_user: dict = Depends(require_permission("insights")),
) -> dict:
    """
    Allows users with AI-ready insights access.
    """
    return current_user