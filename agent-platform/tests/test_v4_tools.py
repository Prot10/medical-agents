"""Tests for v4 tool system — new tools, v4 dataset routing, and cost integration."""

import json
from pathlib import Path

import pytest

from neuroagent_schemas import (
    NeuroBenchCase, CTReport, EchoReport, CardiacMonitoringReport,
    AdvancedImagingReport, SpecializedTestReport,
)
from neuroagent.tools.base import ToolCall, ToolResult
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry
from neuroagent.tools.cost_tracker import CostTracker
from neuroagent.agent.reasoning import AgentTrace
from neuroagent.evaluation.metrics import MetricsCalculator, CaseMetrics, check_critical_action

V4_CASES_DIR = Path(__file__).resolve().parents[2] / "data" / "neurobench_v4" / "cases"


def _load_case(case_id: str) -> NeuroBenchCase:
    path = V4_CASES_DIR / f"{case_id}.json"
    return NeuroBenchCase(**json.loads(path.read_text()))


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


class TestNewOutputSchemas:
    """Verify new Pydantic models can be instantiated and serialized."""

    def test_ct_report(self):
        r = CTReport(
            findings=[{"type": "hemorrhage", "location": "left temporal", "size": "2cm", "density": "hyperdense", "description": "acute"}],
            impression="Acute hemorrhage",
            contrast_used=False,
        )
        d = r.model_dump()
        assert d["impression"] == "Acute hemorrhage"
        assert not d["contrast_used"]

    def test_echo_report(self):
        r = EchoReport(
            chambers={"LV": "normal"},
            valves={"mitral": "normal"},
            ejection_fraction=55.0,
            findings=["No abnormalities"],
            impression="Normal study",
        )
        d = r.model_dump()
        assert d["ejection_fraction"] == 55.0

    def test_cardiac_monitoring_report(self):
        r = CardiacMonitoringReport(
            duration_hours=24,
            monitor_type="holter_24h",
            rhythm_summary="Sinus rhythm",
            impression="Normal Holter",
        )
        d = r.model_dump()
        assert d["duration_hours"] == 24

    def test_advanced_imaging_report(self):
        r = AdvancedImagingReport(
            modality="DaTscan",
            findings=[{"region": "striatum", "signal": "reduced", "description": "asymmetric"}],
            impression="Abnormal DaTscan",
        )
        d = r.model_dump()
        assert d["modality"] == "DaTscan"

    def test_specialized_test_report(self):
        r = SpecializedTestReport(
            test_type="neuropsych_battery",
            findings=[{"test": "MMSE", "value": "22/30", "reference_range": "24-30", "abnormal": "yes"}],
            impression="Mild cognitive impairment",
        )
        d = r.model_dump()
        assert d["test_type"] == "neuropsych_battery"


# ---------------------------------------------------------------------------
# Tool definition tests
# ---------------------------------------------------------------------------


class TestToolDefinitions:
    """Verify all 12 tools have correct schemas."""

    @pytest.fixture
    def registry(self) -> ToolRegistry:
        return ToolRegistry.create_default_registry()

    def test_twelve_tools_registered(self, registry):
        assert len(registry.tools) == 12

    def test_all_tool_names(self, registry):
        expected = {
            "analyze_eeg", "analyze_brain_mri", "analyze_ecg",
            "interpret_labs", "analyze_csf",
            "search_medical_literature", "check_drug_interactions",
            "order_ct_scan", "order_echocardiogram",
            "order_cardiac_monitoring", "order_advanced_imaging",
            "order_specialized_test",
        }
        assert set(registry.tools.keys()) == expected

    def test_mri_has_protocol_param(self, registry):
        defn = registry.get_tool("analyze_brain_mri").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "protocol" in params
        assert "sequences" not in params  # removed
        assert "mri_file_path" not in params  # removed
        assert set(params["protocol"]["enum"]) == {"standard", "epilepsy", "stroke", "tumor", "ms", "dementia"}

    def test_mri_has_contrast_param(self, registry):
        defn = registry.get_tool("analyze_brain_mri").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "contrast" in params
        assert params["contrast"]["type"] == "boolean"

    def test_eeg_has_type_param(self, registry):
        defn = registry.get_tool("analyze_eeg").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "eeg_type" in params
        assert "eeg_file_path" not in params  # removed
        assert set(params["eeg_type"]["enum"]) == {"routine", "ambulatory", "video", "continuous_icu"}

    def test_ecg_no_file_path(self, registry):
        defn = registry.get_tool("analyze_ecg").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "ecg_file_path" not in params

    def test_ct_has_angiography_param(self, registry):
        defn = registry.get_tool("order_ct_scan").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "angiography" in params
        assert "contrast" in params

    def test_echo_has_type_param(self, registry):
        defn = registry.get_tool("order_echocardiogram").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "echo_type" in params
        assert set(params["echo_type"]["enum"]) == {"TTE", "TEE", "bubble_study"}

    def test_cardiac_monitoring_has_type_param(self, registry):
        defn = registry.get_tool("order_cardiac_monitoring").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "monitor_type" in params

    def test_advanced_imaging_has_type_param(self, registry):
        defn = registry.get_tool("order_advanced_imaging").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "imaging_type" in params
        assert "DaTscan" in params["imaging_type"]["enum"]

    def test_specialized_test_has_type_param(self, registry):
        defn = registry.get_tool("order_specialized_test").get_tool_definition()
        params = defn["function"]["parameters"]["properties"]
        assert "test_type" in params
        assert "neuropsych_battery" in params["test_type"]["enum"]

    def test_all_tools_require_clinical_context(self, registry):
        """All diagnostic tools (not literature/drug) should require clinical_context."""
        for name, tool in registry.tools.items():
            defn = tool.get_tool_definition()
            required = defn["function"]["parameters"].get("required", [])
            if name in ("search_medical_literature", "check_drug_interactions"):
                continue
            assert "clinical_context" in required, f"{name} missing required clinical_context"


