"""Normalize NeuroBench v5 case JSON files to match Pydantic schema.

This script fixes systematic validation errors in v5 cases:

1. MRI findings: signal_characteristics is a string → convert to dict
2. MRI findings: extra fields stripped (sequences, normal_structures, enhancement_pattern, etc.)
3. EEG reports: non-standard structure (no classification, uses background_activity/
   abnormal_findings/events_captured/abnormalities) → convert to EEGReport schema
4. optimal_actions: missing tool_parameters → add {}
5. optimal_actions: category values like "very_low", "low", etc. → map to valid enum values
6. followup_outputs MRI/EEG/CT tool outputs: same structural fixes
7. condition: non-enum strings (e.g. "behavioral_variant_frontotemporal_dementia",
   "Anti-NMDA receptor encephalitis") → map to correct enum values
8. Patient (flat v1 format): age/sex/hpi/pmh at top level → nest under demographics/clinical_history
9. initial_tool_outputs: keyed by tool function names (analyze_brain_mri etc.) → canonical names
   (mri, eeg, labs, csf, ct, etc.)
10. ground_truth: non-standard format (optimal_action_sequence: list[str],
    differential_diagnosis, key_reasoning) → convert to ActionStep list + standard fields
11. Medications: list of strings → list of Medication dicts
12. EEGReport/MRIReport in followup_outputs union type: ensure correct structure

Usage:
    uv run python agent-platform/scripts/normalize_v5_cases.py [--dry-run]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

CASES_DIR = Path(__file__).parent.parent.parent / "data" / "neurobench_v5" / "cases"

# ─── Enum mappings ─────────────────────────────────────────────────────────────

CONDITION_MAP: dict[str, str] = {
    "behavioral_variant_frontotemporal_dementia": "ftd",
    "behavioral variant frontotemporal dementia": "ftd",
    "frontotemporal dementia": "ftd",
    "frontotemporal_dementia": "ftd",
    "bvftd": "ftd",
    "anti-nmda receptor encephalitis": "autoimmune_encephalitis_nmdar",
    "anti-nmdar encephalitis": "autoimmune_encephalitis_nmdar",
    "autoimmune encephalitis nmdar": "autoimmune_encephalitis_nmdar",
    "nmdar encephalitis": "autoimmune_encephalitis_nmdar",
    "peripheral neuropathy (diabetic/cidp/toxic)": "peripheral_neuropathy",
    "peripheral neuropathy": "peripheral_neuropathy",
    "cidp": "peripheral_neuropathy",
    "guillain-barré syndrome": "guillain_barre",
    "guillain barre syndrome": "guillain_barre",
    "status epilepticus": "status_epilepticus",
    "subarachnoid hemorrhage": "subarachnoid_hemorrhage",
    "hepatic encephalopathy": "hepatic_encephalopathy",
    "alzheimer's disease": "alzheimers_early",
    "alzheimers disease": "alzheimers_early",
    "parkinson's disease": "parkinsons",
    "parkinsons disease": "parkinsons",
    "migraine with typical aura": "migraine_with_aura",
    "migraine with aura": "migraine_with_aura",
    "migraine without aura": "migraine_without_aura",
    "myasthenia gravis": "myasthenia_gravis",
}

VALID_CATEGORIES = {"required", "acceptable", "contraindicated"}

# Maps tool function names → canonical ToolOutputSet field names
TOOL_NAME_TO_FIELD: dict[str, str] = {
    "analyze_brain_mri": "mri",
    "analyze_eeg": "eeg",
    "analyze_ecg": "ecg",
    "interpret_labs": "labs",
    "analyze_csf": "csf",
    "order_ct_scan": "ct",
    "order_echocardiogram": "echo",
    "order_cardiac_monitoring": "cardiac_monitoring",
    "order_advanced_imaging": "advanced_imaging",
    "order_specialized_test": "specialized_test",
    "search_medical_literature": "literature_search",
    "check_drug_interactions": "drug_interactions",
}

# ─── Signal / MRI helpers ──────────────────────────────────────────────────────


def fix_signal_characteristics(val: Any) -> dict[str, str]:
    """Convert a string signal_characteristics to dict[str,str]."""
    if isinstance(val, dict):
        return {str(k): str(v) for k, v in val.items()}
    if isinstance(val, str):
        return {"description": val}
    if val is None:
        return {}
    return {"description": str(val)}


def fix_mri_finding(finding: dict) -> dict:
    """Normalize a single MRI finding to MRIFinding schema."""
    return {
        "type": str(finding.get("type", "unknown")),
        "location": str(finding.get("location", "")),
        "size": finding.get("size", None),
        "signal_characteristics": fix_signal_characteristics(
            finding.get("signal_characteristics", {})
        ),
        "mass_effect": finding.get("mass_effect", None),
        "borders": finding.get("borders", None),
    }


def fix_mri_report(mri: dict) -> dict:
    """Normalize an MRI report to MRIReport schema."""
    raw_findings = mri.get("findings", [])
    findings = [fix_mri_finding(f) for f in raw_findings if isinstance(f, dict)]

    volumetrics = mri.get("volumetrics")
    if isinstance(volumetrics, dict):
        volumetrics = {str(k): str(v) for k, v in volumetrics.items()}
    else:
        volumetrics = None

    ao = mri.get("additional_observations", [])
    additional_observations = [str(x) for x in ao] if isinstance(ao, list) else []

    dbi = mri.get("differential_by_imaging", [])
    differential_by_imaging = (
        [{str(k): str(v) for k, v in item.items()} for item in dbi if isinstance(item, dict)]
        if isinstance(dbi, list)
        else []
    )

    ra = mri.get("recommended_actions", [])
    recommended_actions = [str(x) for x in ra] if isinstance(ra, list) else []

    return {
        "findings": findings,
        "volumetrics": volumetrics,
        "additional_observations": additional_observations,
        "impression": str(mri.get("impression", "")),
        "differential_by_imaging": differential_by_imaging,
        "recommended_actions": recommended_actions,
    }


# ─── EEG helpers ──────────────────────────────────────────────────────────────


def _determine_eeg_classification(eeg: dict) -> str:
    c = eeg.get("classification")
    if c in ("normal", "abnormal"):
        return c

    impression = (eeg.get("impression", "") + " " + eeg.get("epileptiform_activity", "")).lower()
    if eeg.get("abnormal_findings") or eeg.get("epileptiform_activity"):
        return "abnormal"

    events = eeg.get("events_captured", [])
    if events and isinstance(events, list):
        first = events[0] if isinstance(events[0], dict) else {}
        correlate = first.get("eeg_correlate", "").upper()
        if "NO EEG CHANGE" in correlate or "NO EEG CORRELATE" in correlate:
            # Normal background during event = normal EEG classification
            return "normal"
        return "abnormal"

    if "abnormalities" in eeg and not eeg["abnormalities"]:
        return "normal"

    if any(x in impression for x in ["abnormal", "ictal", "epilepti", "encephalopathy",
                                      "seizure", "delta brush", "slowing", "discharge"]):
        return "abnormal"
    if "normal" in impression and "abnormal" not in impression:
        return "normal"

    return "abnormal"


def _synthesize_eeg_findings(eeg: dict) -> list[dict]:
    """Convert various non-standard EEG finding lists to list[EEGFinding]."""
    # Standard schema: findings list with type/location keys
    raw = eeg.get("findings", [])
    if raw and isinstance(raw[0], dict) and "type" in raw[0] and "location" in raw[0]:
        return [
            {
                "type": str(f.get("type", "")),
                "location": str(f.get("location", "")),
                "frequency": str(f.get("frequency", "")),
                "morphology": str(f.get("morphology", f.get("description", ""))),
                "state": str(f.get("state", "")),
                "clinical_correlation": str(f.get("clinical_correlation", "")),
            }
            for f in raw
            if isinstance(f, dict)
        ]

    findings = []

    # abnormal_findings format (NMDAR style): type/location/frequency/description
    for f in eeg.get("abnormal_findings", []):
        if isinstance(f, dict):
            findings.append({
                "type": str(f.get("type", "abnormality")),
                "location": str(f.get("location", "")),
                "frequency": str(f.get("frequency", "")),
                "morphology": str(f.get("description", "")),
                "state": "",
                "clinical_correlation": "",
            })

    # findings with channel/finding keys (old v1 format)
    for f in raw:
        if isinstance(f, dict) and "channel" in f:
            findings.append({
                "type": str(f.get("channel", "finding")),
                "location": str(f.get("channel", "")),
                "frequency": "",
                "morphology": str(f.get("finding", "")),
                "state": "",
                "clinical_correlation": "",
            })

    # events_captured (FND/SE follow-up style)
    for event in eeg.get("events_captured", []):
        if isinstance(event, dict):
            findings.append({
                "type": str(event.get("event_type", "captured_event")),
                "location": "generalized",
                "frequency": "",
                "morphology": str(event.get("eeg_correlate", event.get("clinical_features", ""))),
                "state": "awake",
                "clinical_correlation": str(event.get("clinical_features", "")),
            })

    # plain string abnormalities
    for item in eeg.get("abnormalities", []):
        if isinstance(item, str):
            findings.append({
                "type": "abnormality",
                "location": "",
                "frequency": "",
                "morphology": item,
                "state": "",
                "clinical_correlation": "",
            })

    return findings


def fix_eeg_report(eeg: dict) -> dict:
    """Normalize an EEG report to EEGReport schema."""
    bg = eeg.get("background", {})
    if isinstance(bg, str):
        bg = {"description": bg}
    elif not isinstance(bg, dict):
        ba = eeg.get("background_activity", "")
        bg = {"description": str(ba)} if ba else {}
    else:
        bg = {str(k): str(v) for k, v in bg.items()}

    artifacts = eeg.get("artifacts", [])
    if isinstance(artifacts, list):
        artifacts = [
            {str(k): str(v) for k, v in a.items()} if isinstance(a, dict) else {"description": str(a)}
            for a in artifacts
        ]
    else:
        artifacts = []

    ap = eeg.get("activating_procedures", {})
    ap = {str(k): str(v) for k, v in ap.items()} if isinstance(ap, dict) else {}

    ra = eeg.get("recommended_actions", eeg.get("recommendations", []))
    recommended_actions = [str(x) for x in ra] if isinstance(ra, list) else []

    return {
        "classification": _determine_eeg_classification(eeg),
        "background": bg,
        "findings": _synthesize_eeg_findings(eeg),
        "artifacts": artifacts,
        "activating_procedures": ap,
        "impression": str(eeg.get("impression", "")),
        "limitations": str(eeg.get("limitations", "")),
        "recommended_actions": recommended_actions,
    }


# ─── CT helpers ───────────────────────────────────────────────────────────────


def fix_ct_finding(finding: dict) -> dict:
    return {
        "type": str(finding.get("type", "unknown")),
        "location": str(finding.get("location", "")),
        "size": finding.get("size", None),
        "density": finding.get("density", None),
        "description": str(finding.get("description", "")),
    }


def fix_ct_report(ct: dict) -> dict:
    raw = ct.get("findings", [])
    findings = [fix_ct_finding(f) for f in raw if isinstance(f, dict)]

    af = ct.get("angiography_findings")
    if isinstance(af, dict):
        af = {str(k): str(v) for k, v in af.items()}
    else:
        af = None

    ao = ct.get("additional_observations", [])
    ra = ct.get("recommended_actions", [])

    return {
        "findings": findings,
        "contrast_used": bool(ct.get("contrast_used", False)),
        "angiography_findings": af,
        "additional_observations": [str(x) for x in ao] if isinstance(ao, list) else [],
        "impression": str(ct.get("impression", "")),
        "recommended_actions": [str(x) for x in ra] if isinstance(ra, list) else [],
    }


# ─── Labs helpers ─────────────────────────────────────────────────────────────


def _normalize_lab_value(item: Any) -> dict | None:
    """Convert various lab value formats to LabValue schema."""
    if not isinstance(item, dict):
        return None

    # Standard schema already has: test, value, unit, reference_range, is_abnormal
    if "test" in item and "value" in item and "reference_range" in item:
        result = {
            "test": str(item["test"]),
            "value": item["value"],  # float | str — keep as-is
            "unit": str(item.get("unit", "")),
            "reference_range": str(item["reference_range"]),
            "is_abnormal": bool(item.get("is_abnormal", item.get("flag", "normal") not in ("normal", ""))),
        }
        if "clinical_significance" in item:
            result["clinical_significance"] = item["clinical_significance"]
        return result

    # Old format with flag instead of is_abnormal
    if "test" in item and "value" in item:
        flag = str(item.get("flag", "normal")).lower()
        is_abnormal = flag not in ("normal", "")
        return {
            "test": str(item["test"]),
            "value": item["value"],
            "unit": str(item.get("unit", "")),
            "reference_range": str(item.get("reference_range", item.get("reference", ""))),
            "is_abnormal": is_abnormal,
        }

    return None


def fix_labs_report(labs: dict) -> dict:
    """Normalize a labs report to LabResults schema."""
    panels = labs.get("panels", {})

    if isinstance(panels, dict):
        # Standard: panels is dict[str, list[LabValue]]
        new_panels = {}
        for panel_name, items in panels.items():
            if isinstance(items, list):
                normalized = [_normalize_lab_value(x) for x in items]
                new_panels[str(panel_name)] = [x for x in normalized if x is not None]
        panels = new_panels
    elif isinstance(panels, list):
        # Old format: panels is list of {panel_name, results: [...]}
        new_panels = {}
        for panel in panels:
            if isinstance(panel, dict):
                name = str(panel.get("panel_name", panel.get("name", "Panel")))
                results = panel.get("results", [])
                if isinstance(results, list):
                    normalized = [_normalize_lab_value(x) for x in results]
                    new_panels[name] = [x for x in normalized if x is not None]
        panels = new_panels
    else:
        panels = {}

    return {
        "panels": panels,
        "interpretation": str(labs.get("interpretation", "")),
        "abnormal_values_summary": [str(x) for x in labs.get("abnormal_values_summary", [])],
    }


# ─── Patient helpers ──────────────────────────────────────────────────────────


def _fix_medications(meds: Any) -> list[dict]:
    """Convert medication list to list[Medication] schema."""
    if not isinstance(meds, list):
        return []
    result = []
    for m in meds:
        if isinstance(m, dict):
            # May have 'name' instead of 'drug'
            drug = m.get("drug", m.get("name", m.get("medication", "")))
            result.append({
                "drug": str(drug),
                "dose": str(m.get("dose", m.get("dosage", ""))),
                "frequency": str(m.get("frequency", m.get("schedule", ""))),
                "indication": str(m.get("indication", m.get("for", ""))),
            })
        elif isinstance(m, str):
            # Plain string like "Amlodipine 5 mg daily (hypertension)"
            # Best-effort parse
            result.append({
                "drug": m,
                "dose": "",
                "frequency": "",
                "indication": "",
            })
    return result


def fix_patient(patient: dict) -> dict:
    """Normalize patient object — handle nested vs flat formats."""
    fixed = dict(patient)

    # patient_id: required
    if not fixed.get("patient_id"):
        fixed["patient_id"] = "UNKNOWN"

    # demographics: required — must have age (int) and sex (male|female)
    if "demographics" not in fixed or not isinstance(fixed.get("demographics"), dict):
        fixed["demographics"] = {}

    demo = fixed["demographics"]
    # Fill from flat patient fields if missing in demographics
    if "age" not in demo or demo["age"] == 50:
        if "age" in fixed and isinstance(fixed["age"], int):
            demo["age"] = fixed["age"]
    if "sex" not in demo or demo["sex"] == "male":
        if "sex" in fixed and fixed["sex"] in ("male", "female"):
            demo["sex"] = fixed["sex"]

    # Ensure required demographics fields
    if "age" not in demo:
        demo["age"] = 50
    if "sex" not in demo:
        demo["sex"] = "male"

    # Clamp age to valid range 18-90
    try:
        age = int(demo["age"])
        demo["age"] = max(18, min(90, age))
    except (TypeError, ValueError):
        demo["age"] = 50

    # sex must be "male" or "female"
    sex = str(demo.get("sex", "male")).lower()
    demo["sex"] = sex if sex in ("male", "female") else "male"

    fixed["demographics"] = demo

    # clinical_history: required
    if "clinical_history" not in fixed or not isinstance(fixed.get("clinical_history"), dict):
        fixed["clinical_history"] = {}

    ch = fixed["clinical_history"]

    # Ensure list fields are lists
    for list_field in ["past_medical_history", "allergies", "family_history"]:
        if list_field not in ch:
            ch[list_field] = []
        elif isinstance(ch[list_field], str):
            ch[list_field] = [ch[list_field]]
        elif not isinstance(ch[list_field], list):
            ch[list_field] = []

    # medications: must be list of Medication dicts
    if "medications" not in ch:
        ch["medications"] = []
    else:
        ch["medications"] = _fix_medications(ch["medications"])

    # social_history: must be dict[str, str]
    if "social_history" not in ch:
        ch["social_history"] = {}
    elif not isinstance(ch["social_history"], dict):
        ch["social_history"] = {"note": str(ch["social_history"])}

    fixed["clinical_history"] = ch

    # neurological_exam: required — needs to be dict (NeurologicalExam model has all fields optional)
    if "neurological_exam" not in fixed or not isinstance(fixed.get("neurological_exam"), dict):
        # Try top-level neurological_exam (some cases have it outside patient)
        fixed["neurological_exam"] = {}

    ne = fixed["neurological_exam"]
    # Ensure all fields are strings
    for field in ["mental_status", "cranial_nerves", "motor", "sensory", "reflexes",
                  "coordination", "gait"]:
        if field not in ne:
            ne[field] = ""
        elif not isinstance(ne[field], str):
            ne[field] = str(ne[field])

    fixed["neurological_exam"] = ne

    # vitals: required — must have all 6 required fields
    if "vitals" not in fixed or not isinstance(fixed.get("vitals"), dict):
        fixed["vitals"] = {
            "bp_systolic": 120, "bp_diastolic": 80,
            "hr": 72, "temp": 37.0, "rr": 14, "spo2": 98
        }

    v = fixed["vitals"]
    defaults = {"bp_systolic": 120, "bp_diastolic": 80, "hr": 72, "temp": 37.0, "rr": 14, "spo2": 98}
    for k, default in defaults.items():
        if k not in v:
            v[k] = default
        else:
            try:
                if k == "temp":
                    v[k] = float(v[k])
                else:
                    v[k] = int(float(str(v[k]).replace(" ", "").split("/")[0].split(" ")[0]))
            except (TypeError, ValueError):
                v[k] = default

    fixed["vitals"] = v

    # chief_complaint: required
    if "chief_complaint" not in fixed or not fixed["chief_complaint"]:
        # Try presenting_complaint, presenting complaint
        fixed["chief_complaint"] = str(
            fixed.get("presenting_complaint", fixed.get("chief_complaint", ""))
        )

    # history_present_illness: required
    if "history_present_illness" not in fixed or not fixed["history_present_illness"]:
        # Try hpi field
        hpi = fixed.get("hpi", "")
        fixed["history_present_illness"] = str(hpi)

    return fixed


# ─── initial_tool_outputs ─────────────────────────────────────────────────────


def fix_csf_report(csf: dict) -> dict:
    """Normalize a CSF report to CSFResults schema."""
    fixed = dict(csf)

    # appearance: required str
    if "appearance" not in fixed or not fixed["appearance"]:
        fixed["appearance"] = "Clear, colorless"

    # opening_pressure: required str
    if "opening_pressure" not in fixed or not fixed["opening_pressure"]:
        fixed["opening_pressure"] = "normal"

    # cell_count: dict[str, str]
    if "cell_count" not in fixed:
        fixed["cell_count"] = {}
    elif not isinstance(fixed["cell_count"], dict):
        fixed["cell_count"] = {"note": str(fixed["cell_count"])}

    # protein: required str — may be inside results list
    if "protein" not in fixed or not fixed["protein"]:
        # Try to find in results list
        for item in fixed.get("results", []):
            if isinstance(item, dict) and "protein" in str(item.get("test", "")).lower():
                fixed["protein"] = str(item.get("value", ""))
                break
        if not fixed.get("protein"):
            fixed["protein"] = "normal"

    # glucose: required str
    if "glucose" not in fixed or not fixed["glucose"]:
        for item in fixed.get("results", []):
            if isinstance(item, dict) and "glucose" in str(item.get("test", "")).lower() \
                    and "csf" in str(item.get("test", "")).lower():
                fixed["glucose"] = str(item.get("value", ""))
                break
        if not fixed.get("glucose"):
            for item in fixed.get("results", []):
                if isinstance(item, dict) and "glucose" in str(item.get("test", "")).lower():
                    fixed["glucose"] = str(item.get("value", ""))
                    break
        if not fixed.get("glucose"):
            fixed["glucose"] = "normal"

    # interpretation: required str
    if "interpretation" not in fixed or not fixed["interpretation"]:
        fixed["interpretation"] = str(fixed.get("summary", fixed.get("impression", "")))
    if not fixed["interpretation"]:
        fixed["interpretation"] = "See results"

    # glucose_ratio: str (optional)
    if "glucose_ratio" not in fixed:
        fixed["glucose_ratio"] = ""

    # special_tests: dict[str, str]
    if "special_tests" not in fixed:
        fixed["special_tests"] = {}
    elif not isinstance(fixed["special_tests"], dict):
        fixed["special_tests"] = {"note": str(fixed["special_tests"])}

    # Drop non-schema fields
    for k in ["results", "report", "summary"]:
        fixed.pop(k, None)

    return fixed


def fix_tool_output_set(tos: dict) -> dict:
    """Normalize the initial_tool_outputs dict.

    Handles two cases:
    1. Canonical keys (mri, eeg, labs, etc.) — just fix internal structure
    2. Tool function name keys (analyze_brain_mri, etc.) — remap keys + fix structure
    """
    # First, remap tool function names to canonical field names
    remapped: dict[str, Any] = {}
    for key, val in tos.items():
        canonical = TOOL_NAME_TO_FIELD.get(key)
        if canonical:
            # If both the function-name key and canonical key exist, prefer the canonical
            if canonical not in remapped:
                remapped[canonical] = val
        else:
            remapped[key] = val

    # Now fix internal structure of each recognized field
    fixed = {}
    for key, val in remapped.items():
        if val is None:
            fixed[key] = None
            continue
        if not isinstance(val, dict):
            fixed[key] = val
            continue

        if key == "mri":
            fixed[key] = fix_mri_report(val)
        elif key == "eeg":
            fixed[key] = fix_eeg_report(val)
        elif key == "ct":
            fixed[key] = fix_ct_report(val)
        elif key == "labs":
            fixed[key] = fix_labs_report(val)
        elif key == "csf":
            fixed[key] = fix_csf_report(val)
        elif key == "cardiac_monitoring":
            fixed[key] = _fix_cardiac_monitoring(val)
        elif key == "echo":
            fixed[key] = _fix_echo_report(val)
        elif key == "advanced_imaging":
            fixed[key] = _fix_advanced_imaging(val)
        elif key == "specialized_test":
            fixed[key] = _fix_specialized_test(val)
        else:
            fixed[key] = val

    return fixed


# ─── followup_outputs ─────────────────────────────────────────────────────────


def _fix_findings_list(findings: Any) -> list[str]:
    """Convert findings that may be list[dict] or list[str] to list[str]."""
    if not isinstance(findings, list):
        return []
    result = []
    for item in findings:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            # Take first meaningful value
            for key in ["finding", "description", "result", "text", "value"]:
                if key in item and item[key]:
                    result.append(str(item[key]))
                    break
            else:
                # Join all values
                parts = [str(v) for v in item.values() if v]
                if parts:
                    result.append("; ".join(parts))
    return result


def _fix_quantitative_data(qd: Any) -> dict[str, str] | None:
    """Convert quantitative_data values to str."""
    if qd is None:
        return None
    if isinstance(qd, dict):
        return {str(k): str(v) for k, v in qd.items()}
    return None


def _fix_cardiac_monitoring(output: dict) -> dict:
    """Normalize CardiacMonitoringReport fields."""
    fixed = dict(output)

    # findings: list[str] (not list[dict])
    if "findings" in fixed:
        fixed["findings"] = _fix_findings_list(fixed["findings"])

    # events: list[dict[str,str]]
    if "events" in fixed and isinstance(fixed["events"], list):
        new_events = []
        for e in fixed["events"]:
            if isinstance(e, dict):
                new_events.append({str(k): str(v) for k, v in e.items()})
        fixed["events"] = new_events

    # heart_rate_range: dict[str, int]
    if "heart_rate_range" in fixed and isinstance(fixed["heart_rate_range"], dict):
        new_hrr = {}
        for k, v in fixed["heart_rate_range"].items():
            try:
                new_hrr[str(k)] = int(v)
            except (TypeError, ValueError):
                pass
        fixed["heart_rate_range"] = new_hrr

    # duration_hours: int
    if "duration_hours" not in fixed:
        # Try "duration" field
        dur = fixed.get("duration", 0)
        if isinstance(dur, str):
            import re
            match = re.search(r'\d+', dur)
            fixed["duration_hours"] = int(match.group()) if match else 0
        else:
            try:
                fixed["duration_hours"] = int(dur)
            except (TypeError, ValueError):
                fixed["duration_hours"] = 0

    # quantitative_data: not in CardiacMonitoringReport schema but
    # if present should not cause errors since it's not in the model

    return fixed


def _fix_echo_report(output: dict) -> dict:
    """Normalize EchoReport findings field (list[str] not list[dict])."""
    fixed = dict(output)
    if "findings" in fixed:
        fixed["findings"] = _fix_findings_list(fixed["findings"])
    return fixed


def _fix_advanced_imaging(output: dict) -> dict:
    """Normalize AdvancedImagingReport."""
    fixed = dict(output)
    # findings: list[dict[str,str]]
    if "findings" in fixed and isinstance(fixed["findings"], list):
        new_findings = []
        for f in fixed["findings"]:
            if isinstance(f, dict):
                new_findings.append({str(k): str(v) for k, v in f.items()})
            elif isinstance(f, str):
                new_findings.append({"description": f})
        fixed["findings"] = new_findings
    # quantitative_data: dict[str,str] | None
    if "quantitative_data" in fixed:
        fixed["quantitative_data"] = _fix_quantitative_data(fixed["quantitative_data"])
    return fixed


def _fix_specialized_test(output: dict) -> dict:
    """Normalize SpecializedTestReport."""
    fixed = dict(output)

    # test_type: may be under test_name
    if "test_type" not in fixed and "test_name" in fixed:
        fixed["test_type"] = str(fixed["test_name"])

    # findings: list[dict[str,str]] — may be a string in some cases
    raw_findings = fixed.get("findings", [])
    if isinstance(raw_findings, str):
        # Convert string to a single-item list
        raw_findings = [{"description": raw_findings}]
    if isinstance(raw_findings, list):
        new_findings = []
        for f in raw_findings:
            if isinstance(f, dict):
                new_findings.append({str(k): str(v) for k, v in f.items()})
            elif isinstance(f, str):
                new_findings.append({"description": f})
        fixed["findings"] = new_findings
    else:
        fixed["findings"] = []

    # quantitative_data: dict[str,str] | None
    if "quantitative_data" in fixed:
        fixed["quantitative_data"] = _fix_quantitative_data(fixed["quantitative_data"])

    # impression: may be under "result"
    if "impression" not in fixed or not fixed["impression"]:
        fixed["impression"] = str(fixed.get("result", fixed.get("summary", "")))

    # recommended_actions: may be under "recommendations"
    if "recommended_actions" not in fixed:
        ra = fixed.get("recommendations", [])
        fixed["recommended_actions"] = [str(x) for x in ra] if isinstance(ra, list) else []

    return fixed


def _get_minimal_valid_output(tool_name: str, fup: dict) -> dict:
    """Create a minimal valid output dict from a followup entry with non-standard fields."""
    canonical = TOOL_NAME_TO_FIELD.get(tool_name, "")
    # Collect all text from the fup for the impression
    text_fields = []
    for k in ["interpretation", "impression", "summary", "finding", "findings", "result"]:
        v = fup.get(k)
        if isinstance(v, str) and v:
            text_fields.append(v)
        elif isinstance(v, dict):
            text_fields.append(str(v))
    impression = " | ".join(text_fields) if text_fields else ""

    return _convert_report_string_to_output(canonical, {"report": impression})


def fix_followup_output(fup: dict) -> dict:
    """Normalize a single followup output entry."""
    fixed = dict(fup)

    # Ensure trigger_action exists (required field)
    if "trigger_action" not in fixed or not fixed["trigger_action"]:
        # Use timestamp + tool_name as fallback
        ts = fixed.get("timestamp", "")
        tn = fixed.get("tool_name", "unknown")
        fixed["trigger_action"] = f"{tn}_{ts}".strip("_") or "unknown_trigger"

    tool_name = fixed.get("tool_name", "")
    output = fixed.get("output", {})

    # If output is missing or empty, generate minimal valid output from other fields
    if not output or output == {}:
        fixed["output"] = _get_minimal_valid_output(tool_name, fixed)
        return fixed

    if not isinstance(output, dict):
        return fixed

    if tool_name == "analyze_brain_mri":
        fixed["output"] = fix_mri_report(output)
    elif tool_name == "analyze_eeg":
        fixed["output"] = fix_eeg_report(output)
    elif tool_name == "order_ct_scan":
        fixed["output"] = fix_ct_report(output)
    elif tool_name == "interpret_labs":
        fixed["output"] = fix_labs_report(output)
    elif tool_name == "order_cardiac_monitoring":
        fixed["output"] = _fix_cardiac_monitoring(output)
    elif tool_name == "order_echocardiogram":
        fixed["output"] = _fix_echo_report(output)
    elif tool_name == "order_advanced_imaging":
        fixed["output"] = _fix_advanced_imaging(output)
    elif tool_name == "order_specialized_test":
        fixed["output"] = _fix_specialized_test(output)
    elif tool_name == "search_medical_literature":
        # LiteratureSearchResult: needs query + summary
        if "query" not in output:
            output["query"] = str(fixed.get("query", ""))
        if "summary" not in output or not output["summary"]:
            output["summary"] = str(fixed.get("interpretation", ""))
        # Ensure results is a list of dicts with string values
        results = output.get("results", [])
        if isinstance(results, list):
            new_results = []
            for r in results:
                if isinstance(r, dict):
                    new_results.append({str(k): str(v) for k, v in r.items()})
            output["results"] = new_results
        fixed["output"] = output

    return fixed


# ─── ground_truth ─────────────────────────────────────────────────────────────


def fix_action_step(step: Any, step_num: int = 1) -> dict | None:
    """Normalize an optimal action step to ActionStep schema."""
    if isinstance(step, str):
        # Convert a plain string action to ActionStep
        return {
            "step": step_num,
            "action": step,
            "tool_name": None,
            "expected_finding": "",
            "category": "required",
            "tool_parameters": {},
        }

    if not isinstance(step, dict):
        return None

    # category must be one of the valid values
    cat = str(step.get("category", "required")).lower().strip()
    if cat not in VALID_CATEGORIES:
        cat_map = {
            "very_low": "acceptable",
            "very low": "acceptable",
            "low": "acceptable",
            "high": "required",
            "very_high": "required",
            "very high": "required",
            "moderate": "acceptable",
            "optional": "acceptable",
            "recommended": "required",
            "strongly_recommended": "required",
            "strongly recommended": "required",
            "contraindicated_if": "contraindicated",
            "do_not": "contraindicated",
            "preferred": "required",
        }
        cat = cat_map.get(cat, "acceptable")

    # tool_parameters: must be a dict
    tool_params = step.get("tool_parameters", {})
    if not isinstance(tool_params, dict):
        tool_params = {}

    # step number
    s = step.get("step", step_num)
    try:
        s = int(s)
    except (TypeError, ValueError):
        s = step_num

    return {
        "step": s,
        "action": str(step.get("action", "")),
        "tool_name": step.get("tool_name", None),
        "expected_finding": str(step.get("expected_finding", "")),
        "category": cat,
        "tool_parameters": tool_params,
    }


def fix_ground_truth(gt: dict) -> dict:
    """Normalize ground_truth to GroundTruth schema."""
    fixed = dict(gt)

    # primary_diagnosis may be a dict (HEP-ENC style)
    pd = fixed.get("primary_diagnosis", "")
    if isinstance(pd, dict):
        # Extract icd_code from nested primary_diagnosis if present
        if "icd_code" not in fixed and "icd_code" in pd:
            fixed["icd_code"] = str(pd["icd_code"])
        # Convert to string using condition or diagnosis key
        fixed["primary_diagnosis"] = str(
            pd.get("condition", pd.get("diagnosis", pd.get("name", str(pd))))
        )
    elif not pd:
        fixed["primary_diagnosis"] = str(gt.get("diagnosis", gt.get("condition_name", "")))

    # icd_code: required str
    if "icd_code" not in fixed or not fixed["icd_code"]:
        fixed["icd_code"] = str(gt.get("icd_code", ""))

    # optimal_actions: list[ActionStep]
    oa_raw = gt.get("optimal_actions", gt.get("optimal_action_sequence", []))
    if isinstance(oa_raw, list):
        new_oa = []
        for i, step in enumerate(oa_raw, start=1):
            fixed_step = fix_action_step(step, i)
            if fixed_step:
                new_oa.append(fixed_step)
        fixed["optimal_actions"] = new_oa
    else:
        fixed["optimal_actions"] = []

    # differential: list[dict[str,str]]
    diff_raw = gt.get(
        "differential",
        gt.get("differential_diagnosis", gt.get("differential_diagnoses", []))
    )
    if isinstance(diff_raw, list):
        new_diff = []
        for item in diff_raw:
            if isinstance(item, dict):
                # Normalize all values to strings
                normalized = {}
                for k, v in item.items():
                    normalized[str(k)] = str(v)
                new_diff.append(normalized)
        fixed["differential"] = new_diff

    # key_reasoning_points
    if "key_reasoning_points" not in fixed or not fixed["key_reasoning_points"]:
        alt = gt.get("key_reasoning", gt.get("reasoning_points", gt.get("key_reasoning", [])))
        if isinstance(alt, list):
            fixed["key_reasoning_points"] = [str(x) for x in alt]
        else:
            fixed["key_reasoning_points"] = []

    # critical_actions: list[str]
    if "critical_actions" not in fixed:
        fixed["critical_actions"] = []
    elif not isinstance(fixed["critical_actions"], list):
        fixed["critical_actions"] = [str(fixed["critical_actions"])]
    else:
        fixed["critical_actions"] = [
            (
                str(x) if isinstance(x, str)
                else ": ".join(str(v) for v in x.values() if v) if isinstance(x, dict)
                else str(x)
            )
            for x in fixed["critical_actions"]
        ]

    # contraindicated_actions: list[str]
    if "contraindicated_actions" not in fixed:
        fixed["contraindicated_actions"] = []
    elif not isinstance(fixed["contraindicated_actions"], list):
        fixed["contraindicated_actions"] = [str(fixed["contraindicated_actions"])]
    else:
        # May be list of dicts (HEP-ENC style) — convert to strings
        new_ca = []
        for item in fixed["contraindicated_actions"]:
            if isinstance(item, str):
                new_ca.append(item)
            elif isinstance(item, dict):
                # Combine action + reason
                parts = []
                for k in ["action", "reason", "description", "text"]:
                    if k in item and item[k]:
                        parts.append(str(item[k]))
                new_ca.append(": ".join(parts) if parts else str(item))
            else:
                new_ca.append(str(item))
        fixed["contraindicated_actions"] = new_ca

    # red_herrings: list[RedHerring]
    if "red_herrings" not in fixed:
        fixed["red_herrings"] = []
    elif not isinstance(fixed["red_herrings"], list):
        fixed["red_herrings"] = []

    # Remove keys not in schema
    keys_to_remove = [
        "optimal_action_sequence", "differential_diagnosis", "differential_diagnoses",
        "key_reasoning", "reasoning_points", "expected_agent_confidence",
        "estimated_diagnosis_difficulty", "tools_required",
    ]
    for k in keys_to_remove:
        fixed.pop(k, None)

    return fixed


# ─── Report-string conversion helpers ────────────────────────────────────────


def _convert_report_string_to_output(tool_type: str, val: dict) -> dict:
    """Convert a tool output with a 'report' string to a minimal valid schema object."""
    report_text = str(val.get("report", val.get("summary", val.get("impression", ""))))
    summary = str(val.get("summary", ""))

    if tool_type == "mri":
        return {
            "findings": [],
            "volumetrics": None,
            "additional_observations": [report_text] if report_text else [],
            "impression": summary or report_text,
            "differential_by_imaging": [],
            "recommended_actions": [],
        }
    elif tool_type == "eeg":
        return {
            "classification": "normal" if "normal" in report_text.lower() else "abnormal",
            "background": {},
            "findings": [],
            "artifacts": [],
            "activating_procedures": {},
            "impression": summary or report_text,
            "limitations": "",
            "recommended_actions": [],
        }
    elif tool_type == "ecg":
        return {
            "rhythm": "sinus rhythm",
            "rate": 72,
            "intervals": {},
            "axis": "",
            "findings": [report_text] if report_text else [],
            "interpretation": summary or report_text,
            "clinical_correlation": "",
        }
    elif tool_type == "labs":
        return {
            "panels": {},
            "interpretation": summary or report_text,
            "abnormal_values_summary": [],
        }
    elif tool_type == "csf":
        return {
            "appearance": "Clear, colorless",
            "opening_pressure": "normal",
            "cell_count": {},
            "protein": "normal",
            "glucose": "normal",
            "glucose_ratio": "",
            "special_tests": {},
            "interpretation": summary or report_text,
        }
    elif tool_type == "ct":
        return {
            "findings": [],
            "contrast_used": False,
            "angiography_findings": None,
            "additional_observations": [report_text] if report_text else [],
            "impression": summary or report_text,
            "recommended_actions": [],
        }
    elif tool_type == "echo":
        return {
            "chambers": {},
            "valves": {},
            "ejection_fraction": None,
            "wall_motion": None,
            "findings": [report_text] if report_text else [],
            "impression": summary or report_text,
            "recommended_actions": [],
        }
    elif tool_type == "cardiac_monitoring":
        return {
            "duration_hours": 0,
            "monitor_type": "",
            "rhythm_summary": summary or report_text,
            "heart_rate_range": {},
            "events": [],
            "findings": [],
            "impression": summary or report_text,
            "recommended_actions": [],
        }
    elif tool_type == "advanced_imaging":
        return {
            "modality": str(val.get("modality", "")),
            "tracer_or_protocol": None,
            "findings": [{"description": report_text}] if report_text else [],
            "quantitative_data": None,
            "impression": summary or report_text,
            "recommended_actions": [],
        }
    elif tool_type == "specialized_test":
        return {
            "test_type": str(val.get("test_type", "")),
            "findings": [{"description": report_text}] if report_text else [],
            "quantitative_data": None,
            "impression": summary or report_text,
            "recommended_actions": [],
        }
    else:
        return val


def _convert_follow_up_outputs(fups: list) -> list[dict]:
    """Convert follow_up_outputs list to followup_outputs format."""
    result = []
    for fup in fups:
        if not isinstance(fup, dict):
            continue
        # Map field names
        trigger = fup.get("trigger_action", fup.get("trigger", ""))
        tool_name = fup.get("tool_name", fup.get("tool", ""))
        output = fup.get("output", fup.get("result", {}))

        if isinstance(output, dict):
            # Apply report-string conversion if needed
            canonical = TOOL_NAME_TO_FIELD.get(tool_name, "")
            if canonical and isinstance(output.get("report"), str):
                output = _convert_report_string_to_output(canonical, output)
            else:
                # Apply standard fixup
                if tool_name == "analyze_brain_mri":
                    output = fix_mri_report(output)
                elif tool_name == "analyze_eeg":
                    output = fix_eeg_report(output)
                elif tool_name == "order_ct_scan":
                    output = fix_ct_report(output)
                elif tool_name == "interpret_labs":
                    output = fix_labs_report(output)
                elif tool_name == "order_cardiac_monitoring":
                    output = _fix_cardiac_monitoring(output)
                elif tool_name == "order_echocardiogram":
                    output = _fix_echo_report(output)
                elif tool_name == "order_advanced_imaging":
                    output = _fix_advanced_imaging(output)
                elif tool_name == "order_specialized_test":
                    output = _fix_specialized_test(output)

        result.append({
            "trigger_action": str(trigger),
            "tool_name": str(tool_name),
            "output": output,
        })
    return result


# ─── Top-level case normalization ─────────────────────────────────────────────


def normalize_case(data: dict) -> tuple[dict, list[str]]:
    """Normalize a single case dict. Returns (fixed_data, list_of_fixes)."""
    fixes: list[str] = []
    fixed = dict(data)

    # ── condition: must be a valid NeurologicalCondition enum value ───────────
    cond = str(fixed.get("condition", "")).lower().strip()
    if cond in CONDITION_MAP and CONDITION_MAP[cond] != fixed.get("condition"):
        orig_cond = fixed["condition"]
        fixed["condition"] = CONDITION_MAP[cond]
        fixes.append(f"condition: mapped '{orig_cond}' → '{fixed['condition']}'")

    # ── patient ───────────────────────────────────────────────────────────────
    if "patient" in fixed and isinstance(fixed["patient"], dict):
        # For cases where neurological_exam exists at top level but not inside patient
        patient = fixed["patient"]
        if (not patient.get("neurological_exam") or patient.get("neurological_exam") == {}) \
                and isinstance(fixed.get("neurological_exam"), dict) and fixed["neurological_exam"]:
            patient["neurological_exam"] = fixed["neurological_exam"]

        # For cases where vitals exists at top level differently (PERI-NEURO/NMDAR old format)
        if not _vitals_are_standard(patient.get("vitals", {})):
            top_vitals = fixed.get("vitals")
            if isinstance(top_vitals, dict) and _vitals_are_standard(top_vitals):
                patient["vitals"] = top_vitals

        # For cases where chief_complaint is missing but present at top level of patient
        if not patient.get("chief_complaint"):
            patient["chief_complaint"] = patient.get("presenting_complaint", "")

        # For cases where history_present_illness is empty but hpi is present
        if not patient.get("history_present_illness") and patient.get("hpi"):
            patient["history_present_illness"] = patient["hpi"]

        orig = json.dumps(patient, sort_keys=True)
        fixed["patient"] = fix_patient(patient)
        if json.dumps(fixed["patient"], sort_keys=True) != orig:
            fixes.append("patient: normalized fields")

    # ── Remap tool_outputs → initial_tool_outputs (MIG-AURA/MG-R* old format) ─
    if "tool_outputs" in fixed and "initial_tool_outputs" not in fixed:
        raw_to = fixed.pop("tool_outputs")
        if isinstance(raw_to, dict):
            # These cases use different key names and report-string format
            # Map to canonical key names
            tool_output_key_map = {
                "brain_mri": "mri",
                "mri": "mri",
                "eeg": "eeg",
                "ecg": "ecg",
                "ecg_report": "ecg",
                "labs": "labs",
                "laboratory": "labs",
                "csf": "csf",
                "csf_analysis": "csf",
                "ct_scan": "ct",
                "ct": "ct",
                "echocardiogram": "echo",
                "echo": "echo",
                "cardiac_monitoring": "cardiac_monitoring",
                "advanced_imaging": "advanced_imaging",
                "specialized_test": "specialized_test",
            }
            converted = {}
            for k, v in raw_to.items():
                canonical = tool_output_key_map.get(k.lower(), k)
                if v is None:
                    converted[canonical] = None
                elif isinstance(v, dict):
                    # Has report/summary → convert to minimal valid structure
                    converted[canonical] = _convert_report_string_to_output(canonical, v)
                elif isinstance(v, str):
                    converted[canonical] = _convert_report_string_to_output(canonical, {"report": v})
            fixed["initial_tool_outputs"] = converted
            fixes.append("initial_tool_outputs: remapped from tool_outputs")

    # ── Remap follow_up_outputs → followup_outputs ─────────────────────────
    if "follow_up_outputs" in fixed and "followup_outputs" not in fixed:
        raw_fups = fixed.pop("follow_up_outputs")
        if isinstance(raw_fups, list):
            fixed["followup_outputs"] = _convert_follow_up_outputs(raw_fups)
            fixes.append("followup_outputs: remapped from follow_up_outputs")

    # ── Ensure initial_tool_outputs exists ────────────────────────────────────
    if "initial_tool_outputs" not in fixed:
        fixed["initial_tool_outputs"] = {}
        fixes.append("initial_tool_outputs: added empty dict")

    # ── initial_tool_outputs ──────────────────────────────────────────────────
    if "initial_tool_outputs" in fixed and isinstance(fixed["initial_tool_outputs"], dict):
        tos = fixed["initial_tool_outputs"]
        orig = json.dumps(tos, sort_keys=True)
        fixed["initial_tool_outputs"] = fix_tool_output_set(tos)
        if json.dumps(fixed["initial_tool_outputs"], sort_keys=True) != orig:
            fixes.append("initial_tool_outputs: normalized")

    # ── Ensure followup_outputs exists ────────────────────────────────────────
    if "followup_outputs" not in fixed:
        fixed["followup_outputs"] = []

    # ── followup_outputs ──────────────────────────────────────────────────────
    if "followup_outputs" in fixed and isinstance(fixed["followup_outputs"], list):
        new_fups = []
        changed = False
        for fup in fixed["followup_outputs"]:
            if isinstance(fup, dict):
                new_fup = fix_followup_output(fup)
                if new_fup != fup:
                    changed = True
                new_fups.append(new_fup)
            else:
                new_fups.append(fup)
        fixed["followup_outputs"] = new_fups
        if changed:
            fixes.append("followup_outputs: normalized tool outputs")

    # ── ground_truth ──────────────────────────────────────────────────────────
    if "ground_truth" in fixed and isinstance(fixed["ground_truth"], dict):
        orig = json.dumps(fixed["ground_truth"], sort_keys=True)
        fixed["ground_truth"] = fix_ground_truth(fixed["ground_truth"])
        if json.dumps(fixed["ground_truth"], sort_keys=True) != orig:
            fixes.append("ground_truth: normalized")

    return fixed, fixes


def _vitals_are_standard(v: Any) -> bool:
    """Return True if vitals dict has all required integer/float fields."""
    if not isinstance(v, dict):
        return False
    required = ["bp_systolic", "bp_diastolic", "hr", "temp", "rr", "spo2"]
    return all(
        k in v and isinstance(v[k], (int, float))
        for k in required
    )


# ─── Main ─────────────────────────────────────────────────────────────────────


def main(dry_run: bool = False) -> None:
    cases = sorted(CASES_DIR.glob("*.json"))
    print(f"Found {len(cases)} case files in {CASES_DIR}")

    total_fixed = 0
    total_unchanged = 0
    all_fixes: dict[str, list[str]] = {}

    for path in cases:
        with open(path) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"  ERROR parsing JSON {path.name}: {e}")
                continue

        fixed, fixes = normalize_case(data)

        if fixes:
            total_fixed += 1
            all_fixes[path.name] = fixes
            if not dry_run:
                with open(path, "w") as f:
                    json.dump(fixed, f, indent=2, ensure_ascii=False)
                    f.write("\n")
        else:
            total_unchanged += 1

    print(f"\nResults:")
    print(f"  Modified:  {total_fixed}")
    print(f"  Unchanged: {total_unchanged}")

    if all_fixes:
        print(f"\nFixes applied ({len(all_fixes)} files):")
        for name, fixes in sorted(all_fixes.items()):
            print(f"  {name}:")
            for fix in fixes:
                print(f"    - {fix}")


def run_validation() -> tuple[int, int, list[str]]:
    """Validate all cases and return (valid_count, invalid_count, errors)."""
    try:
        from neuroagent_schemas.case import NeuroBenchCase
        from pydantic import ValidationError
    except ImportError:
        print("Cannot import neuroagent_schemas — skipping validation")
        return 0, 0, []

    cases = sorted(CASES_DIR.glob("*.json"))
    valid = 0
    invalid = 0
    error_summary: list[str] = []

    for path in cases:
        with open(path) as f:
            data = json.load(f)
        try:
            NeuroBenchCase.model_validate(data)
            valid += 1
        except ValidationError as e:
            invalid += 1
            for err in e.errors():
                loc = " → ".join(str(x) for x in err["loc"])
                error_summary.append(f"{path.name}: [{loc}] {err['msg']}")

    return valid, invalid, error_summary


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("DRY RUN — no files will be written\n")

    print("=== Before normalization ===")
    valid_before, invalid_before, errors_before = run_validation()
    print(f"Valid: {valid_before}, Invalid: {invalid_before}")

    print("\n=== Normalizing cases ===")
    main(dry_run=dry_run)

    if not dry_run:
        print("\n=== After normalization ===")
        valid_after, invalid_after, errors_after = run_validation()
        print(f"Valid: {valid_after}, Invalid: {invalid_after}")
        improvement = valid_after - valid_before
        print(f"\nImprovement: +{improvement} cases now valid")

        if errors_after:
            print(f"\nRemaining errors ({len(errors_after)}):")
            # Group by error type
            error_types: dict[str, int] = {}
            for e in errors_after:
                parts = e.split("] ")
                key = parts[-1] if len(parts) > 1 else e
                error_types[key] = error_types.get(key, 0) + 1
            for msg, count in sorted(error_types.items(), key=lambda x: -x[1])[:25]:
                print(f"  {count:3d}x  {msg}")

            print(f"\nSample errors (first 40):")
            for e in errors_after[:40]:
                print(f"  {e}")
