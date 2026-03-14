"""Unified LLM client supporting OpenAI-compatible APIs (vLLM, OpenAI, Anthropic)."""

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
        self.client = OpenAI(base_url=base_url, api_key=api_key)
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
