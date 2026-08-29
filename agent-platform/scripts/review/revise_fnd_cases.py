"""Keep FND as the frozen-size restraint probe with a positive clinical pathway."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

MRI_CASES = {
    "FND-M01", "FND-M02", "FND-M03", "FND-M05", "FND-M09", "FND-P01", "FND-P07", "FND-P08",
    "FND-RM02", "FND-RP03", "FND-RS02", "FND-RS04", "FND-S01", "FND-S02", "FND-S03", "FND-S04",
    "FND-S05", "FND-S06", "FND-S07", "FND-S10",
}
LAB_PANELS = {
    "FND-M01": ["glucose", "sodium", "calcium"],
    "FND-M02": ["glucose", "sodium", "calcium"],
    "FND-M03": ["glucose", "sodium", "calcium"],
    "FND-M05": ["CBC", "CMP", "ESR", "CRP", "complement C3/C4"],
    "FND-M06": ["CMP", "AED_levels"],
    "FND-M09": ["CBC", "CMP"],
    "FND-P08": ["glucose", "CMP"],
    "FND-RM03": ["CMP", "sodium", "serum_osmolality", "urine_osmolality"],
    "FND-RP02": ["CBC", "CMP", "magnesium", "phosphate", "thiamine_B1"],
    "FND-RP03": ["CBC", "CMP", "ESR", "CRP"],
    "FND-RS01": ["CBC", "CMP", "magnesium", "phosphate", "thiamine_B1"],
    "FND-S09": ["CMP", "magnesium", "thiamine_B1"],
}


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _reports(case: dict[str, Any], tool: str, key: str) -> list[dict[str, Any]]:
    rows = []
    if case["initial_tool_outputs"].get(key): rows.append(case["initial_tool_outputs"][key])
    rows.extend(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool and x.get("output"))
    return rows


def _best(case: dict[str, Any], tool: str, key: str) -> dict[str, Any]:
    rows = _reports(case, tool, key)
    if not rows: raise ValueError(f"{case['case_id']}: missing {tool}")
    return _copy(max(rows, key=lambda x: len(json.dumps(x))))


def _rebuild_outputs(case: dict[str, Any], eeg_selected: bool) -> None:
    cid = case["case_id"]; initial = case["initial_tool_outputs"]
    initial["mri"] = _best(case, "analyze_brain_mri", "mri") if cid in MRI_CASES else None
    initial["eeg"] = _best(case, "analyze_eeg", "eeg") if eeg_selected else None
    initial["labs"] = _best(case, "interpret_labs", "labs") if cid in LAB_PANELS else None
    initial["ecg"] = None; initial["csf"] = None; initial["specialized_test"] = None
    initial["echo"] = None; initial["cardiac_monitoring"] = None; initial["advanced_imaging"] = None
    case["followup_outputs"] = [x for x in case["followup_outputs"] if x.get("tool_name") in
                                {"search_medical_literature", "check_drug_interactions"}]


def _action(tool: str, params: dict[str, Any], text: str, finding: str, category: str = "optional") -> dict[str, Any]:
    return {"action": text, "tool_name": tool, "expected_finding": finding, "category": category,
            "tool_parameters": params, "citation": "[AAN_Functional_Seizures_2025]",
            "guideline_source": "positive FND signs; AAN functional seizures guideline 2025"}


def _revise_actions(case: dict[str, Any], eeg_selected: bool) -> None:
    cid = case["case_id"]; gt = case["ground_truth"]
    treatment = [x["action"] for x in gt["optimal_actions"] if x.get("tool_name") is None]
    for text in treatment:
        if text not in gt.setdefault("critical_actions", []): gt["critical_actions"].append(text)
    removed = {None, "perform_clinical_assessment", "analyze_brain_mri", "analyze_eeg", "analyze_ecg", "analyze_csf",
               "interpret_labs", "order_specialized_test", "order_body_imaging", "order_echocardiogram",
               "order_cardiac_monitoring", "order_advanced_imaging"}
    kept = [x for x in gt["optimal_actions"] if x.get("tool_name") not in removed]
    kept.append(_action(
        "perform_clinical_assessment", {"assessment_type": "functional_neuro_signs"},
        "Perform and document a positive FND examination: internal inconsistency/incongruity, Hoover sign, entrainment/distractibility or positive functional-seizure semiology as appropriate",
        "Positive rule-in signs establish FND; symptoms are real and involuntary, and psychological stress is not a required diagnostic criterion", "required"))
    if cid in MRI_CASES:
        kept.append(_action("analyze_brain_mri", {"protocol": "standard", "contrast": False},
                            "Consider MRI only for the explicit first focal deficit, acute red flag or competing organic neurological disease in this case",
                            "Exclude the named structural mimic; a normal scan does not itself diagnose FND"))
    if eeg_selected:
        kept.append(_action("analyze_eeg", {"eeg_type": "video"},
                            "Consider video-EEG capture of a typical event when epilepsy versus functional seizure remains ambiguous",
                            "Typical clinical event without an epileptic ictal correlate, interpreted together with semiology; interictal normality alone is insufficient"))
    if cid in LAB_PANELS:
        kept.append(_action("interpret_labs", {"panels": LAB_PANELS[cid]},
                            "Consider only case-targeted blood tests for the named metabolic, inflammatory, nutritional or treatment-related mimic",
                            "Answer the specific alternative diagnosis; normal blood tests do not establish FND"))
    for i, row in enumerate(kept, 1): row["step"] = i
    gt["optimal_actions"] = kept


def _clean(case: dict[str, Any]) -> None:
    gt = case["ground_truth"]
    note = ("Interim composition decision, August 2026: FND remains only to keep the frozen dataset at 20 conditions/600 cases. "
            "The positive functional-neurological examination is the sole required diagnostic act; every instrumental test is optional and case-targeted. "
            "DLB remains the preferred future replacement when composition work resumes.")
    if note not in gt.setdefault("key_reasoning_points", []): gt["key_reasoning_points"].append(note)
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = "FND interim reviewer option: positive clinical diagnosis required; every instrumental test optional and selected for explicit red flags"


def revise(case: dict[str, Any]) -> None:
    eeg_selected = any(x.get("tool_name") == "analyze_eeg" for x in case["ground_truth"]["optimal_actions"])
    _rebuild_outputs(case, eeg_selected); _revise_actions(case, eeg_selected); _clean(case)


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--cases", type=Path, default=DEFAULT_CASES); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("FND-*.json")):
        case = json.loads(path.read_text()); before = json.dumps(case, sort_keys=True); revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check: path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"FND cases changed: {changed}")
    if args.check and changed: raise SystemExit(1)


if __name__ == "__main__": main()
