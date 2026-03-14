"""Compress old encounters into concise summaries to prevent context overflow."""

from __future__ import annotations

from ..llm.client import LLMClient

_SUMMARIZE_PROMPT = """\
You are a clinical note summarizer. Compress the following encounter into a concise \
summary preserving ONLY the clinically essential information:

- Diagnoses made
- Key test results (abnormal findings only)
- Medications started, changed, or stopped
- Follow-up plan and outstanding items
- Red flags or safety concerns

Remove all verbose reasoning, normal findings, and procedural details.
Keep it under 200 words.
"""


class MemorySummarizer:
    """Compress verbose encounter records into concise summaries."""

    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm

    def summarize(self, encounter_text: str) -> str:
        """Summarize a verbose encounter into key clinical facts.

        Args:
            encounter_text: Full encounter text to compress.

        Returns:
            Concise clinical summary.
        """
        if self.llm is None:
            return self._rule_based_summarize(encounter_text)

        messages = [
            {"role": "system", "content": _SUMMARIZE_PROMPT},
            {"role": "user", "content": encounter_text},
        ]
        response = self.llm.chat(messages=messages, tools=None, temperature=0.0)
        return response.content or encounter_text

    def _rule_based_summarize(self, text: str) -> str:
        """Simple truncation-based summary when no LLM is available."""
        if len(text) <= 500:
            return text
        return text[:500] + "..."
