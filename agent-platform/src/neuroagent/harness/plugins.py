"""Built-in, statically registered harness plugins."""

from __future__ import annotations

from typing import Any, Mapping

from ..evaluation.policy_reward import ClinicalPolicyReward
from ..llm.client import LLMClient
from .adapters import JsonActionModelAdapter, NativeToolModelAdapter
from .interfaces import Plugin
from .loops import ClinicalPolicyLoop, DirectAnswerLoop, ReactAblationLoop


def _client(config: Mapping[str, Any], model_id: str) -> LLMClient:
    return LLMClient(
        base_url=str(config.get("base_url", "http://localhost:8000/v1")),
        api_key=str(config.get("api_key", "not-needed")),
        model=model_id,
        temperature=float(config.get("temperature", 0.2)),
        max_tokens=int(config.get("max_tokens", 4096)),
        seed=config.get("seed"),
        extra_body=dict(config.get("extra_body", {})),
    )


def builtin_plugins() -> dict[str, Plugin]:
    def native(plugin_id: str, model_id: str) -> Plugin:
        return Plugin(
            plugin_id=plugin_id,
            version="1.0",
            provides="model",
            requires=frozenset(),
            factory=lambda config, _: NativeToolModelAdapter(_client(config, model_id), model_id),
        )

    return {
        "model.qwen3.5-9b": native("model.qwen3.5-9b", "Qwen/Qwen3.5-9B"),
        "model.gemma-4-e4b": native("model.gemma-4-e4b", "google/gemma-4-E4B-it"),
        "model.medgemma-1.5-4b": Plugin(
            plugin_id="model.medgemma-1.5-4b",
            version="1.0",
            provides="model",
            requires=frozenset(),
            factory=lambda config, _: JsonActionModelAdapter(
                _client(config, "google/medgemma-1.5-4b-it"),
                "google/medgemma-1.5-4b-it",
            ),
        ),
        "loop.policy": Plugin(
            plugin_id="loop.policy",
            version="1.0",
            provides="loop",
            requires=frozenset(),
            factory=lambda _config, _services: ClinicalPolicyLoop(),
        ),
        "loop.direct": Plugin(
            plugin_id="loop.direct",
            version="1.0",
            provides="loop",
            requires=frozenset(),
            factory=lambda _config, _services: DirectAnswerLoop(),
        ),
        "loop.react": Plugin(
            plugin_id="loop.react",
            version="1.0",
            provides="loop",
            requires=frozenset(),
            factory=lambda _config, _services: ReactAblationLoop(),
        ),
        "reward.policy": Plugin(
            plugin_id="reward.policy",
            version="1.0",
            provides="reward",
            requires=frozenset(),
            factory=lambda config, _services: ClinicalPolicyReward(
                require_approved=bool(config.get("require_approved", True))
            ),
        ),
    }
