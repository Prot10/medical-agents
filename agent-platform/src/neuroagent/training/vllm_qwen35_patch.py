"""Make TRL's colocated vLLM engine load Qwen3.5 text-only, so weight sync works.

Qwen3.5 ships a multimodal checkpoint. `AutoModelForCausalLM` maps it to
``Qwen3_5ForCausalLM``, which drops the vision tower and names its parameters ``model.*`` —
that is what we train. vLLM instead instantiates ``Qwen3_5ForConditionalGeneration``, whose
parameters are ``language_model.model.*`` plus a ``visual.*`` tower. TRL's weight sync then
tries to push ``model.layers...`` into an engine that has no ``model``, and dies with:

    ValueError: There is no module or parameter named 'model' in Qwen3_5ForConditionalGeneration

vLLM's ``EngineArgs`` exposes ``language_model_only``, which loads only the language model and
therefore reproduces the text-only parameter layout (our serving script already passes the
equivalent ``--language-model-only``). TRL's ``VLLMGeneration`` hard-codes its ``LLM(...)``
kwargs with no passthrough for engine arguments, so the flag is injected at construction.

This is applied only when colocated vLLM is actually in use, and is idempotent.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def _engine_expects_language_model_prefix(generation) -> bool:
    """True when the colocated engine holds a `language_model` submodule.

    Detected from the live engine rather than assumed from the model name, so this is a no-op
    for any model vLLM loads with the same layout the trainer uses. Cached on the instance:
    sync_weights runs per parameter per step.
    """
    cached = getattr(generation, "_neuroagent_needs_lm_prefix", None)
    if cached is not None:
        return cached
    needs = False
    try:
        engine_model = (
            generation.llm.llm_engine.model_executor.driver_worker.model_runner.model
        )
        needs = hasattr(engine_model, "language_model")
    except Exception as exc:  # server mode, or a different vLLM internal layout
        logger.debug("Could not inspect vLLM engine layout (%s); assuming no prefix", exc)
    generation._neuroagent_needs_lm_prefix = needs
    if needs:
        logger.info(
            "vLLM engine exposes a `language_model` submodule — weight-sync names will be "
            "re-prefixed (model.* -> language_model.model.*) to match."
        )
    return needs


def patch_vllm_language_model_only() -> bool:
    """Inject ``language_model_only=True`` into TRL's vLLM engine construction.

    Returns True if the patch is in place (or already was), False if TRL's vLLM module could
    not be imported — in which case vLLM is not in use and there is nothing to patch.
    """
    try:
        from trl.generation import vllm_generation as vg
    except Exception as exc:
        logger.debug("TRL vLLM generation module unavailable (%s)", exc)
        return False

    if getattr(vg, "_neuroagent_language_model_only_patched", False):
        return True

    original_llm = getattr(vg, "LLM", None)
    if original_llm is None:
        logger.warning("TRL's vLLM module exposes no LLM symbol — cannot force text-only load")
        return False

    def _llm_text_only(*args, **kwargs):
        # setdefault, not override: if a future TRL passes it explicitly, respect that.
        kwargs.setdefault("language_model_only", True)
        return original_llm(*args, **kwargs)

    vg.LLM = _llm_text_only

    # `language_model_only` drops the vision tower but does NOT rename anything: the engine is
    # still Qwen3_5ForConditionalGeneration, so its weights are `language_model.model.*` while
    # the trained Qwen3_5ForCausalLM produces `model.*`. TRL normalises names in exactly one
    # place before pushing them, so re-prefix there.
    original_fix = vg.VLLMGeneration._fix_param_name_to_vllm

    def _fix_param_name_with_language_model_prefix(self, name, extra_prefixes=None):
        name = original_fix(self, name, extra_prefixes)
        if _engine_expects_language_model_prefix(self) and not name.startswith("language_model."):
            name = f"language_model.{name}"
        return name

    vg.VLLMGeneration._fix_param_name_to_vllm = _fix_param_name_with_language_model_prefix
    vg._neuroagent_language_model_only_patched = True
    logger.info(
        "vLLM engine will load Qwen3.5 text-only (language_model_only=True) so its parameter "
        "names match the trained Qwen3_5ForCausalLM and weight sync can map them."
    )
    return True
