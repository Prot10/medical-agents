"""Tests for the agent orchestrator (unit tests, no LLM required)."""

import json
from pathlib import Path

import pytest

from neuroagent.agent.orchestrator import (
    AgentConfig,
    AgentConfigError,
    AgentOrchestrator,
    _extract_assessment,
    load_agent_config,
)
from neuroagent.agent.reasoning import AgentTrace, AgentTurn
from neuroagent.agent.reflection import get_reflection_prompt
from neuroagent.agent.planner import restrict_tools, get_forced_tool_order
from neuroagent.llm.client import LLMClient, ThinkTagStreamParser, strip_think_tags
from neuroagent.tools.tool_registry import ToolRegistry
from neuroagent.tools.mock_server import MockServer
from neuroagent_schemas import NeuroBenchCase


@pytest.fixture
def sample_case() -> NeuroBenchCase:
    fixture_path = Path(__file__).parent / "fixtures" / "sample_case.json"
    data = json.loads(fixture_path.read_text())
    return NeuroBenchCase.model_validate(data)


@pytest.fixture
def config():
    return load_agent_config(model="test-model", max_turns=5)


class TestAgentConfig:
    def test_requires_explicit_values(self):
        with pytest.raises(TypeError):
            AgentConfig()

    def test_loads_runtime_yaml(self):
        cfg = load_agent_config()
        assert cfg.max_turns == 15
        assert cfg.enable_reflection is True
        assert cfg.model == "Qwen/Qwen3.5-9B"

    def test_loads_with_overrides(self):
        cfg = load_agent_config(model="custom-model", max_turns=10, enable_reflection=False)
        assert cfg.model == "custom-model"
        assert cfg.max_turns == 10
        assert cfg.enable_reflection is False

    def test_rejects_missing_yaml_keys(self, tmp_path):
        config_path = tmp_path / "agent.yaml"
        config_path.write_text(
            """
llm:
  base_url: "http://localhost:8000/v1"
  api_key: "not-needed"
agent:
  max_turns: 15
  enable_reflection: true
  allowed_tools: null
  excluded_tools: null
  all_info_upfront: false
rules:
  hospital: "us_mayo"
"""
        )

        with pytest.raises(AgentConfigError, match="llm.model"):
            load_agent_config(config_path)

    def test_loads_seed_and_client_robustness_settings(self):
        cfg = load_agent_config()
        assert cfg.seed == 42
        assert cfg.request_timeout == 120.0
        assert cfg.max_retries == 2

    def test_seed_can_be_disabled(self):
        cfg = load_agent_config(seed=None)
        assert cfg.seed is None

    def test_rejects_non_integer_seed(self):
        with pytest.raises(AgentConfigError, match="seed"):
            load_agent_config(seed="not-a-seed")

    def test_rejects_non_positive_timeout(self):
        with pytest.raises(AgentConfigError, match="request_timeout"):
            load_agent_config(request_timeout=0)

    def test_rejects_negative_retries(self):
        with pytest.raises(AgentConfigError, match="max_retries"):
            load_agent_config(max_retries=-1)


class TestAgentTrace:
    def test_empty_trace(self):
        trace = AgentTrace()
        assert trace.turns == []
        assert trace.total_tool_calls == 0
        assert trace.final_response is None

    def test_add_turns(self):
        trace = AgentTrace(case_id="test")
        trace.add_assistant_turn(1, "thinking...", None)
        trace.add_tool_turn(2, "analyze_eeg", {"tool_name": "analyze_eeg", "success": True})
        trace.add_assistant_turn(3, "conclusion", None)
        trace.set_final_response("diagnosis")

        assert len(trace.turns) == 3
        assert trace.total_tool_calls == 1
        assert trace.tools_called == ["analyze_eeg"]
        assert trace.final_response == "diagnosis"

    def test_timer(self):
        trace = AgentTrace()
        trace.start_timer()
        trace.stop_timer()
        assert trace.elapsed_time_seconds >= 0


class TestReflection:
    def test_get_prompt(self):
        prompt = get_reflection_prompt()
        assert prompt["role"] == "user"
        assert "reasoning" in prompt["content"].lower()


