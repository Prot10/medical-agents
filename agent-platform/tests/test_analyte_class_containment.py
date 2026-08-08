"""Ordering the specific assay must satisfy a ground truth that names its class.

`AED_levels` is a family, not a synonym: `normalize_analyte` keeps it distinct from
`valproate_level`, and correctly. But the scoring consequence ran backwards. A ground truth asking for
`AED_levels` — as 13 status-epilepticus cases do — was satisfied only by an agent that echoed the vague
class term, while an agent that ordered the *specific, clinically correct* valproate level scored
nothing for it. In status epilepticus the drug level is the point of the lab order, and the case's own
report delivers it as "Valproate level".

The rule is one-directional on purpose: a class request is covered by any member, but a request for a
named assay is **not** covered by the class term. Vagueness must never be the cheaper way to score,
which was the clinical reviewers' objection to generic buckets to begin with.
"""

from __future__ import annotations

from neuroagent.evaluation.metrics import _optimal_action_satisfied
from neuroagent.tools.vocabulary import analyte_class_members, analyte_satisfied_by


def test_a_class_term_is_covered_by_a_member() -> None:
    assert analyte_satisfied_by("AED_levels", {"valproate_level"})
    assert analyte_satisfied_by("ABG", {"ph", "pco2"})
    assert analyte_satisfied_by("beta-hCG", {"pregnancy_test"})


def test_a_named_assay_is_not_covered_by_its_class() -> None:
    assert not analyte_satisfied_by("valproate level", {"aed_levels"})
    assert not analyte_satisfied_by("bicarbonate", {"abg"})


def test_an_unrelated_analyte_never_covers() -> None:
    assert not analyte_satisfied_by("AED_levels", {"cbc", "cmp"})


def test_the_scorer_credits_the_specific_order() -> None:
    assert _optimal_action_satisfied(
        "interpret_labs", {"panels": ["AED_levels"]},
        [("interpret_labs", {"panels": ["Valproate level"]})],
    )


def test_the_scorer_does_not_credit_the_vague_order() -> None:
    assert not _optimal_action_satisfied(
        "interpret_labs", {"panels": ["valproate_level"]},
        [("interpret_labs", {"panels": ["AED_levels"]})],
    )


def test_every_class_member_is_a_distinct_name() -> None:
    """A class must not list itself, or containment would be trivially reflexive."""
    for term in ("aed_levels", "abg", "beta_hcg", "tox_screen"):
        members = analyte_class_members(term)
        assert members, f"{term} should name a family"
        assert term not in members, f"{term} lists itself as a member"
