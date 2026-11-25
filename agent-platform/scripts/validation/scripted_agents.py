"""E0: scripted agents of known quality, run through the policy loop and scored by the policy reward.

Does the reward rank agents whose quality is known by construction, before any model is involved?
Every agent submits the policy's accepted diagnosis, its ICD-10 code and the required
recommendations, so the agents differ only in the work-up and the reward's process terms are
compared alone:

  perfect   the required and recommended criteria of the case (first alternative, the criterion's
            own arguments), required first, in an order that respects every sequence constraint;
  no_tool   no order at all: the diagnosis at the first turn;
  shotgun   the same case-independent battery for every case: every distinct study some policy of
            the benchmark requires, most often required first, ordered while the turn budget allows.

An order that would overrun the cost budget is skipped, not placed: the required work-up of every
case fits it (at most USD 11 937, glioma), but in three glioma cases the recommended studies on top
of it do not (4 Nov 2026), and an agent that knows the budget would leave them out.

The agents play through `ClinicalPolicyLoop` with the limits of the policy profile (12 turns, the
last one the assessment, USD 15000), so they meet the same turn limit and budget a model meets. They
use no tokens, so token efficiency is at its ceiling for all three. The hypothesis (tracker, E0):
perfect > no_tool and perfect > shotgun on the mean scalar of every condition; a shortcut that
reaches the perfect agent on one condition means the reward must be fixed first.

    uv run python agent-platform/scripts/validation/scripted_agents.py --output outputs/paper/e0

Reference episodes for the supervised fine-tuning baseline (Fig. 6, decided 25 Nov 2026): the
perfect agent on the training cases, written as candidate episode records for `train_sft`
(`--allow-candidates`; they are scripted, not physician-approved). The urgency of the assessment
follows the encounter type, since the policies do not state one:

    uv run python agent-platform/scripts/validation/scripted_agents.py --agents perfect --split train \
        --output outputs/paper/sft-reference --sft-records training_data/sft_reference_episodes.jsonl
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
from multiprocessing import Pool
from pathlib import Path

from neuroagent.datasets import DATASETS, DEFAULT_DATASET_VERSION, load_dataset, split_case_ids
from neuroagent.evaluation.benchmark import PROFILES_DIR, episode_row, summarize
from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent.harness import NeuroBenchEnvironment
from neuroagent.harness.interfaces import ModelTurn, RunContext
from neuroagent.harness.loops import ClinicalPolicyLoop
from neuroagent.harness.profile import load_profiles
from neuroagent.training.data.episodes import EpisodeRecord
from neuroagent.tools.cost_tracker import CostTracker
from neuroagent_schemas import ActionImportance, NeuroBenchCase, SubmitAssessment, ToolAction

AGENTS = ("perfect", "no_tool", "shotgun")
URGENCY = {"emergency": "emergent", "inpatient": "urgent", "outpatient": "routine"}
PROFILE = "policy-qwen3.5-9b"


def _arguments(case: NeuroBenchCase, pattern, label: str, environment: NeuroBenchEnvironment) -> dict:
    """The pattern's own arguments, completed with what the tool schema requires.

    `clinical_context` is the criterion's label; a drug or a literature query the pattern leaves open
    is the one the case stored a result for (as in the perfect-agent check).
    """
    arguments = dict(pattern.required_arguments)
    schema = environment.registry.get_tool(pattern.tool_name).parameter_schema
    stored = case.initial_tool_outputs
    for name in schema.get("required", []):
        if name in arguments:
            continue
        if name == "clinical_context":
            arguments[name] = label
        elif name == "drug":
            arguments[name] = next(iter(stored.drug_interactions or {}), label)
        elif name == "query":
            arguments[name] = next(iter(stored.literature_search or {}), label)
    return arguments


def _perfect_order(case: NeuroBenchCase) -> list:
    """Required, then recommended criteria; a stable topological sort over the sequence constraints."""
    policy = case.ground_truth
    rank = {ActionImportance.REQUIRED: 0, ActionImportance.RECOMMENDED: 1}
    wanted = sorted(
        (c for c in policy.action_criteria if c.importance in rank), key=lambda c: rank[c.importance]
    )
    ids = {c.criterion_id for c in wanted}
    before = {c.criterion_id: set() for c in wanted}
    for constraint in policy.sequence_constraints:
        if constraint.before_criterion_id in ids and constraint.after_criterion_id in ids:
            before[constraint.after_criterion_id].add(constraint.before_criterion_id)
    ordered, done = [], set()
    while len(ordered) < len(wanted):
        ready = [c for c in wanted if c.criterion_id not in done and before[c.criterion_id] <= done]
        if not ready:  # a cycle: the perfect-agent check reports it; keep the remaining order
            ready = [c for c in wanted if c.criterion_id not in done]
        ordered.append(ready[0])
        done.add(ready[0].criterion_id)
    return [(c.alternatives[0], c.label) for c in ordered]


def shotgun_battery(cases: dict[str, NeuroBenchCase]) -> list:
    """Every distinct required study of the benchmark, the most often required first."""
    counts: collections.Counter = collections.Counter()
    patterns = {}
    for case in cases.values():
        for criterion in case.ground_truth.action_criteria:
            if criterion.importance is not ActionImportance.REQUIRED:
                continue
            pattern = criterion.alternatives[0]
            key = (pattern.tool_name, json.dumps(pattern.required_arguments, sort_keys=True))
            counts[key] += 1
            patterns.setdefault(key, pattern)
    return [(patterns[key], "diagnostic work-up") for key, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]


class ScriptedModel:
    """A model adapter that plays a fixed list of orders, then submits the accepted diagnosis."""

    adapter_id = "scripted"

    def __init__(self, agent: str, orders: list, budget_usd: float) -> None:
        self.model_id = f"scripted/{agent}"
        self.agent = agent
        self.orders = list(orders)
        self.budget_usd = budget_usd
        self.costs = CostTracker()

    def next_action(self, *, case, episode, allowed_tools, require_assessment=False, **_) -> ModelTurn:
        environment = NeuroBenchEnvironment(case)
        while self.orders and not require_assessment:
            pattern, label = self.orders.pop(0)
            action = ToolAction(tool_name=pattern.tool_name, arguments=_arguments(case, pattern, label, environment))
            cost = self.costs.compute_cost(action.tool_name, action.arguments).cost_usd
            if episode.total_cost_usd + cost > self.budget_usd:
                continue
            return ModelTurn(action=action)
        policy = case.ground_truth
        return ModelTurn(action=SubmitAssessment(
            primary_diagnosis=policy.diagnosis.accepted[0],
            icd10_code=policy.diagnosis.icd_codes[0] if policy.diagnosis.icd_codes else None,
            confidence=0.9,
            urgency=URGENCY[case.encounter_type.value],
            recommendations=list(policy.assessment.required_recommendations),
        ))


def _run(job: tuple[str, NeuroBenchCase, list, Path]) -> dict:
    agent, case, battery, output = job
    profile = load_profiles(PROFILES_DIR)[PROFILE]
    orders = {"perfect": _perfect_order(case), "no_tool": [], "shotgun": battery}[agent]
    context = RunContext(
        profile_id=f"scripted-{agent}",
        model=ScriptedModel(agent, orders, profile.max_cost_usd),
        loop=ClinicalPolicyLoop(),
        environment=NeuroBenchEnvironment(case),
        max_turns=profile.max_turns,
        max_cost_usd=profile.max_cost_usd,
        max_invalid_actions=profile.max_invalid_actions,
    )
    episode = context.loop.run(context)
    (output / agent / "episodes" / f"{case.case_id}.json").write_text(episode.model_dump_json(indent=2))
    return {"agent": agent, **episode_row(case, episode, ClinicalPolicyReward(require_approved=False))}


def report(rows: list[dict]) -> dict:
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in rows:
        by[row["condition"]][row["agent"]].append(row)
    table, failures = {}, []
    for condition in sorted(by):
        entry = {}
        for agent in AGENTS:
            group = by[condition][agent]
            entry[agent] = {
                "scalar": statistics.fmean(r["reward"]["scalar"] for r in group),
                "capped": sum(bool(r["reward"]["caps_applied"]) for r in group) / len(group),
                "completed": sum(r["status"] == "completed" for r in group) / len(group),
                "tool_calls": statistics.fmean(r["tool_calls"] for r in group),
            }
        table[condition] = entry
        for shortcut in ("no_tool", "shotgun"):
            if entry[shortcut]["scalar"] >= entry["perfect"]["scalar"]:
                failures.append(f"{condition}: {shortcut} {entry[shortcut]['scalar']:.3f} >= perfect {entry['perfect']['scalar']:.3f}")
    # Which components make the gap: mean component per agent over all cases.
    components = [k for k in rows[0]["reward"] if k not in {"caps_applied", "invalid_actions"}]
    means = {
        agent: {k: statistics.fmean(r["reward"][k] for r in rows if r["agent"] == agent) for k in components}
        for agent in AGENTS
    }
    return {"by_condition": table, "components": means, "h1_failures": failures}


def write_sft_records(episodes_dir: Path, cases: list[NeuroBenchCase], path: Path) -> None:
    """Completed perfect-agent episodes as `candidate_not_gold` records; failed ones are left out."""
    from neuroagent_schemas import ClinicalEpisode, RunCompleted

    records, skipped = [], []
    for case in cases:
        episode = ClinicalEpisode.model_validate_json((episodes_dir / f"{case.case_id}.json").read_text())
        if not isinstance(episode.events[-1], RunCompleted):
            skipped.append(case.case_id)
            continue
        records.append(EpisodeRecord(
            candidate_id=f"scripted-perfect/{case.case_id}",
            case_id=case.case_id,
            label="candidate_not_gold",
            provenance={"source": "scripted_agents.py perfect", "policy_review": case.ground_truth.review_status.value},
            episode=episode,
        ))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(record.model_dump_json() + "\n" for record in records))
    print(f"SFT records: {len(records)} written to {path}, {len(skipped)} incomplete left out {skipped[:5]}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--agents", nargs="+", choices=AGENTS, default=list(AGENTS))
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--cases", nargs="+", help="case ids (default: all)")
    selection.add_argument("--split", choices=["train", "validation", "test"])
    parser.add_argument(
        "--sft-records",
        type=Path,
        help="also write the perfect agent's completed episodes as SFT candidate records (train split only)",
    )
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args(argv)
    _, cases = load_dataset(DATASETS[DEFAULT_DATASET_VERSION].path)
    battery = shotgun_battery(cases)
    if args.sft_records and (args.split != "train" or "perfect" not in args.agents):
        parser.error("--sft-records needs --split train and the perfect agent")
    dataset_path = DATASETS[DEFAULT_DATASET_VERSION].path
    if args.cases:
        selected = [cases[c] for c in args.cases]
    elif args.split:
        selected = [cases[c] for c in split_case_ids(dataset_path, args.split)]
    else:
        selected = list(cases.values())
    for agent in args.agents:
        (args.output / agent / "episodes").mkdir(parents=True, exist_ok=True)
    jobs = [(agent, case, battery, args.output) for agent in args.agents for case in selected]
    with Pool(args.workers) as pool:
        rows = pool.map(_run, jobs, chunksize=8)
    for agent in args.agents:
        agent_rows = [r for r in rows if r["agent"] == agent]
        (args.output / agent / "rewards.jsonl").write_text("".join(json.dumps(r) + "\n" for r in agent_rows))
        (args.output / agent / "summary.json").write_text(json.dumps(summarize(agent_rows), indent=2))
    if args.sft_records:
        write_sft_records(args.output / "perfect" / "episodes", selected, args.sft_records)
    (args.output / "shotgun_battery.json").write_text(json.dumps(
        [{"tool": p.tool_name, "arguments": p.required_arguments} for p, _ in battery], indent=1))
    if set(args.agents) == set(AGENTS):
        result = report(rows)
        (args.output / "report.json").write_text(json.dumps(result, indent=2))
        print(f"{'condition':34} " + " ".join(f"{a:>9}" for a in AGENTS) + "   capped(shotgun)")
        for condition, entry in result["by_condition"].items():
            print(f"{condition:34} " + " ".join(f"{entry[a]['scalar']:9.3f}" for a in AGENTS)
                  + f"   {entry['shotgun']['capped']:.2f}")
        print("components (mean over all cases):")
        for k in result["components"]["perfect"]:
            print(f"  {k:32} " + " ".join(f"{result['components'][a][k]:9.3f}" for a in AGENTS))
        print("H1 holds on every condition" if not result["h1_failures"] else "H1 FAILS:\n  " + "\n  ".join(result["h1_failures"]))


if __name__ == "__main__":
    main()
