"""Memory retrieval strategies for patient context building."""

from __future__ import annotations

from typing import Any


class MemoryRetriever:
    """Retrieval strategy for patient memory.

    Implements the retrieval hierarchy:
    1. Always retrieve: demographics, active diagnoses, current medications, allergies
    2. Semantic search: encounters relevant to the current complaint
    3. Recent: most recent N encounters
    4. Trend data: relevant lab/test trends over time
    """

    def __init__(self, patient_memory: Any):
        self.memory = patient_memory

    def retrieve_context(
        self,
        patient_id: str,
        current_complaint: str | None = None,
        max_encounters: int = 5,
    ) -> str:
        """Build a context string from patient memory.

        Args:
            patient_id: Patient identifier.
            current_complaint: Current chief complaint for semantic matching.
            max_encounters: Max encounters to include.

        Returns:
            Formatted context string for system prompt injection.
        """
        return self.memory.retrieve(
            patient_id=patient_id,
            current_complaint=current_complaint,
            max_encounters=max_encounters,
        )
