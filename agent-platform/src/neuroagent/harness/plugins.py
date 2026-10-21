"""Built-in, statically registered harness plugins.

Model plugins are derived from the fixed panel in ``model_registry`` so a model cannot be
evaluated without being registered. A model plugin accepts ``served_model`` to address a LoRA
adapter alias exposed by the server (see ``serve_model.sh``); the episode then records that
alias as the model identifier, which is the evidence that the adapter, not the base, answered.
"""

from __future__ import annotations

from typing import Any, Mapping

from ..evaluation.policy_reward import ClinicalPolicyReward
from ..llm.client import LLMClient
from ..model_registry import AVAILABLE_MODELS
from .adapters import NativeToolModelAdapter
from .interfaces import Plugin
from .loops import ClinicalPolicyLoop, DirectAnswerLoop, ReactAblationLoop


def _model_plugin(entry: Mapping[str, Any]) -> Plugin:
    def factory(config: Mapping[str, Any], _services: Any):
        # Any other config key (temperature, seed, top_k, chat_template_kwargs, ...) overrides
        # the model card defaults for that request.
        transport = {"base_url", "api_key", "served_model"}
        overrides = {key: value for key, value in config.items() if key not in transport}
        client = LLMClient(
            model=str(config.get("served_model", entry["hf_model_id"])),
            request={**entry["request_defaults"], **overrides},
            base_url=str(config.get("base_url", "http://localhost:8000/v1")),
            api_key=str(config.get("api_key", "not-needed")),
        )
        return NativeToolModelAdapter(client)

    return Plugin(
        plugin_id=f"model.{entry['key']}",
        version="1.0",
        provides="model",
        requires=frozenset(),
        factory=factory,
    )


def _simple(plugin_id: str, provides: str, build) -> Plugin:
    return Plugin(
        plugin_id=plugin_id,
        version="1.0",
        provides=provides,
        requires=frozenset(),
        factory=lambda config, _services: build(config),
    )


def builtin_plugins() -> dict[str, Plugin]:
    plugins = [_model_plugin(entry) for entry in AVAILABLE_MODELS] + [
        _simple("loop.policy", "loop", lambda _: ClinicalPolicyLoop()),
        _simple("loop.direct", "loop", lambda _: DirectAnswerLoop()),
        _simple("loop.react", "loop", lambda _: ReactAblationLoop()),
        _simple(
            "reward.policy",
            "reward",
            lambda config: ClinicalPolicyReward(
                require_approved=bool(config.get("require_approved", True))
            ),
        ),
    ]
    return {plugin.plugin_id: plugin for plugin in plugins}
