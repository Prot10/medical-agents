"""Hospital rules engine — load and enforce clinical pathways."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


@dataclass
class PathwayStep:
    """A single step in a clinical pathway."""

    action: str
    timing: str = ""
    mandatory: bool = True
    condition: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ClinicalPathway:
    """A clinical pathway / protocol."""

    name: str
    description: str
    triggers: list[str]
    steps: list[PathwayStep]
    contraindicated: list[str] = field(default_factory=list)

    def get_required_actions(self) -> list[str]:
        """Return tool names of all mandatory steps."""
        return [s.action for s in self.steps if s.mandatory]

    def get_contraindicated_actions(self) -> list[str]:
        return list(self.contraindicated)


@dataclass
class ComplianceResult:
    """Result of checking agent compliance with a pathway."""

    pathway_name: str
    compliant: bool
    missing_required: list[str] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    completed_steps: list[str] = field(default_factory=list)


AVAILABLE_HOSPITALS: dict[str, str] = {
    "us_mayo": "Mayo Clinic, USA (AAN guidelines)",
    "uk_nhs": "NHS England (NICE guidelines)",
    "de_charite": "Charité Berlin, Germany (DGN guidelines)",
    "jp_todai": "University of Tokyo Hospital (JSN/JES guidelines)",
    "br_hcfmusp": "HC-FMUSP São Paulo, Brazil (ABN guidelines)",
}


class RulesEngine:
    """Load and enforce hospital clinical pathways."""

    def __init__(
        self,
        rules_dir: str = "config/hospital_rules",
        hospital: str = "us_mayo",
    ):
        base = Path(rules_dir)
        # Support both new (per-hospital subdirs) and legacy (flat dir) layouts
        hospital_dir = base / hospital
        self.rules_dir = hospital_dir if hospital_dir.is_dir() else base
        self.hospital = hospital
        self.pathways: list[ClinicalPathway] = []
        if self.rules_dir.exists():
            self._load_pathways()

    def _load_pathways(self) -> None:
        """Load all YAML pathway files from the rules directory."""
        for yaml_file in self.rules_dir.glob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)
                if data:
                    pathway = self._parse_pathway(data)
                    self.pathways.append(pathway)
                    logger.info("Loaded pathway: %s", pathway.name)
            except Exception as e:
                logger.error("Failed to load pathway %s: %s", yaml_file, e)

    def _parse_pathway(self, data: dict[str, Any]) -> ClinicalPathway:
        """Parse a YAML dict into a ClinicalPathway."""
        steps = []
        for step_data in data.get("steps", []):
            steps.append(
                PathwayStep(
                    action=step_data["action"],
                    timing=step_data.get("timing", ""),
                    mandatory=step_data.get("mandatory", True),
                    condition=step_data.get("condition"),
                    details={
                        k: v
                        for k, v in step_data.items()
                        if k not in ("action", "timing", "mandatory", "condition")
                    },
                )
            )

        return ClinicalPathway(
            name=data["name"],
            description=data.get("description", ""),
            triggers=data.get("triggers", []),
            steps=steps,
            contraindicated=data.get("contraindicated", []),
        )

    def get_context(self) -> str:
        """Return a compact summary of ALL protocols for the system prompt.

        All pathways are always injected — the agent must determine which
        pathway applies based on the clinical presentation.  Selectively
        injecting only the matching pathway would leak the diagnosis.

        To save tokens, the format is compact: one line per pathway with
        only mandatory steps and contraindicated actions (optional steps
        omitted).
        """
        if not self.pathways:
            return ""

        hospital_label = AVAILABLE_HOSPITALS.get(self.hospital, self.hospital)
        lines = [
            f"You are operating under the clinical protocols of **{hospital_label}**.",
            "Follow the protocol that matches the clinical presentation. Available pathways:",
        ]
        for p in self.pathways:
            triggers = ", ".join(p.triggers)
            # Compact: pathway name + triggers on one line
            lines.append(f"- **{p.name}** (triggers: {triggers})")
            # Only mandatory steps (skip optional to save tokens)
            mandatory_steps = [s for s in p.steps if s.mandatory]
            if mandatory_steps:
                step_names = ", ".join(f"{s.action} ({s.timing})" for s in mandatory_steps)
                lines.append(f"  MANDATORY: {step_names}")
            if p.contraindicated:
                lines.append(f"  CONTRAINDICATED: {'; '.join(p.contraindicated)}")
        return "\n".join(lines)

    def get_pathway(self, trigger: str) -> ClinicalPathway | None:
        """Find a matching clinical pathway for a trigger condition."""
        trigger_lower = trigger.lower()
        for pathway in self.pathways:
            if any(t.lower() in trigger_lower or trigger_lower in t.lower() for t in pathway.triggers):
                return pathway
        return None

    def check_compliance(self, tools_called: list[str], pathway: ClinicalPathway) -> ComplianceResult:
        """Check if the agent's actions comply with a pathway.

        Args:
            tools_called: List of tool names the agent called (in order).
            pathway: The clinical pathway to check against.

        Returns:
            ComplianceResult with details of compliance/violations.
        """
        required = pathway.get_required_actions()
        completed = [a for a in required if a in tools_called]
        missing = [a for a in required if a not in tools_called]

        # Check for contraindicated actions
        violations = []
        for action_desc in pathway.contraindicated:
            # Contraindicated items are free-text descriptions, not tool names
            # This is a simplified check; the LLM judge does detailed assessment
            violations_found = False
            for tool_name in tools_called:
                if tool_name.lower() in action_desc.lower():
                    violations.append(action_desc)
                    violations_found = True
                    break

        return ComplianceResult(
            pathway_name=pathway.name,
            compliant=len(missing) == 0 and len(violations) == 0,
            missing_required=missing,
            violations=violations,
            completed_steps=completed,
        )
