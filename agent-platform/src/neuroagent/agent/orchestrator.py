"""Main agent orchestrator — ReAct loop with tool dispatch."""

from __future__ import annotations

import json
import logging
from typing import Any

import re

from ..llm.client import LLMClient, LLMResponse, LLMToolCall
from ..llm.prompts import apply_reasoning_style, load_prompt, format_tool_result
from ..tools.base import ToolCall, ToolResult
from ..tools.cost_tracker import CostTracker
from ..tools.tool_registry import ToolRegistry
from .config import AgentConfig, AgentConfigError, load_agent_config
from .planner import restrict_tools
from .reasoning import AgentTrace
from .reflection import get_reflection_prompt

# Regex to extract the structured assessment section from the agent's final turn.
# Matches from the first "### Primary Diagnosis" heading to end of string.
_ASSESSMENT_PATTERN = re.compile(
    r"(###\s*Primary Diagnosis.*)",
    flags=re.DOTALL,
)
_NO_CONCLUSION_MESSAGE = "[Agent did not reach a conclusion within turn limit]"
_STRUCTURED_DIAGNOSIS_REPROMPT = (
    "You provided reasoning but did not include a structured "
    "diagnosis. Please provide your final assessment now using "
    "the required format starting with:\n\n"
    "### Primary Diagnosis\n[Diagnosis] (Confidence: X.XX)"
)
_USE_RESPONSE_TOOL_CALLS = object()

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Main agent implementing the ReAct loop for clinical reasoning."""

    def __init__(
        self,
        config: AgentConfig,
        tool_registry: ToolRegistry,
        rules_engine: Any | None = None,  # RulesEngine
        cost_tracker: CostTracker | None = None,
    ):
        self.config = config
        self.llm = LLMClient(
            base_url=config.base_url,
            api_key=config.api_key,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p,
            presence_penalty=config.presence_penalty,
            seed=config.seed,
            timeout=config.request_timeout,
            max_retries=config.max_retries,
        )
        self.tools = tool_registry
        self.rules = rules_engine
        self.cost_tracker = cost_tracker or CostTracker()

    def run(
        self,
        patient_info: str,
        case_id: str | None = None,
    ) -> AgentTrace:
        """Run the agent on a patient case.

        Args:
            patient_info: Initial clinical information (chief complaint + history).
            case_id: Case identifier for tracing.

        Returns:
            AgentTrace with complete record of reasoning and actions.
        """
        trace = AgentTrace(case_id=case_id)
        trace.start_timer()
        self.cost_tracker.reset()

        messages = self._build_initial_messages(patient_info)
        tool_definitions = self._get_tool_definitions()
        tool_request = self._tool_request_kwargs(tool_definitions)

        turn_number = 0
        # Structured assessment the model embedded alongside tool calls, if any.
        # Only used as the salvage value when the loop hits max_turns without
        # finalizing normally — never finalizes early (the agent may still be
        # mid-workup, and _finalize_assessment on the normal path always wins).
        pending_assessment: str | None = None
        for _ in range(self.config.max_turns):
            # Call LLM with tool definitions
            response = self.llm.chat(
                messages=messages,
                **tool_request,
            )

            turn_number += 1
            valid_tool_calls = self._valid_tool_calls(response)

            # If LLM wants to call tool(s)
            if valid_tool_calls:
                # Record assistant turn with tool calls
                trace.add_assistant_turn(
                    turn_number=turn_number,
                    content=response.content,
                    tool_calls=self._tool_call_records(valid_tool_calls),
                    token_usage=response.usage,
                )
                if response.content and _ASSESSMENT_PATTERN.search(response.content):
                    pending_assessment = _extract_assessment(response.content)

                # Add assistant message to conversation
                messages.append(self._format_assistant_message(response, valid_tool_calls))

                # Execute each tool call and add results
                for tc in valid_tool_calls:
                    result, cost_entry = self._execute_tool_call(tc)
                    turn_number += 1
                    trace.add_tool_turn(
                        turn_number=turn_number,
                        tool_name=tc.name,
                        tool_result=result.model_dump(),
                    )

                    messages.append(
                        format_tool_result(
                            tool_call_id=tc.id,
                            tool_name=tc.name,
                            result=result.model_dump(),
                        )
                    )

                    logger.info(
                        "Tool %s → %s",
                        tc.name,
                        "success" if result.success else f"failed: {result.error_message}",
                    )

                # Add reflection prompt after tool results
                if self.config.enable_reflection:
                    messages.append(get_reflection_prompt())

            else:
                # LLM responded with text (no tool call) → it's done
                self._finalize_assessment(trace, messages, response, turn_number)
                break
        else:
            # Hit max_turns without finishing
            logger.warning("Agent hit max turns (%d) without concluding.", self.config.max_turns)
            trace.set_final_response(_salvage_assessment(trace, pending_assessment))

        trace.messages = messages  # the exact conversation, for RFT rollout capture
        self._finalize_trace(trace)
        return trace

    def run_streaming(
        self,
        patient_info: str,
        case_id: str | None = None,
    ):
        """Run the agent and yield SSE event dicts with real-time token streaming.

        Yields delta events for thinking and assessment content so the frontend
        can render tokens as they arrive.

        Event types:
          - thinking_delta: partial thinking text token
          - thinking: complete thinking block (sent after all deltas)
          - tool_call: tool invocation
          - tool_result: tool output
          - reflection: reflection marker
          - assessment_delta: partial assessment text token
          - assessment: complete assessment (sent after all deltas)
          - run_complete: final summary
        """
        trace = AgentTrace(case_id=case_id)
        trace.start_timer()
        self.cost_tracker.reset()

        messages = self._build_initial_messages(patient_info)
        tool_definitions = self._get_tool_definitions()
        tool_request = self._tool_request_kwargs(tool_definitions)

        turn_number = 0
        # Mirrors run(): salvage-only, never finalizes early. Keep in sync.
        pending_assessment: str | None = None
        for _ in range(self.config.max_turns):
            turn_number += 1

            # Stream LLM response token-by-token
            response = None
            think_content = None
            for event in self.llm.chat_stream(
                messages=messages,
                **tool_request,
            ):
                if event["type"] == "think_delta":
                    # Internal reasoning tokens (from <think> tags)
                    yield {
                        "type": "think_delta",
                        "turn_number": turn_number,
                        "delta": event["delta"],
                    }
                elif event["type"] == "content_delta":
                    # Visible reasoning tokens
                    yield {
                        "type": "content_delta",
                        "turn_number": turn_number,
                        "delta": event["delta"],
                    }
                elif event["type"] == "done":
                    response = event["response"]
                    think_content = event.get("think_content")

            if response is None:
                break

            # Filter out hallucinated tool names (e.g. "Final Assessment")
            valid_tool_calls = self._valid_tool_calls(response)

            if valid_tool_calls:
                # Record thinking
                trace.add_assistant_turn(
                    turn_number=turn_number,
                    content=response.content,
                    tool_calls=self._tool_call_records(valid_tool_calls),
                    token_usage=response.usage,
                )
                if response.content and _ASSESSMENT_PATTERN.search(response.content):
                    pending_assessment = _extract_assessment(response.content)

                # If the model didn't produce visible reasoning text (common with
                # Ollama/Qwen3.5 which hides reasoning in <think> tags), extract
                # reasoning from the clinical_context argument of tool calls.
                reasoning = response.content or ""
                if not reasoning and not think_content:
                    contexts = []
                    for tc in valid_tool_calls:
                        ctx = tc.arguments.get("clinical_context", "")
                        if ctx:
                            contexts.append(f"**{tc.name}**: {ctx}")
                    if contexts:
                        reasoning = "\n\n".join(contexts)

                # Send complete thinking event (for replay/trace)
                yield {
                    "type": "thinking",
                    "turn_number": turn_number,
                    "content": reasoning,
                    "think_content": think_content or "",
                    "token_usage": response.usage,
                }

                messages.append(self._format_assistant_message(response, valid_tool_calls))

                # Execute each tool call
                for tc in valid_tool_calls:
                    yield {
                        "type": "tool_call",
                        "turn_number": turn_number,
                        "tool_name": tc.name,
                        "arguments": tc.arguments,
                    }

                    result, cost_entry = self._execute_tool_call(tc)
                    turn_number += 1
                    trace.add_tool_turn(
                        turn_number=turn_number,
                        tool_name=tc.name,
                        tool_result=result.model_dump(),
                    )

                    yield {
                        "type": "tool_result",
                        "turn_number": turn_number,
                        "tool_name": tc.name,
                        "success": result.success,
                        "output": result.model_dump(),
                        "cost_usd": cost_entry.cost_usd,
                    }

                    messages.append(
                        format_tool_result(
                            tool_call_id=tc.id,
                            tool_name=tc.name,
                            result=result.model_dump(),
                        )
                    )

                # Reflection
                if self.config.enable_reflection:
                    messages.append(get_reflection_prompt())
                    yield {"type": "reflection", "turn_number": turn_number}

            else:
                # Final assessment — deltas were already streamed as thinking_delta,
                # now re-emit them as assessment type for the complete record.
                # Shared finalization (incl. the one-shot structured-diagnosis
                # re-prompt) so run() and run_streaming() produce identical
                # final_response/trace for identical model output.
                final_content, final_usage, turn_number = self._finalize_assessment(
                    trace, messages, response, turn_number
                )
                yield {
                    "type": "assessment",
                    "turn_number": turn_number,
                    "content": final_content,
                    "token_usage": final_usage,
                }
                break
        else:
            logger.warning("Agent hit max turns (%d) without concluding.", self.config.max_turns)
            trace.set_final_response(_salvage_assessment(trace, pending_assessment))

        trace.messages = messages  # the exact conversation, for RFT rollout capture
        self._finalize_trace(trace)
        yield {
            "type": "run_complete",
            "total_tool_calls": trace.total_tool_calls,
            "tools_called": trace.tools_called,
            "total_tokens": trace.total_tokens,
            "elapsed_time_seconds": trace.elapsed_time_seconds,
            "final_response": trace.final_response,
            "total_cost_usd": trace.total_cost_usd,
        }

    def run_all_info_upfront(
        self,
        patient_info: str,
        tool_outputs_text: str,
        case_id: str | None = None,
    ) -> AgentTrace:
        """Ablation: give the agent all tool outputs at once (no sequential reasoning).

        Args:
            patient_info: Initial clinical information.
            tool_outputs_text: Pre-formatted string of all tool outputs.
            case_id: Case identifier.

        Returns:
            AgentTrace with the agent's single-shot response.
        """
        trace = AgentTrace(case_id=case_id)
        trace.start_timer()
        self.cost_tracker.reset()

        combined = (
            f"{patient_info}\n\n"
            f"## Available Test Results\n\n{tool_outputs_text}\n\n"
            "Based on all the information above, provide your diagnostic assessment, "
            "differential diagnosis, and recommendations."
        )

        messages = self._build_initial_messages(combined)

        response = self.llm.chat(messages=messages, tools=None)
        trace.add_assistant_turn(
            turn_number=1,
            content=response.content,
            tool_calls=None,
            token_usage=response.usage,
        )
        trace.set_final_response(
            _extract_assessment(response.content or "")
        )
        trace.messages = messages  # the exact conversation, for RFT rollout capture
        self._finalize_trace(trace)
        return trace

    def _build_initial_messages(
        self, patient_info: str,
    ) -> list[dict[str, Any]]:
        system = self._build_system_prompt()
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": patient_info},
        ]

    def _build_system_prompt(self) -> str:
        base = load_prompt("orchestrator.txt")

        # Reasoning-style directive (concise = unchanged base; differential = show exclusion
        # reasoning). Applied before hospital rules so the composed prompt matches the
        # trajectory system prompts byte-for-byte. See llm.prompts.apply_reasoning_style.
        base = apply_reasoning_style(base, self.config.reasoning_style)

        # Inject ALL hospital rules — agent must determine which pathway applies
        if self.rules:
            context = self.rules.get_context()
            if context:
                base += f"\n\n## Hospital Protocols\n{context}"

        return base

    def _get_tool_definitions(self) -> list[dict[str, Any]]:
        all_defs = self.tools.get_all_definitions()
        return restrict_tools(
            all_defs,
            allowed_tools=self.config.allowed_tools,
            excluded_tools=self.config.excluded_tools,
        )

    def _tool_request_kwargs(self, tool_definitions: list[dict[str, Any]]) -> dict[str, Any]:
        if not tool_definitions:
            return {"tools": None, "tool_choice": None}
        return {"tools": tool_definitions, "tool_choice": "auto"}

    def _valid_tool_calls(self, response: LLMResponse) -> list[LLMToolCall]:
        valid: list[LLMToolCall] = []
        for tool_call in response.tool_calls or []:
            if tool_call.name in self.tools.tools:
                valid.append(tool_call)
                continue
            logger.warning(
                "Ignoring unknown tool call %s. Available tools: %s",
                tool_call.name,
                sorted(self.tools.tools),
            )
        return valid

    def _tool_call_records(self, tool_calls: list[LLMToolCall]) -> list[dict[str, Any]]:
        return [{"name": tc.name, "arguments": tc.arguments} for tc in tool_calls]

    def _execute_tool_call(self, tool_call: LLMToolCall) -> tuple[ToolResult, Any]:
        result = self.tools.execute(
            ToolCall(tool_name=tool_call.name, parameters=tool_call.arguments)
        )
        cost_entry = self.cost_tracker.compute_cost(tool_call.name, tool_call.arguments)
        result.cost_usd = cost_entry.cost_usd
        return result, cost_entry

    def _finalize_assessment(
        self,
        trace: AgentTrace,
        messages: list[dict[str, Any]],
        response: LLMResponse,
        turn_number: int,
    ) -> tuple[str, dict[str, Any] | None, int]:
        """Shared finalization for run() and run_streaming().

        Records the concluding assistant turn, extracts the structured
        assessment, and — if the model produced reasoning without the required
        ``### Primary Diagnosis`` section — re-prompts once (non-streaming)
        for the structured format. Sets ``trace.final_response`` so identical
        model output yields an identical final_response/trace in both entry
        points.

        Returns:
            (final_content, final_usage, turn_number): the assistant text the
            final_response was extracted from, its token usage, and the
            (possibly incremented) turn number — used by the streaming path
            to emit the ``assessment`` event.
        """
        trace.add_assistant_turn(
            turn_number=turn_number,
            content=response.content,
            tool_calls=None,
            token_usage=response.usage,
        )

        final_content = response.content or ""
        final_usage = response.usage
        assessment = _extract_assessment(final_content)

        # If the model produced reasoning but no structured diagnosis,
        # re-prompt once to get the required output format.
        if assessment and not _ASSESSMENT_PATTERN.search(assessment):
            logger.info("No structured diagnosis found — re-prompting for format.")
            messages.append(self._format_assistant_message(response, []))
            messages.append({
                "role": "user",
                "content": _STRUCTURED_DIAGNOSIS_REPROMPT,
            })
            retry = self.llm.chat(messages=messages, tools=None)
            turn_number += 1
            trace.add_assistant_turn(
                turn_number=turn_number,
                content=retry.content,
                tool_calls=None,
                token_usage=retry.usage,
            )
            retry_assessment = _extract_assessment(retry.content or "")
            if retry_assessment:
                assessment = retry_assessment
                final_content = retry.content or ""
                final_usage = retry.usage

        trace.set_final_response(assessment)
        return final_content, final_usage, turn_number

    def _finalize_trace(self, trace: AgentTrace) -> None:
        trace.total_cost_usd = self.cost_tracker.total_cost_usd
        trace.cost_entries = [entry.model_dump() for entry in self.cost_tracker.entries]

    def _format_assistant_message(
        self,
        response: LLMResponse,
        tool_calls: list[LLMToolCall] | object = _USE_RESPONSE_TOOL_CALLS,
    ) -> dict[str, Any]:
        """Format an assistant response as an OpenAI-style message.

        The reasoning goes back into `content` inside `<think>` tags rather than into a
        `reasoning_content` field: Qwen's chat template splits `</think>` out of `content`
        itself, and `content` is the only place the OpenAI schema will carry it through
        vLLM. Without this the template renders an empty `<think></think>` for every prior
        turn, and the agent re-reads a blank where its own deliberation should be — while
        the SFT trajectories it was trained on have the reasoning in full.
        """
        msg: dict[str, Any] = {"role": "assistant"}
        if response.content:
            msg["content"] = response.content
        if response.reasoning:
            body = response.content or ""
            msg["content"] = f"<think>\n{response.reasoning.strip()}\n</think>\n\n{body}"
        selected_tool_calls = (
            response.tool_calls or []
            if tool_calls is _USE_RESPONSE_TOOL_CALLS
            else tool_calls
        )
        if selected_tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": json.dumps(tc.arguments),
                    },
                }
                for tc in selected_tool_calls
            ]
        return msg


def _salvage_assessment(trace: AgentTrace, pending_assessment: str | None) -> str:
    """Best final_response when the loop hits max_turns without finalizing.

    Shared by ``run()`` and ``run_streaming()`` so both entry points salvage
    identically. Preference order:

    1. ``pending_assessment`` — a structured assessment the model embedded in
       a tool-calling turn (a real concluded diagnosis).
    2. The most recent assistant turn with non-empty content, run through
       ``_extract_assessment``. Tool turns carry ``content=None`` (see
       ``AgentTrace.add_tool_turn``), so scanning only the last turn — which
       is always a tool turn when max_turns is exhausted — would discard the
       model's actual reasoning.
    3. ``_NO_CONCLUSION_MESSAGE`` if the trace has no usable assistant text.
    """
    if pending_assessment:
        return pending_assessment
    for turn in reversed(trace.turns):
        if turn.role == "assistant" and turn.content:
            extracted = _extract_assessment(turn.content)
            if extracted:
                return extracted
    return _NO_CONCLUSION_MESSAGE


def _extract_assessment(text: str) -> str:
    """Extract the structured clinical assessment from the agent's final turn.

    The agent's last message typically contains reasoning preamble (THINK/REFLECT)
    followed by the structured assessment (### Primary Diagnosis ...).  This
    function extracts only the structured part for ``final_response``.

    If no structured heading is found, the full text is returned as-is.
    """
    if not text:
        return text
    m = _ASSESSMENT_PATTERN.search(text)
    if m:
        return m.group(1).strip()
    return text.strip()
