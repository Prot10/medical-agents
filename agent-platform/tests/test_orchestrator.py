"""Tests for the agent orchestrator (unit tests, no LLM required)."""

import json
from pathlib import Path

import pytest

from neuroagent.agent.orchestrator import AgentConfig, AgentOrchestrator
from neuroagent.agent.reasoning import AgentTrace, AgentTurn
from neuroagent.agent.reflection import get_reflection_prompt
from neuroagent.agent.planner import restrict_tools, get_forced_tool_order
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
        assert "clinical reasoning" in prompt["content"].lower()


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
