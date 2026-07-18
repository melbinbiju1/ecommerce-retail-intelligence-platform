from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


REPORT_DIR = Path("data/processed")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


QUALITY_CHECKS = [
    {
        "check_name": "orders_order_id_not_null",
        "table_name": "raw_orders",
        "sql": "SELECT COUNT(*) AS failed_count FROM raw_orders WHERE order_id IS NULL OR TRIM(order_id) = ''",
        "severity": "critical",
    },
    {
        "check_name": "orders_customer_id_not_null",
        "table_name": "raw_orders",
        "sql": "SELECT COUNT(*) AS failed_count FROM raw_orders WHERE customer_id IS NULL OR TRIM(customer_id) = ''",
        "severity": "critical",
    },
    {
        "check_name": "orders_duplicate_order_id",
        "table_name": "raw_orders",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM (
                SELECT order_id
                FROM raw_orders
                GROUP BY order_id
                HAVING COUNT(*) > 1
            )
        """,
        "severity": "critical",
    },
    {
        "check_name": "customers_duplicate_customer_id",
        "table_name": "raw_customers",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM (
                SELECT customer_id
                FROM raw_customers
                GROUP BY customer_id
                HAVING COUNT(*) > 1
            )
        """,
        "severity": "critical",
    },
    {
        "check_name": "products_duplicate_product_id",
        "table_name": "raw_products",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM (
                SELECT product_id
                FROM raw_products
                GROUP BY product_id
                HAVING COUNT(*) > 1
            )
        """,
        "severity": "critical",
    },
    {
        "check_name": "sellers_duplicate_seller_id",
        "table_name": "raw_sellers",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM (
                SELECT seller_id
                FROM raw_sellers
                GROUP BY seller_id
                HAVING COUNT(*) > 1
            )
        """,
        "severity": "critical",
    },
    {
        "check_name": "order_items_order_id_not_found",
        "table_name": "raw_order_items",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_order_items oi
            LEFT JOIN raw_orders o
                ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL
        """,
        "severity": "critical",
    },
    {
        "check_name": "order_items_product_id_not_found",
        "table_name": "raw_order_items",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_order_items oi
            LEFT JOIN raw_products p
                ON oi.product_id = p.product_id
            WHERE p.product_id IS NULL
        """,
        "severity": "critical",
    },
    {
        "check_name": "order_items_seller_id_not_found",
        "table_name": "raw_order_items",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_order_items oi
            LEFT JOIN raw_sellers s
                ON oi.seller_id = s.seller_id
            WHERE s.seller_id IS NULL
        """,
        "severity": "critical",
    },
    {
        "check_name": "payments_order_id_not_found",
        "table_name": "raw_order_payments",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_order_payments p
            LEFT JOIN raw_orders o
                ON p.order_id = o.order_id
            WHERE o.order_id IS NULL
        """,
        "severity": "critical",
    },
    {
        "check_name": "reviews_order_id_not_found",
        "table_name": "raw_order_reviews",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_order_reviews r
            LEFT JOIN raw_orders o
                ON r.order_id = o.order_id
            WHERE o.order_id IS NULL
        """,
        "severity": "warning",
    },
    {
        "check_name": "order_items_negative_price",
        "table_name": "raw_order_items",
        "sql": "SELECT COUNT(*) AS failed_count FROM raw_order_items WHERE price < 0",
        "severity": "critical",
    },
    {
        "check_name": "order_items_negative_freight",
        "table_name": "raw_order_items",
        "sql": "SELECT COUNT(*) AS failed_count FROM raw_order_items WHERE freight_value < 0",
        "severity": "critical",
    },
    {
        "check_name": "payments_negative_payment_value",
        "table_name": "raw_order_payments",
        "sql": "SELECT COUNT(*) AS failed_count FROM raw_order_payments WHERE payment_value < 0",
        "severity": "critical",
    },
    {
        "check_name": "delivered_orders_missing_customer_delivery_date",
        "table_name": "raw_orders",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NULL
        """,
        "severity": "warning",
    },
    {
        "check_name": "delivery_before_purchase",
        "table_name": "raw_orders",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_orders
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_purchase_timestamp IS NOT NULL
              AND datetime(order_delivered_customer_date) < datetime(order_purchase_timestamp)
        """,
        "severity": "critical",
    },
    {
        "check_name": "estimated_delivery_before_purchase",
        "table_name": "raw_orders",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_orders
            WHERE order_estimated_delivery_date IS NOT NULL
              AND order_purchase_timestamp IS NOT NULL
              AND datetime(order_estimated_delivery_date) < datetime(order_purchase_timestamp)
        """,
        "severity": "warning",
    },
    {
        "check_name": "review_score_out_of_range",
        "table_name": "raw_order_reviews",
        "sql": """
            SELECT COUNT(*) AS failed_count
            FROM raw_order_reviews
            WHERE review_score < 1 OR review_score > 5
        """,
        "severity": "critical",
    },
]


def create_quality_results_table(engine) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS raw_data_quality_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        check_name TEXT NOT NULL,
        table_name TEXT NOT NULL,
        failed_count INTEGER NOT NULL,
        status TEXT NOT NULL,
        severity TEXT NOT NULL,
        checked_at TEXT NOT NULL
    );
    """

    with engine.begin() as connection:
        connection.execute(text(query))


def clear_previous_results(engine) -> None:
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM raw_data_quality_results"))


def run_check(engine, check: dict) -> dict:
    with engine.begin() as connection:
        failed_count = pd.read_sql(text(check["sql"]), connection)["failed_count"].iloc[0]

    failed_count = int(failed_count)
    status = "PASSED" if failed_count == 0 else "FAILED"

    return {
        "check_name": check["check_name"],
        "table_name": check["table_name"],
        "failed_count": failed_count,
        "status": status,
        "severity": check["severity"],
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def insert_quality_result(engine, result: dict) -> None:
    query = text(
        """
        INSERT INTO raw_data_quality_results (
            check_name,
            table_name,
            failed_count,
            status,
            severity,
            checked_at
        )
        VALUES (
            :check_name,
            :table_name,
            :failed_count,
            :status,
            :severity,
            :checked_at
        )
        """
    )

    with engine.begin() as connection:
        connection.execute(query, result)


def main() -> None:
    print("Running raw data quality checks...\n")

    engine = get_engine()
    create_quality_results_table(engine)
    clear_previous_results(engine)

    results = []

    for check in QUALITY_CHECKS:
        result = run_check(engine, check)
        insert_quality_result(engine, result)
        results.append(result)

        print(
            f"{result['status']} | {result['severity']} | "
            f"{result['check_name']} | failed_count={result['failed_count']}"
        )

    results_df = pd.DataFrame(results)
    output_path = REPORT_DIR / "raw_data_quality_results.csv"
    results_df.to_csv(output_path, index=False)

    print("\nRaw data quality checks completed.")
    print(f"Report saved to: {output_path}")

    failed_critical = results_df[
        (results_df["status"] == "FAILED") & (results_df["severity"] == "critical")
    ]

    if len(failed_critical) > 0:
        print("\nCritical failures found:")
        print(failed_critical[["check_name", "table_name", "failed_count"]])
    else:
        print("\nNo critical failures found.")


if __name__ == "__main__":
    main()