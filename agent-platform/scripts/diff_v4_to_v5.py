"""Per-case diff between v4 and v5 ground_truth surface.

Emits a structured changelog summarizing what changed between the v4 dataset
(prior to the realism overhaul and the gold-trajectory regen) and v5 (after).
Used as a paper artifact for the methods / supplementary materials section.

For each case_id present in both v4 and v5, computes:
- primary_diagnosis change (free-text)
- icd_code change
- difficulty change (e.g., straightforward → moderate)
- optimal_actions: added/removed/recategorized tools
- New fields populated: useless_tools count, harmful_tools count,
  sequence_constraints count
- Differential changes: number of entries, top-likelihood entry change
- Citation count (number of ActionSteps now carrying a citation, vs 0 in v4)
- Metadata flags (case_body_concerns / citation_gap / vocab_gap counts)

Cases in v5 but NOT in v4 (the 316 new cases) are listed separately.

Usage:
    uv run python agent-platform/scripts/diff_v4_to_v5.py
    uv run python agent-platform/scripts/diff_v4_to_v5.py --markdown
    uv run python agent-platform/scripts/diff_v4_to_v5.py --case ALS-M01
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


V4_DIR = Path("data/neurobench_v4/cases")
V5_DIR = Path("data/neurobench_v5/cases")


def load_case(path: Path) -> dict:
    return json.loads(path.read_text())


def extract_tools_by_category(gt: dict) -> dict[str, set[str]]:
    """Return {category: {tool_names}} from optimal_actions."""
    by_cat: dict[str, set[str]] = defaultdict(set)
    for a in gt.get("optimal_actions", []) or []:
        tn = a.get("tool_name")
        cat = a.get("category", "")
        if tn:
            by_cat[cat].add(tn)
    return by_cat


def diff_case(v4: dict, v5: dict) -> dict[str, Any]:
    gv4 = v4.get("ground_truth", {})
    gv5 = v5.get("ground_truth", {})

    cats_v4 = extract_tools_by_category(gv4)
    cats_v5 = extract_tools_by_category(gv5)

    all_v4 = set().union(*cats_v4.values()) if cats_v4 else set()
    all_v5 = set().union(*cats_v5.values()) if cats_v5 else set()

    tools_added = sorted(all_v5 - all_v4)
    tools_removed = sorted(all_v4 - all_v5)

    # Citation count
    cited_v5 = sum(
        1 for a in gv5.get("optimal_actions", []) or []
        if (a.get("citation") or "").strip()
    )

    # Metadata flags
    md_v5 = v5.get("metadata", {}) or {}
    case_body_concerns = len(md_v5.get("case_body_concerns", []) or [])
    citation_gap = len(md_v5.get("citation_gap", []) or [])
    vocab_gap = len(md_v5.get("vocab_gap", []) or [])

    return {
        "case_id": v5.get("case_id"),
        "primary_diagnosis_changed": gv4.get("primary_diagnosis") != gv5.get("primary_diagnosis"),
        "primary_diagnosis_v4": gv4.get("primary_diagnosis"),
        "primary_diagnosis_v5": gv5.get("primary_diagnosis"),
        "icd_changed": gv4.get("icd_code") != gv5.get("icd_code"),
        "difficulty_v4": v4.get("difficulty"),
        "difficulty_v5": v5.get("difficulty"),
        "difficulty_changed": v4.get("difficulty") != v5.get("difficulty"),
        "tools_added": tools_added,
        "tools_removed": tools_removed,
        "required_count_v4": len(cats_v4.get("required", set())),
        "required_count_v5": len(cats_v5.get("required", set())),
        "recommended_count_v5": len(cats_v5.get("recommended", set())),
        "optional_count_v5": len(cats_v5.get("optional", set())),
        "useless_tools_v5": len(gv5.get("useless_tools", []) or []),
        "harmful_tools_v5": len(gv5.get("harmful_tools", []) or []),
        "sequence_constraints_v5": len(gv5.get("sequence_constraints", []) or []),
        "differential_count_v4": len(gv4.get("differential", []) or []),
        "differential_count_v5": len(gv5.get("differential", []) or []),
        "cited_actions_v5": cited_v5,
        "total_actions_v5": len(gv5.get("optimal_actions", []) or []),
        "case_body_concerns": case_body_concerns,
        "citation_gap": citation_gap,
        "vocab_gap": vocab_gap,
    }


def summarize(diffs: list[dict]) -> dict[str, Any]:
    n = len(diffs)
    s: dict[str, Any] = {
        "cases_in_both": n,
        "primary_diagnosis_changed": sum(1 for d in diffs if d["primary_diagnosis_changed"]),
        "icd_changed": sum(1 for d in diffs if d["icd_changed"]),
        "difficulty_changed": sum(1 for d in diffs if d["difficulty_changed"]),
        "difficulty_transitions": Counter(),
        "avg_tools_added_per_case": sum(len(d["tools_added"]) for d in diffs) / max(n, 1),
        "avg_tools_removed_per_case": sum(len(d["tools_removed"]) for d in diffs) / max(n, 1),
        "avg_required_v4": sum(d["required_count_v4"] for d in diffs) / max(n, 1),
        "avg_required_v5": sum(d["required_count_v5"] for d in diffs) / max(n, 1),
        "avg_recommended_v5": sum(d["recommended_count_v5"] for d in diffs) / max(n, 1),
        "avg_optional_v5": sum(d["optional_count_v5"] for d in diffs) / max(n, 1),
        "avg_useless_v5": sum(d["useless_tools_v5"] for d in diffs) / max(n, 1),
        "avg_harmful_v5": sum(d["harmful_tools_v5"] for d in diffs) / max(n, 1),
        "avg_sequence_v5": sum(d["sequence_constraints_v5"] for d in diffs) / max(n, 1),
        "avg_cited_v5": sum(d["cited_actions_v5"] for d in diffs) / max(n, 1),
        "avg_total_actions_v5": sum(d["total_actions_v5"] for d in diffs) / max(n, 1),
        "cases_with_concerns": sum(1 for d in diffs if d["case_body_concerns"]),
        "total_case_body_concerns": sum(d["case_body_concerns"] for d in diffs),
        "cases_with_citation_gap": sum(1 for d in diffs if d["citation_gap"]),
        "cases_with_vocab_gap": sum(1 for d in diffs if d["vocab_gap"]),
        "most_added_tools": Counter(),
        "most_removed_tools": Counter(),
    }
    for d in diffs:
        s["difficulty_transitions"][(d["difficulty_v4"], d["difficulty_v5"])] += 1
        for t in d["tools_added"]:
            s["most_added_tools"][t] += 1
        for t in d["tools_removed"]:
            s["most_removed_tools"][t] += 1
    return s


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--markdown", action="store_true", help="Emit markdown changelog")
    p.add_argument("--case", help="Single case_id to inspect")
    p.add_argument(
        "--output",
        type=Path,
        default=Path("data/neurobench_v5/CHANGELOG_v4_to_v5.md"),
        help="Markdown output path (when --markdown)",
    )
    args = p.parse_args()

    if not V4_DIR.is_dir() or not V5_DIR.is_dir():
        print("ERROR: v4 or v5 cases dir missing", file=sys.stderr)
        return 2

    v4_files = {f.stem: f for f in V4_DIR.glob("*.json")}
    v5_files = {f.stem: f for f in V5_DIR.glob("*.json")}

    in_both = sorted(set(v4_files) & set(v5_files))
    v5_only = sorted(set(v5_files) - set(v4_files))
    v4_only = sorted(set(v4_files) - set(v5_files))

    if args.case:
        if args.case not in v4_files or args.case not in v5_files:
            print(f"Case {args.case} not in both v4 and v5", file=sys.stderr)
            return 2
        d = diff_case(load_case(v4_files[args.case]), load_case(v5_files[args.case]))
        print(json.dumps(d, indent=2, default=str))
        return 0

    diffs = []
    for cid in in_both:
        try:
            d = diff_case(load_case(v4_files[cid]), load_case(v5_files[cid]))
            diffs.append(d)
        except Exception as e:
            print(f"WARN {cid}: {e}", file=sys.stderr)

    summary = summarize(diffs)

    if args.markdown:
        out = args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        lines: list[str] = []
        lines.append("# NeuroBench v4 → v5 changelog")
        lines.append("")
        lines.append(f"**Cases in both versions:** {summary['cases_in_both']}")
        lines.append(f"**Cases new in v5:** {len(v5_only)}")
        lines.append(f"**Cases removed in v5:** {len(v4_only)}")
        lines.append("")
        lines.append("## Aggregate changes (v4 → v5)")
        lines.append("")
        lines.append(f"- primary_diagnosis changed: {summary['primary_diagnosis_changed']}")
        lines.append(f"- icd_code changed: {summary['icd_changed']}")
        lines.append(f"- difficulty changed: {summary['difficulty_changed']}")
        lines.append("")
        lines.append("### Difficulty transitions")
        for (v4, v5), n in sorted(summary["difficulty_transitions"].items(), key=lambda x: -x[1]):
            lines.append(f"- {v4} → {v5}: {n}")
        lines.append("")
        lines.append("### Per-case tool workup")
        lines.append(f"- avg required tools v4: {summary['avg_required_v4']:.2f}")
        lines.append(f"- avg required tools v5: {summary['avg_required_v5']:.2f}")
        lines.append(f"- avg recommended tools v5: {summary['avg_recommended_v5']:.2f}")
        lines.append(f"- avg optional tools v5: {summary['avg_optional_v5']:.2f}")
        lines.append(f"- avg useless_tools v5: {summary['avg_useless_v5']:.2f}")
        lines.append(f"- avg harmful_tools v5: {summary['avg_harmful_v5']:.2f}")
        lines.append(f"- avg sequence_constraints v5: {summary['avg_sequence_v5']:.2f}")
        lines.append(f"- avg cited actions v5: {summary['avg_cited_v5']:.2f} / {summary['avg_total_actions_v5']:.2f}")
        lines.append("")
        lines.append("### Tool additions / removals (top 15 each)")
        lines.append("")
        lines.append("**Most-added tools (in v5 but not in v4 for the matching case):**")
        for t, n in summary["most_added_tools"].most_common(15):
            lines.append(f"- {t}: {n} cases")
        lines.append("")
        lines.append("**Most-removed tools (in v4 but not in v5 for the matching case):**")
        for t, n in summary["most_removed_tools"].most_common(15):
            lines.append(f"- {t}: {n} cases")
        lines.append("")
        lines.append("### Authoring flags (v5)")
        lines.append(f"- cases with case_body_concerns: {summary['cases_with_concerns']}")
        lines.append(f"- total case_body_concerns entries: {summary['total_case_body_concerns']}")
        lines.append(f"- cases with citation_gap: {summary['cases_with_citation_gap']}")
        lines.append(f"- cases with vocab_gap: {summary['cases_with_vocab_gap']}")
        lines.append("")
        lines.append("## Per-case detail")
        lines.append("")
        lines.append("| case_id | dx changed | difficulty | required v4→v5 | useless | harmful | seq | cited |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for d in sorted(diffs, key=lambda x: x["case_id"]):
            dx = "✓" if d["primary_diagnosis_changed"] else ""
            diff_change = (
                f"{d['difficulty_v4']} → {d['difficulty_v5']}"
                if d["difficulty_changed"] else d["difficulty_v5"] or ""
            )
            lines.append(
                f"| {d['case_id']} | {dx} | {diff_change} | "
                f"{d['required_count_v4']} → {d['required_count_v5']} | "
                f"{d['useless_tools_v5']} | {d['harmful_tools_v5']} | "
                f"{d['sequence_constraints_v5']} | "
                f"{d['cited_actions_v5']}/{d['total_actions_v5']} |"
            )
        out.write_text("\n".join(lines) + "\n")
        print(f"Wrote markdown changelog to {out}")
    else:
        # Compact text summary
        print(f"Cases in both v4 and v5: {summary['cases_in_both']}")
        print(f"Cases new in v5: {len(v5_only)} (the 316 added beyond v4)")
        print(f"Cases removed in v5: {len(v4_only)}")
        print()
        print("=== Aggregate changes (v4 → v5) ===")
        print(f"  primary_diagnosis changed: {summary['primary_diagnosis_changed']}")
        print(f"  icd_code changed:          {summary['icd_changed']}")
        print(f"  difficulty changed:        {summary['difficulty_changed']}")
        print()
        print("  Difficulty transitions:")
        for (v4, v5), n in sorted(summary["difficulty_transitions"].items(), key=lambda x: -x[1]):
            print(f"    {v4!s:>20} → {v5!s:<20} {n:4d}")
        print()
        print("=== Workup expansion ===")
        print(f"  avg required v4 → v5: {summary['avg_required_v4']:.2f} → {summary['avg_required_v5']:.2f}")
        print(f"  avg recommended v5:   {summary['avg_recommended_v5']:.2f}")
        print(f"  avg optional v5:      {summary['avg_optional_v5']:.2f}")
        print(f"  avg useless v5:       {summary['avg_useless_v5']:.2f}")
        print(f"  avg harmful v5:       {summary['avg_harmful_v5']:.2f}")
        print(f"  avg sequence_v5:      {summary['avg_sequence_v5']:.2f}")
        print(f"  avg cited/total:      {summary['avg_cited_v5']:.2f} / {summary['avg_total_actions_v5']:.2f}")
        print()
        print("=== Top added/removed tools ===")
        print("  Added (top 10):")
        for t, n in summary["most_added_tools"].most_common(10):
            print(f"    {t}: {n}")
        print("  Removed (top 10):")
        for t, n in summary["most_removed_tools"].most_common(10):
            print(f"    {t}: {n}")
        print()
        print("=== Authoring flags (v5) ===")
        print(f"  cases with case_body_concerns: {summary['cases_with_concerns']}")
        print(f"  total case_body_concerns:      {summary['total_case_body_concerns']}")
        print(f"  cases with citation_gap:       {summary['cases_with_citation_gap']}")
        print(f"  cases with vocab_gap:          {summary['cases_with_vocab_gap']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
