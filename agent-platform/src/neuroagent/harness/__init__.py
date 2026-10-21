"""Composable clinical-agent harness."""

from .adapters import SUBMIT_TOOL, ActionDecodeError, NativeToolModelAdapter
from .context import POLICY_SYSTEM_PROMPT, format_patient_info, transcript
from .environment import NeuroBenchEnvironment
from .interfaces import (
    AgentLoop,
    ClinicalEnvironment,
    ModelAdapter,
    ModelTurn,
    Plugin,
    RewardScorer,
    RunContext,
)
from .kernel import HarnessConfigError, HarnessKernel, PluginConfig, ServiceRegistry
from .loops import ClinicalPolicyLoop, DirectAnswerLoop, ReactAblationLoop
from .plugins import builtin_plugins
from .profile import HarnessProfile, load_profile, load_profiles
from .runtime import boot_profile, context_from_profile
from .store import MemoryEpisodeStore

__all__ = [
    "POLICY_SYSTEM_PROMPT",
    "SUBMIT_TOOL",
    "ActionDecodeError",
    "AgentLoop",
    "ClinicalEnvironment",
    "ClinicalPolicyLoop",
    "DirectAnswerLoop",
    "HarnessConfigError",
    "HarnessKernel",
    "HarnessProfile",
    "MemoryEpisodeStore",
    "ModelAdapter",
    "ModelTurn",
    "NativeToolModelAdapter",
    "NeuroBenchEnvironment",
    "Plugin",
    "PluginConfig",
    "ReactAblationLoop",
    "RewardScorer",
    "RunContext",
    "ServiceRegistry",
    "boot_profile",
    "builtin_plugins",
    "context_from_profile",
    "format_patient_info",
    "load_profile",
    "load_profiles",
    "transcript",
]
