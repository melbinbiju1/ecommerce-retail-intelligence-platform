from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DBT_MODELS_DIR = PROJECT_ROOT / "dbt_retail" / "models"


RAW_SOURCE_TABLES = [
    "raw_customers",
    "raw_geolocation",
    "raw_order_items",
    "raw_order_payments",
    "raw_order_reviews",
    "raw_orders",
    "raw_products",
    "raw_sellers",
    "raw_product_category_translation",
]


OPERATIONAL_SOURCE_TABLES = [
    "ops_anomaly_alerts",
    "ops_anomaly_rules",
    "ops_event_log",
    "ops_event_records",
    "ops_event_failed_records",
]


DBT_MODEL_NAMES = [
    file_path.stem
    for file_path in DBT_MODELS_DIR.rglob("*.sql")
]


def replace_table_reference(sql_text: str, table_name: str, replacement: str) -> str:
    pattern = re.compile(
        rf"\b(FROM|JOIN)\s+{table_name}\b",
        flags=re.IGNORECASE,
    )

    return pattern.sub(lambda match: f"{match.group(1)} {replacement}", sql_text)


def update_sql_file(file_path: Path) -> bool:
    original_text = file_path.read_text(encoding="utf-8")
    updated_text = original_text

    for table_name in RAW_SOURCE_TABLES:
        updated_text = replace_table_reference(
            updated_text,
            table_name,
            "{{ source('raw', '" + table_name + "') }}",
        )

    for table_name in OPERATIONAL_SOURCE_TABLES:
        updated_text = replace_table_reference(
            updated_text,
            table_name,
            "{{ source('operations_external', '" + table_name + "') }}",
        )

    for model_name in DBT_MODEL_NAMES:
        if model_name == file_path.stem:
            continue

        updated_text = replace_table_reference(
            updated_text,
            model_name,
            "{{ ref('" + model_name + "') }}",
        )

    if updated_text != original_text:
        file_path.write_text(updated_text, encoding="utf-8")
        return True

    return False


def main() -> None:
    print("Updating dbt model references...")

    updated_files = []

    for file_path in DBT_MODELS_DIR.rglob("*.sql"):
        was_updated = update_sql_file(file_path)

        if was_updated:
            updated_files.append(file_path)

    print(f"Updated dbt files: {len(updated_files)}")

    for file_path in updated_files:
        print(f"- {file_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()