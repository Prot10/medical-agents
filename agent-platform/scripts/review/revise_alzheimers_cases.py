"""Apply Reviewer 1's Alzheimer pathway to cases, reports, and scoring.

The pre-review cases contradicted the answer shown in the review UI: every case exposed both
CSF Alzheimer biomarkers and amyloid PET, several made both mandatory, and routine EEG/ECG
reports remained callable after those rows were described as removed.  This migration makes
the review observable at case level:

* history/informant assessment, validated cognitive testing, labs and structural imaging are
  the required core;
* CSF Alzheimer biomarkers and amyloid PET are optional *alternative* routes, never a pair;
* FDG-PET (or one perfusion-SPECT example) is optional and confined to subtype uncertainty;
* ECG is removed; EEG survives only for two explicit non-routine questions (CJD and recurrent
  unresponsive spells);
* early-onset/familial genetic panels are optional and return an actual result, not boilerplate;
* one existing case exercises non-contrast CT because severe claustrophobia prevents MRI.

The migration is idempotent and touches only ``alzheimers_early`` cases.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

PET_CASES = {
    "ALZ-EARLY-P01", "ALZ-EARLY-P02", "ALZ-EARLY-P03",
    "ALZ-EARLY-RM04", "ALZ-EARLY-RP01", "ALZ-EARLY-RP02",
    "ALZ-EARLY-RP03", "ALZ-EARLY-RP05",
}
FDG_CASES = {
    "ALZ-EARLY-P01", "ALZ-EARLY-P02", "ALZ-EARLY-P03",
    "ALZ-EARLY-RM04", "ALZ-EARLY-RP01", "ALZ-EARLY-RP02",
}
SPECT_CASE = "ALZ-EARLY-RP03"
GENETIC_CASES = {
    "ALZ-EARLY-P02", "ALZ-EARLY-P03", "ALZ-EARLY-P04",
    "ALZ-EARLY-RM01", "ALZ-EARLY-RM03", "ALZ-EARLY-RP01",
    "ALZ-EARLY-RP02",
}
EEG_CASES = {"ALZ-EARLY-RP04", "ALZ-EARLY-RP05"}
CT_CASE = "ALZ-EARLY-RS05"

BASIC_LABS = ["CBC", "CMP", "TSH", "B12", "folate", "homocysteine", "magnesium", "ESR", "CRP"]
AD_CSF_TESTS = ["Abeta42", "Abeta42_40_ratio", "phospho_tau", "total_tau"]


def _modality(row: dict[str, Any]) -> str | None:
    return row.get("tool_parameters", {}).get("modality")


def _followup_modality(row: dict[str, Any]) -> str | None:
    return (row.get("output") or {}).get("modality")


def _normal_lab(test: str, value: Any, unit: str, reference: str) -> dict[str, Any]:
    return {
        "test": test, "value": value, "unit": unit, "reference_range": reference,
        "is_abnormal": False, "clinical_significance": None,
    }


def _complete_lab_panel(case: dict[str, Any]) -> None:
    panels = case["initial_tool_outputs"]["labs"].setdefault("panels", {})
    existing = json.dumps(panels).lower()
    additions = {
        "Magnesium": _normal_lab("Magnesium", 2.0, "mg/dL", "1.7-2.4"),
        "Homocysteine": _normal_lab("Homocysteine", 10.2, "umol/L", "5.0-15.0"),
        "ESR": _normal_lab("ESR", 12, "mm/h", "0-20"),
        "CRP": _normal_lab("CRP", 1.8, "mg/L", "<3.0"),
    }
    for name, result in additions.items():
        if name.lower() not in existing:
            panels.setdefault("Reviewed_cognitive_panel_additions", []).append(result)
    if case["case_id"] == "ALZ-EARLY-M04":
        for group in panels.values():
            if not isinstance(group, list):
                continue
            for result in group:
                if isinstance(result, dict) and str(result.get("test", "")).lower() == "homocysteine":
                    result.update({
                        "value": 19.8, "unit": "umol/L", "reference_range": "5.0-15.0",
                        "is_abnormal": True,
                        "clinical_significance": "Elevated with low B12 and elevated methylmalonic acid, confirming functional B12 deficiency",
                    })


def _ct_report() -> dict[str, Any]:
    return {
        "findings": [
            {
                "type": "Medial temporal volume loss", "location": "Bilateral",
                "size": "moderate", "density": None,
                "description": "Symmetric widening of the temporal horns and choroid fissures, compatible with medial temporal atrophy",
            },
            {
                "type": "Cortical volume loss", "location": "Temporoparietal, bilateral",
                "size": "mild-to-moderate", "density": None,
                "description": "Sulcal prominence greater in the temporoparietal regions than in the frontal lobes",
            },
            {
                "type": "White matter low attenuation", "location": "Periventricular, bilateral",
                "size": "mild", "density": "hypodense",
                "description": "Mild chronic small-vessel change without a strategic territorial or lacunar infarct",
            },
        ],
        "contrast_used": False,
        "angiography_findings": None,
        "additional_observations": [
            "No acute haemorrhage, large territorial infarct, mass effect or hydrocephalus",
            "MRI was not completed because severe claustrophobia persisted despite preparation and the patient declined sedation",
            "CT is less sensitive than MRI for microbleeds, subtle vascular disease and quantitative regional atrophy",
        ],
        "impression": (
            "Non-contrast CT shows bilateral medial-temporal and temporoparietal-predominant "
            "volume loss, supporting a neurodegenerative process, without mass, hydrocephalus or "
            "large infarct. The limitations of CT for microbleeds, subtle vascular disease and "
            "volumetric assessment are explicit."
        ),
        "recommended_actions": [],
    }


def _rp05_eeg() -> dict[str, Any]:
    return {
        "classification": "abnormal",
        "background": {
            "posterior_dominant_rhythm": "8 Hz posterior rhythm",
            "symmetry": "Symmetric", "anterior_posterior_gradient": "Preserved",
            "reactivity": "Reactive to eye opening",
        },
        "findings": [{
            "type": "Captured habitual spells",
            "description": "Two brief behavioural pauses were recorded without ictal EEG evolution",
            "lateralization": "None", "clinical_correlation": "No electrographic seizure",
            "location": "Diffuse",
        }],
        "artifacts": [],
        "activating_procedures": {
            "hyperventilation": "No epileptiform activation",
            "photic_stimulation": "No photoparoxysmal response",
        },
        "impression": (
            "Ambulatory video-EEG captured two habitual brief unresponsive spells without an "
            "ictal correlate. No epileptiform discharges or electrographic seizures were seen; "
            "mild diffuse slowing is nonspecific."
        ),
        "limitations": "A negative recording reduces but does not eliminate the possibility of focal seizures.",
        "recommended_actions": [],
    }


def _convert_fdg_to_spect(report: dict[str, Any]) -> dict[str, Any]:
    converted = json.loads(json.dumps(report))
    converted["modality"] = "perfusion_SPECT"
    converted["tracer_or_protocol"] = "99mTc-HMPAO brain perfusion SPECT"
    for finding in converted.get("findings", []):
        finding["signal"] = (
            finding.get("signal", "")
            .replace("hypometabolic", "hypoperfused")
            .replace("hypometabolism", "hypoperfusion")
            .replace("metabolism", "perfusion")
            .replace("metabolic", "perfusion")
        )
        finding["description"] = "Brain perfusion SPECT map"
    converted["impression"] = (
        converted.get("impression", "")
        .replace("hypometabolic", "hypoperfused")
        .replace("hypometabolism", "hypoperfusion")
        .replace("metabolic activity", "perfusion")
    )
    return converted


def _add_genetic_action(case: dict[str, Any]) -> None:
    if case["case_id"] not in GENETIC_CASES:
        return
    actions = case["ground_truth"]["optimal_actions"]
    existing = next((a for a in actions if str(a.get("tool_parameters", {}).get("test_type", "")).startswith("genetic_panel:")), None)
    if existing is None:
        actions.append({
            "step": 0,
            "action": "Offer an early-onset Alzheimer gene panel after pre-test genetic counselling; do not use APOE genotype as a diagnostic test",
            "tool_name": "order_specialized_test",
            "expected_finding": "APP, PSEN1 and PSEN2 result interpreted under ACMG criteria; most patients without a strong autosomal-dominant pedigree have no pathogenic variant",
            "category": "optional",
            "tool_parameters": {"test_type": "genetic_panel:early_onset_AD"},
            "citation": "[DETeCD_ADRD_2025]", "guideline_source": "DETeCD_ADRD_2025",
        })
    else:
        existing["category"] = "optional"
        existing["action"] = "Offer an early-onset Alzheimer gene panel after pre-test genetic counselling; do not use APOE genotype as a diagnostic test"


def _make_genetic_results_explicit(case: dict[str, Any]) -> None:
    for row in case["followup_outputs"]:
        output = row.get("output") or {}
        if output.get("test_type") != "genetic_panel:early_onset_AD":
            continue
        if case["case_id"] != "ALZ-EARLY-P04":
            output["impression"] = (
                "No pathogenic or likely pathogenic variant detected in APP, PSEN1 or PSEN2; "
                "this negative panel does not exclude Alzheimer disease."
            )


def _revise_actions(case: dict[str, Any]) -> None:
    case_id = case["case_id"]
    revised: list[dict[str, Any]] = []
    for row in case["ground_truth"]["optimal_actions"]:
        tool = row.get("tool_name")
        modality = _modality(row)
        test_type = row.get("tool_parameters", {}).get("test_type")

        if tool in {"analyze_ecg", "analyze_eeg"}:
            continue
        if tool == "analyze_csf" and case_id in PET_CASES:
            continue
        if modality == "amyloid_PET" and case_id not in PET_CASES:
            continue
        if modality == "FDG_PET" and case_id not in FDG_CASES and case_id != SPECT_CASE:
            continue
        if modality not in {None, "amyloid_PET", "FDG_PET", "perfusion_SPECT", "DaTscan"}:
            continue
        if modality == "DaTscan" and case_id != "ALZ-EARLY-RP05":
            continue
        if isinstance(test_type, str) and test_type.startswith("genetic_panel:") and case_id not in GENETIC_CASES:
            continue

        if tool == "interpret_labs":
            row["category"] = "required"
            row["tool_parameters"] = {"panels": BASIC_LABS}
            row["action"] = "Order the reviewed cognitive laboratory panel to identify reversible or contributing causes"
        elif tool == "analyze_brain_mri":
            if case_id == CT_CASE:
                continue
            row["category"] = "required"
        elif tool == "order_specialized_test" and test_type == "neuropsych_battery":
            row["category"] = "required"
        elif tool == "analyze_csf":
            row["category"] = "required" if case_id == "ALZ-EARLY-RP04" else "optional"
            row["tool_parameters"] = {
                "special_tests": (
                    AD_CSF_TESTS + ["14_3_3_protein", "RT_QuIC"]
                    if case_id == "ALZ-EARLY-RP04" else AD_CSF_TESTS
                )
            }
            row["action"] = (
                "Obtain CSF Alzheimer biomarkers as the single optional biological-confirmation route"
                if case_id != "ALZ-EARLY-RP04" else
                "Obtain CSF Alzheimer biomarkers with RT-QuIC and 14-3-3 because the rapid course raises a separate prion-disease question"
            )
        elif modality == "amyloid_PET":
            row["category"] = "optional"
            row["action"] = "Use amyloid PET as the single optional biological-confirmation route; do not add it after conclusive CSF Alzheimer biomarkers"
        elif modality == "FDG_PET":
            row["category"] = "optional"
            row["action"] = "Consider FDG-PET only after clinical assessment, labs and structural imaging if dementia subtype remains uncertain"
            if case_id == SPECT_CASE:
                row["tool_parameters"] = {"modality": "perfusion_SPECT"}
                row["action"] = "Use brain perfusion SPECT as the optional substitute when FDG-PET is unavailable and subtype remains uncertain"
        elif modality == "DaTscan":
            row["category"] = "optional"
        elif isinstance(test_type, str) and test_type.startswith("genetic_panel:"):
            row["category"] = "optional"
        elif tool == "perform_clinical_assessment":
            row["category"] = "required"
        revised.append(row)

    if case_id == CT_CASE and not any(r.get("tool_name") == "order_ct_scan" for r in revised):
        revised.append({
            "step": 0,
            "action": "Obtain a non-contrast head CT as structural imaging because severe claustrophobia makes MRI unavailable; state CT's limitations",
            "tool_name": "order_ct_scan",
            "expected_finding": "Medial-temporal and temporoparietal volume loss without mass, hydrocephalus or large infarct; CT limitations explicitly reported",
            "category": "required", "tool_parameters": {"contrast": False},
            "citation": "[NICE_NG97]", "guideline_source": "NICE_NG97",
        })
    if case_id == "ALZ-EARLY-RP05":
        revised.append({
            "step": 0,
            "action": "Obtain ambulatory video-EEG for the recurrent witnessed unresponsive spells, not as a routine Alzheimer diagnostic test",
            "tool_name": "analyze_eeg",
            "expected_finding": "Habitual pauses without ictal correlate and no epileptiform discharges",
            "category": "optional", "tool_parameters": {"eeg_type": "ambulatory"},
            "citation": "[NICE_NG217]", "guideline_source": "NICE_NG217",
        })
    if case_id == "ALZ-EARLY-RP04":
        revised.append({
            "step": 0,
            "action": "Obtain a routine EEG because CJD is an active differential in this rapidly progressive presentation; this is not routine Alzheimer testing",
            "tool_name": "analyze_eeg",
            "expected_finding": "Diffuse slowing without periodic sharp-wave complexes or seizures",
            "category": "optional", "tool_parameters": {"eeg_type": "routine"},
            "citation": "[CJD_criteria_2017]", "guideline_source": "CJD_criteria_2017",
        })

    case["ground_truth"]["optimal_actions"] = revised
    _add_genetic_action(case)


def _revise_outputs(case: dict[str, Any]) -> None:
    case_id = case["case_id"]
    initial = case["initial_tool_outputs"]
    initial.pop("ecg", None)
    if case_id not in EEG_CASES:
        initial.pop("eeg", None)
    if case_id == "ALZ-EARLY-RP05":
        initial["eeg"] = _rp05_eeg()
    if case_id in PET_CASES:
        initial.pop("csf", None)
    if case_id == CT_CASE:
        initial.pop("mri", None)
        initial["ct"] = _ct_report()

    kept: list[dict[str, Any]] = []
    for row in case["followup_outputs"]:
        tool = row.get("tool_name")
        modality = _followup_modality(row)
        output = row.get("output") or {}
        test_type = output.get("test_type")
        trigger = row.get("trigger_action", "").lower()
        if tool == "analyze_ecg" or (tool == "analyze_eeg" and case_id not in EEG_CASES):
            continue
        if tool == "analyze_csf" and case_id in PET_CASES:
            continue
        if modality == "amyloid_PET" and case_id not in PET_CASES:
            continue
        if modality == "FDG_PET" and case_id not in FDG_CASES and case_id != SPECT_CASE:
            continue
        if modality not in {None, "amyloid_PET", "FDG_PET", "perfusion_SPECT", "DaTscan"}:
            continue
        if modality == "DaTscan" and case_id != "ALZ-EARLY-RP05":
            continue
        if tool == "interpret_labs" and ("genetic" in trigger or "apoe" in trigger):
            continue
        if isinstance(test_type, str) and test_type.startswith("genetic_panel:") and case_id not in GENETIC_CASES:
            continue
        if case_id == SPECT_CASE and modality == "FDG_PET":
            row["trigger_action"] = "request_perfusion_spect_when_fdg_unavailable"
            row["tool_parameters"] = {"modality": "perfusion_SPECT"}
            row["output"] = _convert_fdg_to_spect(output)
        kept.append(row)
    case["followup_outputs"] = kept
    _make_genetic_results_explicit(case)


def _revise_scoring_and_prose(case: dict[str, Any]) -> None:
    case_id = case["case_id"]
    gt = case["ground_truth"]
    if case_id == CT_CASE:
        case.setdefault("metadata", {}).setdefault("panel_required_exemptions", {})["analyze_brain_mri"] = (
            "MRI is unavailable because severe claustrophobia persisted despite preparation and the patient declined sedation; required non-contrast CT is the structural alternative."
        )
        pmh = case["patient"]["clinical_history"]["past_medical_history"]
        note = "Severe claustrophobia; unable to complete MRI despite preparation and declines sedation"
        if note not in pmh:
            pmh.append(note)
        hpi = case["patient"]["history_present_illness"]
        sentence = " He cannot tolerate MRI because of severe claustrophobia and has declined sedation."
        if sentence.strip() not in hpi:
            case["patient"]["history_present_illness"] = hpi + sentence
        gt["useless_tools"] = [r for r in gt.get("useless_tools", []) if r.get("tool_name") != "order_ct_scan"]
        if not any(r.get("tool_name") == "analyze_brain_mri" for r in gt.get("harmful_tools", [])):
            gt.setdefault("harmful_tools", []).append({
                "tool_name": "analyze_brain_mri", "tool_parameters": {},
                "rationale": "MRI is unavailable because severe claustrophobia persisted despite preparation and the patient declines sedation; use non-contrast CT and state its limitations",
                "citation": "[NICE_NG97]",
            })
    if case_id in EEG_CASES:
        gt["useless_tools"] = [r for r in gt.get("useless_tools", []) if r.get("tool_name") != "analyze_eeg"]

    # Keep sequence rules only when both tools remain in this case, substituting CT where needed.
    tools = {r.get("tool_name") for r in gt["optimal_actions"] if r.get("tool_name")}
    constraints = []
    for row in gt.get("sequence_constraints", []):
        row = dict(row)
        if case_id == CT_CASE and row.get("before") == "analyze_brain_mri":
            row["before"] = "order_ct_scan"
        if row.get("before") in tools and row.get("after") in tools:
            constraints.append(row)
    gt["sequence_constraints"] = constraints

    if case_id == "ALZ-EARLY-P04":
        gt["primary_diagnosis"] = "Early-onset Alzheimer's disease with an autosomal-dominant family history"

    replacements = {
        "Pursue biomarker confirmation (CSF AT(N) markers or amyloid PET)": "Consider the single case-designated optional biomarker route if biological confirmation would change management or uncertainty remains",
        "Pursue biomarker confirmation (CSF ATN panel or amyloid PET)": "Consider the single case-designated optional biomarker route if biological confirmation would change management or uncertainty remains",
        "Pursue biomarker confirmation (CSF ATN profile or amyloid PET)": "Consider the single case-designated optional biomarker route if biological confirmation would change management or uncertainty remains",
        "Confirm Alzheimer biological diagnosis with CSF ATN biomarkers or amyloid PET (A+T+ pattern present)": "Consider the case-designated optional CSF biomarker route if biological confirmation would change management",
        "Use FDG-PET to characterize": "Consider optional FDG-PET, after the core assessment, to characterize",
        "biomarkers are required before excluding AD as the primary contributor": "a single optional biomarker route can clarify the primary contributor when that distinction would change management",
        "Order genetic panel for early-onset Alzheimer disease (APP, PSEN1, PSEN2) given onset before age 60 with three-generation autosomal-dominant family history — this is load-bearing for diagnosis and family counseling": "Offer optional APP/PSEN1/PSEN2 testing after genetic counselling because of the young onset and autosomal-dominant pedigree; the clinical diagnosis must not depend on testing being accepted",
    }
    critical = []
    for text in gt.get("critical_actions", []):
        for old, new in replacements.items():
            text = text.replace(old, new)
        if case_id == CT_CASE:
            text = text.replace("structural brain MRI with volumetric/dementia protocol", "non-contrast structural head CT because MRI is unavailable, with its limitations stated")
        critical.append(text)
    gt["critical_actions"] = critical

    exact_replacements = {
        "Continue the AD biomarker workup (CSF ATN or amyloid PET) despite the reversible-cause findings — correction of B12 and thyroid does not exclude coexisting AD":
            "Treat the reversible contributors; if biological confirmation would change management, use the case-designated optional CSF route rather than duplicating CSF and amyloid PET",
        "Do not defer CSF biomarkers or amyloid PET solely because reversible labs are abnormal; the biomarker workup is indicated when clinical and structural findings suggest AD regardless of metabolic comorbidities":
            "Do not assume that correction of reversible contributors excludes coexisting AD; optional CSF confirmation remains available when the result would change management",
        "Young onset with family history raises FTD; however, amnestic profile with hippocampal atrophy, A+T+ CSF biomarkers, and positive amyloid PET argue against FTD pathology":
            "Young onset raises FTD, but the amnestic profile, hippocampal atrophy and the case-designated CSF A+T+ pattern support Alzheimer pathology",
        "The ATN biomarker profile (A+: reduced CSF Aβ42; T+: markedly elevated p-tau 181; N+: elevated total tau; positive amyloid PET) satisfies NIA-AA 2018 biological definition of AD independently of clinical syndrome":
            "The case-designated CSF profile (reduced Aβ42/40 ratio with elevated p-tau and total tau) supports Alzheimer pathology without requiring a duplicate amyloid PET",
        "Confirm AD diagnosis with positive amyloid biomarkers (CSF ATN profile or amyloid PET) rather than relying solely on soft DLB-suggestive features to drive diagnosis":
            "If biological confirmation will change management, use this case's optional amyloid PET route rather than relying solely on soft DLB-suggestive features",
        "DaTscan cannot diagnose AD — it excludes DLB; convergent positive amyloid biomarkers (CSF A+T+ and positive amyloid PET) are required to confirm neurodegenerative pathology":
            "DaTscan does not diagnose AD; it addresses the DLB differential. Optional amyloid PET is the sole Alzheimer biomarker route in this case and must not be duplicated with CSF",
        "In a 76-year-old Black man with 2-year progressive amnestic syndrome and MMSE 21/30, the combination of Scheltens MTA grade 2, temporoparietal cortical volume loss, A+T+ CSF biomarkers (Abeta42 reduced, p-tau elevated), and positive amyloid PET establishes early-stage AD by NIA-AA 2018 biological criteria":
            "In this 76-year-old man, the progressive amnestic syndrome, temporoparietal volume loss and the case-designated CSF A+T+ profile support early-stage Alzheimer disease; amyloid PET is not duplicated",
        "Positive Alzheimer biomarkers (reduced CSF Abeta42/40 ratio, elevated phospho-tau; or positive amyloid PET) confirm A+T+ classification per the NIA-AA 2018 framework, establishing Alzheimer pathology as the biological substrate":
            "The case-designated optional CSF Aβ42/40 and phospho-tau profile can support Alzheimer pathology when biological confirmation would change management; amyloid PET is not duplicated",
    }

    def revise_text(value: Any) -> Any:
        if isinstance(value, str):
            value = exact_replacements.get(value, value)
            if case_id == CT_CASE:
                value = value.replace("temporoparietal rather than frontal atrophy pattern on MRI", "temporoparietal rather than frontal volume-loss pattern on non-contrast CT")
                value = value.replace("Only Fazekas grade 1 white matter changes on MRI", "Only mild periventricular low attenuation on CT")
                value = value.replace("MRI burden is insufficient", "the CT-visible vascular burden is insufficient")
                value = value.replace("temporoparietal atrophy on MRI", "temporoparietal volume loss on non-contrast CT")
            return value
        if isinstance(value, list):
            return [revise_text(item) for item in value]
        if isinstance(value, dict):
            return {key: revise_text(item) for key, item in value.items()}
        return value

    case["ground_truth"] = revise_text(case["ground_truth"])

    metadata = case.setdefault("metadata", {})
    route = (
        "required CSF Alzheimer and prion assays"
        if case_id == "ALZ-EARLY-RP04" else
        "optional amyloid PET" if case_id in PET_CASES else "optional CSF Alzheimer biomarkers"
    )
    structural = "non-contrast head CT because MRI is unavailable" if case_id == CT_CASE else "brain MRI"
    extra = []
    if case_id in FDG_CASES:
        extra.append("optional FDG-PET for the atypical subtype question")
    if case_id == SPECT_CASE:
        extra.append("optional perfusion SPECT because FDG-PET is unavailable")
    if case_id == "ALZ-EARLY-RP05":
        extra.extend(("optional DaTscan for the DLB differential", "optional ambulatory EEG for witnessed unresponsive spells"))
    if case_id == "ALZ-EARLY-RP04":
        extra.append("optional EEG for periodic complexes in the CJD differential")
    if case_id in GENETIC_CASES:
        extra.append("optional counselled APP/PSEN1/PSEN2 testing")
    actual_path = (
        f"Required core: structured assessment with informant and functional staging, validated "
        f"neuropsychological testing, the reviewed cognitive laboratory panel, and {structural}. "
        f"Biomarker route: {route}, with no duplicate CSF/PET confirmation."
    )
    if extra:
        actual_path += " Case-specific additions: " + "; ".join(extra) + "."
    metadata["difficulty_rationale"] = actual_path
    if "difficulty_description" in metadata:
        metadata["difficulty_description"] = actual_path
    if "clinical_notes" in metadata:
        metadata["clinical_notes"] = actual_path
    metadata["revision_reason"] = (
        "Independent 2026-08-10 recheck of Reviewer 1: case actions, authored reports and SFT "
        "pathway aligned; CSF and amyloid PET made non-duplicative alternatives"
    )

    def revise_points(original: list[str]) -> list[str]:
        points = []
        for point in original:
            lower = point.lower()
            if (
                "apoe" in lower
                and not point.startswith("APOE genotype is a risk modifier")
                and not point.startswith("Genetic testing is optional")
            ):
                point = "APOE genotype is a risk modifier and is not a diagnostic test for Alzheimer disease"
            if case_id in PET_CASES and "csf" in lower:
                continue
            if case_id not in PET_CASES and "amyloid pet" in lower:
                continue
            if "mandates genetic testing" in lower:
                point = "Young onset with an autosomal-dominant pedigree warrants offering APP/PSEN1/PSEN2 testing after counselling; testing remains optional"
            if "required to confirm" in lower and "biomarker" in lower:
                point = f"{route.capitalize()} may support the diagnosis when biological confirmation would change management"
            points.append(point)
        return points

    points = revise_points(metadata.get("key_educational_points", []))
    points.append(
        f"This case exposes {route} as its only biomarker route; conclusive CSF biomarkers and amyloid PET must not be ordered together"
    )
    if case_id in GENETIC_CASES:
        points.append("Genetic testing is optional and requires pre-test counselling; APOE is not used to diagnose Alzheimer disease")
    metadata["key_educational_points"] = list(dict.fromkeys(points))
    if "teaching_points" in metadata:
        metadata["teaching_points"] = list(dict.fromkeys(revise_points(metadata["teaching_points"])))

    if case_id == "ALZ-EARLY-P04":
        metadata["diagnostic_challenge"] = (
            "Young age and prior psychiatric attribution anchor away from AD; the three-generation "
            "pedigree must trigger counselling and an offer of optional testing without making the "
            "clinical diagnosis depend on test acceptance"
        )
        metadata["educational_value"] = (
            "Teaches recognition of early-onset AD with an autosomal-dominant pedigree, optional "
            "counselled genetic testing, and non-duplicative biomarker use"
        )


def revise_case(case: dict[str, Any]) -> None:
    if case.get("condition") != "alzheimers_early":
        return
    _complete_lab_panel(case)
    _revise_actions(case)
    _revise_outputs(case)
    _revise_scoring_and_prose(case)

    priority = {
        "perform_clinical_assessment": 10, "order_specialized_test": 20,
        "interpret_labs": 30, "analyze_brain_mri": 40, "order_ct_scan": 40,
        "order_advanced_imaging": 50, "analyze_csf": 60, "analyze_eeg": 70,
    }
    actions = case["ground_truth"]["optimal_actions"]
    actions.sort(key=lambda r: (priority.get(r.get("tool_name"), 5 if r.get("tool_name") is None else 80), r.get("step", 0)))
    for step, row in enumerate(actions, 1):
        row["step"] = step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("ALZ-EARLY-*.json")):
        original = path.read_text()
        case = json.loads(original)
        revise_case(case)
        rendered = json.dumps(case, indent=2, ensure_ascii=False) + "\n"
        if rendered != original:
            changed += 1
            if not args.check:
                path.write_text(rendered)
    print(f"Alzheimer cases changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
