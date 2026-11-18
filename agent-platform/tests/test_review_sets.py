"""Review sets: a fixed case subset re-reviewed in a space of its own.

The re-check set must hold one case per condition, serve only its cases, and file its reviews
apart from the first review of the same case (which must stay untouched).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from neuroagent.datasets import DATASETS
from neuroagent.review_api.app import create_app
from neuroagent.review_api.config import REVIEW_SETS_PATH
from neuroagent.review_api.services.annotation_store import AnnotationStore
from neuroagent.review_api.services.review_sets import load_review_sets
from neuroagent.review_api.services.reviewer_codes import ReviewerCodeRegistry

CODE = "TEST-REVIEW-SETS"
SET_ID = "recheck-2026-11"


def test_recheck_set_has_one_existing_case_per_condition():
    review_set = load_review_sets(REVIEW_SETS_PATH)[SET_ID]
    cases_dir = DATASETS[review_set.base].path / "cases"
    every_condition = {p.stem.rsplit("-", 1)[0] for p in cases_dir.glob("*.json")}
    conditions = [c.rsplit("-", 1)[0] for c in review_set.case_ids]
    assert sorted(conditions) == sorted(every_condition)
    assert all((cases_dir / f"{c}.json").exists() for c in review_set.case_ids)


def test_recheck_set_serves_its_own_frozen_copies():
    """The full review may serve an older version; the set keeps the corrected one."""
    review_set = load_review_sets(REVIEW_SETS_PATH)[SET_ID]
    assert review_set.cases_dir is not None
    stored = sorted(p.stem for p in (review_set.cases_dir / "cases").glob("*.json"))
    assert stored == sorted(review_set.case_ids)


def test_bad_review_set_file_is_refused(tmp_path: Path):
    bad = tmp_path / "sets.yaml"
    bad.write_text("x:\n  base: nope\n  cases: [ALS-S10]\n")
    with pytest.raises(ValueError):
        load_review_sets(bad)
    bad.write_text("x:\n  base: neurobench\n  cases: [ALS-S10, ALS-S10]\n")
    with pytest.raises(ValueError):
        load_review_sets(bad)


@pytest.fixture(scope="module")
def app():
    return create_app()


@pytest.fixture
def client(app, tmp_path: Path):
    codes = tmp_path / "reviewer_codes.yaml"
    codes.write_text(f"reviewers:\n  - code: {CODE}\n    name: Test\n    role: reviewer\n")
    annotations = tmp_path / "annotations"
    app.state.annotation_store = AnnotationStore(annotations, extra_versions=app.state.review_sets)
    app.state.reviewer_registry = ReviewerCodeRegistry(codes)
    app.state.auth_limiter = None
    with TestClient(app) as test_client:
        test_client.headers["X-Reviewer-Code"] = CODE
        test_client.annotations = annotations
        yield test_client


def test_set_is_listed_and_serves_only_its_cases(client):
    sets = {s["id"]: s for s in client.get("/api/v1/review-sets").json()}
    case_ids = sets[SET_ID]["case_ids"]
    assert sets[SET_ID]["case_count"] == len(case_ids) == 20
    listed = [c["case_id"] for c in client.get(f"/api/v1/datasets/{SET_ID}/cases").json()]
    assert listed == case_ids
    outside = "ALS-S01" if "ALS-S01" not in case_ids else "ALS-S02"
    assert client.get(f"/api/v1/datasets/{SET_ID}/cases/{outside}").status_code == 404
    # The set is not offered as a dataset of its own in the dataset picker.
    assert SET_ID not in {d["version"] for d in client.get("/api/v1/datasets").json()}


def test_set_review_is_filed_apart_from_the_first_review(client):
    case_id = client.get("/api/v1/review-sets").json()[0]["case_ids"][0]
    first = client.annotations / "neurobench" / CODE / f"{case_id}.json"
    first.parent.mkdir(parents=True)
    client.get(f"/api/v1/datasets/neurobench/reviews/{case_id}")
    before = first.read_text()

    body = {"id": "c1", "comment": "Now correct.", "severity": "note"}
    assert client.post(f"/api/v1/datasets/{SET_ID}/reviews/{case_id}/comments", json=body).status_code == 201
    again = client.annotations / SET_ID / CODE / f"{case_id}.json"
    assert json.loads(again.read_text())["dataset_version"] == SET_ID
    assert first.read_text() == before
    progress = client.get(f"/api/v1/datasets/{SET_ID}/progress").json()
    assert progress["total_cases"] == 20
