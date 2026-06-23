"""Aggregations over per-reviewer tool reviews (admin dashboard).

Scans every reviewer's tool-review file for a version and rolls up the
proposed tools and coverage annotations so the PI can act on them.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from ..schemas.reviewers import ReviewerCode
from .tool_review_store import ToolReviewStore


def tool_review_summary(
    store: ToolReviewStore,
    version: str,
    reviewers: list[ReviewerCode],
) -> dict[str, Any]:
    """Aggregate proposals + coverage annotations across all reviewers."""
    name_by_code = {r.code: r.name for r in reviewers}

    proposals: list[dict[str, Any]] = []
    # field_path -> aggregated annotation rollup
    coverage: dict[str, dict[str, Any]] = {}
    reviewer_status: list[dict[str, Any]] = []

    for reviewer in reviewers:
        review = store.load(version, reviewer.code)
        if review is None:
            reviewer_status.append(
                {
                    "reviewer_code": reviewer.code,
                    "reviewer_name": reviewer.name,
                    "completed": False,
                    "started": False,
                    "proposal_count": 0,
                    "annotation_count": 0,
                }
            )
            continue

        reviewer_status.append(
            {
                "reviewer_code": reviewer.code,
                "reviewer_name": reviewer.name,
                "completed": review.completed_at is not None,
                "started": True,
                "proposal_count": len(review.proposed_tools),
                "annotation_count": len(review.field_annotations),
            }
        )

        for proposal in review.proposed_tools:
            proposals.append(
                {
                    "id": proposal.id,
                    "reviewer_code": reviewer.code,
                    "reviewer_name": reviewer.name,
                    "name": proposal.name,
                    "description": proposal.description,
                    "rationale": proposal.rationale,
                    "target_conditions": proposal.target_conditions,
                    "modality": proposal.modality,
                    "created_at": proposal.created_at.isoformat(),
                }
            )

        for ann in review.field_annotations:
            bucket = coverage.setdefault(
                ann.field_path,
                {
                    "field_path": ann.field_path,
                    "total": 0,
                    "severity_counts": defaultdict(int),
                    "reviewers": set(),
                    "comments": [],
                },
            )
            bucket["total"] += 1
            bucket["severity_counts"][ann.severity] += 1
            bucket["reviewers"].add(reviewer.code)
            bucket["comments"].append(
                {
                    "reviewer_code": reviewer.code,
                    "reviewer_name": name_by_code.get(reviewer.code, reviewer.code),
                    "severity": ann.severity,
                    "comment": ann.comment,
                }
            )

    coverage_rows = sorted(
        (
            {
                "field_path": b["field_path"],
                "total": b["total"],
                "severity_counts": dict(b["severity_counts"]),
                "reviewers": sorted(b["reviewers"]),
                "comments": b["comments"],
            }
            for b in coverage.values()
        ),
        key=lambda r: (-r["total"], r["field_path"]),
    )

    return {
        "proposals": proposals,
        "coverage": coverage_rows,
        "reviewer_status": reviewer_status,
    }
