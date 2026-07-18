from pathlib import Path
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


EXPECTED_OPERATIONAL_TABLES = [
    "ops_daily_metrics",
    "ops_seller_metrics",
    "ops_category_metrics",
]


def main() -> None:
    engine = get_engine()

    verification_results = []

    for table_name in EXPECTED_OPERATIONAL_TABLES:
        with engine.begin() as connection:
            exists_query = text(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = :table_name
                """
            )

            exists_result = pd.read_sql(
                exists_query,
                connection,
                params={"table_name": table_name},
            )

            exists = not exists_result.empty
            row_count = None

            if exists:
                row_count_query = text(f"SELECT COUNT(*) AS row_count FROM {table_name}")
                row_count = int(
                    pd.read_sql(row_count_query, connection)["row_count"].iloc[0]
                )

            verification_results.append(
                {
                    "table_name": table_name,
                    "exists": exists,
                    "row_count": row_count,
                }
            )

    verification_df = pd.DataFrame(verification_results)

    print(verification_df)

    output_path = Path("data/processed/operational_metrics_verification_report.csv")
    verification_df.to_csv(output_path, index=False)

    print(f"\nVerification report saved to: {output_path}")


if __name__ == "__main__":
    main()