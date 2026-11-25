"""Composable clinical-agent harness."""

from .adapters import SUBMIT_TOOL, ActionDecodeError, NativeToolModelAdapter
from .context import (
    FREE_ORDER_SYSTEM_PROMPT,
    NARRATIVE_SYSTEM_PROMPT,
    POLICY_SYSTEM_PROMPT,
    RULES_ADDENDUM,
    format_patient_info,
    transcript,
)
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
from .free_order import FreeOrderEnvironment, FreeOrderGatekeeper, typed_episode
from .loops import (
    ClinicalPolicyLoop,
    DirectAnswerLoop,
    FreeOrderLoop,
    MultiAgentPanelLoop,
    NarrativeOnlyLoop,
    ReactAblationLoop,
    RulesInPromptLoop,
)
from .plugins import builtin_plugins
from .profile import HarnessProfile, load_profile, load_profiles
from .runtime import boot_profile, context_from_profile
from .store import MemoryEpisodeStore

__all__ = [
    "FREE_ORDER_SYSTEM_PROMPT",
    "FreeOrderEnvironment",
    "FreeOrderGatekeeper",
    "FreeOrderLoop",
    "typed_episode",
    "NARRATIVE_SYSTEM_PROMPT",
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
    "MultiAgentPanelLoop",
    "NarrativeOnlyLoop",
    "NativeToolModelAdapter",
    "NeuroBenchEnvironment",
    "Plugin",
    "PluginConfig",
    "RULES_ADDENDUM",
    "ReactAblationLoop",
    "RewardScorer",
    "RulesInPromptLoop",
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
