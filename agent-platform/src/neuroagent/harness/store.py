"""Append-only in-memory episode store."""

from __future__ import annotations

from neuroagent_schemas import ClinicalEpisode, EpisodeEvent


class MemoryEpisodeStore:
    store_id = "memory"

    def __init__(self) -> None:
        self._events: list[EpisodeEvent] = []

    def append(self, event: EpisodeEvent) -> None:
        self._events.append(event)

    def load(self) -> ClinicalEpisode:
        return ClinicalEpisode(events=list(self._events))
