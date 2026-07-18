from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_OUTPUTS = [
    "logs/full_pipeline.log",
    "data/processed/raw_file_inspection_report.csv",
    "data/processed/raw_database_verification_report.csv",
    "data/processed/raw_data_quality_results.csv",
    "data/processed/dbt_model_verification_report.csv",
    "data/processed/dbt_tests_docs_verification_report.csv",
    "data/processed/operational_anomaly_detection_report.csv",
    "data/processed/operational_event_pipeline_verification_report.csv",
    "data/powerbi_exports/powerbi_export_summary.csv",
    "data/powerbi_exports/powerbi_export_verification_report.csv",
]


def main() -> None:
    results = []

    for relative_path in EXPECTED_OUTPUTS:
        file_path = PROJECT_ROOT / relative_path

        results.append(
            {
                "output_path": relative_path,
                "exists": file_path.exists(),
                "file_size_kb": round(file_path.stat().st_size / 1024, 2)
                if file_path.exists()
                else None,
            }
        )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = PROJECT_ROOT / "data" / "processed" / "full_pipeline_verification_report.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    missing_outputs = results_df[results_df["exists"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if missing_outputs.empty:
        print("\nAll expected full pipeline outputs exist.")
    else:
        print("\nMissing outputs:")
        print(missing_outputs[["output_path"]])


if __name__ == "__main__":
    main()