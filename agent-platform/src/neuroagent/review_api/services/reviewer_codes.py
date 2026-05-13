"""Load and hot-reload reviewer codes from a YAML file."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import yaml

from ..schemas.reviewers import ReviewerCode

logger = logging.getLogger(__name__)


class ReviewerCodeRegistry:
    """In-memory registry of reviewer codes backed by a YAML file.

    Hot-reload: every call to :meth:`get` (or :meth:`reload_if_stale`)
    re-reads the YAML iff its mtime has changed since the last load.
    No file watcher, no inotify — just a stat call per request.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._codes: dict[str, ReviewerCode] = {}
        self._mtime: float = 0.0
        self.reload()

    @property
    def path(self) -> Path:
        return self._path

    def reload_if_stale(self) -> None:
        """Reload the YAML if its mtime changed since last load."""
        if not self._path.exists():
            if self._codes:
                # File was deleted at runtime.
                logger.warning("Reviewer codes file disappeared: %s", self._path)
                self._codes = {}
                self._mtime = 0.0
            return

        current_mtime = self._path.stat().st_mtime
        if current_mtime != self._mtime:
            self.reload()

    def reload(self) -> None:
        if not self._path.exists():
            logger.warning("Reviewer codes file not found at %s", self._path)
            self._codes = {}
            self._mtime = 0.0
            return

        try:
            raw = yaml.safe_load(self._path.read_text()) or {}
        except yaml.YAMLError as exc:
            logger.error("Failed to parse reviewer codes YAML: %s", exc)
            return

        rows: Iterable[dict] = raw.get("reviewers", []) or []
        codes: dict[str, ReviewerCode] = {}
        seen_codes: set[str] = set()
        for row in rows:
            try:
                model = ReviewerCode.model_validate(row)
            except Exception as exc:
                logger.error("Skipping invalid reviewer entry %r: %s", row, exc)
                continue
            if model.code in seen_codes:
                logger.error("Duplicate reviewer code %r — keeping first occurrence", model.code)
                continue
            seen_codes.add(model.code)
            codes[model.code] = model

        self._codes = codes
        self._mtime = self._path.stat().st_mtime
        logger.info("Loaded %d reviewer code(s) from %s", len(codes), self._path)

    def get(self, raw_code: str | None) -> ReviewerCode | None:
        """Look up a reviewer code (case-insensitive)."""
        self.reload_if_stale()
        if not raw_code:
            return None
        normalized = raw_code.strip().upper()
        return self._codes.get(normalized)

    def all(self) -> list[ReviewerCode]:
        self.reload_if_stale()
        return list(self._codes.values())
