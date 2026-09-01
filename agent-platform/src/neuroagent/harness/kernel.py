"""Small deterministic plugin kernel with explicit dependency validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .interfaces import Plugin


class HarnessConfigError(ValueError):
    pass


class ServiceRegistry:
    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def provide(self, service: str, value: Any) -> None:
        if service in self._services:
            raise HarnessConfigError(f"duplicate provider for service {service!r}")
        self._services[service] = value

    def require(self, service: str) -> Any:
        try:
            return self._services[service]
        except KeyError as exc:
            raise HarnessConfigError(f"missing required service {service!r}") from exc

    def as_dict(self) -> dict[str, Any]:
        return dict(self._services)


@dataclass(frozen=True, slots=True)
class PluginConfig:
    plugin_id: str
    config: Mapping[str, Any]


class HarnessKernel:
    def __init__(self, plugins: Mapping[str, Plugin]) -> None:
        self._plugins = dict(plugins)

    def boot(self, configured: list[PluginConfig]) -> ServiceRegistry:
        requested: dict[str, tuple[Plugin, Mapping[str, Any]]] = {}
        for item in configured:
            if item.plugin_id not in self._plugins:
                raise HarnessConfigError(f"unknown plugin {item.plugin_id!r}")
            if item.plugin_id in requested:
                raise HarnessConfigError(f"plugin configured twice: {item.plugin_id!r}")
            requested[item.plugin_id] = (self._plugins[item.plugin_id], item.config)

        registry = ServiceRegistry()
        pending = dict(requested)
        while pending:
            progressed = False
            for plugin_id, (plugin, config) in list(pending.items()):
                if all(requirement in registry.as_dict() for requirement in plugin.requires):
                    service = plugin.factory(config, registry)
                    registry.provide(plugin.provides, service)
                    del pending[plugin_id]
                    progressed = True
            if not progressed:
                unresolved = {
                    plugin_id: sorted(plugin.requires - registry.as_dict().keys())
                    for plugin_id, (plugin, _) in pending.items()
                }
                raise HarnessConfigError(
                    f"unresolved plugin dependencies or cycle: {unresolved}"
                )
        return registry
