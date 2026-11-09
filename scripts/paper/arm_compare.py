"""Several arms on the same cases, averaged over seeds, paired by case against a reference arm.

Prints aggregates only (per arm, per condition): no case ids, no model text. Safe to run on
record-derived cases whose episodes must not leave their storage.

    python scripts/paper/arm_compare.py --root OUT --arms narrative policy grpo-a grpo-b \
        --reference policy --seeds 1 2 3

Each arm is ``OUT/{arm}-s{seed}/rewards.jsonl`` as written by ``neuroagent.evaluation.benchmark``.
A case's value is its mean over the seeds; differences are paired by case, with a 95% case
bootstrap and a two-sided sign-flip permutation p.
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import statistics
from pathlib import Path

REWARD_KEYS = [
    "scalar",
    "diagnosis",
    "required_action_coverage",
    "required_action_coverage_exact",
    "tool_accuracy",
    "safety",
    "stopping",
    "cost_efficiency",
]
ROW_KEYS = ["tool_calls", "completed"]


def load(root: Path, arm: str, seeds: list[int]) -> dict[str, dict[str, float]]:
    """case_id -> metric -> mean over seeds (only cases present in every seed)."""
    per_seed = []
    for seed in seeds:
        path = root / f"{arm}-s{seed}" / "rewards.jsonl"
        per_seed.append({row["case_id"]: row for row in map(json.loads, path.open())})
    common = set.intersection(*(set(s) for s in per_seed))
    out = {}
    for case in common:
        rows = [s[case] for s in per_seed]
        metrics = {k: statistics.fmean(r["reward"][k] for r in rows) for k in REWARD_KEYS if k in rows[0]["reward"]}
        metrics["tool_calls"] = statistics.fmean(r["tool_calls"] for r in rows)
        metrics["completed"] = statistics.fmean(r["status"] == "completed" for r in rows)
        metrics["_condition"] = rows[0]["condition"]
        out[case] = metrics
    return out


def paired(a: list[float], b: list[float], rng: random.Random) -> tuple[float, float, float, float]:
    diffs = [x - y for x, y in zip(a, b)]
    mean = statistics.fmean(diffs)
    boots = sorted(statistics.fmean(rng.choices(diffs, k=len(diffs))) for _ in range(4000))
    extreme = sum(
        abs(statistics.fmean(d if rng.random() < 0.5 else -d for d in diffs)) >= abs(mean) - 1e-12
        for _ in range(4000)
    )
    return mean, boots[100], boots[3899], (extreme + 1) / 4001


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--arms", nargs="+", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--seeds", nargs="+", type=int, default=[1, 2, 3])
    args = parser.parse_args()
    rng = random.Random(0)

    data = {arm: load(args.root, arm, args.seeds) for arm in args.arms}
    cases = sorted(set.intersection(*(set(d) for d in data.values())))
    keys = [k for k in REWARD_KEYS + ROW_KEYS if all(k in data[a][cases[0]] for a in args.arms)]
    print(f"cases in every arm and seed: {len(cases)}   seeds: {args.seeds}")
    conditions = collections.Counter(data[args.reference][c]["_condition"] for c in cases)
    print("cases per condition:", dict(sorted(conditions.items())))

    short = {k: k.replace("required_action_coverage", "req_cov").replace("_efficiency", "_eff")[:12] for k in keys}
    print("\nMeans (case mean over seeds, then over cases)")
    print(f"{'arm':<14}" + "".join(f"{short[k]:>13}" for k in keys))
    for arm in args.arms:
        print(f"{arm:<14}" + "".join(f"{statistics.fmean(data[arm][c][k] for c in cases):>13.3f}" for k in keys))

    print(f"\nPaired against {args.reference}: mean difference [95% bootstrap]  p")
    for arm in args.arms:
        if arm == args.reference:
            continue
        print(f"-- {arm}")
        for k in keys:
            a = [data[arm][c][k] for c in cases]
            b = [data[args.reference][c][k] for c in cases]
            mean, lo, hi, p = paired(a, b, rng)
            print(f"   {k:<32} {mean:+.3f} [{lo:+.3f}, {hi:+.3f}]  p={p:.3f}")

    print("\nPer condition: scalar / diagnosis / required coverage")
    print(f"{'condition':<10}{'n':>4}" + "".join(f"{arm:>24}" for arm in args.arms))
    for cond in sorted(conditions):
        group = [c for c in cases if data[args.reference][c]["_condition"] == cond]
        cells = []
        for arm in args.arms:
            vals = [statistics.fmean(data[arm][c][k] for c in group) for k in ("scalar", "diagnosis", "required_action_coverage")]
            cells.append(f"{vals[0]:.2f}/{vals[1]:.2f}/{vals[2]:.2f}")
        print(f"{cond:<10}{len(group):>4}" + "".join(f"{cell:>24}" for cell in cells))


if __name__ == "__main__":
    main()
