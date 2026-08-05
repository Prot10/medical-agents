from __future__ import annotations
from abc import ABC
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .mock_server import MockServer


class ToolCall(BaseModel):
    """What the agent produces when it wants to call a tool."""
    tool_name: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """What the tool returns to the agent.

    ``extra="forbid"`` so a mistyped field name (e.g. ``error=`` instead of
    ``error_message=``) raises at construction time instead of being silently
    dropped.
    """
    model_config = ConfigDict(extra="forbid")

    tool_name: str
    success: bool
    output: dict[str, Any] | None = None  # serialized tool output
    error_message: str | None = None
    cost_usd: float | None = None  # populated by CostTracker
    from_fallback: bool = False  # True if served from the off-pathway fallback tier


class BaseTool(ABC):
    """Base class for the 16 diagnostic tools.

    ``execute()`` is a template method shared by every tool: validate the
    parameters (warn-only hook), then dispatch to the MockServer in evaluation
    mode or to the real backend otherwise. Subclasses only declare what
    differs — ``name``, ``description``, ``parameter_schema`` — and may
    override ``_validate_parameters`` / ``_execute_real``.
    """

    name: str
    description: str
    parameter_schema: dict[str, Any]

    def __init__(self, mock_server: MockServer | None = None):
        self.mock_server = mock_server

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        """Execute the tool and return a result."""
        self._validate_parameters(parameters)
        if self.mock_server:
            return self.mock_server.get_output(self.name, parameters)
        return self._execute_real(parameters)

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Hook for tool-specific parameter validation.

        Implementations must be warn-only: log the problem and return, never
        raise or alter the result — agent-visible behavior must not change
        based on validation (see tools/vocabulary.py).
        """

    def _execute_real(self, parameters: dict[str, Any]) -> ToolResult:
        """Execute against the real backend (no mock server configured)."""
        raise NotImplementedError(f"Real {self.name} model not yet connected")

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
