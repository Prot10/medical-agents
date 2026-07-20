"""Build the GRPO prompt dataset from NeuroBench cases.

GRPO is on-policy: it needs only the PROMPT for each case. The trainer samples its own
completions and the online CompositeReward scores them against the case ground truth
(`rewards/online_reward.py`). No trajectories are involved — this is why the old
`format_for_grpo.py` (which derives prompts from gold traces, and whose
`_build_prompt_from_trace` returns "") is not used for GRPO.

The prompt is rendered to TEXT here, with the tokenizer's chat template and the exact
tool schemas the orchestrator sends at inference, so what the policy is trained on is
byte-for-byte what it will see when served:

    system : orchestrator.txt (+ reasoning style) + hospital protocols   <- AgentOrchestrator
    user   : format_patient_info(case)                                   <- the eval runner
    tools  : ToolRegistry definitions, restricted by agent.yaml          <- _agent_tool_definitions

TRL treats a string `prompt` column as a "standard" (non-conversational) dataset and does
NOT re-apply the chat template, so the rendered text reaches the model unchanged. Passing
messages instead would let TRL template them a second time and drop the tools block.

Usage:
    python -m neuroagent.training.data.build_grpo_dataset \
        --split train --hospital de_charite \
        --model Qwen/Qwen3.5-9B \
        --output data/neurobench/grpo/train_prompts.jsonl
"""

from __future__ import annotations

import argparse
import json
import logging
import statistics
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[5]
AGENT_PLATFORM = REPO_ROOT / "agent-platform"


def build_prompts(split: str, hospital: str, model: str) -> tuple[list[dict], list[int]]:
    """Render one prompt per case in `split`. Returns (records, prompt_token_lengths)."""
    from transformers import AutoTokenizer

    from neuroagent_schemas import NeuroBenchCase

    from ...agent.config import load_agent_config
    from ...agent.orchestrator import AgentOrchestrator
    from ...evaluation.runner import format_patient_info
    from ...rules.rules_engine import RulesEngine
    from ...tools.tool_registry import ToolRegistry
    from ..train_grpo import _agent_tool_definitions

    dataset_dir = REPO_ROOT / "data" / "neurobench"
    split_file = dataset_dir / "splits" / f"{split}_cases.txt"
    if not split_file.exists():
        raise FileNotFoundError(f"No split file at {split_file}")
    case_ids = [c for c in split_file.read_text().split() if c]

    rules = RulesEngine(
        str(AGENT_PLATFORM / "config" / "hospital_rules"), hospital=hospital
    )
    # The system prompt depends only on config + rules, so one orchestrator serves every
    # case. Building it through AgentOrchestrator (rather than re-implementing the
    # assembly here) is what guarantees the training prompt cannot drift from serving.
    orchestrator = AgentOrchestrator(
        config=load_agent_config(hospital=hospital),
        tool_registry=ToolRegistry.create_default_registry(),
        rules_engine=rules,
    )
    system_prompt = orchestrator._build_system_prompt()
    tools = _agent_tool_definitions()

    tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)

    records: list[dict] = []
    lengths: list[int] = []
    for cid in case_ids:
        case_file = dataset_dir / "cases" / f"{cid}.json"
        if not case_file.exists():
            logger.warning("Case not found, skipping: %s", cid)
            continue
        case = NeuroBenchCase.model_validate(json.loads(case_file.read_text()))

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": format_patient_info(case)},
        ]
        prompt_text = tokenizer.apply_chat_template(
            messages, tools=tools, add_generation_prompt=True, tokenize=False
        )
        lengths.append(len(tokenizer(prompt_text)["input_ids"]))
        records.append({
            "case_id": case.case_id,
            "prompt": prompt_text,
            "condition": case.condition.value,
            "difficulty": case.difficulty.value,
        })

    return records, lengths


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Build the GRPO prompt dataset")
    parser.add_argument("--split", default="train", help="Split to build (train/test)")
    parser.add_argument("--hospital", default="de_charite", help="Hospital rule set (match the eval)")
    parser.add_argument("--model", default="Qwen/Qwen3.5-9B", help="Tokenizer / chat template to render with")
    parser.add_argument("--output", required=True, help="Output .jsonl")
    args = parser.parse_args()

    records, lengths = build_prompts(args.split, args.hospital, args.model)
    if not records:
        raise SystemExit(f"No cases rendered for split {args.split!r}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")

    lengths.sort()
    print(f"\n  wrote {len(records)} prompts -> {out}")
    print(f"  prompt tokens: min={lengths[0]}  median={statistics.median(lengths):.0f}  "
          f"p95={lengths[int(0.95 * (len(lengths) - 1))]}  max={lengths[-1]}")
    print(f"  hospital={args.hospital}  tokenizer={args.model}\n")


if __name__ == "__main__":
    sys.exit(main())
