from pathlib import Path
import os
import sys

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

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin-demo-key")

OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "azure_app_deployment_verification_report.csv"
)

CHECKS = [
    {
        "name": "root",
        "url": f"{APP_BASE_URL}/",
        "requires_auth": False,
    },
    {
        "name": "health",
        "url": f"{APP_BASE_URL}/health/",
        "requires_auth": False,
    },
    {
        "name": "executive_summary",
        "url": f"{APP_BASE_URL}/executive/summary",
        "requires_auth": True,
    },
    {
        "name": "operations_alert_summary",
        "url": f"{APP_BASE_URL}/operations/alert-summary",
        "requires_auth": True,
    },
    {
        "name": "insights_executive_summary",
        "url": f"{APP_BASE_URL}/insights/executive-summary",
        "requires_auth": True,
    },
]


def run_check(check: dict) -> dict:
    headers = {}

    if check["requires_auth"]:
        headers["X-API-Key"] = ADMIN_API_KEY

    try:
        response = requests.get(
            check["url"],
            headers=headers,
            timeout=60,
        )

        return {
            "check_name": check["name"],
            "url": check["url"],
            "status_code": response.status_code,
            "passed": response.status_code == 200,
            "response_preview": response.text[:300],
        }

    except Exception as error:
        return {
            "check_name": check["name"],
            "url": check["url"],
            "status_code": None,
            "passed": False,
            "response_preview": str(error),
        }


def main() -> None:
    results = [run_check(check) for check in CHECKS]

    results_df = pd.DataFrame(results)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(results_df)
    print(f"\nVerification report saved to: {OUTPUT_REPORT}")

    failed_checks = results_df[results_df["passed"] == False]

    if failed_checks.empty:
        print("\nAzure App deployment verification passed.")
    else:
        print("\nSome Azure App deployment checks failed:")
        print(failed_checks[["check_name", "status_code", "response_preview"]])
        raise RuntimeError("Azure App deployment verification failed.")


if __name__ == "__main__":
    main()