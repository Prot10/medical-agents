#!/usr/bin/env python3
"""Migrate NeuroBench v3 dataset to v4 — remap misrouted followup outputs to proper tools.

v3 hacked outputs from missing tools into existing tool schemas:
  - echocardiogram → interpret_labs (LabResults)
  - holter → analyze_ecg (ECGReport)
  - CT/CTA → analyze_brain_mri (MRIReport)
  - PET/DaTscan → analyze_brain_mri (MRIReport)
  - neuropsych → interpret_labs (LabResults)
  - etc.

v4 remaps these to proper tool names and converts output schemas where possible.
The clinical content is preserved; only the wrapping schema changes.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Trigger → new tool mapping
# ---------------------------------------------------------------------------

TRIGGER_REMAP: dict[str, str] = {
    # CT / CTA
    "request_ct_angiography": "order_ct_scan",
    "request_ct_head": "order_ct_scan",
    "request_brain_ct": "order_ct_scan",
    "request_ct_perfusion": "order_ct_scan",
    "request_ct_chest_abdomen": "order_ct_scan",
    "request_ct_chest_abdomen_pelvis": "order_ct_scan",
    "request_ct_cap": "order_ct_scan",
    # Echocardiogram
    "request_echocardiogram": "order_echocardiogram",
    # Cardiac monitoring
    "request_holter_monitor": "order_cardiac_monitoring",
    "request_holter": "order_cardiac_monitoring",
    "request_cardiac_holter": "order_cardiac_monitoring",
    "request_exercise_stress_test": "order_specialized_test",
    # Advanced imaging
    "request_amyloid_pet": "order_advanced_imaging",
    "request_fdg_pet": "order_advanced_imaging",
    "request_datscan": "order_advanced_imaging",
    "request_pet_scan": "order_advanced_imaging",
    "request_mri_perfusion": "order_advanced_imaging",
    "request_mr_spectroscopy": "order_advanced_imaging",
    "request_functional_mri": "order_advanced_imaging",
    "request_cardiac_mri": "order_advanced_imaging",
    "request_carotid_doppler": "order_advanced_imaging",
    # Specialized tests
    "request_neuropsych_testing": "order_specialized_test",
    "request_neuropsych": "order_specialized_test",
    "request_emg_ncs": "order_specialized_test",
    "request_vep": "order_specialized_test",
    "request_tilt_table": "order_specialized_test",
    "request_sleep_study": "order_specialized_test",
    "request_autonomic_testing": "order_specialized_test",
    "request_audiometry": "order_specialized_test",
    "request_oct": "order_specialized_test",
}

# Infer imaging_type or test_type from trigger
TRIGGER_SUBTYPE: dict[str, tuple[str, str]] = {
    # (param_name, param_value) to inject
    "request_amyloid_pet": ("imaging_type", "amyloid_PET"),
    "request_fdg_pet": ("imaging_type", "FDG_PET"),
    "request_datscan": ("imaging_type", "DaTscan"),
    "request_pet_scan": ("imaging_type", "FDG_PET"),
    "request_mri_perfusion": ("imaging_type", "perfusion_MRI"),
    "request_mr_spectroscopy": ("imaging_type", "MR_spectroscopy"),
    "request_functional_mri": ("imaging_type", "perfusion_MRI"),
    "request_cardiac_mri": ("imaging_type", "perfusion_MRI"),
    "request_carotid_doppler": ("imaging_type", "carotid_duplex"),
    "request_neuropsych_testing": ("test_type", "neuropsych_battery"),
    "request_neuropsych": ("test_type", "neuropsych_battery"),
    "request_emg_ncs": ("test_type", "emg_ncs"),
    "request_vep": ("test_type", "vep"),
    "request_tilt_table": ("test_type", "tilt_table"),
    "request_sleep_study": ("test_type", "polysomnography"),
    "request_autonomic_testing": ("test_type", "autonomic_testing"),
    "request_exercise_stress_test": ("test_type", "exercise_stress_test"),
    "request_audiometry": ("test_type", "baep"),
    "request_oct": ("test_type", "vep"),
}


def convert_mri_to_ct(output: dict) -> dict:
    """Convert MRIReport-shaped data to CTReport schema."""
    findings = []
    for f in output.get("findings", []):
        findings.append({
            "type": f.get("type", ""),
            "location": f.get("location", ""),
            "size": f.get("size"),
            "density": None,
            "description": "; ".join(
                f"{k}: {v}" for k, v in f.get("signal_characteristics", {}).items()
            ) if f.get("signal_characteristics") else "",
        })
    return {
        "findings": findings,
        "contrast_used": False,
        "angiography_findings": None,
        "additional_observations": output.get("additional_observations", []),
        "impression": output.get("impression", ""),
        "recommended_actions": output.get("recommended_actions", []),
    }


def convert_labs_to_echo(output: dict) -> dict:
    """Convert LabResults-shaped echo data to EchoReport schema."""
    chambers = {}
    valves = {}
    ef = None
    findings = []
    wall_motion = None

    for panel_name, values in output.get("panels", {}).items():
        for entry in values:
            test = entry.get("test", "")
            value = str(entry.get("value", ""))
            test_lower = test.lower()

            if "ejection fraction" in test_lower:
                # Try to extract numeric EF
                m = re.search(r"(\d+)", value)
                ef = float(m.group(1)) if m else None
                chambers["ejection_fraction"] = value
            elif any(kw in test_lower for kw in ["left ventricul", "lv ", "right ventricl", "rv "]):
                chambers[test] = value
            elif any(kw in test_lower for kw in ["left atri", "la ", "right atri", "ra "]):
                chambers[test] = value
            elif any(kw in test_lower for kw in ["valve", "mitral", "aortic", "tricuspid", "pulmonic"]):
                valves[test] = value
            elif "wall" in test_lower and "motion" in test_lower:
                wall_motion = value
            elif "pericardi" in test_lower:
                findings.append(f"{test}: {value}")
            else:
                findings.append(f"{test}: {value}")

    return {
        "chambers": chambers,
        "valves": valves,
        "ejection_fraction": ef,
        "wall_motion": wall_motion,
        "findings": findings,
        "impression": output.get("interpretation", ""),
        "recommended_actions": [],
    }


def convert_ecg_to_cardiac_monitoring(output: dict) -> dict:
    """Convert ECGReport-shaped Holter data to CardiacMonitoringReport schema."""
    events = []
    for finding in output.get("findings", []):
        events.append({
            "type": "finding",
            "description": finding,
        })

    # Try to extract duration from findings text
    duration = 24  # default
    for finding in output.get("findings", []):
        m = re.search(r"(\d+)[- ]hour", finding.lower())
        if m:
            duration = int(m.group(1))
            break

    return {
        "duration_hours": duration,
        "monitor_type": "holter_24h",
        "rhythm_summary": output.get("rhythm", ""),
        "heart_rate_range": {"average": output.get("rate", 0)},
        "events": events,
        "findings": output.get("findings", []),
        "impression": output.get("interpretation", ""),
        "recommended_actions": [],
    }


def convert_mri_to_advanced(output: dict, imaging_type: str) -> dict:
    """Convert MRIReport-shaped PET/DaTscan/perfusion data to AdvancedImagingReport."""
    findings = []
    for f in output.get("findings", []):
        findings.append({
            "region": f.get("location", ""),
            "signal": "; ".join(
                f"{k}: {v}" for k, v in f.get("signal_characteristics", {}).items()
            ) if f.get("signal_characteristics") else f.get("type", ""),
            "description": f.get("type", ""),
        })

    return {
        "modality": imaging_type,
        "tracer_or_protocol": None,
        "findings": findings,
        "quantitative_data": output.get("volumetrics"),
        "impression": output.get("impression", ""),
        "recommended_actions": output.get("recommended_actions", []),
    }


def convert_labs_to_specialized(output: dict, test_type: str) -> dict:
    """Convert LabResults-shaped neuropsych/EMG/etc to SpecializedTestReport."""
    findings = []
    quant = {}
    for panel_name, values in output.get("panels", {}).items():
        for entry in values:
            test = entry.get("test", "")
            value = str(entry.get("value", ""))
            unit = entry.get("unit", "")
            ref_range = entry.get("reference_range", "")
            is_abnormal = entry.get("is_abnormal", False)

            findings.append({
                "test": test,
                "value": f"{value} {unit}".strip(),
                "reference_range": ref_range,
                "abnormal": "yes" if is_abnormal else "no",
            })
            quant[test] = f"{value} {unit}".strip()

    return {
        "test_type": test_type,
        "findings": findings,
        "quantitative_data": quant if quant else None,
        "impression": output.get("interpretation", ""),
        "recommended_actions": [],
    }


def convert_ecg_to_specialized(output: dict, test_type: str) -> dict:
    """Convert ECGReport-shaped stress test to SpecializedTestReport."""
    findings = [{"description": f} for f in output.get("findings", [])]
    return {
        "test_type": test_type,
        "findings": findings,
        "quantitative_data": {
            "rhythm": output.get("rhythm", ""),
            "rate": str(output.get("rate", "")),
        },
        "impression": output.get("interpretation", ""),
        "recommended_actions": [],
    }


def migrate_followup(followup: dict) -> dict:
    """Migrate a single followup_output entry."""
    trigger = followup["trigger_action"]
    old_tool = followup["tool_name"]
    output = followup["output"]

    new_tool = TRIGGER_REMAP.get(trigger)
    if new_tool is None:
        # No remap needed — keep as-is
        return followup

    new_output = output  # default: keep original

    # Convert output schema based on old → new tool mapping
    if new_tool == "order_ct_scan" and old_tool == "analyze_brain_mri":
        new_output = convert_mri_to_ct(output)
    elif new_tool == "order_echocardiogram" and old_tool == "interpret_labs":
        new_output = convert_labs_to_echo(output)
    elif new_tool == "order_cardiac_monitoring" and old_tool == "analyze_ecg":
        new_output = convert_ecg_to_cardiac_monitoring(output)
    elif new_tool == "order_advanced_imaging" and old_tool == "analyze_brain_mri":
        subtype = TRIGGER_SUBTYPE.get(trigger, ("imaging_type", "FDG_PET"))
        new_output = convert_mri_to_advanced(output, subtype[1])
    elif new_tool == "order_specialized_test" and old_tool == "interpret_labs":
        subtype = TRIGGER_SUBTYPE.get(trigger, ("test_type", "neuropsych_battery"))
        new_output = convert_labs_to_specialized(output, subtype[1])
    elif new_tool == "order_specialized_test" and old_tool == "analyze_ecg":
        subtype = TRIGGER_SUBTYPE.get(trigger, ("test_type", "exercise_stress_test"))
        new_output = convert_ecg_to_specialized(output, subtype[1])

    return {
        "trigger_action": trigger,
        "tool_name": new_tool,
        "output": new_output,
    }


def update_optimal_actions(actions: list[dict]) -> list[dict]:
    """Update ground_truth.optimal_actions tool_name references for new tools."""
    updated = []
    for action in actions:
        a = dict(action)
        tool = a.get("tool_name")
        text = a.get("action", "").lower()

        if tool is None:
            updated.append(a)
            continue

        # Remap based on action text content
        if tool == "analyze_brain_mri":
            if any(kw in text for kw in ["ct scan", "ct head", "ct brain", "non-contrast ct"]):
                a["tool_name"] = "order_ct_scan"
            elif any(kw in text for kw in ["ct angiogr", "cta"]):
                a["tool_name"] = "order_ct_scan"
            elif any(kw in text for kw in ["amyloid pet", "fdg-pet", "fdg pet", "pet scan"]):
                a["tool_name"] = "order_advanced_imaging"
            elif any(kw in text for kw in ["datscan", "dat scan", "dat-scan"]):
                a["tool_name"] = "order_advanced_imaging"
            elif any(kw in text for kw in ["perfusion"]):
                a["tool_name"] = "order_advanced_imaging"
            elif any(kw in text for kw in ["spectroscopy"]):
                a["tool_name"] = "order_advanced_imaging"
            elif any(kw in text for kw in ["carotid duplex", "carotid doppler", "carotid ultrasound"]):
                a["tool_name"] = "order_advanced_imaging"
            elif any(kw in text for kw in ["cardiac mri"]):
                a["tool_name"] = "order_advanced_imaging"

        elif tool == "interpret_labs":
            if any(kw in text for kw in ["echocardiogr", "echocard", "tte", "tee", "transthoracic"]):
                a["tool_name"] = "order_echocardiogram"
            elif any(kw in text for kw in ["neuropsych", "cognitive test", "mmse", "moca"]):
                a["tool_name"] = "order_specialized_test"
            elif any(kw in text for kw in ["emg", "nerve conduction", "electromyogr"]):
                a["tool_name"] = "order_specialized_test"
            elif any(kw in text for kw in ["evoked potential", "vep", "ssep", "baep"]):
                a["tool_name"] = "order_specialized_test"
            elif any(kw in text for kw in ["tilt table", "tilt test"]):
                a["tool_name"] = "order_specialized_test"
            elif any(kw in text for kw in ["polysomnogr", "sleep study"]):
                a["tool_name"] = "order_specialized_test"
            elif any(kw in text for kw in ["autonomic test"]):
                a["tool_name"] = "order_specialized_test"

        elif tool == "analyze_ecg":
            if any(kw in text for kw in ["holter", "cardiac monitor", "event monitor", "telemetry"]):
                a["tool_name"] = "order_cardiac_monitoring"
            elif any(kw in text for kw in ["stress test"]):
                a["tool_name"] = "order_specialized_test"

        updated.append(a)
    return updated


def migrate_case(case_data: dict) -> dict:
    """Migrate a single NeuroBench case from v3 to v4."""
    case = json.loads(json.dumps(case_data))  # deep copy

    # Migrate followup outputs
    case["followup_outputs"] = [
        migrate_followup(fu) for fu in case.get("followup_outputs", [])
    ]

    # Update ground truth optimal_actions tool references
    gt = case.get("ground_truth", {})
    if "optimal_actions" in gt:
        gt["optimal_actions"] = update_optimal_actions(gt["optimal_actions"])

    return case


def main():
    src_dir = Path("data/neurobench_v3/cases")
    dst_dir = Path("data/neurobench_v4/cases")
    dst_dir.mkdir(parents=True, exist_ok=True)

    if not src_dir.exists():
        print(f"Source directory {src_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    cases = sorted(src_dir.glob("*.json"))
    print(f"Migrating {len(cases)} cases from v3 → v4...")

    stats = {"remapped": 0, "kept": 0, "total_followups": 0}

    for case_path in cases:
        with open(case_path) as f:
            data = json.load(f)

        migrated = migrate_case(data)

        # Count remaps
        for old, new in zip(data.get("followup_outputs", []), migrated["followup_outputs"]):
            stats["total_followups"] += 1
            if old["tool_name"] != new["tool_name"]:
                stats["remapped"] += 1
            else:
                stats["kept"] += 1

        dst_path = dst_dir / case_path.name
        with open(dst_path, "w") as f:
            json.dump(migrated, f, indent=2)

    print(f"Done. {stats['remapped']} followups remapped, {stats['kept']} kept as-is "
          f"(out of {stats['total_followups']} total).")
    print(f"Output: {dst_dir}")

    # Validate all cases load
    print("Validating schemas...")
    sys.path.insert(0, str(Path("packages/neuroagent-schemas/src")))
    from neuroagent_schemas import NeuroBenchCase

    errors = 0
    for case_path in sorted(dst_dir.glob("*.json")):
        try:
            with open(case_path) as f:
                data = json.load(f)
            NeuroBenchCase(**data)
        except Exception as e:
            print(f"  FAIL: {case_path.name}: {e}")
            errors += 1

    if errors:
        print(f"{errors} validation errors!")
        sys.exit(1)
    else:
        print(f"All {len(cases)} cases validated OK.")


if __name__ == "__main__":
    main()
