"""Cross-field coherence validator for the v5 gold-trajectory regen schema.

Runs after the fleet authors a case. Checks invariants that schema validation
cannot enforce, e.g.:

1. No tool appears in both `optimal_actions` AND `useless_tools` (contradiction).
2. No tool appears in both `optimal_actions` AND `harmful_tools` (contradiction).
3. Every tool in `optimal_actions[].tool_name` is in the 12-tool universe.
4. Every required tool has a corresponding `initial_tool_outputs` or
   `followup_outputs` entry (so calling it returns a meaningful result).
5. Every `useless_tools` entry has a `fallback_tool_outputs` entry (so the
   agent gets *something* back if it calls it — the off-pathway fallback).
6. SequenceConstraint `before` and `after` tool names are in the 12-tool universe.
7. RedHerring.field_path, when set, resolves to a real location in the case JSON.
8. critical_actions and contraindicated_actions are non-empty (a case without
   either is under-authored).
9. differential is sorted by likelihood descending (very_high → very_low).

Outputs per-case issue counts and a categorical summary. Used as the
acceptance gate: 0 issues required for a case to ship.

Usage:
    uv run python agent-platform/scripts/validate_ground_truth_coherence.py
    uv run python agent-platform/scripts/validate_ground_truth_coherence.py --strict
    uv run python agent-platform/scripts/validate_ground_truth_coherence.py --case ALS-P01.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


CASES_DIR = Path("data/neurobench_v5/cases")

# Canonical 12-tool universe + the specialist consultation tool
CANONICAL_TOOLS = {
    "analyze_brain_mri",
    "analyze_eeg",
    "analyze_ecg",
    "interpret_labs",
    "analyze_csf",
    "order_ct_scan",
    "order_echocardiogram",
    "order_cardiac_monitoring",
    "order_advanced_imaging",
    "order_specialized_test",
    "search_medical_literature",
    "check_drug_interactions",
    "consult_medical_specialist",
}

# Map tool_name → ToolOutputSet field name(s) where its output lives
TOOL_TO_OUTPUT_FIELD: dict[str, list[str]] = {
    "analyze_brain_mri": ["mri"],
    "analyze_eeg": ["eeg"],
    "analyze_ecg": ["ecg"],
    "interpret_labs": ["labs"],
    "analyze_csf": ["csf"],
    "order_ct_scan": ["ct"],
    "order_echocardiogram": ["echo"],
    "order_cardiac_monitoring": ["cardiac_monitoring"],
    "order_advanced_imaging": ["advanced_imaging"],
    "order_specialized_test": ["specialized_test"],
    "search_medical_literature": ["literature_search"],
    "check_drug_interactions": ["drug_interactions"],
    "consult_medical_specialist": [],  # no pre-generated output
}

LIKELIHOOD_ORDER = {
    "very_high": 0, "high": 1, "moderate": 2, "low": 3, "very_low": 4,
}


def _has_output(case: dict, tool_name: str) -> bool:
    """True if the case has a pre-generated output for this tool."""
    fields = TOOL_TO_OUTPUT_FIELD.get(tool_name, [])
    if not fields:
        return True  # consult_medical_specialist — synthesized at runtime
    initial = case.get("initial_tool_outputs", {}) or {}
    followup = case.get("followup_outputs", []) or []
    for f in fields:
        if initial.get(f):
            return True
    for fu in followup:
        if fu.get("tool_name") == tool_name and fu.get("output"):
            return True
    return False


def _has_fallback(case: dict, tool_name: str) -> bool:
    """True if the case has a fallback output for this tool."""
    fields = TOOL_TO_OUTPUT_FIELD.get(tool_name, [])
    if not fields:
        return True
    fallback = case.get("fallback_tool_outputs") or {}
    return any(fallback.get(f) for f in fields)


def _resolve_field_path(case: dict, path: str) -> bool:
    """Best-effort: resolve a dotted path with optional [i] indices."""
    if not path:
        return False
    cur: object = case
    # Tokenize: "initial_tool_outputs.labs.panels.metabolic[3]"
    parts = path.replace("]", "").replace("[", ".").split(".")
    for part in parts:
        if part == "":
            continue
        if part.isdigit() and isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except IndexError:
                return False
        elif isinstance(cur, dict):
            if part not in cur:
                return False
            cur = cur[part]
        else:
            return False
    return True


def _sig(tool_name: str | None, params: dict | None) -> tuple[str, str]:
    """Return a (tool_name, params_signature) tuple for dedup/intersection.

    Two entries are "the same tool" only if both name AND parameters match.
    Required for the catchall tools (`order_specialized_test`,
    `order_advanced_imaging`) where the same tool_name covers many distinct
    tests via tool_parameters. Without this, marking `FDG_PET` as required
    and `DaTscan` as useless triggers a bogus contradiction.
    """
    import json as _json

    name = tool_name or ""
    if not params:
        return (name, "")
    try:
        return (name, _json.dumps(params, sort_keys=True, default=str))
    except Exception:
        return (name, str(params))


def validate_case(case: dict) -> list[str]:
    issues: list[str] = []
    gt = case.get("ground_truth", {})

    optimal_entries = [
        (i, a.get("tool_name"), a.get("tool_parameters") or {})
        for i, a in enumerate(gt.get("optimal_actions", []) or [])
        if a.get("tool_name")
    ]
    optimal_tools = [(i, t) for i, t, _ in optimal_entries]
    optimal_set_name = {t for _, t in optimal_tools}
    optimal_set_sig = {_sig(t, p) for _, t, p in optimal_entries}

    useless_entries = [
        (ut.get("tool_name"), ut.get("tool_parameters") or {})
        for ut in (gt.get("useless_tools") or [])
    ]
    useless = {t for t, _ in useless_entries if t}
    useless_set_sig = {_sig(t, p) for t, p in useless_entries if t}

    harmful_entries = [
        (ht.get("tool_name"), ht.get("tool_parameters") or {})
        for ht in (gt.get("harmful_tools") or [])
    ]
    harmful = {t for t, _ in harmful_entries if t}
    harmful_set_sig = {_sig(t, p) for t, p in harmful_entries if t}

    # 1. optimal ∩ useless — by (tool_name, params) signature
    for sig in optimal_set_sig & useless_set_sig:
        issues.append(
            f"contradiction: `{sig[0]}` with same parameters in BOTH "
            f"optimal_actions AND useless_tools"
        )
    # 2. optimal ∩ harmful — by signature
    for sig in optimal_set_sig & harmful_set_sig:
        issues.append(
            f"contradiction: `{sig[0]}` with same parameters in BOTH "
            f"optimal_actions AND harmful_tools"
        )
    # 3. useless ∩ harmful — by signature
    for sig in useless_set_sig & harmful_set_sig:
        issues.append(
            f"contradiction: `{sig[0]}` with same parameters in BOTH "
            f"useless_tools AND harmful_tools"
        )

    # 3. Tools in 12-tool universe
    for i, t in optimal_tools:
        if t not in CANONICAL_TOOLS:
            issues.append(f"optimal_actions[{i}]: `{t}` not in canonical tool universe")
    for t in useless:
        if t and t not in CANONICAL_TOOLS:
            issues.append(f"useless_tools: `{t}` not in canonical tool universe")
    for t in harmful:
        if t and t not in CANONICAL_TOOLS:
            issues.append(f"harmful_tools: `{t}` not in canonical tool universe")

    # 4. Required tools have a corresponding output
    required = [
        (i, a.get("tool_name"))
        for i, a in enumerate(gt.get("optimal_actions", []) or [])
        if a.get("tool_name") and a.get("category") == "required"
    ]
    for i, t in required:
        if not _has_output(case, t):
            issues.append(
                f"optimal_actions[{i}] (`{t}`, required): "
                f"no initial_tool_outputs / followup_outputs entry — agent will get no result"
            )

    # 5. Useless tools have fallback (so calling them gives the off-pathway tier)
    for t in useless:
        if t and not _has_fallback(case, t):
            issues.append(
                f"useless_tools: `{t}` has no fallback_tool_outputs entry — "
                f"agent calling it will see an empty/error result"
            )

    # 6. SequenceConstraint tool names
    for i, c in enumerate(gt.get("sequence_constraints", []) or []):
        for key in ("before", "after"):
            v = c.get(key)
            if v and v not in CANONICAL_TOOLS:
                issues.append(
                    f"sequence_constraints[{i}].{key}: `{v}` not in canonical tool universe"
                )

    # 7. RedHerring field_path
    for i, rh in enumerate(gt.get("red_herrings", []) or []):
        path = (rh.get("field_path") or "").strip()
        if path and not _resolve_field_path(case, path):
            issues.append(
                f"red_herrings[{i}].field_path=`{path}` does not resolve in case JSON"
            )

    # 8. critical_actions + contraindicated_actions non-empty
    if not (gt.get("critical_actions") or []):
        issues.append("critical_actions is empty — under-authored")
    # contraindicated may legitimately be empty for some conditions; mild warning
    # only via --strict mode (handled in main)

    # 9. differential sorted by likelihood
    diff = gt.get("differential", []) or []
    if len(diff) > 1:
        prev_rank = -1
        for i, d in enumerate(diff):
            lk = d.get("likelihood") if isinstance(d, dict) else None
            rank = LIKELIHOOD_ORDER.get(lk, 99)
            if rank < prev_rank:
                issues.append(
                    f"differential[{i}]: likelihood `{lk}` out of order (should descend)"
                )
            prev_rank = max(prev_rank, rank)

    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cases-dir", type=Path, default=CASES_DIR)
    p.add_argument("--case", help="Inspect a single case in detail")
    p.add_argument("--strict", action="store_true", help="Also flag empty contraindicated_actions")
    args = p.parse_args()

    if not args.cases_dir.is_dir():
        print(f"ERROR: {args.cases_dir} not found", file=sys.stderr)
        return 2

    if args.case:
        path = args.cases_dir / args.case
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            return 2
        case = json.loads(path.read_text())
        issues = validate_case(case)
        if args.strict and not (case.get("ground_truth", {}).get("contraindicated_actions") or []):
            issues.append("contraindicated_actions is empty (strict mode)")
        print(f"{path.name}: {len(issues)} issue(s)")
        for iss in issues:
            print(f"  - {iss}")
        return 1 if issues else 0

    files = sorted(args.cases_dir.glob("*.json"))
    print(f"Validating {len(files)} cases...\n")

    total_issues = 0
    by_category: Counter[str] = Counter()
    by_case: list[tuple[str, int]] = []

    for f in files:
        case = json.loads(f.read_text())
        issues = validate_case(case)
        if args.strict and not (case.get("ground_truth", {}).get("contraindicated_actions") or []):
            issues.append("contraindicated_actions is empty")
        if issues:
            by_case.append((f.name, len(issues)))
            total_issues += len(issues)
            for iss in issues:
                # Use first 60 chars as category
                by_category[iss[:80]] += 1

    print(f"{len(files) - len(by_case)}/{len(files)} cases pass coherence checks")
    if by_case:
        print(f"\nTotal issues: {total_issues}")
        print(f"\nTop categories:")
        for cat, n in by_category.most_common(15):
            print(f"  {n:5d}  {cat}")
        print(f"\nFirst few failing cases:")
        for name, n in sorted(by_case, key=lambda x: -x[1])[:5]:
            print(f"  {name}: {n} issue(s)")
        return 1

    print("\nAll cases pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
