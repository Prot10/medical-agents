"""Per-tool I/O schemas for the Tool Catalog view.

The review_api ships isolated from ``agent-platform/src/neuroagent/tools/`` —
the deploy script only rsyncs ``review_api/`` and the workspace ``__init__.py``.
So the agent-facing ``parameter_schema`` dicts that live next to each tool's
``execute()`` method aren't importable here. We mirror them verbatim below.

**KEEP IN SYNC** with ``agent-platform/src/neuroagent/tools/*.py``. The truth is
the tool class's ``parameter_schema`` attribute, and
``tests/test_tool_io_schemas.py::test_tool_io_schemas_match`` diffs this mirror
against the real classes so drift fails CI.

That test exists because the mirror *did* drift, silently, and it mattered. The
catchall tools' vocabularies are generated from ``costs.yaml`` in the real tools
(see ``tools/vocabulary.py``); commit 9a0636c moved them onto that single source
but only renamed ``imaging_type`` -> ``modality`` here, leaving the stale enum
lists behind. Between 2026-07-19 and 2026-07-27 the clinical reviewers therefore
assessed the tool catalog against 9 of 21 specialized tests, 6 of 12 imaging
modalities and 4 of 6 cardiac monitors, and reported as "missing" six studies the
agent could already order. The vocabulary-bearing parameters are consequently no
longer written out here at all: they are injected from ``costs.yaml``, which the
review_api already loads, so this file cannot go stale on them again.

Return shapes are derived from the Pydantic models in
``neuroagent_schemas.tool_outputs`` — those ARE shipped, so no mirror is needed
for outputs.
"""

from __future__ import annotations

import copy
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, get_args, get_origin

import yaml
from neuroagent_schemas.case import _TOOL_OUTPUT_MODEL
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from ..config import TOOL_COSTS_PATH

logger = logging.getLogger(__name__)

# --- Vocabularies derived from costs.yaml -----------------------------
#
# `(tool, parameter) -> costs.yaml block` for every parameter whose enum is a
# closed vocabulary priced in costs.yaml. Mirrors tools/vocabulary.py, which the
# real tool classes use; kept separate only because tools/ is not shipped to the
# review VPS. Sorted, so enum order matches the real schema exactly.
_COSTS_DERIVED_ENUMS: dict[tuple[str, str], tuple[str, str]] = {
    ("order_advanced_imaging", "modality"): ("order_advanced_imaging", "by_type"),
    ("order_specialized_test", "test_type"): ("order_specialized_test", "by_type"),
    ("order_cardiac_monitoring", "monitor_type"): ("order_cardiac_monitoring", "by_type"),
}

@lru_cache(maxsize=4)
def _load_tool_costs(costs_path: Path = TOOL_COSTS_PATH) -> dict[str, Any]:
    if not costs_path.exists():  # pragma: no cover — misconfiguration
        logger.warning("Tool costs config not found at %s", costs_path)
        return {}
    with open(costs_path) as f:
        return (yaml.safe_load(f) or {}).get("tools", {})


def _vocabulary(tool_name: str, parameter: str) -> list[str] | None:
    """The closed enum for a costs-derived parameter, or None if not one."""
    block = _COSTS_DERIVED_ENUMS.get((tool_name, parameter))
    if block is None:
        return None
    tool_block, key = block
    return sorted(_load_tool_costs().get(tool_block, {}).get(key, {}))


# --- Parameter schemas (verbatim mirror of tools/*.py) ----------------
#
# Parameters listed in `_COSTS_DERIVED_ENUMS` intentionally carry no `enum` key
# here — `parameters_for()` injects it from costs.yaml.