class TestSystemPromptAssembly:
    class FakeRules:
        def get_context(self):
            return "Protocol A\nMANDATORY: analyze_eeg"

    class EmptyRules:
        def get_context(self):
            return ""

    def test_initial_messages_use_system_then_user(self, config):
        agent = AgentOrchestrator(config=config, tool_registry=ToolRegistry())

        messages = agent._build_initial_messages("Patient presentation")

        assert [m["role"] for m in messages] == ["system", "user"]
        assert "NeuroAgent" in messages[0]["content"]
        assert messages[1]["content"] == "Patient presentation"

    def test_system_prompt_injects_rules_context(self, config):
        agent = AgentOrchestrator(
            config=config,
            tool_registry=ToolRegistry(),
            rules_engine=self.FakeRules(),
        )

        prompt = agent._build_system_prompt()

        assert "## Hospital Protocols" in prompt
        assert "Protocol A" in prompt
        assert "MANDATORY: analyze_eeg" in prompt

    def test_system_prompt_skips_empty_rules_context(self, config):
        agent = AgentOrchestrator(
            config=config,
            tool_registry=ToolRegistry(),
            rules_engine=self.EmptyRules(),
        )

        prompt = agent._build_system_prompt()

        assert "## Hospital Protocols" not in prompt


class TestPlanner:
    def test_restrict_allowed(self):
        defs = [
            {"function": {"name": "a"}},
            {"function": {"name": "b"}},
            {"function": {"name": "c"}},
        ]
        result = restrict_tools(defs, allowed_tools=["a", "c"])
        assert len(result) == 2

    def test_restrict_excluded(self):
        defs = [
            {"function": {"name": "a"}},
            {"function": {"name": "b"}},
        ]
        result = restrict_tools(defs, excluded_tools=["a"])
        assert len(result) == 1
        assert result[0]["function"]["name"] == "b"

    def test_forced_order_random(self):
        tools = ["a", "b", "c", "d"]
        result = get_forced_tool_order(tools, strategy="random")
        assert sorted(result) == sorted(tools)

    def test_forced_order_reverse(self):
        tools = ["a", "b", "c"]
        result = get_forced_tool_order(tools, strategy="reverse")
        assert result == ["c", "b", "a"]


class TestStripThinkTags:
    def test_full_think_block(self):
        text = "<think>internal reasoning here</think>\n\nVisible output"
        assert strip_think_tags(text) == "Visible output"

    def test_multiline_think_block(self):
        text = "<think>\nLine 1\nLine 2\nLine 3\n</think>\n\nAnswer"
        assert strip_think_tags(text) == "Answer"

    def test_orphaned_closing_tag(self):
        text = "Some reasoning\n</think>\n\nActual response"
        result = strip_think_tags(text)
        assert "</think>" not in result
        assert "Some reasoning" in result
        assert "Actual response" in result

    def test_no_think_tags(self):
        text = "Normal response without any tags"
        assert strip_think_tags(text) == text

    def test_multiple_think_blocks(self):
        text = "<think>first</think>middle<think>second</think>end"
        assert strip_think_tags(text) == "middleend"

    def test_empty_think_block(self):
        text = "<think></think>content"
        assert strip_think_tags(text) == "content"

    def test_think_with_react_pattern(self):
        """Real-world pattern: model outputs THINK label after think tags."""
        text = (
            "<think>\nLet me analyze the EEG results...\n</think>\n\n"
            "**THINK**: The EEG shows right temporal sharp waves.\n\n"
            "**ACT**:"
        )
        result = strip_think_tags(text)
        assert "<think>" not in result
        assert "</think>" not in result
        assert "**THINK**" in result  # ReAct THINK label should remain


def _run_parser(chunks: list[str]) -> tuple[str, str]:
    """Feed chunks through the parser; return (content, think) accumulations."""
    parser = ThinkTagStreamParser()
    content, think = [], []
    for chunk in chunks:
        for kind, piece in parser.feed(chunk):
            (think if kind == "think" else content).append(piece)
    for kind, piece in parser.flush():
        (think if kind == "think" else content).append(piece)
    return "".join(content), "".join(think)


