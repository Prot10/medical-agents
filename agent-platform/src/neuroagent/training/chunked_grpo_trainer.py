"""A GRPOTrainer that never materialises the full 248k-vocab logits tensor.

Only ``_get_per_token_logps_and_entropies`` is overridden — TRL's generation, advantage,
loss, clipping, checkpointing and our ``rollout_func`` all stay exactly as they are. The
override swaps TRL's

    logits = model(**inputs).logits          # batch x seq x 248320  <- the OOM
    logps  = selective_log_softmax(logits, completion_ids)

for Unsloth's chunked kernel, which computes ``hidden @ lm_head.T`` a chunk at a time from
the transformer's hidden states, so the wide tensor never exists. See ``chunked_logps`` for
the numerical validation and the licensing note.

Every path that this override does not confidently handle (multimodal inputs, an unusual
model layout, a quantised lm_head, a missing kernel) falls back to ``super()``. A silently
wrong logprob would corrupt the gradient without crashing, so the bar for taking the fast
path is "provably the same shape of computation", not "probably fine".
"""

from __future__ import annotations

import logging

import torch
from trl import GRPOTrainer

from .chunked_logps import (
    chunked_entropy_from_hidden,
    load_unsloth_chunked_kernel,
    resolve_lm_head_and_body,
)

logger = logging.getLogger(__name__)


class ChunkedLogpsGRPOTrainer(GRPOTrainer):
    """GRPOTrainer with memory-efficient chunked logprob computation.

    Args:
        logit_chunks: how many pieces to split the flattened (batch*seq) dimension into.
            Unsloth's own default heuristic is ``max(4, context_len // 4096)``; 4 already
            gives ~3.9x and 8 gives ~4.4x at our shapes, with the returns flattening after.
    """

    def __init__(self, *args, logit_chunks: int = 8, **kwargs):
        super().__init__(*args, **kwargs)
        self.logit_chunks = logit_chunks
        self._chunked_kernel = load_unsloth_chunked_kernel()
        self._chunked_warned = False
        if self._chunked_kernel is not None:
            logger.info(
                "Chunked logprobs ENABLED (Unsloth kernel, %d chunks) — the "
                "batch x seq x vocab logits tensor is never materialised.",
                logit_chunks,
            )

    def _fallback_once(self, reason: str):
        if not self._chunked_warned:
            logger.warning("Chunked logprobs unavailable (%s) — using TRL's full-logits path.", reason)
            self._chunked_warned = True

    def _get_per_token_logps_and_entropies(
        self,
        model,
        input_ids,
        attention_mask,
        logits_to_keep,
        batch_size=None,
        compute_entropy=False,
        pixel_values=None,
        image_grid_thw=None,
        num_images=None,
        pixel_attention_mask=None,
        image_sizes=None,
        token_type_ids=None,
        mm_token_type_ids=None,
    ):
        multimodal = any(
            x is not None
            for x in (pixel_values, image_grid_thw, num_images, pixel_attention_mask,
                      image_sizes, token_type_ids, mm_token_type_ids)
        )
        if self._chunked_kernel is None or multimodal:
            if multimodal:
                self._fallback_once("multimodal inputs")
            return super()._get_per_token_logps_and_entropies(
                model, input_ids, attention_mask, logits_to_keep, batch_size, compute_entropy,
                pixel_values, image_grid_thw, num_images, pixel_attention_mask, image_sizes,
                token_type_ids, mm_token_type_ids,
            )

        resolved = resolve_lm_head_and_body(model)
        if resolved is None:
            self._fallback_once("could not resolve lm_head/body, or head is quantised")
            return super()._get_per_token_logps_and_entropies(
                model, input_ids, attention_mask, logits_to_keep, batch_size, compute_entropy,
            )
        body, lm_head_weight = resolved

        try:
            return self._chunked_logps(
                body, lm_head_weight, input_ids, attention_mask, logits_to_keep,
                batch_size, compute_entropy,
            )
        except Exception as exc:
            # Never let this optimisation kill a multi-hour run: fall back to TRL's path and
            # keep training. Disable it for the rest of the run so we fail over once, loudly,
            # rather than paying the exception cost on every step.
            self._chunked_kernel = None
            logger.error(
                "Chunked logprobs failed (%s: %s) — falling back to TRL's full-logits path "
                "for the REST of this run. Training continues.", type(exc).__name__, exc,
            )
            return super()._get_per_token_logps_and_entropies(
                model, input_ids, attention_mask, logits_to_keep, batch_size, compute_entropy,
            )

    def _chunked_logps(
        self, body, lm_head_weight, input_ids, attention_mask, logits_to_keep,
        batch_size, compute_entropy,
    ):
        batch_size = batch_size or input_ids.size(0)
        all_logps, all_entropies = [], []
        for start in range(0, input_ids.size(0), batch_size):
            input_ids_batch = input_ids[start : start + batch_size]
            attention_mask_batch = attention_mask[start : start + batch_size]

            # Hidden states only — we deliberately do NOT call the causal-LM head here.
            out = body(
                input_ids=input_ids_batch,
                attention_mask=attention_mask_batch,
                use_cache=False,
            )
            hidden = getattr(out, "last_hidden_state", None)
            if hidden is None:
                raise TypeError(
                    f"expected hidden states from the transformer body, got "
                    f"{type(out).__name__} — the lm_head/body resolution is wrong"
                )

            # Mirror TRL's alignment exactly: drop the final position (it predicts the token
            # after the sequence), then keep only the completion positions.
            hidden = hidden[:, :-1, :]
            hidden = hidden[:, -logits_to_keep:, :]
            completion_ids = input_ids_batch[:, -logits_to_keep:]

            # temperature is applied INSIDE the kernel, matching TRL's `logits / temperature`.
            logps = self._chunked_kernel(
                hidden,
                lm_head_weight,
                completion_ids,
                chunks=self.logit_chunks,
                temperature=self.temperature,
            )
            all_logps.append(logps)

            if compute_entropy:
                all_entropies.append(
                    chunked_entropy_from_hidden(hidden, lm_head_weight, self.temperature)
                )

        logps = torch.cat(all_logps, dim=0)
        entropies = torch.cat(all_entropies, dim=0) if compute_entropy else None
        return logps, entropies
