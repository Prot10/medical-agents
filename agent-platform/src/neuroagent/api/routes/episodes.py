"""Persisted typed clinical-episode endpoints."""

from __future__ import annotations

import re

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from neuroagent_schemas import (
    ActionProposed,
    ClinicalEpisode,
    ObservationReceived,
    RunCompleted,
    RunFailed,
    RunStarted,
    ToolAction,
)

router = APIRouter(tags=["episodes"])
_EPISODE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_\-]+$")


def validate_episode_id(episode_id: str) -> str:
    """Reject identifiers that could escape the episode directory."""

    if not episode_id or not _EPISODE_ID_PATTERN.fullmatch(episode_id):
        raise HTTPException(status_code=400, detail="Invalid episode ID")
    return episode_id


def _summary(path, case_index: dict[str, dict]) -> dict:
    episode = ClinicalEpisode.model_validate_json(path.read_text())
    started = next(event for event in episode.events if isinstance(event, RunStarted))
    terminal = next(
        (
            event
            for event in reversed(episode.events)
            if isinstance(event, (RunCompleted, RunFailed))
        ),
        None,
    )
    tool_actions = [
        event.action
        for event in episode.events
        if isinstance(event, ActionProposed) and isinstance(event.action, ToolAction)
    ]
    latency_seconds = sum(
        event.latency_seconds
        for event in episode.events
        if isinstance(event, ActionProposed)
    )
    fallback_calls = sum(
        event.from_fallback
        for event in episode.events
        if isinstance(event, ObservationReceived)
    )
    case_meta = case_index.get(started.case_id, {})
    return {
        "episode_id": path.stem,
        "case_id": started.case_id,
        "profile_id": started.profile_id,
        "model_id": started.model_id,
        "condition": case_meta.get("condition", ""),
        "difficulty": case_meta.get("difficulty", ""),
        "status": terminal.type if terminal is not None else "incomplete",
        "tool_call_count": len(tool_actions),
        "tools_called": [action.tool_name for action in tool_actions],
        "fallback_call_count": fallback_calls,
        "total_tokens": episode.total_tokens,
        "total_cost_usd": episode.total_cost_usd,
        "model_latency_seconds": latency_seconds,
    }


@router.get("/episodes")
def list_episodes(request: Request) -> list[dict]:
    """List valid persisted typed episodes."""

    case_index: dict[str, dict] = getattr(request.app.state, "case_index", {})
    result = []
    for path in sorted(request.app.state.episodes_dir.glob("*.json")):
        try:
            result.append(_summary(path, case_index))
        except Exception:
            continue
    return result


@router.get("/episodes/{episode_id}")
def get_episode(episode_id: str, request: Request) -> dict:
    """Return one validated clinical episode."""

    validate_episode_id(episode_id)
    path = request.app.state.episodes_dir / f"{episode_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Episode {episode_id!r} not found")
    episode = ClinicalEpisode.model_validate_json(path.read_text())
    return episode.model_dump(mode="json")


@router.delete("/episodes/{episode_id}", status_code=204)
def delete_episode(episode_id: str, request: Request) -> Response:
    """Delete one persisted clinical episode."""

    validate_episode_id(episode_id)
    path = request.app.state.episodes_dir / f"{episode_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Episode {episode_id!r} not found")
    path.unlink()
    return Response(status_code=204)
