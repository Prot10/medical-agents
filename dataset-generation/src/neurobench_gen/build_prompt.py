"""Build a complete generation prompt for a single NeuroBench case.

Reads the condition YAML, exports the JSON schema from Pydantic models,
and assembles the final prompt that gets passed to `claude -p`.
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
    """Export the NeuroBenchCase Pydantic model as JSON Schema."""
    schema = NeuroBenchCase.model_json_schema()
    return json.dumps(schema, indent=2)


def build_prompt(
    condition_key: str,
    difficulty: str,
    case_id: str,
    conditions_path: str | Path,
    template_path: str | Path,
) -> str:
    """Assemble the full prompt for generating one NeuroBench case."""
    conditions = load_conditions(conditions_path)

    if condition_key not in conditions:
        available = ", ".join(conditions.keys())
        raise ValueError(f"Unknown condition '{condition_key}'. Available: {available}")

    condition = conditions[condition_key]
    json_schema = get_json_schema()

    # Extract the relevant subset of the condition YAML for this difficulty
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
    )

    return prompt


def main():
    """CLI entry point: python build_prompt.py <condition> <difficulty> <case_id>"""
    if len(sys.argv) != 4:
        print("Usage: python build_prompt.py <condition_key> <difficulty> <case_id>")
        print("Example: python build_prompt.py focal_epilepsy_temporal straightforward FEPI-TEMP-S01")
        sys.exit(1)

    condition_key = sys.argv[1]
    difficulty = sys.argv[2]
    case_id = sys.argv[3]

    # Resolve paths relative to this file's location
    base_dir = Path(__file__).resolve().parent.parent.parent
    conditions_path = base_dir / "config" / "conditions.yaml"
    template_path = base_dir / "config" / "prompt_template.md"

    prompt = build_prompt(condition_key, difficulty, case_id, conditions_path, template_path)
    print(prompt)


if __name__ == "__main__":
    main()
