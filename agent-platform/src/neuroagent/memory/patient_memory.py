"""Per-patient longitudinal memory store using ChromaDB."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

import chromadb

logger = logging.getLogger(__name__)


class PatientMemory:
    """Per-patient longitudinal memory store."""

    def __init__(self, db_path: str = "./data/patient_memory"):
        self.db_path = db_path
        self.vector_store = chromadb.PersistentClient(path=db_path)
        self.collection = self.vector_store.get_or_create_collection(
            name="patient_encounters",
            metadata={"hnsw:space": "cosine"},
        )

    def store_encounter(self, patient_id: str, trace: Any) -> None:
        """Store a completed encounter in memory.

        Args:
            patient_id: Unique patient identifier.
            trace: AgentTrace from the completed encounter.
        """
        timestamp = datetime.now().isoformat()
        summary = self._summarize_encounter(trace)

        encounter_id = f"{patient_id}_{timestamp}"

        metadata: dict[str, Any] = {
            "patient_id": patient_id,
            "date": timestamp,
            "tools_called": json.dumps(trace.tools_called),
            "total_tool_calls": trace.total_tool_calls,
        }

        # Extract diagnosis from final response if available
        if trace.final_response:
            metadata["has_diagnosis"] = True
        else:
            metadata["has_diagnosis"] = False

        self.collection.add(
            documents=[summary],
            metadatas=[metadata],
            ids=[encounter_id],
        )

        logger.info("Stored encounter %s for patient %s", encounter_id, patient_id)

    def retrieve(
        self,
        patient_id: str,
        current_complaint: str | None = None,
        max_encounters: int = 5,
    ) -> str:
        """Retrieve relevant patient history for the agent's context.

        Args:
            patient_id: Patient to look up.
            current_complaint: If provided, also do semantic search for similar encounters.
            max_encounters: Maximum encounters to return.

        Returns:
            Formatted patient history string for injection into system prompt.
        """
        # Get all encounters for this patient
        results = self.collection.get(
            where={"patient_id": patient_id},
            include=["documents", "metadatas"],
        )

        if not results["documents"]:
            return ""

        # Sort by date (most recent first)
        encounters = list(zip(results["documents"], results["metadatas"]))
        encounters.sort(key=lambda x: x[1].get("date", ""), reverse=True)

        # Take the most recent ones
        encounters = encounters[:max_encounters]

        # Format as patient history
        parts = [f"Previous encounters for this patient ({len(encounters)} found):"]
        for i, (doc, meta) in enumerate(encounters, 1):
            date = meta.get("date", "unknown")
            parts.append(f"\n### Encounter {i} ({date})")
            parts.append(doc)

        return "\n".join(parts)

    def clear_patient(self, patient_id: str) -> None:
        """Remove all encounters for a patient."""
        results = self.collection.get(where={"patient_id": patient_id})
        if results["ids"]:
            self.collection.delete(ids=results["ids"])

    def clear_all(self) -> None:
        """Remove all stored encounters."""
        self.vector_store.delete_collection("patient_encounters")
        self.collection = self.vector_store.get_or_create_collection(
            name="patient_encounters",
            metadata={"hnsw:space": "cosine"},
        )

    def _summarize_encounter(self, trace: Any) -> str:
        """Extract a summary from an agent trace for storage.

        Keeps key facts (diagnoses, findings, plan) and discards verbose reasoning.
        """
        parts = []

        # Include tool call summary
        if trace.tools_called:
            parts.append(f"Tests performed: {', '.join(trace.tools_called)}")

        # Include final response (the diagnosis and plan)
        if trace.final_response:
            # Truncate if very long
            response = trace.final_response
            if len(response) > 2000:
                response = response[:2000] + "..."
            parts.append(f"Assessment:\n{response}")

        return "\n\n".join(parts) if parts else "No summary available."
