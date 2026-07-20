"""The chunked-logprob override must track TRL's evolving interface.

Not CUDA-gated: this is pure introspection, and it is precisely the check that must run in
every environment. Both halves of the contract have already broken on a TRL upgrade — 1.8
ADDED parameters (num_tiles, compute_aux_loss, image_position_ids, spatial_shapes) and returns
THREE values where 0.29 returned two. Neither failure surfaces where the mistake is: the arity
error is raised inside TRL's caller, several frames away, part-way through a training run.
"""

from __future__ import annotations

import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")


def test_override_matches_trl_signature_and_arity():
    """The override must stay compatible with TRL's evolving interface.

    Both halves of the contract have broken in practice on a TRL upgrade: 1.8 ADDED
    parameters (num_tiles, compute_aux_loss, image_position_ids, spatial_shapes), and it
    returns THREE values where 0.29 returned two. Neither fails where the mistake is — the
    arity error surfaces in TRL's caller, several frames away, mid-run.
    """
    import inspect

    from trl import GRPOTrainer

    from neuroagent.training.chunked_grpo_trainer import ChunkedLogpsGRPOTrainer

    ours = inspect.signature(ChunkedLogpsGRPOTrainer._get_per_token_logps_and_entropies)
    trl = inspect.signature(GRPOTrainer._get_per_token_logps_and_entropies)

    # Every TRL parameter must be accepted, by name or absorbed by **kwargs.
    accepts_var_kw = any(p.kind is p.VAR_KEYWORD for p in ours.parameters.values())
    missing = set(trl.parameters) - set(ours.parameters)
    assert accepts_var_kw or not missing, f"override would reject TRL params: {sorted(missing)}"

    # Return arity must match what TRL's callers unpack.
    src = inspect.getsource(ChunkedLogpsGRPOTrainer._chunked_logps)
    returned = [ln for ln in src.splitlines() if ln.strip().startswith("return ")]
    assert returned, "no return found in _chunked_logps"
    n_ours = len(returned[-1].split("return ", 1)[1].split(","))
    ann = str(trl.return_annotation)
    n_trl = ann.count(",") + 1 if ann.startswith("tuple[") else n_ours
    assert n_ours == n_trl, f"override returns {n_ours} values, TRL expects {n_trl} ({ann})"
