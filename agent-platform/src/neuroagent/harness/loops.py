"""Canonical action-observation loops and isolated experimental ablations."""

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
    """Run one typed clinical action per turn.

    Invalid model output receives the configured number of corrective retries
    without consuming a clinical turn. ReAct changes prompt context only; it
    never changes the action or event contract.
    """

    loop_id = "clinical-policy"
    react = False

    def run(self, context: RunContext):
        self._start(context)
        invalid_actions = 0

        for turn in range(1, context.max_turns + 1):
            require_assessment = turn == context.max_turns
            model_turn, invalid_actions = self._request_valid_action(
                context,
                turn=turn,
                require_assessment=require_assessment,
                invalid_actions=invalid_actions,
            )
            if model_turn is None:
                return context.episode_store.load()

            self._record_model_turn(context, turn, model_turn)
            if isinstance(model_turn.action, SubmitAssessment):
                context.episode_store.append(
                    AssessmentSubmitted(turn=turn, assessment=model_turn.action)
                )
                context.episode_store.append(RunCompleted(turn=turn))
                return context.episode_store.load()

            if require_assessment:
                context.episode_store.append(
                    RunFailed(
                        turn=turn,
                        reason="invalid_action",
                        message="tool action returned when assessment was required",
                    )
                )
                return context.episode_store.load()

            try:
                result = context.environment.execute(model_turn.action)
            except Exception as exc:
                context.episode_store.append(
                    RunFailed(
                        turn=turn,
                        reason="environment_error",
                        message=f"{type(exc).__name__}: {exc}",
                    )
                )
                return context.episode_store.load()

            context.episode_store.append(
                ObservationReceived(
                    turn=turn,
                    tool_name=result.tool_name,
                    success=result.success,
                    output=result.output,
                    error_message=result.error_message,
                    cost_usd=result.cost_usd or 0.0,
                    from_fallback=result.from_fallback,
                )
            )
            episode = context.episode_store.load()
            if (
                context.max_cost_usd is not None
                and episode.total_cost_usd > context.max_cost_usd
            ):
                context.episode_store.append(
                    RunFailed(
                        turn=turn,
                        reason="budget_exhausted",
                        message=f"cost exceeded USD {context.max_cost_usd:.2f}",
                    )
                )
                return context.episode_store.load()

        context.episode_store.append(
            RunFailed(
                turn=context.max_turns,
                reason="max_turns",
                message="no assessment submitted",
            )
        )
        return context.episode_store.load()

    def _request_valid_action(
        self,
        context: RunContext,
        *,
        turn: int,
        require_assessment: bool,
        invalid_actions: int,
    ) -> tuple[ModelTurn | None, int]:
        while True:
            try:
                model_turn = context.model.next_action(
                    case=context.environment.case,
                    episode=context.episode_store.load(),
                    allowed_tools=context.environment.tool_definitions(),
                    require_assessment=require_assessment,
                    react=self.react,
                )
                return model_turn, invalid_actions
            except ActionDecodeError as exc:
                invalid_actions += 1
                retry_allowed = invalid_actions <= context.max_invalid_actions
                context.episode_store.append(
                    ActionRejected(
                        turn=turn,
                        reason=str(exc),
                        retry_allowed=retry_allowed,
                    )
                )
                if retry_allowed:
                    continue
                context.episode_store.append(
                    RunFailed(
                        turn=turn,
                        reason="invalid_action",
                        message=str(exc),
                    )
                )
                return None, invalid_actions
            except Exception as exc:
                context.episode_store.append(
                    RunFailed(
                        turn=turn,
                        reason="model_error",
                        message=f"{type(exc).__name__}: {exc}",
                    )
                )
                return None, invalid_actions

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

    def _record_model_turn(
        self,
        context: RunContext,
        turn: int,
        model_turn: ModelTurn,
    ) -> None:
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
                PluginEvent(
                    turn=turn,
                    namespace=namespace,
                    payload={"value": value},
                )
            )


class ReactAblationLoop(ClinicalPolicyLoop):
    """Prompt-only rationale ablation over the canonical typed policy loop."""

    loop_id = "react-ablation"
    react = True


class DirectAnswerLoop(ClinicalPolicyLoop):
    """Single-turn full-information baseline with no tool selection."""

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
                    cost_usd=0.0,
                    from_fallback=False,
                )
            )

        model_turn, _ = self._request_valid_action(
            context,
            turn=1,
            require_assessment=True,
            invalid_actions=0,
        )
        if model_turn is None:
            return context.episode_store.load()

        self._record_model_turn(context, 1, model_turn)
        if not isinstance(model_turn.action, SubmitAssessment):
            context.episode_store.append(
                RunFailed(
                    turn=1,
                    reason="invalid_action",
                    message="direct baseline requires an assessment",
                )
            )
            return context.episode_store.load()

        context.episode_store.append(
            AssessmentSubmitted(turn=1, assessment=model_turn.action)
        )
        context.episode_store.append(RunCompleted(turn=1))
        return context.episode_store.load()
