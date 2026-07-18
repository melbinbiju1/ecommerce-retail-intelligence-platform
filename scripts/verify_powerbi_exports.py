from pathlib import Path
import pandas as pd


EXPORT_DIR = Path("data/powerbi_exports")

EXPECTED_EXPORTS = [
    "dim_date",
    "dim_customer",
    "dim_product",
    "dim_seller",
    "fact_sales",
    "fact_delivery",
    "fact_payments",
    "fact_reviews",

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

    "ops_daily_metrics",
    "ops_seller_metrics",
    "ops_category_metrics",

    "vw_operational_alert_summary",
    "vw_operational_alerts_by_type",
    "vw_operational_alerts_by_severity",
    "vw_recent_operational_alerts",
    "vw_high_risk_sellers",
    "vw_high_risk_categories",
    "vw_operational_risk_summary",
    "vw_operational_event_summary",
]


def main() -> None:
    print("Verifying Power BI export files...\n")

    results = []

    for export_name in EXPECTED_EXPORTS:
        file_path = EXPORT_DIR / f"{export_name}.csv"

        exists = file_path.exists()
        row_count = None
        column_count = None
        file_size_kb = None

        if exists:
            df = pd.read_csv(file_path)
            row_count = len(df)
            column_count = len(df.columns)
            file_size_kb = round(file_path.stat().st_size / 1024, 2)

        results.append(
            {
                "export_name": export_name,
                "exists": exists,
                "row_count": row_count,
                "column_count": column_count,
                "file_size_kb": file_size_kb,
            }
        )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = EXPORT_DIR / "powerbi_export_verification_report.csv"
    results_df.to_csv(output_path, index=False)

    missing_exports = results_df[results_df["exists"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if missing_exports.empty:
        print("\nAll expected Power BI exports exist.")
    else:
        print("\nMissing exports:")
        print(missing_exports[["export_name"]])
        raise RuntimeError("Some expected Power BI export files are missing.")


if __name__ == "__main__":
    main()