_TOOL_PARAMETERS: dict[str, dict[str, Any]] = {
    "analyze_brain_mri": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context and indication for the MRI.",
            },
            "protocol": {
                "type": "string",
                "enum": ["standard", "epilepsy", "stroke", "tumor", "ms", "dementia"],
                "description": (
                    "MRI protocol to use. 'epilepsy': thin coronal hippocampal cuts (ILAE HARNESS-MRI). "
                    "'stroke': DWI emphasis + MRA. 'tumor': includes perfusion-weighted sequences. "
                    "'ms': sagittal FLAIR + post-contrast T1. 'dementia': volumetric with hippocampal assessment. "
                    "'standard': general brain screen."
                ),
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether gadolinium contrast is needed (e.g., for tumor, MS, infection).",
            },
        },
        "required": ["clinical_context"],
    },
    "analyze_eeg": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the EEG interpretation.",
            },
            "eeg_type": {
                "type": "string",
                "enum": ["routine", "ambulatory", "video", "continuous_icu"],
                "description": (
                    "Type of EEG study. 'routine': 20-40 min outpatient. "
                    "'ambulatory': 24-72 hr home monitoring. "
                    "'video': inpatient video-EEG monitoring (epilepsy surgery workup). "
                    "'continuous_icu': ICU continuous EEG for status monitoring."
                ),
                "default": "routine",
            },
            "patient_age": {
                "type": "integer",
                "description": "Patient age in years.",
            },
            "focus_areas": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Specific areas or patterns to focus on.",
            },
        },
        "required": ["clinical_context"],
    },
    "analyze_ecg": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the ECG interpretation.",
            },
        },
        "required": ["clinical_context"],
    },
    "interpret_labs": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for lab interpretation.",
            },
            "panels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Which lab panels to interpret (e.g., CBC, BMP, LFT, thyroid).",
            },
            "patient_age": {
                "type": "integer",
                "description": "Patient age in years.",
            },
            "patient_sex": {
                "type": "string",
                "description": "Patient sex (e.g., male, female).",
            },
        },
        "required": ["clinical_context"],
    },
    "analyze_csf": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for CSF interpretation.",
            },
            "special_tests": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Special CSF tests to interpret (e.g., HSV PCR, oligoclonal bands).",
            },
        },
        "required": ["clinical_context"],
    },
    "order_ct_scan": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the CT scan.",
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether IV contrast is needed.",
                "default": False,
            },
            "angiography": {
                "type": "boolean",
                "description": "Whether CT angiography (CTA) is needed for vascular assessment.",
                "default": False,
            },
        },
        "required": ["clinical_context"],
    },
    "order_echocardiogram": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the echocardiogram.",
            },
            "echo_type": {
                "type": "string",
                "enum": ["TTE", "TEE", "bubble_study"],
                "description": (
                    "Type of echocardiogram. 'TTE': transthoracic (standard, non-invasive). "
                    "'TEE': transesophageal (better for PFO, thrombus, endocarditis). "
                    "'bubble_study': contrast echo for PFO/shunt detection."
                ),
                "default": "TTE",
            },
        },
        "required": ["clinical_context"],
    },
    "order_cardiac_monitoring": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for cardiac monitoring.",
            },
            "monitor_type": {
                "type": "string",
                "description": (
                    "Type of monitoring. 'holter_24h'/'holter_48h': continuous recording. "
                    "'event_monitor_14d'/'event_monitor_30d': patient-activated, captures "
                    "infrequent events. 'implantable_loop_recorder': months to years of "
                    "monitoring (cryptogenic stroke, unexplained syncope). "
                    "'telemetry': inpatient continuous monitoring."
                ),
                "default": "holter_24h",
            },
        },
        "required": ["clinical_context"],
    },
    "order_advanced_imaging": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the advanced imaging study.",
            },
            "modality": {
                "type": "string",
                "description": (
                    "Imaging modality. 'amyloid_PET'/'tau_PET': Alzheimer biomarkers. "
                    "'FDG_PET': glucose metabolism (dementia pattern, tumor grading). "
                    "'DaTscan': dopamine transporter (parkinsonian syndromes). "
                    "'MIBG_scan': cardiac sympathetic denervation (PD vs MSA). "
                    "'perfusion_MRI': cerebral blood flow. 'MR_spectroscopy': metabolites. "
                    "'MR_angiography'/'MR_venography': arterial / venous sinus imaging. "
                    "'carotid_duplex': carotid stenosis. 'transcranial_doppler': vasospasm."
                ),
            },
        },
        "required": ["clinical_context", "modality"],
    },
    "order_specialized_test": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the specialized test.",
            },
            # `{genetic_panels}` is filled from costs.yaml by parameters_for() —
            # JSON Schema `enum` cannot express the `genetic_panel:<panel>` family,
            # so the real tool documents it in prose and we must reproduce that
            # prose exactly, panel list included.
            "test_type": {
                "type": "string",
                "description": (
                    "Type of specialized test. Also accepts 'genetic_panel:<panel>' where "
                    "<panel> is one of: {genetic_panels}. "
                    "'emg_ncs': nerve conduction + needle EMG. 'emg_single_fiber' and "
                    "'repetitive_nerve_stimulation': neuromuscular junction (myasthenia). "
                    "'respiratory_function': FVC, MIP/MEP, NIF (ALS monitoring, MG crisis "
                    "risk). 'neuropsych_battery': comprehensive cognitive testing. "
                    "'vep'/'ssep'/'baep': evoked potentials. 'tilt_table': syncope. "
                    "'optical_coherence_tomography': retinal RNFL (MS, optic neuritis)."
                ),
            },
        },
        "required": ["clinical_context", "test_type"],
    },
    "search_medical_literature": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Clinical question or search query.",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return.",
                "default": 5,
            },
        },
        "required": ["query"],
    },
    "check_drug_interactions": {
        "type": "object",
        "properties": {
            "drug": {
                "type": "string",
                "description": "The proposed medication to check.",
            },
            "current_medications": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of patient's current medications.",
            },
            "patient_conditions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of patient's medical conditions.",
            },
        },
        "required": ["drug"],
    },
}


