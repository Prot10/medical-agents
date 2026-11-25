"""The policy loop with a physician in the model server's place.

``ClinicalPolicyLoop`` drives a model synchronously, so a human cannot sit inside one call of it.
Instead, every physician step replays the loop from the start: ``PhysicianClient`` stands where
``LLMClient`` stands and answers each chat request with the next action the physician already
sent; when it has none left it raises ``AwaitingPhysician``, which stops the loop exactly at the
request the agent would be answering now. That request (messages and tool list) is what the
physician is shown.

Everything agent-facing therefore comes from the harness, unchanged: the transcript codec, the
tool catalogue and ``SUBMIT_TOOL``, the adapter's decoding and validation (with its error texts),
the loop's turn counting, final-turn rule and invalid-action budget, ``BaseTool.execute``
validation and the MockServer. Observations already recorded are served back from the record
(``ReplayEnvironment``) rather than recomputed, so a case resumes on exactly what the physician
saw even if the app was redeployed in between.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any

from neuroagent_schemas import (
    ClinicalEpisode,
    NeuroBenchCase,
    ObservationReceived,
    RunCompleted,
    RunFailed,
    ToolAction,
)

from neuroagent.harness.adapters import NativeToolModelAdapter, _final_turn
from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent.harness.interfaces import ModelTurn, RunContext
from neuroagent.harness.loops import ClinicalPolicyLoop
from neuroagent.harness.plugins import builtin_plugins
from neuroagent.harness.profile import HarnessProfile
from neuroagent.llm.client import LLMResponse, LLMToolCall, _wire_messages
from neuroagent.tools.base import ToolResult

PHYSICIAN_PROFILE_ID = "policy-physician"
# The plugins a physician episode runs through; the model plugin is the physician.
_PLUGIN_IDS = ("loop.policy", "reward.policy")


class AwaitingPhysician(BaseException):
    """The loop reached a request no recorded action answers.

    A ``BaseException`` on purpose: the loop turns any ``Exception`` of the model into a failed
    episode, and waiting for the physician is not a failure.
    """


@dataclass(frozen=True, slots=True)
class Submission:
    """One action as the physician sent it: a function name and its arguments."""

    name: str
    arguments: dict[str, Any]
    seconds: float = 0.0  # time the physician took, recorded as the action's latency


class PhysicianClient:
    """Stands where ``LLMClient`` stands: answers each request with the physician's next action."""

    def __init__(self, model_id: str, submissions: list[Submission]) -> None:
        self.model = model_id
        self._queue = deque(submissions)
        self.request: dict[str, Any] | None = None

    def chat(self, messages: list[dict[str, Any]], *, tools=None, tool_choice=None) -> LLMResponse:
        # Kept in the wire form the model server receives (arguments as JSON strings).
        self.request = {"messages": _wire_messages(messages), "tools": tools or []}
        if not self._queue:
            raise AwaitingPhysician()
        submission = self._queue.popleft()
        return LLMResponse(
            tool_calls=[LLMToolCall(id="physician", name=submission.name, arguments=submission.arguments)],
            latency_seconds=max(0.0, submission.seconds),
        )


class PhysicianAdapter(NativeToolModelAdapter):
    """The native-tools adapter, unchanged; it only notes what the loop asked for this turn."""

    adapter_id = "physician"

    def __init__(self, client: PhysicianClient) -> None:
        super().__init__(client)
        self.require_assessment = False
        self.notice: str | None = None

    def next_action(self, *, require_assessment: bool = False, correction: str | None = None, **kwargs) -> ModelTurn:
        self.require_assessment = require_assessment
        # The extra text the agent receives on this turn, built by the adapter's own function.
        self.notice = _final_turn(correction) if require_assessment else correction
        return super().next_action(require_assessment=require_assessment, correction=correction, **kwargs)


