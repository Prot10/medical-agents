"""Tests for the audited API security/robustness fixes.

Covers episode-id path traversal validation, the CORS allowlist, hospital-rule
mutation serialization, review-API rate-limiter keying, and annotation-store
write locking.
"""

from __future__ import annotations

import threading

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.requests import Request as StarletteRequest

from neuroagent.api.routes.episodes import validate_episode_id
from neuroagent.datasets import CANONICAL_DATASET_VERSION
from neuroagent.review_api.services.annotation_store import AnnotationStore
from neuroagent.review_api.services.rate_limit import AuthRateLimiter


# ---------------------------------------------------------------------------
# Persisted episode path traversal


@pytest.mark.parametrize("episode_id", ["TIA-S001_123456", "CASE_1-RS002_999", "abc"])
def test_validate_episode_id_accepts_real_ids(episode_id):
    assert validate_episode_id(episode_id) == episode_id


@pytest.mark.parametrize(
    "episode_id",
    ["", "..", "../secrets", "a/b", "a\\\\b", "..\\\\..\\\\x", "x/../y", "a.json", "a b"],
)
def test_validate_episode_id_rejects_traversal(episode_id):
    with pytest.raises(HTTPException) as exc:
        validate_episode_id(episode_id)
    assert exc.value.status_code == 400


def test_episode_endpoints_reject_traversal():
    from neuroagent.api.app import app

    client = TestClient(app)
    resp = client.get("/api/v1/episodes/..%5C..%5Cx")
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Fix 5: CORS


def test_cors_origins_env_extension(monkeypatch):
    from neuroagent.api.app import _cors_origins

    monkeypatch.delenv("NEUROAGENT_CORS_ORIGINS", raising=False)
    origins = _cors_origins()
    assert "http://localhost:8888" in origins
    assert "*" not in origins

    monkeypatch.setenv(
        "NEUROAGENT_CORS_ORIGINS", "http://192.168.1.10:5173, http://0.0.0.0:5173"
    )
    origins = _cors_origins()
    assert "http://192.168.1.10:5173" in origins
    assert "http://0.0.0.0:5173" in origins


def test_cors_rejects_unknown_origin_allows_localhost():
    from neuroagent.api.app import app

    client = TestClient(app)
    preflight = {"Access-Control-Request-Method": "GET"}

    resp = client.options(
        "/api/v1/episodes", headers={"Origin": "http://evil.example", **preflight}
    )
    assert "access-control-allow-origin" not in resp.headers

    resp = client.options(
        "/api/v1/episodes", headers={"Origin": "http://localhost:8888", **preflight}
    )
    assert resp.headers.get("access-control-allow-origin") == "http://localhost:8888"
    # Credentials must not be allowed with the browser-facing API.
    assert resp.headers.get("access-control-allow-credentials") != "true"


# ---------------------------------------------------------------------------
# Fix 8: hospital rules mutations still work (now serialized by a lock)


def _hospitals_app(rules_dir) -> FastAPI:
    from neuroagent.api.routes import hospitals

    app = FastAPI()
    app.state.rules_dir = str(rules_dir)
    app.include_router(hospitals.router, prefix="/api/v1")
    return app


def test_hospital_rules_create_update_delete(tmp_path):
    from neuroagent.rules.rules_engine import AVAILABLE_HOSPITALS

    hospital_id = next(iter(AVAILABLE_HOSPITALS))
    (tmp_path / hospital_id).mkdir()
    client = TestClient(_hospitals_app(tmp_path))

    pathway = {
        "name": "Test Pathway",
        "description": "d",
        "triggers": ["t"],
        "steps": [{"action": "a", "timing": "now", "mandatory": True}],
        "contraindicated": [],
    }
    resp = client.post(f"/api/v1/hospitals/{hospital_id}/rules", json=pathway)
    assert resp.status_code == 201

    resp = client.post(f"/api/v1/hospitals/{hospital_id}/rules", json=pathway)
    assert resp.status_code == 409  # duplicate slug

    pathway["description"] = "updated"
    resp = client.put(f"/api/v1/hospitals/{hospital_id}/rules/0", json=pathway)
    assert resp.status_code == 200
    assert resp.json()["description"] == "updated"

    resp = client.put(f"/api/v1/hospitals/{hospital_id}/rules/5", json=pathway)
    assert resp.status_code == 404  # out of range

    resp = client.delete(f"/api/v1/hospitals/{hospital_id}/rules/0")
    assert resp.status_code == 200
    assert list((tmp_path / hospital_id).glob("*.yaml")) == []


