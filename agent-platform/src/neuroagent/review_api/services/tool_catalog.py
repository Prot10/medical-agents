"""Build the read-only tool catalog grouped by condition.

The catalog joins three sources:

* the dataset's actual conditions (``case.condition.value``),
* the per-condition ``required_modalities`` / ``optional_modalities`` in
  ``dataset-generation/config/conditions.yaml``,
* the tool list + cost ranges in ``agent-platform/config/tools/costs.yaml``.

Condition keys in the cases are the ``NeurologicalCondition`` enum values
(e.g. ``ftd``); a few differ from the ``conditions.yaml`` top-level keys
(e.g. ``frontotemporal_dementia``) and are reconciled via ``_CONDITION_ALIAS``.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from ..schemas.tool_review import (
    ConditionToolGuidance,
    ConditionToolMapping,
    ToolCatalog,
    ToolMeta,
    ToolOutputField,
    ToolParameter,
)
from .tool_io import output_fields_for, parameters_for

logger = logging.getLogger(__name__)

# The 16 diagnostic tools, with clinician-facing descriptions. Order is the
# canonical tool order used across the project.
#
# These are the strings the clinical reviewers quoted back as "current description (to be
# removed)" — the catalog text, not the agent-facing `parameter_schema`. Where their rewrite
# is a property of the study itself it is applied here. Where it is a property of the
# *condition* ("mandatory if the head CT is negative", "not indicated in syncope") it cannot
# be: the catalog shows one description per tool across all conditions, and a
# condition-specific indication in the agent-facing text would hand the agent the diagnosis it
# is meant to infer.
#
# The condition-specific half is not dropped: it is served from
# `config/review/condition_tool_guidance.yaml` beside each condition-tool row, with the
# reviewer's own text, their source and what we did about it. Until that file existed, 35 of
# the 91 annotations landed on three tools whose description was never touched — brain MRI,
# EEG and specialized test — so a reviewer logging back in would have read the exact string
# they had asked us to delete. All three are rewritten below, and none of them now claims a
# per-condition indication.
_TOOL_META: list[dict[str, str | None]] = [
    {
        "name": "analyze_brain_mri",
        "label": "Brain MRI",
        # Six protocols, from costs.yaml. The reviewers' objection was that the list reads as
        # a menu with no consequence and that the cord is not here: spinal imaging is
        # order_body_imaging{spine_MRI}, a separate study at a separate price, which is what
        # made "brain and cord MRI" scoreable at all.
        "description": "Structural brain MRI. The protocol is part of the request "
        "(standard, epilepsy, stroke, tumor, MS, dementia) and so is contrast, which is not a "
        "formality: in some indications a non-enhanced study cannot answer the question. "
        "Covers the brain only — spinal cord imaging is a separate study under body imaging.",
        "modality": "MRI",
    },
    {
        "name": "analyze_eeg",
        "label": "EEG",
        # The modality is the decision here, not the tool: a 30-60 minute routine study and
        # continuous ICU monitoring answer different questions, and several reviewers noted
        # that the shared text gave no signal of that.
        "description": "Electroencephalography for epileptiform and encephalopathic patterns. "
        "The recording type is the substance of the request: routine (awake, 30-60 min), "
        "sleep-deprived or ambulatory to capture events, video for semiology, continuous ICU "
        "monitoring where consciousness is impaired or the patient is sedated or paralysed. A "
        "normal recording does not exclude epilepsy.",
        "modality": "EEG",
    },
    {
        "name": "analyze_ecg",
        "label": "ECG",
        "description": "12-lead electrocardiogram: rhythm, rate, PR/QRS/QT-QTc "
        "intervals, axis, conduction and repolarization. A normal tracing does not "
        "exclude a paroxysmal arrhythmia.",
        "modality": "ECG",
    },
    {
        "name": "interpret_labs",
        "label": "Laboratory studies",
        "description": "Named blood and serum assays, ordered individually rather "
        "than as a routine battery: 154 priced analytes and panels, each scored and "
        "billed separately, from EUR 5 (glucose) to EUR 2300 (paraneoplastic "
        "antibodies).",
        "modality": "LABS",
    },
    {
        "name": "analyze_csf",
        "label": "CSF analysis (lumbar puncture)",
        "description": "Cerebrospinal fluid studies. Opening pressure, cell count "
        "with first-to-last tube comparison, protein and glucose are always "
        "reported; 22 further assays are named and priced individually, from the "
        "IgG index to spectrophotometry for xanthochromia, PCR, autoimmune and "
        "prion panels.",
        "modality": "CSF",
    },
    {
        "name": "order_ct_scan",
        "label": "CT scan (head and neck)",
        "description": "CT of the head and neck only, with or without contrast, or "
        "CT angiography for cervical and intracranial vessels. Thoracic, abdominal "
        "and spinal CT — including CT pulmonary angiography — is body imaging; a "
        "coronary study is advanced imaging.",
        "modality": "CT",
    },
    {
        "name": "order_echocardiogram",
        "label": "Echocardiogram",
        "description": "Ventricular size and systolic function, wall thickness, "
        "valve morphology and gradients, atrial size, pulmonary pressures, "
        "pericardium, intracardiac masses. Transthoracic, transoesophageal, "
        "agitated-saline shunt study, or imaging during graded exercise for a "
        "provoked outflow gradient.",
        "modality": "echo",
    },
    {
        "name": "order_cardiac_monitoring",
        "label": "Cardiac monitoring",
        "description": "Non-invasive rhythm monitoring for symptom–rhythm "
        "correlation, with the modality chosen from event frequency: inpatient "
        "telemetry, 24–48 h Holter, external event monitor, implantable loop "
        "recorder.",
        "modality": "cardiac_monitoring",
    },
    {
        "name": "order_advanced_imaging",
        "label": "Advanced imaging",
        "description": "PET (amyloid, tau, cerebral and cardiac FDG, amino-acid "
        "tracers), DaTscan, MIBG, MR and CT perfusion, MR spectroscopy, MR "
        "angiography and venography, carotid duplex, transcranial Doppler, and "
        "second-line cardiac imaging (cardiac MRI, coronary CTA, coronary "
        "angiography).",
        "modality": "advanced_imaging",
    },
    {
        "name": "order_specialized_test",
        "label": "Specialized test",
        # Seven annotations quoted the previous string as "too broad" or "inappropriate", in
        # multiple sclerosis, FTD, Parkinson's, NPH, ALS, GBS and myasthenia. It was a bag of
        # categories; the named test is what is ordered, priced and scored, so the named tests
        # are what the description lists.
        "description": "One named test, not a category — the value chosen is what is billed "
        "and scored. Nerve and muscle: emg_ncs, repetitive_nerve_stimulation, "
        "emg_single_fiber, respiratory_function, muscle_biopsy, nerve_biopsy, "
        "skin_biopsy_iencf, minor_salivary_gland_biopsy, ice_pack_test. Evoked potentials: "
        "vep, ssep, baep. Vision: optical_coherence_tomography, visual_field_perimetry. "
        "Autonomic and cardiac provocation: autonomic_testing, tilt_table, "
        "exercise_stress_test. Cognition and sleep: neuropsych_battery, polysomnography. "
        "Genetics: genetic_panel:<panel> for a named panel.",
        "modality": "specialized_test",
    },
    # Added after the July 2026 clinical tool review, which found the action space could
    # only image the brain and could not obtain a specimen.
    {
        "name": "order_body_imaging",
        "label": "Body imaging",
        "description": "Cross-sectional imaging outside the CNS: pelvis/abdomen "
        "(occult tumour, portosystemic shunts), chest and thoracic CT angiography "
        "(pulmonary embolism, aortic dissection, intrathoracic mass), mediastinum "
        "(thymoma), spine (cord compression), peripheral nerve.",
        "modality": "body_imaging",
    },
    {
        "name": "order_microbiology",
        "label": "Microbiology (non-CSF)",
        "description": "Blood cultures, whole-blood PCR, throat swab, urine, and "
        "diagnostic paracentesis with ascitic fluid studies.",
        "modality": "microbiology",
    },
    {
        "name": "obtain_tissue_diagnosis",
        "label": "Tissue diagnosis",
        "description": "Resection, stereotactic biopsy or nodal sampling, with the "
        "integrated histopathological report — and, where the entity requires it, the "
        "molecular layer (IDH, 1p/19q, CDKN2A/B, MGMT, ATRX, TERT, H3K27).",
        "modality": "tissue_diagnosis",
    },
    {
        "name": "perform_clinical_assessment",
        "label": "Clinical assessment",
        "description": "Structured bedside assessment: cognitive screen, ICHD-3 "
        "headache/aura history, timed gait and balance, positive functional signs.",
        "modality": "clinical_assessment",
    },
    {
        "name": "search_medical_literature",
        "label": "Literature search",
        "description": "Retrieve published evidence relevant to a clinical question.",
        "modality": None,
    },
    {
        "name": "check_drug_interactions",
        "label": "Drug interaction check",
        "description": "Screen a proposed medication against current drugs and "
        "conditions for interactions and contraindications.",
        "modality": None,
    },
]

# Modality tokens used in conditions.yaml -> canonical tool name.
_MODALITY_TO_TOOL: dict[str, str] = {
    "EEG": "analyze_eeg",
    "MRI": "analyze_brain_mri",
    "ECG": "analyze_ecg",
    "LABS": "interpret_labs",
    "CSF": "analyze_csf",
    "CT": "order_ct_scan",
    "echo": "order_echocardiogram",
    "cardiac_monitoring": "order_cardiac_monitoring",
    "advanced_imaging": "order_advanced_imaging",
    "specialized_test": "order_specialized_test",
    "EMG_NCS": "order_specialized_test",
    "body_imaging": "order_body_imaging",
    "microbiology": "order_microbiology",
    "tissue_diagnosis": "obtain_tissue_diagnosis",
    "clinical_assessment": "perform_clinical_assessment",
}

# Tools available for every condition regardless of modality.
_UNIVERSAL_TOOLS: list[str] = [
    "search_medical_literature",
    "check_drug_interactions",
]

# Enum value (in cases) -> conditions.yaml top-level key, where they differ.
_CONDITION_ALIAS: dict[str, str] = {
    "ftd": "frontotemporal_dementia",
    "nph": "normal_pressure_hydrocephalus",
    "als": "amyotrophic_lateral_sclerosis",
}


def _modalities_to_tools(tokens: list[str]) -> list[str]:
    """Map a list of modality tokens to ordered, de-duplicated tool names."""
    tools: list[str] = []
    for token in tokens:
        tool = _MODALITY_TO_TOOL.get(token)
        if tool is None:
            logger.warning("Unmapped modality token in conditions.yaml: %r", token)
            continue
        if tool not in tools:
            tools.append(tool)
    return tools


def _cost_summary(tool_name: str, costs: dict[str, Any]) -> str | None:
    """Produce an honest cost *floor* label from config/tools/costs.yaml.

    Tool specs mix additive forms (``base`` + ``modifiers``) and
    alternative-option maps (``by_type`` / ``by_panel``); a precise range
    is ambiguous, so we report the entry charge (``from €X``) which is never
    misleading. Free tools render as ``free``. Values are in EUR — see
    ``config/tools/costs.yaml`` for sourcing notes.
    """
    spec = (costs.get("tools") or {}).get(tool_name)
    if spec is None:
        return None

    if isinstance(spec, (int, float)):
        return "free" if spec == 0 else f"€{int(spec)}"

    if not isinstance(spec, dict):
        return None

    # Floor of a study = its fixed base, or the cheapest option offered.
    if "base" in spec and isinstance(spec["base"], (int, float)):
        floor = float(spec["base"])
    else:
        option_values: list[float] = []
        for value in spec.values():
            if isinstance(value, dict):
                option_values.extend(
                    float(v) for v in value.values() if isinstance(v, (int, float))
                )
            elif isinstance(value, (int, float)):
                option_values.append(float(value))
        positive = [v for v in option_values if v > 0]
        if not option_values:
            return None
        floor = min(positive) if positive else 0.0

    if floor == 0:
        return "free"
    return f"from €{int(floor)}"


def _build_parameters(tool_name: str) -> list[ToolParameter]:
    """Flatten the agent's parameter JSON Schema into the ToolParameter list
    the review UI renders."""
    schema = parameters_for(tool_name)
    if schema is None:
        return []
    required = set(schema.get("required") or [])
    out: list[ToolParameter] = []
    for key, spec in (schema.get("properties") or {}).items():
        if not isinstance(spec, dict):
            continue
        items = spec.get("items") if isinstance(spec.get("items"), dict) else None
        default = spec.get("default")
        # Only surface JSON-serialisable defaults to ToolParameter; complex
        # defaults (objects, arrays) would inflate the catalog payload.
        if not isinstance(default, (str, int, bool)) and default is not None:
            default = None
        out.append(
            ToolParameter(
                name=key,
                type=str(spec.get("type") or "string"),
                description=str(spec.get("description") or ""),
                required=key in required,
                enum=list(spec["enum"]) if isinstance(spec.get("enum"), list) else None,
                default=default,
                items_type=str(items.get("type")) if items else None,
            )
        )
    return out


def _build_output_fields(tool_name: str) -> list[ToolOutputField]:
    """Derive the return-shape summary from the Pydantic output model."""
    raw = output_fields_for(tool_name)
    if raw is None:
        return []
    return [
        ToolOutputField(
            name=r["name"],
            type=r["type"],
            description=r["description"],
            required=r["required"],
        )
        for r in raw
    ]


def _load_guidance(path: Path | None) -> dict[str, dict[str, ConditionToolGuidance]]:
    """The clinical reviewers' per-condition guidance, keyed condition -> tool.

    Absent or malformed, the catalog is served without it: a reviewer must be able to work
    even if this file is missing, and a validation error here must not take down the app.
    """
    if path is None or not path.exists():
        logger.warning("Condition-tool guidance not found at %s", path)
        return {}
    raw = yaml.safe_load(path.read_text()) or {}
    out: dict[str, dict[str, ConditionToolGuidance]] = {}
    for condition, tools in raw.items():
        if not isinstance(tools, dict):
            continue
        for tool, entry in tools.items():
            try:
                out.setdefault(condition, {})[tool] = ConditionToolGuidance.model_validate(entry)
            except Exception:  # pragma: no cover — a bad row must not hide the good ones
                logger.exception("Bad guidance entry for %s/%s", condition, tool)
    return out


def build_catalog(
    version: str,
    case_objects: dict[str, Any],
    conditions_yaml_path: Path,
    tool_costs_path: Path,
    guidance_path: Path | None = None,
) -> ToolCatalog:
    """Assemble the tool catalog for ``version`` from the loaded cases."""
    conditions_spec: dict[str, Any] = {}
    if conditions_yaml_path.exists():
        conditions_spec = yaml.safe_load(conditions_yaml_path.read_text()) or {}
    else:  # pragma: no cover — misconfiguration
        logger.warning("conditions.yaml not found at %s", conditions_yaml_path)

    tool_costs: dict[str, Any] = {}
    if tool_costs_path.exists():
        tool_costs = yaml.safe_load(tool_costs_path.read_text()) or {}
    else:  # pragma: no cover
        logger.warning("Tool costs config not found at %s", tool_costs_path)

    guidance = _load_guidance(guidance_path)

    tools = [
        ToolMeta(
            name=m["name"],
            label=m["label"],
            description=m["description"],
            modality=m["modality"],
            cost_summary=_cost_summary(m["name"], tool_costs),
            parameters=_build_parameters(m["name"]),
            output_fields=_build_output_fields(m["name"]),
        )
        for m in _TOOL_META
    ]

    # Distinct conditions actually present in this dataset version.
    present: dict[str, str] = {}  # enum value -> a display label
    for case in case_objects.values():
        key = case.condition.value
        if key in present:
            continue
        yaml_key = _CONDITION_ALIAS.get(key, key)
        entry = conditions_spec.get(yaml_key) or {}
        present[key] = entry.get("name") or key.replace("_", " ").title()

    mappings: list[ConditionToolMapping] = []
    referenced_tools: set[str] = set(_UNIVERSAL_TOOLS)
    for key in sorted(present):
        yaml_key = _CONDITION_ALIAS.get(key, key)
        entry = conditions_spec.get(yaml_key) or {}
        required = _modalities_to_tools(entry.get("required_modalities") or [])
        optional = _modalities_to_tools(entry.get("optional_modalities") or [])
        # A tool that is both required and optional is just required.
        optional = [t for t in optional if t not in required]
        referenced_tools.update(required)
        referenced_tools.update(optional)
        # A tool the review asked for and no case orders yet still carries guidance, and it
        # still counts as referenced: leaving it out of `referenced_tools` would report it as
        # an unmapped tool, which is the opposite of what the review established.
        for_condition = guidance.get(key, {})
        referenced_tools.update(for_condition)
        mappings.append(
            ConditionToolMapping(
                condition=key,
                label=present[key],
                required_tools=required,
                optional_tools=optional,
                guidance=for_condition,
            )
        )

    unmapped = [m["name"] for m in _TOOL_META if m["name"] not in referenced_tools]

    return ToolCatalog(
        version=version,
        tools=tools,
        universal_tools=list(_UNIVERSAL_TOOLS),
        conditions=mappings,
        unmapped_tools=unmapped,
    )