class ReplayEnvironment:
    """The case's environment; orders already answered are answered again from the record."""

    def __init__(self, inner: NeuroBenchEnvironment, recorded: list[ObservationReceived]) -> None:
        self.inner = inner
        self.environment_id = inner.environment_id
        self.case = inner.case
        self._recorded = deque(recorded)

    def tool_definitions(self) -> list[dict[str, Any]]:
        return self.inner.tool_definitions()

    def execute(self, action: ToolAction) -> ToolResult:
        if self._recorded:
            event = self._recorded.popleft()
            return ToolResult(
                tool_name=event.tool_name,
                success=event.success,
                output=event.output,
                error_message=event.error_message,
                cost_usd=event.cost_usd,
                from_fallback=event.from_fallback,
                library=event.library,
                rejected=event.rejected,
                unavailable=event.unavailable,
            )
        return self.inner.execute(action)


@dataclass(slots=True)
class Advance:
    """Where the loop stands after the recorded actions."""

    episode: ClinicalEpisode
    status: str  # "in_progress" | "completed" | "failed"
    # The request the agent would be answering now (None once the episode is over).
    request: dict[str, Any] | None = None
    require_assessment: bool = False
    notice: str | None = None
    invalid_actions: int = 0
    failure_reason: str | None = None
    failure_message: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


def plugin_versions() -> dict[str, str]:
    plugins = builtin_plugins()
    return {plugin_id: plugins[plugin_id].version for plugin_id in _PLUGIN_IDS}


def advance(
    case: NeuroBenchCase,
    profile: HarnessProfile,
    model_id: str,
    submissions: list[Submission],
    recorded: ClinicalEpisode | None = None,
) -> Advance:
    """Run the policy loop over the physician's actions so far.

    ``profile`` supplies the limits (turns, cost, invalid actions) of the checked policy profile.
    ``recorded`` is the episode stored so far; its observations are replayed, not recomputed.
    """
    observations = [
        event
        for event in (recorded.events if recorded else [])
        if isinstance(event, ObservationReceived) and event.turn > 0
    ]
    client = PhysicianClient(model_id, submissions)
    adapter = PhysicianAdapter(client)
    context = RunContext(
        profile_id=PHYSICIAN_PROFILE_ID,
        model=adapter,
        loop=ClinicalPolicyLoop(),
        environment=ReplayEnvironment(NeuroBenchEnvironment(case), observations),
        max_turns=profile.max_turns,
        max_cost_usd=profile.max_cost_usd,
        max_invalid_actions=profile.max_invalid_actions,
        plugin_versions=plugin_versions(),
    )
    try:
        episode = context.loop.run(context)
    except AwaitingPhysician:
        return Advance(
            episode=context.episode_store.load(),
            status="in_progress",
            request=client.request,
            require_assessment=adapter.require_assessment,
            notice=adapter.notice,
            invalid_actions=context.invalid_actions,
        )
    terminal = episode.events[-1]
    failed = isinstance(terminal, RunFailed)
    assert failed or isinstance(terminal, RunCompleted)
    return Advance(
        episode=episode,
        status="failed" if failed else "completed",
        invalid_actions=context.invalid_actions,
        failure_reason=terminal.reason if failed else None,
        failure_message=terminal.message if failed else None,
    )


def merge_events(recorded: ClinicalEpisode | None, replayed: ClinicalEpisode) -> ClinicalEpisode:
    """The stored events, then the events this step added.

    Stored events are never rewritten (they keep their ids and timestamps). The replay must
    reproduce their sequence of types and turns; if it does not, the harness changed in a way
    that alters the course of this episode and the step is refused rather than recorded.
    """
    stored = list(recorded.events) if recorded else []
    signature = [(event.type, event.turn) for event in replayed.events]
    if signature[: len(stored)] != [(event.type, event.turn) for event in stored]:
        raise EpisodeDrift("the replayed episode no longer matches the stored one")
    return ClinicalEpisode(events=[*stored, *replayed.events[len(stored):]])


class EpisodeDrift(RuntimeError):
    pass
