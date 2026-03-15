"""Build a generation prompt for a NeuroBench case seeded from a real case report.

Reads a seed case (from MedCaseReasoning), the condition YAML, exports the
JSON schema from Pydantic models, and assembles the final prompt.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

from neuroagent_schemas.case import NeuroBenchCase


def load_conditions(config_path: str | Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_json_schema() -> str:
    schema = NeuroBenchCase.model_json_schema()
    return json.dumps(schema, indent=2)


def build_prompt_seeded(
    seed_path: str | Path,
    condition_key: str,
    difficulty: str,
    case_id: str,
    conditions_path: str | Path,
    template_path: str | Path,
) -> str:
    """Assemble the full prompt for generating a seeded NeuroBench case."""
    # Load seed case
    with open(seed_path) as f:
        seed = json.load(f)

    # Load condition specs
    conditions = load_conditions(conditions_path)
    if condition_key not in conditions:
        available = ", ".join(conditions.keys())
        raise ValueError(f"Unknown condition '{condition_key}'. Available: {available}")

    condition = conditions[condition_key]
    json_schema = get_json_schema()
    condition_yaml = yaml.dump({condition_key: condition}, default_flow_style=False)

    with open(template_path) as f:
        template = f.read()

    prompt = template.format(
        json_schema=json_schema,
        condition_yaml=condition_yaml,
        case_id=case_id,
        condition_name=condition["name"],
        difficulty=difficulty,
        encounter_type=condition["encounter_type"],
        source_pmcid=seed.get("pmcid", "unknown"),
        source_journal=seed.get("journal", "unknown"),
        source_diagnosis=seed.get("final_diagnosis", "unknown"),
        source_case_prompt=seed.get("case_prompt", ""),
        source_reasoning=seed.get("diagnostic_reasoning", ""),
    )

    return prompt


def main():
    """CLI: python build_prompt_seeded.py <seed_json> <condition> <difficulty> <case_id>"""
    if len(sys.argv) != 5:
        print("Usage: python build_prompt_seeded.py <seed_json> <condition_key> <difficulty> <case_id>")
        print("Example: python build_prompt_seeded.py /tmp/seed.json ischemic_stroke straightforward ISCH-STR-RS01")
        sys.exit(1)

    seed_path = sys.argv[1]
    condition_key = sys.argv[2]
    difficulty = sys.argv[3]
    case_id = sys.argv[4]

    base_dir = Path(__file__).resolve().parent.parent.parent
    conditions_path = base_dir / "config" / "conditions.yaml"
    template_path = base_dir / "config" / "prompt_template_seeded.md"

    prompt = build_prompt_seeded(
        seed_path, condition_key, difficulty, case_id,
        conditions_path, template_path,
    )
    print(prompt)


if __name__ == "__main__":
    main()
