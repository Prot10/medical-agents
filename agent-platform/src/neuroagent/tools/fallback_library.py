"""Benchmark-level fallback tier: a normal, non-contributory result for any legal order.

Cases carry pre-generated outputs for the studies on their pathway, and many carry a case-specific
off-pathway fallback. Where neither exists, the MockServer used to fail the order with a message
that told the agent the study was off-pathway. This library closes that gap: one generic normal
report per tool and parameter value, authored once for the benchmark
(`config/tools/fallback_library.yaml`, physician review pending), so an off-pathway order is
answered the same way in every case and reveals nothing about the patient.

Resolution is by the tool's discriminating parameter (the `by` block names it); tools without one
use `default`. Set-valued orders are assembled from tables: lab analytes, CSF special tests and
molecular assays each get their normal entry.
"""

from __future__ import annotations

import copy
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

from neuroagent_schemas import tool_outputs as T

from .vocabulary import normalize_analyte

DEFAULT_LIBRARY_PATH = Path(__file__).resolve().parents[3] / "config" / "tools" / "fallback_library.yaml"

OUTPUT_MODELS: dict[str, type[BaseModel]] = {
    "analyze_eeg": T.EEGReport,
    "analyze_brain_mri": T.MRIReport,
    "analyze_ecg": T.ECGReport,
    "interpret_labs": T.LabResults,
    "analyze_csf": T.CSFResults,
    "order_ct_scan": T.CTReport,
    "order_echocardiogram": T.EchoReport,
    "order_cardiac_monitoring": T.CardiacMonitoringReport,
    "order_advanced_imaging": T.AdvancedImagingReport,
    "order_specialized_test": T.SpecializedTestReport,
    "order_body_imaging": T.BodyImagingReport,
    "order_microbiology": T.MicrobiologyReport,
    "obtain_tissue_diagnosis": T.TissueDiagnosisReport,
    "perform_clinical_assessment": T.ClinicalAssessmentReport,
    "search_medical_literature": T.LiteratureSearchResult,
    "check_drug_interactions": T.DrugInteractionResult,
}


def _as_names(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return []


class FallbackLibrary:
    def __init__(self, path: Path = DEFAULT_LIBRARY_PATH) -> None:
        self.path = path
        with open(path) as handle:
            data = yaml.safe_load(handle)
        self.tools: dict[str, dict[str, Any]] = data["tools"]
        self.status = data.get("status", "draft")
        self._validate()

    def _validate(self) -> None:
        for tool, entry in self.tools.items():
            model = OUTPUT_MODELS[tool]
            if tool == "interpret_labs":
                for name, rows in entry["analytes"].items():
                    for row in rows:
                        T.LabValue.model_validate({**row, "is_abnormal": False})
                continue
            if "default" in entry:
                model.model_validate(entry["default"])
            for values in entry.get("by", {}).values():
                for output in values.values():
                    model.model_validate(output)
        self._analytes = {normalize_analyte(name): (name, rows) for name, rows in self.tools["interpret_labs"]["analytes"].items()}
        self._csf_tests = {normalize_analyte(name): (name, text) for name, text in self.tools["analyze_csf"]["special_tests"].items()}
        self._assays = {normalize_analyte(name): (name, text) for name, text in self.tools["obtain_tissue_diagnosis"]["molecular_assays"].items()}

    def _entry(self, tool: str, parameters: dict[str, Any]) -> dict[str, Any] | None:
        entry = self.tools.get(tool)
        if entry is None:
            return None
        by = entry.get("by")
        if by:
            parameter, values = next(iter(by.items()))
            selected = parameters.get(parameter)
            if isinstance(selected, str) and selected in values:
                return copy.deepcopy(values[selected])
            if "default" in entry:
                return copy.deepcopy(entry["default"])
            return copy.deepcopy(next(iter(values.values())))  # the parameter was omitted: first listed variant
        return copy.deepcopy(entry["default"]) if "default" in entry else None

    def resolve(self, tool: str, parameters: dict[str, Any]) -> BaseModel | None:
        """The library's answer to a legal order, or None when the tool is not covered."""
        if tool == "interpret_labs":
            return self._labs(parameters)
        output = self._entry(tool, parameters)
        if output is None:
            return None
        if tool == "perform_clinical_assessment":
            # The report says when it was made: the order's timing, else the schema default.
            output["timing"] = str(parameters.get("timing") or "baseline")
        if tool == "analyze_csf":
            output["source"] = str(parameters.get("source") or "lumbar_puncture")
            output["special_tests"] = {
                self._csf_tests[normalize_analyte(name)][0]: self._csf_tests[normalize_analyte(name)][1]
                for name in _as_names(parameters.get("special_tests"))
                if normalize_analyte(name) in self._csf_tests
            }
        elif tool == "obtain_tissue_diagnosis":
            requested = [
                self._assays[normalize_analyte(name)] for name in _as_names(parameters.get("molecular_assays"))
                if normalize_analyte(name) in self._assays
            ]
            if requested:
                output["molecular_findings"] = dict(requested)
        elif tool == "order_ct_scan":
            output["contrast_used"] = bool(parameters.get("contrast"))
        elif tool == "search_medical_literature":
            output["query"] = str(parameters.get("query", ""))
        elif tool == "check_drug_interactions":
            output["proposed"] = str(parameters.get("drug", ""))
        return OUTPUT_MODELS[tool].model_validate(output)

    def _labs(self, parameters: dict[str, Any]) -> T.LabResults:
        entry = self.tools["interpret_labs"]
        requested = _as_names(parameters.get("panels")) or list(entry.get("default_panels", []))
        panels: dict[str, list[T.LabValue]] = {}
        for name in requested:
            hit = self._analytes.get(normalize_analyte(name))
            if hit is None:
                continue
            panels[name] = [T.LabValue(**row, is_abnormal=False) for row in hit[1]]
        return T.LabResults(panels=panels, interpretation=entry["interpretation"], abnormal_values_summary=[])


@lru_cache(maxsize=2)
def default_library(path: Path = DEFAULT_LIBRARY_PATH) -> FallbackLibrary:
    return FallbackLibrary(path)
