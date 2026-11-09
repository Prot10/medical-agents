"""Shared NeuroBench dataset registry and loader."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = REPO_ROOT / "data"
CANONICAL_DATASET_VERSION = "neurobench"
DEFAULT_DATASET_VERSION = CANONICAL_DATASET_VERSION


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


def split_case_ids(dataset_path: Path, split: str) -> list[str]:
    """The case ids of one split file, ``splits/{split}_cases.txt``, in file order."""
    return (dataset_path / "splits" / f"{split}_cases.txt").read_text().split()


def refuse_test_cases(case_ids: Iterable[str], dataset_path: Path | None = None) -> None:
    """Raise if a training or checkpoint-selection set holds a case of the test split.

    Every path that turns cases into weights (GRPO rollouts, SFT episodes, the episode export
    that feeds SFT) or picks among them (`scripts/training/eval_checkpoints.sh`) calls this, so a
    test case cannot get there through a hand-written case list or a run directory evaluated on
    the test split.

    Raises:
        ValueError: Some of ``case_ids`` belong to the test split.
    """
    test = set(split_case_ids(dataset_path or DATASETS[DEFAULT_DATASET_VERSION].path, "test"))
    leaked = sorted(test.intersection(case_ids))
    if leaked:
        shown = ", ".join(leaked[:10]) + (" ..." if len(leaked) > 10 else "")
        raise ValueError(f"{len(leaked)} test-split case(s) where only training or validation cases belong: {shown}")


def load_dataset(
    dataset_path: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, NeuroBenchCase]]:
    """Load every case JSON under ``dataset_path / "cases"``.

    A case file that fails to parse or validate raises because silently dropping
    cases would shrink the benchmark denominator.

    Raises:
        ValueError: A case file is malformed.
    """
    case_index: dict[str, dict[str, Any]] = {}
    case_objects: dict[str, NeuroBenchCase] = {}
    cases_dir = dataset_path / "cases"
    if not cases_dir.exists():
        logger.warning("Cases directory does not exist: %s", cases_dir)
        return case_index, case_objects

    for case_file in sorted(cases_dir.glob("*.json")):
        try:
            data = json.loads(case_file.read_text())
            case = NeuroBenchCase.model_validate(data)
        except Exception as exc:
            raise ValueError(
                f"Invalid NeuroBench case file {case_file}: {exc}"
            ) from exc

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

    return case_index, case_objects
