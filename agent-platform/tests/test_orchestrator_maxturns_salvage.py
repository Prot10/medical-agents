"""Max-turns salvage behavior of the orchestrator (no LLM required).

Covers two bugs:

- O1: when the loop exhausts max_turns, the last trace turn is always a tool
  turn (content=None), so the old fallback recorded _NO_CONCLUSION_MESSAGE
  even when the model had written a diagnosis in its last assistant turn.
  The fallback must scan backwards for the most recent assistant turn with
  non-empty content.
- O2: a completion carrying BOTH tool calls and a complete structured
  assessment in its content never became final_response. The embedded
  assessment is stashed and used as the salvage value at max_turns (but must
  never override the normal finalize path).
"""

from __future__ import annotations

import pytest

from neuroagent.agent.orchestrator import (
    AgentOrchestrator,
    _NO_CONCLUSION_MESSAGE,
    load_agent_config,
)
from neuroagent.llm.client import LLMResponse, LLMToolCall
from neuroagent.tools.base import BaseTool, ToolResult
from neuroagent.tools.tool_registry import ToolRegistry

ASSESSMENT = (
    "### Primary Diagnosis\n"
    "Focal epilepsy (Confidence: 0.92)\n\n"
    "### Recommendations\n"
    "1. Start levetiracetam"
)


class FakeEEGTool(BaseTool):
    name = "analyze_eeg"
    description = "Fake EEG analyzer for tests."
    parameter_schema = {"type": "object", "properties": {}}

    def _execute_real(self, parameters):
        return ToolResult(
            tool_name=self.name,
            success=True,
            output={"finding": "right temporal sharp waves"},
        )


class FakeLLM:
    """Stub for LLMClient: .chat() / .chat_stream() replay canned responses."""

    def __init__(self, responses: list[LLMResponse]):
        self.responses = list(responses)
        self.chat_calls = 0

    def chat(self, messages=None, **kwargs):
        self.chat_calls += 1
        return self.responses.pop(0)

    def chat_stream(self, messages=None, **kwargs):
        response = self.responses.pop(0)
        if response.content:
            yield {"type": "content_delta", "delta": response.content}
        yield {"type": "done", "response": response, "think_content": None}


def _tool_response(content: str | None = None) -> LLMResponse:
    return LLMResponse(
        content=content,
        tool_calls=[LLMToolCall(id="call_1", name="analyze_eeg", arguments={})],
    )


def _make_agent(responses: list[LLMResponse], max_turns: int) -> AgentOrchestrator:
    config = load_agent_config(model="test-model", max_turns=max_turns)
    registry = ToolRegistry()
    registry.register(FakeEEGTool())
    agent = AgentOrchestrator(config=config, tool_registry=registry)
    agent.llm = FakeLLM(responses)
    return agent


def _run_streaming_final_response(agent: AgentOrchestrator) -> str:
    events = list(agent.run_streaming("Patient with seizures", case_id="TEST-S1"))
    complete = [e for e in events if e["type"] == "run_complete"]
    assert len(complete) == 1
    return complete[0]["final_response"]


class TestMaxTurnsSalvagesLastAssistantContent:
    """Bug O1: the fallback must not read the (content-less) tool turn."""

    RESPONSES = [
        _tool_response(content="Ordering an EEG to characterize the events."),
        _tool_response(
            content="The EEG confirms it. The diagnosis is focal epilepsy."
        ),
    ]

    def test_run(self):
        agent = _make_agent(list(self.RESPONSES), max_turns=2)
        trace = agent.run("Patient with seizures", case_id="TEST-S1")

        # Sanity: the loop really exhausted max_turns after tool-calling turns,
        # so the last trace turn is a tool turn with no content.
        assert trace.turns[-1].role == "tool"
        assert trace.turns[-1].content is None

        assert trace.final_response != _NO_CONCLUSION_MESSAGE
        assert trace.final_response == (
            "The EEG confirms it. The diagnosis is focal epilepsy."
        )

    def test_run_streaming_matches_run(self):
        agent = _make_agent(list(self.RESPONSES), max_turns=2)
        final = _run_streaming_final_response(agent)
        assert final == "The EEG confirms it. The diagnosis is focal epilepsy."

    def test_no_assistant_content_anywhere_keeps_no_conclusion(self):
        responses = [_tool_response(content=None), _tool_response(content=None)]
        agent = _make_agent(responses, max_turns=2)
        trace = agent.run("Patient with seizures")
        assert trace.final_response == _NO_CONCLUSION_MESSAGE


