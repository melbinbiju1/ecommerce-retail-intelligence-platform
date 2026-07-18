from pathlib import Path
import json
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    "src/ai_assistant/__init__.py",
    "src/ai_assistant/business_insights.py",
    "src/ai_assistant/llm_context.py",
    "src/api/routes/insights.py",
    "scripts/generate_ai_business_insights.py",
    "scripts/generate_llm_context.py",
    "data/processed/ai_business_insights.json",
    "data/processed/llm_context_summary.json",
]

EXPECTED_INSIGHT_SECTIONS = [
    "executive_summary",
    "sales_performance",
    "operational_risk",
    "recommendations",
]

EXPECTED_LLM_CONTEXT_KEYS = [
    "context_name",
    "purpose",
    "data_governance_note",
    "trusted_source_views",
    "executive_summary",
    "recent_monthly_sales",
    "operational_alert_summary",
    "top_operational_alert_types",
    "sample_high_risk_sellers",
    "sample_high_risk_categories",
    "suggested_llm_tasks",
    "suggested_system_prompt",
]

EXPECTED_ENDPOINT_FUNCTIONS = [
    "get_ai_executive_summary",
    "get_ai_sales_performance",
    "get_ai_operational_risk",
    "get_ai_recommendations",
    "get_llm_context",
]


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

    insights_path = PROJECT_ROOT / "data" / "processed" / "ai_business_insights.json"

    if insights_path.exists():
        with open(insights_path, "r", encoding="utf-8") as file:
            insights = json.load(file)

        for section in EXPECTED_INSIGHT_SECTIONS:
            results.append(
                {
                    "check_type": "insight_section_exists",
                    "item": section,
                    "passed": section in insights,
                }
            )

    llm_context_path = PROJECT_ROOT / "data" / "processed" / "llm_context_summary.json"

    if llm_context_path.exists():
        with open(llm_context_path, "r", encoding="utf-8") as file:
            llm_context = json.load(file)

        for key in EXPECTED_LLM_CONTEXT_KEYS:
            results.append(
                {
                    "check_type": "llm_context_key_exists",
                    "item": key,
                    "passed": key in llm_context,
                }
            )

    main_api_file = PROJECT_ROOT / "src" / "api" / "main.py"
    insights_route_file = PROJECT_ROOT / "src" / "api" / "routes" / "insights.py"

    results.append(
        {
            "check_type": "api_route_registered",
            "item": "insights_router",
            "passed": main_api_file.exists()
            and "insights_router" in main_api_file.read_text(encoding="utf-8"),
        }
    )

    route_text = (
        insights_route_file.read_text(encoding="utf-8")
        if insights_route_file.exists()
        else ""
    )

    for function_name in EXPECTED_ENDPOINT_FUNCTIONS:
        results.append(
            {
                "check_type": "endpoint_function_exists",
                "item": function_name,
                "passed": function_name in route_text,
            }
        )

    results.append(
        {
            "check_type": "llm_context_admin_only",
            "item": "require_roles([\"admin\"])",
            "passed": 'require_roles(["admin"])' in route_text,
        }
    )

    results_df = pd.DataFrame(results)
    print(results_df)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "ai_business_insights_verification_report.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    failed_checks = results_df[results_df["passed"] == False]

    print(f"\nVerification report saved to: {output_path}")

    if failed_checks.empty:
        print("\nAI-ready business insights verification passed.")
    else:
        print("\nSome AI-ready business insights checks failed:")
        print(failed_checks[["check_type", "item"]])


if __name__ == "__main__":
    main()