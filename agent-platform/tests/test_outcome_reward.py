"""The outcome reward sees the diagnosis and the bill, never the policy's process criteria (E1, P2-03)."""

from __future__ import annotations

import pytest

from neuroagent.evaluation.outcome_reward import OutcomeReward

from test_policy_reward import approved_case, by_importance, criterion_action, make_episode


def test_correct_answer_with_no_tests_scores_the_diagnosis_and_the_full_frugality_term():
    case = approved_case()
    assert OutcomeReward(budget_usd=1000.0).score(make_episode(case, []), case).scalar == pytest.approx(1.0)
    wrong = make_episode(case, [], diagnosis="Tension-type headache")
    assert OutcomeReward(budget_usd=1000.0).score(wrong, case).scalar == pytest.approx(0.15)


def test_cost_lowers_the_reward_linearly_up_to_the_budget():
    case = approved_case()
    actions = [criterion_action(c) for c in by_importance(case, "required")][:2]  # USD 100 each in the fixture
    episode = make_episode(case, actions)
    assert OutcomeReward(budget_usd=400.0).score(episode, case).scalar == pytest.approx(0.85 + 0.15 * 0.5)
    assert OutcomeReward(budget_usd=100.0).score(episode, case).scalar == pytest.approx(0.85)
    assert OutcomeReward(budget_usd=400.0, cost_weight=0.0).score(episode, case).scalar == pytest.approx(1.0)


def test_the_scalar_never_reads_the_process_criteria():
    case = approved_case()
    actions = [criterion_action(c) for c in by_importance(case, "required")]
    episode = make_episode(case, actions)
    scorer = OutcomeReward(budget_usd=5000.0)
    stripped = case.model_copy(update={"ground_truth": case.ground_truth.model_copy(update={
        "action_criteria": [], "avoided_actions": [], "sequence_constraints": [],
        "stop_rule": case.ground_truth.stop_rule.model_copy(update={"required_before_assessment": []}),
    })})
    full, bare = scorer.score(episode, case), scorer.score(episode, stripped)
    assert full.scalar == bare.scalar
    assert full.tool_accuracy == 1.0 and bare.tool_accuracy == 0.0  # the logged components do read them
    assert full.caps_applied == []


def test_budget_must_be_positive():
    with pytest.raises(ValueError):
        OutcomeReward(budget_usd=0.0)
