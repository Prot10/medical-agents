"""Small OpenAI-compatible client with strict tool-argument parsing."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Iterator

from openai import OpenAI


@dataclass(frozen=True, slots=True)
class LLMToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True, slots=True)
class LLMResponse:
    content: str | None = None
    tool_calls: list[LLMToolCall] | None = None
    usage: dict[str, int] = field(default_factory=dict)
    latency_seconds: float = 0.0
    raw: Any = None


class LLMResponseDecodeError(ValueError):
    """A provider response used valid transport but invalid structured output."""


class LLMClient:
    """Provider-neutral subset required by the clinical harness."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000/v1",
        api_key: str = "not-needed",
        model: str = "Qwen/Qwen3.5-9B",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        top_p: float = 0.95,
        presence_penalty: float = 0.0,
        seed: int | None = None,
        timeout: float = 120.0,
        max_retries: int = 2,
        extra_body: dict[str, Any] | None = None,
    ) -> None:
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.seed = seed
        self.extra_body = extra_body or {}

    def _kwargs(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None,
        tool_choice: str | None,
        temperature: float | None,
        max_tokens: int | None,
        response_format: dict[str, Any] | None,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
            "max_tokens": self.max_tokens if max_tokens is None else max_tokens,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
        }
        if self.seed is not None:
            kwargs["seed"] = self.seed
        if self.extra_body:
            kwargs["extra_body"] = self.extra_body
        if tools is not None:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice
        if response_format is not None:
            kwargs["response_format"] = response_format
        return kwargs

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | None = "auto",
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> LLMResponse:
        started = time.perf_counter()
        response = self.client.chat.completions.create(
            **self._kwargs(
                messages,
                tools=tools,
                tool_choice=tool_choice,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
            )
        )
        return self._parse_response(response, time.perf_counter() - started)

    def chat_stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | None = "auto",
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        started = time.perf_counter()
        kwargs = self._kwargs(
            messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
        )
        kwargs.update({"stream": True, "stream_options": {"include_usage": True}})
        content: list[str] = []
        calls: dict[int, dict[str, str]] = {}
        usage: dict[str, int] = {}
        for chunk in self.client.chat.completions.create(**kwargs):
            if chunk.usage:
                usage = {
                    "prompt_tokens": int(chunk.usage.prompt_tokens),
                    "completion_tokens": int(chunk.usage.completion_tokens),
                    "total_tokens": int(chunk.usage.total_tokens),
                }
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta.content:
                content.append(delta.content)
                yield {"type": "content_delta", "delta": delta.content}
            for call in delta.tool_calls or []:
                current = calls.setdefault(call.index, {"id": "", "name": "", "arguments": ""})
                if call.id:
                    current["id"] = call.id
                if call.function and call.function.name:
                    current["name"] = call.function.name
                if call.function and call.function.arguments:
                    current["arguments"] += call.function.arguments
        parsed_calls = [
            LLMToolCall(
                id=value["id"],
                name=value["name"],
                arguments=_decode_arguments(value["arguments"]),
            )
            for _, value in sorted(calls.items())
        ] or None
        response = LLMResponse(
            content="".join(content) or None,
            tool_calls=parsed_calls,
            usage=usage,
            latency_seconds=time.perf_counter() - started,
        )
        yield {"type": "done", "response": response}

    def _parse_response(self, response: Any, latency: float) -> LLMResponse:
        message = response.choices[0].message
        calls = [
            LLMToolCall(
                id=call.id,
                name=call.function.name,
                arguments=_decode_arguments(call.function.arguments),
            )
            for call in (message.tool_calls or [])
        ] or None
        usage = {}
        if response.usage:
            usage = {
                "prompt_tokens": int(response.usage.prompt_tokens),
                "completion_tokens": int(response.usage.completion_tokens),
                "total_tokens": int(response.usage.total_tokens),
            }
        return LLMResponse(
            content=message.content,
            tool_calls=calls,
            usage=usage,
            latency_seconds=latency,
            raw=response,
        )


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
