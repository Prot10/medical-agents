"""Medical specialist consultation tool — calls a secondary LLM for expert opinion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..llm.client import LLMClient
from .base import BaseTool, ToolCall, ToolResult

_PROMPT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "config" / "system_prompts"

_SPECIALIST_SYSTEM_PROMPT: str | None = None


def _load_specialist_prompt() -> str:
    global _SPECIALIST_SYSTEM_PROMPT
    if _SPECIALIST_SYSTEM_PROMPT is None:
        path = _PROMPT_DIR / "specialist.txt"
        if path.exists():
            _SPECIALIST_SYSTEM_PROMPT = path.read_text()
        else:
            _SPECIALIST_SYSTEM_PROMPT = (
                "You are a neurology specialist consultant. Provide your clinical "
                "opinion based ONLY on the information provided. Do NOT fabricate "
                "test results. Respond with: Specialist Opinion, Differential "
                "Critique, Red Flags, and Recommendation."
            )
    return _SPECIALIST_SYSTEM_PROMPT


class MedicalSpecialistTool(BaseTool):
    """Consult a medical specialist (secondary LLM) for a second opinion.

    In dual-model mode, this tool calls MedGemma (or another specialist LLM)
    on a separate vLLM instance.  In evaluation mode, it delegates to the
    MockServer like every other tool.  If neither is configured, it returns
    a graceful error.
    """

    name = "consult_medical_specialist"
    description = (
        "Request a second opinion from a medical specialist with deep neurology "
        "domain knowledge (~$75). The specialist reviews your clinical summary "
        "and current differential, then provides an independent assessment, "
        "critiques your differential, flags potential red herrings or missed "
        "diagnoses (including dual pathology), and suggests what to investigate "
        "next. The specialist has NO access to diagnostic tools — they reason "
        "only from the clinical data you provide.\n\n"
        "Use this tool:\n"
        "- After gathering initial evidence (2-3 tool calls), before committing "
        "to a diagnosis\n"
        "- When findings are ambiguous, conflicting, or suggest an atypical "
        "presentation\n"
        "- When you suspect a rare condition, dual pathology, or a diagnosis of "
        "exclusion\n\n"
        "Do NOT call this without first gathering some diagnostic evidence."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_summary": {
                "type": "string",
                "description": (
                    "Summary of the patient presentation and all diagnostic "
                    "findings gathered so far."
                ),
            },
            "current_differential": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Your current ranked differential diagnosis list.",
            },
            "specific_question": {
                "type": "string",
                "description": (
                    "A specific clinical question for the specialist (e.g., "
                    "'Could this be FND superimposed on MS rather than an MS "
                    "relapse?')"
                ),
            },
            "clinical_context": {
                "type": "string",
                "description": "Why you are consulting the specialist at this point.",
            },
        },
        "required": ["clinical_summary", "specific_question"],
    }

    def __init__(
        self,
        mock_server: Any | None = None,
        specialist_client: LLMClient | None = None,
    ):
        self.mock_server = mock_server
        self.specialist_client = specialist_client

    def execute(self, parameters: dict) -> ToolResult:
        # Evaluation mode — delegate to MockServer
        if self.mock_server is not None:
            return self.mock_server.get_output(self.name, parameters)

        # Live dual-model mode — call the specialist LLM
        if self.specialist_client is not None:
            return self._call_specialist(parameters)

        # Neither configured — specialist not available
        return ToolResult(
            tool_name=self.name,
            success=False,
            error_message=(
                "Medical specialist is not available. The dual-model mode is not "
                "enabled. Continue with your own clinical reasoning."
            ),
        )

    def _call_specialist(self, parameters: dict) -> ToolResult:
        """Build prompt and call the specialist LLM."""
        clinical_summary = parameters.get("clinical_summary", "")
        differential = parameters.get("current_differential", [])
        question = parameters.get("specific_question", "")
        context = parameters.get("clinical_context", "")

        user_message = self._build_user_prompt(
            clinical_summary, differential, question, context,
        )

        try:
            response = self.specialist_client.chat(
                messages=[
                    {"role": "system", "content": _load_specialist_prompt()},
                    {"role": "user", "content": user_message},
                ],
                tools=None,  # Specialist gets NO tools — pure knowledge
            )

            return ToolResult(
                tool_name=self.name,
                success=True,
                output={
                    "specialist_opinion": response.content or "",
                    "model": self.specialist_client.model,
                },
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                error_message=f"Specialist consultation failed: {e}",
            )

    @staticmethod
    def _build_user_prompt(
        clinical_summary: str,
        differential: list[str],
        question: str,
        context: str,
    ) -> str:
        parts = [f"## Clinical Summary\n{clinical_summary}"]

        if differential:
            diff_str = "\n".join(f"{i+1}. {d}" for i, d in enumerate(differential))
            parts.append(f"## Current Differential Diagnosis\n{diff_str}")

        parts.append(f"## Specific Question\n{question}")

        if context:
            parts.append(f"## Why I Am Consulting You\n{context}")

        return "\n\n".join(parts)