class TestThinkTagStreamParser:
    def test_plain_content(self):
        content, think = _run_parser(["Hello ", "world"])
        assert content == "Hello world"
        assert think == ""

    def test_simple_think_block(self):
        content, think = _run_parser(["<think>", "reasoning", "</think>", "answer"])
        assert content == "answer"
        assert think == "reasoning"

    def test_open_tag_split_across_chunks(self):
        content, think = _run_parser(["<th", "ink>reason", "ing</thi", "nk>answer"])
        assert content == "answer"
        assert think == "reasoning"

    def test_both_tags_in_one_chunk_keeps_trailing_content(self):
        # The old per-delta check dropped "answer" when both tags arrived together.
        content, think = _run_parser(["<think>reasoning</think>answer"])
        assert content == "answer"
        assert think == "reasoning"

    def test_content_before_open_tag_in_same_chunk(self):
        content, think = _run_parser(["pre<think>mid</think>post"])
        assert content == "prepost"
        assert think == "mid"

    def test_orphaned_closing_tag_is_stripped(self):
        content, think = _run_parser(["some text</th", "ink>answer"])
        assert "</think>" not in content
        assert content == "some textanswer"
        assert think == ""

    def test_false_partial_tag_is_released(self):
        # "<thermal" starts like "<think>" but is ordinary content.
        content, think = _run_parser(["a <th", "ermal issue"])
        assert content == "a <thermal issue"
        assert think == ""

    def test_unclosed_think_flushes_as_think(self):
        content, think = _run_parser(["<think>never closed"])
        assert content == ""
        assert think == "never closed"

    def test_trailing_partial_tag_flushes_as_text(self):
        content, think = _run_parser(["answer<thi"])
        assert content == "answer<thi"

    def test_multiple_think_blocks(self):
        content, think = _run_parser(
            ["<think>one</think>a", "<think>", "two</think>b"]
        )
        assert content == "ab"
        assert think == "onetwo"


class TestLLMClientRequestParams:
    """Seed / timeout / retries plumbing without a live server."""

    class _FakeCompletions:
        def __init__(self):
            self.last_kwargs = None

        def create(self, **kwargs):
            self.last_kwargs = kwargs

            class _Msg:
                content = "ok"
                tool_calls = None

            class _Choice:
                message = _Msg()

            class _Resp:
                choices = [_Choice()]
                usage = None

            return _Resp()

    def _client_with_fake(self, **client_kwargs):
        client = LLMClient(base_url="http://localhost:1/v1", **client_kwargs)
        fake = self._FakeCompletions()
        client.client.chat.completions = fake
        return client, fake

    def test_seed_sent_when_set(self):
        client, fake = self._client_with_fake(seed=42)
        client.chat(messages=[{"role": "user", "content": "hi"}])
        assert fake.last_kwargs["seed"] == 42

    def test_seed_omitted_when_unset(self):
        client, fake = self._client_with_fake()
        client.chat(messages=[{"role": "user", "content": "hi"}])
        assert "seed" not in fake.last_kwargs

    def test_timeout_and_retries_configure_openai_client(self):
        client = LLMClient(
            base_url="http://localhost:1/v1", timeout=33.0, max_retries=5
        )
        assert client.client.timeout == 33.0
        assert client.client.max_retries == 5

    def test_malformed_tool_arguments_fall_back_to_empty_dict(self):
        client = LLMClient(base_url="http://localhost:1/v1")

        class _Func:
            name = "analyze_eeg"
            arguments = "{not valid json"

        class _TC:
            id = "call_1"
            function = _Func()

        class _Msg:
            content = None
            tool_calls = [_TC()]

        class _Choice:
            message = _Msg()

        class _Resp:
            choices = [_Choice()]
            usage = None

        parsed = client._parse_response(_Resp())
        assert parsed.tool_calls[0].arguments == {}


class TestExtractAssessment:
    def test_extracts_from_reasoning(self):
        text = (
            "**THINK**: Some reasoning here...\n\n"
            "**ACT**: Provide final assessment.\n\n"
            "### Primary Diagnosis\n"
            "Focal epilepsy (Confidence: 0.95)\n\n"
            "### Recommendations\n"
            "1. Start levetiracetam"
        )
        result = _extract_assessment(text)
        assert result.startswith("### Primary Diagnosis")
        assert "THINK" not in result
        assert "Focal epilepsy" in result
        assert "levetiracetam" in result

    def test_no_structured_section_returns_full(self):
        text = "The diagnosis is focal epilepsy with DNET."
        result = _extract_assessment(text)
        assert result == text

    def test_empty_string(self):
        assert _extract_assessment("") == ""

    def test_preserves_all_sections(self):
        text = (
            "Reasoning preamble\n\n"
            "### Primary Diagnosis\nDiag\n\n"
            "### Differential Diagnoses\n1. Alt1\n\n"
            "### Key Evidence\n- Finding\n\n"
            "### Recommendations\n1. Rec\n\n"
            "### Red Flags / Alerts\n- Alert"
        )
        result = _extract_assessment(text)
        assert "### Primary Diagnosis" in result
        assert "### Red Flags" in result
        assert "Reasoning preamble" not in result

    def test_max_turns_no_structure(self):
        """Edge case: agent hit max turns mid-reasoning, no structured output."""
        text = "**THINK**: I need more data but I've run out of turns..."
        result = _extract_assessment(text)
        assert result == text.strip()
