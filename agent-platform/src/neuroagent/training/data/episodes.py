"""Typed episode records and their rendering into SFT examples.

An SFT example is rendered by the same transcript codec the harness uses at inference, so the
trained format and the evaluated format cannot drift apart.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from neuroagent_schemas import ClinicalEpisode, NeuroBenchCase, RunCompleted
from pydantic import BaseModel, ConfigDict, field_validator

from ...harness.adapters import SUBMIT_TOOL
from ...harness.context import transcript
from ...harness.environment import NeuroBenchEnvironment

EpisodeLabel = Literal["candidate_not_gold", "physician_approved"]


class EpisodeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    candidate_id: str
    case_id: str
    label: EpisodeLabel
    provenance: dict[str, Any] = {}
    episode: ClinicalEpisode

    @field_validator("episode")
    @classmethod
    def _completed(cls, episode: ClinicalEpisode) -> ClinicalEpisode:
        if not episode.events or not isinstance(episode.events[-1], RunCompleted):
            raise ValueError("only completed episodes can be training examples")
        return episode


def load_episode_records(path: str | Path, *, allow_candidates: bool = False) -> list[EpisodeRecord]:
    allowed = {"physician_approved"} | ({"candidate_not_gold"} if allow_candidates else set())
    records = [
        record
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
        if (record := EpisodeRecord.model_validate_json(line)).label in allowed
    ]
    if not records:
        raise ValueError(
            "no training-eligible episodes; physician_approved is required unless "
            "allow_candidates=True is explicitly set for bootstrap experiments"
        )
    return records


def load_case_map(path: str | Path) -> dict[str, NeuroBenchCase]:
    return {
        item.stem: NeuroBenchCase.model_validate_json(item.read_text())
        for item in Path(path).glob("*.json")
    }


def tool_catalogue(case: NeuroBenchCase) -> list[dict[str, Any]]:
    return [*NeuroBenchEnvironment(case).tool_definitions(), SUBMIT_TOOL]


def sft_rows(record: EpisodeRecord, case: NeuroBenchCase) -> list[dict[str, Any]]:
    """One prompt/completion pair per model turn: the transcript so far, then that turn's action."""
    messages = transcript(case, record.episode)
    tools = tool_catalogue(case)
    return [
        {"prompt": messages[:index], "completion": [message], "tools": tools}
        for index, message in enumerate(messages)
        if message["role"] == "assistant"
    ]
