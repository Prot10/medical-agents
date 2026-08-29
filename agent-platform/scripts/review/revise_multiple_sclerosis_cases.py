"""Apply the July 2026 multiple-sclerosis review to cases and authored outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

# Optic-pathway testing is not a blanket MS panel.  These cases either present with
# optic neuritis or have an equivocal clinical/MRI picture where a subclinical optic
# lesion can answer a specific dissemination-in-space question.
OPTIC_NEURITIS = {
    "MS-RR-M04", "MS-RR-P04", "MS-RR-RS03",
    "MS-RR-S01", "MS-RR-S02", "MS-RR-S03", "MS-RR-S04", "MS-RR-S05",
}
EQUIVOCAL_FOR_VEP = {
    "MS-RR-M01", "MS-RR-M02", "MS-RR-M03", "MS-RR-P01", "MS-RR-P02", "MS-RR-P03",
}
VEP_CASES = OPTIC_NEURITIS | EQUIVOCAL_FOR_VEP
OCT_CASES = OPTIC_NEURITIS

# AQP4/MOG serology is targeted to optic-neuritis or atypical/tumefactive
# demyelination, rather than embedded in the baseline mimic panel in every case.
AQP_MOG_CASES = OPTIC_NEURITIS | {
    "MS-RR-RM01", "MS-RR-RM02", "MS-RR-RP01", "MS-RR-RP02", "MS-RR-RP03",
}

# CSF remains non-mandatory everywhere.  It is recommended only when the
# clinical/MRI picture is equivocal or atypical; in mass-effect cases the action
# explicitly requires imaging safety first.
CSF_RECOMMENDED = EQUIVOCAL_FOR_VEP | {
    "MS-RR-RM01", "MS-RR-RM02", "MS-RR-RP01", "MS-RR-RP02", "MS-RR-RP03",
}

BASE_LABS = ["CBC", "ESR", "CRP", "CMP", "calcium", "glucose", "TSH", "vitamin_B12", "HIV"]


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _all_specialized(case: dict[str, Any]) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    initial = case["initial_tool_outputs"].get("specialized_test")
    if initial:
        reports.append(initial)
    reports.extend(
        x["output"] for x in case["followup_outputs"]
        if x.get("tool_name") == "order_specialized_test" and x.get("output")
    )
    return reports


def _specialized_report(reports: list[dict[str, Any]], kind: str) -> dict[str, Any]:
    aliases = {"optical_coherence_tomography": {"oct", "optical_coherence_tomography"}, "vep": {"vep"}}
    report = next((x for x in reports if str(x.get("test_type", "")).lower() in aliases[kind]), None)
    if report is None:
        raise ValueError(f"Missing {kind} report")
    report = _copy(report)
    report["test_type"] = kind
    return report


def _is_aqp_mog(test: str) -> bool:
    low = test.lower()
    return any(token in low for token in ("aqp4", "aquaporin", "nmo-igg", "mog-igg", "mog antibody", "mog antibodies"))


def _filter_serology_from_labs(payload: dict[str, Any], keep: bool) -> None:
    if keep:
        return
    panels = payload.get("panels", {})
    for name in list(panels):
        panels[name] = [row for row in panels[name] if not _is_aqp_mog(str(row.get("test", "")))]
        if not panels[name]:
            del panels[name]
    summary = payload.get("abnormal_values_summary")
    if isinstance(summary, list):
        payload["abnormal_values_summary"] = [x for x in summary if not _is_aqp_mog(str(x))]


def _negative_serology() -> list[dict[str, Any]]:
    return [
        {"test": "Aquaporin-4 IgG (cell-based assay)", "value": "Negative", "unit": "",
         "reference_range": "Negative", "is_abnormal": False, "clinical_significance": None},
        {"test": "MOG-IgG (cell-based assay)", "value": "Negative", "unit": "",
         "reference_range": "Negative", "is_abnormal": False, "clinical_significance": None},
    ]


def _ensure_targeted_serology(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    labs = case["initial_tool_outputs"].get("labs")
    if not labs:
        raise ValueError(f"{cid}: required laboratory payload missing")
    _filter_serology_from_labs(labs, cid in AQP_MOG_CASES)
    if cid not in AQP_MOG_CASES:
        return
    tests = [str(row.get("test", "")) for values in labs.get("panels", {}).values() for row in values]
    missing = [row for row in _negative_serology() if not any(
        (_is_aqp_mog(test) and ("mog" in test.lower()) == ("mog" in row["test"].lower())) for test in tests
    )]
    if missing:
        labs.setdefault("panels", {}).setdefault("Targeted demyelinating serology", []).extend(missing)


def _rebuild_outputs(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    reports = _all_specialized(case)
    case["initial_tool_outputs"]["eeg"] = None
    case["initial_tool_outputs"]["ecg"] = None
    case["initial_tool_outputs"]["specialized_test"] = None

    rows = []
    for row in case["followup_outputs"]:
        tool = row.get("tool_name")
        trigger = str(row.get("trigger_action", "")).lower()
        if tool in {"analyze_eeg", "analyze_ecg", "order_specialized_test"}:
            continue
        if tool == "interpret_labs" and any(x in trigger for x in ("nmo_antib", "aqp4", "mog_antib")):
            continue
        if tool == "interpret_labs" and row.get("output"):
            _filter_serology_from_labs(row["output"], cid in AQP_MOG_CASES)
        rows.append(row)

    if cid in VEP_CASES:
        rows.append({"trigger_action": "request_visual_evoked_potentials", "tool_name": "order_specialized_test",
                     "tool_parameters": {"test_type": "vep"}, "output": _specialized_report(reports, "vep")})
    if cid in OCT_CASES:
        rows.append({"trigger_action": "request_optical_coherence_tomography", "tool_name": "order_specialized_test",
                     "tool_parameters": {"test_type": "optical_coherence_tomography"},
                     "output": _specialized_report(reports, "optical_coherence_tomography")})
    case["followup_outputs"] = rows
    _ensure_targeted_serology(case)


def _action(tool: str, category: str, params: dict[str, Any], text: str, finding: str) -> dict[str, Any]:
    return {"action": text, "tool_name": tool, "expected_finding": finding, "category": category,
            "tool_parameters": params, "citation": "[McDonald_2024]",
            "guideline_source": "2024 revised McDonald criteria; NICE NG220 (2026)"}


def _revise_actions(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    kept = []
    for row in case["ground_truth"]["optimal_actions"]:
        tool = row.get("tool_name")
        if tool in {"analyze_csf", "interpret_labs", "order_specialized_test", "analyze_eeg", "analyze_ecg"}:
            continue
        if tool == "analyze_brain_mri":
            row["category"] = "required"
            row["tool_parameters"] = {
                "protocol": "ms",
                "contrast": bool(row.get("tool_parameters", {}).get("contrast", True)),
            }
            row["action"] = ("Obtain brain MRI with a dedicated MS protocol, including MS-oriented FLAIR/T2/DWI and "
                             "pre/post-gadolinium T1 when clinically appropriate")
            row["citation"] = "[McDonald_2024]"
            row["guideline_source"] = "2024 revised McDonald criteria; MAGNIMS-CMSC-NAIMS 2024/2025"
        elif tool == "order_body_imaging" and row.get("tool_parameters", {}).get("study") == "spine_MRI":
            row["category"] = "required"
            row["tool_parameters"] = {
                "study": "spine_MRI",
                "contrast": bool(row.get("tool_parameters", {}).get("contrast", True)),
            }
            row["action"] = ("Obtain cervical and thoracic spinal-cord MRI with a dedicated MS protocol and "
                             "gadolinium when clinically appropriate")
            row["citation"] = "[McDonald_2024]"
            row["guideline_source"] = "2024 revised McDonald criteria; MAGNIMS-CMSC-NAIMS 2024/2025"
        kept.append(row)

    csf_category = "recommended" if cid in CSF_RECOMMENDED else "optional"
    safety = " after imaging excludes unsafe mass effect" if cid in {"MS-RR-RM01", "MS-RR-RM02", "MS-RR-RP01", "MS-RR-RP02", "MS-RR-RP03"} else ""
    kept.append(_action(
        "analyze_csf", csf_category,
        {"special_tests": ["oligoclonal_bands", "IgG_index", "kappa_free_light_chain_index"]},
        "Consider CSF analysis with paired serum" + safety + " only when clinical and MRI evidence is insufficient or a competing diagnosis remains",
        "CSF-restricted oligoclonal bands or an elevated kappa free-light-chain index can support the 2024 diagnostic pathway",
    ))
    panels = list(BASE_LABS)
    if cid in AQP_MOG_CASES:
        panels += ["AQP4_IgG_cell_based", "MOG_IgG_cell_based"]
    kept.append(_action(
        "interpret_labs", "required", {"panels": panels},
        "Order a mimic-exclusion laboratory panel; it supports exclusion of alternatives and does not confirm MS",
        "CBC, inflammatory markers, renal/liver function, calcium, glucose, thyroid function, vitamin B12 and HIV; targeted AQP4/MOG only when the phenotype is atypical",
    ))
    if cid in VEP_CASES:
        kept.append(_action(
            "order_specialized_test", "optional", {"test_type": "vep"},
            "Consider visual evoked potentials for this optic-neuritis or equivocal-dissemination question",
            "Delayed P100 latency may provide objective evidence of optic-pathway demyelination",
        ))
    if cid in OCT_CASES:
        kept.append(_action(
            "order_specialized_test", "optional", {"test_type": "optical_coherence_tomography"},
            "Consider OCT because this case has a specific optic-neuritis assessment question",
            "RNFL/ganglion-cell changes provide objective evidence of optic-nerve injury but do not independently confirm MS",
        ))
    for i, row in enumerate(kept, 1):
        row["step"] = i
    case["ground_truth"]["optimal_actions"] = kept


def _clean_reasoning(case: dict[str, Any]) -> None:
    gt = case["ground_truth"]
    gt["critical_actions"] = [
        text for text in gt.get("critical_actions", [])
        if not any(token in text.lower() for token in (
            "order csf", "obtain csf", "perform csf", "perform lumbar puncture", "order lumbar puncture",
            "order optical coherence", "obtain optical coherence", "order visual evoked", "obtain visual evoked",
        ))
    ]
    for field in ("critical_actions", "key_reasoning_points", "contraindicated_actions"):
        revised = []
        for text in gt.get(field, []):
            text = text.replace("McDonald 2017", "the 2024 revised McDonald")
            text = text.replace("per McDonald 2017", "under the 2024 revised McDonald criteria")
            revised.append(text)
        gt[field] = revised
    notes = [
        "July 2026 review applied end to end: brain and cervical/thoracic cord MRI use an MS protocol; CSF is conditional, never mandatory; OCT/VEP and AQP4/MOG testing answer selected optic or atypical questions rather than forming a blanket panel.",
        "The 2024 revised McDonald framework recognizes the optic nerve as a fifth topography and accepts the kappa free-light-chain index as an alternative positive-CSF marker; these additions do not make optic testing or lumbar puncture universal.",
    ]
    points = gt.setdefault("key_reasoning_points", [])
    for note in notes:
        if note not in points:
            points.append(note)
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = (
        "independent MS review: brain+cord MS-protocol MRI, conditional CSF with kFLC, targeted optic testing/serology, authored EEG/ECG removed"
    )


def revise(case: dict[str, Any]) -> None:
    _rebuild_outputs(case)
    _revise_actions(case)
    _clean_reasoning(case)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("MS-RR-*.json")):
        case = json.loads(path.read_text())
        before = json.dumps(case, sort_keys=True)
        revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check:
                path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"Multiple-sclerosis cases changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
