from pydantic import BaseModel
from typing import Any


class HealthResponse(BaseModel):
    status: str
    service: str
    database_connected: bool


class SystemStatusResponse(BaseModel):
    status: str
    service: str
    database_connected: bool
    checked_objects: dict[str, bool]


class APIResponse(BaseModel):
    status: str
    data: Any


class ErrorResponse(BaseModel):
    status: str
    message: str