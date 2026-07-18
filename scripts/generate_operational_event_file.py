from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


OUTPUT_DIR = Path("data/operational_events/incoming")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


EVENT_TYPES = [
    "LATE_DELIVERY",
    "PAYMENT_FAILURE",
    "LOW_REVIEW",
    "ORDER_CANCELLED",
    "HIGH_FREIGHT_COST",
    "SELLER_DELAY_RISK",
    "REVENUE_DROP",
    "CATEGORY_DEMAND_DROP",
]


def main() -> None:
    engine = get_engine()

    anomaly_query = """
    SELECT
        alert_type,
        severity,
        business_area,
        entity_id,
        entity_name,
        metric_name,
        actual_value,
        expected_value,
        alert_description,
        recommended_action
    FROM ops_anomaly_alerts
    ORDER BY RANDOM()
    LIMIT 100
    """

    anomaly_df = pd.read_sql(anomaly_query, engine)

    if anomaly_df.empty:
        raise ValueError(
            "No rows found in ops_anomaly_alerts. Please complete Phase 9 first."
        )

    event_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    event_rows = []

    for index, row in anomaly_df.iterrows():
        event_type = np.random.choice(EVENT_TYPES)

        event_rows.append(
            {
                "event_id": f"OPS-{event_timestamp}-{index + 1}",
                "event_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "event_type": event_type,
                "severity": row["severity"],
                "business_area": row["business_area"],
                "entity_id": row["entity_id"],
                "entity_name": row["entity_name"],
                "metric_name": row["metric_name"],
                "actual_value": row["actual_value"],
                "expected_value": row["expected_value"],
                "event_description": row["alert_description"],
                "recommended_action": row["recommended_action"],
                "source_system": "local_operational_event_simulator",
            }
        )

    event_df = pd.DataFrame(event_rows)

    output_file = OUTPUT_DIR / f"operational_events_{event_timestamp}.csv"
    event_df.to_csv(output_file, index=False)

    print(f"Operational event file created: {output_file}")
    print(f"Rows created: {len(event_df)}")


if __name__ == "__main__":
    main()