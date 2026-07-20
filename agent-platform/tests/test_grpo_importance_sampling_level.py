"""`importance_sampling_level='sequence'` is inert on-policy — and TRL's warning about it is a trap.

Every multi-turn run logs:

    When using `importance_sampling_level='sequence'`, the `'dapo'` loss sums per-token
    contributions, which effectively weights each sequence by its completion length instead
    of optimizing the per-sequence objective. To reproduce the GSPO paper's setup, set
    `loss_type='grpo'`.

Taking that advice would be a mistake here. TRL's own docs call `loss_type='grpo'` "not
recommended due to length bias", and our multi-turn completions vary several-fold in length
(one tool call versus four), which is exactly when that bias bites. `'dapo'` normalises by
active tokens in the global accumulated batch specifically to remove it.

The warning is also inapplicable. TRL sets `old_per_token_logps = None` whenever generation is
aligned with the optimiser step and vLLM is off, and `_compute_loss` then substitutes
`per_token_logps.detach()`, so `log_ratio` is identically zero. Both levels collapse to a
weight of exactly 1 — and, less obviously, to the same GRADIENT: the sequence branch averages
log-ratios over T tokens, but `'dapo'` then sums T identical per-token terms, and the 1/T and
the T cancel.

That cancellation is the whole argument, so it is measured here rather than asserted.

Live again the moment vLLM rollouts are enabled: TRL always computes `old_per_token_logps`
when `vllm_importance_sampling_correction` is on, `log_ratio` stops being zero, and the warning
becomes a real design question. This test is the tripwire for that.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

torch = pytest.importorskip("torch")

# Deliberately ragged: an 8x spread, comparable to a one-tool-call versus four-tool-call
# trajectory. Equal lengths would make the two levels agree trivially and prove nothing.
LENGTHS = [8, 32, 64]
EPS_LOW, EPS_HIGH = 0.2, 0.28  # as configured in run_grpo_trl


def _loss_and_grad(level: str, on_policy: bool = True):
    """Reproduce TRL's _compute_loss ratio math for one importance-sampling level."""
    torch.manual_seed(0)
    B, T = len(LENGTHS), max(LENGTHS)
    logps = torch.randn(B, T, dtype=torch.float64, requires_grad=True)
    mask = torch.zeros(B, T, dtype=torch.float64)
    for i, length in enumerate(LENGTHS):
        mask[i, :length] = 1.0
    advantages = torch.tensor([[1.0], [-0.5], [0.25]], dtype=torch.float64)

    if on_policy:
        # TRL: old_per_token_logps is None -> per_token_logps.detach()
        old = logps.detach()
    else:
        # Stand-in for the vLLM path, where the sampling distribution genuinely differs.
        torch.manual_seed(1)
        old = logps.detach() + 0.05 * torch.randn(B, T, dtype=torch.float64)

    log_ratio = logps - old
    if level == "token":
        log_iw = log_ratio
    else:
        log_iw = ((log_ratio * mask).sum(-1) / mask.sum(-1).clamp(min=1.0)).unsqueeze(-1)

    coef_1 = torch.exp(log_iw)
    coef_2 = torch.clamp(coef_1, 1 - EPS_LOW, 1 + EPS_HIGH)
    per_token_loss = -torch.min(coef_1 * advantages, coef_2 * advantages)
    # loss_type="dapo": normalise by active tokens in the global accumulated batch.
    loss = (per_token_loss * mask).sum() / mask.sum().clamp(min=1.0)
    loss.backward()
    return loss.detach(), logps.grad.clone(), coef_1.detach()


def test_both_levels_have_unit_weight_on_policy():
    """log_ratio is identically zero, so the importance weight is exactly 1 either way."""
    for level in ("token", "sequence"):
        _loss, _grad, coef = _loss_and_grad(level)
        assert torch.allclose(coef, torch.ones_like(coef)), f"{level}: weight != 1"


def test_sequence_and_token_gradients_are_identical_on_policy():
    """The real claim: the 1/T averaging and dapo's per-token sum cancel exactly.

    Bitwise equality, on ragged lengths, is what makes TRL's length-weighting warning
    inapplicable to this configuration.
    """
    loss_t, grad_t, _ = _loss_and_grad("token")
    loss_s, grad_s, _ = _loss_and_grad("sequence")
    assert torch.equal(loss_t, loss_s), (loss_t.item(), loss_s.item())
    assert torch.equal(grad_t, grad_s), f"max diff {(grad_t - grad_s).abs().max().item():.3e}"


def test_the_levels_do_diverge_once_off_policy():
    """Guards against the equality above being vacuous.

    If this ever fails, the on-policy test proves nothing — it would mean the two branches
    agree for some unrelated reason rather than because log_ratio is zero. It also marks the
    regime that vLLM rollouts would put us in, where the warning becomes a real question.
    """
    _loss_t, grad_t, coef_t = _loss_and_grad("token", on_policy=False)
    _loss_s, grad_s, coef_s = _loss_and_grad("sequence", on_policy=False)
    assert not torch.allclose(coef_t, coef_s), "off-policy weights should differ by level"
    assert not torch.equal(grad_t, grad_s), "off-policy gradients should differ by level"


def test_configured_loss_type_is_length_unbiased():
    """Whatever we ship must not be the length-biased aggregation."""
    import inspect

    from neuroagent.training import train_grpo

    sig = inspect.signature(train_grpo.run_grpo_trl)
    loss_type = sig.parameters["loss_type"].default
    # "grpo" normalises over sequence length and is length-biased; the others do not.
    assert loss_type in ("dapo", "dr_grpo", "bnpo"), (
        f"loss_type={loss_type!r} reintroduces the length bias dapo/dr_grpo exist to remove"
    )
