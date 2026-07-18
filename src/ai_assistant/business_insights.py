from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.api.database import fetch_one, fetch_all


@dataclass
class InsightResult:
    title: str
    summary: str
    key_findings: list[str]
    recommended_actions: list[str]
    source_views: list[str]


def _safe_number(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    return int(_safe_number(value, default))


def _get_first_existing_value(
    row: dict,
    possible_columns: list[str],
    default: Any = None,
) -> Any:
    for column in possible_columns:
        if column in row and row[column] is not None:
            return row[column]
    return default


def generate_executive_summary() -> InsightResult:
    platform_totals = fetch_one(
        """
        SELECT
            COALESCE(SUM(item_total_value), 0) AS total_revenue,
            COUNT(DISTINCT order_id) AS total_orders,
            COALESCE(SUM(freight_value), 0) AS total_freight_value
        FROM fact_sales
        """
    )

    customer_totals = fetch_one(
        """
        SELECT
            COUNT(DISTINCT customer_unique_id) AS total_customers
        FROM dim_customer
        """
    )

    seller_totals = fetch_one(
        """
        SELECT
            COUNT(DISTINCT seller_id) AS total_sellers
        FROM dim_seller
        """
    )

    monthly_sales = fetch_all(
        """
        SELECT *
        FROM vw_monthly_sales
        WHERE total_orders >= 10
        ORDER BY year_month DESC
        """,
        limit=3,
    )

    total_revenue = _safe_number(platform_totals.get("total_revenue"))
    total_orders = _safe_int(platform_totals.get("total_orders"))
    total_customers = _safe_int(customer_totals.get("total_customers"))
    total_sellers = _safe_int(seller_totals.get("total_sellers"))

    avg_order_value = 0.0
    if total_orders > 0:
        avg_order_value = total_revenue / total_orders

    key_findings = [
        f"The platform processed {total_orders:,.0f} orders with total revenue value of {total_revenue:,.2f}.",
        f"The business includes {total_customers:,.0f} unique customers and {total_sellers:,.0f} sellers.",
        f"The average order value is {avg_order_value:,.2f}.",
    ]

    if monthly_sales:
        latest_month = monthly_sales[0]
        latest_period = latest_month.get("year_month")
        latest_revenue = _safe_number(latest_month.get("total_revenue"))
        latest_orders = _safe_int(latest_month.get("total_orders"))

        key_findings.append(
            f"The latest meaningful sales period is {latest_period}, with revenue of {latest_revenue:,.2f} from {latest_orders:,.0f} orders."
        )

    recommended_actions = [
        "Monitor monthly revenue and order trends to identify demand changes early.",
        "Use customer geography and product category performance to find priority growth areas.",
        "Review sales KPIs together with operational alerts before making business decisions.",
    ]

    return InsightResult(
        title="Executive Business Summary",
        summary=(
            "The e-commerce platform shows business performance across revenue, "
            "orders, customers, sellers, and recent monthly trends."
        ),
        key_findings=key_findings,
        recommended_actions=recommended_actions,
        source_views=[
            "fact_sales",
            "dim_customer",
            "dim_seller",
            "vw_monthly_sales",
        ],
    )


def generate_sales_performance_summary() -> InsightResult:
    top_products = fetch_all(
        """
        SELECT *
        FROM vw_product_performance
        ORDER BY total_revenue DESC
        """,
        limit=5,
    )

    customer_states = fetch_all(
        """
        SELECT *
        FROM vw_customer_state_performance
        ORDER BY total_revenue DESC
        """,
        limit=5,
    )

    key_findings = []

    if top_products:
        top_category = top_products[0]
        key_findings.append(
            "The highest revenue product category is "
            f"{top_category.get('product_category_name_english')} with revenue of "
            f"{_safe_number(top_category.get('total_revenue')):,.2f}."
        )

    if customer_states:
        top_state = customer_states[0]
        key_findings.append(
            "The highest revenue customer state is "
            f"{top_state.get('customer_state')} with revenue of "
            f"{_safe_number(top_state.get('total_revenue')):,.2f}."
        )

    if not key_findings:
        key_findings.append(
            "Sales performance views are available, but no detailed records were returned in the current query."
        )

    recommended_actions = [
        "Prioritise high-performing product categories in dashboard storytelling.",
        "Use customer state performance to identify strong regional demand.",
        "Compare product revenue with review scores to avoid focusing only on sales volume.",
    ]

    return InsightResult(
        title="Sales Performance Summary",
        summary=(
            "The sales performance layer highlights product category performance and customer geography patterns."
        ),
        key_findings=key_findings,
        recommended_actions=recommended_actions,
        source_views=[
            "vw_product_performance",
            "vw_customer_state_performance",
        ],
    )


def generate_operational_risk_summary() -> InsightResult:
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
        """,
        limit=5,
    )

    high_risk_categories = fetch_all(
        """
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
        """,
        limit=5,
    )

    total_alerts = _safe_int(alert_summary.get("total_alerts"))
    high_alerts = _safe_int(alert_summary.get("high_alerts"))
    medium_alerts = _safe_int(alert_summary.get("medium_alerts"))

    key_findings = [
        f"The anomaly detection layer generated {total_alerts:,.0f} operational alerts.",
        f"There are {high_alerts:,.0f} high severity alerts and {medium_alerts:,.0f} medium severity alerts.",
    ]

    if alerts_by_type:
        top_alert = alerts_by_type[0]
        key_findings.append(
            "The most common alert type is "
            f"{top_alert.get('alert_type')} with {top_alert.get('alert_count')} alerts."
        )

    if high_risk_sellers:
        seller = high_risk_sellers[0]
        key_findings.append(
            "A high-risk seller example is "
            f"{seller.get('seller_id')} with late delivery rate "
            f"{_safe_number(seller.get('late_delivery_rate')):.2f}% and average review score "
            f"{_safe_number(seller.get('avg_review_score')):.2f}."
        )

    if high_risk_categories:
        category = high_risk_categories[0]
        key_findings.append(
            "A high-risk category example is "
            f"{category.get('product_category_name_english')} with risk level "
            f"{category.get('category_risk_level')}."
        )

    recommended_actions = [
        "Prioritise high severity operational alerts before medium severity alerts.",
        "Review sellers with high late delivery rates and low review scores.",
        "Investigate product categories with weak review performance or delivery risk.",
        "Use alert type trends to decide whether issues are related to delivery, seller performance, revenue, freight, or customer satisfaction.",
    ]

    return InsightResult(
        title="Operational Risk Summary",
        summary=(
            "The operational layer highlights anomaly alerts, seller risk, category risk, "
            "and business areas requiring attention."
        ),
        key_findings=key_findings,
        recommended_actions=recommended_actions,
        source_views=[
            "vw_operational_alert_summary",
            "vw_operational_alerts_by_type",
            "vw_high_risk_sellers",
            "vw_high_risk_categories",
        ],
    )


def generate_recommendations() -> InsightResult:
    executive = generate_executive_summary()
    sales = generate_sales_performance_summary()
    risk = generate_operational_risk_summary()

    recommended_actions = [
        "Use the executive dashboard to monitor revenue, order volume, customers, sellers, and review performance.",
        "Use operational anomaly alerts as an early warning layer for delivery, seller, freight, review, and revenue issues.",
        "Create a weekly review process focused on high-risk sellers and high-risk product categories.",
        "Expose the insights layer through FastAPI so dashboards, apps, and future AI tools can reuse the same trusted outputs.",
        "In the Azure version, store API keys in Azure Key Vault and orchestrate the pipeline with Azure Data Factory.",
    ]

    return InsightResult(
        title="AI-Ready Business Recommendations",
        summary=(
            "The project is ready to support AI-assisted business decision-making because "
            "the insights are generated from trusted dbt models, KPI views, and operational risk views."
        ),
        key_findings=executive.key_findings[:2] + sales.key_findings[:1] + risk.key_findings[:2],
        recommended_actions=recommended_actions,
        source_views=sorted(
            set(executive.source_views + sales.source_views + risk.source_views)
        ),
    )


def insight_to_dict(insight: InsightResult) -> dict:
    return {
        "title": insight.title,
        "summary": insight.summary,
        "key_findings": insight.key_findings,
        "recommended_actions": insight.recommended_actions,
        "source_views": insight.source_views,
    }