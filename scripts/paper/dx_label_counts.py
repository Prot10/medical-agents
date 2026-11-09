"""Which primary diagnoses an arm gave, per condition, and how they scored: aggregates only.

A label is printed only when it was given in at least ``--min-cases`` distinct cases, so no line
describes a single case. Safe to run on record-derived runs.

    python scripts/paper/dx_label_counts.py --root OUT --arms tools grpo-best --seeds 1 2 3
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path


def norm(label: str | None) -> str:
    if not label:
        return "<none>"
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 /-]", " ", label.lower())).strip()[:70]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--arms", nargs="+", required=True)
    parser.add_argument("--seeds", nargs="+", type=int, default=[1, 2, 3])
    parser.add_argument("--min-cases", type=int, default=2)
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()
    for arm in args.arms:
        given: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
        cases: dict[tuple[str, str], set] = collections.defaultdict(set)
        correct: dict[tuple[str, str], list] = collections.defaultdict(list)
        for seed in args.seeds:
            for row in map(json.loads, (args.root / f"{arm}-s{seed}" / "rewards.jsonl").open()):
                key = (row["condition"], norm(row.get("primary_diagnosis")))
                given[row["condition"]][key[1]] += 1
                cases[key].add(row["case_id"])
                correct[key].append(row["reward"]["diagnosis"])
        print(f"===== {arm}")
        for condition in sorted(given):
            total = sum(given[condition].values())
            print(f"-- {condition} ({total} episodes)")
            shown = 0
            for label, count in given[condition].most_common():
                if len(cases[(condition, label)]) < args.min_cases:
                    continue
                scores = correct[(condition, label)]
                print(f"   {count:>3}  in {len(cases[(condition, label)]):>2} cases  dx={sum(scores) / len(scores):.2f}  {label}")
                shown += 1
                if shown == args.top:
                    break
            hidden = total - sum(c for l, c in given[condition].items() if len(cases[(condition, l)]) >= args.min_cases)
            print(f"   ({hidden} episodes with labels given in fewer than {args.min_cases} cases)")


if __name__ == "__main__":
    main()
