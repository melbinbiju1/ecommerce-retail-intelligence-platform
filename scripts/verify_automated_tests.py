from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    "tests/conftest.py",
    "tests/unit/test_database.py",
    "tests/unit/test_ai_business_insights.py",
    "tests/api/test_api_health.py",
    "tests/api/test_api_executive.py",
    "tests/api/test_api_operations.py",
    "tests/api/test_api_insights.py",
    "tests/api/test_api_rbac.py",
    "tests/integration/test_pipeline_outputs.py",
    "scripts/run_tests.py",
    "logs/test_run.log",
    "data/processed/automated_test_run_summary.csv",
]

EXPECTED_TEST_KEYWORDS = [
    "test_database_connection",
    "test_generate_executive_summary",
    "test_health_endpoint",
    "test_executive_summary_admin_access",
    "test_alert_summary_admin_access",
    "test_insights_executive_summary_viewer_access",
    "test_missing_api_key_denied_for_protected_endpoint",
    "test_important_pipeline_outputs_exist",
]


def file_contains(relative_path: str, text: str) -> bool:
    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():
        return False

    return text in file_path.read_text(encoding="utf-8")


def main() -> None:
    results = []

    for relative_path in EXPECTED_FILES:
        file_path = PROJECT_ROOT / relative_path

        results.append(
            {
                "check_type": "file_exists",
                "item": relative_path,
                "passed": file_path.exists(),
            }
        )

    test_files = [
        "tests/unit/test_database.py",
        "tests/unit/test_ai_business_insights.py",
        "tests/api/test_api_health.py",
        "tests/api/test_api_executive.py",
        "tests/api/test_api_operations.py",
        "tests/api/test_api_insights.py",
        "tests/api/test_api_rbac.py",
        "tests/integration/test_pipeline_outputs.py",
    ]

    for keyword in EXPECTED_TEST_KEYWORDS:
        passed = any(file_contains(test_file, keyword) for test_file in test_files)

        results.append(
            {
                "check_type": "test_function_exists",
                "item": keyword,
                "passed": passed,
            }
        )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "automated_tests_verification_report.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if failed_checks.empty:
        print("\nAutomated testing verification passed.")
    else:
        print("\nSome automated testing checks failed:")
        print(failed_checks[["check_type", "item"]])


if __name__ == "__main__":
    main()