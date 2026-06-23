"""Tests for the inter-rater kappa helpers in review_api aggregations."""

from __future__ import annotations

from neuroagent.review_api.services.aggregations import (
    _cohen_kappa,
    _kappa_interpretation,
    _pairwise_kappa,
)


class TestCohenKappa:
    def test_no_overlap_returns_none(self):
        assert _cohen_kappa([]) is None

    def test_perfect_agreement(self):
        pairs = [("approved", "approved"), ("needs_changes", "needs_changes")]
        assert _cohen_kappa(pairs) == 1.0

    def test_total_disagreement_is_negative(self):
        pairs = [("approved", "needs_changes"), ("needs_changes", "approved")]
        # po=0, pe=0.5 -> (0-0.5)/(0.5) = -1.0
        assert _cohen_kappa(pairs) == -1.0

    def test_single_category_no_divide_by_zero(self):
        # Both raters only ever said "approved": chance agreement is total.
        pairs = [("approved", "approved")] * 5
        assert _cohen_kappa(pairs) == 1.0

    def test_chance_level_is_zero(self):
        # 2x2 balanced with agreement equal to chance -> kappa ~ 0.
        pairs = [
            ("approved", "approved"),
            ("approved", "needs_changes"),
            ("needs_changes", "approved"),
            ("needs_changes", "needs_changes"),
        ]
        assert abs(_cohen_kappa(pairs)) < 1e-9


class TestInterpretation:
    def test_bands(self):
        assert _kappa_interpretation(-0.1) == "poor"
        assert _kappa_interpretation(0.1) == "slight"
        assert _kappa_interpretation(0.3) == "fair"
        assert _kappa_interpretation(0.5) == "moderate"
        assert _kappa_interpretation(0.7) == "substantial"
        assert _kappa_interpretation(0.9) == "almost perfect"


class TestPairwiseKappa:
    def test_excludes_non_terminal_and_scores_overlap(self):
        # Three reviewers; only terminal (approved/needs_changes) verdicts count.
        per_case = {
            "C1": {"R-A": "approved", "R-B": "approved", "R-C": "pending"},
            "C2": {"R-A": "needs_changes", "R-B": "needs_changes"},
            "C3": {"R-A": "approved", "R-B": "in_progress"},  # B not terminal
        }
        result = _pairwise_kappa(per_case, ["R-A", "R-B", "R-C"])
        # Only the A-B pair has terminal overlap (C1, C2) -> perfect agreement.
        assert result["overall"] == 1.0
        assert result["interpretation"] == "almost perfect"
        ab = [p for p in result["pairs"] if {p["a"], p["b"]} == {"R-A", "R-B"}]
        assert ab and ab[0]["n"] == 2

    def test_no_overlap_returns_note(self):
        per_case = {"C1": {"R-A": "pending", "R-B": "in_progress"}}
        result = _pairwise_kappa(per_case, ["R-A", "R-B"])
        assert result["overall"] is None
        assert result["note"]
        assert result["pairs"] == []
