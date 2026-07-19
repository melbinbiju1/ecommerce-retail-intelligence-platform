from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cloud.azure_sql_database import get_azure_sql_engine  # noqa: E402


OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "adf_pipeline_output_verification_report.csv"
)


def main() -> None:
    engine = get_azure_sql_engine()

    query = text(
        """
        SELECT
            COUNT(*) AS row_count,
            COUNT(DISTINCT order_id) AS unique_orders,
            MIN(order_purchase_timestamp) AS min_order_purchase_timestamp,
            MAX(order_purchase_timestamp) AS max_order_purchase_timestamp
        FROM dbo.adf_stg_orders_raw
        """
    )

    with engine.connect() as connection:
        row = connection.execute(query).mappings().fetchone()

    result = {
        "table_name": "dbo.adf_stg_orders_raw",
        "row_count": row["row_count"],
        "unique_orders": row["unique_orders"],
        "min_order_purchase_timestamp": row["min_order_purchase_timestamp"],
        "max_order_purchase_timestamp": row["max_order_purchase_timestamp"],
        "passed": row["row_count"] > 0,
    }

    results_df = pd.DataFrame([result])

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(results_df)
    print(f"\nVerification report saved to: {OUTPUT_REPORT}")

    if result["passed"]:
        print("\nADF pipeline output verification passed.")
    else:
        raise RuntimeError("ADF pipeline output verification failed.")


if __name__ == "__main__":
    main()