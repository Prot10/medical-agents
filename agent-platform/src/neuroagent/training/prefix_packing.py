"""Exact prefix sharing for a GRPO group: one forward over `prompt + completion_1 + ... + completion_G`.

Every completion in a group continues the same prompt, so the prompt's activations are identical
across the group. Packing the group into one sequence with a block-causal mask (a completion
attends to the prompt and to itself, never to a sibling) and prompt-continuing positions gives
per-token log-probabilities identical to separate forwards while processing the prompt once.

Exact for attention-only models (Granite 4.1; Gemma 4 with its per-layer-type masks). Not
applicable to Qwen3.5, whose gated-delta-net layers carry a recurrent state that cannot be forked.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class PackedGroup:
    input_ids: torch.Tensor  # (1, L)
    position_ids: torch.Tensor  # (1, L)
    attention_mask: torch.Tensor | dict[str, torch.Tensor]  # (1, 1, L, L) bool, True = attend
    completion_slices: list[slice]  # where each completion sits in the packed sequence


def _block_causal(segment: torch.Tensor, position: torch.Tensor) -> torch.Tensor:
    """Attend iff key precedes-or-equals query in position and key is in the prompt or the same segment."""
    q_seg, k_seg = segment[:, None], segment[None, :]
    q_pos, k_pos = position[:, None], position[None, :]
    return (k_pos <= q_pos) & ((k_seg == 0) | (k_seg == q_seg))


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
    full = _block_causal(segment_t, position_t)
    if layer_types and "sliding_attention" in layer_types:
        if sliding_window is None:
            raise ValueError("sliding_window is required for models with sliding attention layers")
        # transformers' overlay: kv_idx > q_idx - sliding_window, on logical positions.
        window = position_t[None, :] > position_t[:, None] - sliding_window
        mask: torch.Tensor | dict[str, torch.Tensor] = {
            "full_attention": full[None, None],
            "sliding_attention": (full & window)[None, None],
        }
    else:
        mask = full[None, None]
    return PackedGroup(
        input_ids=torch.tensor([ids], device=device),
        position_ids=position_t[None],
        attention_mask=mask,
        completion_slices=slices,
    )


def packing_config(model) -> dict | None:
    """Layer-type information for `pack_group`, or None when the architecture cannot be packed."""
    config = getattr(model.config, "get_text_config", lambda: model.config)()
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
