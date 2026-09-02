"""Model adapter that normalizes native tool calling into one typed clinical action."""

from __future__ import annotations

from typing import Any

from neuroagent_schemas import ClinicalAction, SubmitAssessment, ToolAction
from pydantic import ValidationError

from ..llm.client import LLMClient, LLMResponseDecodeError
from .context import SUBMIT_NAME, transcript
from .interfaces import ModelTurn


class ActionDecodeError(ValueError):
    """The provider response cannot be normalized into exactly one allowed action."""


def _inline_refs(schema: dict[str, Any]) -> dict[str, Any]:
    """Resolve local ``$ref`` pointers so the schema can be embedded as a tool definition."""
    definitions = schema.get("$defs", {})

    def resolve(node: Any) -> Any:
        if isinstance(node, dict):
            if "$ref" in node:
                return resolve(definitions[node["$ref"].rsplit("/", 1)[-1]])
            return {key: resolve(value) for key, value in node.items() if key != "$defs"}
        if isinstance(node, list):
            return [resolve(item) for item in node]
        return node

    return resolve(schema)


_SUBMIT_SCHEMA = _inline_refs(SubmitAssessment.model_json_schema())
_SUBMIT_PARAMETERS = {
    **_SUBMIT_SCHEMA,
    "properties": {k: v for k, v in _SUBMIT_SCHEMA["properties"].items() if k != "type"},
    "required": [k for k in _SUBMIT_SCHEMA["required"] if k != "type"],
}
_SUBMIT_PARAMETERS.pop("title", None)

SUBMIT_TOOL = {
    "type": "function",
    "function": {
        "name": SUBMIT_NAME,
        "description": "Finish the encounter with the structured clinical assessment.",
        "parameters": _SUBMIT_PARAMETERS,
    },
}


def _usage(response: Any, key: str) -> int:
    return int(response.usage.get(key, 0))


def _final_turn(correction: str | None) -> str:
    """Models given full evidence tend to conclude in prose; the final turn must say what to call."""
    instruction = "This is the final turn: call submit_assessment now with the structured assessment."
    return f"{correction} {instruction}" if correction else instruction


def _validate(action: ClinicalAction, allowed: set[str], *, require_assessment: bool) -> None:
    if isinstance(action, ToolAction):
        if require_assessment:
            raise ActionDecodeError("a final assessment is required on this turn")
        if action.tool_name not in allowed:
            raise ActionDecodeError(
                f"tool {action.tool_name!r} does not exist; available tools: {sorted(allowed)}"
            )


class NativeToolModelAdapter:
    adapter_id = "native-tools"

    def __init__(self, client: LLMClient) -> None:
        self.client = client
        self.model_id = client.model

    def next_action(
        self,
        *,
        case,
        episode,
        allowed_tools: list[dict[str, Any]],
        require_assessment: bool = False,
        react: bool = False,
        correction: str | None = None,
    ) -> ModelTurn:
        # The catalogue is identical on every turn so the rendered transcript chains as prefixes
        # (training sequences depend on it); the final turn is enforced by instruction and validation.
        tools = [*allowed_tools, SUBMIT_TOOL]
        if require_assessment:
            correction = _final_turn(correction)
        # ``auto`` rather than ``required``: vLLM's required-mode grammar suppressed all assistant
        # content (so the ReAct rationale never appeared) and still allowed several calls at once
        # (measured on Qwen3.5-9B, vLLM 0.23). A text-only reply is an invalid action and is
        # retried with a correction like any other decode failure.
        try:
            response = self.client.chat(
                transcript(case, episode, react=react, correction=correction),
                tools=tools,
                tool_choice="auto",
            )
        except LLMResponseDecodeError as exc:
            raise ActionDecodeError(str(exc)) from exc
        calls = response.tool_calls
        if not calls:
            raise ActionDecodeError(
                "no function call in the response; a prose answer is not an action"
                + (f" (response began: {response.content[:160]!r})" if response.content else "")
            )
        if len(calls) != 1:
            raise ActionDecodeError(f"expected exactly one function call, received {len(calls)}")
        call = calls[0]
        try:
            action = (
                SubmitAssessment(**call.arguments)
                if call.name == SUBMIT_NAME
                else ToolAction(tool_name=call.name, arguments=call.arguments)
            )
        except ValidationError as exc:
            raise ActionDecodeError(str(exc)) from exc
        _validate(
            action,
            {item["function"]["name"] for item in allowed_tools},
            require_assessment=require_assessment,
        )
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
