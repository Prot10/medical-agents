"""Tests for the mock server — ensures proper output matching and follow-ups."""

import json
from pathlib import Path

import pytest

from neuroagent_schemas import NeuroBenchCase
from neuroagent.tools.mock_server import MockServer


@pytest.fixture
def sample_case() -> NeuroBenchCase:
    fixture_path = Path(__file__).parent / "fixtures" / "sample_case.json"
    data = json.loads(fixture_path.read_text())
    return NeuroBenchCase.model_validate(data)


@pytest.fixture
def mock_server(sample_case: NeuroBenchCase) -> MockServer:
    return MockServer(sample_case)


def test_initial_eeg(mock_server):
    result = mock_server.get_output("analyze_eeg", {})
    assert result.success
    assert result.output["classification"] == "abnormal"
    assert len(result.output["findings"]) == 2


def test_initial_mri(mock_server):
    result = mock_server.get_output("analyze_brain_mri", {})
    assert result.success
    assert result.output["findings"][0]["location"] == "Right mesial temporal lobe, centered in the amygdala/anterior hippocampus"


def test_followup_eeg(mock_server):
    """Test that follow-up outputs are served when initial is already consumed."""
    # First call gets initial EEG
    result1 = mock_server.get_output("analyze_eeg", {"clinical_context": "initial"})
    assert result1.success

    # Follow-up EEG should also be available
    result2 = mock_server.get_output("analyze_eeg", {"clinical_context": "video EEG"})
    # The mock server returns initial output on first match, then follow-up
    assert result2.success


def test_ecg_not_available(mock_server):
    result = mock_server.get_output("analyze_ecg", {})
    assert not result.success


class TestFollowUpOutputResolution:
    """Regression: FollowUpToolOutput.output must resolve by tool_name, never
    silently mis-resolve via the overlapping union (which lost content at runtime)."""

    def test_ambiguous_shape_resolves_by_tool_name(self):
        from neuroagent_schemas.case import FollowUpToolOutput
        from neuroagent_schemas.tool_outputs import (
            SpecializedTestReport, AdvancedImagingReport,
        )
        # {findings, impression, recommended_actions} validates as BOTH
        # SpecializedTestReport and AdvancedImagingReport; tool_name must decide.
        shape = {"findings": [{"test": "EMG", "result": "denervation"}],
                 "impression": "widespread denervation", "recommended_actions": []}
        spec = FollowUpToolOutput(trigger_action="x", tool_name="order_specialized_test", output=dict(shape))
        assert isinstance(spec.output, SpecializedTestReport)
        adv = FollowUpToolOutput(trigger_action="x", tool_name="order_advanced_imaging", output=dict(shape))
        assert isinstance(adv.output, AdvancedImagingReport)

    def test_literature_resolves_not_cardiac(self):
        from neuroagent_schemas.case import FollowUpToolOutput
        from neuroagent_schemas.tool_outputs import LiteratureSearchResult
        fu = FollowUpToolOutput(
            trigger_action="x", tool_name="search_medical_literature",
            output={"query": "q", "results": [], "summary": "general evidence"},
        )
        assert isinstance(fu.output, LiteratureSearchResult)
        assert fu.output.summary == "general evidence"

    def test_drug_interaction_has_summary_field(self):
        from neuroagent_schemas.tool_outputs import DrugInteractionResult
        d = DrugInteractionResult(summary="free-text review")
        assert d.summary == "free-text review"

    def test_malformed_output_raises_not_silently_dropped(self):
        from neuroagent_schemas.case import FollowUpToolOutput
        # An output that cannot be a LiteratureSearchResult must error loudly,
        # not resolve to an empty wrong-typed object.
        with pytest.raises(Exception):
            FollowUpToolOutput(
                trigger_action="x", tool_name="search_medical_literature",
                output={"results": "not-a-list-and-no-summary", "query": [1, 2]},
            )


def test_call_log_tracks_all(mock_server):
    mock_server.get_output("analyze_eeg", {"a": 1})
    mock_server.get_output("interpret_labs", {"b": 2})
    mock_server.get_output("analyze_csf", {"c": 3})

    log = mock_server.get_call_log()
    assert len(log) == 3
    assert [c.tool_name for c in log] == ["analyze_eeg", "interpret_labs", "analyze_csf"]
