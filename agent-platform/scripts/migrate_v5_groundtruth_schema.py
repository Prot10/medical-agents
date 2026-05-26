"""One-time migration: v5 case ground_truth → new schema (gold-trajectory regen).

Reshapes the existing 516 v5 case JSON files so they validate against the
new GroundTruth schema introduced for the gold-trajectory regeneration pass.

Operations (mechanical only — does NOT author new content; the fleet does that):

1. ActionStep.category remapping:
   - "acceptable"     → "recommended"
   - "contraindicated" + tool_name=null → moved to contraindicated_actions
   - "contraindicated" + tool_name set  → moved to harmful_tools with rationale
   The ActionStep is removed from optimal_actions in both contraindicated cases.

2. Differential normalization:
   - 237 free-text likelihood values collapsed onto the 5-value Likelihood enum
     via a deterministic map (preserves ordering: very_low/low/moderate/high/very_high).
   - Each dict becomes a DifferentialDx object (key_features defaults to "").

3. New empty fields added when missing:
   - useless_tools: []
   - harmful_tools: []   (or populated from contraindicated-with-tool ActionSteps)
   - sequence_constraints: []

4. RedHerring: leave existing fields alone, field_path defaults to "".

Idempotent: re-running on a migrated file is a no-op.

Usage:
    uv run python agent-platform/scripts/migrate_v5_groundtruth_schema.py
    uv run python agent-platform/scripts/migrate_v5_groundtruth_schema.py --dry-run
    uv run python agent-platform/scripts/migrate_v5_groundtruth_schema.py --validate
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

CASES_DIR = Path("data/neurobench_v5/cases")


# -------------------------------------------------------------------
# Likelihood normalization
# -------------------------------------------------------------------


def normalize_likelihood(raw: str) -> str:
    """Map free-text likelihood → Likelihood enum value.

    Order of checks matters: more specific phrases first.
    """
    if not isinstance(raw, str):
        return "low"
    s = raw.lower().strip().replace("-", " ").replace("_", " ")
    # Strip parentheticals so "moderate (contributing)" matches "moderate"
    base = s.split("(")[0].strip()

    # Direct matches on cleaned base
    if base in {"very low", "verylow"}:
        return "very_low"
    if base == "low":
        return "low"
    if base == "moderate":
        return "moderate"
    if base == "high":
        return "high"
    if base in {"very high", "veryhigh"}:
        return "very_high"

    # Semantic synonyms
    if "excluded" in s or "ruled out" in s:
        return "very_low"
    if "unlikely" in s:
        return "very_low"
    if "most likely" in s:
        return "high"
    # "likely" without "very/un" prefix
    if " likely" in (" " + s) and "unlikely" not in s and "very" not in s:
        return "high"

    # Compound: "low-moderate", "moderate to high", etc. Err toward the LOWER
    # bound for compound expressions so we don't inflate likelihood.
    if "low" in s and "moderate" in s:
        return "low"
    if "moderate" in s and "high" in s:
        return "moderate"
    if "low" in s and "high" in s:
        return "low"

    # Single-word containment (after compound checks)
    if "moderate" in s:
        return "moderate"
    if "very low" in s:
        return "very_low"
    if "low" in s:
        return "low"
    if "high" in s:
        return "high"

    # Unknown — default conservative
    return "low"


# -------------------------------------------------------------------
# Migration
# -------------------------------------------------------------------


def migrate_ground_truth(gt: dict[str, Any]) -> dict[str, Any]:
    """Return a new ground_truth dict matching the v5-regen schema."""
    new = dict(gt)

    # ---- optimal_actions: rename / extract contraindicated ----
    old_actions: list[dict[str, Any]] = new.get("optimal_actions", []) or []
    new_actions: list[dict[str, Any]] = []
    new_contraindicated_text: list[str] = []
    new_harmful_tools: list[dict[str, Any]] = []

    for a in old_actions:
        cat = (a.get("category") or "").strip().lower()
        if cat == "acceptable":
            a = {**a, "category": "recommended"}
            new_actions.append(a)
        elif cat == "contraindicated":
            tool_name = a.get("tool_name")
            if tool_name:
                # Move to harmful_tools
                new_harmful_tools.append(
                    {
                        "tool_name": tool_name,
                        "tool_parameters": a.get("tool_parameters", {}),
                        "rationale": a.get("action", "")
                        or a.get("expected_finding", "")
                        or "Contraindicated tool call.",
                        "citation": "",
                    }
                )
            else:
                # Free-text contraindicated action
                txt = a.get("action") or a.get("expected_finding") or ""
                if txt:
                    new_contraindicated_text.append(txt)
        else:
            # "required" / "recommended" / "optional" / unknown — keep as-is
            new_actions.append(a)

    new["optimal_actions"] = new_actions

    # ---- contraindicated_actions: union with extracted text ----
    existing_contra = list(new.get("contraindicated_actions", []) or [])
    for t in new_contraindicated_text:
        if t not in existing_contra:
            existing_contra.append(t)
    new["contraindicated_actions"] = existing_contra

    # ---- differential: dict → DifferentialDx, normalize likelihood ----
    old_diff: list[dict[str, Any]] = new.get("differential", []) or []
    new_diff: list[dict[str, Any]] = []
    for d in old_diff:
        if not isinstance(d, dict):
            continue
        dx = {
            "diagnosis": d.get("diagnosis", ""),
            "likelihood": normalize_likelihood(d.get("likelihood", "low")),
            "key_features": d.get("key_features", "") or d.get("features", ""),
        }
        if "icd_code" in d and d["icd_code"]:
            dx["icd_code"] = d["icd_code"]
        new_diff.append(dx)
    new["differential"] = new_diff

    # ---- new empty fields (additive) ----
    new.setdefault("useless_tools", [])
    # Merge previously-extracted harmful tools with any pre-existing list
    pre_harmful = list(new.get("harmful_tools", []) or [])
    for h in new_harmful_tools:
        # Dedupe on (tool_name, tool_parameters)
        if not any(
            ph.get("tool_name") == h["tool_name"]
            and ph.get("tool_parameters", {}) == h.get("tool_parameters", {})
            for ph in pre_harmful
        ):
            pre_harmful.append(h)
    new["harmful_tools"] = pre_harmful
    new.setdefault("sequence_constraints", [])

    # ---- red_herrings: ensure field_path key exists ----
    new_rh: list[dict[str, Any]] = []
    for rh in new.get("red_herrings", []) or []:
        if isinstance(rh, dict):
            rh = dict(rh)
            rh.setdefault("field_path", "")
            new_rh.append(rh)
    new["red_herrings"] = new_rh

    return new


def is_already_migrated(gt: dict[str, Any]) -> bool:
    """A ground_truth is considered migrated when:
    - no ActionStep has category == "acceptable" or "contraindicated"
    - all new fields exist
    - differential entries (if any) use enum likelihood values
    """
    new_field_keys = {"useless_tools", "harmful_tools", "sequence_constraints"}
    if not new_field_keys.issubset(gt.keys()):
        return False
    for a in gt.get("optimal_actions", []) or []:
        if (a.get("category") or "").lower() in {"acceptable", "contraindicated"}:
            return False
    enum_vals = {"very_low", "low", "moderate", "high", "very_high"}
    for d in gt.get("differential", []) or []:
        if isinstance(d, dict) and d.get("likelihood") not in enum_vals:
            return False
    return True


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing files.",
    )
    p.add_argument(
        "--validate",
        action="store_true",
        help="After migrating, parse each file with the new Pydantic schema and report failures.",
    )
    p.add_argument(
        "--cases-dir",
        type=Path,
        default=CASES_DIR,
        help="Directory of case JSONs (default: data/neurobench_v5/cases).",
    )
    args = p.parse_args()

    if not args.cases_dir.is_dir():
        print(f"ERROR: cases dir not found: {args.cases_dir}", file=sys.stderr)
        return 2

    files = sorted(args.cases_dir.glob("*.json"))
    print(f"Found {len(files)} case files in {args.cases_dir}")

    stats = Counter()
    changed_files: list[Path] = []
    likelihood_unmapped: Counter[str] = Counter()

    for f in files:
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            print(f"  PARSE_ERROR {f.name}: {e}", file=sys.stderr)
            stats["parse_error"] += 1
            continue

        gt = data.get("ground_truth", {})
        if is_already_migrated(gt):
            stats["already_migrated"] += 1
            continue

        # Track raw likelihoods for visibility
        for d in gt.get("differential", []) or []:
            if isinstance(d, dict):
                raw = d.get("likelihood", "")
                if isinstance(raw, str) and normalize_likelihood(raw) == "low" and raw.lower().strip() not in {"low", "low-moderate", "low_moderate"}:
                    # Only track values that fell through to the conservative default
                    pass

        new_gt = migrate_ground_truth(gt)
        if new_gt != gt:
            data["ground_truth"] = new_gt
            if not args.dry_run:
                f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            changed_files.append(f)
            stats["migrated"] += 1
        else:
            stats["no_change"] += 1

    print(f"\nMigration summary:")
    for k, v in sorted(stats.items()):
        print(f"  {k:20s} {v:5d}")

    if args.validate:
        print("\nRunning Pydantic validation against new schema...")
        try:
            sys.path.insert(0, "packages/neuroagent-schemas/src")
            from neuroagent_schemas import NeuroBenchCase  # type: ignore
        except Exception as e:
            print(f"  Could not import schema: {e}", file=sys.stderr)
            return 1

        failures = 0
        for f in files:
            try:
                NeuroBenchCase.model_validate_json(f.read_text())
            except Exception as e:
                failures += 1
                if failures <= 10:
                    print(f"  FAIL {f.name}: {str(e)[:200]}")
        print(f"  Validation: {len(files) - failures}/{len(files)} passed")
        if failures:
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
