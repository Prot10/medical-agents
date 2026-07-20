"""The multi-turn rollout must survive TRL changing ``_generate_single_turn``'s return arity.

This exact contract broke on the TRL 0.29 -> 1.8 upgrade: 0.29 returned three values, 1.8
returns ``(completion_ids, logprobs)``. The adapter still unpacked three, so the FIRST
multi-turn optimiser step died with ``not enough values to unpack (expected 3, got 2)`` —
raised inside our generate callback, several frames below TRL's trainer, ~20 minutes into a
run after model load and dataset build. Nothing caught it earlier because the HF-generate
path is only reachable with a real trainer on a GPU.

So it is pinned here with a stub trainer instead: cheap, no CUDA, and it fails at the arity
itself rather than wherever the mis-bound value is eventually used. ``completion_ids`` first
is the one part of TRL's contract that has held across versions; the adapter binds that and
ignores the rest, so both arities must work.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

COMPLETIONS = [[11, 22, 33], [44, 55]]


class _GenConfig:
    max_new_tokens = 8192


class _StubTrainer:
    """Minimal stand-in for GRPOTrainer's HF-generate path."""

    use_vllm = False
    vllm_generation = None

    def __init__(self, n_return: int):
        self.n_return = n_return
        self.generation_config = _GenConfig()
        self.seen_max_new_tokens: int | None = None

    def _generate_single_turn(self, prompt_ids, images, multimodal_fields):
        # Record the cap in force during the call: the adapter must narrow the whole-completion
        # budget to a single turn, or one runaway sequence stalls the entire batch.
        self.seen_max_new_tokens = self.generation_config.max_new_tokens
        if self.n_return == 2:
            return COMPLETIONS, None  # TRL 1.8: logprobs is None on the HF path
        return COMPLETIONS, None, {}  # TRL 0.29 shape


def _adapter(per_turn: int = 384):
    from neuroagent.training.rollout.trl_rollout import MultiTurnRolloutFunc

    return MultiTurnRolloutFunc.__new__(MultiTurnRolloutFunc).__class__(
        rollout=object(),
        prompt_to_case={},
        cases={},
        patient_info={},
        reward_fn=lambda *_: 0.0,
        mock_server_factory=lambda _c: None,
        cost_tracker_factory=lambda: None,
        per_turn_max_tokens=per_turn,
    )


@pytest.mark.parametrize("n_return", [2, 3])
def test_completion_ids_bind_under_either_arity(n_return):
    """Whether TRL returns 2 or 3 values, completion_ids must come back intact."""
    trainer = _StubTrainer(n_return)
    fn = _adapter()._make_generate_batch_fn(trainer)
    assert fn([[1, 2], [3]]) == COMPLETIONS


def test_per_turn_cap_is_applied_then_restored():
    """The turn cap must be in force during generate and undone afterwards.

    Leaving it applied would silently shrink every later generation; never applying it lets a
    single non-terminating sequence hold up the whole group.
    """
    trainer = _StubTrainer(2)
    fn = _adapter(per_turn=384)._make_generate_batch_fn(trainer)
    fn([[1, 2]])
    assert trainer.seen_max_new_tokens == 384
    assert trainer.generation_config.max_new_tokens == 8192


def test_cap_restored_even_when_generation_raises():
    """A failed turn must not leave the trainer's budget clamped to one turn."""
    trainer = _StubTrainer(2)

    def boom(*_a, **_k):
        raise RuntimeError("CUDA OOM during generate")

    trainer._generate_single_turn = boom
    fn = _adapter(per_turn=384)._make_generate_batch_fn(trainer)
    with pytest.raises(RuntimeError):
        fn([[1, 2]])
    assert trainer.generation_config.max_new_tokens == 8192


def test_matches_installed_trl_arity():
    """Cross-check the stub against the TRL actually installed.

    The stub only proves the adapter tolerates both shapes. This proves which shape is real,
    so the assumption is measured rather than assumed.
    """
    import inspect

    from trl import GRPOTrainer

    src = inspect.getsource(GRPOTrainer._generate_single_turn)
    finals = [ln.strip() for ln in src.splitlines() if ln.strip().startswith("return ")]
    assert finals, "TRL's _generate_single_turn has no return statement"
    n = len(finals[-1].removeprefix("return ").split(","))
    assert n in (2, 3), f"unexpected TRL arity {n}: {finals[-1]}"
