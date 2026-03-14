"""Tests for the hospital rules engine."""

import pytest

from neuroagent.rules.rules_engine import RulesEngine, ComplianceResult
from neuroagent.rules.pathway_checker import PathwayChecker


@pytest.fixture
def rules_engine():
    return RulesEngine("agent-platform/config/hospital_rules")


def test_load_pathways(rules_engine):
    assert len(rules_engine.pathways) == 5


def test_get_context(rules_engine):
    context = rules_engine.get_context()
    assert "First Unprovoked Seizure" in context
    assert "Acute Stroke Code" in context
    assert "MANDATORY" in context


def test_get_pathway_first_seizure(rules_engine):
    pathway = rules_engine.get_pathway("first_seizure")
    assert pathway is not None
    assert pathway.name == "First Unprovoked Seizure Workup"


def test_get_pathway_stroke(rules_engine):
    pathway = rules_engine.get_pathway("stroke_code")
    assert pathway is not None
    assert "interpret_labs" in pathway.get_required_actions()


def test_get_pathway_not_found(rules_engine):
    pathway = rules_engine.get_pathway("nonexistent_rare_condition_xyz")
    assert pathway is None


def test_compliance_full(rules_engine):
    pathway = rules_engine.get_pathway("first_seizure")
    result = rules_engine.check_compliance(
        tools_called=["interpret_labs", "analyze_eeg", "analyze_brain_mri", "check_drug_interactions"],
        pathway=pathway,
    )
    assert result.compliant
    assert len(result.missing_required) == 0


def test_compliance_missing(rules_engine):
    pathway = rules_engine.get_pathway("first_seizure")
    result = rules_engine.check_compliance(
        tools_called=["interpret_labs"],
        pathway=pathway,
    )
    assert not result.compliant
    assert "analyze_eeg" in result.missing_required
    assert "analyze_brain_mri" in result.missing_required


def test_pathway_checker(rules_engine):
    checker = PathwayChecker(rules_engine)
    result = checker.check_case(
        tools_called=["interpret_labs", "analyze_eeg", "analyze_brain_mri", "check_drug_interactions"],
        condition="first_seizure",
    )
    assert result is not None
    assert result.compliant
