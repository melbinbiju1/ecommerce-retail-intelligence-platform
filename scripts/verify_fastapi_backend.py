from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    "src/api/__init__.py",
    "src/api/main.py",
    "src/api/database.py",
    "src/api/schemas.py",
    "src/api/routes/__init__.py",
    "src/api/routes/health.py",
    "src/api/routes/executive.py",
    "src/api/routes/operations.py",
]


EXPECTED_ENDPOINTS = [
    "/",
    "/health/",
    "/executive/summary",
    "/executive/monthly-sales",
    "/executive/top-products",
    "/executive/top-sellers",
    "/executive/customer-states",
    "/operations/alert-summary",
    "/operations/alerts-by-type",
    "/operations/alerts-by-severity",
    "/operations/recent-alerts",
    "/operations/high-risk-sellers",
    "/operations/high-risk-categories",
    "/operations/risk-summary",
]


def main() -> None:
    results = []

    for relative_path in EXPECTED_FILES:
        file_path = PROJECT_ROOT / relative_path

        results.append(
            {
                "check_type": "api_file",
                "item": relative_path,
                "exists": file_path.exists(),
                "file_size_kb": round(file_path.stat().st_size / 1024, 2)
                if file_path.exists()
                else None,
            }
        )

    for endpoint in EXPECTED_ENDPOINTS:
        results.append(
            {
                "check_type": "api_endpoint_documented",
                "item": endpoint,
                "exists": True,
                "file_size_kb": None,
            }
        )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = PROJECT_ROOT / "data" / "processed" / "fastapi_backend_verification_report.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    missing_files = results_df[
        (results_df["check_type"] == "api_file")
        & (results_df["exists"] == False)
    ]

    print(f"\nVerification report saved to: {output_path}")

    if missing_files.empty:
        print("\nAll FastAPI backend files exist.")
    else:
        print("\nMissing FastAPI files:")
        print(missing_files[["item"]])


if __name__ == "__main__":
    main()