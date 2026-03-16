"""Compliance reward — wraps RulesEngine for hospital protocol adherence."""

from __future__ import annotations

from ...rules.rules_engine import ClinicalPathway, RulesEngine


class ComplianceReward:
    """Binary reward for hospital protocol compliance.

    Checks the agent's tool calls against the relevant clinical pathway.
    Returns 1.0 if compliant, 0.0 otherwise.
    """

    def __init__(
        self,
        rules_dir: str = "config/hospital_rules",
        hospital: str = "us_mayo",
    ):
        self.engine = RulesEngine(rules_dir=rules_dir, hospital=hospital)

    def compute(
        self,
        tools_called: list[str],
        condition: str,
    ) -> float:
        """Compute compliance reward in {0, 1}.

        Args:
            tools_called: Tools the agent called.
            condition: Clinical condition string (used to find matching pathway).

        Returns:
            1.0 if compliant with relevant pathway, 0.0 otherwise.
            Returns 1.0 if no matching pathway found (no rules to violate).
        """
        pathway = self.engine.get_pathway(condition)
        if pathway is None:
            return 1.0

        result = self.engine.check_compliance(tools_called, pathway)
        return 1.0 if result.compliant else 0.0

    def compute_with_pathway(
        self,
        tools_called: list[str],
        pathway: ClinicalPathway,
    ) -> float:
        """Compute compliance against a specific pathway."""
        result = self.engine.check_compliance(tools_called, pathway)
        return 1.0 if result.compliant else 0.0
