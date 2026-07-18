from pathlib import Path
from datetime import datetime
import subprocess
import sys
import re
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

TEST_LOG_FILE = LOG_DIR / "test_run.log"
TEST_SUMMARY_REPORT = PROCESSED_DIR / "automated_test_run_summary.csv"


def write_log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(TEST_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def extract_test_summary(test_output: str) -> dict:
    passed_match = re.search(r"(\d+)\s+passed", test_output)
    failed_match = re.search(r"(\d+)\s+failed", test_output)
    error_match = re.search(r"(\d+)\s+errors?", test_output)
    warning_match = re.search(r"(\d+)\s+warnings?", test_output)

    return {
        "passed_tests": int(passed_match.group(1)) if passed_match else 0,
        "failed_tests": int(failed_match.group(1)) if failed_match else 0,
        "error_count": int(error_match.group(1)) if error_match else 0,
        "warning_count": int(warning_match.group(1)) if warning_match else 0,
    }


def main() -> None:
    print("Running automated tests...")

    start_time = datetime.now()
    write_log("TEST_RUN_STARTED")

    command = [
        sys.executable,
        "-m",
        "pytest",
        "tests",
        "-v",
    ]

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )

    end_time = datetime.now()
    duration_seconds = round((end_time - start_time).total_seconds(), 2)

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    write_log(result.stdout)

    if result.stderr:
        write_log(result.stderr)

    test_summary = extract_test_summary(result.stdout)

    summary_row = {
        "run_started_at": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "run_finished_at": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_seconds": duration_seconds,
        "command": " ".join(command),
        "return_code": result.returncode,
        "status": "PASSED" if result.returncode == 0 else "FAILED",
        "passed_tests": test_summary["passed_tests"],
        "failed_tests": test_summary["failed_tests"],
        "error_count": test_summary["error_count"],
        "warning_count": test_summary["warning_count"],
        "test_structure": "tests/api, tests/unit, tests/integration",
    }

    summary_df = pd.DataFrame([summary_row])
    summary_df.to_csv(TEST_SUMMARY_REPORT, index=False)

    print(f"\nTest summary report saved to: {TEST_SUMMARY_REPORT}")
    write_log(f"TEST_SUMMARY_REPORT_CREATED | {TEST_SUMMARY_REPORT}")

    if result.returncode != 0:
        write_log("TEST_RUN_FAILED")
        raise RuntimeError("Automated tests failed.")

    write_log("TEST_RUN_PASSED")
    print("\nAutomated tests passed successfully.")


if __name__ == "__main__":
    main()