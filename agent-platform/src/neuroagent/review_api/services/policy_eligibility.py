"""Consensus gate for benchmark and fine-tuning eligibility."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ..schemas.annotations import CaseReview


class PolicyEligibility(BaseModel):
    model_config = ConfigDict(extra="forbid")
    eligible: bool
    independent_approvals: int = Field(ge=0)
    terminal_reviews: int = Field(ge=0)
    unresolved_errors: int = Field(ge=0)
    requires_adjudication: bool
    required_reviewers: int = Field(ge=2, le=3)
    reasons: list[str]


def evaluate_policy_eligibility(reviews: list[CaseReview]) -> PolicyEligibility:
    reviewer_codes = [review.reviewer_code for review in reviews]
    if len(reviewer_codes) != len(set(reviewer_codes)):
        raise ValueError("reviews must come from independent reviewer codes")

    terminal = [
        review for review in reviews if review.status in {"approved", "needs_changes"}
    ]
    approvals = [
        review
        for review in terminal
        if review.status == "approved"
        and review.policy_verdict is not None
        and review.policy_verdict.approves_all
    ]
    unresolved_errors = sum(review.unresolved_errors for review in reviews)
    has_revision = any(
        review.status == "needs_changes"
        or (
            review.policy_verdict is not None
            and not review.policy_verdict.approves_all
        )
        for review in terminal
    )
    disagreement = bool(approvals and has_revision)
    eligible = len(approvals) >= 2 and unresolved_errors == 0 and not disagreement
    reasons = []
    if len(approvals) < 2:
        reasons.append("two independent all-dimension approvals are required")
    if unresolved_errors:
        reasons.append("all error annotations must be resolved")
    if disagreement:
        reasons.append("conflicting terminal verdicts require a third clinician")
    return PolicyEligibility(
        eligible=eligible,
        independent_approvals=len(approvals),
        terminal_reviews=len(terminal),
        unresolved_errors=unresolved_errors,
        requires_adjudication=disagreement,
        required_reviewers=3 if disagreement else 2,
        reasons=reasons,
    )
