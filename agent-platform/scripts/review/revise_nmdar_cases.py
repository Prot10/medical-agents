"""Apply Reviewer 2's anti-NMDAR work-up with age/sex-tailored tumour screening."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

TESTICULAR_CASES = {"NMDAR-ENC-M05", "NMDAR-ENC-P02", "NMDAR-ENC-P03", "NMDAR-ENC-RS03"}
CAP_CASES = {"NMDAR-ENC-RP01", "NMDAR-ENC-RP02", "NMDAR-ENC-RP03"}
CONTINUOUS_EEG_CASES = {
    "NMDAR-ENC-M01", "NMDAR-ENC-M03", "NMDAR-ENC-M04", "NMDAR-ENC-M05",
    "NMDAR-ENC-P01", "NMDAR-ENC-P03", "NMDAR-ENC-P05", "NMDAR-ENC-P06",
    "NMDAR-ENC-P07", "NMDAR-ENC-RP02", "NMDAR-ENC-RP03", "NMDAR-ENC-S09",
    "NMDAR-ENC-S10",
}


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _action(tool: str, params: dict[str, Any], text: str, finding: str,
            category: str = "required") -> dict[str, Any]:
    return {
        "action": text, "tool_name": tool, "expected_finding": finding,
        "category": category, "tool_parameters": params, "citation": "[Graus_2016]",
        "guideline_source": "Graus 2016; Titulaer 2013",
    }


def _lab_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for rows in (report.get("panels") or {}).values() for row in rows]


def _find_lab_row(report: dict[str, Any], *needles: str) -> dict[str, Any] | None:
    for row in _lab_rows(report):
        text = f"{row.get('test', '')} {row.get('value', '')}".lower()
        if any(needle.lower() in text for needle in needles):
            return _copy(row)
    return None


def _merge_panels(target: dict[str, Any], source: dict[str, Any]) -> None:
    panels = target.setdefault("panels", {})
    for name, rows in (source.get("panels") or {}).items():
        panels[name] = _copy(rows)


def _normalize_labs(case: dict[str, Any]) -> dict[str, Any]:
    report = _copy(case["initial_tool_outputs"]["labs"])
    for row in case["followup_outputs"]:
        if row.get("tool_name") != "interpret_labs":
            continue
        trigger = row.get("trigger_action", "").lower()
        if "nmdar_antibod" in trigger or "nmdar_antibody" in trigger or "autoimmune_panel" in trigger:
            _merge_panels(report, row["output"])

    panels = report.setdefault("panels", {})
    inr = _find_lab_row(report, "inr") or {
        "test": "PT/INR", "value": "Within reference range", "unit": "",
        "reference_range": "laboratory reference", "is_abnormal": False,
    }
    aptt = _find_lab_row(report, "aptt", "ptt") or {
        "test": "aPTT", "value": "Within reference range", "unit": "",
        "reference_range": "laboratory reference", "is_abnormal": False,
    }
    panels["Coagulation"] = [inr, aptt]

    anti_tpo = _find_lab_row(report, "anti-tpo", "anti_tpo") or {
        "test": "anti-TPO", "value": "Negative", "unit": "",
        "reference_range": "negative", "is_abnormal": False,
    }
    anti_tg = _find_lab_row(report, "thyroglobulin") or {
        "test": "anti-thyroglobulin", "value": "Negative", "unit": "",
        "reference_range": "negative", "is_abnormal": False,
    }
    panels["Thyroid autoantibodies"] = [anti_tpo, anti_tg]

    esr = _find_lab_row(report, "esr") or {
        "test": "ESR", "value": "Within reference range", "unit": "mm/h",
        "reference_range": "age/sex adjusted", "is_abnormal": False,
    }
    crp = _find_lab_row(report, "crp", "c-reactive") or {
        "test": "CRP", "value": "Within reference range", "unit": "mg/L",
        "reference_range": "<5", "is_abnormal": False,
    }
    panels["Reviewed inflammatory markers"] = [esr, crp]

    serum = _find_lab_row(report, "nmdar", "nmda receptor", "glun1")
    if serum is None:
        negative = case["case_id"] == "NMDAR-ENC-RP01"
        serum = {
            "test": "Serum IgG anti-GluN1 (NMDA receptor), live cell-based assay",
            "value": "Negative" if negative else "Positive",
            "unit": "", "reference_range": "negative", "is_abnormal": not negative,
            "clinical_significance": (
                "Serum result is interpreted only with the paired CSF assay; serum alone can be false positive or false negative."
            ),
        }
    panels["Serum anti-GluN1 cell-based assay"] = [serum]

    if not _find_lab_row(report, "lgi1", "caspr2", "gaba-b", "ampa"):
        panels["Autoimmune encephalitis panel"] = [{
            "test": "LGI1/CASPR2/GABA-B/AMPA and other neuronal-surface antibodies",
            "value": "No additional antibody detected", "unit": "",
            "reference_range": "negative", "is_abnormal": False,
        }]
    if not _find_lab_row(report, "hu", "yo", "ri", "ma2", "crmp5"):
        panels["Paraneoplastic antibody panel"] = [{
            "test": "Hu/Yo/Ri/Ma2/CRMP5 and related onconeural antibodies",
            "value": "Negative", "unit": "", "reference_range": "negative",
            "is_abnormal": False,
        }]
    return report


def _normalize_csf(case: dict[str, Any]) -> dict[str, Any]:
    report = _copy(case["initial_tool_outputs"]["csf"])
    special = report.setdefault("special_tests", {})
    blob = json.dumps(special).lower()
    if not any(token in blob for token in ("nmdar", "nmda receptor", "glun1")):
        found = None
        for row in case["followup_outputs"]:
            if row.get("tool_name") != "analyze_csf":
                continue
            for key, value in (row["output"].get("special_tests") or {}).items():
                if any(token in key.lower() for token in ("nmdar", "nmda", "glun1")):
                    found = value
                    break
        if found is None:
            found = "Negative" if case["case_id"] == "NMDAR-ENC-RP01" else "Positive"
        special["NMDAR_antibodies"] = found
    else:
        # Add a canonical key so the requested assay is reachable even when the authored
        # report used one of several human-readable spellings.
        for key, value in list(special.items()):
            if any(token in key.lower() for token in ("nmdar", "nmda", "glun1")):
                special.setdefault("NMDAR_antibodies", value)
                break
    return report


def _lab_imaging_to_body(source: dict[str, Any], region: str) -> dict[str, Any]:
    findings = []
    for row in _lab_rows(source):
        findings.append({
            "structure": str(row.get("test", "")),
            "finding": str(row.get("value", "")),
            "abnormal": str(bool(row.get("is_abnormal", False))).lower(),
        })
    return {
        "region": region, "modality": "ultrasound", "contrast": False,
        "findings": findings, "measurements": None,
        "impression": source.get("interpretation", "Targeted tumour screening completed."),
        "recommended_actions": [],
    }


def _tumour_screen(case: dict[str, Any]) -> tuple[dict[str, Any], str, bool]:
    cid = case["case_id"]
    sex = case["patient"]["demographics"]["sex"].lower()
    existing = case["initial_tool_outputs"].get("body_imaging")
    if sex == "female":
        if existing and existing.get("region") == "pelvis_abdomen" and existing.get("modality") == "ultrasound":
            return _copy(existing), "pelvis_abdomen_ultrasound", False
        source = next(
            row["output"] for row in case["followup_outputs"]
            if row.get("trigger_action") == "request_pelvic_ultrasound"
        )
        return _lab_imaging_to_body(source, "pelvis_abdomen"), "pelvis_abdomen_ultrasound", False
    if cid in TESTICULAR_CASES:
        if existing and existing.get("region") == "testes" and existing.get("modality") == "ultrasound":
            return _copy(existing), "testicular_ultrasound", False
        source = next((
            row["output"] for row in case["followup_outputs"]
            if "testicular" in row.get("trigger_action", "")
        ), None)
        if source is not None:
            report = _lab_imaging_to_body(source, "testes")
        else:
            report = {
                "region": "testes", "modality": "ultrasound", "contrast": False,
                "findings": [
                    {"structure": "Right testis", "finding": "No focal intratesticular mass", "abnormal": "false"},
                    {"structure": "Left testis", "finding": "No focal intratesticular mass", "abnormal": "false"},
                ],
                "measurements": None,
                "impression": "Normal bilateral testicular ultrasound; no germ-cell tumour identified.",
                "recommended_actions": [],
            }
        return report, "testicular_ultrasound", False
    if cid in CAP_CASES:
        if existing and existing.get("region") in {"chest_abdomen_pelvis", "chest/abdomen/pelvis"}:
            return _copy(existing), "chest_abdomen_pelvis_CT", True
        reports = []
        if case["initial_tool_outputs"].get("body_imaging"):
            reports.append(case["initial_tool_outputs"]["body_imaging"])
        reports.extend(
            row["output"] for row in case["followup_outputs"]
            if row.get("tool_name") == "order_body_imaging"
        )
        if not reports:
            raise ValueError(f"{cid}: missing tailored older-male tumour screen")
        return _copy(max(reports, key=lambda x: len(json.dumps(x)))), "chest_abdomen_pelvis_CT", True
    raise ValueError(f"{cid}: no age/sex tumour-screening route")


def _rebuild_outputs(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    screen, _study, _contrast = _tumour_screen(case)
    labs = _normalize_labs(case)
    csf = _normalize_csf(case)
    initial = case["initial_tool_outputs"]
    initial["body_imaging"] = screen
    initial["labs"] = labs
    initial["csf"] = csf
    initial["microbiology"] = None
    initial["advanced_imaging"] = None
    initial["eeg"]["eeg_type"] = "routine"

    continuous = next((
        _copy(row) for row in case["followup_outputs"]
        if row.get("tool_name") == "analyze_eeg" and "continuous" in row.get("trigger_action", "")
    ), None)
    kept = [
        row for row in case["followup_outputs"]
        if row.get("tool_name") not in {
            "interpret_labs", "analyze_csf", "analyze_eeg", "order_body_imaging",
            "order_microbiology", "order_advanced_imaging",
        }
    ]
    if cid in CONTINUOUS_EEG_CASES:
        if continuous is None:
            raise ValueError(f"{cid}: selected continuous EEG has no authored report")
        continuous["trigger_action"] = "request_continuous_eeg"
        continuous["tool_parameters"] = {"eeg_type": "continuous_icu"}
        continuous["output"]["eeg_type"] = "continuous_icu"
        kept.append(continuous)
    case["followup_outputs"] = kept


def _rebuild_actions(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    gt = case["ground_truth"]
    treatment = [row["action"] for row in gt["optimal_actions"] if row.get("tool_name") is None]
    for text in treatment:
        if text not in gt.setdefault("critical_actions", []):
            gt["critical_actions"].append(text)
    other = [
        _copy(row) for row in gt["optimal_actions"]
        if row.get("tool_name") in {"search_medical_literature", "check_drug_interactions"}
    ]
    for row in other:
        row["category"] = "recommended"

    sex = case["patient"]["demographics"]["sex"].lower()
    if sex == "female":
        study, contrast = "pelvis_abdomen_ultrasound", False
        screen_text = "Perform required pelvic and abdominal ultrasound screening for an ovarian teratoma once anti-NMDAR encephalitis is recognised"
    elif cid in TESTICULAR_CASES:
        study, contrast = "testicular_ultrasound", False
        screen_text = "Perform targeted testicular ultrasound as the age- and sex-adapted occult germ-cell tumour screen in this male patient"
    else:
        study, contrast = "chest_abdomen_pelvis_CT", True
        screen_text = "Perform age- and context-adapted chest, abdominal and pelvic tumour screening in this older male patient"

    actions = [
        _action(
            "analyze_brain_mri", {"protocol": "standard", "contrast": True},
            "Obtain contrast-enhanced brain MRI to exclude HSV encephalitis, structural lesions and overlapping demyelination; a normal MRI does not exclude anti-NMDAR encephalitis",
            "Often normal or nonspecific; temporal/cortical signal or overlapping inflammatory lesions may support the differential but do not confirm anti-NMDAR encephalitis",
        ),
        _action(
            "analyze_csf",
            {"basic": ["cell_count", "protein", "glucose"],
             "special_tests": ["oligoclonal_bands", "IgG_index", "HSV_PCR", "NMDAR_antibodies"]},
            "Analyze CSF for cells, protein and glucose, OCB/IgG index, HSV PCR and a cell-based IgG anti-GluN1 assay interpreted in parallel with serum",
            "Variable lymphocytic inflammation; HSV PCR addresses the infectious mimic; CSF anti-GluN1 is the decisive antibody compartment and may differ from serum",
        ),
        _action(
            "analyze_eeg", {"eeg_type": "routine"},
            "Obtain EEG for encephalopathic and epileptiform abnormalities, explicitly assessing for extreme delta brush",
            "Diffuse slowing, seizures or extreme delta brush; absence of the latter does not exclude the diagnosis",
        ),
        _action(
            "interpret_labs",
            {"panels": ["CBC", "CMP", "coagulation", "thyroid", "anti_TPO",
                        "anti_thyroglobulin", "ESR", "CRP", "autoimmune_encephalitis_panel",
                        "paraneoplastic_panel", "NMDAR_IgG_cell_based"]},
            "Obtain the reviewed serum work-up, including a cell-based IgG anti-GluN1 assay that must be interpreted with CSF rather than alone",
            "Systemic, thyroid/inflammatory and alternative autoimmune/paraneoplastic results; paired serum anti-GluN1 can be false positive or false negative in isolation",
        ),
        _action(
            "order_body_imaging", {"study": study, "contrast": contrast}, screen_text,
            "Identify or exclude an ovarian/testicular germ-cell tumour or another context-appropriate occult neoplasm whose treatment changes outcome and relapse risk",
        ),
    ]
    if cid in CONTINUOUS_EEG_CASES:
        actions.append(_action(
            "analyze_eeg", {"eeg_type": "continuous_icu"},
            "Escalate to continuous ICU EEG because this case has severe encephalopathy, electrographic seizures or unreliable clinical event detection",
            "Seizure burden, non-convulsive status and evolution of encephalopathic patterns",
            "recommended",
        ))
    actions.extend(other)
    for i, row in enumerate(actions, 1):
        row["step"] = i
    gt["optimal_actions"] = actions
    gt["sequence_constraints"] = []


def _metadata(case: dict[str, Any]) -> None:
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = (
        "Independent Reviewer 2 anti-NMDAR audit: tumour screening tailored by age/sex and moved "
        "out of lab payloads; paired serum/CSF anti-GluN1 reachable; routine EEG baseline with "
        "selected continuous escalation; blanket CAP CT, FDG-PET and blood cultures removed"
    )


def revise(case: dict[str, Any]) -> None:
    _rebuild_outputs(case)
    _rebuild_actions(case)
    _metadata(case)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("NMDAR-*.json")):
        case = json.loads(path.read_text())
        before = json.dumps(case, sort_keys=True)
        revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check:
                path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"NMDAR cases changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
