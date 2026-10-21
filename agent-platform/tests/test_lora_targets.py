"""GRPO LoRA targets: the language model's decoder projections, never the multimodal towers."""

from __future__ import annotations

import re

import pytest

pytest.importorskip("trl")

from neuroagent.training.train_grpo import LORA_TARGETS  # noqa: E402

TARGETED = [
    "model.layers.3.self_attn.q_proj",  # Qwen3.5 / Granite full attention
    "model.layers.3.linear_attn.in_proj_qkv",  # Qwen3.5 gated delta net
    "model.layers.3.linear_attn.out_proj",
    "model.layers.3.mlp.gate_proj",
    "model.language_model.layers.12.self_attn.o_proj",  # Gemma 4 text tower
    "model.language_model.layers.12.mlp.down_proj",
]
EXCLUDED = [
    "lm_head",
    "model.visual.blocks.5.attn.qkv",  # Qwen3.5 vision tower
    "model.visual.merger.linear_fc1",
    "model.vision_tower.encoder.layers.2.self_attn.q_proj",  # Gemma 4 vision tower
    "model.audio_tower.layers.1.attention.relative_k_proj",
    "model.embed_vision.embedding_projection",
    "model.language_model.layers.12.per_layer_input_gate",  # Gemma per-layer embedding gadgets
    "model.layers.3.mlp.act_fn",  # not a projection
    "model.layers.3.linear_attn.conv1d",
    "model.language_model.per_layer_model_projection",
]


def test_lora_targets_select_language_model_projections_only():
    pattern = re.compile(LORA_TARGETS)
    assert all(pattern.fullmatch(name) for name in TARGETED)
    assert not any(pattern.fullmatch(name) for name in EXCLUDED)
