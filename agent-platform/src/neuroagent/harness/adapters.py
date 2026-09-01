"""Model-family adapters that normalize generation into one typed clinical action."""

from __future__ import annotations

import json
from typing import Any

from neuroagent_schemas import ClinicalAction, SubmitAssessment, ToolAction
from pydantic import TypeAdapter, ValidationError

from ..llm.client import LLMClient, LLMResponseDecodeError
from .context import episode_messages
from .interfaces import ModelTurn


_ACTION_ADAPTER = TypeAdapter(ClinicalAction)
_SUBMIT_NAME = "submit_assessment"
_SUBMIT_TOOL = {
    "type": "function",
    "function": {
        "name": _SUBMIT_NAME,
        "description": "Finish the encounter with the structured clinical assessment.",
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "primary_diagnosis",
                "differential",
                "confidence",
                "urgency",
                "recommendations",
            ],
            "properties": {
                "primary_diagnosis": {"type": "string", "minLength": 1},
                "differential": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["diagnosis"],
                        "properties": {
                            "diagnosis": {"type": "string", "minLength": 1},
                            "confidence": {
                                "anyOf": [{"type": "number", "minimum": 0, "maximum": 1}, {"type": "null"}]
                            },
                        },
                    },
                },
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "urgency": {"type": "string", "enum": ["emergent", "urgent", "routine"]},
                "recommendations": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
}


class ActionDecodeError(ValueError):
    """The provider response cannot be normalized into exactly one allowed action."""


def _usage(response: Any, key: str) -> int:
    return int((response.usage or {}).get(key, 0))


class NativeToolModelAdapter:
    adapter_id = "native-tools"

    def __init__(self, client: LLMClient, model_id: str) -> None:
        self.client = client
        self.model_id = model_id

    def next_action(
        self,
        *,
        case,
        episode,
        allowed_tools: list[dict[str, Any]],
        require_assessment: bool = False,
        react: bool = False,
    ) -> ModelTurn:
        tools = [_SUBMIT_TOOL] if require_assessment else [*allowed_tools, _SUBMIT_TOOL]
        try:
            response = self.client.chat(
                episode_messages(case, episode, react=react),
                tools=tools,
                tool_choice="required",
            )
        except LLMResponseDecodeError as exc:
            raise ActionDecodeError(str(exc)) from exc
        calls = response.tool_calls or []
        if len(calls) != 1:
            raise ActionDecodeError(f"expected exactly one tool call, received {len(calls)}")
        call = calls[0]
        allowed_names = {item["function"]["name"] for item in tools}
        if call.name not in allowed_names:
            raise ActionDecodeError(f"tool {call.name!r} is not allowed")
        try:
            action = (
                SubmitAssessment(**call.arguments)
                if call.name == _SUBMIT_NAME
                else ToolAction(tool_name=call.name, arguments=call.arguments)
            )
        except ValidationError as exc:
            raise ActionDecodeError(str(exc)) from exc
        payload = {}
        if react and response.content and response.content.strip():
            payload["react.rationale"] = response.content.strip()
        return ModelTurn(
            action=action,
            prompt_tokens=_usage(response, "prompt_tokens"),
            completion_tokens=_usage(response, "completion_tokens"),
            latency_seconds=response.latency_seconds,
            plugin_payload=payload,
        )


class JsonActionModelAdapter:
    adapter_id = "json-action"

    def __init__(self, client: LLMClient, model_id: str) -> None:
        self.client = client
        self.model_id = model_id

    def next_action(
        self,
        *,
        case,
        episode,
        allowed_tools: list[dict[str, Any]],
        require_assessment: bool = False,
        react: bool = False,
    ) -> ModelTurn:
        if react:
            raise ActionDecodeError("the JSON adapter is not part of the ReAct ablation")
        allowed_names = [item["function"]["name"] for item in allowed_tools]
        instruction = (
            "Return one JSON object matching the supplied schema. "
            + ("You must submit_assessment now." if require_assessment else
               f"For a tool action, tool_name must be one of: {allowed_names}.")
        )
        messages = episode_messages(case, episode)
        messages.append({"role": "user", "content": instruction})
        schema = _ACTION_ADAPTER.json_schema()
        response = self.client.chat(
            messages,
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "clinical_action", "strict": True, "schema": schema},
            },
        )
        if not response.content:
            raise ActionDecodeError("model returned no JSON content")
        try:
            raw = json.loads(response.content)
            action = _ACTION_ADAPTER.validate_python(raw)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ActionDecodeError(str(exc)) from exc
        if require_assessment and isinstance(action, ToolAction):
            raise ActionDecodeError("a final assessment is required")
        if isinstance(action, ToolAction) and action.tool_name not in allowed_names:
            raise ActionDecodeError(f"tool {action.tool_name!r} is not allowed")
        return ModelTurn(
            action=action,
            prompt_tokens=_usage(response, "prompt_tokens"),
            completion_tokens=_usage(response, "completion_tokens"),
            latency_seconds=response.latency_seconds,
        )
