"""Free-order arm against the menu arm, paired by case, per seed and pooled.

For each seed: means of diagnosis, required coverage (partial and exact), scalar, tool calls and
cost in both arms, the paired difference with a 95% case bootstrap, completion, the free orders by
kind, per-condition diagnosis and required coverage, and why the required criteria were missed
(tool never ordered, same tool with other arguments, matched).

    python scripts/paper/free_order_compare.py --menu OUT/qwen/policy-s{seed} --free OUT/qwen/free-order-s{seed}

``--menu`` and ``--free`` are run folders with ``{seed}`` in place of the seed (each holds
``rewards.jsonl`` and ``episodes/``), e.g. ``outputs/paper/catalogue_full/B-s{seed}``.
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import statistics
from pathlib import Path

from neuroagent.datasets import DATASETS, DEFAULT_DATASET_VERSION, load_dataset
from neuroagent.evaluation.policy_reward import criterion_matches
from neuroagent.harness.free_order import typed_episode
from neuroagent_schemas import ActionImportance, ClinicalEpisode

REWARD_KEYS = ["diagnosis", "required_action_coverage", "required_action_coverage_exact", "scalar"]


def rows(run: Path) -> dict[str, dict]:
    return {row["case_id"]: row for row in map(json.loads, (run / "rewards.jsonl").open())}


def value(row: dict, key: str) -> float:
    return row["reward"][key] if key in REWARD_KEYS else row[key]


def bootstrap(diffs: list[float], rng: random.Random) -> tuple[float, float]:
    means = sorted(statistics.fmean(rng.choices(diffs, k=len(diffs))) for _ in range(2000))
    return means[50], means[1949]


def misses(run: Path, cases) -> collections.Counter:
    counts: collections.Counter = collections.Counter()
    for path in sorted((run / "episodes").glob("*.json")):
        episode = typed_episode(ClinicalEpisode.model_validate_json(path.read_text()))
        actions = episode.tool_actions
        names = {action.tool_name for action in actions}
        for criterion in cases[path.stem].ground_truth.action_criteria:
            if criterion.importance is not ActionImportance.REQUIRED:
                continue
            if any(criterion_matches(criterion, action) for action in actions):
                counts["matched"] += 1
            elif names & {alt.tool_name for alt in criterion.alternatives}:
                counts["same tool, other arguments"] += 1
            else:
                counts["tool never ordered"] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--menu", required=True)
    parser.add_argument("--free", required=True)
    parser.add_argument("--seeds", nargs="+", default=["1", "2", "3"])
    args = parser.parse_args()
    _, cases = load_dataset(DATASETS[DEFAULT_DATASET_VERSION].path)
    rng = random.Random(0)
    pooled: dict[str, list[float]] = collections.defaultdict(list)
    for seed in args.seeds:
        menu_dir, free_dir = Path(args.menu.format(seed=seed)), Path(args.free.format(seed=seed))
        if not (menu_dir / "rewards.jsonl").exists() or not (free_dir / "rewards.jsonl").exists():
            print(f"seed {seed}: missing run, skipped")
            continue
        menu, free = rows(menu_dir), rows(free_dir)
        ids = sorted(menu.keys() & free.keys())
        print(f"seed {seed}: {len(ids)} paired cases")
        for key in [*REWARD_KEYS, "tool_calls", "total_cost_usd"]:
            diffs = [value(free[i], key) - value(menu[i], key) for i in ids]
            pooled[key] += diffs
            low, high = bootstrap(diffs, rng)
            print(
                f"  {key:32} menu {statistics.fmean(value(menu[i], key) for i in ids):9.3f}"
                f"  free {statistics.fmean(value(free[i], key) for i in ids):9.3f}"
                f"  diff {statistics.fmean(diffs):+.3f} [{low:+.3f}, {high:+.3f}]"
            )
        for label, data in (("menu", menu), ("free", free)):
            done = sum(data[i]["status"] == "completed" for i in ids)
            reasons = dict(collections.Counter(data[i]["failure_reason"] for i in ids if data[i]["failure_reason"]))
            print(f"  completed {label}: {done}/{len(ids)} {reasons}")
        kinds: collections.Counter = collections.Counter()
        for i in ids:
            kinds.update(free[i].get("free_orders", {}))
        print("  free orders by kind:", dict(kinds))
        for label, run in (("menu", menu_dir), ("free", free_dir)):
            counts = misses(run, cases)
            total = sum(counts.values()) or 1
            print(f"  required criteria, {label}:", {k: f"{v} ({v / total:.0%})" for k, v in counts.most_common()})
        by_condition = collections.defaultdict(list)
        for i in ids:
            by_condition[free[i]["condition"]].append(i)
        print("  per condition: diagnosis menu/free, required coverage menu/free")
        for condition, group in sorted(by_condition.items()):
            def mean(data, key, group=group):
                return statistics.fmean(data[i]["reward"][key] for i in group)
            print(
                f"    {condition:34} {mean(menu, 'diagnosis'):.2f}/{mean(free, 'diagnosis'):.2f}"
                f"  {mean(menu, 'required_action_coverage'):.2f}/{mean(free, 'required_action_coverage'):.2f}"
            )
    if pooled:
        print("pooled over seeds (case x seed pairs):")
        for key, diffs in pooled.items():
            low, high = bootstrap(diffs, rng)
            print(f"  {key:32} diff {statistics.fmean(diffs):+.3f} [{low:+.3f}, {high:+.3f}]")


if __name__ == "__main__":
    main()
