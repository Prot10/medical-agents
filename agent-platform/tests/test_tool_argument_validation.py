"""The advertised tool schema is the contract: a call outside it is answered with an error, not a substitute result."""

from __future__ import annotations

from pathlib import Path

from neuroagent.datasets import load_dataset
from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent.tools.cost_tracker import CostConfigError, CostTracker
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry
from neuroagent_schemas import ToolAction

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def case():
    _, cases = load_dataset(ROOT / "data" / "neurobench")
    return cases["NMDAR-ENC-M01"]


@pytest.fixture
def environment(case):
    return NeuroBenchEnvironment(case)


def _run(environment, tool, **arguments):
    return environment.execute(ToolAction(tool_name=tool, arguments=arguments))


def test_out_of_vocabulary_enum_is_rejected_and_not_billed(environment):
    result = _run(environment, "order_body_imaging", clinical_context="carotid disease", study="carotid_duplex")
    assert not result.success and result.output is None and not result.from_fallback
    assert result.error_message == "order_body_imaging: study='carotid_duplex' is not in the tool's vocabulary"
    assert result.cost_usd == 0.0


def test_missing_required_argument_is_rejected(environment):
    result = _run(environment, "order_advanced_imaging", clinical_context="vessel imaging")
    assert not result.success
    assert result.error_message == "order_advanced_imaging: 'modality' is a required property"


def test_assay_spelling_that_prices_and_scores_as_a_member_is_legal(environment):
    result = _run(environment, "analyze_csf", clinical_context="encephalitis", special_tests=["Oligoclonal bands", "NMDAR antibodies"])
    assert result.success, result.error_message
    assert result.cost_usd and result.cost_usd > 0
    rejected = _run(environment, "analyze_csf", clinical_context="encephalitis", special_tests=["albumin"])
    assert rejected.error_message == "analyze_csf: special_tests/0='albumin' is not in the tool's vocabulary"


def test_genetic_panels_are_enum_members(environment):
    registry = ToolRegistry.create_default_registry(MockServer(environment.case))
    enum = registry.get_tool("order_specialized_test").parameter_schema["properties"]["test_type"]["enum"]
    panels = [value for value in enum if value.startswith("genetic_panel:")]
    assert panels and len(set(enum)) == len(enum)
    result = _run(environment, "order_specialized_test", clinical_context="hereditary", test_type=panels[0])
    assert result.success, result.error_message
    assert _run(environment, "order_specialized_test", clinical_context="x", test_type="genetic_panel:unknown").success is False


def test_cost_registry_has_no_fallback_rates():
    tracker = CostTracker()
    with pytest.raises(CostConfigError):
        tracker.compute_cost("order_body_imaging", {"study": "carotid_duplex"})
    with pytest.raises(CostConfigError):
        tracker.compute_cost("analyze_csf", {"special_tests": ["albumin"]})
