from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


VIEWS_TO_SAMPLE = [
    "vw_operational_alert_summary",
    "vw_operational_alerts_by_type",
    "vw_operational_alerts_by_severity",
    "vw_high_risk_sellers",
    "vw_high_risk_categories",
    "vw_operational_event_summary",
    "vw_operational_risk_summary",
]


def main() -> None:
    engine = get_engine()

    for view_name in VIEWS_TO_SAMPLE:
        print("\n" + "=" * 100)
        print(f"Sample from {view_name}")
        print("=" * 100)

        query = f"SELECT * FROM {view_name} LIMIT 10"
        df = pd.read_sql(query, engine)
        print(df)


if __name__ == "__main__":
    main()