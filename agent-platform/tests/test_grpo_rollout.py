"""Training-sequence assembly and reward plumbing for GRPO rollouts (no engine needed)."""

from __future__ import annotations

from pathlib import Path

import pytest

from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent.training.train_grpo import TurnRecord, assemble_sequence, make_reward_funcs
from neuroagent_schemas import (
    ActionProposed,
    AssessmentSubmitted,
    ClinicalEpisode,
    NeuroBenchCase,
    RunCompleted,
    RunStarted,
    SubmitAssessment,
)

ROOT = Path(__file__).resolve().parents[2]


class CharTokenizer:
    """One token per character; environment text is tokenized separately from model tokens."""

    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": [ord(c) for c in text]}

    def apply_chat_template(self, messages, tools=None, tokenize=False, add_generation_prompt=False, **kwargs):
        text = "".join(f"<{m['role']}>{m.get('content') or ''}</{m['role']}>" for m in messages)
        return text + ("<assistant>" if add_generation_prompt else "")


def record(prompt_text, raw, messages, tools=()):
    ids = [ord(c) for c in raw]
    return TurnRecord(
        prompt_text=prompt_text, prompt_ids=[ord(c) for c in prompt_text], token_ids=ids,
        logprobs=[-0.5] * len(ids), raw_text=raw, messages=messages, tools=list(tools), finish_reason="stop",
    )


def test_sequence_keeps_model_tokens_and_masks_environment_text():
    tok = CharTokenizer()
    m1 = [{"role": "user", "content": "case"}]
    m2 = m1 + [{"role": "assistant", "content": "CALL"}, {"role": "tool", "content": "obs"}]
    records = [
        record(tok.apply_chat_template(m1, add_generation_prompt=True), "CALL</assistant>", m1),
        record(tok.apply_chat_template(m2, add_generation_prompt=True), "DONE</assistant>", m2),
    ]
    seq = assemble_sequence(tok, records)
    assert seq.prompt_ids == records[0].prompt_ids
    text = "".join(chr(i) for i in seq.completion_ids)
    assert text == "CALL</assistant><tool>obs</tool><assistant>DONE</assistant>"
    assert seq.env_mask == [1] * len("CALL</assistant>") + [0] * len("<tool>obs</tool><assistant>") + [1] * len("DONE</assistant>")
    assert seq.logprobs[: len("CALL</assistant>")] == [-0.5] * len("CALL</assistant>")
    assert seq.conditioning_mismatches == 0 and seq.dropped_retry_tokens == 0 and seq.turns == 2


def test_rerendered_action_mismatch_is_counted_not_fatal():
    tok = CharTokenizer()
    m1 = [{"role": "user", "content": "case"}]
    m2 = m1 + [{"role": "assistant", "content": "call"}, {"role": "tool", "content": "obs"}]
    records = [
        record(tok.apply_chat_template(m1, add_generation_prompt=True), "CALL</assistant>", m1),
        record(tok.apply_chat_template(m2, add_generation_prompt=True), "DONE</assistant>", m2),
    ]
    seq = assemble_sequence(tok, records)
    assert seq.conditioning_mismatches == 1
    assert "".join(chr(i) for i in seq.completion_ids).startswith("CALL</assistant><tool>obs</tool>")


def test_rejected_attempts_are_dropped_and_corrections_do_not_enter_the_sequence():
    tok = CharTokenizer()
    m1 = [{"role": "system", "content": "s"}, {"role": "user", "content": "case"}]
    retry = m1 + [{"role": "user", "content": "The previous response was invalid"}]
    m2 = m1 + [{"role": "assistant", "content": "CALL"}, {"role": "tool", "content": "obs"}]
    records = [
        record(tok.apply_chat_template(m1, add_generation_prompt=True), "prose", m1),          # rejected
        record(tok.apply_chat_template(retry, add_generation_prompt=True), "CALL</assistant>", retry),  # accepted retry
        record(tok.apply_chat_template(m2, add_generation_prompt=True), "DONE</assistant>", m2),
    ]
    seq = assemble_sequence(tok, records)
    text = "".join(chr(i) for i in seq.completion_ids)
    assert text == "CALL</assistant><tool>obs</tool><assistant>DONE</assistant>"
    assert seq.dropped_retry_tokens == len("prose")
    assert seq.conditioning_mismatches == 1  # the accepted retry was conditioned on the correction
    assert seq.turns == 2


def test_reward_funcs_score_episodes_from_the_extra_field():
    case = NeuroBenchCase.model_validate_json((ROOT / "data/neurobench/cases/SE-M02.json").read_text())
    assessment = SubmitAssessment(primary_diagnosis=case.ground_truth.diagnosis.accepted[0], confidence=0.9, urgency="emergent")
    episode = ClinicalEpisode(events=[
        RunStarted(turn=0, case_id=case.case_id, profile_id="p", model_id="m"),
        ActionProposed(turn=1, action=assessment),
        AssessmentSubmitted(turn=1, assessment=assessment),
        RunCompleted(turn=1),
    ])
    funcs = make_reward_funcs({case.case_id: case}, ClinicalPolicyReward(require_approved=False))
    names = [f.__name__ for f in funcs]
    assert names[0] == "policy_scalar" and "diagnosis" in names and names[-1] == "completed"
    values = {f.__name__: f(completions=None, episode=[episode.model_dump_json()])[0] for f in funcs}
    assert values["diagnosis"] == 1.0 and values["completed"] == 1.0
    assert 0 < values["policy_scalar"] < 1
    assert values["required_action_coverage"] == 0.0
