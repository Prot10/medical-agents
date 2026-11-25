"""Export the physicians' agent-mode episodes in the layout of a benchmark run.

One folder per physician, written exactly as ``neuroagent.evaluation.benchmark`` writes a model
run, so the paper's comparison scripts read both the same way::

    <output>/<reviewer id>/episodes/<case id>.json   the ClinicalEpisode
    <output>/<reviewer id>/rewards.jsonl             one row per episode (same row, same scorer)
    <output>/<reviewer id>/summary.json              the run summary (model_id = physician:<id>)
    <output>/<reviewer id>/manifest.json             case, policy, scorer and environment hashes
    <output>/<reviewer id>/physician.jsonl           physician-only data: rationale per action,
                                                     reasoning, timings, telemetry, provenance

Only finished episodes are exported (completed or failed); cases still open are counted in the
summary. Draft policies are scoreable only with ``--allow-draft-policies`` and the summary then
says the numbers are not reportable.

    uv run python agent-platform/scripts/review/export_physician_episodes.py \\
        --section synthetic --output outputs/physicians/synthetic --allow-draft-policies

The MIMIC section is read from the directories in the environment (see
``config/review/agent_mode_sets.yaml``) and its export is refused inside the repository.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from neuroagent.datasets import REPO_ROOT
from neuroagent.evaluation.benchmark import episode_row, summarize
from neuroagent.evaluation.manifest import run_manifest
from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent.review_api.config import AGENT_MODE_RECORDS_DIR, AGENT_MODE_SETS_PATH
from neuroagent.review_api.services.agent_mode.sets import AgentSectionConfig, load_agent_mode
from neuroagent.review_api.services.agent_mode.store import AgentRecordStore


def export_section(section: AgentSectionConfig, output: Path, *, limits: dict, allow_draft: bool) -> dict[str, int]:
    """Write one run folder per physician; returns the number of episodes exported per physician."""
    if section.record_derived and output.resolve().is_relative_to(REPO_ROOT.resolve()):
        raise SystemExit("record-derived episodes are never written inside the repository")
    store = AgentRecordStore()
    scorer = ClinicalPolicyReward(require_approved=not allow_draft)
    exported: dict[str, int] = {}
    for reviewer_id in store.reviewer_ids(section):
        records = store.records_of(section, reviewer_id)
        finished = [
            records[case_id] for case_id in section.case_ids if case_id in records and records[case_id].status != "in_progress"
        ]
        if not finished:
            continue
        run_dir = output / reviewer_id
        (run_dir / "episodes").mkdir(parents=True, exist_ok=True)
        cases = [section.cases[record.case_id] for record in finished]
        rows, physician = [], []
        for record, case in zip(finished, cases):
            (run_dir / "episodes" / f"{case.case_id}.json").write_text(record.episode.model_dump_json(indent=2))
            rows.append(episode_row(case, record.episode, scorer))
            physician.append(
                record.model_dump(mode="json", exclude={"episode"}) | {"invalid_attempts": record.invalid_attempts}
            )
        (run_dir / "manifest.json").write_text(json.dumps(run_manifest(cases, scorer), indent=2))
        (run_dir / "rewards.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))
        (run_dir / "physician.jsonl").write_text("".join(json.dumps(item) + "\n" for item in physician))
        summary = {
            "profile": limits,
            "model_id": f"physician:{reviewer_id}",
            "reviewer_name": finished[0].reviewer_name,
            "dataset": f"agent-mode:{section.key}:{section.set_id}",
            "policy_review": "draft (not reportable)" if allow_draft else "approved",
            "cases_in_set": len(section.case_ids),
            "cases_in_progress": sum(record.status == "in_progress" for record in records.values()),
            **summarize(rows),
        }
        (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
        exported[reviewer_id] = len(rows)
    return exported


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--section", required=True, choices=["synthetic", "mimic"])
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--records-dir", type=Path, default=None,
        help="where the synthetic records are (default: data/review/agent-mode, or REVIEW_AGENT_MODE_DIR)",
    )
    parser.add_argument("--allow-draft-policies", action="store_true")
    args = parser.parse_args(argv)

    records_root = args.records_dir or Path(os.environ.get("REVIEW_AGENT_MODE_DIR") or AGENT_MODE_RECORDS_DIR)
    config = load_agent_mode(AGENT_MODE_SETS_PATH, records_root=records_root)
    if config is None or args.section not in config.sections:
        raise SystemExit(f"section {args.section!r} is not configured here (MIMIC needs its environment variables)")
    limits = {
        "profile_id": "policy-physician",
        "limits_from": config.limits_from,
        "max_turns": config.profile.max_turns,
        "max_cost_usd": config.profile.max_cost_usd,
        "max_invalid_actions": config.profile.max_invalid_actions,
    }
    exported = export_section(config.sections[args.section], args.output, limits=limits, allow_draft=args.allow_draft_policies)
    for reviewer_id, count in exported.items():
        print(f"{reviewer_id:<24} {count} episode(s) -> {args.output / reviewer_id}")
    if not exported:
        print("no finished episode to export")


if __name__ == "__main__":
    main()
