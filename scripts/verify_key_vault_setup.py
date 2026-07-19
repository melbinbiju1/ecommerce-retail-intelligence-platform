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

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

OUTPUT_REPORT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "key_vault_setup_verification_report.csv"
)


def run_endpoint_check(name: str, url: str, api_key: str | None = None) -> dict:
    headers = {}

    if api_key:
        headers["X-API-Key"] = api_key

    try:
        response = requests.get(url, headers=headers, timeout=60)

        return {
            "check_name": name,
            "url": url,
            "status_code": response.status_code,
            "passed": response.status_code == 200,
            "response_preview": response.text[:300],
        }

    except Exception as error:
        return {
            "check_name": name,
            "url": url,
            "status_code": None,
            "passed": False,
            "response_preview": str(error),
        }


def main() -> None:
    checks = [
        run_endpoint_check(
            name="public_health_check",
            url=f"{APP_BASE_URL}/health/",
        ),
        run_endpoint_check(
            name="protected_executive_summary_check",
            url=f"{APP_BASE_URL}/executive/summary",
            api_key=ADMIN_API_KEY,
        ),
        run_endpoint_check(
            name="protected_operations_alert_summary_check",
            url=f"{APP_BASE_URL}/operations/alert-summary",
            api_key=ADMIN_API_KEY,
        ),
    ]

    results_df = pd.DataFrame(checks)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_REPORT, index=False)

    print(results_df)
    print(f"\nVerification report saved to: {OUTPUT_REPORT}")

    failed_checks = results_df[results_df["passed"] == False]

    if failed_checks.empty:
        print("\nKey Vault setup verification passed.")
        print("The deployed API is working after replacing App Service secrets with Key Vault references.")
    else:
        print("\nSome Key Vault setup checks failed:")
        print(failed_checks[["check_name", "status_code", "response_preview"]])
        raise RuntimeError("Key Vault setup verification failed.")


if __name__ == "__main__":
    main()