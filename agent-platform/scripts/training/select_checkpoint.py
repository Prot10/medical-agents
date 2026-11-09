"""Pick each E1 arm's checkpoint on the validation cases, by the arm's own reward (decision D7).

Reads the benchmark outputs that `eval_checkpoints.sh` writes for one run (``OUTPUT/{base,checkpoint-N}-s{seed}/
episodes/*.json``), rescores every episode with both rewards, averages over seeds within a case and then over
cases, and picks the checkpoint with the highest mean of the arm's training reward: the policy arm by the policy
scalar, the outcome arm by the outcome scalar. Ties go to the earlier step. The base model is reported beside the
checkpoints and is never selected. The case list must hold no test-split case.

Usage:
    python agent-platform/scripts/training/select_checkpoint.py EVAL_DIR --reward policy|outcome \
        [--outcome-budget-usd 5913 --outcome-cost-weight 0.15] [--allow-draft-policies] [--json OUT.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

from neuroagent.datasets import DATASETS, DEFAULT_DATASET_VERSION, load_dataset, refuse_test_cases
from neuroagent.evaluation.outcome_reward import OutcomeReward
from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent.harness.free_order import typed_episode
from neuroagent_schemas import ClinicalEpisode

RUN_DIR = re.compile(r"^(base|checkpoint-(\d+))-s(\d+)$")


def score_runs(eval_dir: Path, policy: ClinicalPolicyReward, outcome: OutcomeReward, cases: dict) -> dict:
    """{tag: {"step": int | None, "seeds": [...], "policy": mean, "outcome": mean, ...}} over complete runs."""
    per_case: dict[str, dict[str, dict[str, list[float]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    seeds: dict[str, set[int]] = defaultdict(set)
    for run in sorted(p for p in eval_dir.iterdir() if p.is_dir() and RUN_DIR.match(p.name)):
        tag, _, seed = RUN_DIR.match(run.name).groups()
        episodes = sorted((run / "episodes").glob("*.json"))
        if not episodes:
            continue
        seeds[tag].add(int(seed))
        for path in episodes:
            episode = typed_episode(ClinicalEpisode.model_validate_json(path.read_text()))
            case = cases[path.stem]
            p, o = policy.score(episode, case), outcome.score(episode, case)
            row = per_case[tag][path.stem]
            row["policy"].append(p.scalar)
            row["outcome"].append(o.scalar)
            row["diagnosis"].append(p.diagnosis)
            row["required_coverage"].append(p.required_action_coverage)
            row["cost_usd"].append(episode.total_cost_usd)
            row["tool_calls"].append(float(len(episode.tool_actions)))
    refuse_test_cases({case_id for rows in per_case.values() for case_id in rows})
    common = set.intersection(*(set(rows) for rows in per_case.values())) if per_case else set()
    table = {}
    for tag, rows in per_case.items():
        match = RUN_DIR.match(f"{tag}-s0")
        step = int(match.group(2)) if match.group(2) else None
        table[tag] = {
            "step": step,
            "seeds": sorted(seeds[tag]),
            "cases": len(common),
            **{key: mean(mean(rows[c][key]) for c in common) for key in next(iter(rows.values()))},
        }
    return table


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("eval_dir", type=Path)
    parser.add_argument("--reward", choices=["policy", "outcome"], required=True, help="the arm's training reward")
    parser.add_argument("--outcome-budget-usd", type=float, default=5913.0, help="B, frozen for E1 (decision D6)")
    parser.add_argument("--outcome-cost-weight", type=float, default=0.15)
    parser.add_argument("--allow-draft-policies", action="store_true")
    parser.add_argument("--json", type=Path, help="write the table and the choice here")
    args = parser.parse_args(argv)

    _, cases = load_dataset(DATASETS[DEFAULT_DATASET_VERSION].path)
    approved = not args.allow_draft_policies
    policy = ClinicalPolicyReward(require_approved=approved)
    outcome = OutcomeReward(budget_usd=args.outcome_budget_usd, cost_weight=args.outcome_cost_weight, require_approved=approved)
    table = score_runs(args.eval_dir, policy, outcome, cases)
    checkpoints = {tag: row for tag, row in table.items() if row["step"] is not None}
    if not checkpoints:
        print(f"no scored checkpoint in {args.eval_dir}", file=sys.stderr)
        return 1
    seed_sets = {tuple(row["seeds"]) for row in table.values()}
    if len(seed_sets) > 1:
        print(f"warning: runs have different seeds {sorted(seed_sets)}; compare complete runs only", file=sys.stderr)
    best = max(sorted(checkpoints, key=lambda t: checkpoints[t]["step"]), key=lambda t: checkpoints[t][args.reward])

    keys = ["policy", "outcome", "diagnosis", "required_coverage", "tool_calls", "cost_usd"]
    print(f"{'run':<18}" + "".join(f"{k:>18}" for k in keys))
    for tag in sorted(table, key=lambda t: -1 if table[t]["step"] is None else table[t]["step"]):
        mark = "  <- selected" if tag == best else ""
        print(f"{tag:<18}" + "".join(f"{table[tag][k]:>18.3f}" for k in keys) + mark)
    print(f"selected by the {args.reward} reward: {best}")
    if args.json:
        args.json.write_text(json.dumps({"reward": args.reward, "selected": best, "table": table,
                                         "outcome_budget_usd": args.outcome_budget_usd,
                                         "outcome_cost_weight": args.outcome_cost_weight}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
