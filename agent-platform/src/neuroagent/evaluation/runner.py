"""Evaluation runner — run agent on NeuroBench cases and collect traces."""

from __future__ import annotations

import json
import logging
import os
import tempfile
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

from ..agent.config import AgentConfig
from ..agent.orchestrator import AgentOrchestrator
from ..agent.reasoning import AgentTrace
from ..tools.mock_server import MockServer
from ..tools.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)


@dataclass
class CaseResult:
    """Result of running the agent on a single case."""

    case_id: str
    condition: str
    difficulty: str
    trace: AgentTrace
    metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResults:
    """Collection of all case results from an evaluation run."""

    results: list[CaseResult] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)
    # Cases that raised during execution. Each entry is a structured dict with
    # "case_id", "condition", "difficulty", "error", and "traceback". Callers
    # should report len(failures) so a partially-failed run is never mistaken
    # for a complete one (the denominator matters for the benchmark).
    failures: list[dict[str, Any]] = field(default_factory=list)

    @property
    def num_cases(self) -> int:
        return len(self.results)

    @property
    def num_failures(self) -> int:
        return len(self.failures)


class EvaluationRunner:
    """Run agent on NeuroBench cases and collect traces."""

    def __init__(self, config: AgentConfig, dataset_path: str):
        self.config = config
        self.dataset_path = Path(dataset_path)

    def run_evaluation(
        self,
        split: str = "test",
        max_cases: int | None = None,
        enable_rules: bool = True,
        rules_dir: str = "config/hospital_rules",
        hospital: str = "us_mayo",
        output_dir: str | Path | None = None,
        checkpoint_name: str = "eval_checkpoint.json",
    ) -> EvaluationResults:
        """Run agent on all cases in the specified split.

        A case that raises no longer aborts the run: the error is recorded in
        ``EvaluationResults.failures`` and execution continues with the next case.

        Args:
            split: Dataset split to evaluate ("train", "val", "test").
            max_cases: Limit number of cases (for debugging).
            enable_rules: Whether to enable hospital rules.
            rules_dir: Path to hospital rules YAML directory.
            hospital: Hospital whose rules to load.
            output_dir: If set, results-so-far (including failures) are written
                atomically to ``output_dir / checkpoint_name`` after every case,
                so a crashed or killed run loses at most the in-flight case.
                Default None preserves the previous no-checkpoint behavior.
            checkpoint_name: Filename for the incremental checkpoint.

        Returns:
            EvaluationResults with all case results plus any per-case failures.
        """
        cases = self._load_cases(split, max_cases)
        logger.info("Loaded %d cases from split '%s'", len(cases), split)

        rules_engine = None
        if enable_rules:
            from ..rules.rules_engine import RulesEngine
            rules_engine = RulesEngine(rules_dir, hospital=hospital)

        # Store rules_engine so metrics computation can use it
        self._rules_engine = rules_engine

        eval_results = EvaluationResults(
            config={
                "model": self.config.model,
                "split": split,
                "enable_rules": enable_rules,
                "hospital": hospital,
            }
        )

        checkpoint_path: Path | None = None
        if output_dir is not None:
            checkpoint_path = Path(output_dir) / checkpoint_name
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

        for i, case in enumerate(cases):
            logger.info(
                "Running case %d/%d: %s (%s, %s)",
                i + 1, len(cases), case.case_id, case.condition.value, case.difficulty.value,
            )

            try:
                # Set up mock server and tool registry for this case
                mock_server = MockServer(case)
                tool_registry = ToolRegistry.create_default_registry(mock_server=mock_server)

                # Create agent
                agent = AgentOrchestrator(
                    config=self.config,
                    tool_registry=tool_registry,
                    rules_engine=rules_engine,
                )

                # Format initial patient info
                patient_info = self._format_initial_info(case)

                # Run agent
                trace = agent.run(
                    patient_info=patient_info,
                    case_id=case.case_id,
                )
            except Exception as exc:
                logger.exception("Case %s failed", case.case_id)
                eval_results.failures.append(
                    {
                        "case_id": case.case_id,
                        "condition": case.condition.value,
                        "difficulty": case.difficulty.value,
                        "error": f"{type(exc).__name__}: {exc}",
                        "traceback": traceback.format_exc(limit=10),
                    }
                )
                if checkpoint_path is not None:
                    self._write_checkpoint(checkpoint_path, eval_results)
                continue

            result = CaseResult(
                case_id=case.case_id,
                condition=case.condition.value,
                difficulty=case.difficulty.value,
                trace=trace,
            )
            eval_results.results.append(result)

            logger.info(
                "  → %d tool calls, %.1fs",
                trace.total_tool_calls, trace.elapsed_time_seconds,
            )

            if checkpoint_path is not None:
                self._write_checkpoint(checkpoint_path, eval_results)

        if eval_results.failures:
            logger.error(
                "Evaluation finished with %d/%d case(s) FAILED (dropped from results): %s",
                len(eval_results.failures),
                len(cases),
                [f["case_id"] for f in eval_results.failures],
            )

        return eval_results

    @staticmethod
    def _write_checkpoint(path: Path, eval_results: EvaluationResults) -> None:
        """Atomically persist results-so-far (tempfile in same dir + os.replace)."""
        payload = {
            "config": eval_results.config,
            "num_completed": eval_results.num_cases,
            "num_failures": eval_results.num_failures,
            "results": [
                {
                    "case_id": r.case_id,
                    "condition": r.condition,
                    "difficulty": r.difficulty,
                    "trace": r.trace.model_dump(mode="json"),
                    "metrics": r.metrics,
                }
                for r in eval_results.results
            ],
            "failures": eval_results.failures,
        }
        fd, tmp_name = tempfile.mkstemp(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w") as fh:
                json.dump(payload, fh, indent=2, default=str)
            os.replace(tmp_name, path)
        except BaseException:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise

    def run_single_case(
        self,
        case: NeuroBenchCase,
        enable_rules: bool = True,
        rules_dir: str = "config/hospital_rules",
        hospital: str = "us_mayo",
    ) -> AgentTrace:
        """Run agent on a single case (for debugging)."""
        mock_server = MockServer(case)
        tool_registry = ToolRegistry.create_default_registry(mock_server=mock_server)

        rules_engine = None
        if enable_rules:
            from ..rules.rules_engine import RulesEngine
            rules_engine = RulesEngine(rules_dir, hospital=hospital)

        agent = AgentOrchestrator(
            config=self.config,
            tool_registry=tool_registry,
            rules_engine=rules_engine,
        )

        patient_info = self._format_initial_info(case)
        return agent.run(patient_info=patient_info, case_id=case.case_id)

    def _load_cases(self, split: str, max_cases: int | None) -> list[NeuroBenchCase]:
        """Load cases from the dataset directory."""
        # Check for split file
        split_file = self.dataset_path / "splits" / f"{split}.txt"
        cases_dir = self.dataset_path / "cases"

        if split_file.exists():
            case_ids = split_file.read_text().strip().splitlines()
            case_files = [cases_dir / f"{cid}.json" for cid in case_ids]
            # A split entry without a case file silently changes the benchmark
            # denominator, so treat it as dataset corruption and fail loudly.
            missing = [cf.name for cf in case_files if not cf.exists()]
            if missing:
                raise FileNotFoundError(
                    f"Split '{split}' lists {len(missing)} case file(s) missing from "
                    f"{cases_dir}: {missing[:10]}"
                    + (" ..." if len(missing) > 10 else "")
                )
        elif cases_dir.exists():
            case_files = sorted(cases_dir.glob("*.json"))
        else:
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")

        if max_cases:
            case_files = case_files[:max_cases]

        cases = []
        for cf in case_files:
            data = json.loads(cf.read_text())
            cases.append(NeuroBenchCase.model_validate(data))

        return cases

    def _format_initial_info(self, case: NeuroBenchCase) -> str:
        """Format only what the doctor would tell the agent initially."""
        return format_patient_info(case)


def format_patient_info(case: NeuroBenchCase) -> str:
    """Format patient info as natural language for the agent.

    Shared by the evaluation runner, web API, and comparison scripts.
    """
    p = case.patient
    v = p.vitals
    exam = p.neurological_exam

    parts = [
        f"Patient: {p.demographics.age}-year-old {p.demographics.sex}",
        f"Chief complaint: {p.chief_complaint}",
        f"History of present illness: {p.history_present_illness}",
    ]

    pmh = p.clinical_history.past_medical_history
    if pmh:
        parts.append(f"Past medical history: {'; '.join(pmh)}")

    meds = p.clinical_history.medications
    if meds:
        med_strs = [f"{m.drug} {m.dose} {m.frequency} ({m.indication})" for m in meds]
        parts.append(f"Current medications: {'; '.join(med_strs)}")

    allergies = p.clinical_history.allergies
    if allergies:
        parts.append(f"Allergies: {', '.join(allergies)}")

    fhx = p.clinical_history.family_history
    if fhx:
        parts.append(f"Family history: {'; '.join(fhx)}")

    # Neurological exam as natural language (not JSON)
    exam_parts = []
    if exam.mental_status:
        exam_parts.append(f"Mental status: {exam.mental_status}")
    if exam.cranial_nerves:
        exam_parts.append(f"Cranial nerves: {exam.cranial_nerves}")
    if exam.motor:
        exam_parts.append(f"Motor: {exam.motor}")
    if exam.sensory:
        exam_parts.append(f"Sensory: {exam.sensory}")
    if exam.reflexes:
        exam_parts.append(f"Reflexes: {exam.reflexes}")
    if exam.coordination:
        exam_parts.append(f"Coordination: {exam.coordination}")
    if exam.gait:
        exam_parts.append(f"Gait: {exam.gait}")
    if exam.additional:
        exam_parts.append(f"Additional: {exam.additional}")
    parts.append("Neurological examination:\n" + "\n".join(f"  {e}" for e in exam_parts))

    # Vitals as natural language
    parts.append(
        f"Vitals: BP {v.bp_systolic}/{v.bp_diastolic} mmHg, "
        f"HR {v.hr} bpm, Temp {v.temp}°C, RR {v.rr}, SpO2 {v.spo2}%"
    )

    return "\n".join(parts)
