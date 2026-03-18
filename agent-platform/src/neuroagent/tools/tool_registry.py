from __future__ import annotations
from .base import BaseTool, ToolCall, ToolResult
from typing import Any


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseTool:
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' not registered. Available: {list(self.tools.keys())}")
        return self.tools[name]

    def get_all_definitions(self) -> list[dict[str, Any]]:
        return [t.get_tool_definition() for t in self.tools.values()]

    def execute(self, tool_call: ToolCall) -> ToolResult:
        tool = self.get_tool(tool_call.tool_name)
        return tool.execute(tool_call.parameters)

    @staticmethod
    def create_default_registry(
        mock_server=None,
        specialist_client=None,
    ) -> "ToolRegistry":
        """Create a registry with all diagnostic tools.

        Args:
            mock_server: MockServer for evaluation mode (pre-generated outputs).
            specialist_client: LLMClient for the specialist model (dual-model mode).
                If provided, the ``consult_medical_specialist`` tool is registered
                as the 13th tool.  If only mock_server is set, the specialist tool
                delegates to mock_server like every other tool.

        Returns:
            ToolRegistry with 12 tools (single-model) or 13 tools (dual-model).
        """
        from .eeg_analyzer import EEGAnalyzerTool
        from .mri_analyzer import MRIAnalyzerTool
        from .ecg_analyzer import ECGAnalyzerTool
        from .lab_interpreter import LabInterpreterTool
        from .csf_analyzer import CSFAnalyzerTool
        from .literature_search import LiteratureSearchTool
        from .drug_interaction import DrugInteractionTool
        from .ct_scanner import CTScanTool
        from .echocardiogram import EchocardiogramTool
        from .cardiac_monitoring import CardiacMonitoringTool
        from .advanced_imaging import AdvancedImagingTool
        from .specialized_test import SpecializedTestTool

        registry = ToolRegistry()
        for tool_cls in [
            EEGAnalyzerTool, MRIAnalyzerTool, ECGAnalyzerTool,
            LabInterpreterTool, CSFAnalyzerTool, LiteratureSearchTool,
            DrugInteractionTool, CTScanTool, EchocardiogramTool,
            CardiacMonitoringTool, AdvancedImagingTool, SpecializedTestTool,
        ]:
            registry.register(tool_cls(mock_server=mock_server))

        # Specialist consultation tool — only when dual-model or mock evaluation
        if specialist_client is not None or mock_server is not None:
            from .medical_specialist import MedicalSpecialistTool
            registry.register(MedicalSpecialistTool(
                mock_server=mock_server,
                specialist_client=specialist_client,
            ))

        return registry
