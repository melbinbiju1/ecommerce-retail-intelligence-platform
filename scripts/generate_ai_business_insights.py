from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.ai_assistant.business_insights import (
    generate_executive_summary,
    generate_sales_performance_summary,
    generate_operational_risk_summary,
    generate_recommendations,
    insight_to_dict,
)


def main() -> None:
    output_dir = PROJECT_ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    insights = {
        "executive_summary": insight_to_dict(generate_executive_summary()),
        "sales_performance": insight_to_dict(generate_sales_performance_summary()),
        "operational_risk": insight_to_dict(generate_operational_risk_summary()),
        "recommendations": insight_to_dict(generate_recommendations()),
    }

    output_path = output_dir / "ai_business_insights.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(insights, file, indent=2)

    print(f"AI-ready business insights saved to: {output_path}")


if __name__ == "__main__":
    main()