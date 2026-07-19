from pathlib import Path
import sqlite3
import sys
from datetime import datetime

import pandas as pd
from sqlalchemy import text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cloud.azure_sql_database import get_azure_sql_engine  # noqa: E402


SQLITE_DB_PATH = PROJECT_ROOT / "retail_intelligence.db"

OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "azure_sql_migration_report.csv"
)


CURATED_OBJECTS = [
    "dim_date",
    "dim_customer",
    "dim_product",
    "dim_seller",
    "fact_sales",
    "fact_delivery",
    "fact_payments",
    "fact_reviews",
    "ops_daily_metrics",
    "ops_seller_metrics",
    "ops_category_metrics",
    "ops_anomaly_rules",
    "ops_anomaly_alerts",
    "ops_event_log",
    "ops_event_records",
]


def clean_dataframe_for_sql_server(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataframe values before loading into Azure SQL.
    """
    cleaned_df = df.copy()

    for column in cleaned_df.columns:
        if cleaned_df[column].dtype == "object":
            cleaned_df[column] = cleaned_df[column].astype(str)
            cleaned_df[column] = cleaned_df[column].replace({"nan": None, "NaT": None})

    cleaned_df = cleaned_df.where(pd.notnull(cleaned_df), None)

    return cleaned_df


def sqlite_object_exists(connection: sqlite3.Connection, object_name: str) -> bool:
    query = """
        SELECT name
        FROM sqlite_master
        WHERE name = ?
          AND type IN ('table', 'view')
    """

    result = connection.execute(query, (object_name,)).fetchone()

    return result is not None


def load_sqlite_object_to_dataframe(
    connection: sqlite3.Connection,
    object_name: str,
) -> pd.DataFrame:
    query = f'SELECT * FROM "{object_name}"'
    return pd.read_sql_query(query, connection)


def main() -> None:
    if not SQLITE_DB_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found: {SQLITE_DB_PATH}")

    sqlite_connection = sqlite3.connect(SQLITE_DB_PATH)
    azure_engine = get_azure_sql_engine()

    migration_results = []

    print("Azure SQL curated data migration started.")

    for object_name in CURATED_OBJECTS:
        started_at = datetime.utcnow()

        try:
            if not sqlite_object_exists(sqlite_connection, object_name):
                migration_results.append(
                    {
                        "object_name": object_name,
                        "status": "skipped",
                        "row_count": 0,
                        "started_at": started_at,
                        "finished_at": datetime.utcnow(),
                        "error": "Object not found in SQLite",
                    }
                )
                continue

            print(f"Loading {object_name}...")

            df = load_sqlite_object_to_dataframe(sqlite_connection, object_name)
            df = clean_dataframe_for_sql_server(df)

            df.to_sql(
                name=object_name,
                con=azure_engine,
                schema="dbo",
                if_exists="replace",
                index=False,
                chunksize=1000,
                method=None,
            )

            with azure_engine.connect() as connection:
                row_count = connection.execute(
                    text(f"SELECT COUNT(*) FROM dbo.{object_name}")
                ).scalar()

            migration_results.append(
                {
                    "object_name": object_name,
                    "status": "success",
                    "row_count": row_count,
                    "started_at": started_at,
                    "finished_at": datetime.utcnow(),
                    "error": None,
                }
            )

            print(f"Loaded {object_name}: {row_count} rows")

        except Exception as exc:
            migration_results.append(
                {
                    "object_name": object_name,
                    "status": "failed",
                    "row_count": 0,
                    "started_at": started_at,
                    "finished_at": datetime.utcnow(),
                    "error": str(exc),
                }
            )

            print(f"Failed loading {object_name}: {exc}")

    sqlite_connection.close()

    results_df = pd.DataFrame(migration_results)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(f"\nMigration report saved to: {OUTPUT_REPORT}")

    failed_rows = results_df[results_df["status"] == "failed"]

    if failed_rows.empty:
        print("\nAzure SQL curated data migration completed.")
    else:
        print("\nSome objects failed to migrate:")
        print(failed_rows[["object_name", "error"]])
        raise RuntimeError("Azure SQL migration completed with failures.")


if __name__ == "__main__":
    main()