# --- Output field summary (derived from Pydantic models) --------------


def _format_type(annotation: Any) -> str:
    """Best-effort one-line type label for a Pydantic field annotation.

    Intentionally lossy — reviewers don't need full union/recursion details,
    just a recognisable shape: `str`, `list[str]`, `dict[str, str]`,
    `list[<Object>]`, `<Object>`, `<A | B>`.
    """
    if annotation is None or annotation is type(None):
        return "null"
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin is list:
        if args and isinstance(args[0], type) and issubclass(args[0], BaseModel):
            return f"list[{args[0].__name__}]"
        if args:
            return f"list[{_format_type(args[0])}]"
        return "list"
    if origin is dict:
        if len(args) == 2:
            return f"dict[{_format_type(args[0])}, {_format_type(args[1])}]"
        return "dict"
    # Optional[X] / X | None
    if origin is not None and args:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return _format_type(non_none[0])
        return " | ".join(_format_type(a) for a in non_none)
    if isinstance(annotation, type):
        if issubclass(annotation, BaseModel):
            return annotation.__name__
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def _describe_field(name: str, info: FieldInfo) -> dict[str, Any]:
    return {
        "name": name,
        "type": _format_type(info.annotation),
        "required": info.is_required(),
        "description": info.description or "",
    }


def output_fields_for(tool_name: str) -> list[dict[str, Any]] | None:
    """Return a flat list of top-level fields for the tool's output Pydantic model.

    None if the tool has no registered output model (shouldn't happen for the
    13 current tools, but defensive).
    """
    model = _TOOL_OUTPUT_MODEL.get(tool_name)
    if model is None:
        return None
    return [_describe_field(name, info) for name, info in model.model_fields.items()]


def parameters_for(tool_name: str) -> dict[str, Any] | None:
    """Return the agent-facing JSON schema for the tool's parameters.

    Closed vocabularies (`_COSTS_DERIVED_ENUMS`) and the `{genetic_panels}`
    placeholder are filled from costs.yaml, so what a reviewer sees is what the
    agent can actually order. None if the tool isn't in the mirror — call site
    should treat missing metadata as "unknown" rather than rendering an empty
    form.
    """
    schema = _TOOL_PARAMETERS.get(tool_name)
    if schema is None:
        return None
    schema = copy.deepcopy(schema)
    panels = ", ".join(
        sorted(_load_tool_costs().get("order_specialized_test", {}).get("genetic_panels", {}))
    )
    for parameter, spec in schema.get("properties", {}).items():
        vocabulary = _vocabulary(tool_name, parameter)
        if vocabulary:
            spec["enum"] = vocabulary
        description = spec.get("description")
        if isinstance(description, str) and "{genetic_panels}" in description:
            spec["description"] = description.format(genetic_panels=panels)
    return schema
