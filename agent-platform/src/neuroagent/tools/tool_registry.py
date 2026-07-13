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
        if tool_call.tool_name not in self.tools:
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                output=None,
                error_message=f"Tool '{tool_call.tool_name}' not found. Available: {list(self.tools.keys())}",
            )
        tool = self.get_tool(tool_call.tool_name)
        return tool.execute(tool_call.parameters)

    @staticmethod
    def create_default_registry(
        mock_server=None,
    ) -> "ToolRegistry":
        """Create a registry with all diagnostic tools.

        Args:
            mock_server: MockServer for evaluation mode (pre-generated outputs).

        Returns:
            ToolRegistry with the 12 diagnostic tools.
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

        return registry
