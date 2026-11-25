"""Agent mode: a physician works a case as the agent does (services/agent_mode).

Every route answers 404 when the study is not configured, and a section that is not enabled on
this server (MIMIC, unless its directories are set) does not exist: no route serves it.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..dependencies import agent_mode_reviewer, get_reviewer_registry, require_admin
from ..schemas.agent_mode import ActionRequest
from ..schemas.reviewers import ReviewerCode
from ..services.agent_mode import service
from ..services.agent_mode.sets import AgentModeConfig, AgentSectionConfig
from ..services.reviewer_codes import ReviewerCodeRegistry

router = APIRouter(prefix="/agent-mode", tags=["agent-mode"])
admin_router = APIRouter(prefix="/admin/agent-mode", tags=["agent-mode-admin"])

_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


def _config(request: Request) -> AgentModeConfig:
    config: AgentModeConfig | None = getattr(request.app.state, "agent_mode", None)
    if config is None:
        raise _NOT_FOUND
    return config


def _section(request: Request, key: str, reviewer: ReviewerCode | None = None) -> AgentSectionConfig:
    """The section, or 404 when it is not served here or the code does not list it (a code
    learns nothing about a section it cannot open, not even that it exists)."""
    section = _config(request).sections.get(key)
    if section is None or (reviewer is not None and section.access not in reviewer.sections):
        raise _NOT_FOUND
    return section


def _run(call, *args: Any) -> Any:
    try:
        return call(*args)
    except service.AgentModeError as exc:
        raise HTTPException(status_code=exc.status, detail=exc.detail) from exc


def _deps(request: Request) -> tuple[Any, Any]:
    return request.app.state.agent_record_store, request.app.state.annotations_dir


@router.get("/sections")
def list_sections(request: Request, reviewer: ReviewerCode = Depends(agent_mode_reviewer)) -> list[dict[str, Any]]:
    """The sections this code opens on this server, with the reviewer's progress in each."""
    store, annotations = _deps(request)
    return [
        {key: value for key, value in service.worklist(section, reviewer, store, annotations).items() if key != "cases"}
        for section in _config(request).sections.values()
        if section.access in reviewer.sections
    ]


@router.get("/sections/{key}")
def get_worklist(key: str, request: Request, reviewer: ReviewerCode = Depends(agent_mode_reviewer)) -> dict[str, Any]:
    store, annotations = _deps(request)
    return service.worklist(_section(request, key, reviewer), reviewer, store, annotations)


@router.post("/sections/{key}/cases/{number}/start")
def start_case(
    key: str, number: int, request: Request, reviewer: ReviewerCode = Depends(agent_mode_reviewer)
) -> dict[str, Any]:
    section = _section(request, key, reviewer)
    return _run(service.start_case, _config(request), section, reviewer, number, *_deps(request))


@router.get("/sections/{key}/cases/{number}")
def get_case(
    key: str, number: int, request: Request, reviewer: ReviewerCode = Depends(agent_mode_reviewer)
) -> dict[str, Any]:
    section = _section(request, key, reviewer)
    return _run(service.get_state, _config(request), section, reviewer, number, *_deps(request))


@router.post("/sections/{key}/cases/{number}/actions")
def send_action(
    key: str,
    number: int,
    body: ActionRequest,
    request: Request,
    reviewer: ReviewerCode = Depends(agent_mode_reviewer),
) -> dict[str, Any]:
    section = _section(request, key, reviewer)
    return _run(service.act, _config(request), section, reviewer, number, body, *_deps(request))


@admin_router.get("/overview")
def admin_overview(
    request: Request,
    _admin: ReviewerCode = Depends(require_admin),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> dict[str, Any]:
    """Per-code progress and, per finished episode, the policy reward and its components."""
    store, annotations = _deps(request)
    return service.admin_overview(_config(request), store, registry.all(), annotations)


@admin_router.get("/sections/{key}/reviewers/{reviewer_id}/cases/{number}")
def admin_record(
    key: str, reviewer_id: str, number: int, request: Request, _admin: ReviewerCode = Depends(require_admin)
) -> dict[str, Any]:
    store, _ = _deps(request)
    try:
        return _run(service.admin_record, _section(request, key), store, reviewer_id, number)
    except ValueError as exc:
        raise _NOT_FOUND from exc
