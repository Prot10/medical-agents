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
    ConditionToolMapping,
    ToolCatalog,
    ToolMeta,
    ToolOutputField,
    ToolParameter,
)
from .tool_io import output_fields_for, parameters_for

logger = logging.getLogger(__name__)

# The 12 diagnostic tools, with clinician-facing descriptions. Order is the
# canonical tool order used across the project.
_TOOL_META: list[dict[str, str | None]] = [
    {
        "name": "analyze_brain_mri",
        "label": "Brain MRI",
        "description": "Structural brain MRI with protocol selection (standard, "
        "epilepsy, stroke, tumor, MS, dementia); optional contrast.",
        "modality": "MRI",
    },
    {
        "name": "analyze_eeg",
        "label": "EEG",
        "description": "Electroencephalography — routine, ambulatory, video, or "
        "continuous ICU monitoring for epileptiform and encephalopathic patterns.",
        "modality": "EEG",
    },
    {
        "name": "analyze_ecg",
        "label": "ECG",
        "description": "12-lead electrocardiogram: rhythm, rate, intervals, axis.",
        "modality": "ECG",
    },
    {
        "name": "interpret_labs",
        "label": "Laboratory studies",
        "description": "Blood/serum panels — CBC, metabolic, coagulation, "
        "thyroid, inflammatory, autoimmune/paraneoplastic, genetic.",
        "modality": "LABS",
    },
    {
        "name": "analyze_csf",
        "label": "CSF analysis (lumbar puncture)",
        "description": "Cerebrospinal fluid studies: cell count, protein, glucose, "
        "and special tests (oligoclonal bands, PCR, antibodies, 14-3-3/RT-QuIC).",
        "modality": "CSF",
    },
    {
        "name": "order_ct_scan",
        "label": "CT scan",
        "description": "CT head with/without contrast, or CT angiography (CTA) "
        "for acute hemorrhage and vascular assessment.",
        "modality": "CT",
    },
    {
        "name": "order_echocardiogram",
        "label": "Echocardiogram",
        "description": "Cardiac echo (TTE, TEE, bubble study) for cardioembolic "
        "source and structural heart disease.",
        "modality": "echo",
    },
    {
        "name": "order_cardiac_monitoring",
        "label": "Cardiac monitoring",
        "description": "Holter, extended event monitoring, or inpatient telemetry "
        "for paroxysmal arrhythmia.",
        "modality": "cardiac_monitoring",
    },
    {
        "name": "order_advanced_imaging",
        "label": "Advanced imaging",
        "description": "PET (amyloid/tau/FDG), DaTscan, MIBG, perfusion/spectroscopy "
        "MRI, MR/CT angiography, carotid duplex, transcranial Doppler.",
        "modality": "advanced_imaging",
    },
    {
        "name": "order_specialized_test",
        "label": "Specialized test",
        "description": "EMG/NCS, repetitive nerve stimulation, biopsies, "
        "neuropsych battery, evoked potentials, autonomic/tilt testing, genetics.",
        "modality": "specialized_test",
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


def build_catalog(
    version: str,
    case_objects: dict[str, Any],
    conditions_yaml_path: Path,
    tool_costs_path: Path,
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
        mappings.append(
            ConditionToolMapping(
                condition=key,
                label=present[key],
                required_tools=required,
                optional_tools=optional,
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
