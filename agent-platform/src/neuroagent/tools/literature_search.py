from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class LiteratureSearchTool(BaseTool):
    name = "search_medical_literature"
    description = (
        "Search medical literature and clinical guidelines for evidence "
        "relevant to a clinical question. Returns relevant publications, "
        "guideline recommendations, and evidence levels."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Clinical question or search query.",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return.",
                "default": 5,
            },
        },
        "required": ["query"],
    }

    def __init__(self, mock_server: MockServer | None = None):
        self.mock_server = mock_server

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        if self.mock_server:
            return self.mock_server.get_output(self.name, parameters)
        raise NotImplementedError(f"Real {self.name} model not yet connected")
