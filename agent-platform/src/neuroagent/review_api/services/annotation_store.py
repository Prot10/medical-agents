"""Filesystem-backed store for per-reviewer case reviews.

Layout::

    data/review/annotations/{version}/{reviewer_code}/{case_id}.json

One file = one (reviewer, dataset_version, case) triple. Reviewers cannot
see each other's annotations because they live in separate directories.
"""

from __future__ import annotations

import logging
import re
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path

from neuroagent.datasets import DATASETS

from ..schemas.annotations import CaseReview, CaseReviewSummary

logger = logging.getLogger(__name__)

# Defensive validators — these strings end up as path segments.
_VERSION_PATTERN = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")
_CODE_PATTERN = re.compile(r"^[A-Z0-9-]{3,64}$")
_CASE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_\-]+$")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# Per-(dataset version, reviewer, case) write locks. Module-level so every
# AnnotationStore instance serializes on the same lock for the same file.
# Reentrant so load_or_init can call save() while already holding the lock.
_REVIEW_LOCKS: dict[tuple[str, str, str], threading.RLock] = {}
_REVIEW_LOCKS_GUARD = threading.Lock()


def _review_lock(version: str, reviewer_code: str, case_id: str) -> threading.RLock:
    key = (version, reviewer_code, case_id)
    with _REVIEW_LOCKS_GUARD:
        lock = _REVIEW_LOCKS.get(key)
        if lock is None:
            lock = _REVIEW_LOCKS[key] = threading.RLock()
        return lock


class AnnotationStore:
    """Read/write reviewer-scoped annotation files."""

    def __init__(self, root: Path) -> None:
        self._root = root

    @property
    def root(self) -> Path:
        return self._root

    # ------------------------------------------------------------------
    # Path resolution

    def _validate_version(self, version: str) -> str:
        if not _VERSION_PATTERN.fullmatch(version) or version not in DATASETS:
            raise ValueError(f"Unknown dataset version: {version!r}")
        return version

    def _reviewer_dir(self, version: str, reviewer_code: str) -> Path:
        dataset_version = self._validate_version(version)
        if not _CODE_PATTERN.fullmatch(reviewer_code):
            raise ValueError(f"Invalid reviewer code: {reviewer_code!r}")
        return self._root / dataset_version / reviewer_code

    def _path_for(self, version: str, reviewer_code: str, case_id: str) -> Path:
        if not _CASE_ID_PATTERN.fullmatch(case_id):
            raise ValueError(f"Invalid case id: {case_id!r}")
        return self._reviewer_dir(version, reviewer_code) / f"{case_id}.json"

    def lock_for(
        self, version: str, reviewer_code: str, case_id: str
    ) -> threading.RLock:
        """Reentrant lock guarding one (version, reviewer, case) review file.

        ``save``/``load_or_init``/``delete`` acquire it internally; callers
        that do a load → mutate → save sequence can hold it across the whole
        sequence to make the read-modify-write atomic.
        """
        dataset_version = self._validate_version(version)
        if not _CODE_PATTERN.fullmatch(reviewer_code):
            raise ValueError(f"Invalid reviewer code: {reviewer_code!r}")
        if not _CASE_ID_PATTERN.fullmatch(case_id):
            raise ValueError(f"Invalid case id: {case_id!r}")
        return _review_lock(dataset_version, reviewer_code, case_id)

    # ------------------------------------------------------------------
    # CRUD

    def load(
        self,
        version: str,
        reviewer_code: str,
        case_id: str,
    ) -> CaseReview | None:
        """Return the existing review or None if no file exists."""
        path = self._path_for(version, reviewer_code, case_id)
        if not path.exists():
            return None
        try:
            return CaseReview.model_validate_json(path.read_text())
        except Exception as exc:  # pragma: no cover — corrupted file
            logger.error("Failed to parse review at %s: %s", path, exc)
            return None

    def load_or_init(
        self,
        version: str,
        reviewer_code: str,
        case_id: str,
    ) -> CaseReview:
        """Return the existing review, otherwise a fresh ``pending`` one.

        Side effect: on first load, ``first_opened_at`` is set and the
        review is persisted so the timestamp survives restarts.
        """
        with self.lock_for(version, reviewer_code, case_id):
            existing = self.load(version, reviewer_code, case_id)
            if existing is not None:
                return existing

            now = _utcnow()
            review = CaseReview(
                case_id=case_id,
                dataset_version=self._validate_version(version),
                reviewer_code=reviewer_code,
                first_opened_at=now,
                last_updated_at=now,
            )
            self.save(review)
            return review

    def save(self, review: CaseReview) -> CaseReview:
        """Persist the review atomically."""
        with self.lock_for(
            review.dataset_version, review.reviewer_code, review.case_id
        ):
            review.last_updated_at = _utcnow()
            path = self._path_for(
                review.dataset_version, review.reviewer_code, review.case_id
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            # Atomic write: tempfile + rename.
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

    def delete(self, version: str, reviewer_code: str, case_id: str) -> bool:
        with self.lock_for(version, reviewer_code, case_id):
            path = self._path_for(version, reviewer_code, case_id)
            if not path.exists():
                return False
            path.unlink()
            return True

    # ------------------------------------------------------------------
    # Listing

    def list_for_reviewer(
        self,
        version: str,
        reviewer_code: str,
    ) -> list[CaseReviewSummary]:
        """Cheap per-reviewer summary, suitable for the case-list sidebar."""
        directory = self._reviewer_dir(version, reviewer_code)
        case_ids = (
            {case_file.stem for case_file in directory.glob("*.json")}
            if directory.exists()
            else set()
        )

        summaries: list[CaseReviewSummary] = []
        for case_id in sorted(case_ids):
            review = self.load(version, reviewer_code, case_id)
            if review is None:
                continue
            severity_counts: dict[str, int] = {"note": 0, "issue": 0, "error": 0}
            for annotation in review.field_annotations:
                severity_counts[annotation.severity] = (
                    severity_counts.get(annotation.severity, 0) + 1
                )
            summaries.append(
                CaseReviewSummary(
                    case_id=review.case_id,
                    status=review.status,
                    annotation_count=len(review.field_annotations),
                    comment_count=len(review.case_comments),
                    severity_counts=severity_counts,
                    last_updated_at=review.last_updated_at,
                    time_spent_seconds=review.time_spent_seconds,
                )
            )
        return summaries

    def list_all_reviewers(self, version: str) -> list[str]:
        """List every reviewer code that has at least one stored review for ``version``."""
        version_dir = self._root / self._validate_version(version)
        if not version_dir.exists():
            return []
        return sorted(
            entry.name
            for entry in version_dir.iterdir()
            if entry.is_dir() and _CODE_PATTERN.fullmatch(entry.name)
        )
