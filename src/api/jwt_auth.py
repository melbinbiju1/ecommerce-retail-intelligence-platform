from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

if not JWT_SECRET_KEY:
    JWT_SECRET_KEY = "local-development-jwt-secret-change-me"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Verifies a plain text password against the stored demo password.

    For this portfolio project, demo user passwords are stored as environment
    variables / Key Vault secrets. In a production application, users would
    normally be stored in an identity provider or user database.
    """
    return plain_password == stored_password


def get_demo_users() -> dict:
    """
    Loads demo users from environment variables.

    Roles:
        admin   - full API access
        analyst - analytics and operations access
        viewer  - limited read-only access
    """
    admin_username = os.getenv("JWT_ADMIN_USERNAME", "admin")
    analyst_username = os.getenv("JWT_ANALYST_USERNAME", "analyst")
    viewer_username = os.getenv("JWT_VIEWER_USERNAME", "viewer")

    return {
        admin_username: {
            "username": admin_username,
            "password": os.getenv("JWT_ADMIN_PASSWORD", "admin-password"),
            "role": "admin",
        },
        analyst_username: {
            "username": analyst_username,
            "password": os.getenv("JWT_ANALYST_PASSWORD", "analyst-password"),
            "role": "analyst",
        },
        viewer_username: {
            "username": viewer_username,
            "password": os.getenv("JWT_VIEWER_PASSWORD", "viewer-password"),
            "role": "viewer",
        },
    }


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticates a demo user from environment-backed credentials.
    """
    users = get_demo_users()
    user = users.get(username)

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return {
        "username": user["username"],
        "role": user["role"],
    }


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a signed JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodes and validates a JWT access token.
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "username": username,
            "role": role,
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    FastAPI dependency that returns the current authenticated JWT user.
    """
    return decode_access_token(token)


def require_roles(allowed_roles: list[str]):
    """
    FastAPI dependency factory for JWT role-based authorization.
    Kept for compatibility with any older route or test code.
    """
    def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker