from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


OUTPUT_DIR = Path("data/inventory_events/incoming")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    engine = get_engine()

    query = """
    SELECT
        product_id,
        seller_id,
        reorder_level,
        safety_stock,
        avg_daily_demand
    FROM sim_inventory_policy
    ORDER BY RANDOM()
    LIMIT 100
    """

    policy_df = pd.read_sql(query, engine)

    if policy_df.empty:
        raise ValueError("No rows found in sim_inventory_policy. Please complete Phase 8 first.")

    event_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    movement_types = [
        "RESTOCK",
        "ADJUSTMENT",
        "DAMAGED",
        "RETURN",
        "TRANSFER_IN",
        "TRANSFER_OUT",
    ]

    event_rows = []

    for index, row in policy_df.iterrows():
        movement_type = np.random.choice(
            movement_types,
            p=[0.45, 0.15, 0.10, 0.15, 0.10, 0.05],
        )

        if movement_type in ["RESTOCK", "RETURN", "TRANSFER_IN"]:
            quantity_change = int(np.random.randint(1, 50))
        else:
            quantity_change = int(-np.random.randint(1, 20))

        event_rows.append(
            {
                "event_id": f"INV-{event_timestamp}-{index + 1}",
                "event_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product_id": row["product_id"],
                "seller_id": row["seller_id"],
                "movement_type": movement_type,
                "quantity_change": quantity_change,
                "reason": f"Simulated {movement_type.lower()} inventory event",
                "source_system": "local_inventory_event_simulator",
            }
        )

    event_df = pd.DataFrame(event_rows)

    output_file = OUTPUT_DIR / f"inventory_events_{event_timestamp}.csv"
    event_df.to_csv(output_file, index=False)

    print(f"Inventory event file created: {output_file}")
    print(f"Rows created: {len(event_df)}")


if __name__ == "__main__":
    main()