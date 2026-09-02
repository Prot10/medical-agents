"""Exact prefix sharing for a GRPO group: one forward over `prompt + completion_1 + ... + completion_G`.

Every completion in a group continues the same prompt, so the prompt's activations are identical
across the group. Packing the group into one sequence with a block-causal mask (a completion
attends to the prompt and to itself, never to a sibling) and prompt-continuing positions gives
per-token log-probabilities identical to separate forwards while processing the prompt once.

The mask is a FlexAttention `BlockMask`: block-sparse, so attention memory stays linear in the
sequence length and sibling blocks are skipped. A dense 4D mask would push PyTorch's SDPA onto the
materialised-scores kernel, which at ~18k packed tokens exhausts an A100-40GB. The model must be
loaded with `attn_implementation="flex_attention"` (`packing_config` reports whether it can be).

Exact for attention-only models (Granite 4.1; Gemma 4 with its per-layer-type masks). Not
applicable to Qwen3.5, whose gated-delta-net layers carry a recurrent state that cannot be forked.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import torch
from torch.nn.attention.flex_attention import BlockMask, create_block_mask

ATTN_IMPLEMENTATION = "flex_attention"


@dataclass
class PackedGroup:
    input_ids: torch.Tensor  # (1, L)
    position_ids: torch.Tensor  # (1, L)
    attention_mask: BlockMask | dict[str, BlockMask]
    completion_slices: list[slice]  # where each completion sits in the packed sequence


def pack_group(
    prompt_ids: list[int],
    completions: list[list[int]],
    *,
    layer_types: list[str] | None = None,
    sliding_window: int | None = None,
    device: torch.device | str = "cpu",
) -> PackedGroup:
    ids = list(prompt_ids)
    segment = [0] * len(prompt_ids)
    position = list(range(len(prompt_ids)))
    slices = []
    for index, completion in enumerate(completions, start=1):
        slices.append(slice(len(ids), len(ids) + len(completion)))
        ids += completion
        segment += [index] * len(completion)
        position += range(len(prompt_ids), len(prompt_ids) + len(completion))
    segment_t = torch.tensor(segment, device=device)
    position_t = torch.tensor(position, device=device)
    length = len(ids)

    def block_causal(batch, head, q, kv):
        """Attend iff key precedes-or-equals query in position and key is in the prompt or the same segment."""
        return (position_t[kv] <= position_t[q]) & ((segment_t[kv] == 0) | (segment_t[kv] == segment_t[q]))

    def block_mask(mask_mod):
        return create_block_mask(mask_mod, B=None, H=None, Q_LEN=length, KV_LEN=length, device=str(device))

    full = block_mask(block_causal)
    if layer_types and "sliding_attention" in layer_types:
        if sliding_window is None:
            raise ValueError("sliding_window is required for models with sliding attention layers")

        def sliding(batch, head, q, kv):
            # transformers' overlay: kv_idx > q_idx - sliding_window, on logical positions.
            return block_causal(batch, head, q, kv) & (position_t[kv] > position_t[q] - sliding_window)

        mask: BlockMask | dict[str, BlockMask] = {"full_attention": full, "sliding_attention": block_mask(sliding)}
    else:
        mask = full
    return PackedGroup(
        input_ids=torch.tensor([ids], device=device),
        position_ids=position_t[None],
        attention_mask=mask,
        completion_slices=slices,
    )


def packing_config(config) -> dict | None:
    """Layer-type information for `pack_group`, or None when the architecture cannot be packed."""
    config = getattr(config, "get_text_config", lambda: config)()
    layer_types = getattr(config, "layer_types", None)
    if layer_types and any(t not in ("full_attention", "sliding_attention") for t in layer_types):
        return None  # e.g. Qwen3.5's linear_attention layers
    return {"layer_types": layer_types, "sliding_window": getattr(config, "sliding_window", None)}


def packed_logits_to_keep(packed: PackedGroup, supervised: list[list[int]]) -> tuple[torch.Tensor, torch.Tensor]:
    """Positions (in the packed sequence) whose logits predict a supervised token, and those targets.

    `supervised[i]` lists indices into completion i whose tokens receive loss; the logit that predicts
    completion token j sits at packed position `start + j - 1` (the prompt's last token for j = 0).
    """
    prompt_end = packed.completion_slices[0].start - 1
    keep, targets = [], []
    for sl, positions in zip(packed.completion_slices, supervised):
        for j in positions:
            keep.append(prompt_end if j == 0 else sl.start + j - 1)
            targets.append(packed.input_ids[0, sl.start + j].item())
    return torch.tensor(keep, device=packed.input_ids.device), torch.tensor(targets, device=packed.input_ids.device)


def group_preserving_shuffle(seq_dict: dict[str, Sequence | None], *, group_size: int) -> dict[str, Sequence | None]:
    """Shuffle a generation batch by whole groups so every micro-batch stays one prompt's completions.

    TRL shuffles the generation batch row by row before splitting it into micro-batches, which
    would mix prompts inside a micro-batch and make the packed forward impossible.
    """
    first = next(v for v in seq_dict.values() if v is not None)
    rows = len(first)
    if rows % group_size:
        raise ValueError(f"generation batch of {rows} rows is not a multiple of the group size {group_size}")
    order = torch.randperm(rows // group_size).repeat_interleave(group_size) * group_size
    order = order + torch.arange(rows) % group_size
    return {
        key: (value[order] if isinstance(value, torch.Tensor) else [value[i] for i in order.tolist()]) if value is not None else None
        for key, value in seq_dict.items()
    }
