from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DBT_DIR = PROJECT_ROOT / "dbt_retail"

SQL_FILES_TO_CONVERT = [
    {
        "source_file": PROJECT_ROOT / "sql" / "staging" / "create_staging_tables.sql",
        "target_folder": DBT_DIR / "models" / "staging",
        "materialized": "table",
    },
    {
        "source_file": PROJECT_ROOT / "sql" / "warehouse" / "create_warehouse_tables.sql",
        "target_folder": DBT_DIR / "models" / "warehouse",
        "materialized": "table",
    },
    {
        "source_file": PROJECT_ROOT / "sql" / "kpi_views" / "create_kpi_views.sql",
        "target_folder": DBT_DIR / "models" / "kpis",
        "materialized": "view",
    },
    {
        "source_file": PROJECT_ROOT / "sql" / "operations" / "create_operational_metrics.sql",
        "target_folder": DBT_DIR / "models" / "operations",
        "materialized": "table",
    },
    {
        "source_file": PROJECT_ROOT / "sql" / "kpi_views" / "create_operational_kpi_views.sql",
        "target_folder": DBT_DIR / "models" / "operational_kpis",
        "materialized": "view",
    },
]


RAW_SOURCES_YML = """
version: 2

sources:
  - name: raw
    database: retail_intelligence
    schema: main
    tables:
      - name: raw_customers
      - name: raw_geolocation
      - name: raw_order_items
      - name: raw_order_payments
      - name: raw_order_reviews
      - name: raw_orders
      - name: raw_products
      - name: raw_sellers
      - name: raw_product_category_translation
"""


def find_database_file() -> Path:
    possible_paths = [
        PROJECT_ROOT / "retail_intelligence.db",
        PROJECT_ROOT / "data" / "retail_intelligence.db",
        PROJECT_ROOT / "data" / "database" / "retail_intelligence.db",
        PROJECT_ROOT / "database" / "retail_intelligence.db",
    ]

    for path in possible_paths:
        if path.exists():
            return path.resolve()

    db_files = list(PROJECT_ROOT.rglob("*.db"))

    if len(db_files) == 1:
        return db_files[0].resolve()

    raise FileNotFoundError(
        "Could not find retail_intelligence.db. Please check your database path."
    )


def create_directories() -> None:
    folders = [
        DBT_DIR,
        DBT_DIR / "models",
        DBT_DIR / "models" / "staging",
        DBT_DIR / "models" / "warehouse",
        DBT_DIR / "models" / "kpis",
        DBT_DIR / "models" / "operations",
        DBT_DIR / "models" / "operational_kpis",
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def write_dbt_project_file() -> None:
    content = """
name: ecommerce_retail_intelligence
version: '1.0.0'
config-version: 2

profile: ecommerce_retail_intelligence

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  ecommerce_retail_intelligence:
    staging:
      +materialized: table
    warehouse:
      +materialized: table
    kpis:
      +materialized: view
    operations:
      +materialized: table
    operational_kpis:
      +materialized: view
""".strip()

    (DBT_DIR / "dbt_project.yml").write_text(content, encoding="utf-8")


def write_profiles_file(database_path: Path) -> None:
    database_path_posix = database_path.as_posix()
    schema_directory_posix = database_path.parent.as_posix()

    content = f"""
ecommerce_retail_intelligence:
  target: dev
  outputs:
    dev:
      type: sqlite
      threads: 1
      database: retail_intelligence
      schema: main
      schemas_and_paths:
        main: "{database_path_posix}"
      schema_directory: "{schema_directory_posix}"
""".strip()

    (DBT_DIR / "profiles.yml").write_text(content, encoding="utf-8")


def write_sources_file() -> None:
    sources_path = DBT_DIR / "models" / "staging" / "sources.yml"
    sources_path.write_text(RAW_SOURCES_YML.strip(), encoding="utf-8")


def split_sql_statements(sql_script: str) -> list[str]:
    return [
        statement.strip()
        for statement in sql_script.split(";")
        if statement.strip()
    ]


def remove_drop_statements(sql_script: str) -> str:
    sql_script = re.sub(
        r"DROP\s+(TABLE|VIEW)\s+IF\s+EXISTS\s+[A-Za-z0-9_]+\s*;",
        "",
        sql_script,
        flags=re.IGNORECASE,
    )
    return sql_script


def extract_create_as_models(sql_script: str) -> list[dict]:
    models = []

    pattern = re.compile(
        r"CREATE\s+(TABLE|VIEW)\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z0-9_]+)\s+AS\s+(.*?)(?=;\s*(?:CREATE|DROP|INSERT|$))",
        re.IGNORECASE | re.DOTALL,
    )

    for match in pattern.finditer(sql_script):
        model_name = match.group(2).strip()
        select_sql = match.group(3).strip()

        if select_sql.upper().startswith("SELECT") or select_sql.upper().startswith("WITH"):
            models.append(
                {
                    "model_name": model_name,
                    "select_sql": select_sql,
                }
            )

    return models


def extract_insert_select_models(sql_script: str) -> list[dict]:
    models = []

    pattern = re.compile(
        r"INSERT\s+INTO\s+([A-Za-z0-9_]+)(?:\s*\([^)]*\))?\s+(SELECT|WITH)\s+(.*?)(?=;\s*(?:CREATE|DROP|INSERT|$))",
        re.IGNORECASE | re.DOTALL,
    )

    for match in pattern.finditer(sql_script):
        model_name = match.group(1).strip()
        select_start = match.group(2).strip()
        select_body = match.group(3).strip()

        select_sql = f"{select_start} {select_body}"

        models.append(
            {
                "model_name": model_name,
                "select_sql": select_sql,
            }
        )

    return models


def extract_models(sql_script: str) -> list[dict]:
    sql_script = remove_drop_statements(sql_script)

    models = []
    models.extend(extract_create_as_models(sql_script))
    models.extend(extract_insert_select_models(sql_script))

    unique_models = {}
    for model in models:
        unique_models[model["model_name"]] = model

    return list(unique_models.values())


def convert_sql_file_to_dbt_models(
    source_file: Path,
    target_folder: Path,
    materialized: str,
) -> list[str]:
    if not source_file.exists():
        print(f"WARNING | SQL file not found: {source_file}")
        return []

    sql_script = source_file.read_text(encoding="utf-8")
    models = extract_models(sql_script)

    created_models = []

    for model in models:
        model_name = model["model_name"]
        select_sql = model["select_sql"].strip()

        model_content = f"""
{{{{ config(materialized='{materialized}') }}}}

{select_sql}
""".strip()

        output_file = target_folder / f"{model_name}.sql"
        output_file.write_text(model_content, encoding="utf-8")

        created_models.append(model_name)

    return created_models


def main() -> None:
    print("Setting up dbt project...")

    database_path = find_database_file()

    create_directories()
    write_dbt_project_file()
    write_profiles_file(database_path)
    write_sources_file()

    total_models_created = 0

    for item in SQL_FILES_TO_CONVERT:
        created_models = convert_sql_file_to_dbt_models(
            source_file=item["source_file"],
            target_folder=item["target_folder"],
            materialized=item["materialized"],
        )

        total_models_created += len(created_models)

        print(
            f"Converted {len(created_models)} models from {item['source_file'].relative_to(PROJECT_ROOT)}"
        )

        for model_name in created_models:
            print(f"  - {model_name}")

    print("\ndbt project setup completed.")
    print(f"SQLite database path: {database_path}")
    print(f"Total dbt models created: {total_models_created}")
    print(f"dbt project folder: {DBT_DIR}")


if __name__ == "__main__":
    main()