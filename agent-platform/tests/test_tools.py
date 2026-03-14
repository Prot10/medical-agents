"""Tests for the tool system."""

import json
from pathlib import Path

import pytest

from neuroagent_schemas import NeuroBenchCase
from neuroagent.tools.base import ToolCall, ToolResult, BaseTool
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry


@pytest.fixture
def sample_case() -> NeuroBenchCase:
    fixture_path = Path(__file__).parent / "fixtures" / "sample_case.json"
    data = json.loads(fixture_path.read_text())
    return NeuroBenchCase.model_validate(data)


@pytest.fixture
def mock_server(sample_case: NeuroBenchCase) -> MockServer:
    return MockServer(sample_case)


@pytest.fixture
def registry(mock_server: MockServer) -> ToolRegistry:
    return ToolRegistry.create_default_registry(mock_server=mock_server)


class TestToolCall:
    def test_create(self):
        tc = ToolCall(tool_name="analyze_eeg", parameters={"clinical_context": "seizure"})
        assert tc.tool_name == "analyze_eeg"
        assert tc.parameters == {"clinical_context": "seizure"}

    def test_empty_params(self):
        tc = ToolCall(tool_name="analyze_eeg")
        assert tc.parameters == {}


class TestToolResult:
    def test_success(self):
        tr = ToolResult(tool_name="analyze_eeg", success=True, output={"classification": "abnormal"})
        assert tr.success
        assert tr.output["classification"] == "abnormal"

    def test_failure(self):
        tr = ToolResult(tool_name="analyze_eeg", success=False, error_message="No data")
        assert not tr.success
        assert tr.error_message == "No data"


class TestMockServer:
    def test_eeg_output(self, mock_server: MockServer):
        result = mock_server.get_output("analyze_eeg", {"clinical_context": "seizure"})
        assert result.success
        assert result.output is not None
        assert result.output["classification"] == "abnormal"

    def test_mri_output(self, mock_server: MockServer):
        result = mock_server.get_output("analyze_brain_mri", {"clinical_context": "seizure"})
        assert result.success
        assert len(result.output["findings"]) == 1

    def test_labs_output(self, mock_server: MockServer):
        result = mock_server.get_output("interpret_labs", {"clinical_context": "seizure"})
        assert result.success
        assert "panels" in result.output

    def test_missing_tool(self, mock_server: MockServer):
        result = mock_server.get_output("analyze_csf", {"clinical_context": "seizure"})
        assert not result.success
        assert "No analyze_csf data available" in result.error_message

    def test_literature_search(self, mock_server: MockServer):
        result = mock_server.get_output("search_medical_literature", {"query": "DNET"})
        assert result.success

    def test_drug_interaction(self, mock_server: MockServer):
        result = mock_server.get_output("check_drug_interactions", {"drug": "levetiracetam"})
        assert result.success
        assert result.output["proposed"] == "levetiracetam"

    def test_call_log(self, mock_server: MockServer):
        mock_server.get_output("analyze_eeg", {})
        mock_server.get_output("interpret_labs", {})
        log = mock_server.get_call_log()
        assert len(log) == 2
        assert log[0].tool_name == "analyze_eeg"
        assert log[1].tool_name == "interpret_labs"


class TestToolRegistry:
    def test_default_registry(self, registry: ToolRegistry):
        assert len(registry.tools) == 7

    def test_get_tool(self, registry: ToolRegistry):
        tool = registry.get_tool("analyze_eeg")
        assert tool.name == "analyze_eeg"

    def test_get_missing_tool(self, registry: ToolRegistry):
        with pytest.raises(KeyError):
            registry.get_tool("nonexistent")

    def test_execute(self, registry: ToolRegistry):
        tc = ToolCall(tool_name="analyze_eeg", parameters={"clinical_context": "seizure"})
        result = registry.execute(tc)
        assert result.success

    def test_get_all_definitions(self, registry: ToolRegistry):
        defs = registry.get_all_definitions()
        assert len(defs) == 7
        for d in defs:
            assert d["type"] == "function"
            assert "name" in d["function"]
            assert "description" in d["function"]
            assert "parameters" in d["function"]
