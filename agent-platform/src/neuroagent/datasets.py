"""Shared NeuroBench dataset registry and loader."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = REPO_ROOT / "data"
CANONICAL_DATASET_VERSION = "neurobench"
DEFAULT_DATASET_VERSION = CANONICAL_DATASET_VERSION
DATASET_VERSION_ALIASES = {
    "v5": CANONICAL_DATASET_VERSION,
}


@dataclass(frozen=True, slots=True)
class DatasetInfo:
    version: str
    path: Path
    name: str
    description: str


DATASETS: dict[str, DatasetInfo] = {
    CANONICAL_DATASET_VERSION: DatasetInfo(
        version=CANONICAL_DATASET_VERSION,
        path=DATA_ROOT / "neurobench",
        name="NeuroBench",
        description="Tool-augmented neurology benchmark across 20 conditions.",
    ),
}


def normalize_dataset_version(version: str) -> str:
    """Return the canonical dataset key for ``version`` or its legacy aliases."""
    return DATASET_VERSION_ALIASES.get(version, version)


def resolve_dataset_info(version: str) -> DatasetInfo | None:
    """Resolve a dataset by canonical key or compatibility alias."""
    return DATASETS.get(normalize_dataset_version(version))


def load_dataset(
    dataset_path: Path,
    *,
    skip_invalid: bool = False,
    skipped: list[str] | None = None,
) -> tuple[dict[str, dict[str, Any]], dict[str, NeuroBenchCase]]:
    """Load every case JSON under ``dataset_path / "cases"``.

    Strict by default: a case file that fails to parse or validate raises,
    because silently dropping cases shrinks the benchmark denominator.

    Args:
        dataset_path: Dataset root containing a ``cases/`` directory.
        skip_invalid: If True, restore the old lenient behavior — invalid cases
            are skipped with a prominent warning instead of raising.
        skipped: Optional list that, when provided with ``skip_invalid=True``,
            is extended with the filenames of every skipped case so callers can
            report the exact count.

    Raises:
        ValueError: A case file is malformed and ``skip_invalid`` is False.
    """
    case_index: dict[str, dict[str, Any]] = {}
    case_objects: dict[str, NeuroBenchCase] = {}
    skipped_files: list[str] = []

    cases_dir = dataset_path / "cases"
    if not cases_dir.exists():
        logger.warning("Cases directory does not exist: %s", cases_dir)
        return case_index, case_objects

    for case_file in sorted(cases_dir.glob("*.json")):
        try:
            data = json.loads(case_file.read_text())
            case = NeuroBenchCase.model_validate(data)
        except Exception as exc:
            if not skip_invalid:
                raise ValueError(
                    f"Invalid NeuroBench case file {case_file}: {exc}"
                ) from exc
            logger.error("Skipping invalid case %s: %s", case_file.name, exc)
            skipped_files.append(case_file.name)
            continue

        case_objects[case.case_id] = case
        case_index[case.case_id] = {
            "case_id": case.case_id,
            "condition": case.condition.value,
            "difficulty": case.difficulty.value,
            "encounter_type": case.encounter_type.value,
            "age": case.patient.demographics.age,
            "sex": case.patient.demographics.sex,
            "chief_complaint": case.patient.chief_complaint,
        }

    if skipped_files:
        logger.warning(
            "load_dataset SKIPPED %d invalid case file(s) — loaded %d cases; "
            "the dataset denominator is reduced: %s",
            len(skipped_files), len(case_objects), skipped_files,
        )
        if skipped is not None:
            skipped.extend(skipped_files)

    return case_index, case_objects
