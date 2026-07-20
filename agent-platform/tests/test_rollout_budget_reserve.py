"""The completion budget must never cost a trajectory its diagnosis.

Hitting the budget used to END the rollout mid-workup, so the agent never stated a diagnosis,
`correctness` (the largest reward weight) was structurally 0, and the group-relative advantage
rewarded "finished within budget" over "diagnosed correctly" — i.e. it taught the model to
order FEWER tests. Measured on one trajectory: composite 0.664 with the diagnosis, 0.296
without.

The rollout now reserves budget for the conclusion. A tight budget must degrade HOW MANY tools
the agent can order, never WHETHER it produces an assessment.

Uses the real Qwen3.5 tokenizer (template seams matter) with a canned policy; skipped when no
local tokenizer snapshot is available.
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


def _run(ctx, budget: int):
    """A policy that keeps ordering tools until told the budget is spent, then concludes."""
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
        max_completion_tokens=budget,
    )
    calls = {"n": 0}

    def generate(ids):
        calls["n"] += 1
        tail = tok.decode(ids[-400:])
        told_to_stop = "no further diagnostic budget" in tail
        text = FINAL_TURN if (told_to_stop or calls["n"] >= 6) else TOOL_TURN
        return tok(text, add_special_tokens=False)["input_ids"] + [tok.eos_token_id]

    return case, rollout.rollout_one(
        case, format_patient_info(case), generate, MockServer(case), CostTracker()
    )


@pytest.mark.parametrize("budget", [1000, 1500, 2000, 3000, 16384])
def test_every_budget_still_yields_a_diagnosis(ctx, budget):
    """The core guarantee: a diagnosis at every budget, and never a truncated trajectory."""
    _case, res = _run(ctx, budget)
    assert not res.truncated, f"budget {budget} truncated the trajectory"
    assert res.trace.final_response, f"budget {budget} produced no assessment"
    assert "Primary Diagnosis" in res.trace.final_response
    assert len(res.completion_ids) <= budget
    assert len(res.completion_ids) == len(res.env_mask) == len(res.logprobs)


@pytest.mark.parametrize("budget", [1000, 2000, 16384])
def test_correctness_is_earnable_at_every_budget(ctx, budget):
    """A tight budget must not zero the largest reward component."""
    from neuroagent.training.rewards.composite_reward import CompositeReward

    case, res = _run(ctx, budget)
    composite = CompositeReward.from_config(
        str(REPO / "agent-platform/config/training/reward_weights_grpo_multiturn.yaml"),
        str(REPO / "agent-platform/config/tools/costs.yaml"),
        str(REPO / "agent-platform/config/hospital_rules"),
        "de_charite",
    )
    breakdown = composite.compute_with_breakdown(res.trace, case)
    assert breakdown.correctness == pytest.approx(1.0), (
        f"budget {budget}: correct diagnosis scored {breakdown.correctness}"
    )


def test_budget_degrades_workup_depth_not_the_diagnosis(ctx):
    """A smaller budget should cost tool calls, not the assessment."""
    _c_small, small = _run(ctx, 1000)
    _c_large, large = _run(ctx, 16384)
    assert small.num_tool_calls <= large.num_tool_calls
    assert small.trace.final_response and large.trace.final_response


def test_oversized_tool_result_cannot_truncate(ctx):
    """A single tool report larger than the reserve must not blow past it.

    Checking the budget AFTER appending a result let one ~600-1000 token report jump straight
    over the reserve window and truncate the trajectory anyway (observed at budget=2000). The
    check has to happen before the result is appended.
    """
    for budget in (1800, 1900, 2000, 2100, 2200):
        _case, res = _run(ctx, budget)
        assert not res.truncated, f"budget {budget} truncated despite the reserve"
        assert res.trace.final_response, f"budget {budget} lost the assessment"
