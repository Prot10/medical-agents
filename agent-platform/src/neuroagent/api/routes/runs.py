"""Typed clinical-policy run endpoints."""

from __future__ import annotations

import asyncio
import json
import re
import threading
import time
from typing import Any, AsyncIterator, Callable

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from neuroagent_schemas import ClinicalEpisode, EpisodeEvent, NeuroBenchCase
from pydantic import BaseModel, ConfigDict

from ...evaluation.policy_reward import ClinicalPolicyReward
from ...harness.profile import HarnessProfile, load_profiles
from ...harness.runtime import boot_profile, context_from_profile
from ...harness.store import MemoryEpisodeStore

router = APIRouter(tags=["runs"])


class RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    profile_id: str
    persist: bool = True


class _RunCancelled(BaseException):
    """Raised inside the loop thread once the client has gone; never caught by the loop."""


class _StreamingStore(MemoryEpisodeStore):
    """Episode store that hands every appended event to ``on_event`` as it happens."""

    def __init__(self, on_event: Callable[[EpisodeEvent], None], cancelled: threading.Event) -> None:
        super().__init__()
        self._on_event = on_event
        self._cancelled = cancelled

    def append(self, event: EpisodeEvent) -> None:
        if self._cancelled.is_set():
            raise _RunCancelled
        super().append(event)
        self._on_event(event)


@router.get("/profiles")
def list_profiles(request: Request) -> list[dict[str, Any]]:
    """Return the checked experiment profiles; arbitrary model IDs are not accepted."""
    return [
        profile.model_dump(mode="json")
        for profile in load_profiles(request.app.state.profiles_dir).values()
    ]


def _resolve(body: RunRequest, request: Request) -> tuple[NeuroBenchCase, HarnessProfile]:
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
    return case, profile


def _persist(request: Request, case: NeuroBenchCase, profile: HarnessProfile, payload: dict) -> str:
    # Profile ids carry dots (``policy-qwen3.5-9b``) that the episode-id validator rejects; the
    # file name is only an address, the episode itself records the exact profile id.
    profile_slug = re.sub(r"[^A-Za-z0-9_-]", "-", profile.profile_id)
    episode_path = (
        request.app.state.episodes_dir / f"{case.case_id}_{profile_slug}_{time.time_ns()}.json"
    )
    episode_path.write_text(json.dumps(payload, indent=2))
    return episode_path.stem


def engineering_reward(episode: ClinicalEpisode, case: NeuroBenchCase) -> dict[str, Any]:
    """Policy reward for display, scored even when the case policy is still a draft.

    The production scorer refuses draft policies; the dashboard shows the same breakdown with
    the policy's review status beside it, so a draft score is never mistaken for a result.
    """
    reward = ClinicalPolicyReward(require_approved=False).score(episode, case)
    return {
        "reward": reward.model_dump(mode="json"),
        "policy_review_status": case.ground_truth.review_status.value,
    }


@router.post("/runs")
async def run_case(body: RunRequest, request: Request) -> dict[str, Any]:
    """Execute one case through a checked harness profile."""
    case, profile = _resolve(body, request)

    context = context_from_profile(profile, case, boot_profile(profile))
    episode = await asyncio.to_thread(context.loop.run, context)
    payload = episode.model_dump(mode="json")

    if body.persist:
        payload["episode_id"] = await asyncio.to_thread(_persist, request, case, profile, payload)

    return payload


def _sse(data: dict[str, Any]) -> str:
    return f"data: {json.dumps(data)}\n\n"


@router.post("/runs/stream")
async def stream_run(body: RunRequest, request: Request) -> StreamingResponse:
    """Execute one case and stream each typed episode event as it is appended.

    Frames are the episode events themselves, followed by one ``stream.result`` frame with the
    persisted episode id and the engineering reward, or one ``stream.error`` frame. A client
    that disconnects stops the run at its next event; a cancelled episode is not persisted.
    """
    case, profile = _resolve(body, request)
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
    cancelled = threading.Event()

    def publish(frame: dict[str, Any] | None) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, frame)

    def worker() -> None:
        try:
            context = context_from_profile(profile, case, boot_profile(profile))
            context.episode_store = _StreamingStore(
                lambda event: publish(event.model_dump(mode="json")), cancelled
            )
            episode = context.loop.run(context)
            result: dict[str, Any] = {"type": "stream.result", "episode_id": None}
            if body.persist:
                result["episode_id"] = _persist(
                    request, case, profile, episode.model_dump(mode="json")
                )
            result.update(engineering_reward(episode, case))
            publish(result)
        except _RunCancelled:
            pass
        except Exception as exc:
            publish({"type": "stream.error", "message": f"{type(exc).__name__}: {exc}"})
        finally:
            publish(None)

    async def frames() -> AsyncIterator[str]:
        threading.Thread(target=worker, name=f"run-{case.case_id}", daemon=True).start()
        try:
            while (frame := await queue.get()) is not None:
                yield _sse(frame)
        finally:
            cancelled.set()

    return StreamingResponse(
        frames(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
