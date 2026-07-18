from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    "Dockerfile",
    ".dockerignore",
    "docker/README.md",
    "README.md",
    "docs/architecture.md",
    "docs/data_governance.md",
    "docs/data_dictionary.md",
    "docs/setup_guide.md",
    "requirements.txt",
]

EXPECTED_DOCKERFILE_CONTENT = [
    "FROM python:3.10-slim",
    "WORKDIR /app",
    "COPY requirements.txt",
    "pip install",
    "COPY src ./src",
    "EXPOSE 8000",
    "uvicorn",
    "src.api.main:app",
]

FORBIDDEN_DOCKERFILE_CONTENT = [
    "COPY retail_intelligence.db",
]

EXPECTED_DOCKERIGNORE_CONTENT = [
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".env",
    "dbt_retail/target",
    "dbt_retail/logs",
    "dbt_retail/.dbt",
    "retail_intelligence.db",
    "*.db",
]

EXPECTED_DOCKER_README_CONTENT = [
    "Docker Setup",
    "Build Docker Image",
    "Run Docker Container with SQLite Volume Mount",
    "API Authentication",
    "Troubleshooting",
    "Interview Explanation",
    "mounted into the container at runtime",
]

EXPECTED_MAIN_README_CONTENT = [
    "Docker Containerisation",
    "docker/README.md",
    "docker build -t ecommerce-retail-api .",
    "retail_intelligence.db` is mounted into the container at runtime",
]

EXPECTED_ARCHITECTURE_CONTENT = [
    "Docker Containerisation Layer",
    "Docker image",
    "Docker container",
    "SQLite database mounted at runtime",
]

EXPECTED_GOVERNANCE_CONTENT = [
    "Docker and Deployment Governance",
    "mounted into the container at runtime",
    "Azure Key Vault",
    "Azure SQL Database",
]

EXPECTED_DATA_DICTIONARY_CONTENT = [
    "Docker-Related Files",
    "SQLite database is mounted at runtime",
    "Docker Runtime Data Source",
]

EXPECTED_SETUP_GUIDE_CONTENT = [
    "Setup Guide",
    "Running the API with Docker",
    "docker build -t ecommerce-retail-api .",
    "docker run --name ecommerce-retail-api-container",
    "-v ${PWD}\\retail_intelligence.db:/app/retail_intelligence.db",
    "retail_intelligence.db",
    "docker/README.md",
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

    for text in EXPECTED_DOCKERFILE_CONTENT:
        results.append(
            {
                "check_type": "dockerfile_content",
                "item": text,
                "passed": file_contains("Dockerfile", text),
            }
        )

    for text in FORBIDDEN_DOCKERFILE_CONTENT:
        results.append(
            {
                "check_type": "dockerfile_forbidden_content",
                "item": text,
                "passed": file_does_not_contain("Dockerfile", text),
            }
        )

    for text in EXPECTED_DOCKERIGNORE_CONTENT:
        results.append(
            {
                "check_type": "dockerignore_content",
                "item": text,
                "passed": file_contains(".dockerignore", text),
            }
        )

    for text in EXPECTED_DOCKER_README_CONTENT:
        results.append(
            {
                "check_type": "docker_readme_content",
                "item": text,
                "passed": file_contains("docker/README.md", text),
            }
        )

    for text in EXPECTED_MAIN_README_CONTENT:
        results.append(
            {
                "check_type": "main_readme_content",
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

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "docker_setup_verification_report.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if failed_checks.empty:
        print("\nDocker setup verification passed.")
    else:
        print("\nSome Docker setup checks failed:")
        print(failed_checks[["check_type", "item"]])


if __name__ == "__main__":
    main()