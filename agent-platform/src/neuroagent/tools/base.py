from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any


class ToolCall(BaseModel):
    """What the agent produces when it wants to call a tool."""
    tool_name: str
    parameters: dict[str, Any] = {}


class ToolResult(BaseModel):
    """What the tool returns to the agent."""
    tool_name: str
    success: bool
    output: dict[str, Any] | None = None  # serialized tool output
    error_message: str | None = None
    cost_usd: float | None = None  # populated by CostTracker


class BaseTool(ABC):
    name: str
    description: str
    parameter_schema: dict[str, Any]

    @abstractmethod
    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        """Execute the tool and return a result."""

    def get_tool_definition(self) -> dict[str, Any]:
        """Return OpenAI-style tool definition for the LLM."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameter_schema,
            },
        }
