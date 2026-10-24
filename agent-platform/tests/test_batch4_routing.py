"""MockServer routing added with the batch-4 vocabulary (24 Oct 2026).

* `timing` on `perform_clinical_assessment` and `source` on `analyze_csf` are secondary
  discriminators: NPH's baseline timed gait and post-tap reassessment are the same assessment type,
  and NPH-P08's extended lumbar drainage is the same tool as its tap (NPH R3, R4).
* An earlier call makes a call a repeat only when it ordered the same study (NPH R5).
* A combined lab order receives every stored panel that answers one of its assays, not only the
  first output that matched (MG-P04, SE-P05, SE-M08).
"""

from __future__ import annotations

import json
from pathlib import Path

from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent.tools.cost_tracker import CostTracker
from neuroagent.tools.fallback_library import default_library
from neuroagent_schemas import NeuroBenchCase, ToolAction

CASES = Path(__file__).resolve().parents[2] / "data" / "neurobench" / "cases"


def _env(case_id: str) -> NeuroBenchEnvironment:
    return NeuroBenchEnvironment(NeuroBenchCase.model_validate_json((CASES / f"{case_id}.json").read_text()))


def _call(env: NeuroBenchEnvironment, tool: str, **arguments):
    arguments.setdefault("clinical_context", "test")
    result = env.execute(ToolAction(tool_name=tool, arguments=arguments))
    assert not result.error_message, result.error_message
    return result


def test_timing_routes_baseline_and_post_tap_gait():
    env = _env("NPH-M01")
    post = _call(env, "perform_clinical_assessment", assessment_type="gait_and_balance_timed", timing="post_intervention")
    assert not post.library and post.output["timing"] == "post_intervention"
    base = _call(env, "perform_clinical_assessment", assessment_type="gait_and_balance_timed")
    assert not base.library and base.output["timing"] == "baseline"
    again = _call(env, "perform_clinical_assessment", assessment_type="gait_and_balance_timed")
    assert again.output["timing"] == "baseline"  # a bare re-order is never the post-tap result


def test_lumbar_drain_is_not_the_tap():
    env = _env("NPH-P08")
    tap = _call(env, "analyze_csf")
    assert not tap.library and tap.output.get("source") in ("", "lumbar_puncture")
    drain = _call(env, "analyze_csf", source="lumbar_drain")
    assert not drain.library and drain.output["source"] == "lumbar_drain"
    again = _call(env, "analyze_csf")
    assert again.output.get("source") != "lumbar_drain"


def test_drain_first_does_not_receive_the_tap_and_tap_is_still_served():
    env = _env("NPH-P08")
    drain = _call(env, "analyze_csf", source="lumbar_drain")
    assert drain.output["source"] == "lumbar_drain"
    tap = _call(env, "analyze_csf")
    assert not tap.library and tap.output.get("source") != "lumbar_drain"


def test_repeat_call_counts_only_the_same_study():
    env = _env("NPH-M01")
    server = env.mock_server
    _call(env, "perform_clinical_assessment", assessment_type="cognitive_screen")
    assert not server._is_repeat_call("perform_clinical_assessment", {"assessment_type": "gait_and_balance_timed"})
    assert server._is_repeat_call("perform_clinical_assessment", {"assessment_type": "cognitive_screen"})
    _call(env, "perform_clinical_assessment", assessment_type="gait_and_balance_timed")
    assert not server._is_repeat_call(
        "perform_clinical_assessment", {"assessment_type": "gait_and_balance_timed", "timing": "post_intervention"}
    )
    assert server._is_repeat_call("perform_clinical_assessment", {"assessment_type": "gait_and_balance_timed", "timing": "baseline"})


def test_combined_lab_order_returns_every_matching_panel():
    env = _env("MG-P04")
    labs = _call(env, "interpret_labs", panels=["anti_AChR", "anti_MuSK", "TSH", "anti_LRP4"])
    panels = set(labs.output["panels"])
    assert {"Neuromuscular_Junction_Antibody_Panel", "Thyroid_Function", "Extended_Seronegative_MG_Panel"} <= panels


def test_combined_lab_order_adds_a_followup_panel():
    env = _env("SE-P05")
    labs = _call(env, "interpret_labs", panels=["CBC", "CMP", "magnesium", "tox_screen", "RBC_cholinesterase"])
    assert "Cholinesterase activity" in labs.output["panels"]


def test_single_lab_orders_are_unchanged():
    env = _env("MG-P04")
    lrp4 = _call(env, "interpret_labs", panels=["anti_LRP4"])
    assert set(lrp4.output["panels"]) == {"Extended_Seronegative_MG_Panel"}
    env = _env("MG-P04")
    initial = _call(env, "interpret_labs", panels=["TSH"])
    assert "Extended_Seronegative_MG_Panel" not in initial.output["panels"]


def test_lumbar_drain_is_billed_on_top_of_the_puncture():
    tracker = CostTracker()
    tap = tracker.compute_cost("analyze_csf", {"source": "lumbar_puncture"})
    drain = tracker.compute_cost("analyze_csf", {"source": "lumbar_drain"})
    assert drain.cost_usd == tap.cost_usd + 184
    assert drain.cost_breakdown["source:lumbar_drain"] == 184


def test_library_reports_state_timing_and_source():
    library = default_library()
    post = library.resolve("perform_clinical_assessment", {"assessment_type": "orthostatic_blood_pressure", "timing": "post_intervention"})
    assert post.timing == "post_intervention" and post.assessment_type == "orthostatic_blood_pressure"
    assert library.resolve("perform_clinical_assessment", {"assessment_type": "orthostatic_blood_pressure"}).timing == "baseline"
    drain = library.resolve("analyze_csf", {"source": "lumbar_drain"})
    assert drain.source == "lumbar_drain" and "drain" in json.dumps(drain.model_dump()).lower()
    assert library.resolve("analyze_csf", {}).source == "lumbar_puncture"


def test_genetic_panels_do_not_answer_each_other():
    env = _env("SYNC-CARD-P03")
    other = _call(env, "order_specialized_test", test_type="genetic_panel:cardiomyopathy")
    assert other.library
    own = _call(env, "order_specialized_test", test_type="genetic_panel:inherited_arrhythmia")
    assert not own.library and "SCN5A" in json.dumps(own.output)
