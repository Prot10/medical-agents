"""MockServer routing of EEG type, laboratory panels and MRI contrast (24 Oct 2026).

1. `analyze_eeg` routes by `eeg_type`, read with its schema default (`routine`): a routine order is
   not answered with a stored video-EEG (FND, FEPI-TEMP-RP04 and RS01) or ICU recording (SE).
   `video` and `continuous_icu` are one study for routing (`MockServer._SAME_STUDY`). The index
   recording answers the first order of its own type, and a follow-up of that type answers the
   repeat order only (SE CENTRAL: `request_continuous_eeg_monitoring` with a `continuous_icu` index).
2. `interpret_labs` returns only the stored panels that answer the ordered assays
   (`tools/lab_matching.py`). An assay the case does not store gets the library normal, or "not
   available" in a recorded case, never the first-line labs again.
3. `analyze_brain_mri.contrast` defaults to false. A report that states `contrast_used` answers
   only an order with that value (ALZ-EARLY-RS06); one that does not is not adjudicated. The
   library's normal reports state it and drop their post-gadolinium sentences for a plain order.
4. Matcher fixes (25 Oct 2026): a unit ("mg/dL") is not magnesium; an assay token matches whole
   word stems, so `complement` no longer lands in the CBC ("complete"); a urine or CSF row
   answers only an order that names that specimen, so a CBC or CMP order does not return the
   urinalysis or urine electrolytes; a sleep-deprived EEG order is answered by the stored routine
   EEG when the case stores no sleep-deprived recording (never the reverse), not by the library
   normal.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent.tools.mock_server import MockServer
from neuroagent_schemas import EEGReport, NeuroBenchCase, ToolAction

CASES = Path(__file__).resolve().parents[2] / "data" / "neurobench" / "cases"


def _raw(case_id: str) -> dict:
    path = CASES / f"{case_id}.json"
    if not path.exists():
        pytest.skip(f"dataset case {case_id} not present")
    return json.loads(path.read_text())


def _env(case_id: str, raw: dict | None = None) -> NeuroBenchEnvironment:
    return NeuroBenchEnvironment(NeuroBenchCase.model_validate(raw or _raw(case_id)))


def _call(env: NeuroBenchEnvironment, tool: str, **arguments):
    arguments.setdefault("clinical_context", "test")
    result = env.execute(ToolAction(tool_name=tool, arguments=arguments))
    assert not result.error_message, result.error_message
    return result


# --------------------------------------------------------------------------- 1. EEG type


def test_eeg_report_keeps_its_type():
    report = EEGReport.model_validate({"eeg_type": "video", "classification": "normal", "impression": "x"})
    assert report.eeg_type == "video"


@pytest.mark.parametrize("case_id", ["FND-M01", "FEPI-TEMP-RP04", "FEPI-TEMP-RS01"])
def test_routine_order_is_not_answered_with_the_video_eeg(case_id):
    for arguments in ({}, {"eeg_type": "routine"}):
        result = _call(_env(case_id), "analyze_eeg", **arguments)
        assert result.output["eeg_type"] == "routine", arguments
    video = _call(_env(case_id), "analyze_eeg", eeg_type="video")
    assert not video.from_fallback and video.output["eeg_type"] == "video"


def test_routine_order_in_status_is_not_answered_with_the_icu_recording():
    env = _env("SE-M01")
    assert _call(env, "analyze_eeg").output["eeg_type"] == "routine"
    ceeg = _call(_env("SE-M01"), "analyze_eeg", eeg_type="continuous_icu")
    assert not ceeg.from_fallback and ceeg.output["eeg_type"] == "continuous_icu"


def test_video_and_icu_eeg_are_one_study():
    # SE policies accept `continuous_icu` or `video` for one criterion; NMDAR-ENC stores its
    # monitoring as a follow-up behind a routine index recording.
    se = _call(_env("SE-M01"), "analyze_eeg", eeg_type="video")
    assert not se.from_fallback and se.output["eeg_type"] == "continuous_icu"
    nmdar = _call(_env("NMDAR-ENC-M01"), "analyze_eeg", eeg_type="video")
    assert not nmdar.from_fallback and nmdar.output["eeg_type"] == "continuous_icu"
    fnd = _call(_env("FND-M01"), "analyze_eeg", eeg_type="continuous_icu")
    assert fnd.output["eeg_type"] == "video"


def test_index_recording_answers_the_first_order_and_the_follow_up_the_repeat():
    raw = _raw("SE-P01")
    index = raw["initial_tool_outputs"]["eeg"]
    later = next(f for f in raw["followup_outputs"] if f["tool_name"] == "analyze_eeg")
    env = _env("SE-P01", raw)
    first = _call(env, "analyze_eeg", eeg_type="continuous_icu")
    assert first.output["impression"] == index["impression"]
    second = _call(env, "analyze_eeg", eeg_type="continuous_icu")
    assert second.output["impression"] == later["output"]["impression"]


def test_trigger_repeating_the_index_term_does_not_capture_the_index_order():
    raw = _raw("SE-M01")
    index = raw["initial_tool_outputs"]["eeg"]
    later = {**index, "impression": "Repeat recording after treatment: seizures resolved."}
    raw["followup_outputs"] = [*raw["followup_outputs"], {
        "tool_name": "analyze_eeg", "trigger_action": "request_continuous_eeg_monitoring", "output": later,
    }]
    for arguments in ({"eeg_type": "continuous_icu"},
                      {"eeg_type": "continuous_icu", "clinical_context": "continuous EEG monitoring"}):
        env = _env("SE-M01", raw)
        assert _call(env, "analyze_eeg", **arguments).output["impression"] == index["impression"]
        assert _call(env, "analyze_eeg", **arguments).output["impression"] == later["impression"]


def test_repeat_of_another_eeg_type_is_not_a_repeat():
    env = _env("NMDAR-ENC-M01")
    server: MockServer = env.mock_server
    _call(env, "analyze_eeg")
    assert not server._is_repeat_call("analyze_eeg", {"eeg_type": "continuous_icu"})
    assert server._is_repeat_call("analyze_eeg", {"eeg_type": "routine"})


def test_eeg_guard_fires():
    from test_case_guards import discriminator_defects

    case = {"initial_tool_outputs": {"eeg": {"classification": "normal", "impression": "Normal."}},
            "fallback_tool_outputs": {"eeg": {"eeg_type": "Routine 30-minute EEG", "impression": "x"}}}
    assert len(discriminator_defects(case)) == 2
    case["initial_tool_outputs"]["eeg"]["eeg_type"] = "video"
    case["fallback_tool_outputs"]["eeg"] = None
    assert not discriminator_defects(case)


# --------------------------------------------------------------------------- 2. labs


def _labs(env, *panels):
    return _call(env, "interpret_labs", panels=list(panels))


def test_basic_labs_do_not_return_a_second_tier_panel_stored_beside_them():
    env = _env("NMDAR-ENC-RM02")
    basic = _labs(env, "CBC", "CMP")
    assert "aqp4" not in json.dumps(basic.output).lower()
    assert set(basic.output["panels"]) <= set(_raw("NMDAR-ENC-RM02")["initial_tool_outputs"]["labs"]["panels"])
    aqp4 = _labs(_env("NMDAR-ENC-RM02"), "AQP4_IgG")
    assert "aqp4" in json.dumps(aqp4.output).lower() or "aquaporin" in json.dumps(aqp4.output).lower()


def test_unstored_assay_gets_the_library_normal_not_the_first_line_labs():
    stored = set(_raw("MS-RR-M01")["initial_tool_outputs"]["labs"]["panels"])
    alone = _labs(_env("MS-RR-M01"), "ceruloplasmin")
    assert alone.from_fallback and set(alone.output["panels"]) == {"ceruloplasmin"}
    mixed = _labs(_env("MS-RR-M01"), "CBC", "ceruloplasmin")
    assert set(mixed.output["panels"]) == {"CBC", "ceruloplasmin"} and not stored >= set(mixed.output["panels"])


def test_unstored_assay_is_not_available_in_a_recorded_case():
    raw = _raw("MS-RR-M01")
    raw["provenance"] = "record"
    raw.pop("fallback_tool_outputs", None)
    env = _env("MS-RR-M01", raw)
    result = env.execute(ToolAction(tool_name="interpret_labs", arguments={
        "clinical_context": "test", "panels": ["ceruloplasmin"]}))
    assert result.unavailable
    mixed = _labs(_env("MS-RR-M01", raw), "CBC", "ceruloplasmin")
    assert set(mixed.output["panels"]) == {"CBC"}
    assert "not available" in mixed.output["interpretation"].lower()


def test_cell_based_tokens_do_not_capture_an_nmdar_order():
    # `NMDAR_IgG_cell_based` shared "cell" and "based" with MS-RR-RM01's
    # `request_aqp4_mog_cell_based_assay` follow-up and received the AQP4/MOG result.
    result = _labs(_env("MS-RR-RM01"), "NMDAR_IgG_cell_based")
    assert "aqp4" not in json.dumps(result.output).lower()


# --------------------------------------------------------------------------- 3. MRI contrast


def test_contrast_defaults_to_false():
    from neuroagent.evaluation.policy_reward import executed_arguments

    action = ToolAction(tool_name="analyze_brain_mri", arguments={"clinical_context": "x"})
    assert executed_arguments(action)["contrast"] is False


@pytest.mark.parametrize("order", [[False, True], [True, False], [None, True], [True, True]])
def test_contrast_order_receives_the_contrast_study(order):
    env = _env("ALZ-EARLY-RS06")
    for contrast in order:
        arguments = {"protocol": "dementia"} | ({} if contrast is None else {"contrast": contrast})
        result = _call(env, "analyze_brain_mri", **arguments)
        assert not result.from_fallback
        assert result.output["contrast_used"] is bool(contrast)


def test_library_mri_states_contrast_and_drops_gadolinium_for_a_plain_order():
    from neuroagent.tools.fallback_library import default_library

    library = default_library()
    for protocol in ("standard", "ms", "tumor"):
        plain = library.resolve("analyze_brain_mri", {"protocol": protocol})
        assert plain.contrast_used is False
        assert "gadolinium" not in json.dumps(plain.model_dump()).lower(), protocol
        enhanced = library.resolve("analyze_brain_mri", {"protocol": protocol, "contrast": True})
        assert enhanced.contrast_used is True
        assert "gadolinium" in json.dumps(enhanced.model_dump()).lower(), protocol


# --------------------------------------------------------------------------- 4. matcher fixes


def test_milligram_unit_is_not_magnesium():
    from neuroagent.tools.lab_matching import tokens

    assert "magnesium" not in tokens("Glucose 112 mg/dL")
    assert "magnesium" not in tokens("Creatinine 1.1 mg per dL")
    assert "magnesium" in tokens("Mg 1.6")
    result = _labs(_env("HEP-ENC-M07"), "magnesium")
    assert "Endocrine" not in result.output["panels"]


def test_complement_order_does_not_return_the_cbc():
    result = _labs(_env("SE-M03"), "complement")
    assert "Complete Blood Count" not in result.output["panels"]
    assert "c3" in json.dumps(result.output).lower()


@pytest.mark.parametrize("case_id", ["MG-M04", "ISCH-STR-P03"])
def test_cbc_order_does_not_return_the_urinalysis(case_id):
    result = _labs(_env(case_id), "CBC")
    assert "Urinalysis" not in result.output["panels"]
    assert "Urinalysis" in _labs(_env(case_id), "urinalysis").output["panels"]


def test_urine_sodium_does_not_answer_a_cmp_order():
    result = _labs(_env("SE-S03"), "CMP")
    assert not {"Urinalysis", "Urine studies"} & set(result.output["panels"])
    assert "urine" not in json.dumps(result.output["panels"]).lower()


def test_hbv_dna_is_served_on_its_own():
    stored = _labs(_env("HEP-ENC-S05"), "HBV_DNA")
    assert not stored.from_fallback and set(stored.output["panels"]) == {"HBV_DNA"}
    basic = _labs(_env("HEP-ENC-S05"), "CBC", "CMP")
    assert "hbv" not in json.dumps(basic.output["panels"]).lower()
    library = _labs(_env("MS-RR-M01"), "HBV_DNA")
    assert library.from_fallback and set(library.output["panels"]) == {"HBV_DNA"}


def test_sleep_deprived_order_gets_the_stored_routine_eeg():
    routine = _raw("SE-M01")["fallback_tool_outputs"]["eeg"]
    result = _call(_env("SE-M01"), "analyze_eeg", eeg_type="sleep_deprived")
    assert result.output["impression"] == routine["impression"]


def test_routine_order_never_gets_a_sleep_deprived_recording():
    raw = _raw("FEPI-TEMP-M01")
    assert "sleep_deprived" in json.dumps(raw)
    for arguments in ({}, {"eeg_type": "routine"}):
        result = _call(_env("FEPI-TEMP-M01"), "analyze_eeg", **arguments)
        assert result.output["eeg_type"] == "routine", arguments
