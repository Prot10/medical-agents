"""Unified LLM client supporting OpenAI-compatible APIs (vLLM, OpenAI, Ollama)."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Any

from openai import OpenAI
from pydantic import BaseModel


@dataclass
class LLMResponse:
    """Parsed response from the LLM."""

    content: str | None = None
    tool_calls: list[LLMToolCall] | None = None
    usage: dict[str, int] = field(default_factory=dict)
    raw: Any = None


@dataclass
class LLMToolCall:
    """A tool call extracted from an LLM response."""

    id: str
    name: str
    arguments: dict[str, Any]


class LLMClient:
    """Unified LLM client wrapping OpenAI-compatible APIs."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000/v1",
        api_key: str = "not-needed",
        model: str = "Qwen/Qwen3.5-9B",
        temperature: float = 1.0,
        max_tokens: int = 8192,
        top_p: float = 0.95,
        presence_penalty: float = 1.5,
        extra_body: dict[str, Any] | None = None,
    ):
        # Copilot API requires specific headers to authenticate
        default_headers: dict[str, str] = {}
        if "githubcopilot.com" in base_url:
            default_headers = {
                "Copilot-Integration-Id": "vscode-chat",
                "Editor-Version": "vscode/1.85.1",
            }
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            default_headers=default_headers or None,
        )
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.extra_body = extra_body or {}

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | None = "auto",
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Send a chat completion request and return a parsed response."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
        }
        if self.extra_body:
            kwargs["extra_body"] = self.extra_body
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        response = self.client.chat.completions.create(**kwargs)
        return self._parse_response(response)

    def chat_stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | None = "auto",
        temperature: float | None = None,
        max_tokens: int | None = None,
    ):
        """Stream a chat completion, yielding delta events.

        Yields dicts with keys:
          - {"type": "content_delta", "delta": str}   — visible text token
          - {"type": "think_delta", "delta": str}     — internal reasoning token
          - {"type": "done", "response": LLMResponse, "think_content": str|None}
        """
        # Always use OpenAI-compatible API for streaming.
        # Ollama's native API with think=true + tools is broken for Qwen3.5
        # (see https://github.com/ollama/ollama/issues/14493).
        yield from self._chat_stream_openai(messages, tools, tool_choice, temperature, max_tokens)

    def _chat_stream_openai(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None,
        tool_choice: str | None,
        temperature: float | None,
        max_tokens: int | None,
    ):
        """Stream via OpenAI-compatible API (vLLM) with <think> tag parsing."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if self.extra_body:
            kwargs["extra_body"] = self.extra_body
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        stream = self.client.chat.completions.create(**kwargs)

        content_parts: list[str] = []
        think_parts: list[str] = []
        tool_calls_acc: dict[int, dict[str, Any]] = {}
        usage: dict[str, int] = {}
        in_think = False

        for chunk in stream:
            if chunk.usage:
                usage = {
                    "prompt_tokens": chunk.usage.prompt_tokens,
                    "completion_tokens": chunk.usage.completion_tokens,
                    "total_tokens": chunk.usage.total_tokens,
                }

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.content:
                text = delta.content

                if "<think>" in text:
                    in_think = True
                    before = text.split("<think>")[0]
                    if before:
                        content_parts.append(before)
                        yield {"type": "content_delta", "delta": before}
                    continue
                if "</think>" in text:
                    in_think = False
                    after = text.split("</think>", 1)[1]
                    if after:
                        content_parts.append(after)
                        yield {"type": "content_delta", "delta": after}
                    continue
                if in_think:
                    think_parts.append(text)
                    yield {"type": "think_delta", "delta": text}
                    continue

                content_parts.append(text)
                yield {"type": "content_delta", "delta": text}

            if delta.tool_calls:
                for tc_delta in delta.tool_calls:
                    idx = tc_delta.index
                    if idx not in tool_calls_acc:
                        tool_calls_acc[idx] = {
                            "id": tc_delta.id or "",
                            "name": tc_delta.function.name if tc_delta.function and tc_delta.function.name else "",
                            "arguments": "",
                        }
                    if tc_delta.function and tc_delta.function.arguments:
                        tool_calls_acc[idx]["arguments"] += tc_delta.function.arguments
                    if tc_delta.id:
                        tool_calls_acc[idx]["id"] = tc_delta.id
                    if tc_delta.function and tc_delta.function.name:
                        tool_calls_acc[idx]["name"] = tc_delta.function.name

        think_content = "".join(think_parts) or None
        content = "".join(content_parts) or None
        parsed_tool_calls = None
        if tool_calls_acc:
            parsed_tool_calls = []
            for idx in sorted(tool_calls_acc.keys()):
                tc = tool_calls_acc[idx]
                try:
                    args = json.loads(tc["arguments"])
                except (json.JSONDecodeError, KeyError):
                    args = {}
                parsed_tool_calls.append(
                    LLMToolCall(id=tc["id"], name=tc["name"], arguments=args)
                )

        yield {
            "type": "done",
            "response": LLMResponse(
                content=content,
                tool_calls=parsed_tool_calls,
                usage=usage,
            ),
            "think_content": think_content,
        }

    def _parse_response(self, response: Any) -> LLMResponse:
        """Parse an OpenAI-style response into our LLMResponse."""
        choice = response.choices[0]
        message = choice.message

        tool_calls = None
        if message.tool_calls:
            tool_calls = []
            for tc in message.tool_calls:
                args = tc.function.arguments
                if isinstance(args, str):
                    args = json.loads(args)
                tool_calls.append(
                    LLMToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=args,
                    )
                )

        usage = {}
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        content = message.content
        if content:
            content = strip_think_tags(content)

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            raw=response,
        )


# Pre-compiled regex for stripping <think>...</think> blocks (Qwen3.x thinking mode)
_THINK_PATTERN = re.compile(r"<think>.*?</think>\s*", flags=re.DOTALL)


def strip_think_tags(text: str) -> str:
    """Remove <think>...</think> blocks from model output.

    Qwen3.x models in thinking mode wrap internal chain-of-thought reasoning
    in <think>...</think> tags. This strips them so only the visible response
    remains.  Also handles partial/unclosed tags (e.g. ``</think>`` without
    a preceding ``<think>``).
    """
    text = _THINK_PATTERN.sub("", text)
    # Handle orphaned closing tags (model sometimes omits opening <think>)
    text = text.replace("</think>", "")
    return text.strip()
