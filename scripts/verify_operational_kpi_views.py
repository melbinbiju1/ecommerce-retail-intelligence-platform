from pathlib import Path
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


EXPECTED_VIEWS = [
    "vw_operational_alert_summary",
    "vw_operational_alerts_by_type",
    "vw_operational_alerts_by_severity",
    "vw_recent_operational_alerts",
    "vw_high_risk_sellers",
    "vw_high_risk_categories",
    "vw_operational_event_summary",
    "vw_operational_event_records",
    "vw_operational_risk_summary",
]


def main() -> None:
    engine = get_engine()

    verification_results = []

    for view_name in EXPECTED_VIEWS:
        with engine.begin() as connection:
            exists_query = text(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'view'
                  AND name = :view_name
                """
            )

            exists_result = pd.read_sql(
                exists_query,
                connection,
                params={"view_name": view_name},
            )

            exists = not exists_result.empty
            row_count = None

            if exists:
                row_count_query = text(f"SELECT COUNT(*) AS row_count FROM {view_name}")
                row_count = int(
                    pd.read_sql(row_count_query, connection)["row_count"].iloc[0]
                )

            verification_results.append(
                {
                    "view_name": view_name,
                    "exists": exists,
                    "row_count": row_count,
                }
            )

    verification_df = pd.DataFrame(verification_results)
    print(verification_df)

    output_path = Path("data/processed/operational_kpi_views_verification_report.csv")
    verification_df.to_csv(output_path, index=False)

    print(f"\nVerification report saved to: {output_path}")


if __name__ == "__main__":
    main()