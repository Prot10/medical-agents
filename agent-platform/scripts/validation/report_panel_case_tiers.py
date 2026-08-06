"""Report where the per-condition panel and the individual cases disagree about a tool's tier.

`dataset-generation/config/conditions.yaml` lists, per condition, the modalities a workup is
expected to use and which are required. Those lists are a **generation input**, not a per-case
contract: a case may legitimately require a tool the panel calls optional (a mimic whose
differential turns on it), and may legitimately omit one the panel calls required (an
intercurrent reason not to do it). `validate_cases.py` therefore does not gate on the
difference, and should not.

But nothing surfaced it either, and that is how a real contradiction survived. The clinical
reviewers lowered laboratory studies to OPTIONAL in cardiac syncope; the panel was updated and
all 30 cases still required it, 28 of them behind a `hard` sequence constraint that made
*skipping* an untargeted panel a scored violation. The panel said one thing, the cases another,
and no gate compared them.

So this reports. Read it after a tier change or a batch of new cases, and decide case by case.

Usage:
    uv run python agent-platform/scripts/validation/report_panel_case_tiers.py
    uv run python agent-platform/scripts/validation/report_panel_case_tiers.py --json report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_cases import CASES_DIR  # noqa: E402

from neuroagent.review_api.services.tool_catalog import (  # noqa: E402
    _CONDITION_ALIAS,
    _MODALITY_TO_TOOL,
)

CONDITIONS_YAML = Path("dataset-generation/config/conditions.yaml")


def _tools(tokens: list[str] | None) -> set[str]:
    return {_MODALITY_TO_TOOL[t] for t in tokens or [] if t in _MODALITY_TO_TOOL}


def build_report(cases_dir: Path, conditions_path: Path) -> dict:
    import yaml

    spec = yaml.safe_load(conditions_path.read_text())
    missing: dict[str, Counter] = defaultdict(Counter)
    surplus: dict[str, Counter] = defaultdict(Counter)
    unknown: Counter = Counter()

    for path in sorted(cases_dir.glob("*.json")):
        case = json.loads(path.read_text())
        condition = case["condition"]
        entry = spec.get(_CONDITION_ALIAS.get(condition, condition))
        if entry is None:
            unknown[condition] += 1
            continue
        required = _tools(entry.get("required_modalities"))
        optional = _tools(entry.get("optional_modalities"))
        tiers: dict[str, set[str]] = defaultdict(set)
        for action in case["ground_truth"]["optimal_actions"]:
            if action.get("tool_name"):
                tiers[action["tool_name"]].add(action["category"])
        for tool in sorted(required):
            if "required" not in tiers.get(tool, set()):
                missing[condition][tool] += 1
        for tool in sorted(optional):
            if "required" in tiers.get(tool, set()):
                surplus[condition][tool] += 1

    return {
        "required_by_panel_not_by_case": {c: dict(v) for c, v in missing.items() if v},
        "optional_by_panel_required_by_case": {c: dict(v) for c, v in surplus.items() if v},
        "conditions_with_no_panel": dict(unknown),
        "totals": {
            "required_by_panel_not_by_case": sum(sum(v.values()) for v in missing.values()),
            "optional_by_panel_required_by_case": sum(sum(v.values()) for v in surplus.values()),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cases-dir", type=Path, default=CASES_DIR)
    parser.add_argument("--conditions", type=Path, default=CONDITIONS_YAML)
    parser.add_argument("--json", type=Path, help="write the report as JSON")
    args = parser.parse_args()

    report = build_report(args.cases_dir, args.conditions)
    totals = report["totals"]
    print(
        f"{totals['required_by_panel_not_by_case']} case actions absent though the panel marks "
        f"the tool required"
    )
    for condition, tools in sorted(report["required_by_panel_not_by_case"].items()):
        print(f"  {condition:32} {tools}")
    print(
        f"\n{totals['optional_by_panel_required_by_case']} case actions required though the "
        f"panel marks the tool optional"
    )
    for condition, tools in sorted(report["optional_by_panel_required_by_case"].items()):
        print(f"  {condition:32} {tools}")
    if report["conditions_with_no_panel"]:
        print(f"\nconditions with no panel entry: {report['conditions_with_no_panel']}")
    print(
        "\nNeither number is an error by itself — the panel lists are a generation input, not a "
        "per-case contract. Read them after a tier change: a jump means the two have drifted."
    )
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n")
        print(f"\nwritten to {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
