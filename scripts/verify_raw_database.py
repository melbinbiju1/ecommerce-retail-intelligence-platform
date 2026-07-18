from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


EXPECTED_RAW_TABLES = [
    "raw_customers",
    "raw_geolocation",
    "raw_order_items",
    "raw_order_payments",
    "raw_order_reviews",
    "raw_orders",
    "raw_products",
    "raw_sellers",
    "raw_product_category_translation",
    "raw_load_audit",
]


def main() -> None:
    engine = get_engine()

    print("Verifying raw database tables...\n")

    query = text(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """
    )

    with engine.begin() as connection:
        existing_tables = pd.read_sql(query, connection)["name"].tolist()

    verification_results = []

    for table_name in EXPECTED_RAW_TABLES:
        exists = table_name in existing_tables

        row_count = None

        if exists:
            with engine.begin() as connection:
                row_count_query = text(f"SELECT COUNT(*) AS row_count FROM {table_name}")
                row_count = pd.read_sql(row_count_query, connection)["row_count"].iloc[0]

        verification_results.append(
            {
                "table_name": table_name,
                "exists": exists,
                "row_count": row_count,
            }
        )

    verification_df = pd.DataFrame(verification_results)

    print(verification_df)

    output_path = "data/processed/raw_database_verification_report.csv"
    verification_df.to_csv(output_path, index=False)

    print(f"\nVerification report saved to: {output_path}")


if __name__ == "__main__":
    main()