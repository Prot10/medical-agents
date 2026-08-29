"""Apply the July 2026 focal temporal epilepsy review end to end."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"
CT_ALTERNATIVE_CASE = "FEPI-TEMP-P04"

ROUTINE_CASES = {
    "FEPI-TEMP-M01", "FEPI-TEMP-M02", "FEPI-TEMP-M03", "FEPI-TEMP-M04", "FEPI-TEMP-M05",
    "FEPI-TEMP-P01", "FEPI-TEMP-P05", "FEPI-TEMP-RM01", "FEPI-TEMP-RM02", "FEPI-TEMP-RM03",
    "FEPI-TEMP-RM04", "FEPI-TEMP-RP02", "FEPI-TEMP-RP03", "FEPI-TEMP-RP05",
    "FEPI-TEMP-RS02", "FEPI-TEMP-RS03", "FEPI-TEMP-RS05",
    "FEPI-TEMP-S01", "FEPI-TEMP-S02", "FEPI-TEMP-S03", "FEPI-TEMP-S04", "FEPI-TEMP-S05", "FEPI-TEMP-S06",
}
VIDEO_CASES = {
    "FEPI-TEMP-M05", "FEPI-TEMP-P01", "FEPI-TEMP-P02", "FEPI-TEMP-P03", "FEPI-TEMP-P04",
    "FEPI-TEMP-P05", "FEPI-TEMP-RP04", "FEPI-TEMP-RP05", "FEPI-TEMP-RS01", "FEPI-TEMP-RS04",
}
SLEEP_DEPRIVED_CASES = {"FEPI-TEMP-M01", "FEPI-TEMP-M02", "FEPI-TEMP-M03", "FEPI-TEMP-RM01", "FEPI-TEMP-RP02"}
AMBULATORY_CASES = {"FEPI-TEMP-M03", "FEPI-TEMP-RP02"}
CONTINUOUS_CASES = {"FEPI-TEMP-RP01"}

LAB_CASES = {
    "FEPI-TEMP-M01", "FEPI-TEMP-M02", "FEPI-TEMP-M03", "FEPI-TEMP-M04",
    "FEPI-TEMP-P02", "FEPI-TEMP-P05", "FEPI-TEMP-RM01", "FEPI-TEMP-RM02", "FEPI-TEMP-RM03", "FEPI-TEMP-RM04",
    "FEPI-TEMP-RP01", "FEPI-TEMP-RP02", "FEPI-TEMP-RP03", "FEPI-TEMP-RP05",
    "FEPI-TEMP-RS02", "FEPI-TEMP-RS03", "FEPI-TEMP-RS05",
    "FEPI-TEMP-S01", "FEPI-TEMP-S02", "FEPI-TEMP-S03", "FEPI-TEMP-S04", "FEPI-TEMP-S05", "FEPI-TEMP-S06",
}

ECG_CASES = {
    "FEPI-TEMP-M01", "FEPI-TEMP-M02", "FEPI-TEMP-M03", "FEPI-TEMP-M04", "FEPI-TEMP-M05",
    "FEPI-TEMP-P01", "FEPI-TEMP-P02", "FEPI-TEMP-P05", "FEPI-TEMP-RM03", "FEPI-TEMP-RM04",
    "FEPI-TEMP-RP02", "FEPI-TEMP-RP03", "FEPI-TEMP-RP05", "FEPI-TEMP-RS02", "FEPI-TEMP-RS05",
    "FEPI-TEMP-S01", "FEPI-TEMP-S02", "FEPI-TEMP-S03", "FEPI-TEMP-S04", "FEPI-TEMP-S05", "FEPI-TEMP-S06",
}

NEUROPSYCH_CASES = {
    "FEPI-TEMP-M05", "FEPI-TEMP-P01", "FEPI-TEMP-P04", "FEPI-TEMP-RP04", "FEPI-TEMP-RP05", "FEPI-TEMP-RS04",
}


def _all_reports(case: dict[str, Any], tool: str, initial_key: str) -> list[dict[str, Any]]:
    reports = []
    if case["initial_tool_outputs"].get(initial_key):
        reports.append(case["initial_tool_outputs"][initial_key])
    reports.extend(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool and x.get("output"))
    return reports


def _copy(report: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(report))


def _routine(reports: list[dict[str, Any]]) -> dict[str, Any]:
    report = _copy(reports[0]); report["eeg_type"] = "routine"
    return report


def _prolonged(reports: list[dict[str, Any]]) -> dict[str, Any]:
    report = next((r for r in reports if "video" in str(r.get("impression", "")).lower()), reports[-1])
    return _copy(report)


def _sleep_report(reports: list[dict[str, Any]], cid: str) -> dict[str, Any]:
    source = _prolonged(reports)
    lateral = "left" if "left" in str(source.get("impression", "")).lower() else "right"
    positive = cid not in {"FEPI-TEMP-M03", "FEPI-TEMP-RP02"}
    source["eeg_type"] = "sleep_deprived"
    source["findings"] = ([{
        "type": "Interictal epileptiform discharges", "location": f"{lateral.title()} anterior temporal",
        "frequency": "Activated during drowsiness and NREM sleep", "morphology": "Sharp waves with aftergoing slow wave",
        "state": "Sleep after partial sleep deprivation", "clinical_correlation": "Supports a focal temporal epileptogenic region",
    }] if positive else [])
    source["impression"] = (
        f"Abnormal sleep-deprived EEG with {lateral} anterior temporal epileptiform discharges activated in sleep; no seizure captured."
        if positive else
        "Normal sleep-deprived EEG with adequate NREM sleep captured; no epileptiform discharge or seizure. A normal study does not exclude epilepsy."
    )
    return source


def _long_report(reports: list[dict[str, Any]], kind: str) -> dict[str, Any]:
    report = _prolonged(reports); report["eeg_type"] = kind
    if kind == "ambulatory":
        report["impression"] = str(report.get("impression", "")).replace("continuous video-EEG monitoring", "48-hour ambulatory EEG")
        report["impression"] = report["impression"].replace("72-hour", "48-hour").replace("96-hour", "48-hour")
    elif kind == "continuous_icu":
        report["impression"] = str(report.get("impression", "")).replace("prolonged video-EEG", "continuous ICU EEG")
    return report


def _normal_ecg() -> dict[str, Any]:
    return {"rhythm": "Normal sinus rhythm", "rate": 76,
            "intervals": {"PR": "154 ms", "QRS": "86 ms", "QTc": "416 ms"},
            "axis": "Normal", "findings": ["No pre-excitation, Brugada pattern, long-QT or conduction block"],
            "interpretation": "Normal 12-lead ECG; no cardiac substrate identified to explain transient loss of consciousness.",
            "clinical_correlation": "ECG evaluates a seizure mimic and does not diagnose epilepsy."}


def _ct_alternative() -> dict[str, Any]:
    return {"findings": [], "contrast_used": False, "angiography_findings": None,
            "additional_observations": [
                "No haemorrhage, mass, hydrocephalus, large infarct or calcified epileptogenic lesion",
                "MRI was not completed because severe claustrophobia persisted despite preparation and the patient declined sedation",
                "CT cannot exclude hippocampal sclerosis or subtle focal cortical dysplasia",
            ],
            "impression": "No structural lesion identified on non-contrast CT. This remains MRI-negative focal epilepsy; CT has lower sensitivity for subtle epileptogenic lesions.",
            "recommended_actions": []}


def _pe_report() -> dict[str, Any]:
    return {"region": "chest", "modality": "CT angiography", "contrast": True,
            "findings": [
                {"type": "Pulmonary arterial filling defects", "location": "Bilateral segmental lower-lobe pulmonary arteries",
                 "description": "Acute emboli without saddle embolus", "density": "contrast filling defect"},
                {"type": "Right heart", "location": "Cardiac chambers", "description": "No CT evidence of right-heart strain", "density": "soft tissue"},
            ],
            "measurements": {"RV/LV ratio": "0.8"},
            "impression": "Acute bilateral segmental pulmonary emboli without CT right-heart strain; treat in parallel with the independent focal epilepsy.",
            "recommended_actions": []}


def _panels(case: dict[str, Any], existing: dict[str, Any] | None) -> list[str]:
    cid = case["case_id"]
    if cid == "FEPI-TEMP-P02": return ["CMP", "sodium"]
    if cid == "FEPI-TEMP-RP01": return ["CBC", "CMP", "CRP", "glucose", "sodium"]
    if cid == "FEPI-TEMP-RP02": return ["CBC", "CMP", "D_dimer", "troponin", "BNP"]
    if cid == "FEPI-TEMP-RS02": return ["CMP", "glucose", "sodium"]
    old = (existing or {}).get("tool_parameters", {}).get("panels", [])
    if "AED_levels" in old:
        return [x for x in old if x in {"CMP", "AED_levels", "tox_screen", "sodium"}]
    return ["glucose", "sodium", "calcium"]


def _rebuild_outputs(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    eeg = _all_reports(case, "analyze_eeg", "eeg")
    ecg = _all_reports(case, "analyze_ecg", "ecg")
    specialized = _all_reports(case, "order_specialized_test", "specialized_test")
    rows = [x for x in case["followup_outputs"] if x.get("tool_name") not in {
        "analyze_eeg", "analyze_brain_mri", "analyze_ecg", "order_echocardiogram",
        "order_cardiac_monitoring", "order_specialized_test", "order_ct_scan", "order_body_imaging",
    }]
    case["initial_tool_outputs"].pop("eeg", None)
    case["initial_tool_outputs"].pop("ecg", None)
    case["initial_tool_outputs"].pop("echo", None)
    case["initial_tool_outputs"].pop("cardiac_monitoring", None)
    case["initial_tool_outputs"].pop("specialized_test", None)

    if cid in ROUTINE_CASES:
        case["initial_tool_outputs"]["eeg"] = _routine(eeg)
    for kind, selected in (("sleep_deprived", SLEEP_DEPRIVED_CASES), ("ambulatory", AMBULATORY_CASES),
                           ("video", VIDEO_CASES), ("continuous_icu", CONTINUOUS_CASES)):
        if cid not in selected: continue
        report = _sleep_report(eeg, cid) if kind == "sleep_deprived" else _long_report(eeg, kind)
        rows.append({"trigger_action": f"request_{kind}_eeg", "tool_name": "analyze_eeg",
                     "tool_parameters": {"eeg_type": kind}, "output": report})

    if cid in ECG_CASES:
        case["initial_tool_outputs"]["ecg"] = _copy(ecg[0]) if ecg else _normal_ecg()

    if cid == CT_ALTERNATIVE_CASE:
        case["initial_tool_outputs"].pop("mri", None)
        case["initial_tool_outputs"]["ct"] = _ct_alternative()
    else:
        case["initial_tool_outputs"].pop("ct", None)
    if cid == "FEPI-TEMP-RP05":
        old_ct = next((x for x in case["followup_outputs"] if x.get("tool_name") == "order_ct_scan"), None)
        if old_ct:
            old_ct = _copy(old_ct); old_ct["tool_parameters"] = {"contrast": False}; rows.append(old_ct)

    if cid in NEUROPSYCH_CASES:
        report = next((_copy(x) for x in specialized if x.get("test_type") == "neuropsych_battery"), None)
        if report is None: raise ValueError(f"{cid}: missing neuropsych report")
        report["test_type"] = "neuropsych_battery"
        rows.append({"trigger_action": "request_neuropsych_for_surgical_evaluation", "tool_name": "order_specialized_test",
                     "tool_parameters": {"test_type": "neuropsych_battery"}, "output": report})
    if cid == "FEPI-TEMP-RP02":
        rows.append({"trigger_action": "request_urgent_ctpa_for_pe", "tool_name": "order_body_imaging",
                     "tool_parameters": {"study": "chest_CTA", "contrast": True}, "output": _pe_report()})
    case["followup_outputs"] = rows


def _action(tool: str, category: str, params: dict[str, Any], text: str, finding: str) -> dict[str, Any]:
    return {"action": text, "tool_name": tool, "expected_finding": finding, "category": category,
            "tool_parameters": params, "citation": "[NICE_NG217_2025]", "guideline_source": "NICE_NG217_2025"}


def _revise_actions(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    existing_lab = next((x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == "interpret_labs"), None)
    kept = []
    for row in case["ground_truth"]["optimal_actions"]:
        tool = row.get("tool_name")
        if tool in {"analyze_eeg", "interpret_labs", "analyze_ecg", "order_echocardiogram",
                    "order_cardiac_monitoring", "order_specialized_test", "order_body_imaging"}:
            continue
        if tool == "analyze_brain_mri":
            if cid == CT_ALTERNATIVE_CASE: continue
            row["category"] = "required"
            row["tool_parameters"] = {"protocol": "epilepsy", "contrast": bool(row.get("tool_parameters", {}).get("contrast"))}
            row["action"] = "Obtain brain MRI using a dedicated epilepsy protocol to identify a structural epileptogenic cause"
        if tool == "order_ct_scan":
            if cid != "FEPI-TEMP-RP05": continue
            row["tool_parameters"] = {"contrast": False}; row["category"] = "recommended"
        kept.append(row)

    if cid == CT_ALTERNATIVE_CASE:
        kept.append(_action("order_ct_scan", "required", {"contrast": False},
                            "Use non-contrast head CT because MRI is unavailable from severe claustrophobia",
                            "Exclude a gross structural lesion while explicitly acknowledging that CT cannot exclude subtle dysplasia or hippocampal sclerosis"))
    if cid in ROUTINE_CASES:
        kept.append(_action("analyze_eeg", "required", {"eeg_type": "routine"},
                            "Obtain an awake routine EEG promptly to support classification; never use a normal result to exclude epilepsy",
                            "Interictal focal temporal discharges may support the clinical diagnosis"))
    if cid in SLEEP_DEPRIVED_CASES:
        kept.append(_action("analyze_eeg", "recommended", {"eeg_type": "sleep_deprived"},
                            "Because the routine recording is normal or equivocal, consider a sleep-deprived EEG after discussing risks and benefits",
                            "Sleep may activate focal temporal epileptiform discharges"))
    if cid in AMBULATORY_CASES:
        kept.append(_action("analyze_eeg", "recommended", {"eeg_type": "ambulatory"},
                            "Because routine and sleep-deprived studies remain non-diagnostic, consider ambulatory EEG to capture a habitual event",
                            "Electroclinical temporal-onset event during prolonged ambulatory recording"))
    if cid in VIDEO_CASES:
        kept.append(_action("analyze_eeg", "required", {"eeg_type": "video"},
                            "Use prolonged video-EEG because habitual events must be captured or presurgical/PNES localization is required",
                            "Concordant electroclinical event or absence of ictal correlate for PNES"))
    if cid in CONTINUOUS_CASES:
        kept.append(_action("analyze_eeg", "required", {"eeg_type": "continuous_icu"},
                            "Use continuous ICU EEG for suspected non-convulsive status epilepticus; this is the acute exception, not routine TLE workup",
                            "Ongoing right temporal electrographic seizures requiring urgent treatment"))
    if cid in LAB_CASES:
        kept.append(_action("interpret_labs", "optional", {"panels": _panels(case, existing_lab)},
                            "Order only case-targeted tests for an acute symptomatic seizure, metabolic mimic, drug level or concurrent emergency; do not use a fixed epilepsy panel",
                            "Answer the specific provocation or treatment question in this presentation"))
    if cid in ECG_CASES:
        kept.append(_action("analyze_ecg", "required", {},
                            "Obtain a 12-lead ECG in this first suspected seizure/transient-loss-of-consciousness assessment to identify a cardiac mimic",
                            "Identify or exclude pre-excitation, conduction disease, long-QT or Brugada pattern; ECG does not diagnose epilepsy"))
    if cid in NEUROPSYCH_CASES:
        kept.append(_action("order_specialized_test", "optional", {"test_type": "neuropsych_battery"},
                            "Consider neuropsychological testing for cognitive lateralization and surgical risk in this tertiary epilepsy evaluation",
                            "Memory and language lateralization relevant to resection planning"))
    if cid == "FEPI-TEMP-RP02":
        kept.append(_action("order_body_imaging", "required", {"study": "chest_CTA", "contrast": True},
                            "Obtain urgent CT pulmonary angiography for hemoptysis, dyspnoea and unilateral calf pain; address PE in parallel with epilepsy",
                            "Acute pulmonary emboli, a separate concurrent emergency"))
    for i, row in enumerate(kept, 1): row["step"] = i
    case["ground_truth"]["optimal_actions"] = kept


def _clean(case: dict[str, Any]) -> None:
    cid = case["case_id"]; gt = case["ground_truth"]
    removed = {"order_echocardiogram", "order_cardiac_monitoring"}
    gt["sequence_constraints"] = [x for x in gt.get("sequence_constraints", []) if x.get("before") not in removed and x.get("after") not in removed]
    gt["useless_tools"] = [x for x in gt.get("useless_tools", []) if x.get("tool_name") not in ({"order_ct_scan"} if cid in {CT_ALTERNATIVE_CASE, "FEPI-TEMP-RP05"} else set())]
    if cid in ECG_CASES:
        gt["useless_tools"] = [x for x in gt["useless_tools"] if x.get("tool_name") != "analyze_ecg"]
    for field in ("critical_actions", "key_reasoning_points", "contraindicated_actions"):
        gt[field] = [x for x in gt.get(field, []) if not any(t in str(x).lower() for t in ("echocardiogram", "holter", "tilt-table", "tilt table"))]
    review_note = "July 2026 review applied end to end: routine EEG first when appropriate, staged sleep-deprived/ambulatory escalation, video only for event capture or tertiary evaluation, and continuous ICU EEG only for NCSE."
    if review_note not in gt.setdefault("key_reasoning_points", []):
        gt["key_reasoning_points"].append(review_note)
    if cid == "FEPI-TEMP-RP02":
        gt["key_reasoning_points"] = [x.replace("Cardiac/cardiopulmonary workup is justified per case (PE/syncope differential) and is not 'useless' here.",
                                                      "Urgent chest CT angiography is justified for the concurrent PE; routine echocardiography and rhythm monitoring are not epilepsy tests.") for x in gt["key_reasoning_points"]]
    if cid == CT_ALTERNATIVE_CASE:
        for red in gt.get("red_herrings", []):
            if red.get("field_path") == "initial_tool_outputs.mri.impression":
                red["location"] = "history_present_illness"
                red["field_path"] = "patient.history_present_illness"
                red["data_point"] = "Previously reported normal standard and epilepsy-protocol MRI studies, which led the referring centre to a PNES label; current MRI is unavailable."
    if cid == "FEPI-TEMP-RP04":
        eeg_index = next(i for i, row in enumerate(case["followup_outputs"])
                         if row.get("tool_name") == "analyze_eeg" and row.get("output", {}).get("eeg_type") == "video")
        retained = []
        for red in gt.get("red_herrings", []):
            if str(red.get("field_path", "")).startswith("initial_tool_outputs.labs"):
                continue
            if red.get("field_path") == "initial_tool_outputs.eeg.findings[1]":
                red["location"] = "followup_outputs"
                red["field_path"] = f"followup_outputs[{eeg_index}].output.findings[1]"
            retained.append(red)
        gt["red_herrings"] = retained
    meta = case["metadata"]
    meta["last_revised"] = "2026-08-10"
    meta["revision_reason"] = "independent focal-epilepsy review: staged EEG pathway, dedicated structural imaging, targeted labs/ECG, cardiac tools removed"
    if cid == CT_ALTERNATIVE_CASE:
        meta.setdefault("panel_required_exemptions", {})["analyze_brain_mri"] = "MRI unavailable because severe claustrophobia persisted and sedation was declined; CT is the reviewed structural alternative."
        hpi = case["patient"]["history_present_illness"]
        if "severe claustrophobia" not in hpi.lower():
            case["patient"]["history_present_illness"] = hpi + " She has severe claustrophobia, could not complete MRI despite preparation, and declined sedation; non-contrast CT was accepted instead."


def revise(case: dict[str, Any]) -> None:
    _rebuild_outputs(case)
    if case["case_id"] not in LAB_CASES: case["initial_tool_outputs"].pop("labs", None)
    case["followup_outputs"] = [x for x in case["followup_outputs"] if x.get("tool_name") != "interpret_labs"]
    _revise_actions(case); _clean(case)


def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES); p.add_argument("--check", action="store_true")
    args = p.parse_args(); rendered = []
    for path in sorted(args.cases_dir.glob("FEPI-TEMP-*.json")):
        case = json.loads(path.read_text()); revise(case); rendered.append((path, json.dumps(case, indent=2, ensure_ascii=False) + "\n"))
    changed = sum(path.read_text() != text for path, text in rendered); print(f"Focal epilepsy cases changed: {changed}/{len(rendered)}")
    if args.check and changed: raise SystemExit(1)
    if not args.check:
        for path, text in rendered: path.write_text(text)


if __name__ == "__main__": main()
