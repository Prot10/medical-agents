"""Results analysis and paper figure generation."""

from __future__ import annotations

from typing import Any

import polars as pl

from .runner import EvaluationResults


class ResultsAnalyzer:
    """Analyze evaluation results and generate tables and figures."""

    def results_to_dataframe(self, results: EvaluationResults) -> pl.DataFrame:
        """Convert evaluation results to a Polars DataFrame."""
        rows = []
        for r in results.results:
            row = {
                "case_id": r.case_id,
                "condition": r.condition,
                "difficulty": r.difficulty,
                "tool_calls": r.trace.total_tool_calls,
                "time_seconds": r.trace.elapsed_time_seconds,
                "tools_used": ",".join(r.trace.tools_called),
            }
            row.update(r.metrics)
            rows.append(row)
        return pl.DataFrame(rows)

    def generate_main_table(self, results: EvaluationResults) -> pl.DataFrame:
        """Table 1: Overall metrics summary."""
        df = self.results_to_dataframe(results)

        metrics_cols = [
            "diagnostic_accuracy_top1",
            "diagnostic_accuracy_top3",
            "action_precision",
            "action_recall",
            "critical_actions_hit",
            "efficiency_score",
            "safety_score",
        ]

        available_cols = [c for c in metrics_cols if c in df.columns]
        if not available_cols:
            return pl.DataFrame({"metric": ["No metrics available"], "value": [0.0]})

        summary = {}
        for col in available_cols:
            summary[col] = df[col].mean()

        return pl.DataFrame(
            {"metric": list(summary.keys()), "value": list(summary.values())}
        )

    def generate_condition_breakdown(self, results: EvaluationResults) -> pl.DataFrame:
        """Breakdown of metrics by neurological condition."""
        df = self.results_to_dataframe(results)

        if "diagnostic_accuracy_top1" not in df.columns:
            return df

        return df.group_by("condition").agg(
            pl.col("diagnostic_accuracy_top1").mean().alias("accuracy_top1"),
            pl.col("tool_calls").mean().alias("avg_tool_calls"),
            pl.len().alias("n_cases"),
        ).sort("condition")

    def generate_difficulty_breakdown(self, results: EvaluationResults) -> pl.DataFrame:
        """Breakdown of metrics by difficulty level."""
        df = self.results_to_dataframe(results)

        if "diagnostic_accuracy_top1" not in df.columns:
            return df

        return df.group_by("difficulty").agg(
            pl.col("diagnostic_accuracy_top1").mean().alias("accuracy_top1"),
            pl.col("tool_calls").mean().alias("avg_tool_calls"),
            pl.len().alias("n_cases"),
        ).sort("difficulty")

    def generate_ablation_table(
        self, named_results: dict[str, EvaluationResults]
    ) -> pl.DataFrame:
        """Table 2: Ablation study comparing different configurations."""
        rows = []
        for name, results in named_results.items():
            df = self.results_to_dataframe(results)
            row: dict[str, Any] = {"configuration": name}
            for col in ["diagnostic_accuracy_top1", "action_recall", "safety_score"]:
                if col in df.columns:
                    row[col] = df[col].mean()
            rows.append(row)
        return pl.DataFrame(rows)

    def export_case_examples(
        self, results: EvaluationResults, n: int = 5
    ) -> list[dict[str, Any]]:
        """Export detailed case walkthroughs for the paper's qualitative section."""
        examples = []
        for r in results.results[:n]:
            examples.append({
                "case_id": r.case_id,
                "condition": r.condition,
                "difficulty": r.difficulty,
                "tools_called": r.trace.tools_called,
                "total_tool_calls": r.trace.total_tool_calls,
                "final_response": r.trace.final_response,
                "metrics": r.metrics,
            })
        return examples