class TestReasonAndActEmbeddedAssessment:
    """Bug O2: an assessment embedded in a tool-calling turn is salvaged."""

    RESPONSES = [
        _tool_response(content="Working the case up; ordering EEG."),
        _tool_response(
            content=(
                "I am confident, running one confirmatory EEG.\n\n" + ASSESSMENT
            )
        ),
    ]

    def test_run(self):
        agent = _make_agent(list(self.RESPONSES), max_turns=2)
        trace = agent.run("Patient with seizures")

        assert trace.final_response.startswith("### Primary Diagnosis")
        assert "Focal epilepsy" in trace.final_response
        # The reasoning preamble is stripped, exactly as the finalizer would.
        assert "confirmatory EEG" not in trace.final_response
        # Both tool calls still executed — control flow was not short-circuited.
        assert trace.total_tool_calls == 2

    def test_run_streaming_matches_run(self):
        agent = _make_agent(list(self.RESPONSES), max_turns=2)
        final = _run_streaming_final_response(agent)
        assert final.startswith("### Primary Diagnosis")
        assert "Focal epilepsy" in final

    def test_later_embedded_assessment_wins_over_earlier(self):
        second = ASSESSMENT.replace("0.92", "0.99")
        responses = [
            _tool_response(content="Early guess.\n\n" + ASSESSMENT),
            _tool_response(content="Revised.\n\n" + second),
        ]
        agent = _make_agent(responses, max_turns=2)
        trace = agent.run("Patient with seizures")
        assert "0.99" in trace.final_response


class TestNormalFinalizeStillWins:
    """A text-only concluding turn goes through _finalize_assessment and must
    not be overridden by any stashed embedded assessment."""

    FINAL_TEXT = (
        "**THINK**: All data in.\n\n"
        "### Primary Diagnosis\n"
        "Temporal lobe epilepsy (Confidence: 0.97)\n\n"
        "### Recommendations\n"
        "1. MRI epilepsy protocol"
    )

    def _responses(self) -> list[LLMResponse]:
        return [
            # Tool-calling turn that ALSO embeds an (older) assessment.
            _tool_response(content="Preliminary.\n\n" + ASSESSMENT),
            # Text-only conclusion → normal finalize path.
            LLMResponse(content=self.FINAL_TEXT, tool_calls=None),
        ]

    def test_run(self):
        agent = _make_agent(self._responses(), max_turns=5)
        trace = agent.run("Patient with seizures")

        assert trace.final_response.startswith("### Primary Diagnosis")
        assert "Temporal lobe epilepsy" in trace.final_response
        assert "0.97" in trace.final_response
        # The stale embedded assessment did not leak through.
        assert "0.92" not in trace.final_response
        # No max-turns marker, and no re-prompt happened (2 chat calls only).
        assert trace.final_response != _NO_CONCLUSION_MESSAGE
        assert agent.llm.chat_calls == 2

    def test_run_streaming_matches_run(self):
        agent = _make_agent(self._responses(), max_turns=5)
        final = _run_streaming_final_response(agent)
        assert "Temporal lobe epilepsy" in final
        assert "0.92" not in final


class TestRunAndStreamingParity:
    """Identical canned outputs must yield identical final_response via both
    entry points, in every salvage scenario."""

    @pytest.mark.parametrize(
        "make_responses,max_turns",
        [
            (lambda: [_tool_response("plain text diagnosis, no heading")], 1),
            (lambda: [_tool_response("go.\n\n" + ASSESSMENT)], 1),
            (lambda: [_tool_response(None)], 1),
        ],
    )
    def test_parity(self, make_responses, max_turns):
        run_agent = _make_agent(make_responses(), max_turns=max_turns)
        run_final = run_agent.run("Patient").final_response

        stream_agent = _make_agent(make_responses(), max_turns=max_turns)
        stream_final = _run_streaming_final_response(stream_agent)

        assert run_final == stream_final
