"""Format reward — validates tool-call syntax and assessment structure."""

from __future__ import annotations

import re


# Expected structured assessment sections
_ASSESSMENT_SECTIONS = [
    r"###?\s*Primary Diagnosis",
    r"###?\s*Differential Diagnos[ei]s",
    r"###?\s*Recommended",
]

# Tool call must be valid JSON with name + arguments
_TOOL_CALL_PATTERN = re.compile(
    r'"name"\s*:\s*"[a-z_]+".*"arguments"\s*:\s*\{', re.DOTALL
)


class FormatReward:
    """Binary reward for correct output structure.

    Checks:
    1. Tool calls are well-formed (valid JSON, recognized tool names).
    2. Final assessment contains required sections.
    """

    VALID_TOOL_NAMES = frozenset({
        "analyze_eeg",
        "analyze_brain_mri",
        "analyze_ecg",
        "interpret_labs",
        "analyze_csf",
        "search_medical_literature",
        "check_drug_interactions",
    })

    def compute(
        self,
        tools_called: list[str],
        final_response: str | None,
        tool_calls_raw: list[dict] | None = None,
    ) -> float:
        """Compute format reward in {0, 1}.

        Args:
            tools_called: List of tool names the agent called.
            final_response: The agent's final assessment text.
            tool_calls_raw: Raw tool call dicts (optional, for deeper validation).

        Returns:
            1.0 if format is correct, 0.0 otherwise.
        """
        # Check tool names are valid (no hallucinated tools)
        if tools_called:
            for name in tools_called:
                if name not in self.VALID_TOOL_NAMES:
                    return 0.0

        # Check final response has structured assessment
        if not final_response:
            return 0.0

        sections_found = sum(
            1 for pattern in _ASSESSMENT_SECTIONS
            if re.search(pattern, final_response, re.IGNORECASE)
        )

        # Require at least 2 of 3 sections
        if sections_found < 2:
            return 0.0

        return 1.0
