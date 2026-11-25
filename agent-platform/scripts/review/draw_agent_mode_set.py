"""Draw the synthetic case set of the agent-mode study, freeze its case files, refresh them.

Draw rule: from one split or from all of them (``--split all``: every case of the three split
files), per condition in alphabetical order ``--per-condition`` cases at random with
``random.Random(seed)``; the drawn cases are then shuffled with the same generator until no two
neighbours share a condition, so neither grouping nor order hints at the condition. The case
files are copied as they are into ``data/review/sets/<set id>/cases``, a ``manifest.json`` with
their hashes is written next to them, and the ordered list is printed for
``config/review/agent_mode_sets.yaml``.

    uv run python agent-platform/scripts/review/draw_agent_mode_set.py \\
        --set-id agent-synthetic-2026-11-v2 --seed 20261125 --split all --per-condition 1

Refresh: when the cases are corrected after the draw, re-copy the same case ids from
``data/neurobench/cases`` and update the manifest. Which cases are in the set, and their order,
never change. It is refused once any physician record exists for the set (what a physician
worked on must not change under them), unless ``--force``.

    uv run python agent-platform/scripts/review/draw_agent_mode_set.py --refresh agent-synthetic-2026-11-v2

The record check looks where this machine keeps the records (``data/review/agent-mode`` or
``REVIEW_AGENT_MODE_DIR``): before refreshing a set that is already deployed, check the admin
view of the server too.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from neuroagent.datasets import DATASETS, DEFAULT_DATASET_VERSION, REPO_ROOT, load_dataset, split_case_ids

SPLITS = ("train", "validation", "test")
SETS_DIR = REPO_ROOT / "data" / "review" / "sets"


def draw(case_conditions: dict[str, str], per_condition: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    by_condition: dict[str, list[str]] = defaultdict(list)
    for case_id in sorted(case_conditions):
        by_condition[case_conditions[case_id]].append(case_id)
    drawn = [case_id for condition in sorted(by_condition) for case_id in rng.sample(by_condition[condition], per_condition)]
    while True:
        rng.shuffle(drawn)
        if len(by_condition) == 1 or all(
            case_conditions[a] != case_conditions[b] for a, b in zip(drawn, drawn[1:])
        ):
            return drawn


def pool(dataset: Path, split: str) -> list[str]:
    """The case ids a draw may pick from: one split, or all three (excluded cases stay out)."""
    return [case_id for name in (SPLITS if split == "all" else (split,)) for case_id in split_case_ids(dataset, name)]


def set_hashes(cases_dir: Path) -> dict[str, str]:
    return {path.stem: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(cases_dir.glob("*.json"))}


def write_manifest(set_dir: Path, *, set_id: str, action: str) -> dict:
    """Hashes of the frozen files, and the commit of the cases they were copied from."""
    per_case = set_hashes(set_dir / "cases")
    try:
        commit = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=True, timeout=10
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        commit = None
    manifest = {
        "set_id": set_id,
        "action": action,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "data/neurobench/cases",
        "source_commit": commit,
        "cases": len(per_case),
        "cases_sha256": hashlib.sha256(json.dumps(per_case, sort_keys=True).encode()).hexdigest(),
        "per_case": per_case,
    }
    (set_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def existing_records(set_id: str, records_root: Path) -> int:
    """Physician records of this set on this machine (any section)."""
    return sum(1 for _ in records_root.glob(f"*/{set_id}/*/*.json"))


def refresh(set_id: str, *, source: Path, sets_dir: Path, records_root: Path, force: bool = False) -> dict:
    """Re-copy the set's case ids from ``source`` and update the manifest.

    Raises:
        SystemExit: The set does not exist, a case is gone from the source, or a physician
            record exists for the set and ``force`` is not given.
    """
    set_dir = sets_dir / set_id
    cases_dir = set_dir / "cases"
    if not cases_dir.is_dir():
        raise SystemExit(f"no frozen set at {cases_dir}")
    records = existing_records(set_id, records_root)
    if records and not force:
        raise SystemExit(
            f"{records} physician record(s) exist for {set_id}: refreshing would change what they worked on. "
            "Draw a new set id instead, or pass --force if you are sure."
        )
    case_ids = sorted(path.stem for path in cases_dir.glob("*.json"))
    missing = [case_id for case_id in case_ids if not (source / f"{case_id}.json").exists()]
    if missing:
        raise SystemExit(f"cases no longer in {source}: {missing}")
    before = set_hashes(cases_dir)
    for case_id in case_ids:
        shutil.copyfile(source / f"{case_id}.json", cases_dir / f"{case_id}.json")
    manifest = write_manifest(set_dir, set_id=set_id, action="refresh")
    changed = sorted(case_id for case_id in case_ids if before[case_id] != manifest["per_case"][case_id])
    return {"cases": len(case_ids), "changed": changed, "cases_sha256": manifest["cases_sha256"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", metavar="SET_ID", help="re-copy an existing set's cases from data/neurobench/cases")
    parser.add_argument("--force", action="store_true", help="with --refresh: refresh even if physician records exist")
    parser.add_argument("--set-id")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--split", default="all", choices=[*SPLITS, "all"])
    parser.add_argument("--per-condition", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="print the draw, copy nothing")
    args = parser.parse_args()

    dataset = DATASETS[DEFAULT_DATASET_VERSION].path
    if args.refresh:
        records_root = Path(os.environ.get("REVIEW_AGENT_MODE_DIR") or REPO_ROOT / "data" / "review" / "agent-mode")
        result = refresh(args.refresh, source=dataset / "cases", sets_dir=SETS_DIR, records_root=records_root, force=args.force)
        print(f"{args.refresh}: {result['cases']} cases re-copied, {len(result['changed'])} changed: {result['changed']}")
        print(f"cases_sha256 {result['cases_sha256']}")
        return
    if not args.set_id or args.seed is None:
        parser.error("--set-id and --seed are required for a draw")

    _, cases = load_dataset(dataset)
    conditions = {case_id: cases[case_id].condition.value for case_id in pool(dataset, args.split)}
    drawn = draw(conditions, args.per_condition, args.seed)
    if not args.dry_run:
        target = SETS_DIR / args.set_id / "cases"
        if target.exists():
            raise SystemExit(f"{target} exists: a frozen set is never redrawn in place, choose a new --set-id (or --refresh it)")
        target.mkdir(parents=True)
        for case_id in drawn:
            shutil.copyfile(dataset / "cases" / f"{case_id}.json", target / f"{case_id}.json")
        write_manifest(target.parent, set_id=args.set_id, action="draw")
    print("    cases:")
    for case_id in drawn:
        print(f"      - {case_id}")


if __name__ == "__main__":
    main()
