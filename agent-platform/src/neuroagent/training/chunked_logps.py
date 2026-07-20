"""Memory-efficient per-token logprobs for GRPO, via Unsloth's chunked kernel.

Qwen3.5 has a 248,320-token vocabulary. TRL's GRPO computes per-token logprobs by
materialising the full logits tensor — ``batch x seq_len x 248320`` — which at our
multi-turn shapes is the single largest allocation in the run and the direct cause of the
backward-pass OOM (measured: 16.4 GB for a mere batch=2, seq=2048, and 22.7 GB at
batch=8, seq=3072 on a 39.5 GB card).

Unsloth solves this with ``chunked_hidden_states_selective_log_softmax``: it takes the
model's HIDDEN STATES plus the ``lm_head`` weight and computes ``hidden @ lm_head.T`` one
chunk at a time, so the full logits tensor never exists. We call their kernel directly
rather than reimplementing it — measured here at our real shapes:

    chunks=4 : forward max-err 9.5e-07, grad max-err 1.1e-03 rel, peak 4.20 GB (3.9x less)
    chunks=8 : forward max-err 9.5e-07, grad max-err 1.1e-03 rel, peak 3.72 GB (4.4x less)

The forward matches to fp32 round-off; the gradient agrees to ~1e-3 relative, which is
inside bf16's own precision (eps ~8e-3) — accumulation-order noise, not a discrepancy.

Licensing: unsloth-zoo is LGPL-3.0-or-later. We IMPORT it as a dependency (dynamic linking),
which keeps this file under the project's own licence; copying the kernel's source in-tree
would make that file LGPL. Do not vendor it.

Entropy: Unsloth's kernel returns only logprobs — their integration replaces TRL's loss
wholesale so they never need TRL's entropy. We keep TRL's loss and swap only the logprob
computation, so ``_chunked_entropy_from_hidden`` below reproduces TRL's
``entropy_from_logits`` chunk-wise (under ``no_grad``, as TRL does).
"""

from __future__ import annotations

import logging
import os
from typing import Any

import torch

logger = logging.getLogger(__name__)


def load_unsloth_chunked_kernel():
    """Import Unsloth's chunked log-softmax kernel, or return None if unavailable.

    Two import-time side effects of ``unsloth_zoo`` are neutralised here:
      * its ``__init__`` refuses to load unless ``UNSLOTH_IS_PRESENT`` is set (normally set
        by importing ``unsloth``, which would patch transformers/TRL — we must NOT let it,
        our multi-turn rollout depends on stock TRL 0.29 ``rollout_func``);
      * it CLEARS ``PYTORCH_CUDA_ALLOC_CONF``, dropping our ``expandable_segments:True``
        anti-fragmentation setting. We save and restore it.
    """
    import contextlib
    import io

    saved_alloc_conf = os.environ.get("PYTORCH_CUDA_ALLOC_CONF")
    os.environ.setdefault("UNSLOTH_IS_PRESENT", "1")
    try:
        # unsloth_zoo prints a banner ("🦥 Unsloth: Will patch your computer...") with a bare
        # print() at import, which bypasses logging and lands on the terminal that the training
        # UI owns. Swallow it — the import itself is what we want, not the advertisement.
        with contextlib.redirect_stdout(io.StringIO()):
            from unsloth_zoo.rl_replacements import (
                chunked_hidden_states_selective_log_softmax,
            )
    except Exception as exc:  # not installed / incompatible — caller falls back to TRL
        logger.warning("Unsloth chunked kernel unavailable (%s); using TRL's full-logits path", exc)
        return None
    finally:
        if saved_alloc_conf is not None:
            os.environ["PYTORCH_CUDA_ALLOC_CONF"] = saved_alloc_conf
        elif "PYTORCH_CUDA_ALLOC_CONF" in os.environ:
            del os.environ["PYTORCH_CUDA_ALLOC_CONF"]
    return chunked_hidden_states_selective_log_softmax


def resolve_lm_head_and_body(model: Any) -> tuple[Any, torch.Tensor] | None:
    """Find (transformer_body, lm_head_weight), unwrapping PEFT/accelerate wrappers.

    Returns None when the layout is not the plain causal-LM one this path assumes, so the
    caller can fall back to TRL rather than guess. The weight must be a real dense tensor:
    under QLoRA the 4-bit layers are packed, and a packed weight cannot be used in the
    chunked matmul. (Measured on Qwen3.5-4B QLoRA, ``lm_head`` stays a bf16 ``nn.Linear`` —
    bitsandbytes does not quantise it — so this path applies.)
    """
    # Descend through PeftModel / LoraModel / DDP / compiled wrappers AND through the causal
    # LM itself. Attribute access on a PeftModel forwards to the wrapped model, so the wrapper
    # ALSO answers to `.lm_head`/`.model` — stopping at the first match hands back the causal
    # LM as the "body", whose forward returns logits (CausalLMOutputWithPast), not hidden
    # states. Keep descending while the candidate still exposes an lm_head; the first module
    # WITHOUT one is the transformer body.
    lm_head = None
    body = model
    for _ in range(8):
        head = getattr(body, "lm_head", None)
        inner = getattr(body, "model", None)
        if head is not None and inner is not None and inner is not body:
            lm_head = head
            body = inner
            continue
        # No lm_head here: either we've reached the body, or we're at a pure wrapper.
        if head is None and lm_head is not None:
            break
        nxt = None
        for attr in ("module", "base_model", "_orig_mod"):
            cand = getattr(body, attr, None)
            if cand is not None and cand is not body:
                nxt = cand
                break
        if nxt is None:
            break
        body = nxt

    if lm_head is None or body is None or body is model:
        return None
    weight = getattr(lm_head, "weight", None)
    if weight is None or getattr(weight, "quant_state", None) is not None:
        return None  # packed 4-bit head — not usable in a raw matmul
    if weight.dim() != 2:
        return None
    return body, weight


@torch.no_grad()
def chunked_entropy_from_hidden(
    hidden: torch.Tensor, lm_head_weight: torch.Tensor, temperature: float, chunk_rows: int = 128
) -> torch.Tensor:
    """Per-token Shannon entropy without materialising full logits.

    Reproduces TRL's ``entropy_from_logits`` (``-sum(exp(logp) * logp)``) but computes the
    logits chunk-by-chunk from hidden states, so the 248k-wide tensor is never held whole.
    Runs under ``no_grad`` exactly as TRL's call site does, so nothing is retained for backward.
    """
    n_embd = hidden.shape[-1]
    flat = hidden.reshape(-1, n_embd)
    out = []
    for chunk in flat.split(chunk_rows, dim=0):
        logits = (chunk.to(lm_head_weight.dtype) @ lm_head_weight.t()).to(torch.float32)
        if temperature != 1.0:
            logits = logits / temperature
        logps = torch.log_softmax(logits, dim=-1)
        out.append(-(torch.exp(logps) * logps).sum(-1))
    return torch.cat(out, dim=0).reshape(hidden.shape[:-1])
