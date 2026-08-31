"""Noise injection for robustness evaluation."""

from __future__ import annotations

import random
from enum import Enum
from typing import Any

from pydantic import BaseModel


class NoiseType(str, Enum):
    """Types of noise that can be injected into tool outputs."""

    ACCURACY = "accuracy"  # Replace correct findings with incorrect ones
    COMPLETENESS = "completeness"  # Remove some findings
    CONFIDENCE = "confidence"  # Miscalibrate confidence scores
    CONTRADICTION = "contradiction"  # Make findings contradict other modalities
    SPECIFICITY = "specificity"  # Replace detailed findings with vague ones


class NoiseInjector:
    """Injects controlled noise into mock tool outputs for robustness testing.

    For full noise injection, an LLM is used to modify outputs while keeping
    them valid Pydantic models. This class provides rule-based noise injection
    for the simpler noise types (CONFIDENCE, COMPLETENESS) and stubs for
    LLM-based injection (ACCURACY, CONTRADICTION, SPECIFICITY).
    """

    def __init__(self, llm_client: Any | None = None, seed: int = 42):
        self.llm = llm_client
        self.rng = random.Random(seed)

    def inject(
        self,
        tool_output: dict[str, Any],
        tool_name: str,
        noise_type: NoiseType,
        severity: float,
    ) -> dict[str, Any]:
        """Inject noise into a tool output.

        Args:
            tool_output: Serialized tool output dict.
            tool_name: Name of the tool (for context).
            noise_type: Type of noise to inject.
            severity: Noise level, 0.0 (none) to 1.0 (maximum).

        Returns:
            Modified tool output dict.
        """
        if severity <= 0.0:
            return tool_output

        # Make a deep copy to avoid modifying the original
        import copy
        output = copy.deepcopy(tool_output)

        if noise_type == NoiseType.CONFIDENCE:
            return self._inject_confidence_noise(output, severity)
        elif noise_type == NoiseType.COMPLETENESS:
            return self._inject_completeness_noise(output, severity)
        elif noise_type in (NoiseType.ACCURACY, NoiseType.CONTRADICTION, NoiseType.SPECIFICITY):
            if self.llm:
                return self._inject_llm_noise(output, tool_name, noise_type, severity)
            # Fallback: simple completeness noise
            return self._inject_completeness_noise(output, severity)

        return output

    def _inject_confidence_noise(self, output: dict, severity: float) -> dict:
        """Miscalibrate confidence scores."""
        if "confidence" in output:
            original = output["confidence"]
            # Add random noise proportional to severity
            noise = self.rng.gauss(0, severity * 0.3)
            output["confidence"] = max(0.0, min(1.0, original + noise))
        return output

    def _inject_completeness_noise(self, output: dict, severity: float) -> dict:
        """Remove findings based on severity level."""
        if "findings" in output and isinstance(output["findings"], list):
            findings = output["findings"]
            if findings:
                # Remove a fraction of findings based on severity
                n_remove = max(0, int(len(findings) * severity))
                if n_remove > 0 and n_remove < len(findings):
                    indices_to_remove = self.rng.sample(range(len(findings)), n_remove)
                    output["findings"] = [
                        f for i, f in enumerate(findings) if i not in indices_to_remove
                    ]
        return output

    def _inject_llm_noise(
        self, output: dict, tool_name: str, noise_type: NoiseType, severity: float
    ) -> dict:
        """Use LLM to inject sophisticated noise while preserving schema validity."""
        # This requires the LLM client to be configured
        # For now, return the output with completeness noise as fallback
        return self._inject_completeness_noise(output, severity)
