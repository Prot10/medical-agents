"""A turn cut off by the per-turn cap must be counted, not silently read as a conclusion.

The rollout ends a trajectory when a generated turn contains no parseable tool call. That is
correct when the model is finished — and wrong when the turn was simply cut off mid-reasoning
by `per_turn_max_tokens`, because a clipped turn also has no parseable tool call. The two are
indistinguishable downstream, so a cap set slightly too low silently converts "still working"
into "chose to stop without ordering any tests", and the trajectory is scored accordingly:
no tool calls, no diagnosis, correctness 0. The reward looks like bad clinical judgement when
it is really a truncated buffer.

Observed for real: a fresh (untrained) LoRA produced clipped_ratio 1.0 with
`completions/mean_terminated_length` 0.0 — every turn hit the 512-token cap and never emitted
EOS, so every trajectory ended after one turn with zero tool calls.

Uses the real Qwen3.5 tokenizer, because the EOS ids being checked are tokenizer-specific.
"""

from __future__ import annotations

import glob
import json
import os
from pathlib import Path

import pytest

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

REPO = Path(__file__).resolve().parents[2]


def _find_tokenizer() -> str | None:
    for c in glob.glob("/dev/shm/hf/hub/models--Qwen--Qwen3.5-*/snapshots/*"):
        if os.path.exists(os.path.join(c, "tokenizer_config.json")):
            return c
    return None


TOKENIZER_PATH = _find_tokenizer()
pytestmark = pytest.mark.skipif(
    TOKENIZER_PATH is None, reason="no local Qwen3.5 tokenizer snapshot"
)

TOOL_TURN = (
    "Considering the workup.\n</think>\n\n<tool_call>\n<function=analyze_brain_mri>\n"
    "<parameter=clinical_context>bulbar weakness</parameter>\n</function>\n</tool_call>"
)
FINAL_TURN = (
    "Concluding.\n</think>\n\n### Primary Diagnosis\n"
    "Amyotrophic lateral sclerosis (ALS), bulbar-onset\n\n"
    "### Differential Diagnoses\n1. Kennedy disease\n\n### Recommendations\nRiluzole"
)
# No closing </think>, no tool call, no EOS — what a turn guillotined at max_new_tokens
# actually looks like.
CLIPPED_TURN = "Let me reason about the differential at length. " * 12


@pytest.fixture(scope="module")
def ctx():
    from transformers import AutoTokenizer

    from neuroagent.agent.config import load_agent_config
    from neuroagent.agent.orchestrator import AgentOrchestrator
    from neuroagent.agent.reflection import get_reflection_prompt
    from neuroagent.rules.rules_engine import RulesEngine
    from neuroagent.tools.tool_registry import ToolRegistry
    from neuroagent.training.train_grpo import (
        _agent_tool_definitions,
        load_training_chat_template,
    )

    tok = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
    rules = RulesEngine(
        str(REPO / "agent-platform/config/hospital_rules"), hospital="de_charite"
    )
    orch = AgentOrchestrator(
        load_agent_config(hospital="de_charite"),
        ToolRegistry.create_default_registry(),
        rules,
    )
    return {
        "tok": tok,
        "tools": _agent_tool_definitions(),
        "system": orch._build_system_prompt(),
        "template": load_training_chat_template(),
        "reflection": get_reflection_prompt(),
    }


def _run(ctx, turn_texts, with_eos):
    """Drive one trajectory through a canned sequence of turns.

    `with_eos` decides whether each turn terminates properly or is left dangling, which is
    exactly the signal the clipped-turn counter keys on.
    """
    from neuroagent_schemas import NeuroBenchCase

    from neuroagent.evaluation.runner import format_patient_info
    from neuroagent.tools.cost_tracker import CostTracker
    from neuroagent.tools.mock_server import MockServer
    from neuroagent.training.rollout.react_rollout import ReactRollout

    tok = ctx["tok"]
    case = NeuroBenchCase.model_validate(
        json.loads((REPO / "data/neurobench/cases/ALS-M01.json").read_text())
    )
    rollout = ReactRollout(
        tokenizer=tok,
        tools=ctx["tools"],
        system_prompt=ctx["system"],
        chat_template=ctx["template"],
        enable_reflection=True,
        reflection_message=ctx["reflection"],
        max_completion_tokens=16384,
    )
    seq = list(turn_texts)
    calls = {"n": 0}

    def generate(_ids):
        text = seq[min(calls["n"], len(seq) - 1)]
        eos = with_eos[min(calls["n"], len(with_eos) - 1)]
        calls["n"] += 1
        ids = tok(text, add_special_tokens=False)["input_ids"]
        return ids + ([tok.eos_token_id] if eos else [])

    return rollout.rollout_one(
        case, format_patient_info(case), generate, MockServer(case), CostTracker()
    )


