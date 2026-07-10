"""Filesystem-backed store for per-reviewer tool reviews.

Layout::

    data/review/tool_reviews/{version}/{reviewer_code}.json

One file = one (reviewer, dataset_version) pair. Mirrors
:class:`AnnotationStore` (atomic tempfile+rename writes, defensive path
validators) but there is a single file per reviewer rather than one per
case.
"""

from __future__ import annotations

import logging
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from neuroagent.datasets import DATASET_VERSION_ALIASES, normalize_dataset_version

from ..schemas.tool_review import ToolReview

logger = logging.getLogger(__name__)

# Defensive validators — these strings end up as path segments.
_VERSION_PATTERN = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")
_CODE_PATTERN = re.compile(r"^[A-Z0-9-]{3,64}$")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ToolReviewStore:
    """Read/write reviewer-scoped tool-review files."""

    def __init__(self, root: Path) -> None:
        self._root = root

    @property
    def root(self) -> Path:
        return self._root

    # ------------------------------------------------------------------
    # Path resolution

    def _validate_version(self, version: str) -> str:
        if not _VERSION_PATTERN.fullmatch(version):
            raise ValueError(f"Invalid dataset version: {version!r}")
        return normalize_dataset_version(version)

    def _version_candidates(self, version: str) -> list[str]:
        canonical = self._validate_version(version)
        aliases = [
            alias
            for alias, target in DATASET_VERSION_ALIASES.items()
            if target == canonical and alias != canonical
        ]
        return [canonical, *aliases]

    def _path_for(self, version: str, reviewer_code: str) -> Path:
        canonical = self._validate_version(version)
        if not _CODE_PATTERN.fullmatch(reviewer_code):
            raise ValueError(f"Invalid reviewer code: {reviewer_code!r}")
        return self._root / canonical / f"{reviewer_code}.json"

    def _path_for_key(self, version: str, reviewer_code: str) -> Path:
        if not _CODE_PATTERN.fullmatch(reviewer_code):
            raise ValueError(f"Invalid reviewer code: {reviewer_code!r}")
        return self._root / version / f"{reviewer_code}.json"

    # ------------------------------------------------------------------
    # CRUD

    def load(self, version: str, reviewer_code: str) -> ToolReview | None:
        """Return the existing tool review or None if no file exists."""
        paths = [
            self._path_for_key(candidate, reviewer_code)
            for candidate in self._version_candidates(version)
        ]
        path = next((candidate for candidate in paths if candidate.exists()), None)
        if path is None:
            return None
        try:
            review = ToolReview.model_validate_json(path.read_text())
            review.dataset_version = normalize_dataset_version(review.dataset_version)
            return review
        except Exception as exc:  # pragma: no cover — corrupted file
            logger.error("Failed to parse tool review at %s: %s", path, exc)
            return None

    def load_or_init(self, version: str, reviewer_code: str) -> ToolReview:
        """Return the existing review, otherwise a fresh one (persisted).

        Side effect: on first load, ``first_opened_at`` is set and the
        review is persisted so the timestamp survives restarts.
        """
        existing = self.load(version, reviewer_code)
        if existing is not None:
            return existing

        now = _utcnow()
        review = ToolReview(
            reviewer_code=reviewer_code,
            dataset_version=normalize_dataset_version(version),
            first_opened_at=now,
            last_updated_at=now,
        )
        self.save(review)
        return review

    def save(self, review: ToolReview) -> ToolReview:
        """Persist the review atomically (tempfile + rename)."""
        review.last_updated_at = _utcnow()
        review.dataset_version = normalize_dataset_version(review.dataset_version)
        path = self._path_for(review.dataset_version, review.reviewer_code)
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            "w",
            dir=str(path.parent),
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
            encoding="utf-8",
        ) as fh:
            fh.write(review.model_dump_json(indent=2))
            tmp_path = Path(fh.name)
        tmp_path.replace(path)
        return review

    # ------------------------------------------------------------------
    # Listing

    def list_all_reviewers(self, version: str) -> list[str]:
        """List reviewer codes that have a stored tool review for ``version``."""
        reviewers: set[str] = set()
        for candidate in self._version_candidates(version):
            version_dir = self._root / candidate
            if not version_dir.exists():
                continue
            reviewers.update(
                f.stem for f in version_dir.glob("*.json") if _CODE_PATTERN.fullmatch(f.stem)
            )
        return sorted(reviewers)
