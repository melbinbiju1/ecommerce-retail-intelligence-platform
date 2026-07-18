from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


def main() -> None:
    engine = get_engine()

    print("\n" + "=" * 100)
    print("Sample anomaly alerts")
    print("=" * 100)

    alerts_df = pd.read_sql(
        """
        SELECT
            alert_id,
            alert_date,
            alert_type,
            severity,
            business_area,
            entity_id,
            entity_name,
            metric_name,
            actual_value,
            expected_value,
            difference_percentage,
            alert_description,
            recommended_action
        FROM ops_anomaly_alerts
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                ELSE 4
            END,
            alert_id
        LIMIT 25
        """,
        engine,
    )

    print(alerts_df)

    print("\n" + "=" * 100)
    print("Anomaly rules")
    print("=" * 100)

    rules_df = pd.read_sql(
        """
        SELECT
            rule_name,
            business_area,
            metric_name,
            severity,
            rule_description,
            is_active
        FROM ops_anomaly_rules
        ORDER BY rule_id
        """,
        engine,
    )

    print(rules_df)


if __name__ == "__main__":
    main()