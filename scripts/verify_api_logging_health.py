from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    "src/api/logging_config.py",
    "src/api/database.py",
    "src/api/schemas.py",
    "src/api/routes/health.py",
    "src/api/main.py",
]

EXPECTED_FEATURES = {
    "src/api/logging_config.py": [
        "RotatingFileHandler",
        "api.log",
        "setup_api_logger",
    ],
    "src/api/database.py": [
        "check_database_connection",
        "check_database_object_exists",
        "api_logger.exception",
    ],
    "src/api/routes/health.py": [
        "/status",
        "SystemStatusResponse",
        "checked_objects",
    ],
    "src/api/main.py": [
        "@app.middleware",
        "log_requests",
        "global_exception_handler",
        "Internal server error",
    ],
}


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

    for relative_path, features in EXPECTED_FEATURES.items():
        for feature in features:
            results.append(
                {
                    "check_type": "feature_present",
                    "item": f"{relative_path} | {feature}",
                    "passed": file_contains(relative_path, feature),
                }
            )

    log_file = PROJECT_ROOT / "logs" / "api.log"

    results.append(
        {
            "check_type": "log_file_available",
            "item": "logs/api.log",
            "passed": log_file.exists(),
        }
    )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "api_logging_health_verification_report.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if failed_checks.empty:
        print("\nAPI logging, error handling, and health check verification passed.")
    else:
        print("\nSome checks failed:")
        print(failed_checks[["check_type", "item"]])


if __name__ == "__main__":
    main()