"""Review sets: fixed case subsets that reviewers re-review in a space of their own.

A set is declared in ``config/review/review_sets.yaml``. The app serves it as one more dataset
version (its id), holding only the listed cases of its base dataset in the listed order, and
the annotation store files its reviews under that id, apart from the base dataset's reviews.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import yaml

from neuroagent.datasets import DATASETS, REPO_ROOT, load_dataset

if TYPE_CHECKING:
    from ..schemas.reviewers import ReviewerCode

_SET_ID_PATTERN = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")

# recheck: corrected cases, "is it right now?". second_review: cases another physician already
# reviewed in this exact version, reviewed again independently (inter-physician agreement).
SetKind = Literal["recheck", "second_review"]
_KINDS: tuple[str, ...] = ("recheck", "second_review")


@dataclass(frozen=True, slots=True)
class ReviewSet:
    id: str
    base: str
    name: str
    description: str
    case_ids: tuple[str, ...]
    # Own frozen case files (holding cases/<case id>.json), or None to serve the base's files.
    cases_dir: Path | None = None
    kind: SetKind = "recheck"
    # Shown only to the codes that list it in their `review_sets` (and to admins).
    assigned_only: bool = False


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
        kind = body.get("kind", "recheck")
        if kind not in _KINDS:
            raise ValueError(f"Review set {set_id!r}: unknown kind {kind!r}")
        assigned_only = body.get("assigned_only", False)
        if not isinstance(assigned_only, bool):
            raise ValueError(f"Review set {set_id!r}: assigned_only must be true or false")
        sets[set_id] = ReviewSet(
            id=set_id,
            base=base,
            name=str(body.get("name") or set_id),
            description=str(body.get("description") or "").strip(),
            case_ids=case_ids,
            cases_dir=REPO_ROOT / body["cases_dir"] if body.get("cases_dir") else None,
            kind=kind,
            assigned_only=assigned_only,
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


def visible_sets(reviewer: ReviewerCode, sets: dict[str, ReviewSet]) -> list[ReviewSet]:
    """The sets a code may open, in file order.

    A guided code (with ``review_sets``) opens exactly its assigned sets. An admin opens every
    set. Any other code opens the sets that are not ``assigned_only``.

    Raises:
        ValueError: A guided code names a set that does not exist (a misconfigured code must
            fail loudly, not fall back to the full review).
    """
    if reviewer.is_guided:
        unknown = [s for s in reviewer.review_sets if s not in sets]
        if unknown:
            raise ValueError(f"Reviewer code assigned to unknown review set(s): {unknown}")
        return [sets[s] for s in sets if s in reviewer.review_sets]
    if reviewer.role == "admin":
        return list(sets.values())
    return [s for s in sets.values() if not s.assigned_only]
