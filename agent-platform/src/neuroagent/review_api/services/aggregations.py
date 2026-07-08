"""Aggregations over per-reviewer annotations.

These power the admin dashboard. They scan the filesystem each call —
acceptable for ≤20 reviewers × ≤600 cases (a few thousand small reads
under a second). If it ever feels slow, wrap with a memoization cache
invalidated on every write that goes through ``AnnotationStore``.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from neuroagent_schemas import NeuroBenchCase

from ..schemas.annotations import CaseReview, ReviewStatus
from ..schemas.reviewers import ReviewerCode
from .annotation_store import AnnotationStore

_STATUS_VALUES: tuple[ReviewStatus, ...] = (
    "pending",
    "in_progress",
    "needs_changes",
    "approved",
)


def _empty_status_counts() -> dict[ReviewStatus, int]:
    return {s: 0 for s in _STATUS_VALUES}


# Statuses that represent a settled verdict (agreement is only meaningful here;
# pending/in_progress mean "not yet judged").
_TERMINAL_STATUSES: tuple[ReviewStatus, ...] = ("approved", "needs_changes")


def _cohen_kappa(pairs: list[tuple[str, str]]) -> float | None:
    """Cohen's kappa for a list of (rater_a_label, rater_b_label) verdicts.

    Returns None when there is no overlap to score. When chance agreement is
    total (both raters only ever used one identical category), returns 1.0 if
    they always matched, else 0.0 — avoiding a divide-by-zero.
    """
    n = len(pairs)
    if n == 0:
        return None
    labels = {lbl for pair in pairs for lbl in pair}
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for label in labels:
        pa = sum(1 for a, _ in pairs if a == label) / n
        pb = sum(1 for _, b in pairs if b == label) / n
        pe += pa * pb
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else 0.0
    return (po - pe) / (1.0 - pe)


def _kappa_interpretation(kappa: float) -> str:
    """Landis & Koch (1977) strength-of-agreement bands."""
    if kappa < 0:
        return "poor"
    if kappa < 0.20:
        return "slight"
    if kappa < 0.40:
        return "fair"
    if kappa < 0.60:
        return "moderate"
    if kappa < 0.80:
        return "substantial"
    return "almost perfect"


def _pairwise_kappa(
    per_case_statuses: dict[str, dict[str, ReviewStatus]],
    reviewer_codes: list[str],
) -> dict[str, Any]:
    """Mean pairwise Cohen's kappa over settled verdicts (approved vs needs_changes).

    Robust to reviewers having rated different subsets of cases: for each pair we
    score only the cases both reviewers settled. The overall figure is the mean
    of the per-pair kappas — interpretable with variable participation, unlike a
    single Fleiss' kappa that assumes a fixed rater count per case.
    """
    pair_rows: list[dict[str, Any]] = []
    for i, a in enumerate(reviewer_codes):
        for b in reviewer_codes[i + 1 :]:
            verdicts: list[tuple[str, str]] = []
            for statuses in per_case_statuses.values():
                sa, sb = statuses.get(a), statuses.get(b)
                if sa in _TERMINAL_STATUSES and sb in _TERMINAL_STATUSES:
                    verdicts.append((sa, sb))
            kappa = _cohen_kappa(verdicts)
            if kappa is None:
                continue
            pair_rows.append(
                {
                    "a": a,
                    "b": b,
                    "kappa": round(kappa, 3),
                    "n": len(verdicts),
                }
            )

    if not pair_rows:
        return {
            "overall": None,
            "interpretation": None,
            "method": "cohen_pairwise_mean",
            "pairs": [],
            "note": "Not enough settled (approved/needs_changes) overlap to score agreement yet.",
        }

    overall = sum(p["kappa"] for p in pair_rows) / len(pair_rows)
    return {
        "overall": round(overall, 3),
        "interpretation": _kappa_interpretation(overall),
        "method": "cohen_pairwise_mean",
        "pairs": sorted(pair_rows, key=lambda p: (-p["n"], p["a"], p["b"])),
        "note": None,
    }


def reviewer_progress_summary(
    store: AnnotationStore,
    version: str,
    reviewer_code: str,
    case_objects: dict[str, NeuroBenchCase],
) -> dict[str, Any]:
    """Per-reviewer progress: totals + by-status + by-condition rollup."""
    summaries = store.list_for_reviewer(version, reviewer_code)
    by_status = _empty_status_counts()
    case_status: dict[str, ReviewStatus] = {}
    for summary in summaries:
        by_status[summary.status] = by_status.get(summary.status, 0) + 1
        case_status[summary.case_id] = summary.status

    total = len(case_objects)
    touched = len(summaries)
    by_status["pending"] = total - touched + by_status.get("pending", 0)

    total_time_spent_seconds = sum(s.time_spent_seconds for s in summaries)
    avg_time_spent_seconds = (
        total_time_spent_seconds / touched if touched else 0.0
    )

    # Roll up by condition.
    by_condition: dict[str, dict[ReviewStatus, int]] = defaultdict(_empty_status_counts)
    for case_id, case in case_objects.items():
        condition = case.condition.value
        status_for_case = case_status.get(case_id, "pending")
        by_condition[condition][status_for_case] = (
            by_condition[condition].get(status_for_case, 0) + 1
        )

    return {
        "reviewer_code": reviewer_code,
        "dataset_version": version,
        "total_cases": total,
        "touched_cases": touched,
        "total_time_spent_seconds": total_time_spent_seconds,
        "avg_time_spent_seconds": round(avg_time_spent_seconds, 1),
        "by_status": by_status,
        "by_condition": {
            condition: dict(counts) for condition, counts in by_condition.items()
        },
    }


def all_reviewers_progress(
    store: AnnotationStore,
    version: str,
    reviewers: list[ReviewerCode],
    case_objects: dict[str, NeuroBenchCase],
) -> list[dict[str, Any]]:
    """Per-reviewer progress for the admin dashboard."""
    return [
        {
            "code": reviewer.code,
            "name": reviewer.name,
            "role": reviewer.role,
            **reviewer_progress_summary(store, version, reviewer.code, case_objects),
        }
        for reviewer in reviewers
        if reviewer.role == "reviewer"
    ]


def inter_rater_agreement(
    store: AnnotationStore,
    version: str,
    reviewers: list[ReviewerCode],
    case_objects: dict[str, NeuroBenchCase],
) -> dict[str, Any]:
    """Per-case status for every reviewer, plus unanimous/disagreement flags."""
    reviewer_codes = [r.code for r in reviewers if r.role == "reviewer"]

    per_case_statuses: dict[str, dict[str, ReviewStatus]] = {
        case_id: {} for case_id in case_objects
    }
    for reviewer_code in reviewer_codes:
        for summary in store.list_for_reviewer(version, reviewer_code):
            if summary.case_id in per_case_statuses:
                per_case_statuses[summary.case_id][reviewer_code] = summary.status

    rows: list[dict[str, Any]] = []
    consensus_counts: Counter[str] = Counter()
    for case_id, case in case_objects.items():
        statuses = per_case_statuses[case_id]
        # Fill in pending for reviewers who haven't touched it.
        filled: dict[str, ReviewStatus] = {
            code: statuses.get(code, "pending") for code in reviewer_codes
        }
        # "Unanimous" only when every reviewer has reached a terminal status
        # (approved / needs_changes) AND agrees. Mixed terminal+pending is
        # "in_review" — disagreement can't be measured before everyone weighs in.
        terminal = {"approved", "needs_changes"}
        statuses_set = set(filled.values())
        if statuses_set <= terminal:
            consensus = "unanimous" if len(statuses_set) == 1 else "disagree"
        else:
            consensus = "in_review"
        consensus_counts[consensus] += 1

        rows.append(
            {
                "case_id": case_id,
                "condition": case.condition.value,
                "difficulty": case.difficulty.value,
                "statuses": filled,
                "consensus": consensus,
            }
        )

    return {
        "reviewer_codes": reviewer_codes,
        "rows": rows,
        "consensus_summary": dict(consensus_counts),
        "kappa": _pairwise_kappa(per_case_statuses, reviewer_codes),
    }


def field_hotspots(
    store: AnnotationStore,
    version: str,
    reviewer_codes: list[str],
    case_objects: dict[str, NeuroBenchCase],
) -> list[dict[str, Any]]:
    """Aggregate annotations across all reviewers, grouped by field_path.

    For each field path we report:
        - total annotations across reviewers
        - severity breakdown
        - list of reviewers that touched it
        - most recent comment snippet
        - examples of cases that have at least one annotation on this field
    """
    per_field: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "field_path": "",
            "total": 0,
            "by_severity": {"note": 0, "issue": 0, "error": 0},
            "reviewers": set(),
            "case_ids": set(),
            "latest_comment": None,
            "latest_at": None,
        }
    )

    for reviewer_code in reviewer_codes:
        for summary in store.list_for_reviewer(version, reviewer_code):
            review = store.load(version, reviewer_code, summary.case_id)
            if review is None:
                continue
            for annotation in review.field_annotations:
                bucket = per_field[annotation.field_path]
                bucket["field_path"] = annotation.field_path
                bucket["total"] += 1
                bucket["by_severity"][annotation.severity] = (
                    bucket["by_severity"].get(annotation.severity, 0) + 1
                )
                bucket["reviewers"].add(reviewer_code)
                bucket["case_ids"].add(review.case_id)
                if (
                    bucket["latest_at"] is None
                    or annotation.updated_at > bucket["latest_at"]
                ):
                    bucket["latest_at"] = annotation.updated_at
                    bucket["latest_comment"] = annotation.comment[:200]

    out: list[dict[str, Any]] = []
    for entry in per_field.values():
        out.append(
            {
                "field_path": entry["field_path"],
                "total": entry["total"],
                "by_severity": entry["by_severity"],
                "reviewer_codes": sorted(entry["reviewers"]),
                "case_ids": sorted(entry["case_ids"]),
                "latest_comment": entry["latest_comment"],
                "latest_at": entry["latest_at"].isoformat() if entry["latest_at"] else None,
            }
        )
    out.sort(key=lambda row: (-len(row["reviewer_codes"]), -row["total"]))
    return out


def case_diff(
    store: AnnotationStore,
    version: str,
    case_id: str,
    reviewers: list[ReviewerCode],
) -> dict[str, Any]:
    """All reviewers' reviews for one case, organised for the side-by-side diff."""
    reviewer_entries: list[dict[str, Any]] = []
    field_rows: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"field_path": "", "by_reviewer": {}}
    )

    for reviewer in reviewers:
        if reviewer.role != "reviewer":
            continue
        review: CaseReview | None = store.load(version, reviewer.code, case_id)
        reviewer_entries.append(
            {
                "code": reviewer.code,
                "name": reviewer.name,
                "status": review.status if review else "pending",
                "annotation_count": len(review.field_annotations) if review else 0,
                "comment_count": len(review.case_comments) if review else 0,
                "case_comments": [
                    c.model_dump(mode="json") for c in (review.case_comments if review else [])
                ],
            }
        )
        if review is None:
            continue
        for annotation in review.field_annotations:
            entry = field_rows[annotation.field_path]
            entry["field_path"] = annotation.field_path
            entry["by_reviewer"][reviewer.code] = annotation.model_dump(mode="json")

    statuses = {entry["code"]: entry["status"] for entry in reviewer_entries}
    unique = set(statuses.values())
    if len(unique) <= 1:
        consensus = "unanimous"
    elif {"approved", "needs_changes"} <= unique:
        consensus = "disagree"
    else:
        consensus = "partial"

    return {
        "case_id": case_id,
        "dataset_version": version,
        "reviewers": reviewer_entries,
        "field_rows": sorted(field_rows.values(), key=lambda r: r["field_path"]),
        "consensus": consensus,
    }
