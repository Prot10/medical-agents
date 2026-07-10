"""Emit the stems that failed validation, with their issues, as JSON for the repair workflow.

Rejection sampling keeps only trajectories that pass validation. Rather than discarding a
near-miss outright, we give the teacher one repair round with the exact validator complaints —
this is much cheaper than regenerating from scratch and preserves the good reasoning.

Usage:
    uv run python agent-platform/scripts/training/list_repair_targets.py \
        --output-dir training_data/gold_trajectories
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="List trajectories needing repair")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max", type=int, default=None, help="Cap the number of stems returned")
    parser.add_argument("--json-only", action="store_true", help="Print only the JSON payload")
    args = parser.parse_args()

    out = Path(args.output_dir)
    rejected_dir = out / "rejected"
    manifest = {
        f"{m['case_id']}_{m['style']}": m
        for m in json.loads((out / "manifest.json").read_text())
    }

    targets = []
    for path in sorted(rejected_dir.glob("*.json")) if rejected_dir.exists() else []:
        data = json.loads(path.read_text())
        stem = path.stem
        if stem not in manifest:
            continue
        issues = data.get("issues")
        if not issues:
            reason = data.get("reason", "unknown")
            issues = [
                "The trace could not be parsed. Most likely an unbalanced tag: every "
                "<think>, <tool_call> and <tool_response> must have a matching closing tag, "
                "and a <tool_call> must be closed by </tool_call> (not </tool_response>)."
                if reason == "unparseable" else reason
            ]
        targets.append({"stem": stem, "issues": issues})

    # Prompts that were never generated at all also need a (first) attempt.
    raw_dir = out / "raw"
    missing = [
        {"stem": stem, "issues": []}
        for stem in manifest
        if not (raw_dir / f"{stem}.txt").exists()
    ]

    if args.max:
        targets = targets[: args.max]

    payload = {"repair": targets, "missing": missing}
    if args.json_only:
        print(json.dumps(payload))
        return

    print(f"needing repair: {len(targets)}")
    for t in targets:
        print(f"  {t['stem']}: {t['issues']}")
    print(f"never generated: {len(missing)}")
    print()
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
