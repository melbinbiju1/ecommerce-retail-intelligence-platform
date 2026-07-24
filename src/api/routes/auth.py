from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.api.jwt_auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    expires_in_minutes: int


class CurrentUserResponse(BaseModel):
    username: str
    role: str


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a demo user and returns a JWT Bearer token.
    """
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "role": user["role"],
        },
        expires_delta=access_token_expires,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        role=user["role"],
        expires_in_minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    )


@router.get("/me", response_model=CurrentUserResponse)
def read_current_user(current_user: dict = Depends(get_current_user)):
    """
    Returns the authenticated JWT user's username and role.
    """
    return CurrentUserResponse(
        username=current_user["username"],
        role=current_user["role"],
    )