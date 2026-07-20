"""Token-alignment and masking tests for the multi-turn ReAct rollout.

These use the REAL Qwen3.5 tokenizer (so the chat-template token seams are exercised) with a
CANNED policy, so the whole rollout is validated without a GPU. Skipped if no local Qwen3.5
tokenizer snapshot is available.
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
    for pat in (
        "/dev/shm/hf/hub/models--Qwen--Qwen3.5-*/snapshots/*",
        str(REPO / "*/checkpoints/sft_Qwen3.5-*"),
    ):
        for c in glob.glob(pat):
            if os.path.exists(os.path.join(c, "tokenizer_config.json")):
                return c
    return None


TOKENIZER_PATH = _find_tokenizer()
pytestmark = pytest.mark.skipif(
    TOKENIZER_PATH is None, reason="no local Qwen3.5 tokenizer snapshot"
)


@pytest.fixture(scope="module")
def rollout_ctx():
    from transformers import AutoTokenizer

    from neuroagent.agent.config import load_agent_config
    from neuroagent.agent.orchestrator import AgentOrchestrator
    from neuroagent.rules.rules_engine import RulesEngine
    from neuroagent.tools.tool_registry import ToolRegistry
    from neuroagent.training.rollout.react_rollout import ReactRollout
    from neuroagent.training.train_grpo import _agent_tool_definitions

    tok = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
    rules = RulesEngine(
        str(REPO / "agent-platform/config/hospital_rules"), hospital="de_charite"
    )
    orch = AgentOrchestrator(
        load_agent_config(hospital="de_charite"),
        ToolRegistry.create_default_registry(),
        rules,
    )
    tools = _agent_tool_definitions()
    rollout = ReactRollout(
        tokenizer=tok, tools=tools, system_prompt=orch._build_system_prompt()
    )
    return tok, rollout


def _canned(tok, turns):
    eos = tok.eos_token_id
    seqs = [tok(t, add_special_tokens=False)["input_ids"] + [eos] for t in turns]
    it = iter(seqs)
    return lambda ids: next(it)


def _case():
    from neuroagent_schemas import NeuroBenchCase

    p = REPO / "data/neurobench/cases/ALS-M01.json"
    return NeuroBenchCase.model_validate(json.loads(p.read_text()))


def _run(tok, rollout, turns):
    from neuroagent.evaluation.runner import format_patient_info
    from neuroagent.tools.cost_tracker import CostTracker
    from neuroagent.tools.mock_server import MockServer

    case = _case()
    return case, rollout.rollout_one(
        case=case,
        patient_info=format_patient_info(case),
        generate_fn=_canned(tok, turns),
        mock_server=MockServer(case),
        cost_tracker=CostTracker(),
    )


T1_MRI = (
    "Bulbar onset suggests ALS.\n</think>\n\n<tool_call>\n<function=analyze_brain_mri>\n"
    "<parameter=clinical_context>bulbar weakness</parameter>\n</function>\n</tool_call>"
)
T2_EMG = (
    "Now EMG.\n</think>\n\n<tool_call>\n<function=order_specialized_test>\n"
    "<parameter=test_type>emg_ncs</parameter>\n</function>\n</tool_call>"
)
T_CONCLUDE = (
    "Confirmed.\n</think>\n\n### Primary Diagnosis\nAmyotrophic lateral sclerosis (ALS)"
)


def test_mask_length_matches_completion(rollout_ctx):
    tok, rollout = rollout_ctx
    _, res = _run(tok, rollout, [T1_MRI, T_CONCLUDE])
    assert len(res.completion_ids) == len(res.env_mask)


def test_model_tokens_are_generated_tool_tokens_are_masked(rollout_ctx):
    tok, rollout = rollout_ctx
    _, res = _run(tok, rollout, [T1_MRI, T2_EMG, T_CONCLUDE])
    model_txt = tok.decode([t for t, m in zip(res.completion_ids, res.env_mask) if m == 1])
    tool_txt = tok.decode([t for t, m in zip(res.completion_ids, res.env_mask) if m == 0])
    # The policy's own tokens carry the reasoning and the tool CALLS…
    assert "bulbar" in model_txt.lower() and "emg" in model_txt.lower()
    assert "Primary Diagnosis" in model_txt
    # …but never a tool RESPONSE (those are masked out of the loss).
    assert "tool_response" not in model_txt
    assert "tool_response" in tool_txt


def test_tools_executed_and_trace_scored(rollout_ctx):
    tok, rollout = rollout_ctx
    case, res = _run(tok, rollout, [T1_MRI, T2_EMG, T_CONCLUDE])
    assert res.trace.tools_called == ["analyze_brain_mri", "order_specialized_test"]
    assert res.num_tool_calls == 2
    assert not res.truncated
    # final_response is the committed, think-free assessment.
    assert "<think>" not in (res.trace.final_response or "")
    assert "lateral sclerosis" in (res.trace.final_response or "").lower()


def test_reconstruction_is_template_exact_at_seams(rollout_ctx):
    tok, rollout = rollout_ctx
    _, res = _run(tok, rollout, [T1_MRI, T_CONCLUDE])
    full = tok.decode(res.prompt_ids + res.completion_ids)
    # The turn seam matches the serving render exactly: assistant closes, newline, tool turn.
    assert "</tool_call><|im_end|>\n<|im_start|>user\n<tool_response>" in full
    # Reasoning is preserved in history (reflection off → no think-stripping).
    assert "<think>" in full


def test_reward_scores_real_trajectory(rollout_ctx):
    tok, rollout = rollout_ctx
    from neuroagent.training.rewards.composite_reward import CompositeReward

    case, res = _run(tok, rollout, [T1_MRI, T2_EMG, T_CONCLUDE])
    comp = CompositeReward.from_config(
        str(REPO / "agent-platform/config/training/reward_weights_grpo.yaml"),
        str(REPO / "agent-platform/config/tools/costs.yaml"),
        str(REPO / "agent-platform/config/hospital_rules"),
        "de_charite",
    )
    reward = comp.compute(res.trace, case)
    assert -1.0 <= reward <= 1.0
    # A think-only, no-tool trajectory must score strictly lower (the leak is closed).
    _, empty = _run(tok, rollout, ["I am unsure.\n</think>\n\nI need more information."])
    assert comp.compute(empty.trace, case) < reward
