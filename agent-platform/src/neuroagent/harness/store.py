"""In-memory and JSONL episode stores."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from neuroagent_schemas import ClinicalEpisode, EpisodeEvent
from pydantic import TypeAdapter

_EVENT_ADAPTER = TypeAdapter(EpisodeEvent)


class MemoryEpisodeStore:
    store_id = "memory"

    def __init__(self) -> None:
        self._events: list[Any] = []

    def append(self, event: Any) -> None:
        self._events.append(event)

    def load(self) -> ClinicalEpisode:
        return ClinicalEpisode(events=list(self._events))


class JsonlEpisodeStore(MemoryEpisodeStore):
    store_id = "jsonl"

    def __init__(self, path: str | Path) -> None:
        super().__init__()
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: Any) -> None:
        super().append(event)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.model_dump(mode="json"), sort_keys=True) + "\n")

    def load_existing(self) -> ClinicalEpisode:
        events = []
        if self.path.exists():
            with self.path.open(encoding="utf-8") as handle:
                for line in handle:
                    if line.strip():
                        events.append(_EVENT_ADAPTER.validate_json(line))
        self._events = events
        return self.load()
