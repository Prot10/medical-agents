from __future__ import annotations

from pathlib import Path

from neuroagent.harness import (
    ClinicalPolicyLoop,
    DirectAnswerLoop,
    MemoryEpisodeStore,
    ModelTurn,
    ReactAblationLoop,
    RunContext,
)
from neuroagent.tools.base import ToolResult
from neuroagent_schemas import (
    ActionProposed,
    AssessmentSubmitted,
    ClinicalEpisode,
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
    adapter_id = "fake"
    model_id = "fake/model"

    def __init__(self, turns):
        self.turns = iter(turns)
        self.calls = []

    def next_action(self, **kwargs):
        self.calls.append(kwargs)
        return next(self.turns)


def assessment():
    return SubmitAssessment(
        primary_diagnosis="status epilepticus",
        confidence=0.9,
        urgency="emergent",
        recommendations=["Treat promptly"],
    )


def context(loop, model, *, max_turns=3):
    environment = FakeEnvironment(load_case())
    return RunContext(
        profile_id="test",
        model=model,
        loop=loop,
        environment=environment,
        episode_store=MemoryEpisodeStore(),
        max_turns=max_turns,
    )


def test_policy_loop_has_one_action_per_turn_and_explicit_submission():
    loop = ClinicalPolicyLoop()
    model = FakeModel(
        [
            ModelTurn(action=ToolAction(tool_name="analyze_eeg"), prompt_tokens=10),
            ModelTurn(action=assessment(), completion_tokens=5),
        ]
    )
    ctx = context(loop, model)
    episode = loop.run(ctx)
    assert [type(action) for action in episode.actions] == [ToolAction, SubmitAssessment]
    assert sum(isinstance(event, ObservationReceived) for event in episode.events) == 1
    assert sum(isinstance(event, AssessmentSubmitted) for event in episode.events) == 1
    assert isinstance(episode.events[-1], RunCompleted)
    assert episode.total_cost_usd == 125.0


def test_last_turn_forces_assessment():
    loop = ClinicalPolicyLoop()
    model = FakeModel([ModelTurn(action=assessment())])
    ctx = context(loop, model, max_turns=1)
    loop.run(ctx)
    assert model.calls[0]["require_assessment"] is True


def test_react_is_namespaced_and_only_enabled_in_ablation():
    loop = ReactAblationLoop()
    model = FakeModel(
        [
            ModelTurn(
                action=assessment(),
                plugin_payload={"react.rationale": "EEG confirms ongoing seizure."},
            )
        ]
    )
    episode = loop.run(context(loop, model, max_turns=1))
    events = [event for event in episode.events if isinstance(event, PluginEvent)]
    assert len(events) == 1
    assert events[0].namespace == "react.rationale"
    assert model.calls[0]["react"] is True


def test_direct_answer_uses_zero_cost_observations_and_no_tool_action():
    loop = DirectAnswerLoop()
    model = FakeModel([ModelTurn(action=assessment())])
    episode = loop.run(context(loop, model, max_turns=1))
    assert episode.tool_actions == []
    assert episode.total_cost_usd == 0
    assert episode.assessment is not None


def test_tool_when_assessment_required_fails_explicitly():
    loop = ClinicalPolicyLoop()
    model = FakeModel([ModelTurn(action=ToolAction(tool_name="analyze_eeg"))])
    episode = loop.run(context(loop, model, max_turns=1))
    assert isinstance(episode.events[-1], RunFailed)
    assert episode.events[-1].reason == "invalid_action"
