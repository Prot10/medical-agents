"""Typed episode loading and model-family SFT codecs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from neuroagent_schemas import (
    ActionProposed,
    ClinicalEpisode,
    NeuroBenchCase,
    ObservationReceived,
)
from pydantic import BaseModel, ConfigDict

from ...harness.context import POLICY_SYSTEM_PROMPT, format_patient_info


class EpisodeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    candidate_id: str
    case_id: str
    source_style: str
    label: Literal["candidate_not_gold", "physician_approved"]
    episode: ClinicalEpisode


def load_episode_records(
    path: str | Path,
    *,
    allow_candidates: bool = False,
) -> list[EpisodeRecord]:
    allowed = {"physician_approved"}
    if allow_candidates:
        allowed.add("candidate_not_gold")
    records = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            record = EpisodeRecord.model_validate_json(line)
            if record.label in allowed:
                records.append(record)
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


def episode_to_messages(
    record: EpisodeRecord,
    case: NeuroBenchCase,
    *,
    codec: Literal["native-tools", "json-action"],
) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": POLICY_SYSTEM_PROMPT},
        {"role": "user", "content": format_patient_info(case)},
    ]
    call_index = 0
    for event in record.episode.events:
        if isinstance(event, ActionProposed):
            action = event.action
            if codec == "json-action":
                messages.append(
                    {
                        "role": "assistant",
                        "content": json.dumps(action.model_dump(mode="json"), sort_keys=True),
                    }
                )
            elif action.type == "tool":
                call_index += 1
                messages.append(
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": f"call_{call_index}",
                                "type": "function",
                                "function": {
                                    "name": action.tool_name,
                                    "arguments": json.dumps(action.arguments, sort_keys=True),
                                },
                            }
                        ],
                    }
                )
            else:
                call_index += 1
                arguments = action.model_dump(mode="json", exclude={"type"})
                messages.append(
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": f"call_{call_index}",
                                "type": "function",
                                "function": {
                                    "name": "submit_assessment",
                                    "arguments": json.dumps(arguments, sort_keys=True),
                                },
                            }
                        ],
                    }
                )
        elif isinstance(event, ObservationReceived):
            payload = json.dumps(
                {
                    "success": event.success,
                    "output": event.output,
                    "error_message": event.error_message,
                },
                sort_keys=True,
            )
            if codec == "native-tools":
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": f"call_{call_index}",
                        "name": event.tool_name,
                        "content": payload,
                    }
                )
            else:
                messages.append(
                    {
                        "role": "user",
                        "content": f"Observation from {event.tool_name}: {payload}",
                    }
                )
    return messages
