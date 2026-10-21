from neuroagent.review_api.schemas.annotations import (
    CaseReview,
    FieldAnnotation,
    PolicyReviewVerdict,
)
from neuroagent.review_api.services.policy_eligibility import evaluate_policy_eligibility


def verdict(**updates):
    raw = {
        "scenario_plausibility": "approve",
        "diagnosis": "approve",
        "actions": "approve",
        "avoided_actions": "approve",
        "sequencing": "approve",
        "stopping": "approve",
        "assessment": "approve",
    }
    raw.update(updates)
    return PolicyReviewVerdict(**raw)


def review(code, status="approved", policy_verdict=None, annotations=None):
    return CaseReview(
        case_id="case",
        dataset_version="v2",
        reviewer_code=code,
        status=status,
        policy_verdict=policy_verdict or verdict(),
        field_annotations=annotations or [],
    )


def test_two_independent_approvals_are_eligible():
    result = evaluate_policy_eligibility([review("DOC-1"), review("DOC-2")])
    assert result.eligible
    assert result.independent_approvals == 2
    assert not result.requires_adjudication


def test_disagreement_requires_third_reviewer():
    result = evaluate_policy_eligibility(
        [
            review("DOC-1"),
            review(
                "DOC-2",
                status="needs_changes",
                policy_verdict=verdict(avoided_actions="needs_revision"),
            ),
        ]
    )
    assert not result.eligible
    assert result.requires_adjudication
    assert result.required_reviewers == 3


def test_unresolved_error_blocks_eligibility():
    annotation = FieldAnnotation(
        id="a",
        field_path="ground_truth.actions",
        comment="Unsafe criterion",
        severity="error",
    )
    result = evaluate_policy_eligibility(
        [review("DOC-1", annotations=[annotation]), review("DOC-2")]
    )
    assert not result.eligible
    assert result.unresolved_errors == 1


def test_duplicate_reviewer_is_not_independent():
    try:
        evaluate_policy_eligibility([review("DOC-1"), review("DOC-1")])
    except ValueError as exc:
        assert "independent" in str(exc)
    else:
        raise AssertionError("duplicate reviewer accepted")
