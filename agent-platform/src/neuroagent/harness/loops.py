"""Canonical action-observation loop and its isolated ablations."""

from __future__ import annotations

from neuroagent_schemas import (
    ActionProposed,
    ActionRejected,
    AssessmentSubmitted,
    ModelRequested,
    ObservationReceived,
    PluginEvent,
    RunCompleted,
    RunFailed,
    RunStarted,
    SubmitAssessment,
)

from .adapters import ActionDecodeError
from .interfaces import ModelTurn, RunContext


class ClinicalPolicyLoop:
    """One typed clinical action per turn; the final turn must submit the assessment.

    Invalid model output is retried with a one-off correction, without consuming a clinical
    turn, until the episode's invalid-action budget is spent. ReAct changes prompt context only;
    it never changes the action or event contract.
    """

    loop_id = "clinical-policy"
    react = False

    def run(self, context: RunContext):
        self._start(context)
        for turn in range(1, context.max_turns + 1):
            require_assessment = turn == context.max_turns
            model_turn = self._request_valid_action(context, turn, require_assessment)
            if model_turn is None:
                return context.episode_store.load()

            self._record_model_turn(context, turn, model_turn)
            if isinstance(model_turn.action, SubmitAssessment):
                context.episode_store.append(
                    AssessmentSubmitted(turn=turn, assessment=model_turn.action)
                )
                context.episode_store.append(RunCompleted(turn=turn))
                return context.episode_store.load()

            try:
                result = context.environment.execute(model_turn.action)
            except Exception as exc:
                return self._fail(context, turn, "environment_error", f"{type(exc).__name__}: {exc}")

            context.episode_store.append(
                ObservationReceived(
                    turn=turn,
                    tool_name=result.tool_name,
                    success=result.success,
                    output=result.output,
                    error_message=result.error_message,
                    cost_usd=result.cost_usd or 0.0,
                    from_fallback=result.from_fallback,
                    rejected=result.rejected,
                )
            )
            total_cost = context.episode_store.load().total_cost_usd
            if context.max_cost_usd is not None and total_cost > context.max_cost_usd:
                return self._fail(
                    context, turn, "budget_exhausted", f"cost exceeded USD {context.max_cost_usd:.2f}"
                )
        raise AssertionError("the final turn always submits or fails")

    def _request_valid_action(
        self, context: RunContext, turn: int, require_assessment: bool
    ) -> ModelTurn | None:
        correction: str | None = None
        while True:
            try:
                return context.model.next_action(
                    case=context.environment.case,
                    episode=context.episode_store.load(),
                    allowed_tools=context.environment.tool_definitions(),
                    require_assessment=require_assessment,
                    react=self.react,
                    correction=correction,
                )
            except ActionDecodeError as exc:
                context.invalid_actions += 1
                retry_allowed = context.invalid_actions <= context.max_invalid_actions
                context.episode_store.append(
                    ActionRejected(turn=turn, reason=str(exc), retry_allowed=retry_allowed)
                )
                if not retry_allowed:
                    self._fail(context, turn, "invalid_action", str(exc))
                    return None
                correction = (
                    f"The previous response was invalid: {exc}. "
                    "Return exactly one valid structured action."
                )
            except Exception as exc:
                self._fail(context, turn, "model_error", f"{type(exc).__name__}: {exc}")
                return None

    @staticmethod
    def _fail(context: RunContext, turn: int, reason: str, message: str):
        context.episode_store.append(RunFailed(turn=turn, reason=reason, message=message))
        return context.episode_store.load()

    def _start(self, context: RunContext) -> None:
        context.episode_store.append(
            RunStarted(
                turn=0,
                case_id=context.environment.case.case_id,
                profile_id=context.profile_id,
                model_id=context.model.model_id,
                plugin_versions=context.plugin_versions,
            )
        )

    @staticmethod
    def _record_model_turn(context: RunContext, turn: int, model_turn: ModelTurn) -> None:
        context.episode_store.append(
            ModelRequested(turn=turn, prompt_tokens=model_turn.prompt_tokens)
        )
        context.episode_store.append(
            ActionProposed(
                turn=turn,
                action=model_turn.action,
                completion_tokens=model_turn.completion_tokens,
                latency_seconds=model_turn.latency_seconds,
            )
        )
        for namespace, value in model_turn.plugin_payload.items():
            context.episode_store.append(
                PluginEvent(turn=turn, namespace=namespace, payload={"value": value})
            )


class ReactAblationLoop(ClinicalPolicyLoop):
    """Prompt-only rationale ablation over the canonical typed policy loop."""

    loop_id = "react-ablation"
    react = True


class DirectAnswerLoop(ClinicalPolicyLoop):
    """Single-turn full-information baseline: every stored result is given, no tool selection."""

    loop_id = "direct-answer"

    def run(self, context: RunContext):
        self._start(context)
        for result in context.environment.direct_observations():
            context.episode_store.append(
                ObservationReceived(
                    turn=0,
                    tool_name=result.tool_name,
                    success=result.success,
                    output=result.output,
                    error_message=result.error_message,
                )
            )
        model_turn = self._request_valid_action(context, 1, require_assessment=True)
        if model_turn is None:
            return context.episode_store.load()
        self._record_model_turn(context, 1, model_turn)
        context.episode_store.append(AssessmentSubmitted(turn=1, assessment=model_turn.action))
        context.episode_store.append(RunCompleted(turn=1))
        return context.episode_store.load()
