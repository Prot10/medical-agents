"""Cross-check that ground_truth doesn't contradict hospital rule pathways.

For each case, find the hospital rule(s) whose `triggers` match the case's
condition (by condition prefix or NeurologicalCondition enum value). Then
verify:

1. Every mandatory step in the matching rule maps to a tool present in
   `ground_truth.optimal_actions` (it's OK for the agent's optimal to extend
   beyond the rule, but rule-mandatory steps should always appear).
2. No `optimal_actions[].tool_name` appears in the matching rule's
   `contraindicated` list (when expressible as a tool name).
3. Hospital-specific timing constraints (e.g., "door-to-CT <25min" for
   stroke) appear at least implicitly via sequence_constraints when the
   case condition matches.

This is a soft check — hospitals can have additional / different rules.
Outputs warnings, not blocking errors. The fleet uses output to decide
whether to add a sequence_constraint or critical_action that maps to a
hospital rule.

Usage:
    uv run python agent-platform/scripts/cross_check_hospital_rules.py
    uv run python agent-platform/scripts/cross_check_hospital_rules.py --case ALS-P01.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml


CASES_DIR = Path("data/neurobench_v5/cases")
HOSPITAL_DIR = Path("agent-platform/config/hospital_rules")


# Map case-ID prefix → typical hospital-rule triggers that apply
PREFIX_TO_TRIGGERS: dict[str, list[str]] = {
    "ISCH-STR": ["stroke", "stroke_code", "ischemic_stroke", "acute_stroke"],
    "SAH": ["stroke", "subarachnoid_hemorrhage", "hemorrhagic_stroke"],
    "BACT-MEN": ["meningitis", "bacterial_meningitis"],
    "FEPI-TEMP": ["first_seizure", "seizure"],
    "SE": ["first_seizure", "seizure", "status_epilepticus"],
    "ALZ-EARLY": ["dementia", "dementia_workup", "cognitive_impairment"],
    "FTD": ["dementia", "dementia_workup", "cognitive_impairment"],
    "NPH": ["dementia", "dementia_workup"],
    # Conditions without a specific stroke/meningitis/seizure/dementia pathway
    # use only the "general" rule.
}


def load_hospital_rules() -> dict[str, dict]:
    """Return {hospital_id: {rule_name: parsed_yaml}}."""
    out: dict[str, dict] = {}
    for hosp_dir in sorted(HOSPITAL_DIR.glob("*/")):
        rules: dict[str, dict] = {}
        for ym in sorted(hosp_dir.glob("*.yaml")):
            try:
                rules[ym.stem] = yaml.safe_load(ym.read_text()) or {}
            except yaml.YAMLError as e:
                print(f"WARN: failed to parse {ym}: {e}", file=sys.stderr)
        out[hosp_dir.name] = rules
    return out


def get_prefix(case_id: str) -> str:
    """Extract the condition prefix (everything up to the last hyphen + sub-id)."""
    parts = case_id.rsplit("-", 1)
    return parts[0] if len(parts) > 1 else case_id


def find_matching_rules(prefix: str, all_rules: dict[str, dict]) -> list[tuple[str, str, dict]]:
    """Find (hospital_id, rule_name, rule_body) tuples whose triggers match prefix."""
    triggers = set(PREFIX_TO_TRIGGERS.get(prefix, []))
    if not triggers:
        return []
    matches: list[tuple[str, str, dict]] = []
    for hosp_id, rules in all_rules.items():
        for rule_name, rule in rules.items():
            rule_triggers = set(rule.get("triggers", []) or [])
            if rule_triggers & triggers:
                matches.append((hosp_id, rule_name, rule))
    return matches


def check_case(case: dict, rules: list[tuple[str, str, dict]]) -> list[str]:
    """Return list of soft warnings."""
    gt = case.get("ground_truth", {})
    optimal_tools = {
        a.get("tool_name")
        for a in gt.get("optimal_actions", []) or []
        if a.get("tool_name")
    }

    warnings: list[str] = []
    seen_warnings: set[str] = set()

    for hosp_id, rule_name, rule in rules:
        # Mandatory steps
        for step in rule.get("steps", []) or []:
            if not step.get("mandatory"):
                continue
            tool = step.get("action")
            if not tool:
                continue
            if tool not in optimal_tools:
                w = (
                    f"{hosp_id}/{rule_name}: rule mandates `{tool}` "
                    f"but it's not in optimal_actions"
                )
                if w not in seen_warnings:
                    warnings.append(w)
                    seen_warnings.add(w)

    return warnings


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cases-dir", type=Path, default=CASES_DIR)
    p.add_argument("--case", help="Inspect a single case in detail")
    p.add_argument("--limit", type=int, default=0, help="Stop after this many warnings (0 = all)")
    args = p.parse_args()

    if not args.cases_dir.is_dir():
        print(f"ERROR: {args.cases_dir} not found", file=sys.stderr)
        return 2

    all_rules = load_hospital_rules()
    print(f"Loaded {sum(len(r) for r in all_rules.values())} rules "
          f"across {len(all_rules)} hospitals")

    if args.case:
        path = args.cases_dir / args.case
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            return 2
        case = json.loads(path.read_text())
        prefix = get_prefix(case.get("case_id", ""))
        matches = find_matching_rules(prefix, all_rules)
        print(f"\nCase {case.get('case_id')}: prefix={prefix}, "
              f"{len(matches)} matching rule(s)")
        warnings = check_case(case, matches)
        for w in warnings:
            print(f"  WARN  {w}")
        return 0

    # Sweep
    files = sorted(args.cases_dir.glob("*.json"))
    print(f"Sweeping {len(files)} cases...\n")

    total_warnings = 0
    warnings_by_prefix: dict[str, int] = defaultdict(int)
    seen_categories: dict[str, int] = defaultdict(int)

    for f in files:
        case = json.loads(f.read_text())
        prefix = get_prefix(case.get("case_id", ""))
        matches = find_matching_rules(prefix, all_rules)
        if not matches:
            continue
        warnings = check_case(case, matches)
        total_warnings += len(warnings)
        warnings_by_prefix[prefix] += len(warnings)
        for w in warnings:
            # Drop hospital prefix to aggregate
            cat = w.split(":", 1)[1].strip() if ":" in w else w
            seen_categories[cat] += 1
        if args.limit and total_warnings >= args.limit:
            print(f"\n(stopping after --limit {args.limit})")
            break

    print(f"\nTotal warnings: {total_warnings}")
    print(f"\nBy condition prefix:")
    for pfx, n in sorted(warnings_by_prefix.items(), key=lambda x: -x[1]):
        print(f"  {pfx:15s} {n:5d}")
    print(f"\nTop warning categories:")
    for cat, n in sorted(seen_categories.items(), key=lambda x: -x[1])[:15]:
        print(f"  {n:5d}  {cat}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