# ---------------------------------------------------------------------------
# V4 dataset & mock server routing tests
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not V4_CASES_DIR.exists(), reason="v4 dataset not generated")
class TestV4MockServerRouting:
    """Test that v4 cases route new tools to proper outputs via MockServer."""

    def test_stroke_ct_routing(self):
        """CT scan should return CTReport from v4 stroke case followup."""
        case = _load_case("ISCH-STR-S01")
        mock = MockServer(case)
        result = mock.get_output("order_ct_scan", {"clinical_context": "stroke", "angiography": True})
        assert result.success
        assert "findings" in result.output
        assert "impression" in result.output

    def test_stroke_echo_routing(self):
        """Echocardiogram should return EchoReport from v4 stroke case followup."""
        case = _load_case("ISCH-STR-S01")
        mock = MockServer(case)
        result = mock.get_output("order_echocardiogram", {"clinical_context": "stroke", "echo_type": "TTE"})
        assert result.success
        assert "impression" in result.output

    def test_stroke_holter_routing(self):
        """Cardiac monitoring should return CardiacMonitoringReport from v4 stroke case."""
        case = _load_case("ISCH-STR-S01")
        mock = MockServer(case)
        result = mock.get_output("order_cardiac_monitoring", {"clinical_context": "afib screening"})
        assert result.success
        assert "impression" in result.output

    def test_alzheimer_neuropsych_routing(self):
        """Specialized test should return SpecializedTestReport for neuropsych."""
        case = _load_case("ALZ-EARLY-M01")
        mock = MockServer(case)
        result = mock.get_output("order_specialized_test", {"clinical_context": "cognitive", "test_type": "neuropsych_battery"})
        assert result.success
        assert "impression" in result.output

    def test_alzheimer_amyloid_pet_routing(self):
        """Advanced imaging should return AdvancedImagingReport for amyloid PET."""
        case = _load_case("ALZ-EARLY-M01")
        mock = MockServer(case)
        result = mock.get_output("order_advanced_imaging", {"clinical_context": "AD confirmation", "imaging_type": "amyloid_PET"})
        assert result.success
        assert "impression" in result.output

    def test_original_tools_still_work(self):
        """Existing tools (EEG, MRI, labs) should still route correctly."""
        case = _load_case("ISCH-STR-S01")
        mock = MockServer(case)

        mri = mock.get_output("analyze_brain_mri", {"clinical_context": "stroke"})
        assert mri.success
        assert "findings" in mri.output

        labs = mock.get_output("interpret_labs", {"clinical_context": "stroke"})
        assert labs.success
        assert "panels" in labs.output

        ecg = mock.get_output("analyze_ecg", {"clinical_context": "cardiac"})
        assert ecg.success

    def test_missing_tool_returns_error(self):
        """Calling a tool with no data should fail gracefully."""
        case = _load_case("ALZ-EARLY-S01")
        mock = MockServer(case)
        result = mock.get_output("order_ct_scan", {"clinical_context": "not needed"})
        assert not result.success
        assert "No order_ct_scan data available" in result.error_message


