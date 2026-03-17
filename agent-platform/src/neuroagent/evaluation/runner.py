"""Evaluation runner — run agent on NeuroBench cases and collect traces."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

from ..agent.orchestrator import AgentConfig, AgentOrchestrator
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

    @property
    def num_cases(self) -> int:
        return len(self.results)


class EvaluationRunner:
    """Run agent on NeuroBench cases and collect traces."""

    def __init__(self, config: AgentConfig, dataset_path: str):
        self.config = config
        self.dataset_path = Path(dataset_path)

    def run_evaluation(
        self,
        split: str = "test",
        max_cases: int | None = None,
        enable_memory: bool = False,
        enable_rules: bool = True,
        rules_dir: str = "config/hospital_rules",
        hospital: str = "us_mayo",
    ) -> EvaluationResults:
        """Run agent on all cases in the specified split.

        Args:
            split: Dataset split to evaluate ("train", "val", "test").
            max_cases: Limit number of cases (for debugging).
            enable_memory: Whether to enable patient memory.
            enable_rules: Whether to enable hospital rules.
            rules_dir: Path to hospital rules YAML directory.

        Returns:
            EvaluationResults with all case results.
        """
        cases = self._load_cases(split, max_cases)
        logger.info("Loaded %d cases from split '%s'", len(cases), split)

        # Set up optional components
        memory = None
        if enable_memory:
            from ..memory.patient_memory import PatientMemory
            memory = PatientMemory()

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
                "enable_memory": enable_memory,
                "enable_rules": enable_rules,
                "hospital": hospital,
            }
        )

        for i, case in enumerate(cases):
            logger.info(
                "Running case %d/%d: %s (%s, %s)",
                i + 1, len(cases), case.case_id, case.condition.value, case.difficulty.value,
            )

            # Set up mock server and tool registry for this case
            mock_server = MockServer(case)
            tool_registry = ToolRegistry.create_default_registry(mock_server=mock_server)

            # Create agent
            agent = AgentOrchestrator(
                config=self.config,
                tool_registry=tool_registry,
                memory=memory,
                rules_engine=rules_engine,
            )

            # Format initial patient info
            patient_info = self._format_initial_info(case)

            # Run agent
            trace = agent.run(
                patient_info=patient_info,
                patient_id=case.patient.patient_id if enable_memory else None,
                case_id=case.case_id,
            )

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

        return eval_results

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
        elif cases_dir.exists():
            case_files = sorted(cases_dir.glob("*.json"))
        else:
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")

        if max_cases:
            case_files = case_files[:max_cases]

        cases = []
        for cf in case_files:
            if cf.exists():
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
