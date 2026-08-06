"""The closed parameter vocabulary for the two catchall diagnostic tools.

`order_specialized_test` and `order_advanced_imaging` each stand in for many distinct
studies, selected by a single parameter (`test_type` / `modality`). That parameter is a
**closed vocabulary**: if two cases could spell the same study differently ("EMG/NCS" vs
"nerve conduction studies"), the metric layer would count them as different tools and cost
lookup would fall back to a default rate.

`config/tools/costs.yaml` is the single source of truth — every vocabulary term is a row
there, so a term cannot exist without a price. The tool schemas, the case validator, and
`dataset-generation/TOOL_PARAMETER_VOCABULARY.md` all derive from it.

This module exists because those three artifacts previously each carried their own copy and
drifted: the tool enums exposed 9 of 19 specialized tests and 6 of 11 imaging modalities,
while the 600 benchmark cases and costs.yaml used the full vocabulary. Ground-truth values
that were perfectly legal became "invalid" against the tool the agent actually calls.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

DEFAULT_COSTS_PATH = Path(__file__).resolve().parents[3] / "config" / "tools" / "costs.yaml"

# A genetic panel is written `genetic_panel:<panel>`; `<panel>` must be a row in the
# `genetic_panels` block. JSON Schema `enum` cannot express this, so the tool schema lists
# the fixed test types and the validator checks the prefixed form.
GENETIC_PANEL_PREFIX = "genetic_panel:"


@lru_cache(maxsize=4)
def _load_tools(costs_path: Path = DEFAULT_COSTS_PATH) -> dict[str, Any]:
    if not costs_path.exists():
        return {}
    with open(costs_path) as f:
        return (yaml.safe_load(f) or {}).get("tools", {})


def specialized_test_types(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `order_specialized_test.test_type` vocabulary (excluding genetic panels)."""
    return sorted(_load_tools(costs_path).get("order_specialized_test", {}).get("by_type", {}))


