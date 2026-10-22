"""The harness opened to general medicine and to recorded cases, with NeuroBench left as it was.

Three changes, each opt-in through the case: `domain: general_medicine` adds the costs.yaml
`general_medicine` vocabulary pack to the catalogue, `provenance: record` answers an order the
clinicians never placed with "not available" instead of a library normal report, and the prompt
renders a general examination and missing vitals. A NeuroBench case sets neither field, and these
tests pin that its catalogue does not move.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from neuroagent.harness.context import format_patient_info
from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent.tools.cost_tracker import CostTracker
from neuroagent.tools.tool_registry import ToolRegistry
from neuroagent.tools.vocabulary import DEFAULT_COSTS_PATH, all_packs, merge_packs
from neuroagent_schemas import NeuroBenchCase, ToolAction
from pydantic import ValidationError

FIXTURE = Path(__file__).parent / "fixtures" / "sample_case.json"
GENERAL = ("general_medicine",)


def _case(**overrides) -> NeuroBenchCase:
    data = json.loads(FIXTURE.read_text())
    data.update(overrides)
    return NeuroBenchCase.model_validate(data)


def _enums(registry: ToolRegistry) -> dict[tuple[str, str], set[str]]:
    out = {}
    for name, tool in registry.tools.items():
        for key, prop in tool.parameter_schema["properties"].items():
            members = prop.get("items", {}).get("enum") if prop.get("type") == "array" else prop.get("enum")
            if members:
                out[(name, key)] = set(members)
    return out


def _pack_terms() -> dict[str, dict[str, list[str]]]:
    config = yaml.safe_load(DEFAULT_COSTS_PATH.read_text())
    return {
        tool: {block: list(rows) for block, rows in blocks.items()}
        for tool, blocks in config["packs"]["general_medicine"]["tools"].items()
    }


def test_a_neurology_case_sees_the_neurobench_catalogue():
    environment = NeuroBenchEnvironment(_case())
    assert environment.tool_definitions() == ToolRegistry.create_default_registry().get_all_definitions()
    advertised = set().union(*_enums(environment.registry).values())
    for blocks in _pack_terms().values():
        for terms in blocks.values():
            assert not advertised & set(terms)


def test_a_general_medicine_case_advertises_and_accepts_the_pack():
    environment = NeuroBenchEnvironment(_case(domain="general_medicine"))
    neuro, general = _enums(ToolRegistry.create_default_registry()), _enums(environment.registry)
    assert set(neuro) == set(general)
    for key, members in neuro.items():
        assert members <= general[key]  # the pack only adds
    assert "chest_xray" in general[("order_body_imaging", "study")]
    assert "sputum" in general[("order_microbiology", "specimen")]
    assert "upper_endoscopy" in general[("order_specialized_test", "test_type")]
    assert "lipase" in general[("interpret_labs", "panels")]
    tool = environment.registry.get_tool("order_body_imaging")
    assert tool.validation_error({"clinical_context": "cough", "study": "chest_xray"}) is None
    assert "chest_xray" in tool.parameter_schema["properties"]["study"]["description"]
    neuro_tool = ToolRegistry.create_default_registry().get_tool("order_body_imaging")
    assert "not in the tool's vocabulary" in neuro_tool.validation_error(
        {"clinical_context": "cough", "study": "chest_xray"}
    )


def test_every_pack_term_is_priced():
    tracker = CostTracker()
    probes = {
        "order_body_imaging": "study",
        "order_microbiology": "specimen",
        "order_specialized_test": "test_type",
        "obtain_tissue_diagnosis": "procedure",
        "order_advanced_imaging": "modality",
    }
    for tool, blocks in _pack_terms().items():
        for term in blocks.get("by_type", []):
            assert tracker.compute_cost(tool, {probes[tool]: term}).cost_usd > 0, (tool, term)
        for term in blocks.get("by_panel", []):
            assert tracker.compute_cost(tool, {"panels": [term]}).cost_usd > 0, (tool, term)


def test_a_pack_may_not_reprice_an_existing_term():
    config = {
        "tools": {"interpret_labs": {"by_panel": {"beta-hCG": 14}}},
        "packs": {"p": {"tools": {"interpret_labs": {"by_panel": {"beta_hCG": 18}}}}},
    }
    with pytest.raises(ValueError, match="re-prices"):
        merge_packs(config, ("p",))
    with pytest.raises(KeyError):
        merge_packs(config, ("missing",))
    assert all_packs() == GENERAL


def test_a_recorded_case_answers_an_unplaced_order_not_available_and_bills_it():
    environment = NeuroBenchEnvironment(_case(domain="general_medicine", provenance="record"))
    result = environment.execute(
        ToolAction(tool_name="order_body_imaging", arguments={"clinical_context": "cough", "study": "chest_xray"})
    )
    assert not result.success and result.unavailable and not result.from_fallback
    assert result.output is None
    assert "Not available" in result.error_message and "study=chest_xray" in result.error_message
    assert result.cost_usd > 0  # the order was placed


def test_a_recorded_case_still_serves_what_was_recorded_and_the_knowledge_tools():
    environment = NeuroBenchEnvironment(_case(provenance="record"))
    labs = environment.execute(ToolAction(tool_name="interpret_labs", arguments={"clinical_context": "seizure"}))
    assert labs.success and not labs.unavailable
    search = environment.execute(
        ToolAction(tool_name="search_medical_literature", arguments={"query": "anything"})
    )
    assert search.success and not search.unavailable


def test_a_synthetic_case_keeps_the_library_normal_report():
    environment = NeuroBenchEnvironment(_case())
    result = environment.execute(
        ToolAction(tool_name="order_body_imaging", arguments={"clinical_context": "x", "study": "chest_CT"})
    )
    assert result.success and result.library and not result.unavailable


def test_a_recorded_case_cannot_carry_authored_fallback_reports():
    data = json.loads(FIXTURE.read_text())
    data.update(provenance="record", fallback_tool_outputs={})
    with pytest.raises(ValidationError, match="not available"):
        NeuroBenchCase.model_validate(data)


def test_the_prompt_renders_a_general_examination_and_missing_vitals():
    data = json.loads(FIXTURE.read_text())
    data["domain"] = "general_medicine"
    data["patient"].pop("neurological_exam")
    data["patient"]["physical_exam"] = {"chest": "crackles at the right base", "abdomen": "soft"}
    data["patient"]["vitals"] = {"bp_systolic": 98, "bp_diastolic": 60, "temp": 38.9, "spo2": 91}
    text = format_patient_info(NeuroBenchCase.model_validate(data))
    assert "Neurological examination" not in text
    assert "Physical examination:\n  chest: crackles at the right base\n  abdomen: soft" in text
    assert text.endswith("Vitals: BP 98/60 mmHg, Temp 38.9°C, SpO2 91% (not recorded: HR, RR)")


class _Scripted:
    adapter_id = "scripted"
    model_id = "scripted/model"

    def __init__(self, turns):
        self.turns = iter(turns)

    def next_action(self, **kwargs):
        return next(self.turns)


def test_the_unavailable_flag_reaches_the_episode():
    from neuroagent.harness import ClinicalPolicyLoop, ModelTurn, RunContext
    from neuroagent_schemas import ObservationReceived, SubmitAssessment

    loop = ClinicalPolicyLoop()
    model = _Scripted([
        ModelTurn(action=ToolAction(
            tool_name="order_microbiology", arguments={"clinical_context": "cough", "specimen": "sputum"},
        )),
        ModelTurn(action=SubmitAssessment(
            primary_diagnosis="pneumonia", confidence=0.6, urgency="urgent", recommendations=["treat"],
        )),
    ])
    episode = loop.run(RunContext(
        profile_id="test", model=model, loop=loop, max_turns=3, max_invalid_actions=0,
        environment=NeuroBenchEnvironment(_case(domain="general_medicine", provenance="record")),
    ))
    observation = next(event for event in episode.events if isinstance(event, ObservationReceived))
    assert observation.unavailable and not observation.success and observation.cost_usd > 0
