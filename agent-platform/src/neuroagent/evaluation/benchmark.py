"""Run one checked profile over a case set against the model server currently loaded.

Every episode is persisted whether it completed or failed, so failure rates stay in the
denominator. Draft policies are scoreable only with ``--allow-draft-policies``; the summary
records that the numbers came from draft policies and they are not reportable.

    uv run python -m neuroagent.evaluation.benchmark --profile policy-qwen3.5-9b \\
        --cases FEPI-TEMP-M01 SAH-M01 --output outputs/smoke/policy-qwen --allow-draft-policies
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from neuroagent_schemas import (
    ActionProposed,
    ActionRejected,
    ClinicalEpisode,
    NeuroBenchCase,
    RunCompleted,
    RunFailed,
)

from ..datasets import DATASETS, DEFAULT_DATASET_VERSION, load_dataset
from ..harness.profile import HarnessProfile, load_profiles
from ..harness.runtime import boot_profile, context_from_profile
from .policy_reward import ClinicalPolicyReward

PROFILES_DIR = Path(__file__).resolve().parents[3] / "config" / "profiles"


def select_cases(
    cases: dict[str, NeuroBenchCase], *, case_ids: list[str], split: str | None, dataset_path: Path
) -> list[NeuroBenchCase]:
    if case_ids:
        missing = sorted(set(case_ids) - cases.keys())
        if missing:
            raise SystemExit(f"unknown cases: {missing}")
        return [cases[case_id] for case_id in case_ids]
    if split:
        ids = (dataset_path / "splits" / f"{split}_cases.txt").read_text().split()
        return [cases[case_id] for case_id in ids]
    return list(cases.values())


def run_episode(
    profile: HarnessProfile, services: Any, case: NeuroBenchCase, episode_path: Path
) -> ClinicalEpisode:
    context = context_from_profile(profile, case, services)
    episode = context.loop.run(context)
    episode_path.write_text(episode.model_dump_json(indent=2))
    return episode


def episode_row(case: NeuroBenchCase, episode: ClinicalEpisode, scorer: ClinicalPolicyReward) -> dict:
    terminal = episode.events[-1]
    proposals = [event for event in episode.events if isinstance(event, ActionProposed)]
    row = {
        "case_id": case.case_id,
        "condition": case.condition.value,
        "difficulty": case.difficulty.value,
        "encounter_type": case.encounter_type.value,
        "status": "completed" if isinstance(terminal, RunCompleted) else "failed",
        "failure_reason": terminal.reason if isinstance(terminal, RunFailed) else None,
        "invalid_actions": sum(isinstance(event, ActionRejected) for event in episode.events),
        "tool_calls": len(episode.tool_actions),
        "tools_called": [action.tool_name for action in episode.tool_actions],
        "primary_diagnosis": episode.assessment.primary_diagnosis if episode.assessment else None,
        "total_cost_usd": episode.total_cost_usd,
        "total_tokens": episode.total_tokens,
        "model_latency_seconds": sum(event.latency_seconds for event in proposals),
        "reward": scorer.score(episode, case).model_dump(mode="json"),
    }
    return row


def summarize(rows: list[dict]) -> dict:
    completed = [row for row in rows if row["status"] == "completed"]
    components = [key for key in rows[0]["reward"] if key not in {"caps_applied", "invalid_actions"}]

    def mean(values: list[float]) -> float | None:
        return round(statistics.fmean(values), 4) if values else None

    return {
        "episodes": len(rows),
        "completed": len(completed),
        "completion_rate": round(len(completed) / len(rows), 4),
        "failure_reasons": dict(Counter(row["failure_reason"] for row in rows if row["failure_reason"])),
        "invalid_actions_total": sum(row["invalid_actions"] for row in rows),
        "episodes_with_invalid_actions": sum(row["invalid_actions"] > 0 for row in rows),
        "caps_applied": dict(Counter(cap for row in rows for cap in row["reward"]["caps_applied"])),
        "mean_reward": {key: mean([row["reward"][key] for row in rows]) for key in components},
        "mean_tool_calls": mean([row["tool_calls"] for row in rows]),
        "mean_cost_usd": mean([row["total_cost_usd"] for row in rows]),
        "mean_tokens": mean([row["total_tokens"] for row in rows]),
        "mean_model_latency_seconds": mean([row["model_latency_seconds"] for row in rows]),
        "by_condition": {
            condition: {
                "episodes": len(group),
                "completion_rate": round(sum(r["status"] == "completed" for r in group) / len(group), 4),
                "mean_scalar": mean([r["reward"]["scalar"] for r in group]),
                "diagnosis_accuracy": mean([r["reward"]["diagnosis"] for r in group]),
            }
            for condition in sorted({row["condition"] for row in rows})
            if (group := [row for row in rows if row["condition"] == condition])
        },
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--output", required=True, type=Path)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--cases", nargs="+", default=[])
    selection.add_argument("--split", choices=["train", "test"])
    selection.add_argument("--all", action="store_true")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--seed", type=int, default=None, help="sampling seed sent with every request")
    parser.add_argument(
        "--served-model",
        default=None,
        help="served model name to address instead of the base id, e.g. a LoRA alias from serve_model.sh",
    )
    parser.add_argument("--allow-draft-policies", action="store_true")
    parser.add_argument("--resume", action="store_true", help="skip cases whose episode file exists")
    args = parser.parse_args(argv)

    profiles = load_profiles(PROFILES_DIR)
    if args.profile not in profiles:
        raise SystemExit(f"unknown profile {args.profile!r}; available: {sorted(profiles)}")
    profile = profiles[args.profile]
    overrides = {
        key: value
        for key, value in (("seed", args.seed), ("served_model", args.served_model))
        if value is not None
    }
    for plugin in profile.plugins:
        if plugin.id.startswith("model."):
            plugin.config.update(overrides)

    dataset = DATASETS[DEFAULT_DATASET_VERSION]
    _, cases = load_dataset(dataset.path)
    selected = select_cases(cases, case_ids=args.cases, split=args.split, dataset_path=dataset.path)

    services = boot_profile(profile)
    scorer = (
        ClinicalPolicyReward(require_approved=False)
        if args.allow_draft_policies
        else services.require("reward")
    )
    episodes_dir = args.output / "episodes"
    episodes_dir.mkdir(parents=True, exist_ok=True)

    def one(case: NeuroBenchCase) -> dict:
        path = episodes_dir / f"{case.case_id}.json"
        if args.resume and path.exists():
            episode = ClinicalEpisode.model_validate_json(path.read_text())
        else:
            episode = run_episode(profile, services, case, path)
        row = episode_row(case, episode, scorer)
        print(
            f"{case.case_id:<22} {row['status']:<9} {row['failure_reason'] or '':<18} "
            f"tools={row['tool_calls']:<2} invalid={row['invalid_actions']} "
            f"scalar={row['reward']['scalar']:.3f} dx={row['reward']['diagnosis']:.0f} "
            f"cost=${row['total_cost_usd']:.0f} latency={row['model_latency_seconds']:.1f}s",
            flush=True,
        )
        return row

    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        rows = list(pool.map(one, selected))
    wall = time.perf_counter() - started

    (args.output / "rewards.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))
    summary = {
        "profile": profile.model_dump(mode="json"),
        "model_id": services.require("model").model_id,
        "dataset": dataset.version,
        "policy_review": "draft (not reportable)" if args.allow_draft_policies else "approved",
        "seed": args.seed,
        "wall_seconds": round(wall, 1),
        **summarize(rows),
    }
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k not in {"profile", "by_condition"}}, indent=2))


if __name__ == "__main__":
    main()