# ---------------------------------------------------------------------------
# Fix 9: rate limiter keying


def _make_request(headers: dict[str, str], client_host: str | None = "10.0.0.1"):
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
    }
    if client_host is not None:
        scope["client"] = (client_host, 12345)
    return StarletteRequest(scope)


def test_rate_limiter_ignores_spoofable_headers():
    key = AuthRateLimiter.client_key(
        _make_request({"CF-Connecting-IP": "6.6.6.6", "X-Forwarded-For": "7.7.7.7"})
    )
    assert key == "10.0.0.1"


def test_rate_limiter_uses_x_real_ip_from_proxy():
    key = AuthRateLimiter.client_key(
        _make_request({"X-Real-IP": "203.0.113.9", "X-Forwarded-For": "7.7.7.7"})
    )
    assert key == "203.0.113.9"


def test_rate_limiter_falls_back_to_socket_peer():
    assert AuthRateLimiter.client_key(_make_request({})) == "10.0.0.1"
    assert AuthRateLimiter.client_key(_make_request({}, client_host=None)) == "unknown"


def test_rate_limiter_lockout_not_bypassable_by_header_rotation():
    limiter = AuthRateLimiter(max_failures=3, window_seconds=60, lockout_seconds=60)
    for spoofed in ("1.1.1.1", "2.2.2.2", "3.3.3.3"):
        request = _make_request({"X-Forwarded-For": spoofed})
        limiter.record_failure(AuthRateLimiter.client_key(request))
    # All three failures landed on the real peer address → locked out.
    assert limiter.retry_after("10.0.0.1") is not None


# ---------------------------------------------------------------------------
# Fix 10: annotation store locking


def test_annotation_store_lock_is_shared_across_store_instances(tmp_path):
    first_store = AnnotationStore(tmp_path)
    second_store = AnnotationStore(tmp_path)
    first_lock = first_store.lock_for(
        CANONICAL_DATASET_VERSION, "REV-1", "TIA-RS001"
    )
    second_lock = second_store.lock_for(
        CANONICAL_DATASET_VERSION, "REV-1", "TIA-RS001"
    )
    assert first_lock is second_lock
    other = first_store.lock_for(
        CANONICAL_DATASET_VERSION, "REV-2", "TIA-RS001"
    )
    assert other is not first_lock


def test_annotation_store_concurrent_init_is_consistent(tmp_path):
    store = AnnotationStore(tmp_path)
    n = 8
    barrier = threading.Barrier(n)
    results = []

    def worker():
        barrier.wait()
        results.append(store.load_or_init(CANONICAL_DATASET_VERSION, "REV-1", "CASE-1"))

    threads = [threading.Thread(target=worker) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    opened = {r.first_opened_at for r in results}
    assert len(opened) == 1, "load_or_init raced and re-initialized the review"


def test_annotation_store_concurrent_writes_do_not_lose_updates(tmp_path):
    store = AnnotationStore(tmp_path)
    version, code, case_id = CANONICAL_DATASET_VERSION, "REV-1", "CASE-2"
    store.load_or_init(version, code, case_id)

    n_threads, n_iters = 8, 25

    def worker():
        for _ in range(n_iters):
            with store.lock_for(version, code, case_id):
                review = store.load_or_init(version, code, case_id)
                review.time_spent_seconds += 1
                store.save(review)

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    final = store.load(version, code, case_id)
    assert final is not None
    assert final.time_spent_seconds == n_threads * n_iters