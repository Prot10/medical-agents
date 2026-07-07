"""Per-tool I/O schemas for the Tool Catalog view.

The review_api ships isolated from ``agent-platform/src/neuroagent/tools/`` —
the deploy script only rsyncs ``review_api/`` and the workspace ``__init__.py``.
So the agent-facing ``parameter_schema`` dicts that live next to each tool's
``execute()`` method aren't importable here. We mirror them verbatim below.

**KEEP IN SYNC** with ``agent-platform/src/neuroagent/tools/*.py``. The truth
is the tool class's ``parameter_schema`` attribute; the test
``test_tool_io_schemas_match`` (when added) should diff this mirror against the
real classes to catch drift in CI.

Return shapes are derived from the Pydantic models in
``neuroagent_schemas.tool_outputs`` — those ARE shipped, so no mirror is needed
for outputs.
"""

from __future__ import annotations

from typing import Any, get_args, get_origin

from neuroagent_schemas.case import _TOOL_OUTPUT_MODEL
from pydantic import BaseModel
from pydantic.fields import FieldInfo


# --- Parameter schemas (verbatim mirror of tools/*.py) ----------------

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
                "enum": ["holter_24h", "holter_48h", "event_monitor_30d", "telemetry"],
                "description": (
                    "Type of monitoring. 'holter_24h'/'holter_48h': continuous recording. "
                    "'event_monitor_30d': patient-activated, captures infrequent events. "
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
            "imaging_type": {
                "type": "string",
                "enum": [
                    "amyloid_PET", "FDG_PET", "DaTscan",
                    "perfusion_MRI", "MR_spectroscopy", "carotid_duplex",
                ],
                "description": (
                    "Type of advanced imaging. 'amyloid_PET': amyloid plaque detection "
                    "(Alzheimer's). 'FDG_PET': glucose metabolism (dementia, tumor). "
                    "'DaTscan': dopamine transporter imaging (parkinsonian syndromes). "
                    "'perfusion_MRI': cerebral blood flow (stroke, tumor grading). "
                    "'MR_spectroscopy': brain metabolite analysis (tumor, metabolic). "
                    "'carotid_duplex': carotid artery stenosis screening."
                ),
            },
        },
        "required": ["clinical_context", "imaging_type"],
    },
    "order_specialized_test": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the specialized test.",
            },
            "test_type": {
                "type": "string",
                "enum": [
                    "neuropsych_battery", "emg_ncs", "vep", "ssep", "baep",
                    "tilt_table", "polysomnography", "autonomic_testing",
                    "exercise_stress_test",
                ],
                "description": (
                    "Type of specialized test. 'neuropsych_battery': comprehensive "
                    "cognitive testing (MMSE, MoCA, RAVLT, etc.). 'emg_ncs': "
                    "electromyography and nerve conduction studies. 'vep'/'ssep'/'baep': "
                    "evoked potentials. 'tilt_table': orthostatic syncope evaluation. "
                    "'polysomnography': overnight sleep study. 'autonomic_testing': "
                    "autonomic reflex screen. 'exercise_stress_test': cardiac stress test."
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

    None if the tool isn't in the mirror — call site should treat missing
    metadata as "unknown" rather than rendering an empty form.
    """
    return _TOOL_PARAMETERS.get(tool_name)
