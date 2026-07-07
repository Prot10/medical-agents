"""Tests for the agent orchestrator (unit tests, no LLM required)."""

import json
from pathlib import Path

import pytest

from neuroagent.agent.orchestrator import AgentConfig, AgentOrchestrator, _extract_assessment
from neuroagent.agent.reasoning import AgentTrace, AgentTurn
from neuroagent.agent.reflection import get_reflection_prompt
from neuroagent.agent.planner import restrict_tools, get_forced_tool_order
from neuroagent.llm.client import strip_think_tags
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
    return AgentConfig(model="test-model", max_turns=5)


class TestAgentConfig:
    def test_defaults(self):
        cfg = AgentConfig()
        assert cfg.max_turns == 15
        assert cfg.enable_reflection is True

    def test_custom(self):
        cfg = AgentConfig(model="custom-model", max_turns=10, enable_reflection=False)
        assert cfg.model == "custom-model"
        assert cfg.max_turns == 10
        assert cfg.enable_reflection is False


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

    class FakeMemory:
        def retrieve(self, patient_id):
            return f"History for {patient_id}"

    def test_initial_messages_use_system_then_user(self, config):
        agent = AgentOrchestrator(config=config, tool_registry=ToolRegistry())

        messages = agent._build_initial_messages("Patient presentation", patient_id=None)

        assert [m["role"] for m in messages] == ["system", "user"]
        assert "NeuroAgent" in messages[0]["content"]
        assert messages[1]["content"] == "Patient presentation"

    def test_system_prompt_injects_rules_context(self, config):
        agent = AgentOrchestrator(
            config=config,
            tool_registry=ToolRegistry(),
            rules_engine=self.FakeRules(),
        )

        prompt = agent._build_system_prompt(patient_id=None)

        assert "## Hospital Protocols" in prompt
        assert "Protocol A" in prompt
        assert "MANDATORY: analyze_eeg" in prompt

    def test_system_prompt_skips_empty_rules_context(self, config):
        agent = AgentOrchestrator(
            config=config,
            tool_registry=ToolRegistry(),
            rules_engine=self.EmptyRules(),
        )

        prompt = agent._build_system_prompt(patient_id=None)

        assert "## Hospital Protocols" not in prompt

    def test_system_prompt_injects_memory_only_with_patient_id(self, config):
        agent = AgentOrchestrator(
            config=config,
            tool_registry=ToolRegistry(),
            memory=self.FakeMemory(),
        )

        without_patient = agent._build_system_prompt(patient_id=None)
        with_patient = agent._build_system_prompt(patient_id="P001")

        assert "## Patient History" not in without_patient
        assert "## Patient History (From Previous Encounters)" in with_patient
        assert "History for P001" in with_patient


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