# ---------------------------------------------------------------------------
# V4 dataset validation
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not V4_CASES_DIR.exists(), reason="v4 dataset not generated")
class TestV4DatasetIntegrity:
    """Validate all 200 v4 cases load correctly."""

    def test_all_cases_load(self):
        cases = sorted(V4_CASES_DIR.glob("*.json"))
        assert len(cases) == 200
        for path in cases:
            data = json.loads(path.read_text())
            case = NeuroBenchCase(**data)
            assert case.case_id
            assert case.ground_truth.primary_diagnosis

    def test_no_misrouted_echo(self):
        """No echocardiogram followups should still be routed to interpret_labs."""
        for path in sorted(V4_CASES_DIR.glob("*.json")):
            data = json.loads(path.read_text())
            for fu in data.get("followup_outputs", []):
                if "echocardiogram" in fu["trigger_action"]:
                    assert fu["tool_name"] == "order_echocardiogram", (
                        f'{data["case_id"]}: echocardiogram still routed to {fu["tool_name"]}'
                    )

    def test_no_misrouted_holter(self):
        """No Holter followups should still be routed to analyze_ecg."""
        for path in sorted(V4_CASES_DIR.glob("*.json")):
            data = json.loads(path.read_text())
            for fu in data.get("followup_outputs", []):
                if "holter" in fu["trigger_action"]:
                    assert fu["tool_name"] == "order_cardiac_monitoring", (
                        f'{data["case_id"]}: holter still routed to {fu["tool_name"]}'
                    )

    def test_no_misrouted_ct(self):
        """No CT followups should still be routed to analyze_brain_mri."""
        for path in sorted(V4_CASES_DIR.glob("*.json")):
            data = json.loads(path.read_text())
            for fu in data.get("followup_outputs", []):
                trigger = fu["trigger_action"]
                if trigger in ("request_ct_angiography", "request_ct_head", "request_brain_ct"):
                    assert fu["tool_name"] == "order_ct_scan", (
                        f'{data["case_id"]}: {trigger} still routed to {fu["tool_name"]}'
                    )

    def test_no_misrouted_pet(self):
        """No PET/DaTscan followups should still be routed to analyze_brain_mri."""
        pet_triggers = {"request_amyloid_pet", "request_fdg_pet", "request_datscan", "request_pet_scan"}
        for path in sorted(V4_CASES_DIR.glob("*.json")):
            data = json.loads(path.read_text())
            for fu in data.get("followup_outputs", []):
                if fu["trigger_action"] in pet_triggers:
                    assert fu["tool_name"] == "order_advanced_imaging", (
                        f'{data["case_id"]}: {fu["trigger_action"]} still routed to {fu["tool_name"]}'
                    )


# ---------------------------------------------------------------------------
# Metrics with new tools
# ---------------------------------------------------------------------------


class TestMetricsWithNewTools:
    """Test that evaluation metrics work with 12-tool set."""

    def test_critical_action_matches_ct(self):
        assert check_critical_action("Order CT scan to rule out hemorrhage", ["order_ct_scan"], "")
        assert not check_critical_action("Order CT scan to rule out hemorrhage", ["analyze_brain_mri"], "")

    def test_critical_action_matches_echo(self):
        assert check_critical_action("Order transthoracic echocardiogram", ["order_echocardiogram"], "")
        assert not check_critical_action("Order transthoracic echocardiogram", ["interpret_labs"], "")

    def test_critical_action_matches_holter(self):
        assert check_critical_action("Order Holter monitor for arrhythmia", ["order_cardiac_monitoring"], "")

    def test_critical_action_matches_pet(self):
        assert check_critical_action("Order amyloid PET for AD confirmation", ["order_advanced_imaging"], "")
        assert check_critical_action("Order DaTscan for parkinsonian evaluation", ["order_advanced_imaging"], "")

    def test_critical_action_matches_neuropsych(self):
        assert check_critical_action("Perform neuropsychological testing", ["order_specialized_test"], "")

    def test_critical_action_matches_emg(self):
        assert check_critical_action("Order EMG/nerve conduction studies", ["order_specialized_test"], "")

    def test_cost_metrics_populated(self):
        """Verify cost fields are computed in CaseMetrics."""
        trace = AgentTrace(case_id="test")
        trace.tools_called = ["analyze_brain_mri", "interpret_labs"]
        trace.total_tool_calls = 2
        trace.total_cost_usd = 345.0  # MRI(320) + labs(25)
        trace.final_response = "### Primary Diagnosis\nTest"

        fixture_path = Path(__file__).parent / "fixtures" / "sample_case.json"
        case = NeuroBenchCase(**json.loads(fixture_path.read_text()))

        calc = MetricsCalculator()
        metrics = calc.compute_all(trace, case.ground_truth)
        assert metrics.total_cost_usd == 345.0
        assert metrics.optimal_cost_usd > 0  # Should be computed from ground truth


# ---------------------------------------------------------------------------
# ToolResult cost field
# ---------------------------------------------------------------------------


class TestToolResultCost:
    def test_cost_field_exists(self):
        tr = ToolResult(tool_name="analyze_ecg", success=True, output={}, cost_usd=20.0)
        assert tr.cost_usd == 20.0

    def test_cost_field_optional(self):
        tr = ToolResult(tool_name="analyze_ecg", success=True, output={})
        assert tr.cost_usd is None


# ---------------------------------------------------------------------------
# AgentTrace cost fields
# ---------------------------------------------------------------------------


class TestAgentTraceCost:
    def test_trace_has_cost_fields(self):
        trace = AgentTrace()
        assert trace.total_cost_usd == 0.0
        assert trace.cost_entries == []

    def test_trace_cost_serialization(self):
        trace = AgentTrace(
            total_cost_usd=1315.0,
            cost_entries=[{"tool_name": "analyze_ecg", "cost_usd": 20.0}],
        )
        d = trace.model_dump()
        assert d["total_cost_usd"] == 1315.0
        assert len(d["cost_entries"]) == 1
