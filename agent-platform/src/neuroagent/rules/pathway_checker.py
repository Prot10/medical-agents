"""Pathway compliance checker — wraps the rules engine for evaluation."""

from __future__ import annotations

from typing import Any

from .rules_engine import ComplianceResult, RulesEngine


class PathwayChecker:
    """High-level interface for checking agent compliance with clinical pathways."""

    def __init__(self, rules_engine: RulesEngine):
        self.engine = rules_engine

    def check_case(
        self,
        tools_called: list[str],
        condition: str,
    ) -> ComplianceResult | None:
        """Check compliance for a case given its condition.

        Args:
            tools_called: Ordered list of tools the agent called.
            condition: The neurological condition (used to find matching pathway).

        Returns:
            ComplianceResult if a matching pathway was found, None otherwise.
        """
        pathway = self.engine.get_pathway(condition)
        if pathway is None:
            return None
        return self.engine.check_compliance(tools_called, pathway)

    def check_all_pathways(
        self,
        tools_called: list[str],
    ) -> list[ComplianceResult]:
        """Check compliance against all loaded pathways.

        Returns:
            List of ComplianceResult for each pathway.
        """
        results = []
        for pathway in self.engine.pathways:
            result = self.engine.check_compliance(tools_called, pathway)
            results.append(result)
        return results
