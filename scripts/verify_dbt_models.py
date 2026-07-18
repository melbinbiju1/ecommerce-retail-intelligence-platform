from pathlib import Path
import sys
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.db_utils import get_engine


DBT_MODEL_FOLDERS = [
    Path("dbt_retail/models/staging"),
    Path("dbt_retail/models/warehouse"),
    Path("dbt_retail/models/kpis"),
    Path("dbt_retail/models/operations"),
    Path("dbt_retail/models/operational_kpis"),
]


def get_model_names() -> list[str]:
    model_names = []

    for folder in DBT_MODEL_FOLDERS:
        if folder.exists():
            for file_path in folder.glob("*.sql"):
                model_names.append(file_path.stem)

    return sorted(set(model_names))


def check_model_exists(engine, model_name: str) -> dict:
    with engine.begin() as connection:
        exists_query = text(
            """
            SELECT
                name,
                type
            FROM sqlite_master
            WHERE name = :model_name
              AND type IN ('table', 'view')
            """
        )

        exists_result = pd.read_sql(
            exists_query,
            connection,
            params={"model_name": model_name},
        )

        exists = not exists_result.empty
        object_type = exists_result["type"].iloc[0] if exists else None
        row_count = None

        if exists:
            row_count_query = text(f"SELECT COUNT(*) AS row_count FROM {model_name}")
            row_count = int(
                pd.read_sql(row_count_query, connection)["row_count"].iloc[0]
            )

        return {
            "model_name": model_name,
            "exists": exists,
            "object_type": object_type,
            "row_count": row_count,
        }


def main() -> None:
    print("Verifying dbt models in SQLite database...\n")

    engine = get_engine()
    model_names = get_model_names()

    if not model_names:
        raise ValueError("No dbt model SQL files found in dbt_retail/models.")

    results = []

    for model_name in model_names:
        results.append(check_model_exists(engine, model_name))

    results_df = pd.DataFrame(results)

    print(results_df)

    output_path = Path("data/processed/dbt_model_verification_report.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    missing_models = results_df[results_df["exists"] == False]

    print(f"\nTotal dbt models checked: {len(results_df)}")
    print(f"Models found in database: {int(results_df['exists'].sum())}")
    print(f"Missing models: {len(missing_models)}")
    print(f"\ndbt model verification report saved to: {output_path}")

    if missing_models.empty:
        print("\nAll dbt models exist in the database.")
    else:
        print("\nMissing dbt models:")
        print(missing_models[["model_name"]])


if __name__ == "__main__":
    main()