"""Packed group forward (FlexAttention block mask) must reproduce per-row SDPA log-probabilities (tiny random models, CPU)."""

from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")
transformers = pytest.importorskip("transformers")

from neuroagent.training.prefix_packing import (  # noqa: E402
    ATTN_IMPLEMENTATION,
    group_preserving_shuffle,
    pack_group,
    packed_group_logps,
    packed_logits_to_keep,
    packing_config,
)


def _tiny(config_cls, **overrides):
    config = config_cls(
        vocab_size=257, hidden_size=64, intermediate_size=128, num_hidden_layers=4, num_attention_heads=4,
        num_key_value_heads=2, max_position_embeddings=512, **overrides,
    )
    torch.manual_seed(0)
    model = transformers.AutoModelForCausalLM.from_config(config).eval()
    return model


def _per_row_logps(model, prompt, completions):
    rows = []
    for completion in completions:
        ids = torch.tensor([prompt + completion])
        with torch.no_grad():
            logits = model(input_ids=ids).logits[0].float()
        start = len(prompt)
        rows.append(torch.log_softmax(logits[start - 1 : start - 1 + len(completion)], -1).gather(-1, ids[0, start:, None])[:, 0])
    return rows


def _packed_logps(model, prompt, completions):
    cfg = packing_config(model.config)
    assert cfg is not None and cfg["kernel_options"] is None  # tiny heads: default tiles
    model.set_attn_implementation(ATTN_IMPLEMENTATION)
    packed = pack_group(prompt, completions, layer_types=cfg["layer_types"], sliding_window=cfg["sliding_window"])
    keep, targets = packed_logits_to_keep(packed, [list(range(len(c))) for c in completions])
    with torch.no_grad():
        logps, entropy = packed_group_logps(model, packed, keep, targets, compute_entropy=True, chunk=5)
    assert entropy.shape == logps.shape and torch.isfinite(entropy).all()
    out, offset = [], 0
    for completion in completions:
        out.append(logps[offset : offset + len(completion)])
        offset += len(completion)
    return out


@pytest.mark.parametrize("model_name", ["granite", "gemma4"])
def test_packed_group_matches_separate_forwards(model_name):
    if model_name == "granite":
        from transformers import GraniteConfig

        model = _tiny(GraniteConfig, logits_scaling=16.0)  # Granite 4.1 divides its logits
    else:
        from transformers import Gemma4TextConfig

        # Three sliding layers then a full one, window smaller than the sequences so it matters.
        model = _tiny(
            Gemma4TextConfig, sliding_window=8, layer_types=["sliding_attention"] * 3 + ["full_attention"],
            head_dim=16, global_head_dim=16, final_logit_softcapping=30.0,  # Gemma 4 soft-caps its logits
        )
    torch.manual_seed(1)
    prompt = torch.randint(3, 250, (20,)).tolist()
    completions = [torch.randint(3, 250, (n,)).tolist() for n in (7, 12, 5)]
    separate = _per_row_logps(model, prompt, completions)
    packed = _packed_logps(model, prompt, completions)
    for a, b in zip(separate, packed):
        assert torch.allclose(a, b, atol=1e-4, rtol=1e-4), (a - b).abs().max()


def test_qwen_style_hybrid_layers_are_not_packable():
    class Cfg:
        layer_types = ["linear_attention", "full_attention"]

    assert packing_config(Cfg()) is None


def test_group_preserving_shuffle_keeps_each_group_contiguous():
    torch.manual_seed(3)
    prompt_ids = torch.tensor([[p] * 2 for p in (0, 0, 0, 1, 1, 1, 2, 2, 2)])
    batch = {"prompt_ids": prompt_ids, "case_id": ["a", "a", "a", "b", "b", "b", "c", "c", "c"], "none": None, "scalar": torch.tensor(7)}
    out = group_preserving_shuffle(batch, group_size=3)
    groups = [out["case_id"][i : i + 3] for i in range(0, 9, 3)]
    assert all(len(set(g)) == 1 for g in groups) and sorted(g[0] for g in groups) == ["a", "b", "c"]
    assert torch.equal(out["prompt_ids"][:, 0], torch.tensor([{"a": 0, "b": 1, "c": 2}[c] for c in out["case_id"]]))
    assert out["none"] is None and out["scalar"].item() == 7
    with pytest.raises(ValueError):
        group_preserving_shuffle(batch, group_size=4)


def test_wide_heads_get_smaller_flex_tiles():
    class Cfg:
        layer_types = ["sliding_attention", "full_attention"]
        sliding_window = 512
        head_dim = 256
        global_head_dim = 512

    assert packing_config(Cfg())["kernel_options"] == {"BLOCK_M": 16, "BLOCK_N": 16, "num_stages": 1}
    Cfg.global_head_dim = 256
    assert packing_config(Cfg())["kernel_options"] == {"BLOCK_M": 32, "BLOCK_N": 32}
