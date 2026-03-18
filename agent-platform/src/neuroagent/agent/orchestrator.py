"""Main agent orchestrator — ReAct loop with tool dispatch."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any

import re

from ..llm.client import LLMClient, LLMResponse
from ..llm.prompts import load_prompt, format_tool_result
from ..tools.base import ToolCall, ToolResult
from ..tools.cost_tracker import CostTracker
from ..tools.tool_registry import ToolRegistry
from .planner import restrict_tools
from .reasoning import AgentTrace
from .reflection import get_reflection_prompt

# Regex to extract the structured assessment section from the agent's final turn.
# Matches from the first "### Primary Diagnosis" heading to end of string.
_ASSESSMENT_PATTERN = re.compile(
    r"(###\s*Primary Diagnosis.*)",
    flags=re.DOTALL,
)

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for the agent orchestrator."""

    # LLM settings
    base_url: str = "http://localhost:8000/v1"
    api_key: str = "not-needed"
    model: str = "Qwen/Qwen3.5-9B"
    temperature: float = 1.0
    max_tokens: int = 8192
    top_p: float = 0.95
    presence_penalty: float = 1.5

    # Agent behavior
    max_turns: int = 15
    enable_reflection: bool = True

    # Hospital rules
    hospital: str = "us_mayo"  # Hospital rule set: us_mayo, uk_nhs, de_charite, jp_todai, br_hcfmusp

    # Ablation controls
    allowed_tools: list[str] | None = None
    excluded_tools: list[str] | None = None
    all_info_upfront: bool = False  # If True, give all tool outputs at once

    # Dual-model specialist (optional — disabled by default for backward compat)
    specialist_enabled: bool = False
    specialist_base_url: str = "http://localhost:8001/v1"
    specialist_model: str = "google/medgemma-1.5-4b-it"
    specialist_api_key: str = "not-needed"
    specialist_temperature: float = 0.3  # Lower temp for deterministic specialist
    specialist_max_tokens: int = 4096


