from fastapi import APIRouter, Query, Depends

from src.api.database import fetch_one, fetch_all
from src.api.schemas import APIResponse
from src.api.auth import require_roles


router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get("/alert-summary", response_model=APIResponse)
def get_alert_summary(
    role: str = Depends(require_roles(["admin", "analyst"])),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_operational_alert_summary
    """

    data = fetch_one(query)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/alerts-by-type", response_model=APIResponse)
def get_alerts_by_type(
    role: str = Depends(require_roles(["admin", "analyst"])),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_operational_alerts_by_type
    ORDER BY alert_count DESC
    """

    data = fetch_all(query)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/alerts-by-severity", response_model=APIResponse)
def get_alerts_by_severity(
    role: str = Depends(require_roles(["admin", "analyst"])),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_operational_alerts_by_severity
    ORDER BY alert_count DESC
    """

    data = fetch_all(query)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/recent-alerts", response_model=APIResponse)
def get_recent_alerts(
    limit: int = Query(default=20, ge=1, le=100),
    role: str = Depends(require_roles(["admin", "analyst"])),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_recent_operational_alerts
    ORDER BY created_at DESC
    """

    data = fetch_all(query, limit=limit)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/high-risk-sellers", response_model=APIResponse)
def get_high_risk_sellers(
    limit: int = Query(default=20, ge=1, le=100),
    role: str = Depends(require_roles(["admin", "analyst"])),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_high_risk_sellers
    ORDER BY 
        CASE seller_risk_level
            WHEN 'high' THEN 1
            WHEN 'medium' THEN 2
            ELSE 3
        END,
        late_delivery_rate DESC,
        avg_review_score ASC
    """

    data = fetch_all(query, limit=limit)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/high-risk-categories", response_model=APIResponse)
def get_high_risk_categories(
    limit: int = Query(default=20, ge=1, le=100),
    role: str = Depends(require_roles(["admin", "analyst"])),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_high_risk_categories
    ORDER BY 
        CASE category_risk_level
            WHEN 'high' THEN 1
            WHEN 'medium' THEN 2
            ELSE 3
        END,
        late_delivery_rate DESC,
        avg_review_score ASC
    """

    data = fetch_all(query, limit=limit)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/risk-summary", response_model=APIResponse)
def get_risk_summary(
    role: str = Depends(require_roles(["admin", "analyst"])),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_operational_risk_summary
    """

    data = fetch_all(query)

    return APIResponse(
        status="success",
        data=data,
    )