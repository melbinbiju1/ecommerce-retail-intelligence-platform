from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


LOG_DIR = Path("logs")
REPORT_DIR = Path("data/processed")

LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def write_log(message: str) -> None:
    log_file = LOG_DIR / "operational_anomaly_detection.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def create_anomaly_tables(engine) -> None:
    create_rules_sql = """
    CREATE TABLE IF NOT EXISTS ops_anomaly_rules (
        rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_name TEXT NOT NULL,
        business_area TEXT NOT NULL,
        metric_name TEXT NOT NULL,
        rule_description TEXT NOT NULL,
        severity TEXT NOT NULL,
        is_active INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );
    """

    create_alerts_sql = """
    CREATE TABLE IF NOT EXISTS ops_anomaly_alerts (
        alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_date TEXT,
        alert_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        business_area TEXT NOT NULL,
        entity_id TEXT,
        entity_name TEXT,
        metric_name TEXT NOT NULL,
        actual_value REAL,
        expected_value REAL,
        difference_value REAL,
        difference_percentage REAL,
        alert_description TEXT NOT NULL,
        recommended_action TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """

    with engine.begin() as connection:
        connection.execute(text(create_rules_sql))
        connection.execute(text(create_alerts_sql))


def refresh_anomaly_rules(engine) -> None:
    rules = [
        {
            "rule_name": "revenue_drop",
            "business_area": "sales",
            "metric_name": "total_revenue",
            "rule_description": "Daily revenue is more than 30% below the rolling 30-day average.",
            "severity": "high",
        },
        {
            "rule_name": "order_volume_spike",
            "business_area": "sales",
            "metric_name": "total_orders",
            "rule_description": "Daily order volume is more than 50% above the rolling 30-day average.",
            "severity": "medium",
        },
        {
            "rule_name": "delivery_delay_spike",
            "business_area": "delivery",
            "metric_name": "late_delivery_rate",
            "rule_description": "Late delivery rate is above 25%.",
            "severity": "high",
        },
        {
            "rule_name": "cancellation_spike",
            "business_area": "orders",
            "metric_name": "cancelled_order_rate",
            "rule_description": "Cancelled order rate is above 5%.",
            "severity": "medium",
        },
        {
            "rule_name": "low_review_spike",
            "business_area": "customer_satisfaction",
            "metric_name": "low_review_rate",
            "rule_description": "Low review rate is above 30%.",
            "severity": "high",
        },
        {
            "rule_name": "freight_cost_spike",
            "business_area": "logistics",
            "metric_name": "freight_revenue",
            "rule_description": "Daily freight value is more than 50% above the rolling 30-day average.",
            "severity": "medium",
        },
        {
            "rule_name": "seller_performance_risk",
            "business_area": "seller_operations",
            "metric_name": "seller_risk_level",
            "rule_description": "Seller has high operational risk based on delivery delay rate or low review score.",
            "severity": "high",
        },
        {
            "rule_name": "category_performance_risk",
            "business_area": "product_category",
            "metric_name": "category_risk_level",
            "rule_description": "Product category has high operational risk based on delivery delay rate or low review score.",
            "severity": "medium",
        },
    ]

    with engine.begin() as connection:
        connection.execute(text("DELETE FROM ops_anomaly_rules"))

        for rule in rules:
            connection.execute(
                text(
                    """
                    INSERT INTO ops_anomaly_rules (
                        rule_name,
                        business_area,
                        metric_name,
                        rule_description,
                        severity,
                        is_active,
                        created_at
                    )
                    VALUES (
                        :rule_name,
                        :business_area,
                        :metric_name,
                        :rule_description,
                        :severity,
                        1,
                        :created_at
                    )
                    """
                ),
                {
                    **rule,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )


def calculate_daily_anomalies(engine) -> pd.DataFrame:
    daily_df = pd.read_sql(
        """
        SELECT *
        FROM ops_daily_metrics
        ORDER BY metric_date
        """,
        engine,
    )

    daily_df["metric_date"] = pd.to_datetime(daily_df["metric_date"])

    numeric_columns = [
        "total_revenue",
        "total_orders",
        "freight_revenue",
    ]

    for column in numeric_columns:
        daily_df[f"{column}_rolling_30_avg"] = (
            daily_df[column].rolling(window=30, min_periods=7).mean()
        )

    alerts = []

    for _, row in daily_df.iterrows():
        alert_date = row["metric_date"].strftime("%Y-%m-%d")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Revenue drop
        expected_revenue = row["total_revenue_rolling_30_avg"]
        if pd.notna(expected_revenue) and expected_revenue > 0:
            difference = row["total_revenue"] - expected_revenue
            difference_pct = (difference / expected_revenue) * 100

            if difference_pct <= -30:
                alerts.append(
                    {
                        "alert_date": alert_date,
                        "alert_type": "REVENUE_DROP",
                        "severity": "high",
                        "business_area": "sales",
                        "entity_id": None,
                        "entity_name": None,
                        "metric_name": "total_revenue",
                        "actual_value": round(row["total_revenue"], 2),
                        "expected_value": round(expected_revenue, 2),
                        "difference_value": round(difference, 2),
                        "difference_percentage": round(difference_pct, 2),
                        "alert_description": "Daily revenue is significantly below the recent 30-day average.",
                        "recommended_action": "Review product categories, seller activity, cancellations, and delivery issues for this date.",
                        "created_at": created_at,
                    }
                )

        # Order volume spike
        expected_orders = row["total_orders_rolling_30_avg"]
        if pd.notna(expected_orders) and expected_orders > 0:
            difference = row["total_orders"] - expected_orders
            difference_pct = (difference / expected_orders) * 100

            if difference_pct >= 50:
                alerts.append(
                    {
                        "alert_date": alert_date,
                        "alert_type": "ORDER_VOLUME_SPIKE",
                        "severity": "medium",
                        "business_area": "sales",
                        "entity_id": None,
                        "entity_name": None,
                        "metric_name": "total_orders",
                        "actual_value": round(row["total_orders"], 2),
                        "expected_value": round(expected_orders, 2),
                        "difference_value": round(difference, 2),
                        "difference_percentage": round(difference_pct, 2),
                        "alert_description": "Daily order volume is unusually high compared with the recent 30-day average.",
                        "recommended_action": "Check campaigns, promotions, seasonal demand, and operational capacity.",
                        "created_at": created_at,
                    }
                )

        # Freight cost spike
        expected_freight = row["freight_revenue_rolling_30_avg"]
        if pd.notna(expected_freight) and expected_freight > 0:
            difference = row["freight_revenue"] - expected_freight
            difference_pct = (difference / expected_freight) * 100

            if difference_pct >= 50:
                alerts.append(
                    {
                        "alert_date": alert_date,
                        "alert_type": "FREIGHT_COST_SPIKE",
                        "severity": "medium",
                        "business_area": "logistics",
                        "entity_id": None,
                        "entity_name": None,
                        "metric_name": "freight_revenue",
                        "actual_value": round(row["freight_revenue"], 2),
                        "expected_value": round(expected_freight, 2),
                        "difference_value": round(difference, 2),
                        "difference_percentage": round(difference_pct, 2),
                        "alert_description": "Daily freight value is unusually high compared with the recent 30-day average.",
                        "recommended_action": "Review affected product categories, delivery distances, seller regions, and freight pricing.",
                        "created_at": created_at,
                    }
                )

        # Delivery delay spike
        if row["late_delivery_rate"] >= 25:
            alerts.append(
                {
                    "alert_date": alert_date,
                    "alert_type": "DELIVERY_DELAY_SPIKE",
                    "severity": "high",
                    "business_area": "delivery",
                    "entity_id": None,
                    "entity_name": None,
                    "metric_name": "late_delivery_rate",
                    "actual_value": round(row["late_delivery_rate"], 2),
                    "expected_value": 25,
                    "difference_value": round(row["late_delivery_rate"] - 25, 2),
                    "difference_percentage": None,
                    "alert_description": "Late delivery rate is above the operational threshold.",
                    "recommended_action": "Investigate logistics delays, seller dispatch performance, and affected customer regions.",
                    "created_at": created_at,
                }
            )

        # Cancellation spike
        if row["cancelled_order_rate"] >= 5:
            alerts.append(
                {
                    "alert_date": alert_date,
                    "alert_type": "CANCELLATION_SPIKE",
                    "severity": "medium",
                    "business_area": "orders",
                    "entity_id": None,
                    "entity_name": None,
                    "metric_name": "cancelled_order_rate",
                    "actual_value": round(row["cancelled_order_rate"], 2),
                    "expected_value": 5,
                    "difference_value": round(row["cancelled_order_rate"] - 5, 2),
                    "difference_percentage": None,
                    "alert_description": "Cancellation rate is above the operational threshold.",
                    "recommended_action": "Review order fulfilment issues, seller availability, payment issues, and customer cancellation reasons.",
                    "created_at": created_at,
                }
            )

        # Low review spike
        if row["low_review_rate"] >= 30:
            alerts.append(
                {
                    "alert_date": alert_date,
                    "alert_type": "LOW_REVIEW_SPIKE",
                    "severity": "high",
                    "business_area": "customer_satisfaction",
                    "entity_id": None,
                    "entity_name": None,
                    "metric_name": "low_review_rate",
                    "actual_value": round(row["low_review_rate"], 2),
                    "expected_value": 30,
                    "difference_value": round(row["low_review_rate"] - 30, 2),
                    "difference_percentage": None,
                    "alert_description": "Low review rate is above the operational threshold.",
                    "recommended_action": "Review delivery delays, product categories, seller issues, and customer comments for this date.",
                    "created_at": created_at,
                }
            )

    return pd.DataFrame(alerts)


def calculate_seller_anomalies(engine) -> pd.DataFrame:
    seller_df = pd.read_sql(
        """
        SELECT *
        FROM ops_seller_metrics
        WHERE seller_risk_level = 'high'
        """,
        engine,
    )

    alerts = []

    for _, row in seller_df.iterrows():
        alerts.append(
            {
                "alert_date": None,
                "alert_type": "SELLER_PERFORMANCE_RISK",
                "severity": "high",
                "business_area": "seller_operations",
                "entity_id": row["seller_id"],
                "entity_name": f"{row['seller_city']}, {row['seller_state']}",
                "metric_name": "seller_risk_level",
                "actual_value": row["late_delivery_rate"],
                "expected_value": 15,
                "difference_value": None,
                "difference_percentage": None,
                "alert_description": "Seller shows high operational risk based on delivery delays or low review scores.",
                "recommended_action": "Review seller SLA performance, delivery process, customer reviews, and fulfilment reliability.",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return pd.DataFrame(alerts)


def calculate_category_anomalies(engine) -> pd.DataFrame:
    category_df = pd.read_sql(
        """
        SELECT *
        FROM ops_category_metrics
        WHERE category_risk_level = 'high'
        """,
        engine,
    )

    alerts = []

    for _, row in category_df.iterrows():
        alerts.append(
            {
                "alert_date": None,
                "alert_type": "CATEGORY_PERFORMANCE_RISK",
                "severity": "medium",
                "business_area": "product_category",
                "entity_id": row["product_category_name_english"],
                "entity_name": row["product_category_name_english"],
                "metric_name": "category_risk_level",
                "actual_value": row["late_delivery_rate"],
                "expected_value": 15,
                "difference_value": None,
                "difference_percentage": None,
                "alert_description": "Product category shows operational risk based on delivery delays or review scores.",
                "recommended_action": "Review product quality, seller performance, delivery patterns, and customer review feedback for this category.",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return pd.DataFrame(alerts)


def save_alerts(engine, alerts_df: pd.DataFrame) -> None:
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM ops_anomaly_alerts"))

    if not alerts_df.empty:
        alerts_df.to_sql("ops_anomaly_alerts", engine, if_exists="append", index=False)


def create_report(alerts_df: pd.DataFrame) -> None:
    if alerts_df.empty:
        report_df = pd.DataFrame(
            [
                {
                    "total_alerts": 0,
                    "high_alerts": 0,
                    "medium_alerts": 0,
                    "critical_alerts": 0,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            ]
        )
    else:
        report_df = pd.DataFrame(
            [
                {
                    "total_alerts": len(alerts_df),
                    "high_alerts": int((alerts_df["severity"] == "high").sum()),
                    "medium_alerts": int((alerts_df["severity"] == "medium").sum()),
                    "critical_alerts": int((alerts_df["severity"] == "critical").sum()),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            ]
        )

    report_path = REPORT_DIR / "operational_anomaly_detection_report.csv"
    report_df.to_csv(report_path, index=False)


def main() -> None:
    print("Starting operational anomaly detection...")

    engine = get_engine()

    try:
        create_anomaly_tables(engine)
        refresh_anomaly_rules(engine)

        daily_alerts_df = calculate_daily_anomalies(engine)
        seller_alerts_df = calculate_seller_anomalies(engine)
        category_alerts_df = calculate_category_anomalies(engine)

        alerts_df = pd.concat(
            [daily_alerts_df, seller_alerts_df, category_alerts_df],
            ignore_index=True,
        )

        save_alerts(engine, alerts_df)
        create_report(alerts_df)

        write_log(
            f"SUCCESS | Operational anomaly detection completed | alerts={len(alerts_df)}"
        )

        print("Operational anomaly detection completed successfully.")
        print(f"Total alerts created: {len(alerts_df)}")
        print("Tables created/updated:")
        print("- ops_anomaly_rules")
        print("- ops_anomaly_alerts")
        print("Report created: data/processed/operational_anomaly_detection_report.csv")

    except Exception as error:
        write_log(f"FAILED | Operational anomaly detection failed | {error}")
        print(f"Operational anomaly detection failed: {error}")
        raise


if __name__ == "__main__":
    main()