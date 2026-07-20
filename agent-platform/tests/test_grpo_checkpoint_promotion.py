"""The run must ship the best-held-out-reward checkpoint, not its last step.

Downstream (serving, eval) reads `<output>/adapter_model.safetensors`. For RL the last step is
routinely past the point where held-out reward peaked, so promoting the wrong checkpoint does
not fail — it quietly reports a worse model. Nothing in the logs looks wrong.

This whole path had no test. It is also the last thing a 20+ hour run does, so a bug here costs
the entire run: `_make_best_reward_callback` has to recognise TRL's metric key, and
`_promote_best_checkpoint` has to find and copy the right directory.

The callback half matters because TRL renames things: it logs eval metrics by prefixing "eval_"
onto its internal keys, so the reward arrives as `eval_reward`. When that key drifted before,
`metric_for_best_model` raised KeyError — here it would instead silently never fire, leaving
best_step None and shipping the last step.
"""

from __future__ import annotations

import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")


def _ckpt(root, step: int, payload: str):
    d = root / f"checkpoint-{step}"
    d.mkdir()
    (d / "adapter_model.safetensors").write_text(payload)
    (d / "adapter_config.json").write_text(f'{{"step": {step}}}')
    return d


def test_promotes_the_best_step_not_the_last(tmp_path):
    from neuroagent.training.train_grpo import _promote_best_checkpoint

    _ckpt(tmp_path, 3, "BEST")
    _ckpt(tmp_path, 6, "LAST")
    # The root starts out holding the last step, as trainer.save_model leaves it.
    (tmp_path / "adapter_model.safetensors").write_text("LAST")

    _promote_best_checkpoint(str(tmp_path), best_step=3)

    assert (tmp_path / "adapter_model.safetensors").read_text() == "BEST"
    assert (tmp_path / "adapter_config.json").read_text() == '{"step": 3}'


def test_missing_checkpoint_leaves_the_last_step_intact(tmp_path):
    """Degrade to the last step rather than corrupting the root.

    Reachable when save_steps and eval_steps fall out of alignment, or rotation deletes the
    best checkpoint before the run ends.
    """
    from neuroagent.training.train_grpo import _promote_best_checkpoint

    (tmp_path / "adapter_model.safetensors").write_text("LAST")
    _promote_best_checkpoint(str(tmp_path), best_step=99)
    assert (tmp_path / "adapter_model.safetensors").read_text() == "LAST"


def test_no_eval_leaves_the_last_step_intact(tmp_path):
    """best_step is None when no held-out eval ever ran."""
    from neuroagent.training.train_grpo import _promote_best_checkpoint

    (tmp_path / "adapter_model.safetensors").write_text("LAST")
    _promote_best_checkpoint(str(tmp_path), best_step=None)
    assert (tmp_path / "adapter_model.safetensors").read_text() == "LAST"


def test_callback_tracks_the_highest_reward_not_the_latest():
    """Reward is noisy and non-monotonic in RL; a later, worse eval must not win."""
    from neuroagent.training.train_grpo import _make_best_reward_callback

    cb = _make_best_reward_callback()

    class _State:
        global_step = 0

    st = _State()
    for step, reward in ((3, 0.045), (6, 0.031), (9, 0.052), (12, 0.040)):
        st.global_step = step
        cb.on_log(args=None, state=st, control=None, logs={"eval_reward": reward})

    assert cb.best_step == 9
    assert cb.best_reward == 0.052


def test_callback_ignores_training_logs():
    """Training logs carry `reward`; only the `eval_` prefixed one selects a checkpoint.

    Selecting on the training reward would pick a checkpoint by how well it fits the prompts it
    just trained on — the failure the held-out split exists to prevent.
    """
    from neuroagent.training.train_grpo import _make_best_reward_callback

    cb = _make_best_reward_callback()

    class _State:
        global_step = 5

    cb.on_log(args=None, state=_State(), control=None,
              logs={"reward": 0.9, "reward_std": 0.1, "loss": 0.0})
    assert cb.best_step is None
    assert cb.best_reward is None


def test_callback_key_matches_what_trl_actually_emits():
    """Pin the key to TRL's own construction, not to a remembered string.

    TRL builds eval metric names as f"eval_{key}" over the same keys it logs during training,
    where the reward is `reward`. If that ever changes, the callback silently stops firing and
    the run ships its last step.
    """
    import inspect

    from trl import GRPOTrainer

    src = inspect.getsource(GRPOTrainer.log)
    assert 'f"eval_{key}"' in src, (
        "TRL no longer builds eval metric keys as eval_<key>; the best-reward callback's "
        "'eval_reward' lookup needs rechecking"
    )
