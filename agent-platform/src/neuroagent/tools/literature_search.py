from __future__ import annotations
from .base import BaseTool


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
