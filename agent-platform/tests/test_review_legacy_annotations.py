"""Reviews written before schema v2 and the per-dimension verdict stay usable.

Production reviews carry a terminal status without `policy_verdict`, and some annotate
ground-truth fields that schema v2 removed (`ground_truth.optimal_actions[3]`). They must load,
keep every annotation, and an error on a removed field must be resolvable so that it does not
block approval forever.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from neuroagent.review_api.app import create_app
from neuroagent.review_api.services.annotation_store import AnnotationStore
from neuroagent.review_api.services.reviewer_codes import ReviewerCodeRegistry

CODE = "NB-TEST-REVW-AAAA"
CASE = "ALS-M01"
VERDICT = {
    "scenario_plausibility": "approve",
    "diagnosis": "approve",
    "actions": "approve",
    "avoided_actions": "approve",
    "sequencing": "approve",
    "stopping": "approve",
    "assessment": "approve",
    "comment": "",
}


def _legacy_review(status: str) -> dict:
    """A review as the pre-v2 app wrote it: no policy_verdict key at all."""
    stamp = "2026-10-01T10:00:00Z"

    def annotation(ident: str, path: str, severity: str) -> dict:
        return {
            "id": ident,
            "field_path": path,
            "field_snippet": None,
            "comment": f"legacy {severity}",
            "severity": severity,
            "created_at": stamp,
            "updated_at": stamp,
            "resolved": False,
        }

    return {
        "case_id": CASE,
        "dataset_version": "neurobench",
        "reviewer_code": CODE,
        "status": status,
        "field_annotations": [
            annotation("removed", "ground_truth.optimal_actions[3]", "error"),
            annotation("kept", "followup_outputs[1]", "issue"),
        ],
        "case_comments": [],
        "first_opened_at": stamp,
        "last_updated_at": stamp,
        "last_active_at": None,
        "time_spent_seconds": 120,
    }


@pytest.fixture(scope="module")
def app():
    return create_app()


@pytest.fixture
def client(app, tmp_path: Path):
    codes = tmp_path / "reviewer_codes.yaml"
    codes.write_text(f"reviewers:\n  - code: {CODE}\n    name: Test\n    role: reviewer\n")
    annotations = tmp_path / "annotations"
    review_dir = annotations / "neurobench" / CODE
    review_dir.mkdir(parents=True)
    (review_dir / f"{CASE}.json").write_text(json.dumps(_legacy_review("needs_changes")))
    app.state.annotation_store = AnnotationStore(annotations)
    app.state.reviewer_registry = ReviewerCodeRegistry(codes)
    app.state.auth_limiter = None
    with TestClient(app) as test_client:
        test_client.headers["X-Reviewer-Code"] = CODE
        test_client.review_file = review_dir / f"{CASE}.json"
        yield test_client


def _base(path: str = "") -> str:
    return f"/api/v1/datasets/neurobench/reviews/{CASE}{path}"


def test_legacy_review_loads_with_every_annotation(client):
    review = client.get(_base()).json()
    assert review["status"] == "needs_changes"
    assert review["policy_verdict"] is None
    assert [a["id"] for a in review["field_annotations"]] == ["removed", "kept"]


def test_error_on_removed_field_blocks_approval_until_resolved(client):
    approve = {"status": "approved", "policy_verdict": VERDICT}
    blocked = client.patch(_base("/status"), json=approve)
    assert blocked.status_code == 422
    # A refused request leaves the file as it was.
    assert json.loads(client.review_file.read_text())["status"] == "needs_changes"

    resolved = client.put(_base("/annotations/removed"), json={"resolved": True})
    assert resolved.status_code == 200
    kept = {a["id"]: a for a in resolved.json()["field_annotations"]}
    assert kept["removed"]["resolved"] is True
    assert kept["removed"]["comment"] == "legacy error"
    assert kept["removed"]["field_path"] == "ground_truth.optimal_actions[3]"

    approved = client.patch(_base("/status"), json=approve)
    assert approved.status_code == 200
    assert approved.json()["policy_verdict"]["actions"] == "approve"
    assert len(approved.json()["field_annotations"]) == 2


def test_reopening_restores_the_block(client):
    client.put(_base("/annotations/removed"), json={"resolved": True})
    client.put(_base("/annotations/removed"), json={"resolved": False})
    blocked = client.patch(_base("/status"), json={"status": "approved", "policy_verdict": VERDICT})
    assert blocked.status_code == 422
