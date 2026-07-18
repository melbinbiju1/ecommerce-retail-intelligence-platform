from pathlib import Path
import json
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DBT_DIR = PROJECT_ROOT / "dbt_retail"
TARGET_DIR = DBT_DIR / "target"


EXPECTED_SCHEMA_FILES = [
    DBT_DIR / "models" / "staging" / "schema.yml",
    DBT_DIR / "models" / "warehouse" / "schema.yml",
    DBT_DIR / "models" / "kpis" / "schema.yml",
    DBT_DIR / "models" / "operations" / "schema.yml",
    DBT_DIR / "models" / "operational_kpis" / "schema.yml",
]


EXPECTED_DOC_FILES = [
    TARGET_DIR / "manifest.json",
    TARGET_DIR / "catalog.json",
    TARGET_DIR / "index.html",
]


def count_manifest_items(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        return {
            "models_in_manifest": None,
            "sources_in_manifest": None,
            "tests_in_manifest": None,
        }

    with open(manifest_path, "r", encoding="utf-8") as file:
        manifest = json.load(file)

    nodes = manifest.get("nodes", {})
    sources = manifest.get("sources", {})

    model_count = sum(
        1
        for node in nodes.values()
        if node.get("resource_type") == "model"
    )

    test_count = sum(
        1
        for node in nodes.values()
        if node.get("resource_type") == "test"
    )

    return {
        "models_in_manifest": model_count,
        "sources_in_manifest": len(sources),
        "tests_in_manifest": test_count,
    }


def main() -> None:
    results = []

    for file_path in EXPECTED_SCHEMA_FILES:
        results.append(
            {
                "file_type": "schema_file",
                "file_path": str(file_path.relative_to(PROJECT_ROOT)),
                "exists": file_path.exists(),
            }
        )

    for file_path in EXPECTED_DOC_FILES:
        results.append(
            {
                "file_type": "dbt_docs_artifact",
                "file_path": str(file_path.relative_to(PROJECT_ROOT)),
                "exists": file_path.exists(),
            }
        )

    results_df = pd.DataFrame(results)
    print(results_df)

    manifest_stats = count_manifest_items(TARGET_DIR / "manifest.json")

    print("\ndbt manifest summary:")
    for key, value in manifest_stats.items():
        print(f"{key}: {value}")

    output_path = PROJECT_ROOT / "data" / "processed" / "dbt_tests_docs_verification_report.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    print(f"\nVerification report saved to: {output_path}")

    missing_files = results_df[results_df["exists"] == False]

    if missing_files.empty:
        print("\nAll expected dbt schema and documentation files exist.")
    else:
        print("\nMissing files:")
        print(missing_files[["file_path"]])


if __name__ == "__main__":
    main()