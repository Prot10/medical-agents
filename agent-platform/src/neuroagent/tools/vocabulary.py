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


def normalize_analyte(value: str) -> str:
    """Canonical form of a lab panel / CSF assay name, for comparison only.

    `costs.yaml` carries spelling aliases of the same assay at the same price
    (`D-dimer`/`D_dimer`, `Free T4`/`free_T4`, `protein C`/`protein_C`, ...) because the
    600 cases were authored with free text. Scoring compares normalised names so a model
    writing `Protein C` is not marked as having missed `protein_C`.
    """
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def _canonical_analytes(names: list[str]) -> list[str]:
    """Deduplicate spelling aliases, preferring the snake_case spelling.

    Used for the *advertised* enum: the aliases stay priced so existing cases keep working,
    but the agent is shown one name per assay.
    """
    best: dict[str, str] = {}
    for name in names:
        key = normalize_analyte(name)
        current = best.get(key)
        if current is None or (" " in current and " " not in name):
            best[key] = name
    return sorted(best.values())


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
