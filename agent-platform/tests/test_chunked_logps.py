"""Regression tests for the chunked (Unsloth-kernel) logprob path.

The chunked path replaces TRL's full-logits computation in GRPO. A silent numerical
discrepancy here would corrupt the policy gradient WITHOUT crashing, so it is pinned:
against an fp32 reference the chunked logprobs and entropies must match essentially
exactly, at materially lower peak memory.

GPU-only (the kernel is a CUDA matmul path); skipped on CPU-only machines.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

torch = pytest.importorskip("torch")

pytestmark = pytest.mark.skipif(
    not torch.cuda.is_available(), reason="chunked logprob kernel requires CUDA"
)


@pytest.fixture(scope="module")
def kernel():
    from neuroagent.training.chunked_logps import load_unsloth_chunked_kernel

    k = load_unsloth_chunked_kernel()
    if k is None:
        pytest.skip("unsloth-zoo not installed")
    return k


def _fp32_reference(hidden, lm_head_weight, index, temperature=1.0):
    """Ground truth: full logits in fp32, then gather - logsumexp."""
    logits = (hidden.to(lm_head_weight.dtype) @ lm_head_weight.t()).to(torch.float32)
    if temperature != 1.0:
        logits = logits / temperature
    selected = torch.gather(logits, -1, index.unsqueeze(-1)).squeeze(-1)
    return selected - torch.logsumexp(logits, dim=-1)


@pytest.mark.parametrize("chunks", [4, 8])
@pytest.mark.parametrize("temperature", [1.0, 0.7])
def test_chunked_logps_match_fp32_reference(kernel, chunks, temperature):
    torch.manual_seed(0)
    b, t, h, v = 2, 256, 256, 4096  # small but same computation shape
    hidden = torch.randn(b, t, h, device="cuda", dtype=torch.bfloat16)
    lm_head = torch.randn(v, h, device="cuda", dtype=torch.bfloat16) * 0.02
    index = torch.randint(0, v, (b, t), device="cuda")

    got = kernel(hidden, lm_head, index, chunks=chunks, temperature=temperature)
    want = _fp32_reference(hidden, lm_head, index, temperature)
    assert torch.isfinite(got).all()
    assert (got - want).abs().max().item() < 1e-4


def test_chunked_entropy_matches_trl_definition(kernel):
    """Our chunked entropy must reproduce TRL's entropy_from_logits."""
    from trl.trainer.utils import entropy_from_logits

    from neuroagent.training.chunked_logps import chunked_entropy_from_hidden

    torch.manual_seed(0)
    b, t, h, v = 2, 128, 256, 4096
    hidden = torch.randn(b, t, h, device="cuda", dtype=torch.bfloat16)
    lm_head = torch.randn(v, h, device="cuda", dtype=torch.bfloat16) * 0.02

    logits = (hidden.to(lm_head.dtype) @ lm_head.t()).to(torch.float32)
    want = entropy_from_logits(logits)
    got = chunked_entropy_from_hidden(hidden, lm_head, temperature=1.0)
    assert (got - want).abs().max().item() < 1e-3


def test_chunked_uses_less_memory_than_full_logits(kernel):
    """The whole point: the batch x seq x vocab tensor must never be materialised."""
    torch.manual_seed(0)
    b, t, h, v = 2, 512, 256, 32768  # wide vocab is what makes the full path expensive
    hidden = torch.randn(b, t, h, device="cuda", dtype=torch.bfloat16)
    lm_head = torch.randn(v, h, device="cuda", dtype=torch.bfloat16) * 0.02
    index = torch.randint(0, v, (b, t), device="cuda")

    torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    _fp32_reference(hidden, lm_head, index)
    full_peak = torch.cuda.max_memory_allocated()

    torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    kernel(hidden, lm_head, index, chunks=8, temperature=1.0)
    chunked_peak = torch.cuda.max_memory_allocated()

    assert chunked_peak < full_peak, (chunked_peak, full_peak)


def test_resolver_rejects_quantised_head():
    """A packed 4-bit head cannot feed a raw matmul — the resolver must decline, not guess."""
    from neuroagent.training.chunked_logps import resolve_lm_head_and_body

    class _W(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.weight = torch.zeros(4, 4)
            self.weight.quant_state = object()  # mimic bitsandbytes packed weight

    class _M(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.lm_head = _W()
            self.model = torch.nn.Identity()

    assert resolve_lm_head_and_body(_M()) is None
