"""NeuroBench's deterministic clinical environment."""

from __future__ import annotations

from typing import Any

from neuroagent_schemas import NeuroBenchCase, ToolAction

from ..tools.base import ToolCall, ToolResult
from ..tools.cost_tracker import CostTracker
from ..tools.mock_server import MockServer
from ..tools.tool_registry import ToolRegistry


_INITIAL_OUTPUT_TO_TOOL = {
    "eeg": "analyze_eeg",
    "mri": "analyze_brain_mri",
    "ecg": "analyze_ecg",
    "labs": "interpret_labs",
    "csf": "analyze_csf",
    "ct": "order_ct_scan",
    "echo": "order_echocardiogram",
    "cardiac_monitoring": "order_cardiac_monitoring",
    "advanced_imaging": "order_advanced_imaging",
    "specialized_test": "order_specialized_test",
    "body_imaging": "order_body_imaging",
    "microbiology": "order_microbiology",
    "tissue_diagnosis": "obtain_tissue_diagnosis",
    "clinical_assessment": "perform_clinical_assessment",
}


class NeuroBenchEnvironment:
    environment_id = "neurobench-v2"

    def __init__(
        self,
        case: NeuroBenchCase,
        *,
        registry: ToolRegistry | None = None,
        cost_tracker: CostTracker | None = None,
    ) -> None:
        self.case = case
        self.mock_server = MockServer(case)
        self.registry = registry or ToolRegistry.create_default_registry(mock_server=self.mock_server)
        self.cost_tracker = cost_tracker or CostTracker()

    def tool_definitions(self) -> list[dict[str, Any]]:
        return self.registry.get_all_definitions()

    def execute(self, action: ToolAction) -> ToolResult:
        result = self.registry.execute(
            ToolCall(tool_name=action.tool_name, parameters=action.arguments)
        )
        cost = self.cost_tracker.compute_cost(action.tool_name, action.arguments)
        return result.model_copy(update={"cost_usd": cost.cost_usd})

    def direct_observations(self) -> list[ToolResult]:
        """All pre-generated initial results for the non-agentic direct-answer baseline."""
        observations: list[ToolResult] = []
        raw = self.case.initial_tool_outputs.model_dump(exclude_none=True)
        for field, output in raw.items():
            if field in _INITIAL_OUTPUT_TO_TOOL:
                observations.append(
                    ToolResult(
                        tool_name=_INITIAL_OUTPUT_TO_TOOL[field],
                        success=True,
                        output=output,
                        cost_usd=0.0,
                    )
                )
        for query, output in (raw.get("literature_search") or {}).items():
            observations.append(
                ToolResult(
                    tool_name="search_medical_literature",
                    success=True,
                    output={"query": query, "result": output},
                    cost_usd=0.0,
                )
            )
        for query, output in (raw.get("drug_interactions") or {}).items():
            observations.append(
                ToolResult(
                    tool_name="check_drug_interactions",
                    success=True,
                    output={"query": query, "result": output},
                    cost_usd=0.0,
                )
            )
        return observations
