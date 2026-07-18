from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


EXPECTED_PIPELINE_OUTPUTS = [
    "retail_intelligence.db",
    "data/processed/raw_database_verification_report.csv",
    "data/processed/dbt_model_verification_report.csv",
    "data/processed/api_logging_health_verification_report.csv",
    "data/processed/ai_business_insights.json",
    "data/processed/llm_context_summary.json",
    "data/powerbi_exports/powerbi_export_summary.csv",
]


def test_important_pipeline_outputs_exist():
    missing_outputs = [
        output_path
        for output_path in EXPECTED_PIPELINE_OUTPUTS
        if not (PROJECT_ROOT / output_path).exists()
    ]

    assert missing_outputs == []