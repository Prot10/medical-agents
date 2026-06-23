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

from ..schemas.tool_review import ToolReview

logger = logging.getLogger(__name__)

# Defensive validators — these strings end up as path segments.
_VERSION_PATTERN = re.compile(r"^v\d{1,3}$")
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

    def _path_for(self, version: str, reviewer_code: str) -> Path:
        if not _VERSION_PATTERN.fullmatch(version):
            raise ValueError(f"Invalid dataset version: {version!r}")
        if not _CODE_PATTERN.fullmatch(reviewer_code):
            raise ValueError(f"Invalid reviewer code: {reviewer_code!r}")
        return self._root / version / f"{reviewer_code}.json"

    # ------------------------------------------------------------------
    # CRUD

    def load(self, version: str, reviewer_code: str) -> ToolReview | None:
        """Return the existing tool review or None if no file exists."""
        path = self._path_for(version, reviewer_code)
        if not path.exists():
            return None
        try:
            return ToolReview.model_validate_json(path.read_text())
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
            dataset_version=version,
            first_opened_at=now,
            last_updated_at=now,
        )
        self.save(review)
        return review

    def save(self, review: ToolReview) -> ToolReview:
        """Persist the review atomically (tempfile + rename)."""
        review.last_updated_at = _utcnow()
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
        if not _VERSION_PATTERN.fullmatch(version):
            raise ValueError(f"Invalid dataset version: {version!r}")
        version_dir = self._root / version
        if not version_dir.exists():
            return []
        return sorted(
            f.stem
            for f in version_dir.glob("*.json")
            if _CODE_PATTERN.fullmatch(f.stem)
        )
