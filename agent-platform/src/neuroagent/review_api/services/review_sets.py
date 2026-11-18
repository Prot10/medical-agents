"""Review sets: fixed case subsets that reviewers re-review in a space of their own.

A set is declared in ``config/review/review_sets.yaml``. The app serves it as one more dataset
version (its id), holding only the listed cases of its base dataset in the listed order, and
the annotation store files its reviews under that id, apart from the base dataset's reviews.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from neuroagent.datasets import DATASETS, REPO_ROOT, load_dataset

_SET_ID_PATTERN = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")


@dataclass(frozen=True, slots=True)
class ReviewSet:
    id: str
    base: str
    name: str
    description: str
    case_ids: tuple[str, ...]
    # Own frozen case files (holding cases/<case id>.json), or None to serve the base's files.
    cases_dir: Path | None = None


def load_review_sets(path: Path) -> dict[str, ReviewSet]:
    """Read and check the review-set file; a missing file means no sets.

    Raises:
        ValueError: A set has a bad id, an unknown base dataset, a repeated case or no cases.
    """
    if not path.exists():
        return {}
    raw: dict[str, Any] = yaml.safe_load(path.read_text()) or {}
    sets: dict[str, ReviewSet] = {}
    for set_id, body in raw.items():
        if not _SET_ID_PATTERN.fullmatch(set_id) or set_id in DATASETS:
            raise ValueError(f"Invalid review set id: {set_id!r}")
        base = body.get("base")
        if base not in DATASETS:
            raise ValueError(f"Review set {set_id!r}: unknown base dataset {base!r}")
        case_ids = tuple(body.get("cases") or ())
        if not case_ids or len(set(case_ids)) != len(case_ids):
            raise ValueError(f"Review set {set_id!r}: cases must be a non-empty list without repeats")
        sets[set_id] = ReviewSet(
            id=set_id,
            base=base,
            name=str(body.get("name") or set_id),
            description=str(body.get("description") or "").strip(),
            case_ids=case_ids,
            cases_dir=REPO_ROOT / body["cases_dir"] if body.get("cases_dir") else None,
        )
    return sets


def subset_dataset(
    review_set: ReviewSet, base: tuple[dict[str, dict], dict[str, Any]]
) -> tuple[dict[str, dict], dict[str, Any]]:
    """The set's index and case objects, in the set's order.

    The cases come from the set's own ``cases_dir`` when it has one, else from ``base`` (the
    base dataset's index and objects).

    Raises:
        ValueError: A listed case is missing, or ``cases_dir`` holds a case the set does not list.
    """
    index, objects = load_dataset(review_set.cases_dir) if review_set.cases_dir else base
    missing = [c for c in review_set.case_ids if c not in objects]
    if missing:
        raise ValueError(f"Review set {review_set.id!r}: cases not found: {missing}")
    if review_set.cases_dir:
        extra = sorted(set(objects) - set(review_set.case_ids))
        if extra:
            raise ValueError(f"Review set {review_set.id!r}: {review_set.cases_dir} holds unlisted cases {extra}")
    return (
        {c: index[c] for c in review_set.case_ids},
        {c: objects[c] for c in review_set.case_ids},
    )
