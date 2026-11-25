#!/usr/bin/env python3
"""Draw the MIMIC case set of the agent-mode study from the final processed cases.

Standard library only: it runs with a plain ``python3`` on rockhopper or lxplus, called by
``deployment/hostinger/push-mimic-cases.sh``. It reads only each case's ``case_id`` and
``condition`` and prints only counts per condition: never a case id, never case text.

Rule (``--n`` cases, default 20), stratified by condition:

1. one case for every condition present;
2. the remaining slots are shared among the conditions in proportion to the cases each still has
   (its size minus the one already taken), by largest remainder (ties: the larger condition,
   then alphabetical); no condition gets more cases than it has;
3. within each condition (alphabetical order), that many cases are drawn at random from its
   sorted case ids with ``random.Random(seed)``;
4. the drawn cases are shuffled with the same generator: that is the order they are served in.

The ordered ids are written one per line to every ``--write`` path.

    python3 draw_mimic_set.py <folder of case JSON files> --seed 20261125 --write <list file> [--write <copy>]
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path


def allocate(sizes: dict[str, int], n: int) -> dict[str, int]:
    """How many cases each condition contributes to a set of ``n``."""
    if n < len(sizes):
        raise ValueError(f"{n} cases cannot cover {len(sizes)} conditions")
    if n > sum(sizes.values()):
        raise ValueError(f"{n} cases asked, {sum(sizes.values())} available")
    allocation = {condition: 1 for condition in sizes}
    while (slots := n - sum(allocation.values())) > 0:
        room = {condition: sizes[condition] - allocation[condition] for condition in sizes}
        total = sum(room.values())
        quota = {condition: slots * room[condition] / total for condition in sizes}
        share = {condition: min(int(quota[condition]), room[condition]) for condition in sizes}
        leftover = slots - sum(share.values())
        by_remainder = sorted(sizes, key=lambda c: (-(quota[c] - int(quota[c])), -sizes[c], c))
        for condition in by_remainder:
            if leftover and share[condition] < room[condition]:
                share[condition] += 1
                leftover -= 1
        for condition in sizes:
            allocation[condition] += share[condition]
    return allocation


def draw(conditions: dict[str, str], n: int, seed: int) -> tuple[list[str], dict[str, int]]:
    """The ordered case ids of the set and the number drawn per condition.

    ``conditions`` maps each case id to its condition.
    """
    by_condition: dict[str, list[str]] = {}
    for case_id in sorted(conditions):
        by_condition.setdefault(conditions[case_id], []).append(case_id)
    allocation = allocate({condition: len(ids) for condition, ids in by_condition.items()}, n)
    rng = random.Random(seed)
    drawn = [case_id for condition in sorted(by_condition) for case_id in rng.sample(by_condition[condition], allocation[condition])]
    rng.shuffle(drawn)
    return drawn, allocation


def read_conditions(folder: Path) -> dict[str, str]:
    """``case_id`` → ``condition`` of every case file in ``folder``.

    Raises:
        ValueError: A file is not a case, or is not named after its case id. The message carries
            no file name and no content.
    """
    conditions: dict[str, str] = {}
    bad = 0
    for path in sorted(folder.glob("*.json")):
        try:
            data = json.loads(path.read_text())
            case_id, condition = data["case_id"], data["condition"]
            ok = isinstance(case_id, str) and isinstance(condition, str) and path.stem == case_id
        except (ValueError, KeyError, TypeError):
            ok = False
        if ok:
            conditions[case_id] = condition
        else:
            bad += 1
    if bad:
        raise ValueError(f"{bad} file(s) are not case files named <case_id>.json with a condition")
    return conditions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--write", type=Path, action="append", default=[], help="file to write the ordered ids to (repeatable)")
    args = parser.parse_args(argv)
    try:
        conditions = read_conditions(args.folder)
        drawn, allocation = draw(conditions, args.n, args.seed)
    except ValueError as exc:
        print(f"draw refused: {exc}", file=sys.stderr)
        return 1
    sizes: dict[str, int] = {}
    for condition in conditions.values():
        sizes[condition] = sizes.get(condition, 0) + 1
    print(f"{len(conditions)} cases, {len(sizes)} conditions; drawing {args.n} with seed {args.seed}")
    for condition in sorted(sizes, key=lambda c: (-sizes[c], c)):
        print(f"  {condition:<28} {allocation[condition]:>3} of {sizes[condition]}")
    for path in args.write:
        path.write_text("".join(f"{case_id}\n" for case_id in drawn))
    return 0


if __name__ == "__main__":
    sys.exit(main())