def test_properly_terminated_turns_count_zero_clipped(ctx):
    """The baseline: a normal trajectory must not report phantom clipping."""
    res = _run(ctx, [TOOL_TURN, FINAL_TURN], [True, True])
    assert res.clipped_turns == 0
    assert res.num_tool_calls == 1
    assert "Primary Diagnosis" in res.trace.final_response


def test_a_turn_without_eos_is_counted_as_clipped(ctx):
    """The failure the counter exists for: cut off mid-reasoning, read as a conclusion."""
    res = _run(ctx, [CLIPPED_TURN], [False])
    assert res.clipped_turns == 1
    # The damage is still done — this is what the trajectory looks like to the reward.
    assert res.num_tool_calls == 0


def test_clipping_is_counted_per_turn_not_per_trajectory(ctx):
    """Several clipped turns must not collapse into a single count."""
    res = _run(ctx, [TOOL_TURN, TOOL_TURN, FINAL_TURN], [False, False, True])
    assert res.clipped_turns == 2


def test_clipped_is_independent_of_the_budget_truncation_flag(ctx):
    """Two different failures, two different signals.

    `truncated` is the whole-completion budget; `clipped_turns` is the per-turn cap. A
    generous budget must not mask a clipped turn.
    """
    res = _run(ctx, [CLIPPED_TURN], [False])
    assert res.clipped_turns == 1
    assert not res.truncated


def test_a_cap_below_the_first_turn_destroys_the_whole_trajectory(ctx):
    """The regression that made every rollout degenerate, pinned.

    `per_turn_max_tokens` defaulted to 512, justified by a "~300-400 tokens per turn" average.
    Measured on the same model and config, changing only that value:

        512  -> mean 1.0 turns, 0.0 tool calls, reward_std 0.02-0.03
        4096 -> mean 3.0-6.2 turns, 1.0-3.8 tool calls, reward_std 0.20

    The average was the wrong statistic. Qwen3.5 writes a long <think> before its first tool
    call, so THAT turn runs far past the mean; cut mid-reasoning it carries no parseable tool
    call, the rollout reads it as a conclusion, and the trajectory ends after one turn having
    ordered nothing. A GRPO run would have trained entirely on such rollouts while loss, reward
    and truncation rate all looked healthy.

    Simulated here with a turn whose tool call sits past the cut point.
    """
    long_think = "Weighing the differential carefully. " * 40
    turn_with_late_call = long_think + TOOL_TURN

    res = _run(ctx, [turn_with_late_call, FINAL_TURN], [True, True])
    assert res.num_tool_calls == 1, "sanity: the tool call must be reachable when not cut"

    # Now cut the same turn before its tool call, exactly as a tight cap would.
    tok = ctx["tok"]
    cut = tok.decode(tok(turn_with_late_call, add_special_tokens=False)["input_ids"][:120])
    cut_res = _run(ctx, [cut], [False])
    assert cut_res.num_tool_calls == 0, "cut turn should lose its tool call"
    assert cut_res.clipped_turns == 1, "and it must be REPORTED, not silently read as a conclusion"


def test_turn_lengths_are_recorded_for_sizing_the_cap(ctx):
    """The cap has to be set from the observed tail, so the tail must be observable."""
    res = _run(ctx, [TOOL_TURN, TOOL_TURN, FINAL_TURN], [True, True, True])
    assert len(res.turn_lengths) == 3
    assert all(n > 0 for n in res.turn_lengths)
    # Per-turn lengths must describe the assistant turns only, never the tool results, or the
    # number used to size the cap would be inflated by environment tokens.
    assert max(res.turn_lengths) < len(res.completion_ids)
