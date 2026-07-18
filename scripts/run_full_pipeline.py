from pathlib import Path
from datetime import datetime
import argparse
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

PIPELINE_LOG_FILE = LOG_DIR / "full_pipeline.log"


def write_log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(PIPELINE_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def run_command(
    command: list[str],
    step_name: str,
    cwd: Path | None = None,
    continue_on_failure: bool = False,
) -> bool:
    working_directory = cwd if cwd else PROJECT_ROOT

    print("\n" + "=" * 100)
    print(f"STARTING STEP: {step_name}")
    print("=" * 100)

    write_log(f"STARTED | {step_name} | command={' '.join(command)}")

    result = subprocess.run(
        command,
        cwd=working_directory,
        text=True,
        capture_output=True,
        shell=False,
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        print(f"SUCCESS: {step_name}")
        write_log(f"SUCCESS | {step_name}")
        return True

    print(f"FAILED: {step_name}")
    write_log(f"FAILED | {step_name} | return_code={result.returncode}")

    if continue_on_failure:
        print(f"Continuing pipeline because continue_on_failure=True for: {step_name}")
        write_log(f"CONTINUED_AFTER_FAILURE | {step_name}")
        return False

    raise RuntimeError(f"Pipeline stopped because this step failed: {step_name}")


def check_required_paths() -> None:
    required_paths = [
        PROJECT_ROOT / "data" / "raw",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "dbt_retail",
        PROJECT_ROOT / "dbt_retail" / "dbt_project.yml",
        PROJECT_ROOT / "dbt_retail" / "profiles.yml",
    ]

    missing_paths = [path for path in required_paths if not path.exists()]

    if missing_paths:
        print("Missing required project paths:")
        for path in missing_paths:
            print(f"- {path}")
        raise FileNotFoundError("Some required project paths are missing.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the full local data engineering pipeline."
    )

    parser.add_argument(
        "--skip-dbt-test",
        action="store_true",
        help="Skip dbt tests if you only want to refresh models and exports.",
    )

    parser.add_argument(
        "--generate-event-file",
        action="store_true",
        help="Generate a sample operational event file before processing event files.",
    )

    args = parser.parse_args()

    pipeline_start_time = datetime.now()

    print("Starting full local pipeline...")
    print(f"Project root: {PROJECT_ROOT}")
    write_log("PIPELINE_STARTED")

    check_required_paths()

    python_executable = sys.executable

    pipeline_steps = [
        {
            "step_name": "Raw file inspection",
            "command": [python_executable, "scripts/inspect_raw_data.py"],
            "cwd": PROJECT_ROOT,
            "continue_on_failure": False,
        },
        {
            "step_name": "Raw data ingestion into SQLite",
            "command": [python_executable, "scripts/load_raw_to_sqlite.py"],
            "cwd": PROJECT_ROOT,
            "continue_on_failure": False,
        },
        {
            "step_name": "Raw database verification",
            "command": [python_executable, "scripts/verify_raw_database.py"],
            "cwd": PROJECT_ROOT,
            "continue_on_failure": False,
        },
        {
            "step_name": "Raw data quality checks",
            "command": [python_executable, "scripts/run_raw_data_quality_checks.py"],
            "cwd": PROJECT_ROOT,
            "continue_on_failure": False,
        },
        {
            "step_name": "dbt run",
            "command": ["dbt", "run", "--profiles-dir", "."],
            "cwd": PROJECT_ROOT / "dbt_retail",
            "continue_on_failure": False,
        },
    ]

    if not args.skip_dbt_test:
        pipeline_steps.append(
            {
                "step_name": "dbt test",
                "command": ["dbt", "test", "--profiles-dir", "."],
                "cwd": PROJECT_ROOT / "dbt_retail",
                "continue_on_failure": False,
            }
        )

    pipeline_steps.extend(
        [
            {
                "step_name": "Operational anomaly detection",
                "command": [python_executable, "scripts/detect_operational_anomalies.py"],
                "cwd": PROJECT_ROOT,
                "continue_on_failure": False,
            },
        ]
    )

    if args.generate_event_file:
        pipeline_steps.append(
            {
                "step_name": "Generate sample operational event file",
                "command": [python_executable, "scripts/generate_operational_event_file.py"],
                "cwd": PROJECT_ROOT,
                "continue_on_failure": False,
            }
        )

    pipeline_steps.extend(
        [
            {
                "step_name": "Process operational event files",
                "command": [python_executable, "scripts/process_operational_event_files.py"],
                "cwd": PROJECT_ROOT,
                "continue_on_failure": False,
            },
            {
                "step_name": "Refresh operational KPI views",
                "command": ["dbt", "run", "--profiles-dir", ".", "--select", "operational_kpis"],
                "cwd": PROJECT_ROOT / "dbt_retail",
                "continue_on_failure": False,
            },
            {
                "step_name": "Export Power BI CSV files",
                "command": [python_executable, "scripts/export_powerbi_views.py"],
                "cwd": PROJECT_ROOT,
                "continue_on_failure": False,
            },
            {
                "step_name": "Verify Power BI exports",
                "command": [python_executable, "scripts/verify_powerbi_exports.py"],
                "cwd": PROJECT_ROOT,
                "continue_on_failure": False,
            },
        ]
    )

    completed_steps = 0

    for step in pipeline_steps:
        run_command(
            command=step["command"],
            step_name=step["step_name"],
            cwd=step["cwd"],
            continue_on_failure=step["continue_on_failure"],
        )
        completed_steps += 1

    pipeline_end_time = datetime.now()
    duration_seconds = round(
        (pipeline_end_time - pipeline_start_time).total_seconds(),
        2,
    )

    print("\n" + "=" * 100)
    print("FULL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 100)
    print(f"Completed steps: {completed_steps}")
    print(f"Duration seconds: {duration_seconds}")
    print(f"Log file: {PIPELINE_LOG_FILE}")

    write_log(
        f"PIPELINE_COMPLETED | completed_steps={completed_steps} | duration_seconds={duration_seconds}"
    )


if __name__ == "__main__":
    main()