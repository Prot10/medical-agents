from __future__ import annotations

from pathlib import Path

from neuroagent.harness import (
    SUBMIT_TOOL,
    ActionDecodeError,
    ClinicalPolicyLoop,
    DirectAnswerLoop,
    ModelTurn,
    ReactAblationLoop,
    RunContext,
    transcript,
)
from neuroagent.tools.base import ToolResult
from neuroagent_schemas import (
    AssessmentSubmitted,
    NeuroBenchCase,
    ObservationReceived,
    PluginEvent,
    RunCompleted,
    RunFailed,
    SubmitAssessment,
    ToolAction,
)

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = ROOT / "data/neurobench/cases/SE-M02.json"


def load_case() -> NeuroBenchCase:
    return NeuroBenchCase.model_validate_json(CASE_PATH.read_text())


class FakeEnvironment:
    environment_id = "fake"

    def __init__(self, case):
        self.case = case
        self.executed = []

    def tool_definitions(self):
        return [{"type": "function", "function": {"name": "analyze_eeg", "parameters": {}}}]

    def execute(self, action):
        self.executed.append(action)
        return ToolResult(
            tool_name=action.tool_name,
            success=True,
            output={"impression": "epileptiform activity"},
            cost_usd=125.0,
        )

    def direct_observations(self):
        return [
            ToolResult(
                tool_name="analyze_eeg",
                success=True,
                output={"impression": "epileptiform activity"},
                cost_usd=0.0,
            )
        ]


class FakeModel:
    """Yields scripted turns; a string entry raises ActionDecodeError with that reason."""

    adapter_id = "fake"
    model_id = "fake/model"

    def __init__(self, turns):
        self.turns = iter(turns)
        self.calls = []

    def next_action(self, **kwargs):
        self.calls.append(kwargs)
        turn = next(self.turns)
        if isinstance(turn, str):
            raise ActionDecodeError(turn)
        return turn


def assessment():
    return SubmitAssessment(
        primary_diagnosis="status epilepticus",
        confidence=0.9,
        urgency="emergent",
        recommendations=["Treat promptly"],
    )


def context(loop, model, *, max_turns=3, max_invalid_actions=2):
    return RunContext(
        profile_id="test",
        model=model,
        loop=loop,
        environment=FakeEnvironment(load_case()),
        max_turns=max_turns,
        max_invalid_actions=max_invalid_actions,
    )


def test_policy_loop_has_one_action_per_turn_and_explicit_submission():
    loop = ClinicalPolicyLoop()
    model = FakeModel(
        [
            ModelTurn(action=ToolAction(tool_name="analyze_eeg"), prompt_tokens=10),
            ModelTurn(action=assessment(), completion_tokens=5),
        ]
    )
    episode = loop.run(context(loop, model))
    assert [type(action) for action in episode.actions] == [ToolAction, SubmitAssessment]
    assert sum(isinstance(event, ObservationReceived) for event in episode.events) == 1
    assert sum(isinstance(event, AssessmentSubmitted) for event in episode.events) == 1
    assert isinstance(episode.events[-1], RunCompleted)
    assert episode.total_cost_usd == 125.0


def test_last_turn_forces_assessment():
    loop = ClinicalPolicyLoop()
    model = FakeModel([ModelTurn(action=assessment())])
    loop.run(context(loop, model, max_turns=1))
    assert model.calls[0]["require_assessment"] is True


def test_invalid_output_is_retried_with_a_correction_then_fails_within_budget():
    loop = ClinicalPolicyLoop()
    model = FakeModel(["bad json", ModelTurn(action=assessment())])
    episode = loop.run(context(loop, model, max_turns=1, max_invalid_actions=1))
    assert isinstance(episode.events[-1], RunCompleted)
    assert model.calls[0]["correction"] is None
    assert "bad json" in model.calls[1]["correction"]

    model = FakeModel(["bad json", "still bad"])
    episode = loop.run(context(loop, model, max_turns=1, max_invalid_actions=1))
    assert isinstance(episode.events[-1], RunFailed)
    assert episode.events[-1].reason == "invalid_action"
    assert len(model.calls) == 2


def test_react_is_namespaced_and_replayed_only_in_the_ablation():
    loop = ReactAblationLoop()
    model = FakeModel(
        [
            ModelTurn(
                action=ToolAction(tool_name="analyze_eeg"),
                plugin_payload={"react.rationale": "EEG confirms ongoing seizure."},
            ),
            ModelTurn(action=assessment()),
        ]
    )
    episode = loop.run(context(loop, model, max_turns=2))
    events = [event for event in episode.events if isinstance(event, PluginEvent)]
    assert len(events) == 1 and events[0].namespace == "react.rationale"
    assert model.calls[0]["react"] is True
    case = load_case()
    assert transcript(case, episode, react=True)[2]["content"] == "EEG confirms ongoing seizure."
    assert transcript(case, episode)[2]["content"] is None


def test_direct_answer_presents_evidence_as_preloaded_results():
    loop = DirectAnswerLoop()
    model = FakeModel([ModelTurn(action=assessment())])
    episode = loop.run(context(loop, model, max_turns=1))
    assert episode.tool_actions == []
    assert episode.total_cost_usd == 0
    assert episode.assessment is not None
    messages = transcript(load_case(), episode)
    assert messages[2]["role"] == "user"
    assert messages[2]["content"].startswith("Results already available")
    assert not any(message["role"] == "tool" for message in messages)


def test_transcript_uses_tool_calls_and_tool_messages():
    loop = ClinicalPolicyLoop()
    model = FakeModel([ModelTurn(action=ToolAction(tool_name="analyze_eeg")), ModelTurn(action=assessment())])
    episode = loop.run(context(loop, model))
    messages = transcript(load_case(), episode)
    assert [message["role"] for message in messages] == ["system", "user", "assistant", "tool", "assistant"]
    call = messages[2]["tool_calls"][0]
    assert call["function"]["name"] == "analyze_eeg"
    assert messages[3]["tool_call_id"] == call["id"]
    assert messages[4]["tool_calls"][0]["function"]["name"] == "submit_assessment"
    assert messages[4]["tool_calls"][0]["function"]["arguments"]["urgency"] == "emergent"


def test_submit_tool_schema_is_self_contained():
    parameters = SUBMIT_TOOL["function"]["parameters"]
    assert "$ref" not in str(parameters) and "$defs" not in parameters
    assert "type" not in parameters["properties"]
    assert set(parameters["required"]) == {"primary_diagnosis", "confidence", "urgency"}
