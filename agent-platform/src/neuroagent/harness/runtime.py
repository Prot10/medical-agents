"""Boot a checked profile and bind its services to one case."""

from __future__ import annotations

from pathlib import Path

from neuroagent_schemas import NeuroBenchCase

from .environment import NeuroBenchEnvironment
from .interfaces import EpisodeStore, RunContext
from .kernel import HarnessKernel
from .plugins import builtin_plugins
from .profile import HarnessProfile, load_profile
from .store import MemoryEpisodeStore


def boot_profile(profile: HarnessProfile):
    return HarnessKernel(builtin_plugins()).boot(profile.plugin_configs())


def context_from_profile(
    profile: HarnessProfile,
    case: NeuroBenchCase,
    *,
    episode_store: EpisodeStore | None = None,
) -> RunContext:
    plugins = builtin_plugins()
    services = HarnessKernel(plugins).boot(profile.plugin_configs())
    model = services.require("model")
    loop = services.require("loop")
    versions = {item.id: plugins[item.id].version for item in profile.plugins}
    return RunContext(
        profile_id=profile.profile_id,
        model=model,
        loop=loop,
        environment=NeuroBenchEnvironment(case),
        episode_store=episode_store or MemoryEpisodeStore(),
        max_turns=profile.max_turns,
        max_cost_usd=profile.max_cost_usd,
        plugin_versions=versions,
    )


def run_profile(path: str | Path, case: NeuroBenchCase):
    profile = load_profile(path)
    context = context_from_profile(profile, case)
    return context.loop.run(context)
