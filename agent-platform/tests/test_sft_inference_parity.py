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
import os
from pathlib import Path

import pytest

os.environ.setdefault("HF_HOME", "/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface")

from neuroagent.agent.orchestrator import AgentOrchestrator
from neuroagent.llm.client import LLMResponse, LLMToolCall, extract_think_content
from neuroagent.llm.prompts import apply_reasoning_style
from neuroagent.training.chat_template import apply_training_chat_template
from neuroagent.training.train_grpo import _agent_tool_definitions

MODEL = "Qwen/Qwen3.5-9B"
TRAJECTORIES = Path(__file__).resolve().parents[2] / "training_data/gold_trajectories/trajectories.jsonl"


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
    def trajectory(self) -> dict:
        return json.loads(TRAJECTORIES.read_text().splitlines()[0])

    def test_training_renders_the_tool_schemas(self, trajectory):
        """Without the tools column the student never sees the functions it must call."""
        tok = _tokenizer()
        tools = _agent_tool_definitions()

        without = tok.apply_chat_template(trajectory["messages"], tokenize=False)
        with_tools = tok.apply_chat_template(trajectory["messages"], tokenize=False, tools=tools)

        assert "# Tools" not in without
        assert "# Tools" in with_tools
        for name in ("analyze_brain_mri", "order_specialized_test", "check_drug_interactions"):
            assert name in with_tools

    def test_serving_history_reproduces_the_training_text(self, trajectory):
        """Replay the trajectory as the orchestrator would build it, and compare renderings."""
        tok = _tokenizer()
        tools = _agent_tool_definitions()

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

        assert "<think>\n\n</think>" not in serving_text, "reasoning was dropped from history"
        assert serving_text == training_text

    def test_assistant_only_mask_covers_reasoning_and_excludes_observations(self, trajectory):
        tok = _tokenizer()
        apply_training_chat_template(tok)
        encoded = tok.apply_chat_template(
            trajectory["messages"],
            tools=_agent_tool_definitions(),
            tokenize=True,
            return_dict=True,
            return_assistant_tokens_mask=True,
        )
        mask, ids = encoded["assistant_masks"], encoded["input_ids"]
        assert sum(mask) > 0, "assistant_only_loss would train on nothing"

        in_loss = tok.decode([t for t, m in zip(ids, mask) if m])
        assert "<think>" in in_loss, "the student is not trained on its own reasoning"

        observation = next(m["content"] for m in trajectory["messages"] if m["role"] == "tool")
        distinctive = observation.strip().splitlines()[3].strip()[:24]
        assert distinctive and distinctive not in in_loss, "loss lands on a tool observation"


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

    def test_every_case_has_both_styles(self, style_pairs):
        assert len(style_pairs) == 500

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
