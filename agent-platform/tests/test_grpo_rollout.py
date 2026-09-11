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
    assert seq.prompt_ids == records[0].prompt_ids  # the canonical prompt, not the retry's corrected one


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


def test_engine_client_streams_turns_without_a_barrier():
    """A slow episode must not hold up a fast one: turns are submitted as they arrive and the batch is stepped continuously."""
    import threading
    from types import SimpleNamespace

    from neuroagent.training.train_grpo import BatchedEngineClient

    class Engine:
        def __init__(self):
            self.queue = {}
            self.timeline = []

        def add_request(self, request_id, prompt, params):
            # request ids carry the number of engine steps this turn takes
            self.queue[request_id] = [int(prompt.split(":")[1]), prompt]

        def step(self):
            import time

            time.sleep(0.01)  # a real decode step dwarfs the episode threads' bookkeeping
            self.steps = getattr(self, "steps", 0) + 1
            outs = []
            for rid, entry in list(self.queue.items()):
                entry[0] -= 1
                if entry[0] <= 0:
                    del self.queue[rid]
                    self.timeline.append((rid, self.steps))
                    outs.append(SimpleNamespace(
                        request_id=rid, finished=True, prompt_token_ids=[1, 2],
                        outputs=[SimpleNamespace(token_ids=[7], text="ok", logprobs=[{7: SimpleNamespace(logprob=-0.1)}], finish_reason="stop")],
                    ))
            return outs

    class Tok:
        def apply_chat_template(self, messages, **_):
            return messages[-1]["content"]

        def decode(self, ids, **_):
            return "ok"

    class Parser:
        def __init__(self, *_, **__):
            pass

        def extract_tool_calls(self, text, request):
            return SimpleNamespace(content=text, tool_calls=[])

    client = object.__new__(BatchedEngineClient)
    client.engine, client.tokenizer, client.parser_cls = Engine(), Tok(), Parser
    client.request_cls = lambda **kw: SimpleNamespace(tools=kw.get("tools"))
    client.template_kwargs, client.sampling, client.records = {}, None, {}
    client.engine_steps = client.max_inflight = 0
    client._pending, client._live, client._cv = {}, set(), threading.Condition()
    from collections import defaultdict
    client.records = defaultdict(list)

    def episode(name, costs):
        client.episode_started()
        try:
            for cost in costs:
                client.chat([{"role": "user", "content": f"{name}:{cost}"}])
        finally:
            client.episode_finished()

    threads = [threading.Thread(target=episode, args=("fast", [1, 1, 1])), threading.Thread(target=episode, args=("slow", [6]))]
    for t in threads:
        t.start()
    client.serve_until_done(2)
    for t in threads:
        t.join()
    # The fast episode's three turns were all served while the slow turn (6 engine steps) was
    # still generating; a per-turn barrier would have needed 8 steps.
    slow_thread = next(thread for thread, recs in client.records.items() if len(recs) == 1)
    finished_at = {rid: step for rid, step in client.engine.timeline}
    assert sorted(len(recs) for recs in client.records.values()) == [1, 3]
    assert max(step for rid, step in finished_at.items() if not rid.startswith(f"{slow_thread}-")) <= 6
    assert client.engine_steps == 6 and client.max_inflight == 2


def test_archive_adapter_keeps_the_adapter_out_of_the_rotation(tmp_path):
    from neuroagent.training.train_grpo import archive_adapter

    checkpoint = tmp_path / "checkpoint-25"
    checkpoint.mkdir()
    (checkpoint / "adapter_config.json").write_text("{}")
    (checkpoint / "adapter_model.safetensors").write_bytes(b"weights")
    (checkpoint / "optimizer.pt").write_bytes(b"optimizer")
    archived = archive_adapter(checkpoint, tmp_path / "adapters")
    assert archived == tmp_path / "adapters" / "checkpoint-25"
    assert sorted(path.name for path in archived.iterdir()) == ["adapter_config.json", "adapter_model.safetensors"]
    assert (archived / "adapter_model.safetensors").read_bytes() == b"weights"


def test_weights_are_refused_on_the_local_disk():
    import pytest

    from neuroagent.training.train_grpo import WEIGHTS_ROOT, require_eos

    assert require_eos(f"{WEIGHTS_ROOT}/run/qwen3.5-9b") == Path(f"{WEIGHTS_ROOT}/run/qwen3.5-9b")
    for local in ("outputs/grpo/run/train", "/home/user/weights", "/dev/shm/weights", "/eosx/run"):
        with pytest.raises(ValueError, match="must be written on EOS"):
            require_eos(local)
