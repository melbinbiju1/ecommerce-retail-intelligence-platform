from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    "src/api/auth.py",
    "src/api/main.py",
    "src/api/routes/executive.py",
    "src/api/routes/operations.py",
    ".env.example",
]

EXPECTED_AUTH_FEATURES = [
    "X-API-Key",
    "admin-demo-key",
    "analyst-demo-key",
    "viewer-demo-key",
    "require_roles",
    "get_current_role",
]

EXPECTED_EXECUTIVE_PROTECTION = [
    'require_roles(["admin", "analyst", "viewer"])',
    'require_roles(["admin", "analyst"])',
]

EXPECTED_OPERATIONS_PROTECTION = [
    'require_roles(["admin", "analyst"])',
]

EXPECTED_OPERATIONAL_QUERY_FIXES = [
    "ORDER BY alert_count DESC",
    "ORDER BY created_at DESC",
    "seller_risk_level",
    "category_risk_level",
    "late_delivery_rate DESC",
    "avg_review_score ASC",
]


def file_contains(path: Path, text: str) -> bool:
    if not path.exists():
        return False

    return text in path.read_text(encoding="utf-8")


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

    auth_file = PROJECT_ROOT / "src" / "api" / "auth.py"
    env_file = PROJECT_ROOT / ".env.example"
    executive_file = PROJECT_ROOT / "src" / "api" / "routes" / "executive.py"
    operations_file = PROJECT_ROOT / "src" / "api" / "routes" / "operations.py"

    for feature in EXPECTED_AUTH_FEATURES:
        passed = file_contains(auth_file, feature) or file_contains(env_file, feature)

        results.append(
            {
                "check_type": "auth_feature_present",
                "item": feature,
                "passed": passed,
            }
        )

    for protection in EXPECTED_EXECUTIVE_PROTECTION:
        results.append(
            {
                "check_type": "executive_route_protection",
                "item": protection,
                "passed": file_contains(executive_file, protection),
            }
        )

    for protection in EXPECTED_OPERATIONS_PROTECTION:
        results.append(
            {
                "check_type": "operations_route_protection",
                "item": protection,
                "passed": file_contains(operations_file, protection),
            }
        )

    for query_fix in EXPECTED_OPERATIONAL_QUERY_FIXES:
        results.append(
            {
                "check_type": "operations_query_validation",
                "item": query_fix,
                "passed": file_contains(operations_file, query_fix),
            }
        )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "api_auth_rbac_verification_report.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if failed_checks.empty:
        print("\nAPI authentication and RBAC verification passed.")
    else:
        print("\nSome authentication/RBAC checks failed:")
        print(failed_checks[["check_type", "item"]])


if __name__ == "__main__":
    main()