"""Agent trace and turn models for recording agent reasoning."""

from __future__ import annotations

import time
from pydantic import BaseModel, ConfigDict, Field


class AgentTurn(BaseModel):
    """A single turn in the agent's reasoning chain."""

    turn_number: int
    role: str  # "assistant" or "tool"
    content: str | None = None
    tool_calls: list[dict] | None = None  # raw tool call dicts
    tool_results: list[dict] | None = None  # raw tool result dicts
    token_usage: dict[str, int] = {}


class AgentTrace(BaseModel):
    """Complete record of an agent run on a single case."""

    case_id: str | None = None
    turns: list[AgentTurn] = []
    final_response: str | None = None
    total_tool_calls: int = 0
    tools_called: list[str] = []
    total_tokens: int = 0
    elapsed_time_seconds: float = 0.0
    _start_time: float | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def start_timer(self) -> None:
        self._start_time = time.time()

    def stop_timer(self) -> None:
        if self._start_time is not None:
            self.elapsed_time_seconds = time.time() - self._start_time

    def add_assistant_turn(
        self,
        turn_number: int,
        content: str | None,
        tool_calls: list[dict] | None,
        token_usage: dict[str, int] | None = None,
    ) -> None:
        self.turns.append(
            AgentTurn(
                turn_number=turn_number,
                role="assistant",
                content=content,
                tool_calls=tool_calls,
                token_usage=token_usage or {},
            )
        )
        if token_usage:
            self.total_tokens += token_usage.get("total_tokens", 0)

    def add_tool_turn(
        self,
        turn_number: int,
        tool_name: str,
        tool_result: dict,
    ) -> None:
        self.turns.append(
            AgentTurn(
                turn_number=turn_number,
                role="tool",
                tool_results=[tool_result],
            )
        )
        self.total_tool_calls += 1
        self.tools_called.append(tool_name)

    def set_final_response(self, content: str) -> None:
        self.final_response = content
        self.stop_timer()
