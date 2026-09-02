"""Typed clinical-policy run endpoints."""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from ...harness.profile import load_profiles
from ...harness.runtime import boot_profile, context_from_profile

router = APIRouter(tags=["runs"])


class RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    profile_id: str
    persist: bool = True


@router.get("/profiles")
def list_profiles(request: Request) -> list[dict[str, Any]]:
    """Return the checked experiment profiles; arbitrary model IDs are not accepted."""
    return [
        profile.model_dump(mode="json")
        for profile in load_profiles(request.app.state.profiles_dir).values()
    ]


@router.post("/runs")
async def run_case(body: RunRequest, request: Request) -> dict[str, Any]:
    """Execute one case through a checked harness profile."""
    case = request.app.state.case_objects.get(body.case_id)
    if case is None:
        raise HTTPException(status_code=404, detail=f"case {body.case_id!r} not found")

    profiles = load_profiles(request.app.state.profiles_dir)
    profile = profiles.get(body.profile_id)
    if profile is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"profile {body.profile_id!r} not found",
                "available_profiles": sorted(profiles),
            },
        )

    context = context_from_profile(profile, case, boot_profile(profile))
    episode = await asyncio.to_thread(context.loop.run, context)
    payload = episode.model_dump(mode="json")

    if body.persist:
        episode_path = (
            request.app.state.episodes_dir
            / f"{case.case_id}_{profile.profile_id}_{time.time_ns()}.json"
        )
        await asyncio.to_thread(episode_path.write_text, json.dumps(payload, indent=2))
        payload["episode_id"] = episode_path.stem

    return payload