class AgentOrchestrator:
    """Main agent implementing the ReAct loop for clinical reasoning."""

    def __init__(
        self,
        config: AgentConfig,
        tool_registry: ToolRegistry,
        memory: Any | None = None,  # PatientMemory (imported lazily to avoid circular deps)
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
        )
        self.tools = tool_registry
        self.memory = memory
        self.rules = rules_engine
        self.cost_tracker = cost_tracker or CostTracker()

    def run(
        self,
        patient_info: str,
        patient_id: str | None = None,
        case_id: str | None = None,
    ) -> AgentTrace:
        """Run the agent on a patient case.

        Args:
            patient_info: Initial clinical information (chief complaint + history).
            patient_id: If set, load/store patient memory.
            case_id: Case identifier for tracing.

        Returns:
            AgentTrace with complete record of reasoning and actions.
        """
        trace = AgentTrace(case_id=case_id)
        trace.start_timer()
        self.cost_tracker.reset()

        messages = self._build_initial_messages(patient_info, patient_id)
        tool_definitions = self._get_tool_definitions()

        turn_number = 0
        for _ in range(self.config.max_turns):
            # Call LLM with tool definitions
            response = self.llm.chat(
                messages=messages,
                tools=tool_definitions if tool_definitions else None,
                tool_choice="auto" if tool_definitions else None,
            )

            turn_number += 1

            # If LLM wants to call tool(s)
            if response.tool_calls:
                # Record assistant turn with tool calls
                trace.add_assistant_turn(
                    turn_number=turn_number,
                    content=response.content,
                    tool_calls=[
                        {"name": tc.name, "arguments": tc.arguments}
                        for tc in response.tool_calls
                    ],
                    token_usage=response.usage,
                )

                # Add assistant message to conversation
                messages.append(self._format_assistant_message(response))

                # Execute each tool call and add results
                for tc in response.tool_calls:
                    tool_call = ToolCall(tool_name=tc.name, parameters=tc.arguments)
                    result = self.tools.execute(tool_call)

                    # Track cost
                    cost_entry = self.cost_tracker.compute_cost(tc.name, tc.arguments)
                    result.cost_usd = cost_entry.cost_usd

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
                trace.add_assistant_turn(
                    turn_number=turn_number,
                    content=response.content,
                    tool_calls=None,
                    token_usage=response.usage,
                )

                assessment = _extract_assessment(response.content or "")

                # If the model produced reasoning but no structured diagnosis,
                # re-prompt once to get the required output format.
                if assessment and not _ASSESSMENT_PATTERN.search(assessment):
                    logger.info("No structured diagnosis found — re-prompting for format.")
                    messages.append(self._format_assistant_message(response))
                    messages.append({
                        "role": "user",
                        "content": (
                            "You provided reasoning but did not include a structured "
                            "diagnosis. Please provide your final assessment now using "
                            "the required format starting with:\n\n"
                            "### Primary Diagnosis\n[Diagnosis] (Confidence: X.XX)"
                        ),
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

                trace.set_final_response(assessment)
                break
        else:
            # Hit max_turns without finishing
            logger.warning("Agent hit max turns (%d) without concluding.", self.config.max_turns)
            last_content = trace.turns[-1].content if trace.turns else ""
            trace.set_final_response(
                _extract_assessment(last_content or "")
                or "[Agent did not reach a conclusion within turn limit]"
            )

        # Finalize cost tracking
        trace.total_cost_usd = self.cost_tracker.total_cost_usd
        trace.cost_entries = [e.model_dump() for e in self.cost_tracker.entries]

        # Store encounter in patient memory
        if self.memory and patient_id:
            self.memory.store_encounter(patient_id, trace)

        return trace

    def run_streaming(
        self,
        patient_info: str,
        patient_id: str | None = None,
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

        messages = self._build_initial_messages(patient_info, patient_id)
        tool_definitions = self._get_tool_definitions()

        turn_number = 0
        for _ in range(self.config.max_turns):
            turn_number += 1

            # Stream LLM response token-by-token
            response = None
            think_content = None
            for event in self.llm.chat_stream(
                messages=messages,
                tools=tool_definitions if tool_definitions else None,
                tool_choice="auto" if tool_definitions else None,
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
            valid_tool_calls = [
                tc for tc in (response.tool_calls or [])
                if tc.name in self.tools.tools
            ]

            if valid_tool_calls:
                # Record thinking
                trace.add_assistant_turn(
                    turn_number=turn_number,
                    content=response.content,
                    tool_calls=[
                        {"name": tc.name, "arguments": tc.arguments}
                        for tc in valid_tool_calls
                    ],
                    token_usage=response.usage,
                )

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

                messages.append(self._format_assistant_message(response))

                # Execute each tool call
                for tc in valid_tool_calls:
                    yield {
                        "type": "tool_call",
                        "turn_number": turn_number,
                        "tool_name": tc.name,
                        "arguments": tc.arguments,
                    }

                    tool_call = ToolCall(tool_name=tc.name, parameters=tc.arguments)
                    result = self.tools.execute(tool_call)

                    # Track cost
                    cost_entry = self.cost_tracker.compute_cost(tc.name, tc.arguments)
                    result.cost_usd = cost_entry.cost_usd

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
                # now re-emit them as assessment type for the complete record
                trace.add_assistant_turn(
                    turn_number=turn_number,
                    content=response.content,
                    tool_calls=None,
                    token_usage=response.usage,
                )
                final = _extract_assessment(response.content or "")
                trace.set_final_response(final)

                yield {
                    "type": "assessment",
                    "turn_number": turn_number,
                    "content": response.content or "",
                    "token_usage": response.usage,
                }
                break
        else:
            last_content = trace.turns[-1].content if trace.turns else ""
            trace.set_final_response(
                _extract_assessment(last_content or "")
                or "[Agent did not reach a conclusion within turn limit]"
            )

        # Finalize cost tracking
        trace.total_cost_usd = self.cost_tracker.total_cost_usd
        trace.cost_entries = [e.model_dump() for e in self.cost_tracker.entries]

        # Store encounter in patient memory
        if self.memory and patient_id:
            self.memory.store_encounter(patient_id, trace)

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

        combined = (
            f"{patient_info}\n\n"
            f"## Available Test Results\n\n{tool_outputs_text}\n\n"
            "Based on all the information above, provide your diagnostic assessment, "
            "differential diagnosis, and recommendations."
        )

        messages = self._build_initial_messages(combined, patient_id=None)

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
        return trace

    def _build_initial_messages(
        self, patient_info: str, patient_id: str | None,
    ) -> list[dict[str, Any]]:
        system = self._build_system_prompt(patient_id)
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": patient_info},
        ]

    def _build_system_prompt(self, patient_id: str | None) -> str:
        try:
            base = load_prompt("orchestrator.txt")
        except FileNotFoundError:
            base = _DEFAULT_SYSTEM_PROMPT

        # Inject ALL hospital rules — agent must determine which pathway applies
        if self.rules:
            context = self.rules.get_context()
            if context:
                base += f"\n\n## Hospital Protocols\n{context}"

        # Inject patient memory
        if self.memory and patient_id:
            history = self.memory.retrieve(patient_id)
            if history:
                base += f"\n\n## Patient History (From Previous Encounters)\n{history}"

        return base

    def _get_tool_definitions(self) -> list[dict[str, Any]]:
        all_defs = self.tools.get_all_definitions()
        return restrict_tools(
            all_defs,
            allowed_tools=self.config.allowed_tools,
            excluded_tools=self.config.excluded_tools,
        )

    def _format_assistant_message(self, response: LLMResponse) -> dict[str, Any]:
        """Format an assistant response as an OpenAI-style message."""
        msg: dict[str, Any] = {"role": "assistant"}
        if response.content:
            msg["content"] = response.content
        if response.tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": json.dumps(tc.arguments),
                    },
                }
                for tc in response.tool_calls
            ]
        return msg


