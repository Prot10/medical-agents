"""Streaming run endpoint: event order, terminal frame, persistence, reward and cancellation."""

from __future__ import annotations

import json
import threading

import pytest
from fastapi.testclient import TestClient

from neuroagent.api.app import app
from neuroagent.api.routes import runs
from neuroagent.harness import ClinicalPolicyLoop, ModelTurn, RunContext
from neuroagent.tools.base import ToolResult
from neuroagent_schemas import ClinicalEpisode, RunStarted, SubmitAssessment, ToolAction

CASE_ID = "SE-M02"
PROFILE_ID = "policy-qwen3.5-9b"


class FakeEnvironment:
    environment_id = "fake"

    def __init__(self, case):
        self.case = case

    def tool_definitions(self):
        return [{"type": "function", "function": {"name": "analyze_eeg", "parameters": {}}}]

    def execute(self, action):
        return ToolResult(
            tool_name=action.tool_name,
            success=True,
            output={"impression": "epileptiform activity"},
            cost_usd=125.0,
        )


class FakeModel:
    adapter_id = "fake"
    model_id = "fake/model"

    def __init__(self, turns):
        self.turns = iter(turns)

    def next_action(self, **_kwargs):
        turn = next(self.turns)
        if isinstance(turn, Exception):
            raise turn
        return turn


def _assessment():
    return SubmitAssessment(
        primary_diagnosis="status epilepticus", confidence=0.9, urgency="emergent"
    )


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(app.state, "episodes_dir", tmp_path)
    return TestClient(app)


def _script(monkeypatch, turns):
    monkeypatch.setattr(runs, "boot_profile", lambda profile: None)
    monkeypatch.setattr(
        runs,
        "context_from_profile",
        lambda profile, case, services: RunContext(
            profile_id=profile.profile_id,
            model=FakeModel(turns),
            loop=ClinicalPolicyLoop(),
            environment=FakeEnvironment(case),
            max_turns=profile.max_turns,
        ),
    )


def _frames(response) -> list[dict]:
    return [
        json.loads(block[len("data: "):])
        for block in response.text.split("\n\n")
        if block.startswith("data: ")
    ]


def test_stream_emits_episode_events_then_one_result(client, monkeypatch, tmp_path):
    _script(
        monkeypatch,
        [ModelTurn(action=ToolAction(tool_name="analyze_eeg")), ModelTurn(action=_assessment())],
    )
    response = client.post(
        "/api/v1/runs/stream", json={"case_id": CASE_ID, "profile_id": PROFILE_ID}
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    frames = _frames(response)
    assert [frame["type"] for frame in frames] == [
        "run.started",
        "model.requested",
        "action.proposed",
        "observation.received",
        "model.requested",
        "action.proposed",
        "assessment.submitted",
        "run.completed",
        "stream.result",
    ]
    result = frames[-1]
    assert result["policy_review_status"] in {"draft", "needs_revision", "approved"}
    assert 0.0 <= result["reward"]["scalar"] <= 1.0

    persisted = tmp_path / f"{result['episode_id']}.json"
    episode = ClinicalEpisode.model_validate_json(persisted.read_text())
    assert [event.model_dump(mode="json") for event in episode.events] == frames[:-1]

    reward = client.get(f"/api/v1/episodes/{result['episode_id']}/reward")
    assert reward.status_code == 200
    assert reward.json()["reward"] == result["reward"]


def test_stream_without_persist_writes_nothing(client, monkeypatch, tmp_path):
    _script(monkeypatch, [ModelTurn(action=_assessment())])
    response = client.post(
        "/api/v1/runs/stream",
        json={"case_id": CASE_ID, "profile_id": PROFILE_ID, "persist": False},
    )
    assert _frames(response)[-1]["episode_id"] is None
    assert list(tmp_path.iterdir()) == []


def test_model_error_is_an_episode_event_not_a_stream_error(client, monkeypatch):
    _script(monkeypatch, [RuntimeError("server down")])
    frames = _frames(
        client.post("/api/v1/runs/stream", json={"case_id": CASE_ID, "profile_id": PROFILE_ID})
    )
    assert frames[-2]["type"] == "run.failed"
    assert frames[-2]["reason"] == "model_error"
    assert frames[-1]["type"] == "stream.result"


def test_boot_failure_ends_the_stream_with_an_error_frame(client, monkeypatch):
    def broken(profile):
        raise ConnectionError("no model server")

    monkeypatch.setattr(runs, "boot_profile", broken)
    frames = _frames(
        client.post("/api/v1/runs/stream", json={"case_id": CASE_ID, "profile_id": PROFILE_ID})
    )
    assert frames == [{"type": "stream.error", "message": "ConnectionError: no model server"}]


@pytest.mark.parametrize(
    "body",
    [
        {"case_id": "NOPE-X01", "profile_id": PROFILE_ID},
        {"case_id": CASE_ID, "profile_id": "not-a-profile"},
    ],
)
def test_unknown_case_or_profile_is_rejected_before_streaming(client, body):
    assert client.post("/api/v1/runs/stream", json=body).status_code == 404


def test_cancelled_store_stops_the_loop_without_recording():
    seen = []
    cancelled = threading.Event()
    store = runs._StreamingStore(seen.append, cancelled)
    event = RunStarted(turn=0, case_id=CASE_ID, profile_id=PROFILE_ID, model_id="m")
    store.append(event)
    cancelled.set()
    with pytest.raises(runs._RunCancelled):
        store.append(event)
    assert seen == [event]
    assert len(store.load().events) == 1
