"""The text SFT trains on must be the text the served model sees.

Two silent divergences existed here, and neither would have failed a single test:

* the agent passes `tools=` to vLLM, which renders a ~3k-token `# Tools` schema block into
  the system message; SFT rendered the same trajectory with no tools at all;
* the agent stripped `<think>` before appending an assistant turn to the history, so Qwen's
  template emitted an empty `<think></think>` for every prior turn, while the trajectory the
  student trained on carried the reasoning in full.

A student trained on prompt A and served prompt B is not the model you evaluated. These
tests render both with the real tokenizer and require them to agree.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import pytest

os.environ.setdefault("HF_HOME", "/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface")

from neuroagent.agent.orchestrator import AgentOrchestrator
from neuroagent.llm.client import LLMResponse, LLMToolCall, extract_think_content
from neuroagent.llm.prompts import apply_reasoning_style
from neuroagent.training.chat_template import apply_training_chat_template
from neuroagent.training.train_grpo import _agent_tool_definitions, _log_sequence_stats

MODEL = "Qwen/Qwen3.5-9B"
REPO_ROOT = Path(__file__).resolve().parents[2]
TRAJECTORIES = REPO_ROOT / "training_data/gold_trajectories/trajectories.jsonl"
TRAIN_SPLIT = REPO_ROOT / "data/neurobench/splits/train_cases.txt"

# Deterministic sample stride: checking only trajectories[0] once let a format bug
# in trajectory 2..N ship; every 50th trajectory spreads the check across cases,
# styles, and hospitals at negligible cost.
SAMPLE_STRIDE = 50

# A turn with more than one <think> block cannot round-trip byte-identically:
# the serving stack merges all think blocks into one (`extract_think_content`
# joins them; the orchestrator re-embeds a single block). 7 such teacher traces
# existed and were normalized in-place to the merged serving form; this guard
# keeps new ones out.


def _has_multi_think_turn(trajectory: dict) -> bool:
    return any(
        m["role"] == "assistant" and (m["content"] or "").count("<think>") > 1
        for m in trajectory["messages"]
    )


def _tokenizer():
    transformers = pytest.importorskip("transformers")
    try:
        return transformers.AutoTokenizer.from_pretrained(
            MODEL, trust_remote_code=True, local_files_only=True
        )
    except Exception as exc:  # noqa: BLE001 - the weights simply are not on this box
        pytest.skip(f"{MODEL} tokenizer not cached locally: {exc}")


def _vllm_normalize(messages: list[dict]) -> list[dict]:
    """What vLLM does to an outbound request before templating (chat_utils.py)."""
    out = []
    for message in messages:
        message = dict(message)
        if message.get("role") == "assistant" and message.get("tool_calls"):
            calls = []
            for call in message["tool_calls"]:
                call = json.loads(json.dumps(call))
                args = call["function"].get("arguments")
                if isinstance(args, str):
                    call["function"]["arguments"] = json.loads(args) if args else {}
                calls.append(call)
            message["tool_calls"] = calls
        out.append(message)
    return out


class TestReasoningSurvivesTheRoundTrip:
    def test_extract_think_content_returns_the_body(self):
        assert extract_think_content("<think>\nweigh the EMG\n</think>\n\nanswer") == "weigh the EMG"

    def test_no_think_block_is_none(self):
        assert extract_think_content("just an answer") is None

    def test_assistant_message_carries_reasoning_back_into_content(self):
        response = LLMResponse(
            content="Ordering an EMG.",
            reasoning="Mixed UMN and LMN signs point to motor neuron disease.",
            tool_calls=[LLMToolCall(id="c1", name="analyze_eeg", arguments={})],
        )
        message = AgentOrchestrator._format_assistant_message(None, response, response.tool_calls)

        assert message["content"].startswith("<think>\n")
        assert "Mixed UMN and LMN signs" in message["content"]
        assert message["content"].endswith("Ordering an EMG.")

    def test_a_response_without_reasoning_is_left_alone(self):
        response = LLMResponse(content="Ordering an EMG.")
        message = AgentOrchestrator._format_assistant_message(None, response, [])
        assert message["content"] == "Ordering an EMG."
        assert "<think>" not in message["content"]


@pytest.mark.skipif(not TRAJECTORIES.exists(), reason="gold trajectories not present")
class TestTrainingPromptEqualsServingPrompt:
    @pytest.fixture(scope="class")
    def trajectories_sample(self) -> list[dict]:
        """Every SAMPLE_STRIDE-th trajectory — a deterministic spread, not just [0]."""
        lines = [l for l in TRAJECTORIES.read_text().splitlines() if l.strip()]
        sample = [json.loads(lines[i]) for i in range(0, len(lines), SAMPLE_STRIDE)]
        assert sample, "trajectories.jsonl is empty"
        return sample

    def test_training_renders_the_tool_schemas(self, trajectories_sample):
        """Without the tools column the student never sees the functions it must call."""
        tok = _tokenizer()
        tools = _agent_tool_definitions()

        for trajectory in trajectories_sample:
            without = tok.apply_chat_template(trajectory["messages"], tokenize=False)
            with_tools = tok.apply_chat_template(
                trajectory["messages"], tokenize=False, tools=tools
            )

            assert "# Tools" not in without
            assert "# Tools" in with_tools, trajectory["case_id"]
            for name in ("analyze_brain_mri", "order_specialized_test", "check_drug_interactions"):
                assert name in with_tools, trajectory["case_id"]

    def test_serving_history_reproduces_the_training_text(self, trajectories_sample):
        """Replay each trajectory as the orchestrator would build it, and compare renderings."""
        tok = _tokenizer()
        tools = _agent_tool_definitions()

        for trajectory in trajectories_sample:
            served: list[dict] = []
            for message in trajectory["messages"]:
                if message["role"] != "assistant":
                    served.append(message)
                    continue
                # The client splits reasoning out of content; the orchestrator puts it back.
                reasoning = extract_think_content(message["content"] or "")
                response = LLMResponse(
                    content=(message["content"] or "").split("</think>")[-1].lstrip(),
                    reasoning=reasoning,
                    tool_calls=[
                        LLMToolCall(id=f"c{i}", name=c["function"]["name"], arguments=c["function"]["arguments"])
                        for i, c in enumerate(message.get("tool_calls") or [])
                    ],
                )
                served.append(
                    AgentOrchestrator._format_assistant_message(None, response, response.tool_calls)
                )

            training_text = tok.apply_chat_template(trajectory["messages"], tokenize=False, tools=tools)
            serving_text = tok.apply_chat_template(_vllm_normalize(served), tokenize=False, tools=tools)

            assert "<think>\n\n</think>" not in serving_text, (
                f"{trajectory['case_id']}: reasoning was dropped from history"
            )
            assert serving_text == training_text, trajectory["case_id"]

    def test_no_multi_think_turns(self):
        """Every assistant turn carries at most one <think> block. Serving merges
        multiple blocks into one, so a multi-think trajectory is a parity bug."""
        lines = [l for l in TRAJECTORIES.read_text().splitlines() if l.strip()]
        offenders = [
            (t["case_id"], t["style"])
            for t in map(json.loads, lines)
            if _has_multi_think_turn(t)
        ]
        assert not offenders, offenders

    def test_assistant_only_mask_covers_reasoning_and_excludes_observations(
        self, trajectories_sample
    ):
        tok = _tokenizer()
        apply_training_chat_template(tok)
        tools = _agent_tool_definitions()

        for trajectory in trajectories_sample:
            encoded = tok.apply_chat_template(
                trajectory["messages"],
                tools=tools,
                tokenize=True,
                return_dict=True,
                return_assistant_tokens_mask=True,
            )
            mask, ids = encoded["assistant_masks"], encoded["input_ids"]
            assert sum(mask) > 0, (
                f"{trajectory['case_id']}: assistant_only_loss would train on nothing"
            )

            in_loss = tok.decode([t for t, m in zip(ids, mask) if m])
            assert "<think>" in in_loss, (
                f"{trajectory['case_id']}: the student is not trained on its own reasoning"
            )

            observation = next(
                m["content"] for m in trajectory["messages"] if m["role"] == "tool"
            )
            obs_lines = [l.strip() for l in observation.strip().splitlines() if l.strip()]
            distinctive = obs_lines[min(3, len(obs_lines) - 1)][:24]
            assert distinctive and distinctive not in in_loss, (
                f"{trajectory['case_id']}: loss lands on a tool observation"
            )

    def test_truncation_boundary_cuts_the_final_assistant_segment_loudly(
        self, trajectories_sample, caplog
    ):
        """A sequence over max_seq_length loses its TAIL — the final diagnosis.

        Verifies both halves of the contract: (a) the tokens beyond the boundary
        really are the final assistant segment (so silent truncation would cut
        the answer, not padding), and (b) `_log_sequence_stats` reports the cut
        loudly before training, and stays quiet when everything fits.
        """
        tok = _tokenizer()
        tools = _agent_tool_definitions()
        trajectory = trajectories_sample[0]

        text = tok.apply_chat_template(trajectory["messages"], tokenize=False, tools=tools)
        ids = tok(text, add_special_tokens=False).input_ids
        n_tokens = len(ids)

        # (a) The tail of the token stream is final-assistant content: truncating
        # just below the full length must eat into the last assistant message.
        tail_text = tok.decode(ids[-40:])
        final_assistant = trajectory["messages"][-1]["content"]
        assert any(
            chunk and chunk in final_assistant
            for chunk in (tail_text[i:i + 12] for i in range(0, len(tail_text) - 12, 6))
        ), "the sequence tail is not the final assistant segment"

        rows = [{"messages": trajectory["messages"], "tools": tools}]
        logger_name = "neuroagent.training.train_grpo"

        # (b) One token short of the full length → the cut is reported loudly.
        with caplog.at_level(logging.INFO, logger=logger_name):
            _log_sequence_stats(rows, tok, max_seq_length=n_tokens - 1, tools=tools)
        assert any(
            "WILL BE TRUNCATED" in r.getMessage() for r in caplog.records
        ), "an over-length trajectory was not reported"

        caplog.clear()
        with caplog.at_level(logging.INFO, logger=logger_name):
            _log_sequence_stats(rows, tok, max_seq_length=n_tokens, tools=tools)
        assert not any("WILL BE TRUNCATED" in r.getMessage() for r in caplog.records)
        assert any("No truncation" in r.getMessage() for r in caplog.records)


@pytest.mark.skipif(not TRAJECTORIES.exists(), reason="gold trajectories not present")
class TestReasoningStyleParity:
    """The style directive the agent appends must reproduce the trajectory system prompts.

    Every case appears in two styles. efficient_linear = the base prompt (concise, the
    inference default); differential_reasoned = base + the exclusion-reasoning directive. If
    the agent's `apply_reasoning_style` does not reproduce the exact stored prompt, the SFT
    model is served a prompt it was not trained on — the class of bug this whole module exists
    to prevent, now for the system prompt itself.
    """

    @pytest.fixture(scope="class")
    def trajectories(self) -> list[dict]:
        return [
            json.loads(line)
            for line in TRAJECTORIES.read_text().splitlines()
            if line.strip()
        ]

    @pytest.fixture(scope="class")
    def style_pairs(self) -> dict:
        from collections import defaultdict

        by_case = defaultdict(dict)
        for line in TRAJECTORIES.read_text().splitlines():
            if not line.strip():
                continue
            t = json.loads(line)
            by_case[t["case_id"]][t["style"]] = t["messages"][0]["content"]
        return {c: s for c, s in by_case.items() if len(s) == 2}

    @pytest.mark.skipif(not TRAIN_SPLIT.exists(), reason="train split file not present")
    def test_every_case_has_both_styles(self, style_pairs):
        """Both styles exist for every TRAIN-split case — size derived from the
        split file, not hardcoded, so a regenerated/expanded split keeps this honest."""
        train_ids = {c for c in TRAIN_SPLIT.read_text().split() if c}
        assert len(style_pairs) == len(train_ids)
        assert set(style_pairs) == train_ids

    def test_directive_present_exactly_for_differential(self, trajectories):
        """The directive marks differential trajectories and only those."""
        marker = "## Reasoning Approach"
        for t in trajectories:
            has = marker in t["messages"][0]["content"]
            expect = t["style"] == "differential_reasoned"
            assert has == expect, f"{t['case_id']} {t['style']}: directive present={has}"

    def test_the_agent_appends_the_directive_where_it_is_stored(self, trajectories):
        """`apply_reasoning_style` reproduces each trajectory's own prompt idempotently.

        Applying the trajectory's own style to its own prompt must be a fixed point — the
        directive is already where the orchestrator would put it (before hospital protocols),
        so re-applying changes nothing. This ties the stored prompt to the agent's transform
        without assuming the two styles of a case share a hospital context (373 do not).
        """
        mismatches = []
        for t in trajectories:
            prompt = t["messages"][0]["content"]
            if apply_reasoning_style(prompt, t["style"]) != prompt:
                mismatches.append((t["case_id"], t["style"]))
        assert mismatches == [], mismatches[:5]

    def test_directive_sits_immediately_before_hospital_protocols(self, trajectories):
        """When a differential prompt has hospital rules, the directive precedes them."""
        for t in trajectories:
            prompt = t["messages"][0]["content"]
            if t["style"] != "differential_reasoned" or "## Hospital Protocols" not in prompt:
                continue
            before = prompt.split("## Hospital Protocols")[0]
            assert "## Reasoning Approach" in before, f"{t['case_id']}: directive after protocols"

    def test_no_identical_prompt_conflicts_remain(self, style_pairs):
        """The 127 same-prompt pairs are gone: the two styles now differ for every case."""
        collisions = [c for c, p in style_pairs.items()
                      if p["efficient_linear"] == p["differential_reasoned"]]
        assert collisions == [], collisions[:5]
