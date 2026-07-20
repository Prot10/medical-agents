"""The single-turn GRPO reward must (a) have every weighted component live, (b) hard-gate
safety, and (c) never reward under-ordering. These are the fixes for the first GRPO run, where
half the reward weight was constant-zero and the reward barely moved.
"""

from __future__ import annotations

from neuroagent.training.rewards.clinical_reward import ClinicalScores
from neuroagent.training.rewards.composite_reward import CompositeReward, RewardWeights


def _reward(**kwargs) -> CompositeReward:
    return CompositeReward(
        weights=RewardWeights(
            correctness=0.0, actions=0.45, safety=0.30, cost=0.10, compliance=0.15, format=0.0
        ),
        tool_costs_path="agent-platform/config/tools/costs.yaml",
        rules_dir="agent-platform/config/hospital_rules",
        hospital="de_charite",
        **kwargs,
    )


def test_grpo_reward_config_loads_with_gates():
    r = CompositeReward.from_config(
        reward_config_path="agent-platform/config/training/reward_weights_grpo.yaml",
        tool_costs_path="agent-platform/config/tools/costs.yaml",
        rules_dir="agent-platform/config/hospital_rules",
        hospital="de_charite",
    )
    # correctness and format are zero-weighted (unreachable in one shot); the schedule is off.
    assert r.static_weights.correctness == 0.0
    assert r.static_weights.format == 0.0
    assert r.static_weights.actions > 0 and r.static_weights.safety > 0
    assert r.dynamic_schedule is None
    assert r.safety_gate is True
    assert r.cost_requires_workup == 0.5


def test_safety_gate_caps_a_contraindicated_trajectory():
    """A harmful action hard-caps the composite; without the gate the weighted sum is positive."""
    gated = _reward(safety_gate=True, safety_gate_cap=0.0)
    ungated = _reward(safety_gate=False)

    # A trajectory that scores well on every axis EXCEPT it took a contraindicated action.
    clinical = ClinicalScores(
        correctness=1.0, actions=0.9, safety=-1.0,  # safety already negative from the offset
        action_recall=0.9, critical_actions_hit=1.0, contraindicated_actions_taken=1,
    )
    # Drive the gate directly through the documented public path: monkey-patch the clinical
    # scorer so we exercise the composite's gate, not MetricsCalculator.
    for r in (gated, ungated):
        r.clinical.compute = lambda trace, gt, _c=clinical: _c  # type: ignore

    import types

    fake_trace = types.SimpleNamespace(tools_called=["analyze_brain_mri"], final_response="x")
    fake_case = types.SimpleNamespace(
        ground_truth=types.SimpleNamespace(optimal_actions=[]),
        condition=types.SimpleNamespace(value="als"),
    )
    g = gated.compute(fake_trace, fake_case)
    u = ungated.compute(fake_trace, fake_case)
    assert g <= 0.0, f"gate should cap unsafe trajectory at <=0, got {g}"
    assert u > g, "the ungated reward should be higher — proving the gate actually bites"


def test_cost_credit_withheld_until_workup_ordered():
    """With cost_requires_workup, an incomplete workup earns no cost bonus even if it is cheap."""
    r = _reward(cost_requires_workup=0.5)

    import types
    fake_trace = types.SimpleNamespace(tools_called=[], final_response="x")
    fake_case = types.SimpleNamespace(
        ground_truth=types.SimpleNamespace(optimal_actions=[]),
        condition=types.SimpleNamespace(value="als"),
    )
    # critical_actions_hit below threshold -> cost component must be zeroed.
    low = ClinicalScores(correctness=0.0, actions=0.0, safety=0.5,
                         action_recall=0.0, critical_actions_hit=0.0, contraindicated_actions_taken=0)
    r.clinical.compute = lambda trace, gt, _c=low: _c  # type: ignore
    bd = r.compute_with_breakdown(fake_trace, fake_case)
    assert bd.cost == 0.0, "cost must be withheld when the required workup was not ordered"
