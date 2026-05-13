"""Load NeuroBench cases from disk at startup."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

logger = logging.getLogger(__name__)


def load_dataset(
    dataset_path: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, NeuroBenchCase]]:
    """Load every case JSON under ``dataset_path / "cases"``.

    Returns
    -------
    (case_index, case_objects)
        ``case_index`` is a lightweight summary keyed by ``case_id``.
        ``case_objects`` holds the fully-parsed ``NeuroBenchCase`` instances.
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
            logger.error("Failed to load case %s: %s", case_file.name, exc)
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

    return case_index, case_objects
