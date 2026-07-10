"""Apply the deterministic half of the NeuroBench case migration.

Everything here is a 1:1 mapping that needs no clinical judgment, so it belongs in an
auditable script rather than in an LLM. Whatever survives this pass is, by construction,
a question a clinician has to answer — see `validate_cases.py --json` for the manifest.

Four operations, all idempotent:

1. `consult_medical_specialist` steps lose their `tool_name` (set to null) and their
   orphaned `tool_parameters`. The tool was deliberately removed in `64d4091`; the step is
   still a real clinical action and its `action` prose already names the specialty, so the
   step survives — only its (impossible) tool call goes. `metrics.py` skips tool-less steps,
   so `action_recall` and `required_coverage` stop being capped below 1.0.
2. Sequence constraints ordering that removed tool are dropped: a constraint on a tool that
   cannot be called can be neither satisfied nor violated.
3. Parameter keys that spell one concept several ways collapse onto the schema's name
   (`proposed_drug` / `proposed_medication` / `proposed` -> `drug`, and so on).
4. Off-enum values with an unambiguous canonical form are rewritten (`MS_protocol` -> `ms`).

Usage:
    uv run python agent-platform/scripts/validation/migrate_cases.py --dry-run
    uv run python agent-platform/scripts/validation/migrate_cases.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_cases import (  # noqa: E402
    CASES_DIR,
    REMOVED_TOOLS,
    RENAMABLE_KEYS,
    RENAMABLE_VALUES,
)

# Keys whose schema counterpart is a list while the case stores a scalar.
LIST_VALUED_TARGETS = {("analyze_brain_mri", "sequences")}

GT_TOOL_SECTIONS = ("optimal_actions", "useless_tools", "harmful_tools")

# `analyze_csf.tests` conflates two different things. `costs.yaml` prices the LP procedure
# together with "cell count, protein, glucose" in `analyze_csf.base`, and charges separately
# per entry in `special_tests`. Leaving the basics in `special_tests` bills them a second
# time at `default_test`. So the list is split, not renamed.
CSF_BASIC_TESTS = {
    "cell count", "cell_count", "cells", "protein", "glucose",
    "gram_stain", "culture", "routine",
}
# Spelling variants of rows that already exist in costs.yaml::analyze_csf.by_special_test.
CSF_SPECIAL_ALIASES = {
    "oligoclonal bands": "oligoclonal_bands",
    "14-3-3": "14_3_3_protein",
    "RT-QuIC": "RT_QuIC",
    "ACE": "ACE_CSF",
}


def _split_csf_tests(params: dict[str, Any], stats: Counter) -> dict[str, Any]:
    """Move billable assays into `special_tests`; keep the always-done panel in `basic`."""
    if "tests" not in params:
        return params

    out = dict(params)
    raw = out.pop("tests") or []
    basic = list(out.get("basic") or [])
    special = list(out.get("special_tests") or [])

    for test in raw:
        if test in CSF_BASIC_TESTS:
            if test not in basic:
                basic.append(test)
            stats[f"csf_test_basic:{test}"] += 1
        else:
            canonical = CSF_SPECIAL_ALIASES.get(test, test)
            if canonical != test:
                stats[f"csf_test_alias:{test}->{canonical}"] += 1
            if canonical not in special:
                special.append(canonical)

    if basic:
        out["basic"] = basic
    if special:
        out["special_tests"] = special
    stats["csf_tests_split"] += 1
    return out


def _migrate_parameters(tool: str, params: dict[str, Any], stats: Counter) -> dict[str, Any]:
    """Rename keys onto the schema's spelling and rewrite unambiguous off-enum values."""
    migrated: dict[str, Any] = {}
    for key, value in params.items():
        target = RENAMABLE_KEYS.get((tool, key), key)
        if target != key:
            stats[f"param_key:{tool}.{key}->{target}"] += 1
        if (tool, target) in LIST_VALUED_TARGETS and not isinstance(value, list):
            value = [value]
            stats[f"param_wrap_list:{tool}.{target}"] += 1

        canonical = RENAMABLE_VALUES.get((tool, target, str(value)))
        if canonical is not None:
            stats[f"param_value:{tool}.{target}={value}->{canonical}"] += 1
            value = canonical

        if target in migrated and migrated[target] != value:
            # Two source keys collapsing onto one target with different values would lose
            # data silently. Never seen in practice; fail loudly if the data changes.
            raise ValueError(
                f"{tool}: `{key}` -> `{target}` collides with an existing value "
                f"({migrated[target]!r} vs {value!r})"
            )
        migrated[target] = value
    return migrated


def migrate_case(case: dict[str, Any], stats: Counter) -> bool:
    """Mutate `case` in place. Returns True if anything changed."""
    before = json.dumps(case, sort_keys=True)
    gt = case.get("ground_truth") or {}

    for section in GT_TOOL_SECTIONS:
        for entry in gt.get(section) or []:
            tool = entry.get("tool_name")
            if not tool:
                continue

            if tool in REMOVED_TOOLS:
                if section == "optimal_actions":
                    # The clinical step stays; only its impossible tool call is removed.
                    entry["tool_name"] = None
                    entry["tool_parameters"] = {}
                    stats[f"tool_removed:{section}.{tool}"] += 1
                else:
                    # A removed tool cannot be called, so it cannot be useless or harmful.
                    entry["_drop"] = True
                    stats[f"tool_removed_dropped:{section}.{tool}"] += 1
                continue

            params = entry.get("tool_parameters")
            if params:
                if tool == "analyze_csf":
                    params = _split_csf_tests(params, stats)
                entry["tool_parameters"] = _migrate_parameters(tool, params, stats)

        if any(e.get("_drop") for e in gt.get(section) or []):
            gt[section] = [e for e in gt[section] if not e.pop("_drop", False)]

    constraints = gt.get("sequence_constraints")
    if constraints:
        kept = [
            c for c in constraints
            if c.get("before") not in REMOVED_TOOLS and c.get("after") not in REMOVED_TOOLS
        ]
        if len(kept) != len(constraints):
            stats["sequence_constraint_dropped"] += len(constraints) - len(kept)
            gt["sequence_constraints"] = kept

    return json.dumps(case, sort_keys=True) != before


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic NeuroBench case migration")
    parser.add_argument("--cases-dir", default=str(CASES_DIR))
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    parser.add_argument("--report", default=None, help="Write the per-case change report here")
    args = parser.parse_args()

    files = sorted(Path(args.cases_dir).glob("*.json"))
    if not files:
        print(f"No cases under {args.cases_dir}", file=sys.stderr)
        return 2

    stats: Counter[str] = Counter()
    changed: list[str] = []

    for path in files:
        raw = path.read_text()
        case = json.loads(raw)
        case_stats: Counter[str] = Counter()
        if migrate_case(case, case_stats):
            changed.append(path.name)
            stats.update(case_stats)
            if not args.dry_run:
                # Match the corpus convention: 2-space indent, unicode kept, trailing newline.
                path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")

    verb = "would change" if args.dry_run else "changed"
    print(f"{verb} {len(changed)}/{len(files)} cases\n")
    print("Operations:")
    for key, n in sorted(stats.items(), key=lambda kv: -kv[1]):
        print(f"  {n:5d}  {key}")

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(
            json.dumps({"changed_cases": changed, "operations": dict(stats)}, indent=2)
        )
        print(f"\nReport -> {args.report}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
