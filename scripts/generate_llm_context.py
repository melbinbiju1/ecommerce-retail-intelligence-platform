from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.ai_assistant.llm_context import build_llm_context_summary


def main() -> None:
    output_dir = PROJECT_ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    context = build_llm_context_summary()

    output_path = output_dir / "llm_context_summary.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(context, file, indent=2)

    print(f"LLM-ready context summary saved to: {output_path}")


if __name__ == "__main__":
    main()