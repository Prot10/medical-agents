"""The run manifest tells a case change from a policy change and records the scorer (P0-04)."""

from __future__ import annotations

from neuroagent.evaluation.manifest import case_hashes, run_manifest
from neuroagent.evaluation.outcome_reward import OutcomeReward
from neuroagent.evaluation.policy_reward import ClinicalPolicyReward

from test_policy_reward import approved_case


def test_case_and_policy_hashes_move_independently():
    case = approved_case()
    reviewed = case.model_copy(update={"ground_truth": case.ground_truth.model_copy(update={"sequence_constraints": []})})
    edited = case.model_copy(update={"patient": case.patient.model_copy(update={"chief_complaint": "something else"})})
    base, after_review, after_edit = case_hashes(case), case_hashes(reviewed), case_hashes(edited)
    assert after_review["case"] == base["case"] and after_review["policy"] != base["policy"]
    assert after_edit["case"] != base["case"] and after_edit["policy"] == base["policy"]


def test_manifest_is_deterministic_and_order_free():
    case = approved_case()
    other = case.model_copy(update={"case_id": "OTHER-M01"})
    scorer = ClinicalPolicyReward(require_approved=False)
    first, second = run_manifest([case, other], scorer), run_manifest([other, case], scorer)
    assert first["cases"] == second["cases"]
    assert first["scorer"] == second["scorer"]
    assert first["cases"]["n"] == 2


def test_manifest_records_the_scorer_and_its_configuration():
    case = approved_case()
    policy = run_manifest([case], ClinicalPolicyReward(require_approved=False))["scorer"]
    outcome = run_manifest([case], OutcomeReward(budget_usd=6992.0, require_approved=False))["scorer"]
    assert policy["id"] == "clinical-policy-v2" and policy["config"] == {"require_approved": False}
    assert outcome["id"] == "outcome-v1"
    assert outcome["config"] == {"budget_usd": 6992.0, "cost_weight": 0.15}
    assert set(policy["source_sha256"]) == set(outcome["source_sha256"])
