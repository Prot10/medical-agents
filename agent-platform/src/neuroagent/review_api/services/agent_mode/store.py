"""Filesystem store of agent-mode records.

One record per (reviewer, section, case)::

    <records_dir>/<section>/<set id>/<reviewer id>/<case id>.json          the record, replaced atomically
    <records_dir>/<section>/<set id>/<reviewer id>/<case id>.events.jsonl  append-only log of what happened

The record holds the episode and the physician-only data; the log holds every request as it was
received (with server timestamps), so the record can be audited or rebuilt. The reviewer directory
is the code's public id, never the secret code.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
import threading
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ...schemas.agent_mode import AgentRecord
from .sets import AgentSectionConfig

_REVIEWER_ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,31}$")
_CASE_ID = re.compile(r"^[A-Za-z0-9_.\-]{1,96}$")
_locks: dict[str, threading.RLock] = defaultdict(threading.RLock)
_locks_guard = threading.Lock()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AgentRecordStore:
    def reviewer_dir(self, section: AgentSectionConfig, reviewer_id: str) -> Path:
        if not _REVIEWER_ID.fullmatch(reviewer_id):
            raise ValueError(f"invalid reviewer id: {reviewer_id!r}")
        return section.records_dir / section.key / section.set_id / reviewer_id

    def path(self, section: AgentSectionConfig, reviewer_id: str, case_id: str) -> Path:
        if not _CASE_ID.fullmatch(case_id):
            raise ValueError(f"invalid case id: {case_id!r}")
        return self.reviewer_dir(section, reviewer_id) / f"{case_id}.json"

    def lock(self, section: AgentSectionConfig, reviewer_id: str) -> threading.RLock:
        """One lock per reviewer and section: a reviewer works one case at a time."""
        with _locks_guard:
            return _locks[str(self.reviewer_dir(section, reviewer_id))]

    def load(self, section: AgentSectionConfig, reviewer_id: str, case_id: str) -> AgentRecord | None:
        path = self.path(section, reviewer_id, case_id)
        if not path.exists():
            return None
        return AgentRecord.model_validate_json(path.read_text())

    def save(self, section: AgentSectionConfig, record: AgentRecord) -> None:
        path = self.path(section, record.reviewer_id, record.case_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=path.parent, prefix=f".{path.stem}.", suffix=".tmp", delete=False) as fh:
            fh.write(record.model_dump_json(indent=2))
            fh.flush()
            os.fsync(fh.fileno())
            tmp = Path(fh.name)
        tmp.replace(path)

    def log(self, section: AgentSectionConfig, reviewer_id: str, case_id: str, kind: str, **payload: Any) -> None:
        path = self.path(section, reviewer_id, case_id).with_suffix(".events.jsonl")
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps({"at": utcnow().isoformat(), "type": kind, **payload}, ensure_ascii=False)
        with path.open("a") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())

    def records_of(self, section: AgentSectionConfig, reviewer_id: str) -> dict[str, AgentRecord]:
        directory = self.reviewer_dir(section, reviewer_id)
        if not directory.is_dir():
            return {}
        records = (AgentRecord.model_validate_json(path.read_text()) for path in sorted(directory.glob("*.json")))
        return {record.case_id: record for record in records}

    def reviewer_ids(self, section: AgentSectionConfig) -> list[str]:
        directory = section.records_dir / section.key / section.set_id
        if not directory.is_dir():
            return []
        return sorted(entry.name for entry in directory.iterdir() if entry.is_dir() and _REVIEWER_ID.fullmatch(entry.name))
