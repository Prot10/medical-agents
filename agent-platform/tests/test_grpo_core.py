import pytest

from neuroagent.training.grpo import group_relative_advantages


def test_group_relative_advantages_are_centered():
    advantages = group_relative_advantages([0.1, 0.3, 0.6, 0.8])
    assert sum(advantages) == pytest.approx(0, abs=1e-9)


def test_grpo_rejects_single_sample_groups():
    with pytest.raises(ValueError):
        group_relative_advantages([0.5])
