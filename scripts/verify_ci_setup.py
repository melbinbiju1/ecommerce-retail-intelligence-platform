from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    ".github/workflows/ci.yml",
    "README.md",
    "docs/architecture.md",
    "docs/data_governance.md",
    "docs/data_dictionary.md",
    "docs/setup_guide.md",
    "scripts/verify_ci_setup.py",
    "scripts/verify_docker_setup.py",
]

EXPECTED_CI_WORKFLOW_CONTENT = [
    "name: CI Pipeline",
    "actions/checkout@v4",
    "actions/setup-python@v5",
    "python-version: \"3.10\"",
    "pip install -r requirements.txt",
    "python -m compileall src scripts",
    "Validate core Python imports",
    "python scripts/verify_docker_setup.py",
    "python scripts/verify_ci_setup.py",
    "docker build -t ecommerce-retail-api .",
    "workflow_dispatch",
    "Confirm large local database is not tracked",
]

EXPECTED_README_CONTENT = [
    "GitHub Actions CI Pipeline",
    ".github/workflows/ci.yml",
    "python -m compileall src scripts",
    "docker build -t ecommerce-retail-api .",
    "does not commit the local SQLite database",
]

EXPECTED_ARCHITECTURE_CONTENT = [
    "CI Pipeline Architecture",
    "GitHub Actions",
    "Build Docker image",
    "database-independent CI",
]

EXPECTED_GOVERNANCE_CONTENT = [
    "CI Governance",
    "Continuous Integration",
    "large local SQLite database",
    "Continuous Deployment",
]

EXPECTED_DATA_DICTIONARY_CONTENT = [
    "CI/CD-Related Files",
    ".github/workflows/ci.yml",
    "CI Workflow",
    "CI setup verification report",
]

EXPECTED_SETUP_GUIDE_CONTENT = [
    "Setup Guide",
    "Running the API with Docker",
    "Running CI Checks Locally",
    "GitHub Actions CI Workflow",
    "python scripts\\verify_ci_setup.py",
    "docker build -t ecommerce-retail-api .",
    "retail_intelligence.db",
]

EXPECTED_GITIGNORE_CONTENT = [
    "retail_intelligence.db",
    "*.db",
]

FORBIDDEN_CI_WORKFLOW_CONTENT = [
    "pytest tests -v",
    "COPY retail_intelligence.db",
]


def read_file(relative_path: str) -> str:
    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():
        return ""

    return file_path.read_text(encoding="utf-8")


def file_contains(relative_path: str, text: str) -> bool:
    return text in read_file(relative_path)


def file_does_not_contain(relative_path: str, text: str) -> bool:
    return text not in read_file(relative_path)


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

    for text in EXPECTED_CI_WORKFLOW_CONTENT:
        results.append(
            {
                "check_type": "ci_workflow_content",
                "item": text,
                "passed": file_contains(".github/workflows/ci.yml", text),
            }
        )

    for text in FORBIDDEN_CI_WORKFLOW_CONTENT:
        results.append(
            {
                "check_type": "ci_workflow_forbidden_content",
                "item": text,
                "passed": file_does_not_contain(".github/workflows/ci.yml", text),
            }
        )

    for text in EXPECTED_README_CONTENT:
        results.append(
            {
                "check_type": "readme_content",
                "item": text,
                "passed": file_contains("README.md", text),
            }
        )

    for text in EXPECTED_ARCHITECTURE_CONTENT:
        results.append(
            {
                "check_type": "architecture_content",
                "item": text,
                "passed": file_contains("docs/architecture.md", text),
            }
        )

    for text in EXPECTED_GOVERNANCE_CONTENT:
        results.append(
            {
                "check_type": "governance_content",
                "item": text,
                "passed": file_contains("docs/data_governance.md", text),
            }
        )

    for text in EXPECTED_DATA_DICTIONARY_CONTENT:
        results.append(
            {
                "check_type": "data_dictionary_content",
                "item": text,
                "passed": file_contains("docs/data_dictionary.md", text),
            }
        )

    for text in EXPECTED_SETUP_GUIDE_CONTENT:
        results.append(
            {
                "check_type": "setup_guide_content",
                "item": text,
                "passed": file_contains("docs/setup_guide.md", text),
            }
        )

    for text in EXPECTED_GITIGNORE_CONTENT:
        results.append(
            {
                "check_type": "gitignore_content",
                "item": text,
                "passed": file_contains(".gitignore", text),
            }
        )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "ci_setup_verification_report.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if failed_checks.empty:
        print("\nCI setup verification passed.")
    else:
        print("\nSome CI setup checks failed:")
        print(failed_checks[["check_type", "item"]])


if __name__ == "__main__":
    main()