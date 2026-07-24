from fastapi import APIRouter, Depends

from src.api.dependencies import require_admin, require_insights_access, require_executive_access
from src.api.schemas import APIResponse
from src.ai_assistant.business_insights import (
    generate_executive_summary,
    generate_sales_performance_summary,
    generate_operational_risk_summary,
    generate_recommendations,
    insight_to_dict,
)
from src.ai_assistant.llm_context import build_llm_context_summary


router = APIRouter(prefix="/insights", tags=["AI-Ready Business Insights"])


@router.get("/executive-summary", response_model=APIResponse)
def get_ai_executive_summary(
    current_user: dict = Depends(require_executive_access),
) -> APIResponse:
    insight = generate_executive_summary()

    return APIResponse(
        status="success",
        data=insight_to_dict(insight),
    )


@router.get("/sales-performance", response_model=APIResponse)
def get_ai_sales_performance(
    current_user: dict = Depends(require_insights_access),
) -> APIResponse:
    insight = generate_sales_performance_summary()

    return APIResponse(
        status="success",
        data=insight_to_dict(insight),
    )


@router.get("/operational-risk", response_model=APIResponse)
def get_ai_operational_risk(
    current_user: dict = Depends(require_insights_access),
) -> APIResponse:
    insight = generate_operational_risk_summary()

    return APIResponse(
        status="success",
        data=insight_to_dict(insight),
    )


@router.get("/recommendations", response_model=APIResponse)
def get_ai_recommendations(
    current_user: dict = Depends(require_insights_access),
) -> APIResponse:
    insight = generate_recommendations()

    return APIResponse(
        status="success",
        data=insight_to_dict(insight),
    )


@router.get("/llm-context", response_model=APIResponse)
def get_llm_context(
    current_user: dict = Depends(require_admin),
) -> APIResponse:
    context = build_llm_context_summary()

    return APIResponse(
        status="success",
        data=context,
    )