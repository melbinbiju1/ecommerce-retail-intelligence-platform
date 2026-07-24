from fastapi import APIRouter, Depends, Query

from src.api.database import fetch_one, fetch_all
from src.api.dependencies import require_executive_access, require_permission
from src.api.schemas import APIResponse


router = APIRouter(prefix="/executive", tags=["Executive"])


@router.get("/summary", response_model=APIResponse)
def get_executive_summary(
    current_user: dict = Depends(require_executive_access),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_executive_summary
    """

    data = fetch_one(query)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/monthly-sales", response_model=APIResponse)
def get_monthly_sales(
    current_user: dict = Depends(require_executive_access),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_monthly_sales
    ORDER BY year_month
    """

    data = fetch_all(query)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/top-products", response_model=APIResponse)
def get_top_products(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: dict = Depends(require_permission("insights")),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_product_performance
    ORDER BY total_revenue DESC
    """

    data = fetch_all(query, limit=limit)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/top-sellers", response_model=APIResponse)
def get_top_sellers(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: dict = Depends(require_permission("insights")),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_seller_performance
    ORDER BY total_revenue DESC
    """

    data = fetch_all(query, limit=limit)

    return APIResponse(
        status="success",
        data=data,
    )


@router.get("/customer-states", response_model=APIResponse)
def get_customer_states(
    current_user: dict = Depends(require_permission("insights")),
) -> APIResponse:
    query = """
    SELECT *
    FROM vw_customer_state_performance
    ORDER BY total_revenue DESC
    """

    data = fetch_all(query)

    return APIResponse(
        status="success",
        data=data,
    )