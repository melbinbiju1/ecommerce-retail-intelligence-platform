from fastapi import APIRouter

from src.api.schemas import HealthResponse, SystemStatusResponse
from src.api.database import (
    check_database_connection,
    check_database_object_exists,
)


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
def health_check() -> HealthResponse:
    database_connected = check_database_connection()

    return HealthResponse(
        status="ok" if database_connected else "error",
        service="E-Commerce Retail Intelligence API",
        database_connected=database_connected,
    )


@router.get("/status", response_model=SystemStatusResponse)
def system_status() -> SystemStatusResponse:
    important_objects = [
        "fact_sales",
        "dim_customer",
        "dim_seller",
        "vw_executive_summary",
        "vw_monthly_sales",
        "vw_operational_alert_summary",
        "vw_operational_alerts_by_type",
        "vw_high_risk_sellers",
        "vw_high_risk_categories",
    ]

    object_status = {
        object_name: check_database_object_exists(object_name)
        for object_name in important_objects
    }

    database_connected = check_database_connection()
    all_objects_available = all(object_status.values())

    return SystemStatusResponse(
        status="ok" if database_connected and all_objects_available else "warning",
        service="E-Commerce Retail Intelligence API",
        database_connected=database_connected,
        checked_objects=object_status,
    )