"""Multi-turn ("grouped") GRPO rollout: drive the real ReAct loop against the training
policy, so the reward is computed on a genuine multi-turn trajectory (tool responses and
all) rather than a single-shot completion. See ``react_rollout.ReactRollout``.
"""

from __future__ import annotations

from .react_rollout import ReactRollout, RolloutResult

__all__ = ["ReactRollout", "RolloutResult"]
