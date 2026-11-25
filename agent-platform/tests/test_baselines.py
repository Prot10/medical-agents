"""Fig. 6 baselines: rules in the prompt and the multi-agent panel (25 Nov 2026)."""

from __future__ import annotations

from neuroagent.harness import (
    POLICY_SYSTEM_PROMPT,
    RULES_ADDENDUM,
    ActionDecodeError,
    ModelTurn,
    MultiAgentPanelLoop,
    RulesInPromptLoop,
    transcript,
)
from neuroagent.harness.panel import PANEL_NAMESPACE, PANEL_ROLES
from neuroagent.harness.profile import load_profiles
from neuroagent.harness.runtime import boot_profile
from neuroagent.evaluation.benchmark import PROFILES_DIR
from neuroagent_schemas import PluginEvent, RunCompleted, RunFailed, ToolAction

from test_policy_harness import FakeModel, assessment, context, load_case


class PanelModel(FakeModel):
    """FakeModel that also answers the role calls with a fixed text and token counts."""

    def __init__(self, turns):
        super().__init__(turns)
        self.discussions = []

    def discuss(self, messages, *, max_tokens):
        self.discussions.append(messages)
        return f"note {len(self.discussions)}", 100, 10


def test_rules_prompt_is_the_policy_prompt_plus_the_rules():
    loop = RulesInPromptLoop()
    model = FakeModel([ModelTurn(action=assessment())])
    episode = loop.run(context(loop, model, max_turns=1))
    assert model.calls[0]["rules"] is True
    system = transcript(load_case(), episode, rules=True)[0]["content"]
    assert system == POLICY_SYSTEM_PROMPT + "\n\n" + RULES_ADDENDUM
    # The rules name nothing specific to a case or condition.
    assert load_case().ground_truth.diagnosis.accepted[0].lower() not in RULES_ADDENDUM.lower()


def test_rules_never_enter_a_default_transcript():
    loop = RulesInPromptLoop()
    episode = loop.run(context(loop, FakeModel([ModelTurn(action=assessment())]), max_turns=1))
    assert RULES_ADDENDUM not in transcript(load_case(), episode)[0]["content"]


def test_panel_runs_five_roles_per_turn_and_counts_their_tokens():
    loop = MultiAgentPanelLoop()
    model = PanelModel(
        [
            ModelTurn(action=ToolAction(tool_name="analyze_eeg"), prompt_tokens=50, completion_tokens=5),
            ModelTurn(action=assessment(), prompt_tokens=60, completion_tokens=6),
        ]
    )
    episode = loop.run(context(loop, model))
    assert isinstance(episode.events[-1], RunCompleted)
    assert len(model.discussions) == 2 * len(PANEL_ROLES)
    # Role tokens (5 x 100 prompt, 5 x 10 completion per turn) are added to the chair's.
    assert episode.total_tokens == (50 + 5 + 60 + 6) + 2 * len(PANEL_ROLES) * 110
    discussion = [e for e in episode.events if isinstance(e, PluginEvent) and e.namespace == PANEL_NAMESPACE]
    assert len(discussion) == 2
    assert list(discussion[0].payload["value"]) == [name for name, _ in PANEL_ROLES]
    # The chair sees the discussion as one-off feedback; roles get no tool catalogue.
    assert "The panel has discussed this step" in model.calls[0]["correction"]
    assert all("tools" not in str(m[0]) for m in model.discussions[:1])
    # A later role hears the earlier ones.
    assert "[hypothesis] note 1" in model.discussions[1][-1]["content"]


def test_panel_discussion_is_not_replayed_in_the_transcript():
    loop = MultiAgentPanelLoop()
    model = PanelModel([ModelTurn(action=ToolAction(tool_name="analyze_eeg")), ModelTurn(action=assessment())])
    episode = loop.run(context(loop, model))
    rendered = str(transcript(load_case(), episode))
    assert "note 1" not in rendered and "panel has discussed" not in rendered


def test_panel_retries_invalid_chair_output_with_the_same_discussion():
    loop = MultiAgentPanelLoop()
    model = PanelModel(["bad call", ModelTurn(action=assessment())])
    episode = loop.run(context(loop, model, max_turns=1))
    assert isinstance(episode.events[-1], RunCompleted)
    assert len(model.discussions) == len(PANEL_ROLES)
    retry = model.calls[1]["correction"]
    assert "The panel has discussed this step" in retry and "bad call" in retry


def test_panel_fails_within_the_invalid_action_budget():
    loop = MultiAgentPanelLoop()
    model = PanelModel(["bad 1", "bad 2"])
    episode = loop.run(context(loop, model, max_turns=1, max_invalid_actions=1))
    assert isinstance(episode.events[-1], RunFailed)
    assert episode.events[-1].reason == "invalid_action"


def test_baseline_profiles_boot():
    profiles = load_profiles(PROFILES_DIR)
    expected = {
        "rules-qwen3.5-9b": "RulesInPromptLoop",
        "panel-qwen3.5-9b": "MultiAgentPanelLoop",
        "policy-qwen3.8-27b": "ClinicalPolicyLoop",
        "rules-qwen3.8-27b": "RulesInPromptLoop",
        "panel-qwen3.8-27b": "MultiAgentPanelLoop",
    }
    for profile_id, loop in expected.items():
        assert type(boot_profile(profiles[profile_id]).require("loop")).__name__ == loop
