"""Apply Reviewer 1's Parkinson comments to cases and authored tool reports.

This migration is intentionally case-specific.  It removes the apparent routine panel that
survived the first review pass, removes authored EEG/ECG and formal autonomic/tilt studies,
and offers neuropsychology, polysomnography and counselled genetics only when the history
actually raises those questions.  PD-RP04 is the sole required-neuropsych exception because
the encounter is a DBS candidacy assessment rather than routine PD diagnosis.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

CT_ALTERNATIVE_CASE = "PD-S06"

LAB_PANELS = {
    "PD-M04": ["TSH"],
    "PD-P04": ["ceruloplasmin", "serum_copper", "24h_urinary_copper"],
    "PD-RM02": ["LFTs", "ammonia", "valproate_level"],
    "PD-RM05": ["TSH"],
    "PD-RP04": ["CBC", "CMP", "iron_studies"],
    "PD-RS01": ["BMP", "TSH", "lithium_level"],
    "PD-RS03": ["BMP", "TSH", "B12", "HbA1c"],
    "PD-RS04": ["BMP", "TSH", "B12", "folate", "HbA1c"],
    "PD-RS05": ["TSH"],
}

NEUROPSYCH_CASES = {
    "PD-P02", "PD-P03", "PD-RM02", "PD-RM04", "PD-RM05", "PD-RP01",
    "PD-RP02", "PD-RP03", "PD-RP04", "PD-RS03", "PD-RS04",
}

PSG_CASES = {
    "PD-M01", "PD-M02", "PD-M04", "PD-M05", "PD-RM02",
    "PD-RM03", "PD-RM04", "PD-RP03", "PD-RP05", "PD-RS01", "PD-S03",
}

GENETIC_CASES = {"PD-P04", "PD-RM05"}

# DaT imaging is retained only where the case contains a live degenerative-vs-nondegenerative
# question.  It is not useful for distinguishing idiopathic PD from MSA or PSP.
DAT_CASES = {
    "PD-M01", "PD-M02", "PD-M03", "PD-M04", "PD-P02", "PD-P04",
    "PD-RM02", "PD-RM03", "PD-RM05", "PD-RP05", "PD-S05", "PD-S06",
}
MIBG_CASES = {"PD-P01", "PD-P02", "PD-RP02", "PD-RP03"}
FDG_CASES = {"PD-P02"}


def _reports(case: dict[str, Any], tool: str, initial_key: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if case["initial_tool_outputs"].get(initial_key):
        out.append(case["initial_tool_outputs"][initial_key])
    out.extend(
        row["output"] for row in case["followup_outputs"]
        if row.get("tool_name") == tool and row.get("output")
    )
    return out


def _special_kind(report: dict[str, Any]) -> str:
    blob = (str(report.get("test_type", "")) + " " + str(report.get("impression", ""))).lower()
    if "polysom" in blob or "rem without atonia" in blob or "sleep efficiency" in blob:
        return "polysomnography"
    if "neuropsych" in blob or "moca" in blob or "trail making" in blob or "cognitive" in blob:
        return "neuropsych_battery"
    if "autonomic" in blob or "qsart" in blob or "valsava" in blob:
        return "autonomic_testing"
    if "tilt" in blob:
        return "tilt_table"
    return str(report.get("test_type", ""))


def _advanced_kind(report: dict[str, Any]) -> str:
    blob = " ".join(str(report.get(k, "")) for k in ("modality", "tracer_or_protocol", "impression")).lower()
    if "mibg" in blob:
        return "MIBG_scan"
    if "datscan" in blob or "dopamine transporter" in blob or "ioflupane" in blob:
        return "DaTscan"
    if "fdg" in blob or "hypometab" in blob:
        return "FDG_PET"
    if "tau" in blob:
        return "tau_PET"
    return str(report.get("modality", ""))


def _pick(reports: list[dict[str, Any]], kind: str, classifier: Callable[[dict[str, Any]], str]) -> dict[str, Any]:
    for report in reports:
        if classifier(report) == kind:
            return json.loads(json.dumps(report))
    raise ValueError(f"no authored {kind} report")


def _genetic_report() -> dict[str, Any]:
    genes = ["PRKN", "PINK1", "PARK7", "LRRK2", "GBA1", "SNCA"]
    findings = [
        {"panel": "Young-onset Parkinson disease panel", "test": f"{gene} sequencing/CNV",
         "result": "No pathogenic or likely pathogenic variant", "reference_range": "No pathogenic variant"}
        for gene in genes
    ]
    return {
        "test_type": "genetic_panel:PD",
        "findings": findings,
        "quantitative_data": {gene: "No pathogenic or likely pathogenic variant" for gene in genes},
        "impression": (
            "No pathogenic or likely pathogenic variant detected on the counselled young-onset "
            "Parkinson disease panel. A negative panel does not exclude Parkinson disease."
        ),
        "recommended_actions": [],
    }


def _rm05_targeted_labs() -> dict[str, Any]:
    return {
        "panels": {"Thyroid": [
            {"test": "TSH", "value": 5.8, "unit": "mIU/L", "reference_range": "0.4-4.0",
             "is_abnormal": True, "clinical_significance": "Mild undertreatment may contribute to fatigue but does not explain asymmetric levodopa-responsive parkinsonism"},
            {"test": "Free T4", "value": 0.9, "unit": "ng/dL", "reference_range": "0.8-1.8",
             "is_abnormal": False, "clinical_significance": None},
        ]},
        "interpretation": "Mildly elevated TSH with free T4 in range; adjust replacement separately from the PD assessment.",
        "abnormal_values_summary": ["TSH 5.8 mIU/L (elevated)"],
        "recommended_actions": [],
    }


def _rm05_dat_report() -> dict[str, Any]:
    return {
        "modality": "DaTscan", "tracer_or_protocol": "I-123 ioflupane SPECT",
        "findings": [{
            "region": "Right posterior putamen greater than left posterior putamen",
            "signal": "Markedly reduced right and mildly reduced left striatal dopamine-transporter binding",
            "description": "Asymmetric presynaptic nigrostriatal dopaminergic deficit, contralateral to the initially worse left side",
        }],
        "quantitative_data": None,
        "impression": (
            "Abnormal asymmetric DaTscan supporting a degenerative nigrostriatal syndrome rather than "
            "pure intermittent prochlorperazine-induced parkinsonism; the scan does not establish PD subtype."
        ),
        "recommended_actions": [],
    }


def _ct_report() -> dict[str, Any]:
    return {
        "findings": [
            {"type": "Mild age-appropriate volume loss", "location": "Diffuse", "size": "mild",
             "density": None, "description": "No disproportionate regional atrophy or ventriculomegaly"},
        ],
        "contrast_used": False,
        "angiography_findings": None,
        "additional_observations": [
            "No haemorrhage, mass effect, hydrocephalus or large territorial infarct",
            "No strategic basal-ganglia infarct or extensive small-vessel burden to explain parkinsonism",
            "MRI was not completed because severe claustrophobia persisted despite preparation and the patient declined sedation",
            "CT is less sensitive than MRI for subtle atypical-parkinsonism patterns and small-vessel disease",
        ],
        "impression": (
            "Non-contrast head CT shows no structural explanation for the parkinsonian syndrome. "
            "The lower sensitivity of CT relative to MRI is explicitly acknowledged."
        ),
        "recommended_actions": [],
    }


def _rebuild_specialized(case: dict[str, Any], reports: list[dict[str, Any]]) -> None:
    cid = case["case_id"]
    rows = [r for r in case["followup_outputs"] if r.get("tool_name") != "order_specialized_test"]
    case["initial_tool_outputs"].pop("specialized_test", None)
    if cid in NEUROPSYCH_CASES:
        report = _pick(reports, "neuropsych_battery", _special_kind)
        report["test_type"] = "neuropsych_battery"
        rows.append({"trigger_action": "request_optional_neuropsych_for_active_cognitive_question",
                     "tool_name": "order_specialized_test",
                     "tool_parameters": {"test_type": "neuropsych_battery"}, "output": report})
    if cid in PSG_CASES:
        report = _pick(reports, "polysomnography", _special_kind)
        report["test_type"] = "polysomnography"
        rows.append({"trigger_action": "request_optional_psg_for_reported_dream_enactment",
                     "tool_name": "order_specialized_test",
                     "tool_parameters": {"test_type": "polysomnography"}, "output": report})
    if cid in GENETIC_CASES:
        rows.append({"trigger_action": "request_optional_counselled_young_onset_pd_genetics",
                     "tool_name": "order_specialized_test",
                     "tool_parameters": {"test_type": "genetic_panel:PD"}, "output": _genetic_report()})
    case["followup_outputs"] = rows


def _rebuild_advanced(case: dict[str, Any], reports: list[dict[str, Any]]) -> None:
    cid = case["case_id"]
    rows = [r for r in case["followup_outputs"] if r.get("tool_name") != "order_advanced_imaging"]
    case["initial_tool_outputs"].pop("advanced_imaging", None)
    for kind, selected, trigger in (
        ("DaTscan", DAT_CASES, "request_optional_datscan_for_live_degenerative_differential"),
        ("MIBG_scan", MIBG_CASES, "request_optional_mibg_for_synucleinopathy_differential"),
        ("FDG_PET", FDG_CASES, "request_optional_fdg_for_dlb_ad_differential"),
    ):
        if cid not in selected:
            continue
        report = _pick(reports, kind, _advanced_kind)
        report["modality"] = kind
        rows.append({"trigger_action": trigger, "tool_name": "order_advanced_imaging",
                     "tool_parameters": {"modality": kind}, "output": report})
    case["followup_outputs"] = rows


def _special_action(test_type: str, category: str, action: str, finding: str) -> dict[str, Any]:
    return {"action": action, "tool_name": "order_specialized_test", "expected_finding": finding,
            "category": category, "tool_parameters": {"test_type": test_type},
            "citation": "[NICE_NG71]", "guideline_source": "NICE_NG71"}


def _advanced_action(modality: str, action: str, finding: str) -> dict[str, Any]:
    return {"action": action, "tool_name": "order_advanced_imaging", "expected_finding": finding,
            "category": "optional", "tool_parameters": {"modality": modality},
            "citation": "[NICE_NG71]", "guideline_source": "NICE_NG71"}


def _revise_actions(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    kept: list[dict[str, Any]] = []
    for row in case["ground_truth"]["optimal_actions"]:
        tool = row.get("tool_name")
        if tool in {"analyze_eeg", "analyze_ecg", "order_specialized_test", "order_advanced_imaging", "interpret_labs"}:
            continue
        if tool == "analyze_brain_mri":
            if cid == CT_ALTERNATIVE_CASE:
                continue
            row["category"] = "required"
            row["tool_parameters"] = {"protocol": "standard", "contrast": False}
            row["action"] = (
                "Obtain structural brain MRI to exclude a secondary or atypical parkinsonian syndrome; "
                "do not use MRI itself to diagnose idiopathic Parkinson disease"
            )
        if tool == "order_ct_scan":
            continue
        kept.append(row)

    if cid == CT_ALTERNATIVE_CASE:
        kept.append({
            "action": "Obtain non-contrast head CT because severe claustrophobia makes MRI unavailable",
            "tool_name": "order_ct_scan",
            "expected_finding": "No mass, hydrocephalus, haemorrhage or strategic infarct; acknowledge lower sensitivity than MRI",
            "category": "required", "tool_parameters": {"contrast": False},
            "citation": "[NICE_NG71]", "guideline_source": "NICE_NG71",
        })
    if cid in LAB_PANELS:
        kept.append({
            "action": "Order only the case-targeted blood studies; there is no fixed routine PD laboratory panel",
            "tool_name": "interpret_labs",
            "expected_finding": "Address the specific metabolic, toxic, young-onset or pretreatment question in this case",
            "category": "optional", "tool_parameters": {"panels": LAB_PANELS[cid]},
            "citation": "[Postuma_2015]", "guideline_source": "Postuma_2015",
        })
    if cid in NEUROPSYCH_CASES:
        category = "required" if cid == "PD-RP04" else "optional"
        rationale = (
            "Obtain formal neuropsychological testing for DBS candidacy; exclude dementia and characterize PD-MCI"
            if cid == "PD-RP04" else
            "Consider formal neuropsychological testing because cognitive impairment is clinically active in this case"
        )
        kept.append(_special_action("neuropsych_battery", category, rationale,
                                    "Characterize the cognitive profile and functional implications"))
    if cid in PSG_CASES:
        kept.append(_special_action(
            "polysomnography", "optional",
            "Consider video-polysomnography because the history reports dream enactment; this is not routine PD testing",
            "Document REM sleep without atonia if the clinical RBD question remains unresolved",
        ))
    if cid in GENETIC_CASES:
        kept.append(_special_action(
            "genetic_panel:PD", "optional",
            "Offer a targeted Parkinson disease panel only after genetic counselling because this is young-onset disease",
            "A result may inform counselling but is not required to establish the clinical diagnosis",
        ))
    if cid in DAT_CASES:
        kept.append(_advanced_action(
            "DaTscan",
            "Consider presynaptic dopamine-transporter imaging only because this case has a live degenerative-versus-nondegenerative parkinsonism differential",
            "Abnormal striatal uptake supports nigrostriatal degeneration but does not distinguish PD from MSA or PSP",
        ))
    if cid in MIBG_CASES:
        kept.append(_advanced_action(
            "MIBG_scan", "Consider cardiac MIBG only as a supportive biomarker in the active synucleinopathy differential",
            "Cardiac sympathetic denervation pattern may support, but cannot alone establish, the subtype",
        ))
    if cid in FDG_CASES:
        kept.append(_advanced_action(
            "FDG_PET", "Consider FDG-PET only if the DLB-versus-Alzheimer pattern remains uncertain after clinical assessment and structural imaging",
            "Occipital hypometabolism with relative posterior cingulate preservation may support DLB",
        ))

    for step, row in enumerate(kept, 1):
        row["step"] = step
    case["ground_truth"]["optimal_actions"] = kept


def _clean_ground_truth(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    gt = case["ground_truth"]
    # CT is a valid structural alternative, not a universally useless order.
    gt["useless_tools"] = [x for x in gt.get("useless_tools", []) if x.get("tool_name") != "order_ct_scan"]
    fallback_keys = {"analyze_eeg": "eeg", "analyze_ecg": "ecg"}
    for tool, rationale in (
        ("analyze_eeg", "EEG is not a diagnostic test for Parkinson disease or its usual parkinsonian differentials"),
        ("analyze_ecg", "ECG is not a diagnostic test for Parkinson disease"),
    ):
        has_fallback = bool(case.get("fallback_tool_outputs", {}).get(fallback_keys[tool]))
        if not has_fallback:
            gt["useless_tools"] = [x for x in gt["useless_tools"] if x.get("tool_name") != tool]
        elif not any(x.get("tool_name") == tool for x in gt["useless_tools"]):
            gt["useless_tools"].append({"tool_name": tool, "tool_parameters": {}, "rationale": rationale,
                                        "citation": "[NICE_NG71]"})

    removed_tools = {"analyze_eeg", "analyze_ecg"}
    removed_special = {"autonomic_testing", "tilt_table", "emg_ncs", "repetitive_nerve_stimulation",
                       "nerve_biopsy", "muscle_biopsy", "ssep", "vep", "baep"}
    gt["sequence_constraints"] = [
        x for x in gt.get("sequence_constraints", [])
        if x.get("before") not in removed_tools and x.get("after") not in removed_tools
        and not any(t in json.dumps(x).lower() for t in removed_special)
    ]
    for field in ("critical_actions", "contraindicated_actions", "key_reasoning_points"):
        cleaned = []
        for item in gt.get(field, []):
            low = str(item).lower()
            if any(term in low for term in ("formal autonomic testing", "autonomic testing", "tilt-table", "tilt table")):
                continue
            if "datscan" in low and cid not in DAT_CASES:
                continue
            if ("tau-pet" in low or "tau pet" in low):
                continue
            cleaned.append(item)
        gt[field] = cleaned
    tier_note = (
        "July 2026 review applied: PD remains a clinical diagnosis; no fixed routine laboratory panel, "
        "EEG, ECG, formal autonomic or tilt-table testing is part of the PD diagnostic pathway."
    )
    if not any("July 2026 review applied" in str(x) for x in gt.get("key_reasoning_points", [])):
        gt.setdefault("key_reasoning_points", []).append(tier_note)
    if cid == "PD-M05":
        psg_index = next(
            i for i, row in enumerate(case["followup_outputs"])
            if row.get("tool_name") == "order_specialized_test"
            and row.get("output", {}).get("test_type") == "polysomnography"
        )
        for red in gt.get("red_herrings", []):
            if red.get("field_path") == "initial_tool_outputs.specialized_test.findings":
                red["location"] = "followup_outputs"
                red["field_path"] = f"followup_outputs[{psg_index}].output.findings"


def _clean_metadata(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    meta = case["metadata"]
    for key in ("eeg", "ecg"):
        meta.get("fallback_tool_kinds", {}).pop(key, None)
    concerns = []
    for concern in meta.get("case_body_concerns", []):
        text = json.dumps(concern).lower()
        if "required tool(s)" in text or "removed_useless" in text:
            continue
        concerns.append(concern)
    meta["case_body_concerns"] = concerns
    meta["last_revised"] = "2026-08-10"
    meta["revision_reason"] = (
        "independent end-to-end Parkinson tool review: case-targeted labs only; EEG/ECG and "
        "autonomic/tilt removed; cognition, RBD, genetics and advanced imaging narrowed to live questions"
    )
    required = sum(x.get("category") == "required" for x in case["ground_truth"]["optimal_actions"])
    meta["difficulty_rationale"] = (
        f"{required} required tool actions after the independent reviewer audit; remaining optional studies are case-specific"
    )
    if cid == "PD-P01":
        meta["clinical_notes"] = (
            "MSA-P puzzle supported by early severe orthostatic failure documented clinically, poor levodopa response, "
            "and MSA-pattern structural MRI; MIBG and polysomnography are optional supportive studies."
        )
    if cid == "PD-P04":
        meta["key_educational_points"] = [
            "Young-onset parkinsonism warrants targeted Wilson disease exclusion when clinically appropriate.",
            "Counselled PD genetic-panel testing is optional and a negative result does not exclude the clinical diagnosis.",
            "DaT imaging is optional here because a degenerative-versus-functional/dystonic differential is active; it does not subtype degenerative parkinsonism.",
            "Age alone must not be used to reject a clinical Parkinson disease diagnosis.",
        ]
    if cid == "PD-RP01" and isinstance(meta.get("difficulty_description"), str):
        meta["difficulty_description"] = meta["difficulty_description"].replace(
            "requiring integration of DaTscan, levodopa challenge, and longitudinal clinical features",
            "requiring integration of orthostatic measurements, levodopa response, and longitudinal clinical features",
        )
    if cid == "PD-RP04" and isinstance(meta.get("difficulty_description"), str):
        meta["difficulty_description"] = (
            "Advanced levodopa-responsive PD with motor fluctuations and dyskinesia undergoing DBS candidacy review; "
            "formal neuropsychological characterization and medication-interaction review are the load-bearing tool questions."
        )


def revise(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    if cid == "PD-RM05" and not case["initial_tool_outputs"].get("labs"):
        case["initial_tool_outputs"]["labs"] = _rm05_targeted_labs()
    specialized = _reports(case, "order_specialized_test", "specialized_test")
    advanced = _reports(case, "order_advanced_imaging", "advanced_imaging")
    if cid == "PD-RM05" and not any(_advanced_kind(x) == "DaTscan" for x in advanced):
        advanced.append(_rm05_dat_report())

    case["initial_tool_outputs"].pop("eeg", None)
    case["initial_tool_outputs"].pop("ecg", None)
    if cid not in LAB_PANELS:
        case["initial_tool_outputs"].pop("labs", None)
    case["followup_outputs"] = [
        r for r in case["followup_outputs"]
        if r.get("tool_name") not in {"analyze_eeg", "analyze_ecg", "interpret_labs"}
    ]

    if cid == CT_ALTERNATIVE_CASE:
        case.setdefault("metadata", {}).setdefault("panel_required_exemptions", {})["analyze_brain_mri"] = (
            "MRI is unavailable because severe claustrophobia persisted despite preparation and the patient declined sedation; required non-contrast CT is the structural alternative."
        )
        case["initial_tool_outputs"].pop("mri", None)
        case["initial_tool_outputs"]["ct"] = _ct_report()
        hpi = case["patient"]["history_present_illness"]
        note = (" She has severe longstanding claustrophobia and declined brain MRI despite preparation; "
                "she also declined sedation but agreed to non-contrast CT.")
        if "severe longstanding claustrophobia" not in hpi:
            case["patient"]["history_present_illness"] = hpi.rstrip() + note

    _rebuild_specialized(case, specialized)
    _rebuild_advanced(case, advanced)
    _revise_actions(case)
    _clean_ground_truth(case)
    _clean_metadata(case)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered: list[tuple[Path, str]] = []
    for path in sorted(args.cases_dir.glob("PD-*.json")):
        case = json.loads(path.read_text())
        revise(case)
        rendered.append((path, json.dumps(case, indent=2, ensure_ascii=False) + "\n"))
    changed = sum(path.read_text() != text for path, text in rendered)
    print(f"Parkinson cases changed: {changed}/{len(rendered)}")
    if args.check and changed:
        raise SystemExit(1)
    if not args.check:
        for path, text in rendered:
            path.write_text(text)


if __name__ == "__main__":
    main()
