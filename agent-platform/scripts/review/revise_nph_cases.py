"""Apply the July 2026 NPH tool review to the case-level ground truth.

This is intentionally condition-specific.  The reviewers asked for a clinical tap-test
pathway, not a generic specialized-test pathway:

* the CSF action is the lumbar puncture, opening pressure, and 30--50 mL tap;
* the clinical assessment is the timed pre/post gait and cognitive comparison;
* a standalone neuropsychological battery and advanced imaging are not NPH gold actions;
* unrelated CSF assays must not arrive for free with the base tap-test order.

Two case-specific CSF questions survive as separate, explicitly priced actions: Alzheimer
biomarkers in NPH-P01 (whose ground truth includes AD copathology), and cytology plus flow
cytometry in NPH-P06 (active cancer with leptomeningeal disease in the differential).

The migration is idempotent and only touches the 30 cases whose condition is ``nph``.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

AD_TESTS = ["Abeta42", "phospho_tau", "total_tau"]
CYTOLOGY_TESTS = ["cytology", "flow_cytometry"]


def _walk_strings(value: Any, transform: Any) -> Any:
    if isinstance(value, str):
        return transform(value)
    if isinstance(value, list):
        return [_walk_strings(item, transform) for item in value]
    if isinstance(value, dict):
        return {key: _walk_strings(item, transform) for key, item in value.items()}
    return value


def _revise_prose(text: str) -> str:
    replacements = {
        ">=20% improvement in timed-up-and-go or 10-metre walk":
            ">10% improvement in TUG is a commonly used positive criterion; absolute change "
            "and concordant gait and cognitive findings should also be considered",
        "Baseline timed gait recorded before the tap and repeated after it, with the response "
        "read against the >=20% threshold and the cognitive screen repeated alongside":
            "Baseline timed gait recorded before the tap and repeated after it, with the response "
            "interpreted from the prespecified objective change and the cognitive screen repeated "
            "alongside",
        "Reversible-cause labs (TSH, B12, RPR, HIV) are mandatory before attributing the "
        "syndrome to NPH":
            "Reversible-cause laboratory tests do not diagnose NPH and are optional; order "
            "targeted tests only when the presentation suggests a metabolic, endocrine, "
            "infectious, inflammatory, vitamin, or medication-related mimic",
        "Large-volume lumbar puncture (30-50 mL tap test) with opening pressure and pre/post "
        "gait + neuropsych assessment":
            "Large-volume lumbar puncture (30-50 mL tap test) with opening pressure and "
            "prespecified pre/post objective gait and cognitive assessment",
        "Opening pressure <25 cmH2O (normal); 30-50 mL CSF removed; pre/post tap gait and "
        "neuropsych assessment shows objective improvement supporting shunt-responsive iNPH":
            "Opening pressure compatible with NPH criteria; 30-50 mL CSF removed; prespecified "
            "pre/post gait and cognitive measures show objective change relevant to shunt "
            "responsiveness",
        "The tap test is a 30-50 mL large-volume LP with pre/post objective gait (TUG, "
        "10-metre walk) and neuropsychological assessment; opening pressure must be normal "
        "(<25 cmH2O) to satisfy the 'normal pressure' criterion":
            "The tap test removes 30-50 mL of CSF after measuring opening pressure and compares "
            "prespecified objective gait and cognitive measures before and after drainage; a "
            "positive response supports shunt responsiveness, while a negative single tap does "
            "not exclude NPH",
        "Approximately 50% of iNPH patients have AD copathology — this lowers cognitive benefit "
        "from shunting but does not negate gait benefit":
            "Alzheimer copathology is common in iNPH and may reduce cognitive benefit from "
            "shunting without necessarily eliminating gait benefit",
        "Document objective pre-tap gait (TUG and 10-metre walk) and neuropsychological baseline "
        "so that pre/post-tap change can be quantified":
            "Document objective pre-tap gait (TUG and 10-metre walk) and a brief cognitive "
            "baseline so that pre/post-tap change can be quantified",
        "Establish objective pre-tap gait baseline (TUG and 10-metre walk) and "
        "neuropsychological baseline before performing the tap test":
            "Establish objective pre-tap gait (TUG and 10-metre walk) and brief cognitive "
            "baselines before performing the tap test",
        "pre/post objective gait and neuropsychological assessment":
            "pre/post objective gait and brief cognitive assessment",
        "pre/post gait and neuropsych assessment":
            "pre/post gait and cognitive assessment",
        "neuropsychological baseline before the tap test":
            "brief cognitive baseline before the tap test",
        "neuropsychological baseline so that pre/post-tap change can be quantified":
            "brief cognitive baseline so that pre/post-tap change can be quantified",
        "CSF biomarkers / amyloid PET resolve copathology":
            "targeted CSF Alzheimer biomarkers can evaluate suspected copathology when the "
            "result would change counselling or management",
        "Tap trial TUG improvement >20%": "Objective tap-test gait improvement",
        "tap trial TUG improvement >20%": "objective tap-test gait improvement",
        "positive tap trial (TUG >20%)": "positive tap trial with objective gait improvement",
        "Positive tap trial (TUG >20%)": "Positive tap trial with objective gait improvement",
        "A positive high-volume tap trial, defined as TUG improvement >20%,":
            "A high-volume tap trial with objective gait improvement",
        "negative amyloid PET associated with better cognitive outcomes":
            "cognitive outcomes vary with comorbidity and baseline impairment",
        "Negative amyloid PET is associated with better cognitive outcomes following shunting. ":
            "Cognitive outcome after shunting is less predictable than gait outcome. ",
        "Even patients with MoCA <20 at baseline recover 4-6 points on average post-shunting "
        "when amyloid PET negative":
            "Baseline cognitive impairment alone does not preclude gait benefit after shunting",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # The old 20% rule labelled 12--19% responses as subthreshold.  SINPHONI used >10%
    # TUG improvement; retain the measured numbers and remove the now-false labels.
    text = re.sub(
        r"(\d+(?:\.\d+)?% improvement)(?: —|;)? (?:just )?(?:below threshold|subthreshold)",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(\d+(?:\.\d+)?% improvement)(?: —|;)? (?:just )?above threshold",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\bneuropsychological (?:profile|pattern)\b",
        "cognitive profile",
        text,
        flags=re.I,
    )
    text = re.sub(r"\bneuropsychological scores\b", "brief cognitive scores", text, flags=re.I)
    text = re.sub(r"\bneuropsychological testing\b", "cognitive assessment", text, flags=re.I)
    return text


def _remove_pet_sentences(text: str) -> str:
    """Remove unsupported PET claims from evidence summaries, not patient history."""
    text = re.sub(
        r"[^.!?\n]*(?:amyloid[ -]PET|FDG-PET)[^.!?\n]*[.!?]",
        "",
        text,
        flags=re.IGNORECASE,
    )
    return re.sub(r"\s{2,}", " ", text).strip()


def _base_csf_summary(csf: dict[str, Any]) -> str:
    count = csf.get("cell_count") or {}
    bits = [f"Opening pressure: {csf.get('opening_pressure')}"]
    if count:
        bits.append(
            f"WBC: {count.get('WBC')}; RBC: {count.get('RBC', 'not reported')}"
        )
    bits.extend((f"Protein: {csf.get('protein')}", f"Glucose: {csf.get('glucose')}"))
    return ". ".join(bits) + "."


def _tap_payload_from_specialized(report: dict[str, Any]) -> tuple[dict[str, Any], str]:
    payload: dict[str, Any] = {}
    for row in report.get("results") or report.get("findings") or []:
        payload.update(row)
    match = re.search(
        r"tap trial \((\d+) mL\)",
        report.get("test_type", "") + " " + report.get("impression", ""),
        re.I,
    )
    if match:
        payload["volume_removed"] = f"{match.group(1)} mL"
    elif "38 mL" in report.get("test_type", ""):
        payload["volume_removed"] = "38 mL"
    return payload, report.get("impression", "")


def _keep_tap_fields(special: dict[str, Any]) -> dict[str, Any]:
    markers = (
        "volume_removed", "pre_tap", "post_tap", "tug", "10m", "walk", "moca",
        "gait", "urinary", "freezing", "cognitive", "behavioral", "note",
    )
    return {
        key: value for key, value in special.items()
        if any(marker in key.lower() for marker in markers)
    }


def _targeted_csf_output(original: dict[str, Any], keys: set[str]) -> dict[str, Any]:
    output = {
        key: value for key, value in original.items()
        if key != "special_tests" and key != "interpretation"
    }
    selected = {
        key: value for key, value in (original.get("special_tests") or {}).items()
        if key in keys or (
            key in {"beta-amyloid_42", "beta_amyloid_42"} and "Abeta42" in keys
        )
    }
    output["special_tests"] = selected
    output["interpretation"] = "; ".join(str(value) for value in selected.values())
    return output


def _append_targeted_action(
    case: dict[str, Any], *, tests: list[str], category: str, action: str,
    expected: str, trigger: str, output: dict[str, Any],
) -> None:
    actions = case["ground_truth"]["optimal_actions"]
    if not any(
        row.get("tool_name") == "analyze_csf"
        and row.get("tool_parameters", {}).get("special_tests") == tests
        for row in actions
    ):
        actions.append({
            "step": 0,
            "action": action,
            "tool_name": "analyze_csf",
            "expected_finding": expected,
            "category": category,
            "tool_parameters": {"special_tests": tests},
            "citation": "[Nakajima_2021]",
            "guideline_source": "NPH_pack",
        })
    if not any(row.get("trigger_action") == trigger for row in case["followup_outputs"]):
        case["followup_outputs"].append({
            "trigger_action": trigger,
            "tool_name": "analyze_csf",
            "tool_parameters": {"special_tests": tests},
            "output": output,
        })


def revise_case(
    case: dict[str, Any], *, source_case: dict[str, Any] | None = None,
) -> dict[str, int]:
    if case.get("condition") != "nph":
        return {}

    stats: dict[str, int] = {}
    case_id = case["case_id"]
    original_csf = json.loads(json.dumps(case["initial_tool_outputs"]["csf"]))

    actions = case["ground_truth"]["optimal_actions"]
    kept = []
    for row in actions:
        is_neuropsych = (
            row.get("tool_name") == "order_specialized_test"
            and row.get("tool_parameters", {}).get("test_type") == "neuropsych_battery"
        )
        is_advanced = row.get("tool_name") == "order_advanced_imaging"
        if is_neuropsych or is_advanced:
            key = "neuropsych_action_removed" if is_neuropsych else "advanced_action_removed"
            stats[key] = stats.get(key, 0) + 1
            continue
        kept.append(row)
    case["ground_truth"]["optimal_actions"] = kept

    # REMOVE in the reviewer matrix must change what the simulated tools can return, not
    # merely stop rewarding the calls.  Otherwise an agent can still order PET, flow MRI,
    # a neuropsychology battery, EMG, or urodynamics and receive the old authored result.
    removed_followups = [
        row for row in case["followup_outputs"]
        if row.get("tool_name") in {"order_advanced_imaging", "order_specialized_test"}
    ]
    if removed_followups:
        case["followup_outputs"] = [
            row for row in case["followup_outputs"] if row not in removed_followups
        ]
        stats["removed_advanced_or_specialized_followups"] = len(removed_followups)

    initial = case["initial_tool_outputs"]
    specialized = initial.get("specialized_test")
    tap_impression = ""
    if specialized:
        label = specialized.get("test_type", "").lower()
        if "neuropsych" in label:
            initial.pop("specialized_test")
            stats["initial_neuropsych_report_removed"] = 1
        elif "tap trial" in label or "lumbar puncture" in label:
            tap_fields, tap_impression = _tap_payload_from_specialized(specialized)
            initial["csf"].setdefault("special_tests", {}).update(tap_fields)
            initial.pop("specialized_test")
            stats["tap_report_moved_to_csf"] = 1

    # M09 stored the actual tap as an unparameterized follow-up while the initial CSF result
    # contained only unrelated assays.  Promote the report that answers the required action.
    if case_id == "NPH-M09":
        tap_rows = [
            row for row in case["followup_outputs"]
            if row.get("trigger_action") == "request_tap_test_gait_assessment"
        ]
        if tap_rows:
            initial["csf"] = tap_rows[0]["output"]
            case["followup_outputs"] = [row for row in case["followup_outputs"] if row not in tap_rows]
            stats["tap_followup_promoted"] = 1

    csf = initial["csf"]
    csf["special_tests"] = _keep_tap_fields(csf.get("special_tests") or {})
    # A migration interrupted after removing the misrouted specialized-test object can be
    # resumed safely: recover only the tap payload from the pre-migration revision.
    if len(csf["special_tests"]) <= 1 and source_case is not None:
        source_specialized = source_case.get("initial_tool_outputs", {}).get("specialized_test")
        if source_specialized and "neuropsych" not in source_specialized.get("test_type", "").lower():
            recovered, recovered_impression = _tap_payload_from_specialized(source_specialized)
            if recovered:
                csf["special_tests"].update(recovered)
                tap_impression = recovered_impression
                stats["tap_payload_recovered"] = 1
    if case_id == "NPH-S11" and not csf["special_tests"]:
        # The original case stored these measurements in the CSF report while a separate
        # neuropsychology object happened to say "prior to tap trial" in its label.  Preserve
        # the actual tap data and do not mistake that label for the tap report.
        csf["special_tests"] = {
            "volume_removed": "40 mL",
            "pre_tap_TUG": "26 seconds",
            "post_tap_TUG_2h": "21 seconds (19% improvement)",
            "post_tap_TUG_24h": "17 seconds (35% improvement)",
            "pre_tap_10m_walk": "19 seconds",
            "post_tap_10m_walk_24h": "13 seconds (32% improvement)",
            "pre_tap_MoCA": "23/30",
            "post_tap_MoCA_24h": "26/30 (3-point improvement)",
        }
        tap_impression = (
            "Large-volume tap (40 mL): TUG improved from 26 to 17 seconds at 24 hours "
            "(35%); 10-meter walk improved from 19 to 13 seconds (32%); MoCA improved "
            "from 23/30 to 26/30."
        )
    base = _base_csf_summary(csf)
    existing = csf.get("interpretation", "")
    if tap_impression:
        csf["interpretation"] = f"{base} {tap_impression}"
    elif "tap" in existing.lower() or "tug" in existing.lower():
        # Existing tap reports are already case-specific and retain the measured values.
        csf["interpretation"] = existing
    else:
        csf["interpretation"] = base

    if case_id == "NPH-P01":
        targeted = _targeted_csf_output(
            original_csf,
            {"beta-amyloid_42", "Abeta42", "phospho_tau", "total_tau", "ptau_abeta_ratio"},
        )
        _append_targeted_action(
            case,
            tests=AD_TESTS,
            category="recommended",
            action="Targeted CSF Alzheimer biomarkers to evaluate the suspected AD copathology",
            expected="Low Abeta42 with elevated phospho-tau and total tau supports concurrent Alzheimer pathology",
            trigger="request_targeted_csf_abeta42_phospho_tau",
            output=targeted,
        )
        stats["targeted_ad_csf_action_added"] = 1
    elif case_id == "NPH-P06":
        targeted = _targeted_csf_output(original_csf, set(CYTOLOGY_TESTS))
        _append_targeted_action(
            case,
            tests=CYTOLOGY_TESTS,
            category="required",
            action="Targeted CSF cytology and flow cytometry to exclude leptomeningeal carcinomatosis",
            expected="No malignant cells and no abnormal population on flow cytometry",
            trigger="request_targeted_csf_cytology_flow",
            output=targeted,
        )
        stats["targeted_cytology_action_added"] = 1

    # The base tap action must not silently request legacy assays.  Targeted AD markers in
    # P01 and cytology/flow in P06 remain separate actions with their own parameters/costs.
    for row in case["ground_truth"]["optimal_actions"]:
        if row.get("tool_name") == "analyze_csf" and "tap" in row.get("action", "").lower():
            row["tool_parameters"] = {}

    # Literature summaries may still be useful, but claims based on the removed PET pathway
    # are not.  Patient history is deliberately left untouched when it records a genuinely
    # prior cognitive assessment or says that PET was never obtained.
    for row in case["followup_outputs"]:
        if row.get("tool_name") == "search_medical_literature":
            row["output"] = _walk_strings(row.get("output", {}), _remove_pet_sentences)

    vocab_gap = case.get("metadata", {}).get("vocab_gap")
    if isinstance(vocab_gap, list):
        case["metadata"]["vocab_gap"] = [
            item for item in vocab_gap
            if "extended_lumbar_drainage" not in str(item)
            and "neuropsych_battery" not in str(item)
        ]

    revised = _walk_strings(case, _revise_prose)
    case.clear()
    case.update(revised)

    # These three legacy CSF narratives listed assays that are absent from the now-clean
    # base payload.  Keep the measured tap response and remove the unrequested results.
    if case_id in {"NPH-M10", "NPH-P08", "NPH-P09"}:
        interpretation = case["initial_tool_outputs"]["csf"].get("interpretation", "")
        interpretation = re.sub(
            r"(?:No malignant cells on cytology|Cytology: [Nn]o malignant cells)\.\s*",
            "",
            interpretation,
        )
        interpretation = re.sub(
            r"CSF AD biomarkers within normal limits \([^)]*\)\.\s*",
            "",
            interpretation,
        )
        case["initial_tool_outputs"]["csf"]["interpretation"] = interpretation

    # Case-specific ground-truth statements that made removed advanced imaging load-bearing.
    descriptions = {
        "NPH-M01": (
            "Moderate NPH — Evans index borderline (0.31), moderate white matter disease, "
            "and a measurable but modest tap response; possible AD copathology remains a "
            "separate counselling question."
        ),
        "NPH-M04": (
            "Moderate NPH with prior cervical surgery (myelopathy red herring), treated "
            "hypothyroidism, family history of AD, and mixed cognitive features."
        ),
        "NPH-P01": (
            "Diagnostic-puzzle NPH with a prior Alzheimer's diagnosis, a modest tap response, "
            "and AD copathology supported by separately ordered targeted CSF biomarkers."
        ),
        "NPH-P04": (
            "Diagnostic-puzzle NPH superimposed on bvFTD; behavioral disinhibition overlaps "
            "with FTD, while serial objective drainage assessment clarifies the NPH component."
        ),
        "NPH-P09": (
            "Cognitive-predominant iNPH with a prior Alzheimer's label as the main anchor: "
            "subtle magnetic gait, DESH/callosal-angle findings, and a strongly positive "
            "objective tap response support shunt-responsive iNPH without requiring PET."
        ),
        "NPH-S01": (
            "Classic NPH: complete clinical triad, Evans index 0.38, callosal angle 72 degrees, "
            "DESH pattern, and a strongly positive objective tap response."
        ),
        "NPH-S06": (
            "Straightforward severe iNPH in an 80-year-old with prior CABG: florid structural "
            "imaging and a strongly positive tap response; age and cardiac history complicate "
            "procedural counselling."
        ),
    }
    if case_id in descriptions:
        case["metadata"]["difficulty_variant_description"] = descriptions[case_id]

    if case_id == "NPH-M10":
        case["ground_truth"]["differential"][3]["key_features"] = (
            "Cognitive slowing is frontal-subcortical rather than predominantly amnestic; "
            "hippocampal atrophy is mild and gait disturbance is disproportionate to cognition"
        )
        case["ground_truth"]["optimal_actions"][3]["expected_finding"] = (
            "Opening pressure 17 cmH2O; 40 mL removed; TUG and 10-m walk improve 32% at "
            "24 hours; MoCA improves 2 points"
        )
        case["ground_truth"]["critical_actions"][4] = (
            "Record timed gait and a brief cognitive baseline before the tap, then repeat the "
            "same measures at prespecified intervals"
        )

    if case_id == "NPH-P01":
        literature = next(
            row for row in case["followup_outputs"]
            if row.get("trigger_action") == "request_literature_nph_alzheimer_copathology"
        )
        literature["output"] = {
            "query": "iNPH coexisting Alzheimer pathology shunt counselling",
            "results": [{
                "title": "Guidelines for management of idiopathic normal pressure hydrocephalus",
                "year": "2021",
                "key_finding": (
                    "Coexisting neurodegenerative disease should be considered when counselling "
                    "about outcome, but it does not replace assessment of the NPH syndrome, MRI "
                    "features, and objective response to CSF drainage."
                ),
            }],
            "summary": (
                "Targeted Alzheimer biomarkers answer a separate copathology question; the NPH "
                "diagnosis and shunt evaluation still rest on the clinical syndrome, structural "
                "imaging, and objective drainage response."
            ),
        }

    if case_id == "NPH-P08":
        case["ground_truth"]["differential"][4]["key_features"] = (
            "Cognitive impairment is frontal-subcortical rather than predominantly amnestic; "
            "the gait-predominant syndrome and preserved hippocampal volumes argue against AD "
            "as the sole explanation"
        )
        case["ground_truth"]["critical_actions"][1] = (
            "Document objective pre-tap TUG, 10-metre walk, and a brief cognitive score so the "
            "same measures can be compared after drainage"
        )

    if case_id == "NPH-P09":
        gt = case["ground_truth"]
        gt["differential"][0]["key_features"] = (
            "Cognitive slowing and family history created an Alzheimer anchor, but the "
            "gait-predominant syndrome, DESH, and objective tap response support iNPH"
        )
        gt["optimal_actions"][0]["action"] = (
            "Literature review of iNPH diagnostic criteria and cognitive-predominant presentations"
        )
        gt["optimal_actions"][0]["expected_finding"] = (
            "Consensus criteria emphasizing clinical syndrome, structural imaging, and objective "
            "response assessment; a negative single tap does not exclude iNPH"
        )
        gt["optimal_actions"][3]["expected_finding"] = (
            "Opening pressure 14 cmH2O; 40 mL removed; TUG improves 32%, 10-m walk 27%, "
            "and MoCA 3 points at 24 hours"
        )
        gt["optimal_actions"][5]["action"] = (
            "Neurosurgery consultation for VP shunt candidacy after MRI and objective tap testing"
        )
        gt["optimal_actions"][5]["expected_finding"] = (
            "Neurosurgery assesses candidacy and discusses expected gait benefit, procedural "
            "risk, and uncertainty in cognitive recovery"
        )
        gt["critical_actions"] = [
            item for item in gt["critical_actions"] if "amyloid PET" not in item
        ]
        gt["critical_actions"] = [
            item.replace("imaging, tap test, and amyloid PET", "MRI and objective tap testing")
            for item in gt["critical_actions"]
        ]
        gt["key_reasoning_points"] = [
            item for item in gt["key_reasoning_points"] if "amyloid PET" not in item
        ]
        gt["red_herrings"][0]["correct_interpretation"] = (
            "The prior AD label did not account for the gait syndrome; MRI with Evans index "
            "0.36, DESH, and callosal angle 74 degrees mandates an iNPH evaluation"
        )
        gt["red_herrings"][1]["correct_interpretation"] = (
            "Family history is a risk factor, not a diagnosis; DESH, the magnetic gait, and the "
            "objective tap response are more specific evidence for the current syndrome"
        )
        comparison = case["initial_tool_outputs"]["clinical_assessment"]["pre_post_comparison"]
        comparison["after the tap"] = (
            "At 24 hours, TUG improved from 28 to 19 seconds (32%), the 10-metre walk from "
            "22 to 16 seconds (27%), and MoCA by 3 points"
        )
        literature = next(
            row for row in case["followup_outputs"]
            if row.get("trigger_action") == "request_literature_nph_cognitive_predominant"
        )
        literature["output"] = {
            "query": "iNPH cognitive-predominant presentation objective tap-test assessment",
            "results": [{
                "title": "Guidelines for management of idiopathic normal pressure hydrocephalus",
                "year": "2021",
                "key_finding": (
                    "Assess gait with an objective measure such as TUG or a short-distance walk "
                    "before and after CSF drainage, repeat assessment over the following days, "
                    "and do not treat a negative single tap as exclusionary."
                ),
            }],
            "summary": (
                "The clinical syndrome, structural MRI pattern, and prespecified change on repeated "
                "gait and brief cognitive measures support the diagnosis; no PET result is required."
            ),
        }

    if case_id == "NPH-S11":
        base_action = next(
            row for row in case["ground_truth"]["optimal_actions"]
            if row.get("tool_name") == "analyze_csf" and "tap" in row.get("action", "").lower()
        )
        base_action["tool_parameters"] = {}
        base_action["expected_finding"] = (
            "Opening pressure 13 cmH2O; 40 mL removed; TUG improves 35%, 10-m walk 32%, "
            "and MoCA 3 points at 24 hours"
        )
        case["ground_truth"]["differential"][1]["key_features"] = (
            "Cognitive decline and family history raise AD concern, but gait-predominant triad, "
            "DESH, and a frontal-subcortical cognitive pattern argue against AD as the sole cause"
        )
        case["ground_truth"]["key_reasoning_points"] = [
            item for item in case["ground_truth"]["key_reasoning_points"]
            if "CSF biomarkers" not in item
        ]

    positive = case["initial_tool_outputs"]["clinical_assessment"].get("criteria_met", {})
    if "response_meets_the_threshold" in positive:
        positive["response_meets_the_threshold"] = case_id != "NPH-P08"
    scores = case["initial_tool_outputs"]["clinical_assessment"].get("scores", {})
    if "positive-response threshold" in scores:
        scores["positive-response threshold"] = (
            ">10% TUG improvement is a commonly used criterion; interpret with absolute change "
            "and concordant gait/cognitive findings"
        )

    positive_impression = (
        "Objective gait and cognition were measured before the large-volume tap and repeated "
        "after it. The objective improvement is consistent with a positive tap response and "
        "increases the likelihood of shunt responsiveness; it must be integrated with the "
        "clinical syndrome and structural imaging."
    )
    negative_impression = (
        "Objective gait and cognition were measured before the large-volume tap and repeated "
        "after it. No objective improvement occurred after this single tap. Because sensitivity "
        "is limited, this does not exclude shunt-responsive NPH; extended lumbar drainage is a "
        "reasonable next test when the clinical and imaging evidence remains strong."
    )
    case["initial_tool_outputs"]["clinical_assessment"]["impression"] = (
        negative_impression if case_id == "NPH-P08" else positive_impression
    )

    actions = case["ground_truth"]["optimal_actions"]
    for step, row in enumerate(actions, start=1):
        row["step"] = step

    counts = {
        tier: sum(row.get("category") == tier for row in actions)
        for tier in ("required", "recommended", "optional")
    }
    red_herrings = len(case["ground_truth"].get("red_herrings") or [])
    differentials = len(case["ground_truth"].get("differential") or [])
    case["metadata"]["difficulty_rationale"] = (
        f"{counts['required']} required, {counts['recommended']} recommended, and "
        f"{counts['optional']} optional actions after the July 2026 NPH review; "
        f"{red_herrings} grounded red herring(s); {differentials} differential alternatives."
    )
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = (
        "case-level re-audit of all NPH reviewer requests: the tap report is routed to CSF, "
        "timed gait/cognitive assessment is the required pre/post measure, the standalone "
        "neuropsychological battery and advanced imaging are removed from gold actions and "
        "callable authored follow-ups, "
        "laboratories remain optional, unrelated CSF assays are no longer returned for free, "
        "and the unsupported universal 20% response threshold is corrected"
    )
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    totals: dict[str, int] = {}
    changed = 0
    changed_paths: list[str] = []
    seen = 0
    for path in sorted(args.cases_dir.glob("NPH-*.json")):
        before = path.read_text()
        case = json.loads(before)
        if case.get("condition") != "nph":
            continue
        seen += 1
        source_case = None
        try:
            relative = path.resolve().relative_to(ROOT)
            source_raw = subprocess.check_output(
                ["git", "show", f"HEAD:{relative.as_posix()}"],
                cwd=ROOT,
                text=True,
                stderr=subprocess.DEVNULL,
            )
            source_case = json.loads(source_raw)
        except (subprocess.CalledProcessError, ValueError):
            pass
        stats = revise_case(case, source_case=source_case)
        after = json.dumps(case, indent=2, ensure_ascii=False) + "\n"
        if after != before:
            changed += 1
            changed_paths.append(path.name)
            if not args.dry_run:
                path.write_text(after)
        for key, value in stats.items():
            totals[key] = totals.get(key, 0) + value

    if seen != 30:
        raise SystemExit(f"expected 30 NPH cases, found {seen}")
    print(f"{'would change' if args.dry_run else 'changed'} {changed}/{seen} NPH cases")
    if changed_paths:
        print("cases: " + ", ".join(changed_paths))
    for key, value in sorted(totals.items()):
        print(f"{value:3d} {key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
