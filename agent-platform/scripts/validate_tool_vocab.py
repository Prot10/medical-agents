"""Validate that all tool_parameters in v5 cases come from the closed vocabulary.

Reads `dataset-generation/TOOL_PARAMETER_VOCABULARY.md` (the source of truth)
and `agent-platform/config/tools/costs.yaml` (the cost-lookup table) and checks
every case file for:

- `optimal_actions[].tool_parameters` values matching the vocab when the
  tool is `order_specialized_test` or `order_advanced_imaging`.
- `useless_tools[].tool_parameters` and `harmful_tools[].tool_parameters` ditto.
- That every catchall tool_parameters value has a corresponding cost entry.

Used as a pre-fleet sanity check AND as a post-fleet acceptance gate.

Usage:
    uv run python agent-platform/scripts/validate_tool_vocab.py
    uv run python agent-platform/scripts/validate_tool_vocab.py --cases-dir data/neurobench_v5/cases
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

CASES_DIR = Path("data/neurobench_v5/cases")
COSTS_YAML = Path("agent-platform/config/tools/costs.yaml")

CATCHALL_TOOLS = {"order_specialized_test", "order_advanced_imaging"}


def load_vocab() -> tuple[set[str], set[str], set[str]]:
    """Return (specialized_test_keys, advanced_imaging_modalities, genetic_panels)."""
    with open(COSTS_YAML) as f:
        cfg = yaml.safe_load(f)
    tools = cfg.get("tools", {})

    spec = set((tools.get("order_specialized_test", {}).get("by_type") or {}).keys())
    panels = set(
        (tools.get("order_specialized_test", {}).get("genetic_panels") or {}).keys()
    )
    adv = set((tools.get("order_advanced_imaging", {}).get("by_type") or {}).keys())
    return spec, adv, panels


def check_param_value(
    tool_name: str,
    params: dict,
    spec_vocab: set[str],
    adv_vocab: set[str],
    panel_vocab: set[str],
) -> str | None:
    """Return an error string if params violate the vocab, None otherwise."""
    if tool_name == "order_specialized_test":
        val = params.get("test_type")
        if val is None:
            return None  # parameters not specified — allowed
        if isinstance(val, str) and val.startswith("genetic_panel:"):
            panel = val.split(":", 1)[1]
            if panel not in panel_vocab:
                return f"unknown genetic_panel '{panel}' (not in {sorted(panel_vocab)})"
            return None
        if val not in spec_vocab:
            return f"unknown test_type '{val}' (not in specialized_test vocab)"

    elif tool_name == "order_advanced_imaging":
        val = params.get("modality")
        if val is None:
            return None
        if val not in adv_vocab:
            return f"unknown modality '{val}' (not in advanced_imaging vocab)"

    return None


def validate_case(
    path: Path,
    spec_vocab: set[str],
    adv_vocab: set[str],
    panel_vocab: set[str],
) -> list[str]:
    issues: list[str] = []
    case = json.loads(path.read_text())
    gt = case.get("ground_truth", {})

    sections = [
        ("optimal_actions", "tool_name", "tool_parameters"),
        ("useless_tools", "tool_name", "tool_parameters"),
        ("harmful_tools", "tool_name", "tool_parameters"),
    ]
    for section, tn_key, tp_key in sections:
        for i, entry in enumerate(gt.get(section, []) or []):
            tn = entry.get(tn_key)
            if tn not in CATCHALL_TOOLS:
                continue
            tp = entry.get(tp_key) or {}
            err = check_param_value(tn, tp, spec_vocab, adv_vocab, panel_vocab)
            if err:
                issues.append(f"{section}[{i}] {tn}: {err}")
    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cases-dir", type=Path, default=CASES_DIR)
    args = p.parse_args()

    if not args.cases_dir.is_dir():
        print(f"ERROR: {args.cases_dir} not found", file=sys.stderr)
        return 2

    spec, adv, panels = load_vocab()
    print(f"Loaded vocab:")
    print(f"  specialized_test ({len(spec)}): {sorted(spec)}")
    print(f"  advanced_imaging ({len(adv)}): {sorted(adv)}")
    print(f"  genetic_panels   ({len(panels)}): {sorted(panels)}")

    files = sorted(args.cases_dir.glob("*.json"))
    print(f"\nValidating {len(files)} cases in {args.cases_dir}...")

    total_issues = 0
    failing_cases: list[str] = []
    issue_summary: Counter[str] = Counter()
    for f in files:
        issues = validate_case(f, spec, adv, panels)
        if issues:
            failing_cases.append(f.name)
            total_issues += len(issues)
            for iss in issues:
                # Aggregate first portion of issue as category
                cat = iss.split(":", 1)[1].strip() if ":" in iss else iss
                issue_summary[cat[:80]] += 1

    print(f"\n{len(files) - len(failing_cases)}/{len(files)} cases pass vocab check")
    if failing_cases:
        print(f"  Total issues: {total_issues}")
        print(f"  Top issue categories:")
        for cat, count in issue_summary.most_common(10):
            print(f"    {count:4d}  {cat}")
        # Show first 5 failing cases in detail
        print(f"\nFirst few failing cases:")
        for name in failing_cases[:5]:
            f = args.cases_dir / name
            issues = validate_case(f, spec, adv, panels)
            print(f"  {name}:")
            for iss in issues[:3]:
                print(f"    - {iss}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