_DEFAULT_SYSTEM_PROMPT = """\
You are NeuroAgent, an expert neurology clinical decision support system. You assist \
neurologists by systematically analyzing patient cases through sequential tool use, \
evidence synthesis, and structured clinical reasoning.

## Your Role
- You are a tool-augmented clinical reasoning agent specialized in neurology.
- You receive a patient's initial clinical information and must determine the diagnosis \
through sequential investigation.
- You have access to diagnostic tools (EEG, MRI, ECG, labs, CSF analysis), medical \
literature search, and drug interaction checking.
- You must decide WHICH tools to call and in WHAT ORDER based on clinical reasoning.

## CRITICAL: Visible Reasoning Before Every Action

You MUST always write your clinical reasoning as text content BEFORE making any tool \
calls. This is essential — your reasoning must be visible to the clinician reviewing \
your work.

**Before your first tool call**, write a brief clinical assessment covering:
- Your initial impression based on the patient presentation
- Your preliminary differential diagnosis
- What investigations you want to order first and WHY

**Before each subsequent tool call**, write your updated reasoning covering:
- What you learned from the previous results
- How the findings changed your differential
- What you want to investigate next and WHY

**Never call a tool without first writing your reasoning.** The text content and tool \
calls are sent together — always include both.

## Reasoning Process (ReAct Loop)
For each step, follow this pattern:

1. **THINK** (write as text): State your current clinical reasoning.
   - What is the current differential diagnosis?
   - What information do you need next?
   - Why are you choosing this particular tool/test?

2. **ACT**: Call the appropriate tool(s) with relevant parameters.

3. **OBSERVE**: Review the tool results (provided by the system).

4. **REFLECT** (write as text): Update your reasoning based on new information.
   - How do these findings change your differential?
   - What is the most likely diagnosis now?
   - Do you need more information or are you ready to conclude?

## Output Format
When you have gathered enough information, provide your final assessment as text \
(without calling any more tools) in this structure:

### Primary Diagnosis
[Diagnosis] (Confidence: X.XX)

### Differential Diagnoses
1. [Alternative 1] - [Key supporting/opposing features]
2. [Alternative 2] - [Key supporting/opposing features]
3. [Alternative 3] - [Key supporting/opposing features]

### Key Evidence
- [Finding 1 from Tool X]
- [Finding 2 from Tool Y]
- [How findings integrate to support the diagnosis]

### Recommendations
1. [Treatment recommendation]
2. [Follow-up plan]
3. [Safety considerations]

### Red Flags / Alerts
- [Any urgent findings or safety concerns]

## Important Guidelines
- Always consider the clinical context when ordering tests.
- Do not order unnecessary tests — each tool call should be clinically justified.
- Flag any urgent or emergent findings immediately.
- Acknowledge uncertainty explicitly with confidence levels.
- Consider patient safety at every step — flag contraindicated actions.
- If results are inconsistent across modalities, note the discrepancy and reason about it.
"""


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
