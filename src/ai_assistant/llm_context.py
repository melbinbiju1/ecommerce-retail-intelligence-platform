from __future__ import annotations

from datetime import datetime

from src.api.database import fetch_one, fetch_all


def build_llm_context_summary() -> dict:
    executive_summary = fetch_one("SELECT * FROM vw_executive_summary")

    recent_monthly_sales = fetch_all(
        """
        SELECT *
        FROM vw_monthly_sales
        ORDER BY year_month DESC
        """,
        limit=6,
    )

    alert_summary = fetch_one("SELECT * FROM vw_operational_alert_summary")

    alerts_by_type = fetch_all(
        """
        SELECT *
        FROM vw_operational_alerts_by_type
        ORDER BY alert_count DESC
        """,
        limit=5,
    )

    high_risk_sellers = fetch_all(
        """
        SELECT
            seller_id,
            seller_city,
            seller_state,
            total_orders,
            total_revenue,
            late_delivery_rate,
            avg_review_score,
            seller_risk_level
        FROM vw_high_risk_sellers
        ORDER BY
            CASE seller_risk_level
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                ELSE 3
            END,
            late_delivery_rate DESC,
            avg_review_score ASC
        """,
        limit=5,
    )

    high_risk_categories = fetch_all(
        """
        SELECT
            product_category_name_english,
            total_orders,
            total_revenue,
            avg_review_score,
            late_delivery_rate,
            category_risk_level
        FROM vw_high_risk_categories
        ORDER BY
            CASE category_risk_level
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                ELSE 3
            END,
            late_delivery_rate DESC,
            avg_review_score ASC
        """,
        limit=5,
    )

    context = {
        "context_name": "E-Commerce Retail Intelligence LLM Context",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "purpose": (
            "Structured business context prepared from trusted dbt-built views. "
            "This context can be passed to a future LLM to generate natural-language "
            "executive insights without exposing raw source tables."
        ),
        "data_governance_note": (
            "The LLM should answer only using the provided curated context. "
            "It should not invent figures, expose raw data, or make unsupported claims."
        ),
        "trusted_source_views": [
            "vw_executive_summary",
            "vw_monthly_sales",
            "vw_operational_alert_summary",
            "vw_operational_alerts_by_type",
            "vw_high_risk_sellers",
            "vw_high_risk_categories",
        ],
        "executive_summary": executive_summary,
        "recent_monthly_sales": recent_monthly_sales,
        "operational_alert_summary": alert_summary,
        "top_operational_alert_types": alerts_by_type,
        "sample_high_risk_sellers": high_risk_sellers,
        "sample_high_risk_categories": high_risk_categories,
        "suggested_llm_tasks": [
            "Generate a short executive summary.",
            "Explain the most important operational risks.",
            "Recommend actions for high-risk sellers and categories.",
            "Summarise revenue and order trends.",
            "Create a business-friendly weekly performance update.",
        ],
        "suggested_system_prompt": (
            "You are a business insights assistant for an e-commerce data platform. "
            "Use only the structured context provided. Do not invent numbers. "
            "When a figure is not available, say it is not available. "
            "Explain insights clearly for business users and recommend practical actions."
        ),
    }

    return context