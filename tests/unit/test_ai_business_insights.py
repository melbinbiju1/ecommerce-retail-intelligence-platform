from src.ai_assistant.business_insights import (
    generate_executive_summary,
    generate_sales_performance_summary,
    generate_operational_risk_summary,
    generate_recommendations,
    insight_to_dict,
)
from src.ai_assistant.llm_context import build_llm_context_summary


def test_generate_executive_summary():
    insight = generate_executive_summary()
    insight_dict = insight_to_dict(insight)

    assert insight_dict["title"] == "Executive Business Summary"
    assert len(insight_dict["key_findings"]) > 0
    assert len(insight_dict["recommended_actions"]) > 0
    assert "fact_sales" in insight_dict["source_views"]


def test_generate_sales_performance_summary():
    insight = generate_sales_performance_summary()
    insight_dict = insight_to_dict(insight)

    assert insight_dict["title"] == "Sales Performance Summary"
    assert len(insight_dict["key_findings"]) > 0


def test_generate_operational_risk_summary():
    insight = generate_operational_risk_summary()
    insight_dict = insight_to_dict(insight)

    assert insight_dict["title"] == "Operational Risk Summary"
    assert len(insight_dict["recommended_actions"]) > 0


def test_generate_recommendations():
    insight = generate_recommendations()
    insight_dict = insight_to_dict(insight)

    assert insight_dict["title"] == "AI-Ready Business Recommendations"
    assert len(insight_dict["source_views"]) > 0


def test_build_llm_context_summary():
    context = build_llm_context_summary()

    assert context["context_name"] == "E-Commerce Retail Intelligence LLM Context"
    assert "trusted_source_views" in context
    assert "suggested_system_prompt" in context