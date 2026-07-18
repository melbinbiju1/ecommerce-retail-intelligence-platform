from pathlib import Path
from datetime import datetime
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


OUTPUT_DIR = Path("data/powerbi_exports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


OBJECTS_TO_EXPORT = [
    # Core Power BI star schema model built by dbt
    "dim_date",
    "dim_customer",
    "dim_product",
    "dim_seller",
    "fact_sales",
    "fact_delivery",
    "fact_payments",
    "fact_reviews",

    # Business KPI views built by dbt
    "vw_executive_summary",
    "vw_monthly_sales",
    "vw_product_performance",
    "vw_seller_performance",
    "vw_customer_state_performance",
    "vw_delivery_performance",
    "vw_payment_analysis",
    "vw_review_analysis",
    "vw_late_delivery_by_state",
    "vw_category_review_performance",

    # Operational metrics built by dbt
    "ops_daily_metrics",
    "ops_seller_metrics",
    "ops_category_metrics",

    # Operational anomaly and risk views built by dbt
    "vw_operational_alert_summary",
    "vw_operational_alerts_by_type",
    "vw_operational_alerts_by_severity",
    "vw_recent_operational_alerts",
    "vw_high_risk_sellers",
    "vw_high_risk_categories",
    "vw_operational_risk_summary",

    # Event pipeline summary only
    "vw_operational_event_summary",
]


def write_log(message: str) -> None:
    log_file = LOG_DIR / "powerbi_export.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def export_object(object_name: str, engine) -> dict:
    try:
        query = f"SELECT * FROM {object_name}"
        df = pd.read_sql(query, engine)

        output_path = OUTPUT_DIR / f"{object_name}.csv"
        df.to_csv(output_path, index=False)

        print(f"SUCCESS | {object_name} | rows={len(df)}")

        return {
            "object_name": object_name,
            "status": "SUCCESS",
            "row_count": len(df),
            "column_count": len(df.columns),
            "output_file": str(output_path),
            "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error_message": "",
        }

    except Exception as error:
        print(f"FAILED | {object_name} | {error}")

        return {
            "object_name": object_name,
            "status": "FAILED",
            "row_count": 0,
            "column_count": 0,
            "output_file": "",
            "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error_message": str(error),
        }


def main() -> None:
    print("Exporting dbt-built Power BI tables and views...")

    engine = get_engine()
    export_results = []

    for object_name in OBJECTS_TO_EXPORT:
        export_results.append(export_object(object_name, engine))

    summary_df = pd.DataFrame(export_results)
    summary_path = OUTPUT_DIR / "powerbi_export_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    successful_exports = int((summary_df["status"] == "SUCCESS").sum())
    failed_exports = int((summary_df["status"] == "FAILED").sum())

    write_log(
        f"Power BI export completed | successful={successful_exports} | failed={failed_exports}"
    )

    print(f"\nExport summary saved to: {summary_path}")
    print(f"Successful exports: {successful_exports}")
    print(f"Failed exports: {failed_exports}")

    if failed_exports > 0:
        print("\nSome exports failed. Check data/powerbi_exports/powerbi_export_summary.csv")
        raise RuntimeError("Power BI export completed with failures.")

    print("\nPower BI export completed successfully.")


if __name__ == "__main__":
    main()