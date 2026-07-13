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
    # The model's own reasoning for this turn, with `<think>` tags removed. `content` never
    # carries it, because everything downstream that reads `content` — the diagnosis matcher,
    # the trace, the UI — wants the answer, not the deliberation. But the *next* prompt does:
    # the agent must be able to build on what it just worked out. See
    # `AgentOrchestrator._format_assistant_message`.
    reasoning: str | None = None


@dataclass
class LLMToolCall:
    """A tool call extracted from an LLM response."""

    id: str
    name: str
    arguments: dict[str, Any]


class ThinkTagStreamParser:
    """Incremental parser splitting a streamed response into content vs. think text.

    Qwen3.x thinking mode wraps chain-of-thought in ``<think>...</think>``. When
    streaming, a tag can be split across delta chunks (``"<thi"`` + ``"nk>"``) or a
    single chunk can contain both tags plus surrounding text. This buffers just
    enough text to resolve tags deterministically:

    - ``feed(text)`` returns ``[(kind, piece), ...]`` events, where ``kind`` is
      ``"content"`` or ``"think"``. Tag text itself is never emitted.
    - ``flush()`` returns events for whatever remains buffered at end-of-stream
      (e.g. a trailing partial tag that never completed).

    An orphaned ``</think>`` without a preceding ``<think>`` (a known Qwen quirk,
    see ``strip_think_tags``) is stripped and treated as a no-op boundary.
    """

    _OPEN = "<think>"
    _CLOSE = "</think>"

    def __init__(self) -> None:
        self._buffer = ""
        self.in_think = False

    def feed(self, text: str) -> list[tuple[str, str]]:
        self._buffer += text
        events: list[tuple[str, str]] = []

        while True:
            if self.in_think:
                idx = self._buffer.find(self._CLOSE)
                if idx != -1:
                    if idx:
                        events.append(("think", self._buffer[:idx]))
                    self._buffer = self._buffer[idx + len(self._CLOSE):]
                    self.in_think = False
                    continue
                kind, tags = "think", (self._CLOSE,)
            else:
                # Outside a think block, watch for an opening tag and also strip
                # orphaned closing tags (model sometimes omits the opening one).
                found = [
                    (i, t)
                    for t in (self._OPEN, self._CLOSE)
                    if (i := self._buffer.find(t)) != -1
                ]
                if found:
                    idx, tag = min(found)
                    if idx:
                        events.append(("content", self._buffer[:idx]))
                    self._buffer = self._buffer[idx + len(tag):]
                    self.in_think = tag == self._OPEN
                    continue
                kind, tags = "content", (self._OPEN, self._CLOSE)

            # No complete tag in the buffer: emit everything except a trailing
            # fragment that could still turn into one of the awaited tags.
            hold = max(self._partial_tag_suffix(tag) for tag in tags)
            emit_len = len(self._buffer) - hold
            if emit_len > 0:
                events.append((kind, self._buffer[:emit_len]))
                self._buffer = self._buffer[emit_len:]
            return events

    def flush(self) -> list[tuple[str, str]]:
        """End-of-stream: return any buffered text under the current state."""
        if not self._buffer:
            return []
        events = [("think" if self.in_think else "content", self._buffer)]
        self._buffer = ""
        return events

    def _partial_tag_suffix(self, tag: str) -> int:
        """Length of the longest buffer suffix that is a proper prefix of ``tag``."""
        for k in range(min(len(tag) - 1, len(self._buffer)), 0, -1):
            if self._buffer.endswith(tag[:k]):
                return k
        return 0


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
        seed: int | None = None,
        timeout: float = 120.0,
        max_retries: int = 2,
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
            timeout=timeout,
            max_retries=max_retries,
        )
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        # Forwarded as `seed=` on every request so sampling is reproducible even
        # at temperature > 0 (supported by vLLM and the OpenAI API).
        self.seed = seed
        self.timeout = timeout
        self.max_retries = max_retries
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
        if self.seed is not None:
            kwargs["seed"] = self.seed
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
        if self.seed is not None:
            kwargs["seed"] = self.seed
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
        think_parser = ThinkTagStreamParser()

        def _emit(kind: str, piece: str):
            if kind == "think":
                think_parts.append(piece)
                return {"type": "think_delta", "delta": piece}
            content_parts.append(piece)
            return {"type": "content_delta", "delta": piece}

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
                for kind, piece in think_parser.feed(delta.content):
                    yield _emit(kind, piece)

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

        # Flush any text still buffered in the parser (e.g. a trailing partial tag).
        for kind, piece in think_parser.flush():
            yield _emit(kind, piece)

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
                reasoning=think_content.strip() if think_content else None,
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
                    # Same fallback as the streaming path: a malformed argument
                    # payload becomes an empty dict instead of crashing the turn.
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {}
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
        # vLLM's `--reasoning-parser qwen3` splits the thinking out for us; without it the
        # `<think>` block arrives inline. Take whichever we were given, and keep it: the
        # next prompt replays it so the agent can build on its own reasoning.
        reasoning = getattr(message, "reasoning_content", None)
        if not reasoning and content:
            reasoning = extract_think_content(content)
        if content:
            content = strip_think_tags(content)

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            raw=response,
            reasoning=reasoning,
        )


# Pre-compiled regex for stripping <think>...</think> blocks (Qwen3.x thinking mode)
_THINK_PATTERN = re.compile(r"<think>.*?</think>\s*", flags=re.DOTALL)
# Same block, but capturing the body — `_THINK_PATTERN` has no group, so `findall` on it
# would return whole matches including the tags.
_THINK_CAPTURE = re.compile(r"<think>(.*?)</think>", flags=re.DOTALL)


def extract_think_content(text: str) -> str | None:
    """The text inside `<think>...</think>`, or None when the model emitted none."""
    blocks = _THINK_CAPTURE.findall(text)
    joined = "\n".join(b.strip() for b in blocks if b and b.strip())
    return joined or None


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
