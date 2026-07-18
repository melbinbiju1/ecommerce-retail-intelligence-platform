from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_DOCS = [
    "docs/data_governance.md",
    "docs/data_lineage.md",
    "docs/azure_sql_migration_plan.md",
]


def main() -> None:
    results = []

    for relative_path in EXPECTED_DOCS:
        file_path = PROJECT_ROOT / relative_path

        exists = file_path.exists()
        word_count = None
        file_size_kb = None

        if exists:
            content = file_path.read_text(encoding="utf-8")
            word_count = len(content.split())
            file_size_kb = round(file_path.stat().st_size / 1024, 2)

        results.append(
            {
                "document": relative_path,
                "exists": exists,
                "word_count": word_count,
                "file_size_kb": file_size_kb,
            }
        )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = PROJECT_ROOT / "data" / "processed" / "governance_docs_verification_report.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    missing_docs = results_df[results_df["exists"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if missing_docs.empty:
        print("\nAll governance and migration documents exist.")
    else:
        print("\nMissing documents:")
        print(missing_docs[["document"]])


if __name__ == "__main__":
    main()