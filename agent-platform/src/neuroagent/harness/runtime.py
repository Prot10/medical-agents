"""Boot a checked profile and bind its services to one case."""

from __future__ import annotations

from neuroagent_schemas import NeuroBenchCase

from .environment import NeuroBenchEnvironment
from .interfaces import RunContext
from .kernel import HarnessKernel, ServiceRegistry
from .plugins import builtin_plugins
from .profile import HarnessProfile


def boot_profile(profile: HarnessProfile) -> ServiceRegistry:
    return HarnessKernel(builtin_plugins()).boot(profile.plugin_configs())


def context_from_profile(
    profile: HarnessProfile, case: NeuroBenchCase, services: ServiceRegistry
) -> RunContext:
    plugins = builtin_plugins()
    return RunContext(
        profile_id=profile.profile_id,
        model=services.require("model"),
        loop=services.require("loop"),
        environment=NeuroBenchEnvironment(case),
        max_turns=profile.max_turns,
        max_cost_usd=profile.max_cost_usd,
        max_invalid_actions=profile.max_invalid_actions,
        plugin_versions={item.id: plugins[item.id].version for item in profile.plugins},
    )
