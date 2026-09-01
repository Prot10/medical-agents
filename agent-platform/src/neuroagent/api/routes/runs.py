"""Typed clinical-policy run endpoints."""

from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from ...harness.profile import HarnessProfile, load_profile
from ...harness.runtime import context_from_profile


router = APIRouter(tags=["runs"])


class RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    profile_id: str = "policy-qwen3.5-9b"
    persist: bool = True


def _load_profiles(profile_dir: Path) -> dict[str, tuple[Path, HarnessProfile]]:
    profiles: dict[str, tuple[Path, HarnessProfile]] = {}
    for path in sorted(profile_dir.glob("*.yaml")):
        profile = load_profile(path)
        if profile.profile_id in profiles:
            raise RuntimeError(f"duplicate profile_id: {profile.profile_id}")
        profiles[profile.profile_id] = (path, profile)
    return profiles


@router.get("/profiles")
def list_profiles(request: Request) -> list[dict[str, Any]]:
    """Return the checked experiment profiles; arbitrary model IDs are not accepted."""

    profiles = _load_profiles(request.app.state.profiles_dir)
    return [
        {
            "profile_id": profile.profile_id,
            "max_turns": profile.max_turns,
            "max_cost_usd": profile.max_cost_usd,
            "plugins": [
                {"id": item.id, "config": item.config}
                for item in profile.plugins
            ],
        }
        for _, profile in profiles.values()
    ]


@router.post("/runs")
async def run_case(body: RunRequest, request: Request) -> dict[str, Any]:
    """Execute one case through a checked harness profile."""

    case = request.app.state.case_objects.get(body.case_id)
    if case is None:
        raise HTTPException(
            status_code=404,
            detail=f"case {body.case_id!r} not found",
        )

    profiles = _load_profiles(request.app.state.profiles_dir)
    entry = profiles.get(body.profile_id)
    if entry is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"profile {body.profile_id!r} not found",
                "available_profiles": sorted(profiles),
            },
        )

    _, profile = entry
    context = context_from_profile(profile, case)
    episode = await asyncio.to_thread(context.loop.run, context)
    payload = episode.model_dump(mode="json")

    if body.persist:
        episode_path = (
            request.app.state.episodes_dir
            / f"{case.case_id}_{profile.profile_id}_{time.time_ns()}.json"
        )
        await asyncio.to_thread(
            episode_path.write_text,
            json.dumps(payload, indent=2),
        )
        payload["episode_id"] = episode_path.stem

    return payload
