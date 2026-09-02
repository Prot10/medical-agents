"""Packed group forward must reproduce per-row log-probabilities exactly (tiny random models, CPU)."""

from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")
transformers = pytest.importorskip("transformers")

from neuroagent.training.prefix_packing import pack_group, packed_logits_to_keep, packing_config  # noqa: E402


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
    cfg = packing_config(model)
    assert cfg is not None
    packed = pack_group(prompt, completions, **cfg)
    keep, targets = packed_logits_to_keep(packed, [list(range(len(c))) for c in completions])
    with torch.no_grad():
        logits = model(
            input_ids=packed.input_ids, position_ids=packed.position_ids, attention_mask=packed.attention_mask,
            logits_to_keep=keep, use_cache=False,
        ).logits[0].float()
    logps = torch.log_softmax(logits, -1).gather(-1, targets[:, None])[:, 0]
    out, offset = [], 0
    for completion in completions:
        out.append(logps[offset : offset + len(completion)])
        offset += len(completion)
    return out


@pytest.mark.parametrize("model_name", ["granite", "gemma4"])
def test_packed_group_matches_separate_forwards(model_name):
    if model_name == "granite":
        from transformers import GraniteConfig

        model = _tiny(GraniteConfig)
    else:
        from transformers import Gemma4TextConfig

        # Three sliding layers then a full one, window smaller than the sequences so it matters.
        model = _tiny(Gemma4TextConfig, sliding_window=8, layer_types=["sliding_attention"] * 3 + ["full_attention"], head_dim=16)
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

    class Model:
        config = Cfg()

    assert packing_config(Model()) is None
