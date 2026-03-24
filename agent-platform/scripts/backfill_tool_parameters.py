"""Backfill tool_parameters in v4 optimal_actions from action text.

Reads each v4 case, infers tool parameters from the free-text action
description, and writes the updated case back.  Parameters are used by
_compute_optimal_cost() for accurate cost estimation.

Usage:
    uv run python agent-platform/scripts/backfill_tool_parameters.py [--dry-run]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CASES_DIR = Path(__file__).resolve().parents[1] / ".." / "data" / "neurobench_v4" / "cases"


# ------------------------------------------------------------------
# Inference rules per tool
# ------------------------------------------------------------------

def _infer_mri_params(action: str) -> dict:
    text = action.lower()
    params: dict = {}

    # Protocol
    if any(k in text for k in ("epilepsy protocol", "hippocampal", "harness")):
        params["protocol"] = "epilepsy"
    elif any(k in text for k in ("stroke", "dwi", "diffusion", "mra ")):
        params["protocol"] = "stroke"
    elif any(k in text for k in ("tumor", "perfusion", "spectroscopy", "lesion", "mass")):
        params["protocol"] = "tumor"
    elif any(k in text for k in (" ms ", "multiple sclerosis", "demyelinat", "sagittal flair")):
        params["protocol"] = "ms"
    elif any(k in text for k in ("volumetric", "dementia", "hippocampal assessment", "alzheimer")):
        params["protocol"] = "dementia"
    else:
        params["protocol"] = "standard"

    # Contrast
    if any(k in text for k in ("gadolinium", "with contrast", "with and without contrast",
                                "post-contrast", "contrast-enhanced")):
        params["contrast"] = True
    else:
        params["contrast"] = False

    return params


def _infer_eeg_params(action: str) -> dict:
    text = action.lower()
    if any(k in text for k in ("video-eeg", "video eeg", "prolonged video")):
        return {"eeg_type": "video"}
    if any(k in text for k in ("continuous eeg", "continuous_icu", "icu eeg")):
        return {"eeg_type": "continuous_icu"}
    if any(k in text for k in ("ambulatory", "home monitoring")):
        return {"eeg_type": "ambulatory"}
    return {"eeg_type": "routine"}


def _infer_ct_params(action: str) -> dict:
    text = action.lower()
    params: dict = {}
    if any(k in text for k in ("cta", "angiography", "angiogram", "ct angiogr")):
        params["angiography"] = True
    else:
        params["angiography"] = False
    if "with contrast" in text and "without contrast" not in text:
        params["contrast"] = True
    elif "non-contrast" in text or "without contrast" in text:
        params["contrast"] = False
    else:
        params["contrast"] = False
    return params


def _infer_echo_params(action: str) -> dict:
    text = action.lower()
    if "transesophageal" in text or "tee" in text.split():
        return {"echo_type": "TEE"}
    if "bubble" in text or "agitated saline" in text:
        return {"echo_type": "bubble_study"}
    return {"echo_type": "TTE"}


def _infer_cardiac_monitoring_params(action: str) -> dict:
    text = action.lower()
    if any(k in text for k in ("event monitor", "event recorder", "30-day", "30 day")):
        return {"monitor_type": "event_monitor_30d"}
    if "48" in text or "72" in text:
        return {"monitor_type": "holter_48h"}
    # Check for "holter" before "telemetry" — "continuous cardiac monitoring with Holter"
    # should map to holter, not telemetry
    if "holter" in text:
        return {"monitor_type": "holter_24h"}
    if any(k in text for k in ("telemetry", "continuous cardiac", "continuous telemetry")):
        return {"monitor_type": "telemetry"}
    return {"monitor_type": "holter_24h"}


def _infer_advanced_imaging_params(action: str) -> dict:
    text = action.lower()
    if any(k in text for k in ("amyloid pet", "amyloid-pet", "amyloid plaque")):
        return {"imaging_type": "amyloid_PET"}
    if "datscan" in text or "dat scan" in text or "dopamine transporter" in text:
        return {"imaging_type": "DaTscan"}
    if any(k in text for k in ("fdg-pet", "fdg pet", "fdg_pet", "glucose metabolism")):
        return {"imaging_type": "FDG_PET"}
    if "perfusion" in text:
        return {"imaging_type": "perfusion_MRI"}
    if "spectroscopy" in text or "metabolite" in text:
        return {"imaging_type": "MR_spectroscopy"}
    if any(k in text for k in ("carotid duplex", "carotid doppler", "carotid ultrasound")):
        return {"imaging_type": "carotid_duplex"}
    # Default to FDG_PET for generic PET references
    if "pet" in text:
        return {"imaging_type": "FDG_PET"}
    return {"imaging_type": "FDG_PET"}


def _infer_specialized_test_params(action: str) -> dict:
    text = action.lower()
    if any(k in text for k in ("neuropsych", "cognitive test", "cognitive profile")):
        return {"test_type": "neuropsych_battery"}
    if any(k in text for k in ("emg", "nerve conduction", "electromyogr", "ncs")):
        return {"test_type": "emg_ncs"}
    if "visual evoked" in text or "vep" in text.split():
        return {"test_type": "vep"}
    if "somatosensory" in text or "ssep" in text.split():
        return {"test_type": "ssep"}
    if "brainstem auditory" in text or "baep" in text.split():
        return {"test_type": "baep"}
    if any(k in text for k in ("tilt table", "tilt test", "orthostatic")):
        return {"test_type": "tilt_table"}
    if any(k in text for k in ("polysomnogr", "sleep study", "sleep behavior")):
        return {"test_type": "polysomnography"}
    if any(k in text for k in ("autonomic test", "autonomic reflex", "dysautonomia")):
        return {"test_type": "autonomic_testing"}
    if "stress test" in text or "exercise test" in text:
        return {"test_type": "exercise_stress_test"}
    return {"test_type": "neuropsych_battery"}


def _infer_labs_params(action: str) -> dict:
    """Infer lab panels from action text."""
    text = action.lower()
    panels: list[str] = []

    panel_keywords = {
        "CBC": ["cbc", "complete blood count"],
        "BMP": ["bmp", "basic metabolic"],
        "CMP": ["cmp", "comprehensive metabolic"],
        "LFT": ["lft", "liver function", "hepatic panel"],
        "coagulation": ["coagulation", "coag", "inr", "pt/inr", "pt ", "aptt"],
        "thyroid": ["thyroid", "tsh"],
        "lipid": ["lipid"],
        "B12": ["b12", "vitamin b12"],
        "folate": ["folate"],
        "ESR": ["esr"],
        "CRP": ["crp", "c-reactive"],
        "troponin": ["troponin"],
        "HbA1c": ["hba1c", "a1c", "glycemic"],
        "RPR": ["rpr", "syphilis"],
        "HIV": ["hiv"],
        "drug_screen": ["drug screen", "toxicology"],
        "prolactin": ["prolactin"],
        "AED_levels": ["aed level", "antiepilep"],
        "dementia_workup": ["dementia screening", "dementia labs", "dementia workup"],
        "inflammatory_markers": ["inflammatory marker", "esr.*crp", "crp.*esr"],
        "autoimmune_encephalitis": ["autoimmune encephalitis", "nmdar antibod",
                                     "anti-nmda", "encephalitis panel"],
        "paraneoplastic": ["paraneoplastic"],
        "NMO_MOG": ["nmo", "aquaporin", "mog antibod"],
        "genetic": ["genetic", "gene panel", "apoe"],
    }

    for panel, keywords in panel_keywords.items():
        if any(kw in text for kw in keywords):
            panels.append(panel)

    if not panels:
        panels = ["CBC", "BMP"]

    return {"panels": panels}


def _infer_csf_params(action: str) -> dict:
    """Infer CSF special tests from action text."""
    text = action.lower()
    tests: list[str] = []

    test_keywords = {
        "oligoclonal_bands": ["oligoclonal"],
        "IgG_index": ["igg index"],
        "HSV_PCR": ["hsv pcr", "herpes pcr", "hsv-1"],
        "meningitis_panel": ["meningitis panel", "meningitis/encephalitis pcr",
                              "bacterial culture", "gram stain"],
        "cytology": ["cytology"],
        "flow_cytometry": ["flow cytometry"],
        "autoimmune_panel": ["autoimmune panel", "autoimmune encephalitis",
                              "nmdar antibod", "anti-nmda"],
        "14_3_3_protein": ["14-3-3"],
        "RT_QuIC": ["rt-quic"],
        "Abeta42": ["abeta42", "amyloid-beta", "aβ42", "amyloid beta"],
        "phospho_tau": ["phospho-tau", "p-tau"],
        "total_tau": ["total tau", "t-tau"],
        "NMDAR_antibodies": ["nmdar antibod", "anti-nmda"],
        "MOG_antibodies": ["mog antibod"],
    }

    for test, keywords in test_keywords.items():
        if any(kw in text for kw in keywords):
            tests.append(test)

    if tests:
        return {"special_tests": tests}
    return {}


TOOL_INFER_MAP = {
    "analyze_brain_mri": _infer_mri_params,
    "analyze_eeg": _infer_eeg_params,
    "order_ct_scan": _infer_ct_params,
    "order_echocardiogram": _infer_echo_params,
    "order_cardiac_monitoring": _infer_cardiac_monitoring_params,
    "order_advanced_imaging": _infer_advanced_imaging_params,
    "order_specialized_test": _infer_specialized_test_params,
    "interpret_labs": _infer_labs_params,
    "analyze_csf": _infer_csf_params,
}


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def backfill_case(case_data: dict) -> int:
    """Add tool_parameters to optimal_actions. Returns count of actions updated."""
    updated = 0
    for action in case_data["ground_truth"]["optimal_actions"]:
        tool_name = action.get("tool_name")
        if not tool_name:
            continue

        infer_fn = TOOL_INFER_MAP.get(tool_name)
        if infer_fn:
            params = infer_fn(action["action"])
            if params:
                action["tool_parameters"] = params
                updated += 1
        # Tools with no parameter inference (analyze_ecg, search_medical_literature,
        # check_drug_interactions) keep tool_parameters = {} (base cost only)

    return updated


def main():
    dry_run = "--dry-run" in sys.argv

    cases_dir = CASES_DIR.resolve()
    if not cases_dir.exists():
        print(f"Error: {cases_dir} not found")
        sys.exit(1)

    case_files = sorted(cases_dir.glob("*.json"))
    print(f"Processing {len(case_files)} cases (dry_run={dry_run})...")

    total_updated = 0
    for path in case_files:
        data = json.loads(path.read_text())
        count = backfill_case(data)
        total_updated += count

        if not dry_run:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

        if count > 0:
            print(f"  {data['case_id']}: {count} actions updated")

    print(f"\nDone. {total_updated} actions across {len(case_files)} cases.")
    if dry_run:
        print("(dry run — no files modified)")


if __name__ == "__main__":
    main()
