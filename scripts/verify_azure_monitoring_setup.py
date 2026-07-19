from pathlib import Path
import os
import sys
from datetime import datetime, timezone

import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

APP_BASE_URL = os.getenv(
    "AZURE_APP_BASE_URL",
    "https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net",
).rstrip("/")

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "azure_monitoring_setup_verification_report.csv"
)


MONITORING_EXPECTATIONS = [
    {
        "check_name": "app_service_logs_enabled",
        "component": "Azure App Service",
        "expected_configuration": "Application logging enabled with file system logging",
        "verification_method": "Verified manually in Azure Portal and Log Stream",
        "passed": True,
    },
    {
        "check_name": "log_stream_verified",
        "component": "Azure App Service",
        "expected_configuration": "Log Stream shows container or request activity",
        "verification_method": "Verified manually after calling /health/",
        "passed": True,
    },
    {
        "check_name": "built_in_health_check_skipped",
        "component": "Azure App Service",
        "expected_configuration": "Built-in Health Check requires Basic B1 or higher",
        "verification_method": "Skipped intentionally because project uses Free App Service plan",
        "passed": True,
    },
    {
        "check_name": "application_insights_created",
        "component": "Application Insights",
        "expected_configuration": "Application Insights resource created for the deployed API",
        "verification_method": "Verified manually in Azure Portal",
        "passed": True,
    },
    {
        "check_name": "availability_test_created",
        "component": "Application Insights",
        "expected_configuration": "Standard availability test created for /health/",
        "verification_method": "Verified manually with successful availability result",
        "passed": True,
    },
    {
        "check_name": "availability_alert_rule_created",
        "component": "Azure Monitor Alerts",
        "expected_configuration": "Automatic alert rule created for availability test failures",
        "verification_method": "Verified manually in Azure Portal",
        "passed": True,
    },
]


def run_endpoint_check(
    check_name: str,
    url: str,
    api_key: str | None = None,
) -> dict:
    headers = {}

    if api_key:
        headers["X-API-Key"] = api_key

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=60,
        )

        return {
            "check_name": check_name,
            "component": "Deployed FastAPI API",
            "expected_configuration": "Endpoint returns HTTP 200",
            "verification_method": "Automated HTTP request",
            "url": url,
            "status_code": response.status_code,
            "passed": response.status_code == 200,
            "response_preview": response.text[:300],
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as error:
        return {
            "check_name": check_name,
            "component": "Deployed FastAPI API",
            "expected_configuration": "Endpoint returns HTTP 200",
            "verification_method": "Automated HTTP request",
            "url": url,
            "status_code": None,
            "passed": False,
            "response_preview": str(error),
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        }


def main() -> None:
    automated_checks = [
        run_endpoint_check(
            check_name="public_health_endpoint_available",
            url=f"{APP_BASE_URL}/health/",
        ),
        run_endpoint_check(
            check_name="protected_executive_summary_available",
            url=f"{APP_BASE_URL}/executive/summary",
            api_key=ADMIN_API_KEY,
        ),
        run_endpoint_check(
            check_name="protected_operations_alert_summary_available",
            url=f"{APP_BASE_URL}/operations/alert-summary",
            api_key=ADMIN_API_KEY,
        ),
    ]

    manual_checks = []

    for check in MONITORING_EXPECTATIONS:
        manual_checks.append(
            {
                **check,
                "url": None,
                "status_code": None,
                "response_preview": None,
                "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        )

    results_df = pd.DataFrame(manual_checks + automated_checks)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(results_df)
    print(f"\nVerification report saved to: {OUTPUT_REPORT}")

    failed_checks = results_df[results_df["passed"] == False]

    if failed_checks.empty:
        print("\nAzure monitoring setup verification passed.")
        print("Monitoring evidence includes App Service logs, Application Insights availability test, alert rule, and endpoint checks.")
    else:
        print("\nSome Azure monitoring setup checks failed:")
        print(
            failed_checks[
                [
                    "check_name",
                    "component",
                    "status_code",
                    "response_preview",
                ]
            ]
        )
        raise RuntimeError("Azure monitoring setup verification failed.")


if __name__ == "__main__":
    main()