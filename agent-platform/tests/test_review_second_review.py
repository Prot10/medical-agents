"""Second reviews: each physician reviews, in a set assigned to their code, the cases the other
physician already reviewed, in the exact version the other annotated.

A guided code (``review_sets`` in reviewer_codes.yaml) must reach its set and nothing else; the
sets reserved to assigned codes must stay hidden from every other reviewer; the frozen copies
must be the cases of master 481dff25 (what the VPS served when the first reviews were written).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from neuroagent.datasets import REPO_ROOT
from neuroagent.review_api.app import create_app
from neuroagent.review_api.config import REVIEW_SETS_PATH
from neuroagent.review_api.schemas.reviewers import ReviewerCode
from neuroagent.review_api.services.annotation_store import AnnotationStore
from neuroagent.review_api.services.review_sets import load_review_sets
from neuroagent.review_api.services.reviewer_codes import ReviewerCodeRegistry

ISCH = "second-review-isch-str-2026-11"
NMDAR = "second-review-nmdar-enc-2026-11"
ANNOTATED_COMMIT = "481dff25"
GUIDED = "TEST-GUIDED-ISCH"
PLAIN = "TEST-PLAIN"
ADMIN = "TEST-ADMIN"


@pytest.mark.parametrize("set_id, condition", [(ISCH, "ISCH-STR"), (NMDAR, "NMDAR-ENC")])
def test_second_review_sets_are_frozen_at_the_annotated_version(set_id, condition):
    review_set = load_review_sets(REVIEW_SETS_PATH)[set_id]
    assert review_set.kind == "second_review" and review_set.assigned_only
    assert len(review_set.case_ids) == 20
    assert all(c.startswith(condition + "-") for c in review_set.case_ids)
    assert review_set.cases_dir is not None
    stored = sorted(p.stem for p in (review_set.cases_dir / "cases").glob("*.json"))
    assert stored == sorted(review_set.case_ids)
    if subprocess.run(["git", "cat-file", "-e", ANNOTATED_COMMIT], cwd=REPO_ROOT).returncode:
        pytest.skip("annotated commit not in this clone")
    for case_id in review_set.case_ids:
        frozen = (review_set.cases_dir / "cases" / f"{case_id}.json").read_bytes()
        annotated = subprocess.run(
            ["git", "show", f"{ANNOTATED_COMMIT}:data/neurobench/cases/{case_id}.json"],
            cwd=REPO_ROOT, capture_output=True, check=True,
        ).stdout
        assert frozen == annotated, case_id


def test_review_sets_field_is_for_dataset_review_codes_only():
    with pytest.raises(ValueError):
        ReviewerCode(code="X-ADMIN", name="A", role="admin", review_sets=[ISCH])
    with pytest.raises(ValueError):
        ReviewerCode(code="X-AGENT", name="A", sections=["agent_synthetic"], review_sets=[ISCH])
    with pytest.raises(ValueError):
        ReviewerCode(code="X-TWICE", name="A", review_sets=[ISCH, ISCH])


@pytest.fixture(scope="module")
def app():
    return create_app()


@pytest.fixture
def client(app, tmp_path: Path):
    codes = tmp_path / "reviewer_codes.yaml"
    codes.write_text(
        "reviewers:\n"
        f"  - {{code: {GUIDED}, name: Guided, review_sets: [{ISCH}]}}\n"
        f"  - {{code: {PLAIN}, name: Plain}}\n"
        f"  - {{code: {ADMIN}, name: Admin, role: admin}}\n"
        "  - {code: TEST-BROKEN, name: Broken, review_sets: [no-such-set]}\n"
    )
    app.state.annotation_store = AnnotationStore(tmp_path / "ann", extra_versions=app.state.review_sets)
    app.state.reviewer_registry = ReviewerCodeRegistry(codes)
    app.state.auth_limiter = None
    with TestClient(app) as test_client:
        yield test_client


def _get(client, code, path):
    return client.get(f"/api/v1{path}", headers={"X-Reviewer-Code": code})


def test_guided_code_sees_and_reaches_only_its_set(client):
    me = _get(client, GUIDED, "/reviewers/me").json()
    assert me["review_sets"] == [ISCH]
    sets = _get(client, GUIDED, "/review-sets").json()
    assert [s["id"] for s in sets] == [ISCH] and sets[0]["kind"] == "second_review"
    assert _get(client, GUIDED, "/datasets").json() == []
    case_id = sets[0]["case_ids"][0]
    assert _get(client, GUIDED, f"/datasets/{ISCH}/cases/{case_id}").status_code == 200
    assert _get(client, GUIDED, f"/datasets/{ISCH}/reviews/{case_id}").status_code == 200
    for version in ("neurobench", "recheck-2026-11", NMDAR):
        assert _get(client, GUIDED, f"/datasets/{version}/cases").status_code == 403
        assert _get(client, GUIDED, f"/datasets/{version}/progress").status_code == 403
    assert _get(client, GUIDED, "/datasets/neurobench/tool-catalog").status_code == 403


def test_reserved_sets_stay_hidden_from_other_reviewers(client):
    assert [s["id"] for s in _get(client, PLAIN, "/review-sets").json()] == ["recheck-2026-11"]
    assert _get(client, PLAIN, f"/datasets/{ISCH}/cases").status_code == 403
    assert _get(client, PLAIN, "/datasets/neurobench/cases").status_code == 200
    admin_sets = {s["id"] for s in _get(client, ADMIN, "/review-sets").json()}
    assert {ISCH, NMDAR, "recheck-2026-11"} <= admin_sets


def test_code_assigned_to_a_missing_set_fails_loudly(client):
    assert _get(client, "TEST-BROKEN", "/review-sets").status_code == 500
