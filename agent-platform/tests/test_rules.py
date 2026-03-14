"""Tests for the hospital rules engine."""

import pytest

from neuroagent.rules.rules_engine import (
    AVAILABLE_HOSPITALS,
    RulesEngine,
    ComplianceResult,
)
from neuroagent.rules.pathway_checker import PathwayChecker


RULES_DIR = "agent-platform/config/hospital_rules"


@pytest.fixture(params=list(AVAILABLE_HOSPITALS.keys()))
def rules_engine(request):
    """Parametrized fixture that runs tests against every hospital rule set."""
    return RulesEngine(RULES_DIR, hospital=request.param)


@pytest.fixture
def us_rules():
    return RulesEngine(RULES_DIR, hospital="us_mayo")


def test_all_hospitals_exist():
    """Every declared hospital should have a loadable rule set."""
    for hospital_id in AVAILABLE_HOSPITALS:
        engine = RulesEngine(RULES_DIR, hospital=hospital_id)
        assert len(engine.pathways) == 5, f"{hospital_id} should have 5 pathways"


def test_load_pathways(rules_engine):
    assert len(rules_engine.pathways) == 5


def test_get_context_includes_hospital_name(rules_engine):
    context = rules_engine.get_context()
    assert "protocols" in context.lower()
    assert "MANDATORY" in context


def test_get_context_us(us_rules):
    context = us_rules.get_context()
    assert "Mayo Clinic" in context
    assert "AAN" in context or "First Unprovoked Seizure" in context


def test_get_pathway_first_seizure(us_rules):
    pathway = us_rules.get_pathway("first_seizure")
    assert pathway is not None
    assert "seizure" in pathway.name.lower() or "Seizure" in pathway.name


def test_get_pathway_stroke(us_rules):
    pathway = us_rules.get_pathway("stroke_code")
    assert pathway is not None
    assert "interpret_labs" in pathway.get_required_actions()


def test_get_pathway_not_found(us_rules):
    pathway = us_rules.get_pathway("nonexistent_rare_condition_xyz")
    assert pathway is None


def test_compliance_full(us_rules):
    pathway = us_rules.get_pathway("first_seizure")
    result = us_rules.check_compliance(
        tools_called=["interpret_labs", "analyze_eeg", "analyze_brain_mri", "check_drug_interactions"],
        pathway=pathway,
    )
    assert result.compliant
    assert len(result.missing_required) == 0


def test_compliance_missing(us_rules):
    pathway = us_rules.get_pathway("first_seizure")
    result = us_rules.check_compliance(
        tools_called=["interpret_labs"],
        pathway=pathway,
    )
    assert not result.compliant
    assert "analyze_eeg" in result.missing_required
    assert "analyze_brain_mri" in result.missing_required


def test_pathway_checker(us_rules):
    checker = PathwayChecker(us_rules)
    result = checker.check_case(
        tools_called=["interpret_labs", "analyze_eeg", "analyze_brain_mri", "check_drug_interactions"],
        condition="first_seizure",
    )
    assert result is not None
    assert result.compliant


def test_no_check_hospital_rules_in_steps():
    """Hospital rules should not reference themselves as a tool step."""
    for hospital_id in AVAILABLE_HOSPITALS:
        engine = RulesEngine(RULES_DIR, hospital=hospital_id)
        for pathway in engine.pathways:
            for step in pathway.steps:
                assert step.action != "check_hospital_rules", (
                    f"{hospital_id}/{pathway.name} still references check_hospital_rules as a step"
                )


def test_hospitals_have_distinct_context():
    """Different hospitals should produce different system prompt context."""
    contexts = {}
    for hospital_id in AVAILABLE_HOSPITALS:
        engine = RulesEngine(RULES_DIR, hospital=hospital_id)
        contexts[hospital_id] = engine.get_context()

    # Each hospital's context should be unique
    context_values = list(contexts.values())
    assert len(set(context_values)) == len(context_values), "Hospital contexts should be distinct"
