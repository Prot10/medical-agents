from __future__ import annotations
from abc import ABC
from functools import cached_property
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, TYPE_CHECKING

from jsonschema import Draft202012Validator

from .vocabulary import normalize_analyte

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
    library: bool = False  # True if the fallback came from the benchmark-level library, not the case
    rejected: bool = False  # True when the call violated the tool's schema and was never placed


class BaseTool(ABC):
    """Base class for the 16 diagnostic tools.

    ``execute()`` is a template method shared by every tool: validate the
    arguments against the advertised ``parameter_schema`` (the catalogue the
    model sees is the contract), then dispatch to the MockServer in evaluation
    mode or to the real backend otherwise. A call that violates the schema is
    answered with a failed result naming the problem, exactly as a real order
    system rejects an unknown study; it is never served a substitute output.
    Assay lists (lab panels, CSF tests, molecular assays) accept any spelling
    that prices and scores as an advertised member (`vocabulary.normalize_analyte`).
    Subclasses only declare what differs — ``name``, ``description``,
    ``parameter_schema`` — and may override ``_execute_real``.
    """

    name: str
    description: str
    parameter_schema: dict[str, Any]

    def __init__(self, mock_server: MockServer | None = None):
        self.mock_server = mock_server

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        """Execute the tool and return a result."""
        error = self.validation_error(parameters)
        if error is not None:
            return ToolResult(tool_name=self.name, success=False, error_message=error, rejected=True)
        if self.mock_server:
            return self.mock_server.get_output(self.name, parameters)
        return self._execute_real(parameters)

    @cached_property
    def _validator(self) -> Draft202012Validator:
        return Draft202012Validator(self.parameter_schema)

    @cached_property
    def _assay_lists(self) -> dict[str, dict[str, str]]:
        """Array-of-enum properties: normalised key → advertised member."""
        lists = {}
        for key, prop in self.parameter_schema["properties"].items():
            members = prop.get("items", {}).get("enum") if prop.get("type") == "array" else None
            if members:
                lists[key] = {normalize_analyte(member): member for member in members}
        return lists

    def validation_error(self, parameters: dict[str, Any]) -> str | None:
        """Why the arguments violate the advertised schema, or None when they are legal."""
        view = dict(parameters) if isinstance(parameters, dict) else parameters
        if isinstance(view, dict):
            for key, members in self._assay_lists.items():
                if isinstance(view.get(key), list):
                    view[key] = [
                        members.get(normalize_analyte(item), item) if isinstance(item, str) else item
                        for item in view[key]
                    ]
        error = next(iter(sorted(self._validator.iter_errors(view), key=lambda e: list(e.absolute_path))), None)
        if error is None:
            return None
        path = "/".join(str(part) for part in error.absolute_path)
        if error.validator == "enum":
            return f"{self.name}: {path}={error.instance!r} is not in the tool's vocabulary"
        if error.validator == "required":
            return f"{self.name}: {error.message}"
        return f"{self.name}: {path + ': ' if path else ''}{error.message}"

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
