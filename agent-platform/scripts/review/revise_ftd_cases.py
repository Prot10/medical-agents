"""Apply Reviewer 1's FTD comments to actions, authored reports and case prose.

The old cases made advanced imaging and genetics effectively mandatory despite the reviewed
panel saying optional, offered amyloid/tau/DaT imaging nearly indiscriminately, and retained
EMG reports in cases without motor-neuron findings.  This migration keeps a narrow set of
case-specific exceptions (FTD-MND, HIV CNS exclusion, and Parkinsonism overlap) and otherwise
implements the requested FTD pathway.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

CORE_LABS = ["CBC", "CMP", "TSH", "B12", "folate", "ESR", "CRP"]
SPECT_CASE = "FTD-S12"
CT_ALTERNATIVE_CASE = "FTD-S06"
AMYLOID_CASES = {"FTD-M04", "FTD-P03", "FTD-P06"}
GENETIC_CASES = {
    "FTD-M02", "FTD-M04", "FTD-M07", "FTD-M08",
    "FTD-P01", "FTD-P02", "FTD-P03", "FTD-P04", "FTD-P05", "FTD-P07", "FTD-P08",
    "FTD-S01", "FTD-S03", "FTD-S05", "FTD-S07", "FTD-S08", "FTD-S10",
}

PRIMARY_REPLACEMENTS = {
    "FTD-M02": "Behavioral variant frontotemporal dementia (bvFTD), probable, familial, with ALS in a first-degree relative",
    "FTD-P01": "Behavioral variant frontotemporal dementia (bvFTD), probable, with subtle structural imaging and a suggestive family history",
    "FTD-P02": "Behavioral variant frontotemporal dementia (bvFTD), probable, young-onset, previously misdiagnosed as a psychiatric disorder",
    "FTD-P03": "Behavioral variant frontotemporal dementia (bvFTD), probable, with comorbid major depressive disorder",
    "FTD-P04": "Behavioral variant frontotemporal dementia (bvFTD), probable, with co-existing Parkinson's disease",
    "FTD-P05": "Behavioral variant frontotemporal dementia (bvFTD), probable, young-onset, with high cognitive reserve and minimal structural change",
    "FTD-P07": "Behavioral variant frontotemporal dementia (bvFTD), probable, familial",
    "FTD-P06": "Behavioral variant frontotemporal dementia (bvFTD), probable, with concurrent small-vessel cerebrovascular disease",
    "FTD-S03": "Behavioral variant frontotemporal dementia (bvFTD), probable, familial",
    "FTD-S05": "Behavioral variant frontotemporal dementia (bvFTD), probable, familial",
    "FTD-S07": "Behavioral variant frontotemporal dementia (bvFTD), probable, familial",
    "FTD-S10": "Behavioral variant frontotemporal dementia (bvFTD), probable, familial",
}


def _normal_lab(test: str, value: Any, unit: str, reference: str) -> dict[str, Any]:
    return {"test": test, "value": value, "unit": unit, "reference_range": reference,
            "is_abnormal": False, "clinical_significance": None}


def _complete_labs(case: dict[str, Any]) -> None:
    panels = case["initial_tool_outputs"]["labs"].setdefault("panels", {})
    blob = json.dumps(panels).lower()
    for name, result in {
        "ESR": _normal_lab("ESR", 11, "mm/h", "0-20"),
        "CRP": _normal_lab("CRP", 1.6, "mg/L", "<3.0"),
    }.items():
        if name.lower() not in blob:
            panels.setdefault("Reviewed_FTD_panel_additions", []).append(result)


def _all_reports(case: dict[str, Any], tool: str, initial_key: str) -> list[dict[str, Any]]:
    reports = []
    initial = case["initial_tool_outputs"].get(initial_key)
    if initial:
        reports.append(initial)
    reports.extend(
        row["output"] for row in case["followup_outputs"]
        if row.get("tool_name") == tool and row.get("output")
    )
    return reports


def _advanced_kind(report: dict[str, Any]) -> str:
    blob = (str(report.get("modality", "")) + " " + str(report.get("impression", ""))).lower()
    if "datscan" in blob or "dopamine transporter" in blob:
        return "DaTscan"
    if "amyloid" in blob:
        return "amyloid_PET"
    if "tau pet" in blob or "flortaucipir" in blob:
        return "tau_PET"
    if "fdg" in blob or "hypometab" in blob:
        return "FDG_PET"
    return str(report.get("modality", ""))


def _special_kind(report: dict[str, Any]) -> str:
    blob = (str(report.get("test_type", "")) + " " + str(report.get("impression", ""))).lower()
    if "genetic" in blob or "c9orf" in blob or "pathogenic variant" in blob:
        return "genetic_panel:ALS" if "als" in str(report.get("test_type", "")).lower() else "genetic_panel:FTD"
    if "respir" in blob or "forced vital" in blob:
        return "respiratory_function"
    if "emg" in blob or "nerve conduction" in blob:
        return "emg_ncs"
    if "neuropsych" in blob or "cognitive" in blob or "social cognition" in blob:
        return "neuropsych_battery"
    return str(report.get("test_type", ""))


def _pick(reports: list[dict[str, Any]], kind: str, classify: Any) -> dict[str, Any]:
    matches = [json.loads(json.dumps(r)) for r in reports if classify(r) == kind]
    if not matches:
        raise ValueError(f"no authored {kind} report")
    # Prefer an actual positive/negative result over generic methodology prose.
    matches.sort(key=lambda r: any(
        marker in str(r.get("impression", "")).lower()
        for marker in ("abnormal values", "pathogenic", "no pathogenic", "all values within")
    ), reverse=True)
    return matches[0]


def _ct_report() -> dict[str, Any]:
    return {
        "findings": [
            {"type": "Cortical volume loss", "location": "Bilateral frontal and anterior temporal lobes",
             "size": "moderate", "density": None,
             "description": "Disproportionate widening of frontal and anterior temporal sulci with relative posterior preservation"},
            {"type": "White matter low attenuation", "location": "Periventricular, bilateral",
             "size": "mild", "density": "hypodense",
             "description": "Mild chronic small-vessel change without strategic infarct"},
        ],
        "contrast_used": False, "angiography_findings": None,
        "additional_observations": [
            "No haemorrhage, mass effect, hydrocephalus or large territorial infarct",
            "MRI was not completed because severe claustrophobia persisted despite preparation and the patient declined sedation",
            "CT is less sensitive than MRI for subtle regional atrophy, microbleeds and small-vessel disease",
        ],
        "impression": (
            "Non-contrast CT shows frontal and anterior-temporal-predominant volume loss with "
            "relative posterior preservation, supporting a frontotemporal neurodegenerative "
            "pattern. CT's lower sensitivity than MRI is explicitly acknowledged."
        ),
        "recommended_actions": [],
    }


def _to_spect(report: dict[str, Any]) -> dict[str, Any]:
    out = json.loads(json.dumps(report))
    out["modality"] = "perfusion_SPECT"
    out["tracer_or_protocol"] = "99mTc-HMPAO brain perfusion SPECT"
    for finding in out.get("findings", []):
        finding["signal"] = (finding.get("signal", "")
                             .replace("hypometabolism", "hypoperfusion")
                             .replace("hypometabolic", "hypoperfused")
                             .replace("metabolism", "perfusion"))
        finding["description"] = "Brain perfusion SPECT map"
    out["impression"] = (out.get("impression", "")
                         .replace("hypometabolism", "hypoperfusion")
                         .replace("hypometabolic", "hypoperfused"))
    return out


def _rebuild_specialized(case: dict[str, Any], reports: list[dict[str, Any]]) -> None:
    case_id = case["case_id"]
    rows = [r for r in case["followup_outputs"] if r.get("tool_name") != "order_specialized_test"]
    case["initial_tool_outputs"].pop("specialized_test", None)

    neuro = _pick(reports, "neuropsych_battery", _special_kind)
    neuro["test_type"] = "neuropsych_battery"
    rows.append({"trigger_action": "request_reviewed_neuropsych_battery", "tool_name": "order_specialized_test",
                 "tool_parameters": {"test_type": "neuropsych_battery"}, "output": neuro})

    if case_id in GENETIC_CASES:
        kind = "genetic_panel:ALS" if case_id == "FTD-P08" else "genetic_panel:FTD"
        genetic = _pick(reports, kind, _special_kind)
        genetic["test_type"] = kind
        impression = str(genetic.get("impression", ""))
        if not any(x in impression.lower() for x in ("pathogenic", "no pathogenic", "all values within")):
            genetic["impression"] = (
                "No pathogenic or likely pathogenic variant detected in C9orf72, GRN or MAPT; "
                "a negative panel does not exclude frontotemporal dementia."
            )
        rows.append({"trigger_action": "request_optional_counselled_ftd_genetics", "tool_name": "order_specialized_test",
                     "tool_parameters": {"test_type": kind}, "output": genetic})

    if case_id == "FTD-P08":
        for kind in ("emg_ncs", "respiratory_function"):
            report = _pick(reports, kind, _special_kind)
            report["test_type"] = kind
            rows.append({"trigger_action": f"request_ftd_mnd_{kind}", "tool_name": "order_specialized_test",
                         "tool_parameters": {"test_type": kind}, "output": report})
    case["followup_outputs"] = rows


def _rebuild_advanced(case: dict[str, Any], reports: list[dict[str, Any]]) -> None:
    case_id = case["case_id"]
    rows = [r for r in case["followup_outputs"] if r.get("tool_name") != "order_advanced_imaging"]
    case["initial_tool_outputs"].pop("advanced_imaging", None)

    fdg = _pick(reports, "FDG_PET", _advanced_kind)
    modality = "perfusion_SPECT" if case_id == SPECT_CASE else "FDG_PET"
    fdg = _to_spect(fdg) if case_id == SPECT_CASE else fdg
    fdg["modality"] = modality
    rows.append({"trigger_action": f"request_optional_{modality.lower()}", "tool_name": "order_advanced_imaging",
                 "tool_parameters": {"modality": modality}, "output": fdg})

    if case_id in AMYLOID_CASES:
        amyloid = _pick(reports, "amyloid_PET", _advanced_kind)
        amyloid["modality"] = "amyloid_PET"
        rows.append({"trigger_action": "request_optional_amyloid_pet_for_ad_differential", "tool_name": "order_advanced_imaging",
                     "tool_parameters": {"modality": "amyloid_PET"}, "output": amyloid})
    if case_id == "FTD-P04":
        dat = _pick(reports, "DaTscan", _advanced_kind)
        dat["modality"] = "DaTscan"
        rows.append({"trigger_action": "request_optional_datscan_for_coexisting_parkinsons", "tool_name": "order_advanced_imaging",
                     "tool_parameters": {"modality": "DaTscan"}, "output": dat})
    case["followup_outputs"] = rows


def _revise_actions(case: dict[str, Any]) -> None:
    case_id = case["case_id"]
    revised = []
    neuropsych = None
    genetic = None
    emg = respiratory = None
    for row in case["ground_truth"]["optimal_actions"]:
        tool = row.get("tool_name")
        params = row.get("tool_parameters", {})
        test = params.get("test_type")
        if tool == "order_advanced_imaging":
            continue
        if tool == "analyze_csf":
            if case_id != "FTD-M08":
                continue
            row["category"] = "required"
            row["tool_parameters"] = {"special_tests": ["HIV_RNA", "JCV_PCR", "cryptococcal_antigen"]}
            row["action"] = "Obtain targeted CSF HIV RNA, JC-virus PCR and cryptococcal antigen because this HIV-positive patient has a separate CNS-infection differential; this is not routine FTD biomarker testing"
        if tool == "order_specialized_test":
            if test == "neuropsych_battery":
                neuropsych = row
            elif isinstance(test, str) and test.startswith("genetic_panel:"):
                genetic = row
            elif test == "emg_ncs":
                emg = row
            elif test == "respiratory_function":
                respiratory = row
            continue
        if tool == "analyze_brain_mri" and case_id == CT_ALTERNATIVE_CASE:
            continue
        if tool == "analyze_brain_mri":
            use_contrast = bool(params.get("contrast")) or "T1_post_contrast" in params.get("sequences", [])
            row["tool_parameters"] = {"protocol": "dementia", "contrast": use_contrast}
        if tool == "order_ct_scan":
            row["tool_parameters"] = {"contrast": False}
        if tool == "interpret_labs":
            if "plasma_progranulin" in params.get("panels", []):
                row["category"] = "optional"
            else:
                targeted = []
                if case_id == "FTD-M08": targeted = ["HIV"]
                elif case_id == "FTD-M09": targeted = ["tox_screen", "BAL", "ammonia", "LFTs", "RPR"]
                elif case_id == "FTD-P08": targeted = ["CK", "LFTs"]
                row["tool_parameters"] = {"panels": CORE_LABS + targeted}
                row["category"] = "required"
        if tool == "perform_clinical_assessment":
            row["category"] = "required"
        revised.append(row)

    assert neuropsych is not None
    neuropsych["category"] = "required"
    neuropsych["tool_parameters"] = {"test_type": "neuropsych_battery"}
    revised.append(neuropsych)

    if case_id in GENETIC_CASES:
        assert genetic is not None
        genetic["category"] = "optional"
        genetic["action"] = "Offer an FTD/ALS gene panel after pre-test genetic counselling because of young onset or a suggestive pedigree; testing remains optional"
        revised.append(genetic)

    if case_id == "FTD-P08":
        assert emg is not None and respiratory is not None
        emg["category"] = "required"
        respiratory["category"] = "required"
        revised.extend((emg, respiratory))

    modality = "perfusion_SPECT" if case_id == SPECT_CASE else "FDG_PET"
    revised.append({
        "step": 0,
        "action": (
            "Use brain perfusion SPECT as the optional substitute when FDG-PET is unavailable and subtype remains uncertain"
            if modality == "perfusion_SPECT" else
            "Consider FDG-PET only after clinical assessment, labs and structural imaging if the dementia subtype remains uncertain"
        ),
        "tool_name": "order_advanced_imaging",
        "expected_finding": "Frontal and anterior-temporal dysfunction with relative posterior preservation, interpreted in clinical context",
        "category": "optional", "tool_parameters": {"modality": modality},
        "citation": "[NICE_NG97]", "guideline_source": "NICE_NG97",
    })
    if case_id in AMYLOID_CASES:
        revised.append({
            "step": 0, "action": "Consider amyloid PET only for the active Alzheimer-pathology differential; it is not routine FTD imaging",
            "tool_name": "order_advanced_imaging", "expected_finding": "Amyloid-negative result weighs against Alzheimer pathology",
            "category": "optional", "tool_parameters": {"modality": "amyloid_PET"},
            "citation": "[Amyloid_PET_AUC_2025]", "guideline_source": "Amyloid_PET_AUC_2025",
        })
    if case_id == "FTD-P04":
        revised.append({
            "step": 0, "action": "Consider DaTscan for the separate question of co-existing Parkinson's disease; it does not diagnose FTD",
            "tool_name": "order_advanced_imaging", "expected_finding": "Reduced striatal dopamine-transporter uptake supports the co-existing parkinsonian disorder",
            "category": "optional", "tool_parameters": {"modality": "DaTscan"},
            "citation": "[DLB_criteria_2017]", "guideline_source": "DLB_criteria_2017",
        })
    if case_id == CT_ALTERNATIVE_CASE and not any(r.get("tool_name") == "order_ct_scan" for r in revised):
        revised.append({
            "step": 0, "action": "Obtain non-contrast head CT as structural imaging because severe claustrophobia makes MRI unavailable; state CT's limitations",
            "tool_name": "order_ct_scan", "expected_finding": "Frontotemporal-predominant volume loss without mass, hydrocephalus or large infarct",
            "category": "required", "tool_parameters": {"contrast": False},
            "citation": "[NICE_NG97]", "guideline_source": "NICE_NG97",
        })
    case["ground_truth"]["optimal_actions"] = revised


def _revise_outputs(case: dict[str, Any]) -> None:
    advanced = _all_reports(case, "order_advanced_imaging", "advanced_imaging")
    specialized = _all_reports(case, "order_specialized_test", "specialized_test")
    _rebuild_specialized(case, specialized)
    _rebuild_advanced(case, advanced)

    case_id = case["case_id"]
    initial = case["initial_tool_outputs"]
    if case_id == CT_ALTERNATIVE_CASE:
        initial.pop("mri", None)
        initial["ct"] = _ct_report()
    elif not any(a.get("tool_name") == "order_ct_scan" for a in case["ground_truth"]["optimal_actions"]):
        initial.pop("ct", None)

    # Only the HIV case retains a case-authored CSF pathway.
    if case_id != "FTD-M08":
        initial.pop("csf", None)
        case["followup_outputs"] = [r for r in case["followup_outputs"] if r.get("tool_name") != "analyze_csf"]
    else:
        csf_rows = [r for r in case["followup_outputs"] if r.get("tool_name") == "analyze_csf"]
        if not csf_rows:
            raise ValueError("FTD-M08 missing authored HIV CSF report")
        chosen = next((r for r in csf_rows if "hiv" in r.get("trigger_action", "").lower()), csf_rows[0])
        chosen["tool_parameters"] = {
            "special_tests": ["HIV_RNA", "JCV_PCR", "cryptococcal_antigen"]
        }
        case["followup_outputs"] = [r for r in case["followup_outputs"] if r.get("tool_name") != "analyze_csf"] + [chosen]

    # These were unscored leftovers, not FTD investigations.
    case["followup_outputs"] = [
        r for r in case["followup_outputs"]
        if r.get("tool_name") not in {"order_cardiac_monitoring"}
    ]


def _revise_prose(case: dict[str, Any]) -> None:
    case_id = case["case_id"]
    gt = case["ground_truth"]
    if case_id in PRIMARY_REPLACEMENTS:
        gt["primary_diagnosis"] = PRIMARY_REPLACEMENTS[case_id]

    if case_id == CT_ALTERNATIVE_CASE:
        case.setdefault("metadata", {}).setdefault("panel_required_exemptions", {})["analyze_brain_mri"] = (
            "MRI is unavailable because severe claustrophobia persisted despite preparation and the patient declined sedation; required non-contrast CT is the structural alternative."
        )
        note = "Severe claustrophobia; unable to complete MRI despite preparation and declines sedation"
        pmh = case["patient"]["clinical_history"]["past_medical_history"]
        if note not in pmh:
            pmh.append(note)
        sentence = " He cannot tolerate MRI because of severe claustrophobia and has declined sedation."
        if sentence.strip() not in case["patient"]["history_present_illness"]:
            case["patient"]["history_present_illness"] += sentence
        gt["useless_tools"] = [r for r in gt.get("useless_tools", []) if r.get("tool_name") != "order_ct_scan"]
        if not any(r.get("tool_name") == "analyze_brain_mri" for r in gt.get("harmful_tools", [])):
            gt.setdefault("harmful_tools", []).append({
                "tool_name": "analyze_brain_mri", "tool_parameters": {},
                "rationale": "MRI is unavailable after failed preparation for severe claustrophobia and the patient declines sedation; use non-contrast CT and state its limitations",
                "citation": "[NICE_NG97]",
            })

    if case_id in {"FTD-P08"}:
        gt["useless_tools"] = [r for r in gt.get("useless_tools", []) if r.get("tool_name") != "order_specialized_test"]
    if case_id == "FTD-S12":
        gt["red_herrings"] = [
            row for row in gt.get("red_herrings", [])
            if row.get("field_path") != "initial_tool_outputs.ct.impression"
        ]
        for row in gt.get("red_herrings", []):
            if row.get("field_path") == "patient.clinical_history.past_medical_history[2]":
                row["location"] = "patient.clinical_history.past_medical_history[2]"
                row["correct_interpretation"] = (
                    "The prior TIA resolved completely four years before the current syndrome. "
                    "An 18-month progressive language decline is inconsistent with a fixed stroke "
                    "deficit; structural MRI shows the focal degenerative pattern."
                )

    exact = {
        "Advanced imaging (FDG-PET) is required when MRI is normal but clinical suspicion remains high":
            "FDG-PET is optional when MRI is normal and the subtype remains uncertain after the core assessment",
        "Genetic confirmation is required for the final diagnosis":
            "Genetic testing is optional after counselling and is not required for the clinical syndrome diagnosis",
        "MAPT mutations are tauopathies with heterogeneous phenotypes; tau PET aids characterisation.":
            "MAPT variants can cause inherited FTD, but optional counselled genetic testing — not tau PET — addresses the aetiological question in this case",
        "Vertical gaze palsy, axial rigidity, postural instability; tau PET can support if positive.":
            "Vertical gaze palsy, axial rigidity and early postural instability would support PSP; those clinical features are not present here",
        "Affected sibling shifts genetic testing from optional to required.":
            "An affected sibling strengthens the indication to offer genetic counselling and optional testing but does not make testing mandatory for the clinical diagnosis",
        "Differential biomarker test required; FDG and amyloid PET clarify.":
            "If the subtype remains uncertain after the core assessment, optional FDG-PET can clarify the regional functional pattern; amyloid PET is not routine in this case",
    }

    def walk(value: Any) -> Any:
        if isinstance(value, str):
            value = exact.get(value, value)
            value = value.replace("required FDG-PET", "optional FDG-PET")
            value = value.replace("FDG-PET is required", "FDG-PET is optional")
            value = value.replace("genetic testing is required", "genetic testing is optional after counselling")
            value = value.replace("genetic confirmation is load-bearing", "genetic testing is optional and informs aetiology and counselling")
            if case_id == CT_ALTERNATIVE_CASE:
                value = value.replace("frontotemporal atrophy on MRI", "frontotemporal-predominant volume loss on non-contrast CT")
                value = value.replace("MRI demonstrates", "Non-contrast CT demonstrates")
            return value
        if isinstance(value, list): return [walk(x) for x in value]
        if isinstance(value, dict): return {k: walk(v) for k, v in value.items()}
        return value
    case["ground_truth"] = walk(gt)

    metadata = case.setdefault("metadata", {})
    structural = "non-contrast CT because MRI is unavailable" if case_id == CT_ALTERNATIVE_CASE else "brain MRI"
    additions = ["optional perfusion SPECT" if case_id == SPECT_CASE else "optional FDG-PET"]
    if case_id in AMYLOID_CASES: additions.append("optional amyloid PET for an active AD differential")
    if case_id in GENETIC_CASES: additions.append("optional counselled genetic testing")
    if case_id == "FTD-P04": additions.append("optional DaTscan solely for co-existing Parkinson's disease")
    if case_id == "FTD-P08": additions.append("required EMG/NCS and respiratory testing for the motor-neuron-disease component")
    if case_id == "FTD-M08": additions.append("required targeted CSF testing for HIV CNS and opportunistic infection")
    actual = (
        f"Required core: structured behavioural/cognitive assessment with informant, validated "
        f"neuropsychological testing, targeted baseline labs, and {structural}. "
        + "Case-specific additions: " + "; ".join(additions) + "."
    )
    for key in ("difficulty_rationale", "difficulty_description", "clinical_notes"):
        if key in metadata or key == "difficulty_rationale": metadata[key] = actual
    metadata["revision_reason"] = (
        "Independent 2026-08-10 recheck of Reviewer 1: advanced imaging and genetics made "
        "optional, broad specialized studies removed, outputs and SFT pathway aligned"
    )
    metadata["case_body_concerns"] = []

    points = []
    for point in metadata.get("key_educational_points", []):
        lower = point.lower()
        if "tau pet" in lower: continue
        if (
            "genetic" in lower
            and not point.startswith("Genetic testing is optional")
            and any(word in lower for word in ("required", "mandat", "load-bearing"))
        ):
            point = "Genetic testing is optional after counselling and is targeted to young-onset or familial presentations"
        if "fdg" in lower and "required" in lower:
            point = point.replace("required", "optional").replace("Required", "Optional")
        points.append(point)
    if case_id in GENETIC_CASES:
        points.append("Genetic testing is optional after counselling and is not required to diagnose the clinical FTD syndrome")
    metadata["key_educational_points"] = list(dict.fromkeys(points))


def revise_case(case: dict[str, Any]) -> None:
    if case.get("condition") != "ftd": return
    _complete_labs(case)
    _revise_actions(case)
    _revise_outputs(case)
    _revise_prose(case)

    tools = {a.get("tool_name") for a in case["ground_truth"]["optimal_actions"] if a.get("tool_name")}
    constraints = []
    for row in case["ground_truth"].get("sequence_constraints", []):
        row = dict(row)
        if case["case_id"] == CT_ALTERNATIVE_CASE and row.get("before") == "analyze_brain_mri":
            row["before"] = "order_ct_scan"
        if row.get("before") in tools and row.get("after") in tools:
            constraints.append(row)
    case["ground_truth"]["sequence_constraints"] = constraints

    priority = {"perform_clinical_assessment": 10, "order_specialized_test": 20,
                "interpret_labs": 30, "analyze_brain_mri": 40, "order_ct_scan": 40,
                "order_advanced_imaging": 50, "analyze_csf": 60}
    actions = case["ground_truth"]["optimal_actions"]
    actions.sort(key=lambda r: (priority.get(r.get("tool_name"), 5 if r.get("tool_name") is None else 80), r.get("step", 0)))
    for step, row in enumerate(actions, 1): row["step"] = step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("FTD-*.json")):
        original = path.read_text(); case = json.loads(original); revise_case(case)
        rendered = json.dumps(case, indent=2, ensure_ascii=False) + "\n"
        if rendered != original:
            changed += 1
            if not args.check: path.write_text(rendered)
    print(f"FTD cases changed: {changed}")
    if args.check and changed: raise SystemExit(1)


if __name__ == "__main__": main()
