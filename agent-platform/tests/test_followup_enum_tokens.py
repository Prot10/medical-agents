"""Which stored report answers an order: the October 2026 review's MockServer fixes.

1. Candidates are filtered by whether they describe the study ordered BEFORE the matcher
   chooses (SE-M05: a pelvic ultrasound order tied between the MRI and ultrasound follow-ups,
   took the MRI, had it refused on modality and fell to the library normal).
2. The called tool's own enum terms route as whole terms (SE CENTRAL 4:
   `request_continuous_eeg_monitoring` capturing the index `continuous_icu` order).
3. `order_cardiac_monitoring` routes by `monitor_type` and recording length (VASC-DEM M04, P08,
   P09, S07, S09; MIG-AURA-P07).
4. A case fallback that names its study with a vocabulary term answers only that study
   (GLIO-HG; NMDAR-ENC CENTRAL 4).
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from neuroagent.tools.cardiac_monitoring import CardiacMonitoringTool
from neuroagent.tools.csf_analyzer import CSFAnalyzerTool
from neuroagent.tools.echocardiogram import EchocardiogramTool
from neuroagent.tools.eeg_analyzer import EEGAnalyzerTool
from neuroagent.tools.followup_matcher import match_followup, resolve_followup
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.vocabulary import eeg_types, normalize_analyte, lab_panels
from neuroagent_schemas import NeuroBenchCase
from neuroagent_schemas.case import FollowUpToolOutput
from neuroagent_schemas.tool_outputs import AdvancedImagingReport, CardiacMonitoringReport

CASES = Path(__file__).resolve().parents[2] / "data" / "neurobench" / "cases"


def _case(case_id: str) -> NeuroBenchCase:
    path = CASES / f"{case_id}.json"
    if not path.exists():
        pytest.skip(f"dataset case {case_id} not present")
    return NeuroBenchCase.model_validate(json.loads(path.read_text()))


def _fu(trigger: str, tool: str, tag: str):
    return SimpleNamespace(trigger_action=trigger, tool_name=tool, output={"tag": tag})


# --------------------------------------------------------------------------- 1. filter first


def test_a_refused_sibling_does_not_shadow_the_follow_up_that_answers():
    fus = [
        _fu("request_pelvis_abdomen_mri", "order_body_imaging", "MRI"),
        _fu("request_pelvis_abdomen_ultrasound", "order_body_imaging", "ultrasound"),
    ]
    # The context names both modalities, so the two triggers tie on tokens.
    call = {"study": "pelvis_abdomen_ultrasound", "clinical_context": "pelvic ultrasound/MRI/CT"}
    assert match_followup("order_body_imaging", call, fus).output["tag"] == "MRI"  # the old tie
    chosen = match_followup(
        "order_body_imaging", call, fus, accepts=lambda fu: fu.output["tag"] == "ultrasound"
    )
    assert chosen.output["tag"] == "ultrasound"


def test_se_m05_pelvic_ultrasound_is_answered_by_the_case_ultrasound():
    case = _case("SE-M05")
    stored = next(
        f for f in case.followup_outputs
        if f.tool_name == "order_body_imaging" and f.output.modality == "ultrasound"
    )
    result = MockServer(case).get_output(
        "order_body_imaging",
        {"study": "pelvis_abdomen_ultrasound",
         "clinical_context": "Pelvic ultrasound, MRI or CT for an ovarian teratoma"},
    )
    assert result.success and not result.from_fallback
    assert result.output == stored.output.model_dump()


# --------------------------------------------------------------------------- 2. enum terms

EEG_TERMS = eeg_types()


def test_another_terms_tokens_in_free_text_do_not_route():
    # FEPI-TEMP M03 / RP02: an ambulatory order whose context recalls the non-diagnostic
    # sleep-deprived study was answered with the sleep-deprived EEG.
    fus = [
        _fu("request_sleep_deprived_eeg", "analyze_eeg", "sleep"),
        _fu("request_ambulatory_eeg", "analyze_eeg", "ambulatory"),
    ]
    call = {"eeg_type": "ambulatory", "clinical_context": "routine and sleep-deprived EEGs non-diagnostic"}
    chosen = match_followup("analyze_eeg", call, fus, enum_terms=EEG_TERMS)
    assert chosen.output["tag"] == "ambulatory"


def test_a_partial_trigger_answers_an_explicit_order_when_the_index_is_another_study():
    # NMDAR-ENC: routine initial EEG, `request_continuous_eeg` holds the cEEG.
    fus = [_fu("request_continuous_eeg", "analyze_eeg", "cEEG")]
    got = resolve_followup(
        "analyze_eeg", {"eeg_type": "continuous_icu"}, fus, set(),
        has_initial_output=True, is_repeat_call=False, enum_terms=EEG_TERMS,
    )
    assert got is not None and got.output["tag"] == "cEEG"


def test_a_partial_trigger_does_not_capture_an_index_order_that_is_already_that_study():
    # SE: the initial output is the continuous recording; the follow-up is a later one.
    fus = [_fu("request_continuous_eeg_monitoring", "analyze_eeg", "later")]
    call = {"eeg_type": "continuous_icu"}
    first = resolve_followup(
        "analyze_eeg", call, fus, set(), has_initial_output=True, is_repeat_call=False,
        enum_terms=EEG_TERMS, index_terms=["continuous_icu"],
    )
    assert first is None  # the initial answers the index order
    repeat = resolve_followup(
        "analyze_eeg", call, fus, set(), has_initial_output=True, is_repeat_call=True,
        enum_terms=EEG_TERMS, index_terms=["continuous_icu"],
    )
    assert repeat is not None and repeat.output["tag"] == "later"  # a plain re-order of it


def test_a_default_term_counts_only_as_a_whole():
    csf = ["lumbar_puncture", "shunt_tap", "external_ventricular_drain"]
    tap = {"clinical_context": "large-volume lumbar puncture tap test"}
    # NPH-P08: extended drainage shares "lumbar" with the implied lumbar puncture.
    drainage = [_fu("request_extended_lumbar_drainage", "analyze_csf", "ELD")]
    assert match_followup("analyze_csf", tap, drainage, enum_terms=csf,
                          implied_terms=["lumbar_puncture"]) is None
    # BACT-MEN: the LP follow-up names the whole implied term and still answers.
    lp = [_fu("request_csf_culture_final_report", "analyze_csf", "final"),
          _fu("request_lumbar_puncture", "analyze_csf", "LP")]
    chosen = match_followup("analyze_csf", {**tap, "special_tests": ["culture"]}, lp,
                            enum_terms=csf, implied_terms=["lumbar_puncture"])
    assert chosen.output["tag"] == "LP"


@pytest.mark.parametrize(
    "tool_cls", [EEGAnalyzerTool, CSFAnalyzerTool, EchocardiogramTool, CardiacMonitoringTool]
)
def test_enum_defaults_mirror_the_tool_schemas(tool_cls):
    tool = tool_cls()
    key, default = MockServer._ENUM_DEFAULTS[tool.name]
    assert tool.parameter_schema["properties"][key]["default"] == default


# --------------------------------------------------------------------------- 3. monitors


def _with(case: NeuroBenchCase, *followups: FollowUpToolOutput, fallback=None, initial=None):
    case = case.model_copy(deep=True)
    case.followup_outputs = [
        f for f in case.followup_outputs if f.tool_name != "order_cardiac_monitoring"
    ] + list(followups)
    case.initial_tool_outputs.cardiac_monitoring = initial
    if case.fallback_tool_outputs is not None:
        case.fallback_tool_outputs.cardiac_monitoring = fallback
        case.fallback_tool_outputs.advanced_imaging = None
    return case


def _monitor(monitor_type: str, hours: int, tag: str) -> CardiacMonitoringReport:
    return CardiacMonitoringReport(monitor_type=monitor_type, duration_hours=hours, impression=tag)


def _order(server: MockServer, monitor_type: str):
    return server.get_output(
        "order_cardiac_monitoring", {"clinical_context": "paroxysmal AF?", "monitor_type": monitor_type}
    )


def test_each_monitor_order_receives_its_own_stored_recording():
    holter = _monitor("holter_24h", 24, "holter")
    ilr = _monitor("implantable_loop_recorder", 4320, "ILR: AF burden 3%")
    case = _with(
        _case("FEPI-TEMP-M01"),
        FollowUpToolOutput(trigger_action="request_holter", tool_name="order_cardiac_monitoring", output=holter),
        FollowUpToolOutput(trigger_action="request_loop_recorder", tool_name="order_cardiac_monitoring", output=ilr),
    )
    assert _order(MockServer(case), "holter_24h").output["impression"] == "holter"
    assert _order(MockServer(case), "implantable_loop_recorder").output["impression"].startswith("ILR")


def test_a_short_order_never_receives_a_longer_recording():
    # VASC-DEM-P08 / MIG-AURA-P07: 12 months of device data or a loop recorder's AF served for
    # a 24-hour Holter order.
    device = CardiacMonitoringReport(
        monitor_type="pacemaker interrogation, stored device diagnostics", duration_hours=8760,
        impression="AF burden 2.1%",
    )
    case = _with(_case("FEPI-TEMP-M01"), initial=device)
    for short in ("holter_24h", "holter_48h", "telemetry", "event_monitor_30d"):
        result = _order(MockServer(case), short)
        assert result.library and result.output["impression"] != "AF burden 2.1%", short
    assert not _order(MockServer(case), "implantable_loop_recorder").library  # prose, as long


def test_a_longer_order_and_a_same_tier_order_keep_the_case_recording():
    holter48 = _monitor("holter_48h", 48, "48 h: paroxysmal AF")
    case = _with(_case("FEPI-TEMP-M01"), initial=holter48)
    for order in ("holter_24h", "holter_48h", "event_monitor_30d", "implantable_loop_recorder"):
        assert _order(MockServer(case), order).output["impression"] == "48 h: paroxysmal AF", order


def test_device_interrogation_answers_and_is_answered_by_its_own_type_only():
    device = _monitor("device_interrogation", 4320, "device")
    case = _with(_case("FEPI-TEMP-M01"), initial=device)
    assert _order(MockServer(case), "device_interrogation").output["impression"] == "device"
    assert _order(MockServer(case), "implantable_loop_recorder").library
    holter_only = _with(_case("FEPI-TEMP-M01"), initial=_monitor("holter_24h", 24, "holter"))
    result = _order(MockServer(holter_only), "device_interrogation")
    assert result.library and result.output["monitor_type"] == "device_interrogation"


# --------------------------------------------------------------------------- 4. case fallback


def test_a_typed_case_fallback_answers_only_its_own_study():
    case = _case("FEPI-TEMP-M01").model_copy(deep=True)
    assert case.fallback_tool_outputs is not None
    case.initial_tool_outputs.advanced_imaging = None
    case.followup_outputs = [f for f in case.followup_outputs if f.tool_name != "order_advanced_imaging"]
    case.fallback_tool_outputs.advanced_imaging = AdvancedImagingReport(
        modality="amino_acid_PET", impression="case-specific FET-PET"
    )
    call = lambda modality: MockServer(case).get_output(  # noqa: E731
        "order_advanced_imaging", {"clinical_context": "x", "modality": modality}
    )
    assert call("amino_acid_PET").output["impression"] == "case-specific FET-PET"
    other = call("FDG_PET")
    assert other.library and other.output["modality"] == "FDG_PET"
    # A fallback that names no study is not adjudicated and still answers any modality.
    case.fallback_tool_outputs.advanced_imaging = AdvancedImagingReport(impression="non-contributory")
    assert call("FDG_PET").output["impression"] == "non-contributory"


# --------------------------------------------------------------------------- vocabulary


def test_b12_spellings_are_one_assay():
    assert normalize_analyte("B12") == normalize_analyte("vitamin_B12")
    assert "vitamin_B12" in lab_panels() and "B12" not in lab_panels()
