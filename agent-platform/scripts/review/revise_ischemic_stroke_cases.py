"""Apply Reviewer 2's acute-stroke imaging/lab pathway without delaying reperfusion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"
PERFUSION_CASES = {"ISCH-STR-M03", "ISCH-STR-P04"}
EEG_CASES = {"ISCH-STR-RM01"}


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _action(tool: str, params: dict[str, Any], text: str, finding: str,
            category: str) -> dict[str, Any]:
    return {
        "action": text, "tool_name": tool, "expected_finding": finding,
        "category": category, "tool_parameters": params,
        "citation": "[AHA_ASA_Stroke_2026]", "guideline_source": "AHA/ASA acute ischemic stroke guideline 2026",
    }


def _reports(case: dict[str, Any], tool: str, key: str) -> list[dict[str, Any]]:
    rows = []
    if case["initial_tool_outputs"].get(key):
        rows.append(case["initial_tool_outputs"][key])
    rows.extend(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool and x.get("output"))
    return rows


def _best(case: dict[str, Any], tool: str, key: str) -> dict[str, Any]:
    rows = _reports(case, tool, key)
    if not rows:
        raise ValueError(f"{case['case_id']}: missing {tool}")
    return _copy(max(rows, key=lambda x: len(json.dumps(x))))


def _cta(case: dict[str, Any]) -> dict[str, Any]:
    rows = [
        x["output"] for x in case["followup_outputs"]
        if x.get("tool_name") == "order_ct_scan" and (
            "angiography" in x.get("trigger_action", "") or "cta" in x.get("trigger_action", "")
        )
    ]
    if not rows:
        raise ValueError(f"{case['case_id']}: required CTA has no report")
    return _copy(max(rows, key=lambda x: len(json.dumps(x))))


def _perfusion(case: dict[str, Any]) -> dict[str, Any] | None:
    rows = [
        x["output"] for x in case["followup_outputs"]
        if "perfusion" in x.get("trigger_action", "")
        and x.get("tool_name") in {"order_ct_scan", "order_advanced_imaging"}
    ]
    if not rows:
        return None
    source = _copy(max(rows, key=lambda x: len(json.dumps(x))))
    if source.get("modality"):
        source["modality"] = "CT_perfusion"
        return source
    findings = [
        {
            "region": str(row.get("location", row.get("type", "brain"))),
            "signal": str(row.get("size", "CT perfusion parameter abnormality")),
            "description": str(row.get("description", row.get("type", ""))),
        }
        for row in source.get("findings", [])
    ]
    return {
        "modality": "CT_perfusion",
        "tracer_or_protocol": "CT perfusion with automated CBF/CBV/MTT/Tmax analysis",
        "findings": findings,
        "quantitative_data": {},
        "impression": source.get("impression", ""),
        "recommended_actions": source.get("recommended_actions", []),
    }


def _rebuild_outputs(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    cta = _cta(case)
    perfusion = _perfusion(case)
    initial = case["initial_tool_outputs"]
    initial["mri"] = _best(case, "analyze_brain_mri", "mri")
    initial["eeg"] = _best(case, "analyze_eeg", "eeg") if cid in EEG_CASES else None
    initial["advanced_imaging"] = None

    kept = [
        row for row in case["followup_outputs"]
        if row.get("tool_name") not in {"order_ct_scan", "order_advanced_imaging", "analyze_brain_mri", "analyze_eeg"}
    ]
    kept.append({
        "trigger_action": "request_ct_angiography", "tool_name": "order_ct_scan",
        "tool_parameters": {"contrast": True, "angiography": True}, "output": cta,
    })
    if cid in PERFUSION_CASES:
        if perfusion is None:
            raise ValueError(f"{cid}: selected extended-window perfusion case has no report")
        kept.append({
            "trigger_action": "request_ct_perfusion", "tool_name": "order_advanced_imaging",
            "tool_parameters": {"modality": "CT_perfusion"}, "output": perfusion,
        })
    case["followup_outputs"] = kept


def _rebuild_actions(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    gt = case["ground_truth"]
    old = gt["optimal_actions"]
    for row in old:
        if row.get("tool_name") is None and row["action"] not in gt.setdefault("critical_actions", []):
            gt["critical_actions"].append(row["action"])

    # Preserve genuinely case-specific downstream work-up, but advanced vascular duplicates
    # are removed because the reviewed CTA already covers head/neck vessels.
    preserve = {
        "analyze_ecg", "order_echocardiogram", "order_cardiac_monitoring",
        "order_microbiology", "order_specialized_test", "check_drug_interactions",
        "search_medical_literature",
    }
    other = [_copy(row) for row in old if row.get("tool_name") in preserve]
    for row in other:
        if row.get("tool_name") == "search_medical_literature":
            row["category"] = "recommended"

    # Baseline laboratory action plus selected aetiological panels, explicitly later-phase.
    lab_actions = [row for row in old if row.get("tool_name") == "interpret_labs"]
    selected_labs = []
    for row in lab_actions:
        panels = row.get("tool_parameters", {}).get("panels", [])
        if any(x in panels for x in ("CBC", "BMP", "glucose", "troponin")):
            continue
        selected = _copy(row)
        selected["category"] = "recommended"
        prefix = "After reperfusion decisions, "
        tail = selected["action"]
        while tail.startswith(prefix):
            tail = tail[len(prefix):]
        selected["action"] = prefix + tail.lstrip().lower()
        selected_labs.append(selected)

    actions = [
        _action(
            "order_ct_scan", {"contrast": False, "angiography": False},
            "Obtain emergent noncontrast head CT first to exclude intracranial hemorrhage and assess ischemic burden before reperfusion therapy",
            "No hemorrhage; early ischemic change/ASPECTS may be normal or subtle. NCCT alone is sufficient for most thrombolysis decisions",
            "required",
        ),
        _action(
            "order_ct_scan", {"contrast": True, "angiography": True},
            "Obtain a separate rapid CTA of the cervical and intracranial vessels for large-vessel-occlusion assessment and thrombectomy planning; do not wait for serum creatinine",
            "Occlusion/stenosis/dissection anatomy or absence of an LVO; this is subsequent to and not a substitute for NCCT",
            "required",
        ),
        _action(
            "interpret_labs", {"panels": ["glucose", "CBC", "coagulation", "creatinine", "troponin"]},
            "Check glucose before thrombolysis and obtain CBC, coagulation, renal function and baseline troponin, but do not delay thrombolysis for routine results or CTA/CTP for creatinine",
            "Identify a glucose mimic and relevant safety abnormalities; baseline troponin/ECG do not delay reperfusion",
            "required",
        ),
        _action(
            "analyze_brain_mri", {"protocol": "stroke", "contrast": False},
            "Consider brain MRI only when immediately available without delaying reperfusion, especially for wake-up/unknown-onset stroke, posterior circulation, paediatric stroke or a difficult mimic",
            "DWI lesion with ADC reduction; DWI-FLAIR mismatch may support selected unknown-onset treatment. MRI is not routine mandatory imaging",
            "optional",
        ),
    ]
    if cid in PERFUSION_CASES:
        actions.append(_action(
            "order_advanced_imaging", {"modality": "CT_perfusion"},
            "Use automated CT perfusion for tissue-based selection in this wake-up/extended-window case only because it is immediately available and will not delay treatment",
            "Quantified ischemic core and salvageable penumbra/mismatch for extended-window thrombolysis or thrombectomy selection",
            "optional",
        ))
    if cid in EEG_CASES:
        actions.append(_action(
            "analyze_eeg", {"eeg_type": "routine"},
            "Consider EEG only because the involuntary tonic hand event creates a genuine seizure-mimic question; EEG must not delay reperfusion",
            "Epileptiform activity or its absence interpreted with the clinical event; EEG is not a routine stroke test",
            "optional",
        ))
    actions.extend(selected_labs)
    actions.extend(other)
    for i, row in enumerate(actions, 1):
        row["step"] = i
    gt["optimal_actions"] = actions
    gt["sequence_constraints"] = [
        {
            "before": "order_ct_scan", "after": "check_drug_interactions",
            "reason": "Review NCCT for hemorrhage while evaluating thrombolytic eligibility; routine laboratory, ECG, MRI and advanced imaging must not delay reperfusion.",
            "citation": "[AHA_ASA_Stroke_2026]", "severity": "hard",
        }
    ] if any(x.get("tool_name") == "check_drug_interactions" for x in actions) else []
    note = (
        "AHA/ASA 2026 sequencing: glucose is checked before thrombolysis, but routine CBC/coagulation "
        "results are not awaited without a reason to expect abnormality; ECG/troponin do not delay "
        "reperfusion, and CTA/CTP do not wait for creatinine."
    )
    if note not in gt.setdefault("key_reasoning_points", []):
        gt["key_reasoning_points"].append(note)


def revise(case: dict[str, Any]) -> None:
    _rebuild_outputs(case)
    _rebuild_actions(case)
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = (
        "Independent Reviewer 2 stroke audit: NCCT and CTA separated; MRI optional; CTP routed "
        "only to two extended-window cases; routine MRA/TCD/duplex duplication removed; acute labs "
        "carry explicit do-not-delay rules; EEG retained for one seizure-mimic case"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("ISCH-STR-*.json")):
        case = json.loads(path.read_text())
        before = json.dumps(case, sort_keys=True)
        revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check:
                path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"ischemic-stroke cases changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
