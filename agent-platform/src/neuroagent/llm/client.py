"""Small OpenAI-compatible client with strict tool-argument parsing."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any

from openai import OpenAI

# Request keys the OpenAI SDK accepts as named parameters; everything else (top_k,
# chat_template_kwargs, ...) travels in ``extra_body`` and is understood by vLLM.
_NAMED_PARAMETERS = frozenset({"temperature", "top_p", "presence_penalty", "frequency_penalty", "max_tokens", "seed"})


@dataclass(frozen=True, slots=True)
class LLMToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True, slots=True)
class LLMResponse:
    content: str | None = None
    tool_calls: list[LLMToolCall] = field(default_factory=list)
    usage: dict[str, int] = field(default_factory=dict)
    latency_seconds: float = 0.0


class LLMResponseDecodeError(ValueError):
    """A provider response used valid transport but invalid structured output."""


class LLMClient:
    """Provider-neutral subset required by the clinical harness.

    ``request`` holds the sampling and template settings sent with every chat request
    (temperature, top_p, top_k, presence_penalty, max_tokens, seed, chat_template_kwargs, ...).
    """

    def __init__(
        self,
        *,
        model: str,
        request: dict[str, Any],
        base_url: str = "http://localhost:8000/v1",
        api_key: str = "not-needed",
        timeout: float = 300.0,
        max_retries: int = 2,
    ) -> None:
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout, max_retries=max_retries)
        self.model = model
        self.request = {"max_tokens": 4096, **request}

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {"model": self.model, "messages": _wire_messages(messages)}
        kwargs.update({key: value for key, value in self.request.items() if key in _NAMED_PARAMETERS})
        extra_body = {key: value for key, value in self.request.items() if key not in _NAMED_PARAMETERS}
        if extra_body:
            kwargs["extra_body"] = extra_body
        if tools is not None:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice or "auto"
        if response_format is not None:
            kwargs["response_format"] = response_format
        started = time.perf_counter()
        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message
        usage = {}
        if response.usage:
            usage = {
                "prompt_tokens": int(response.usage.prompt_tokens),
                "completion_tokens": int(response.usage.completion_tokens),
            }
        return LLMResponse(
            content=message.content,
            tool_calls=[
                LLMToolCall(
                    id=call.id,
                    name=call.function.name,
                    arguments=_decode_arguments(call.function.arguments),
                )
                for call in (message.tool_calls or [])
            ],
            usage=usage,
            latency_seconds=time.perf_counter() - started,
        )


def _wire_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Serialize tool-call arguments: the transcript keeps mappings, the API wants JSON strings."""
    wired = []
    for message in messages:
        calls = message.get("tool_calls")
        if calls:
            message = {
                **message,
                "tool_calls": [
                    {
                        **call,
                        "function": {
                            **call["function"],
                            "arguments": json.dumps(call["function"]["arguments"], sort_keys=True),
                        },
                    }
                    for call in calls
                ],
            }
        wired.append(message)
    return wired


def _decode_arguments(arguments: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(arguments, dict):
        return arguments
    try:
        decoded = json.loads(arguments)
    except json.JSONDecodeError as exc:
        raise LLMResponseDecodeError("tool arguments are not valid JSON") from exc
    if not isinstance(decoded, dict):
        raise LLMResponseDecodeError("tool arguments must decode to a JSON object")
    return decoded
