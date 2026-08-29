"""Apply the July 2026 migraine-with-aura review to actions and authored data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

# Imaging is selected by a concrete red flag.  The five required exceptions are
# not routine migraine: two infarcts, MELAS, familial aneurysm and migralepsy.
MRI_REQUIRED = {"MIG-AURA-P03", "MIG-AURA-P07", "MIG-AURA-P08", "MIG-AURA-P09", "MIG-AURA-RM11"}
MRI_RECOMMENDED = {
    "MIG-AURA-M01", "MIG-AURA-M03", "MIG-AURA-M04", "MIG-AURA-M05", "MIG-AURA-M06", "MIG-AURA-M07",
    "MIG-AURA-P01", "MIG-AURA-P02", "MIG-AURA-P04", "MIG-AURA-P05", "MIG-AURA-P06",
}
MRI_OPTIONAL = {"MIG-AURA-M02", "MIG-AURA-M08", "MIG-AURA-RS11"}
MRI_CASES = MRI_REQUIRED | MRI_RECOMMENDED | MRI_OPTIONAL

LAB_PANELS = {
    "MIG-AURA-P01": ["ESR", "CRP", "glucose", "HbA1c", "lipid_panel"],
    "MIG-AURA-P03": ["glucose", "HbA1c", "lipid_panel", "antiphospholipid"],
    "MIG-AURA-P07": ["glucose", "HbA1c", "lipid_panel", "antiphospholipid"],
    "MIG-AURA-P08": ["lactate", "CK", "m3243A_G_mtDNA"],
    "MIG-AURA-RM11": ["CBC", "CMP", "glucose", "lactate"],
}

EEG_CASE = "MIG-AURA-RM11"
ECHO_CASES = {"MIG-AURA-P03", "MIG-AURA-P07", "MIG-AURA-P08"}
MONITOR_CASES = {"MIG-AURA-P02", "MIG-AURA-P03", "MIG-AURA-P07"}
ADVANCED_CASES = {"MIG-AURA-P08"}
SPECIALIZED_CASES = {"MIG-AURA-P04", "MIG-AURA-P06"}


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _reports(case: dict[str, Any], tool: str, initial_key: str) -> list[dict[str, Any]]:
    rows = []
    initial = case["initial_tool_outputs"].get(initial_key)
    if initial:
        rows.append(initial)
    rows.extend(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool and x.get("output"))
    return rows


def _best_labs(case: dict[str, Any]) -> dict[str, Any]:
    reports = _reports(case, "interpret_labs", "labs")
    return _copy(max(reports, key=lambda x: sum(len(v) for v in x.get("panels", {}).values())))


def _report_for(case: dict[str, Any], tool: str, initial_key: str, test_type: str | None = None) -> dict[str, Any]:
    rows = _reports(case, tool, initial_key)
    if test_type:
        rows = [x for x in rows if x.get("test_type") == test_type]
    if not rows:
        raise ValueError(f"{case['case_id']}: missing {tool} {test_type or ''}")
    return _copy(rows[0])


def _rebuild_outputs(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    initial = case["initial_tool_outputs"]
    initial["ecg"] = None
    initial["csf"] = None
    initial["eeg"] = _report_for(case, "analyze_eeg", "eeg") if cid == EEG_CASE else None
    initial["mri"] = initial.get("mri") if cid in MRI_CASES else None
    initial["labs"] = _best_labs(case) if cid in LAB_PANELS else None
    initial["echo"] = None
    initial["cardiac_monitoring"] = None
    initial["advanced_imaging"] = None
    initial["specialized_test"] = None

    rows = []
    keep_tools = set()
    if cid in ECHO_CASES: keep_tools.add("order_echocardiogram")
    if cid in MONITOR_CASES: keep_tools.add("order_cardiac_monitoring")
    if cid in ADVANCED_CASES: keep_tools.add("order_advanced_imaging")
    if cid in SPECIALIZED_CASES: keep_tools.add("order_specialized_test")
    for row in case["followup_outputs"]:
        tool = row.get("tool_name")
        if tool in {"analyze_eeg", "analyze_ecg", "analyze_csf", "interpret_labs", "analyze_brain_mri"}:
            continue
        if tool in {"order_echocardiogram", "order_cardiac_monitoring", "order_advanced_imaging", "order_specialized_test"} and tool not in keep_tools:
            continue
        rows.append(row)
    case["followup_outputs"] = rows


def _action(tool: str, category: str, params: dict[str, Any], text: str, finding: str,
            source: str = "ICHD-3; NICE CG150 (2025)") -> dict[str, Any]:
    return {"action": text, "tool_name": tool, "expected_finding": finding, "category": category,
            "tool_parameters": params, "citation": "[ICHD_3]", "guideline_source": source}


def _clinical_action() -> dict[str, Any]:
    return _action(
        "perform_clinical_assessment", "required", {"assessment_type": "structured_headache_history_ichd3"},
        "Take a structured headache/aura history, neurological examination and red-flag review; apply every ICHD-3 1.2 criterion explicitly",
        "Document attack count; reversible aura modalities; gradual spread; succession; 5–60 minute duration (motor up to 72 hours); unilateral and positive symptoms; relation to headache; medications; examination and red flags",
    )


def _revise_actions(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    removed = {"perform_clinical_assessment", "analyze_brain_mri", "analyze_eeg", "analyze_ecg", "analyze_csf",
               "interpret_labs", "order_echocardiogram", "order_cardiac_monitoring", "order_advanced_imaging",
               "order_specialized_test"}
    kept = [x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") not in removed and x.get("tool_name") is not None]
    kept.append(_clinical_action())

    if cid in MRI_CASES:
        category = "required" if cid in MRI_REQUIRED else "recommended" if cid in MRI_RECOMMENDED else "optional"
        protocol = "stroke" if cid in {"MIG-AURA-P03", "MIG-AURA-P07", "MIG-AURA-P09", "MIG-AURA-RM11"} else "standard"
        reason = {
            "MIG-AURA-P03": "document the infarct required for migrainous-infarction criteria and exclude another stroke mechanism",
            "MIG-AURA-P07": "document a persistent PCA-territory infarct that is not migrainous infarction",
            "MIG-AURA-P08": "investigate persistent deficits and a mitochondrial stroke-like disorder",
            "MIG-AURA-P09": "evaluate motor aura plus a first-degree familial subarachnoid-haemorrhage red flag",
            "MIG-AURA-RM11": "exclude an acute structural lesion after motor aura and a witnessed seizure",
        }.get(cid, "evaluate this first, changed, late-onset, prolonged, motor, brainstem or otherwise atypical aura")
        kept.append(_action("analyze_brain_mri", category, {"protocol": protocol, "contrast": False},
                            f"Obtain brain MRI because imaging answers a specific red-flag question: {reason}",
                            "Identify or exclude infarct, haemorrhage, mass, vascular lesion or another secondary mimic; MRI does not establish routine migraine"))
    if cid == EEG_CASE:
        kept.append(_action("analyze_eeg", "required", {"eeg_type": "video"},
                            "Obtain video-EEG because a convulsive event was witnessed; this evaluates the seizure component, not the migraine",
                            "Capture or assess epileptiform activity relevant to the suspected aura-triggered seizure"))
    if cid in LAB_PANELS:
        category = "recommended" if cid == "MIG-AURA-P01" else "optional"
        kept.append(_action("interpret_labs", category, {"panels": LAB_PANELS[cid]},
                            "Order only tests targeted to this case's secondary-headache, infarct, mitochondrial or seizure differential",
                            "Answer the specific alternative-diagnosis question; blood tests do not confirm migraine"))
    if cid in MONITOR_CASES:
        old = next(x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == "order_cardiac_monitoring")
        old["category"] = "required"
        old["tool_parameters"] = {"monitor_type": old.get("tool_parameters", {}).get("monitor_type", "event_monitor_30d")}
        kept.append(old)
    if cid in ECHO_CASES:
        old = next(x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == "order_echocardiogram")
        old["category"] = "required"
        old["tool_parameters"] = {"echo_type": old.get("tool_parameters", {}).get("echo_type", "TTE")}
        kept.append(old)
    if cid in ADVANCED_CASES:
        old = next(x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == "order_advanced_imaging")
        kept.append(old)
    if cid in SPECIALIZED_CASES:
        kept.extend(x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == "order_specialized_test")
    for i, row in enumerate(kept, 1): row["step"] = i
    case["ground_truth"]["optimal_actions"] = kept


def _criterion_bool(old: dict[str, Any], key: str, default: bool) -> bool:
    value = old.get(key)
    return value if isinstance(value, bool) else default


def _repair_assessment(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    out = case["initial_tool_outputs"].get("clinical_assessment")
    if not out:
        raise ValueError(f"{cid}: missing structured ICHD-3 assessment")
    old = out.get("criteria_met", {})
    gradual = _criterion_bool(old, "gradual_spread_over_at_least_five_minutes", True)
    duration = _criterion_bool(old, "each_symptom_lasts_five_to_sixty_minutes", True)
    unilateral = _criterion_bool(old, "unilateral_symptoms", True)
    headache = _criterion_bool(old, "accompanied_or_followed_by_headache", True)
    succession = cid in {"MIG-AURA-M02", "MIG-AURA-M03", "MIG-AURA-M04", "MIG-AURA-M07", "MIG-AURA-M08",
                         "MIG-AURA-P08", "MIG-AURA-P09", "MIG-AURA-RM11", "MIG-AURA-RS11", "MIG-AURA-S02"}
    positive = cid not in {"MIG-AURA-P01", "MIG-AURA-P02", "MIG-AURA-P05", "MIG-AURA-P06"}
    count = sum((gradual, succession, duration, unilateral, positive, headache))
    at_least_two = _criterion_bool(old, "at_least_two_attacks", cid not in {"MIG-AURA-M01", "MIG-AURA-M07"})
    full_reversal = _criterion_bool(old, "aura_fully_reversible", cid not in {"MIG-AURA-P03", "MIG-AURA-P07", "MIG-AURA-P08"})
    better = _criterion_bool(old, "not_better_accounted_for_by_another_diagnosis", cid not in {"MIG-AURA-P07", "MIG-AURA-P08"})
    out["scores"] = {
        "ICHD-3 criterion C characteristics met": f"{count} of 6 (at least 3 required)",
        "reference criteria applied": "ICHD-3 1.2 and the relevant subtype/complication criteria",
        "aura modalities documented": "visual, sensory, speech/language, motor and/or brainstem features as present in the history",
    }
    out["criteria_met"] = {
        "at_least_two_attacks": at_least_two,
        "one_or_more_fully_reversible_aura_symptoms": full_reversal,
        "gradual_spread_over_at_least_five_minutes": gradual,
        "two_or_more_aura_symptoms_in_succession": succession,
        "each_symptom_lasts_five_to_sixty_minutes_motor_up_to_seventy_two_hours": duration,
        "at_least_one_unilateral_aura_symptom": unilateral,
        "at_least_one_positive_aura_symptom": positive,
        "aura_accompanied_or_followed_within_sixty_minutes_by_headache": headache,
        "at_least_three_of_six_characteristics": count >= 3,
        "not_better_accounted_for_by_another_diagnosis": better,
    }
    if cid in {"MIG-AURA-P03", "MIG-AURA-P07", "MIG-AURA-P08"}:
        out["impression"] = ("The structured history identifies a persistent deficit or a better alternative explanation. "
                             "This is not routine aura confirmation: targeted imaging and etiologic testing are required to distinguish migrainous infarction, another stroke mechanism or MELAS.")
    elif not at_least_two:
        out["impression"] = ("The phenotype has aura-like temporal features but does not yet meet the ICHD-3 requirement for at least two attacks. "
                             "Record it as probable/first-episode aura and investigate only the documented red flags.")
    else:
        out["impression"] = (f"Structured history documents {count} of 6 ICHD-3 criterion-C characteristics with reversible aura symptoms, "
                             "neurological examination and red-flag review. Imaging or laboratory testing is not the diagnostic test for a typical attack.")


def _clean(case: dict[str, Any]) -> None:
    cid = case["case_id"]; gt = case["ground_truth"]
    permitted = {"analyze_eeg"} if cid == EEG_CASE else set()
    if cid in MRI_CASES: permitted.add("analyze_brain_mri")
    if cid in ECHO_CASES: permitted.add("order_echocardiogram")
    if cid in MONITOR_CASES: permitted.add("order_cardiac_monitoring")
    gt["useless_tools"] = [x for x in gt.get("useless_tools", []) if x.get("tool_name") not in permitted]
    gt["red_herrings"] = [x for x in gt.get("red_herrings", []) if not (
        (case["initial_tool_outputs"].get("eeg") is None and "eeg" in str(x.get("data_point", "")).lower()) or
        (case["initial_tool_outputs"].get("mri") is None and "mri" in str(x.get("data_point", "")).lower())
    )]
    for field in ("critical_actions", "key_reasoning_points", "contraindicated_actions"):
        gt[field] = [x for x in gt.get(field, []) if not any(token in str(x).lower() for token in
                     ("routine eeg", "routine ecg", "routine lumbar puncture", "routine echocardiogram"))]
    note = ("July 2026 review applied end to end: ICHD-3 history/examination is required in all cases; "
            "routine MRI, EEG, ECG, CSF, echocardiography, cardiac monitoring and laboratory panels are absent. "
            "Retained tests answer an explicit atypical-aura, seizure, infarct, MELAS, CADASIL or aneurysm question.")
    if note not in gt.setdefault("key_reasoning_points", []): gt["key_reasoning_points"].append(note)
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = "independent migraine review: corrected 3-of-6 ICHD-3 assessment, removed authored routine tests, retained explicit red-flag exceptions"


def revise(case: dict[str, Any]) -> None:
    _rebuild_outputs(case)
    _revise_actions(case)
    _repair_assessment(case)
    _clean(case)


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--cases", type=Path, default=DEFAULT_CASES); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("MIG-AURA-*.json")):
        case = json.loads(path.read_text()); before = json.dumps(case, sort_keys=True); revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check: path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"Migraine cases changed: {changed}")
    if args.check and changed: raise SystemExit(1)


if __name__ == "__main__": main()
