"""Draw the synthetic case set of the agent-mode study and freeze its case files.

Rule: from one split, per condition (alphabetical order) ``--per-condition`` cases at random with
``random.Random(seed)``; the drawn cases are then shuffled with the same generator until no two
neighbours share a condition, so the order gives a physician no cue. The case files are copied
as they are into ``data/review/sets/<set id>/cases`` and the ordered list is printed for
``config/review/agent_mode_sets.yaml``.

    uv run python agent-platform/scripts/review/draw_agent_mode_set.py \\
        --set-id agent-synthetic-2026-11 --seed 20261125 --split test --per-condition 2
"""

from __future__ import annotations

import argparse
import random
import shutil
from collections import defaultdict

from neuroagent.datasets import DATASETS, DEFAULT_DATASET_VERSION, REPO_ROOT, load_dataset, split_case_ids


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--set-id", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--split", default="test", choices=["train", "validation", "test"])
    parser.add_argument("--per-condition", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true", help="print the draw, copy nothing")
    args = parser.parse_args()

    dataset = DATASETS[DEFAULT_DATASET_VERSION].path
    _, cases = load_dataset(dataset)
    conditions = {case_id: cases[case_id].condition.value for case_id in split_case_ids(dataset, args.split)}
    drawn = draw(conditions, args.per_condition, args.seed)
    if not args.dry_run:
        target = REPO_ROOT / "data" / "review" / "sets" / args.set_id / "cases"
        if target.exists():
            raise SystemExit(f"{target} exists: a frozen set is never redrawn in place, choose a new --set-id")
        target.mkdir(parents=True)
        for case_id in drawn:
            shutil.copyfile(dataset / "cases" / f"{case_id}.json", target / f"{case_id}.json")
    print("    cases:")
    for case_id in drawn:
        print(f"      - {case_id}")


if __name__ == "__main__":
    main()
