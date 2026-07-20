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
    ) -> float | None:
        """Compute compliance reward in {0, 1}, or ``None`` when there is nothing to measure.

        Args:
            tools_called: Tools the agent called.
            condition: Clinical condition string (used to find matching pathway).

        Returns:
            1.0 if compliant with the relevant pathway, 0.0 otherwise, or ``None``
            if no pathway covers this condition. ``None`` means "no measurement" —
            only 5 of the ~23 conditions have a pathway, so returning a constant
            1.0 for the other ~18 injected a fixed +weight that is invisible to a
            group-relative advantage (dead gradient) yet real when comparing across
            conditions. The composite renormalises around a ``None`` so the live
            components carry the full weight instead. See ``CompositeReward``.
        """
        pathway = self.engine.get_pathway(condition)
        if pathway is None:
            return None

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
