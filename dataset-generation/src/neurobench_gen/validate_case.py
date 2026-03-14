"""Validate a generated NeuroBench case JSON file against Pydantic schemas.

Usage:
    python validate_case.py <json_file> [--strict]

Returns exit code 0 if valid, 1 if invalid.
Prints validation errors to stderr.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import ValidationError

from neuroagent_schemas.case import NeuroBenchCase


def validate_json_file(json_path: str | Path, strict: bool = False) -> tuple[bool, list[str]]:
    """Validate a case JSON file.

    Returns (is_valid, list_of_issues).
    """
    path = Path(json_path)
    issues: list[str] = []

    # Check file exists and is valid JSON
    if not path.exists():
        return False, [f"File not found: {path}"]

    try:
        with open(path) as f:
            raw = f.read()
    except Exception as e:
        return False, [f"Cannot read file: {e}"]

    # Try to parse JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    if not isinstance(data, dict):
        return False, [f"Expected JSON object, got {type(data).__name__}"]

    # Validate against Pydantic schema
    try:
        case = NeuroBenchCase.model_validate(data)
    except ValidationError as e:
        for err in e.errors():
            loc = " → ".join(str(x) for x in err["loc"])
            issues.append(f"[{loc}] {err['msg']}")
        return False, issues

    # Rule-based clinical plausibility checks
    issues.extend(_check_clinical_plausibility(case))

    # Completeness checks
    issues.extend(_check_completeness(case))

    if strict and issues:
        return False, issues

    # In non-strict mode, only Pydantic validation failures count as invalid
    return True, issues


def _check_clinical_plausibility(case: NeuroBenchCase) -> list[str]:
    """Rule-based checks for physiological plausibility."""
    issues = []
    v = case.patient.vitals

    # Vital signs ranges
    if not (60 <= v.bp_systolic <= 220):
        issues.append(f"WARNING: BP systolic {v.bp_systolic} outside 60-220 range")
    if not (30 <= v.bp_diastolic <= 140):
        issues.append(f"WARNING: BP diastolic {v.bp_diastolic} outside 30-140 range")
    if v.bp_diastolic >= v.bp_systolic:
        issues.append(f"WARNING: Diastolic ({v.bp_diastolic}) >= Systolic ({v.bp_systolic})")
    if not (30 <= v.hr <= 200):
        issues.append(f"WARNING: Heart rate {v.hr} outside 30-200 range")
    if not (35.0 <= v.temp <= 42.0):
        issues.append(f"WARNING: Temperature {v.temp} outside 35.0-42.0 range")
    if not (8 <= v.rr <= 40):
        issues.append(f"WARNING: Respiratory rate {v.rr} outside 8-40 range")
    if not (70 <= v.spo2 <= 100):
        issues.append(f"WARNING: SpO2 {v.spo2} outside 70-100 range")

    # Age check
    age = case.patient.demographics.age
    if not (18 <= age <= 90):
        issues.append(f"WARNING: Age {age} outside 18-90 range")

    # History of present illness should have some substance
    hpi = case.patient.history_present_illness
    if len(hpi.split()) < 50:
        issues.append(f"WARNING: HPI too short ({len(hpi.split())} words, expected 50+)")

    return issues


def _check_completeness(case: NeuroBenchCase) -> list[str]:
    """Check that required fields are populated."""
    issues = []

    # Ground truth checks
    gt = case.ground_truth
    if not gt.primary_diagnosis:
        issues.append("WARNING: Missing primary_diagnosis in ground_truth")
    if not gt.icd_code:
        issues.append("WARNING: Missing icd_code in ground_truth")
    if len(gt.differential) < 2:
        issues.append(f"WARNING: Only {len(gt.differential)} differential diagnoses (expected 3+)")
    if len(gt.optimal_actions) < 3:
        issues.append(f"WARNING: Only {len(gt.optimal_actions)} optimal actions (expected 3+)")
    if not gt.critical_actions:
        issues.append("WARNING: No critical_actions defined")
    if not gt.key_reasoning_points:
        issues.append("WARNING: No key_reasoning_points defined")

    # Follow-up outputs
    if len(case.followup_outputs) < 5:
        issues.append(f"WARNING: Only {len(case.followup_outputs)} follow-up outputs (expected 5+)")

    # Check that at least some tool outputs exist
    tos = case.initial_tool_outputs
    has_any = any([tos.eeg, tos.mri, tos.ecg, tos.labs, tos.csf])
    if not has_any:
        issues.append("WARNING: No tool outputs generated at all")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_case.py <json_file> [--strict]")
        sys.exit(1)

    json_path = sys.argv[1]
    strict = "--strict" in sys.argv

    is_valid, issues = validate_json_file(json_path, strict=strict)

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)

    if is_valid:
        print(f"VALID: {json_path}")
        sys.exit(0)
    else:
        print(f"INVALID: {json_path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