def genetic_panels(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """Allowed `<panel>` suffixes for `genetic_panel:<panel>`."""
    return sorted(_load_tools(costs_path).get("order_specialized_test", {}).get("genetic_panels", {}))


def advanced_imaging_modalities(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `order_advanced_imaging.modality` vocabulary."""
    return by_type_values("order_advanced_imaging", costs_path)


# Different *names* for one assay, as opposed to different spellings of one name. Punctuation
# folding cannot reconcile these, so before this map the benchmark held two priced rows for the
# same test that did not compare equal: ground truth asked `syphilis` in 30 case actions and
# `RPR` in 118, and an agent naming either failed the other. Same for the paraneoplastic panel
# (37 actions vs 1), liver function (33 vs 2) and the inflammatory bundle (31 vs 1).
#
# Key: the punctuation-folded alias. Value: the canonical *display* spelling, which is the one
# advertised to the agent — a named assay wherever there is one, since naming the assay rather
# than the question is the whole point of the per-study vocabulary.
_ANALYTE_SYNONYMS: dict[str, str] = {
    "syphilis": "RPR",
    "lft": "LFTs",
    "lipid": "lipid_panel",
    "lipids": "lipid_panel",
    "ua": "urinalysis",
    "paraneoplastic": "paraneoplastic_panel",
    "paraneoplastic_antibodies": "paraneoplastic_panel",
    "autoimmune_encephalitis": "autoimmune_encephalitis_panel",
    "inflammatory": "inflammatory_markers",
    "esr_crp": "inflammatory_markers",
    "toxicology": "tox_screen",
    "drug_screen": "tox_screen",
    "adamts13_activity": "ADAMTS13",
    "complement_c3/c4": "complement",
    "smear": "peripheral smear",
    "blood_cultures_x3": "blood_cultures",
}


def _fold(value: str) -> str:
    """Punctuation- and case-folded form: `Protein C`, `protein-C` and `protein_C` agree."""
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def normalize_analyte(value: str) -> str:
    """Comparison key for a lab panel / CSF assay name.

    Two levels. `costs.yaml` carries spelling aliases of the same name at the same price
    (`D-dimer`/`D_dimer`, `Free T4`/`free_T4`, `protein C`/`protein_C`, ...) because the 600
    cases were authored with free text, so scoring folds punctuation and case: a model writing
    `Protein C` has not missed `protein_C`. It also carries distinct *names* for one assay,
    which folding cannot reconcile — see `_ANALYTE_SYNONYMS`.

    Used by the metric layer (`evaluation/metrics.py::_as_set`) and by `CostTracker`, so the
    bill and the score read one workup the same way.
    """
    folded = _fold(value)
    canonical = _ANALYTE_SYNONYMS.get(folded)
    return _fold(canonical) if canonical else folded


def canonical_analyte(value: str) -> str:
    """The display spelling to advertise for an assay, resolving synonyms."""
    return _ANALYTE_SYNONYMS.get(_fold(value), value)


def _canonical_analytes(names: list[str]) -> list[str]:
    """Deduplicate aliases to one advertised name per assay.

    Used for the *advertised* enum: every alias stays priced so existing cases keep working,
    but the agent is shown one name. A synonym's canonical target wins outright; otherwise the
    snake_case spelling is preferred over the spaced one.
    """
    candidates: dict[str, set[str]] = {}
    for name in names:
        # A synonym resolves to its canonical target, so every alias of one assay contributes
        # the same string here and the only remaining choice is between spellings of one name.
        candidates.setdefault(normalize_analyte(name), set()).add(canonical_analyte(name))
    # Prefer the project's snake_case house style: no space, then underscore over hyphen.
    return sorted(
        min(group, key=lambda d: (" " in d, "-" in d, d)) for group in candidates.values()
    )


def lab_panels(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The priced `interpret_labs.panels` vocabulary, aliases collapsed.

    Not closed in the same sense as the catchall enums: an out-of-vocabulary analyte still
    executes and is charged `default_panel`. The list exists so the agent can *name* the
    assay it wants, because the score and the bill are both per-analyte.
    """
    return _canonical_analytes(
        list(_load_tools(costs_path).get("interpret_labs", {}).get("by_panel", {}))
    )


def csf_special_tests(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The priced `analyze_csf.special_tests` vocabulary."""
    return _canonical_analytes(
        list(_load_tools(costs_path).get("analyze_csf", {}).get("by_special_test", {}))
    )


def by_type_values(tool_name: str, costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """Every value priced under a tool's `by_type` block — the tool's legal enum."""
    return sorted(_load_tools(costs_path).get(tool_name, {}).get("by_type", {}))


# The three enums that were still written out by hand in their tool class, and so could drift
# from costs.yaml exactly as the review app's catalog did. Derived here instead, which is what
# made `exercise_echo` orderable the moment it was priced.


def echocardiogram_types(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `order_echocardiogram.echo_type` vocabulary."""
    return by_type_values("order_echocardiogram", costs_path)


def eeg_types(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `analyze_eeg.eeg_type` vocabulary."""
    return by_type_values("analyze_eeg", costs_path)


def mri_protocols(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `analyze_brain_mri.protocol` vocabulary.

    Read from the `protocols` block rather than `by_type`: protocol selection does not change
    what is billed (the radiologist chooses the sequences), so every row is priced at 0 and
    the MRI's cost comes from `base` + `contrast`. The block is still the source of the enum,
    so a protocol cannot be orderable without being declared.
    """
    return sorted(_load_tools(costs_path).get("analyze_brain_mri", {}).get("protocols", {}))


# --- Tools added after the July 2026 clinical tool review ----------------------------------
#
# Each has a single discriminator backed by a `by_type` block, so these are thin wrappers
# over `by_type_values` and exist only to give the tool schemas a named accessor — the same
# shape as `advanced_imaging_modalities`. Adding a term means adding a priced row; nothing
# can be orderable without a price.


def body_imaging_studies(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `order_body_imaging.study` vocabulary (`<region>_<modality>`)."""
    return by_type_values("order_body_imaging", costs_path)


def microbiology_specimens(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `order_microbiology.specimen` vocabulary."""
    return by_type_values("order_microbiology", costs_path)


def tissue_procedures(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `obtain_tissue_diagnosis.procedure` vocabulary."""
    return by_type_values("obtain_tissue_diagnosis", costs_path)


def molecular_assays(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The priced `obtain_tissue_diagnosis.molecular_assays` vocabulary."""
    return sorted(
        _load_tools(costs_path).get("obtain_tissue_diagnosis", {}).get("by_molecular_assay", {})
    )


def assessment_types(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `perform_clinical_assessment.assessment_type` vocabulary."""
    return by_type_values("perform_clinical_assessment", costs_path)


def is_valid_body_imaging_study(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in body_imaging_studies(costs_path)


def is_valid_specimen(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in microbiology_specimens(costs_path)


def is_valid_tissue_procedure(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in tissue_procedures(costs_path)


def is_valid_molecular_assay(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return normalize_analyte(value) in {
        normalize_analyte(a) for a in molecular_assays(costs_path)
    }


def is_valid_assessment_type(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in assessment_types(costs_path)


def is_valid_test_type(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    """True for a fixed test type or a `genetic_panel:<panel>` with a known panel."""
    if value.startswith(GENETIC_PANEL_PREFIX):
        return value[len(GENETIC_PANEL_PREFIX) :] in genetic_panels(costs_path)
    return value in specialized_test_types(costs_path)


def is_valid_modality(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in advanced_imaging_modalities(costs_path)


def is_valid_echo_type(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in echocardiogram_types(costs_path)


def is_valid_eeg_type(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in eeg_types(costs_path)


def is_valid_mri_protocol(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in mri_protocols(costs_path)
