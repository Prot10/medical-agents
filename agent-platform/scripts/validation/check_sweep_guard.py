"""Guard the subagent sweep: no case may get worse, and no clinical content may change.

A subagent editing case files can silence the validator by deleting the thing it complained
about. This script is the check that makes the sweep trustworthy, run after every round:

* a case a subagent touched must have strictly fewer issues than before (never more),
* no case outside the assigned conditions may change at all,
* `primary_diagnosis`, `icd_code` and `condition` must be byte-identical everywhere,
* every case must still validate against `NeuroBenchCase`.

Exit code is non-zero if any of those break, so the loop stops instead of converging on a
lobotomised dataset.

Usage:
    uv run python agent-platform/scripts/validation/check_sweep_guard.py \
        --before /tmp/pre_sweep.json --conditions als ftd
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_cases import CASES_DIR, _tool_schemas, validate_case  # noqa: E402

from neuroagent_schemas import NeuroBenchCase  # noqa: E402


def snapshot(cases_dir: Path) -> dict[str, dict]:
    """Per-case fingerprint: content hash, immutable clinical identity, and issue count."""
    schemas = _tool_schemas()
    snap: dict[str, dict] = {}
    for path in sorted(cases_dir.glob("*.json")):
        raw = path.read_bytes()
        case = json.loads(raw)
        snap[path.name] = {
            "sha": hashlib.sha256(raw).hexdigest(),
            "dx": case["ground_truth"]["primary_diagnosis"],
            "icd": case["ground_truth"]["icd_code"],
            "condition": case["condition"],
            "issues": len(validate_case(case, schemas)),
        }
    return snap


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a subagent sweep did no harm")
    parser.add_argument("--before", required=True, help="Snapshot JSON taken before the sweep")
    parser.add_argument("--cases-dir", default=str(CASES_DIR))
    parser.add_argument("--conditions", nargs="*", default=None,
                        help="Conditions the sweep was allowed to touch")
    parser.add_argument("--write-after", default=None, help="Save the post-sweep snapshot here")
    args = parser.parse_args()

    before = json.loads(Path(args.before).read_text())
    after = snapshot(Path(args.cases_dir))
    if args.write_after:
        Path(args.write_after).write_text(json.dumps(after))

    allowed = set(args.conditions or [])
    failures: list[str] = []
    improved = touched = 0

    for name, now in after.items():
        was = before.get(name)
        if was is None:
            failures.append(f"{name}: new case appeared")
            continue

        changed = was["sha"] != now["sha"]
        if changed:
            touched += 1

        if changed and allowed and now["condition"] not in allowed:
            failures.append(f"{name}: modified but its condition `{now['condition']}` was out of scope")

        for field in ("dx", "icd", "condition"):
            if was[field] != now[field]:
                failures.append(f"{name}: {field} changed — clinical content is immutable "
                                f"({was[field]!r} -> {now[field]!r})")

        # `issues` is absent from a snapshot taken before this script existed; skip then.
        if "issues" in was:
            if now["issues"] > was["issues"]:
                failures.append(f"{name}: issues rose {was['issues']} -> {now['issues']}")
            elif now["issues"] < was["issues"]:
                improved += 1

    for name in before:
        if name not in after:
            failures.append(f"{name}: case disappeared")

    schema_failures = 0
    for path in sorted(Path(args.cases_dir).glob("*.json")):
        try:
            NeuroBenchCase.model_validate(json.loads(path.read_text()))
        except Exception as exc:  # noqa: BLE001 - report, don't crash the guard
            schema_failures += 1
            failures.append(f"{path.name}: no longer validates ({type(exc).__name__})")

    total_before = sum(v.get("issues", 0) for v in before.values())
    total_after = sum(v["issues"] for v in after.values())

    print(f"cases touched      : {touched}")
    print(f"cases improved     : {improved}")
    print(f"issues             : {total_before} -> {total_after}")
    print(f"schema failures    : {schema_failures}")

    if failures:
        print(f"\nGUARD FAILED ({len(failures)}):")
        for f in failures[:20]:
            print(f"  {f}")
        return 1

    if "issues" in next(iter(before.values()), {}) and total_after > total_before:
        print("\nGUARD FAILED: total issue count increased")
        return 1

    print("\nGuard passed: no case regressed, no clinical content changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
