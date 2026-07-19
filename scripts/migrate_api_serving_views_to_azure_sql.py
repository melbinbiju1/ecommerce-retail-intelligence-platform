from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.db_utils import get_engine as get_sqlite_engine  # noqa: E402
from src.cloud.azure_sql_database import get_azure_sql_engine  # noqa: E402


OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "azure_sql_api_serving_views_migration_report.csv"
)

API_SERVING_OBJECTS = [
    "vw_executive_summary",
    "vw_monthly_sales",
    "vw_product_performance",
    "vw_seller_performance",
    "vw_customer_state_performance",
    "vw_operational_alert_summary",
    "vw_operational_alerts_by_type",
    "vw_operational_alerts_by_severity",
    "vw_recent_operational_alerts",
    "vw_high_risk_sellers",
    "vw_high_risk_categories",
    "vw_operational_risk_summary",
]


def clean_dataframe_for_sql_server(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = df.copy()

    for column in cleaned_df.columns:
        if cleaned_df[column].dtype == "object":
            cleaned_df[column] = cleaned_df[column].astype(str)
            cleaned_df[column] = cleaned_df[column].replace(
                {
                    "nan": None,
                    "NaN": None,
                    "None": None,
                    "NaT": None,
                }
            )

    cleaned_df = cleaned_df.where(pd.notnull(cleaned_df), None)

    return cleaned_df


def main() -> None:
    sqlite_engine = get_sqlite_engine()
    azure_engine = get_azure_sql_engine()

    migration_results = []

    for object_name in API_SERVING_OBJECTS:
        print(f"\nMigrating API serving object: {object_name}")

        try:
            query = f"SELECT * FROM {object_name}"

            source_df = pd.read_sql(query, sqlite_engine)
            source_df = clean_dataframe_for_sql_server(source_df)

            source_df.to_sql(
                name=object_name,
                con=azure_engine,
                schema="dbo",
                if_exists="replace",
                index=False,
                chunksize=1000,
            )

            migration_results.append(
                {
                    "object_name": object_name,
                    "source_type": "sqlite_view",
                    "target_type": "azure_sql_api_serving_table",
                    "row_count": len(source_df),
                    "status": "success",
                    "error_message": None,
                }
            )

            print(f"Successfully migrated {object_name}: {len(source_df)} rows")

        except Exception as error:
            migration_results.append(
                {
                    "object_name": object_name,
                    "source_type": "sqlite_view",
                    "target_type": "azure_sql_api_serving_table",
                    "row_count": None,
                    "status": "failed",
                    "error_message": str(error),
                }
            )

            print(f"Failed to migrate {object_name}: {error}")

    results_df = pd.DataFrame(migration_results)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print("\nAPI serving views migration report:")
    print(results_df)

    print(f"\nReport saved to: {OUTPUT_REPORT}")

    failed = results_df[results_df["status"] == "failed"]

    if failed.empty:
        print("\nAzure SQL API serving views migration completed successfully.")
    else:
        raise RuntimeError("One or more API serving objects failed to migrate.")


if __name__ == "__main__":
    main()