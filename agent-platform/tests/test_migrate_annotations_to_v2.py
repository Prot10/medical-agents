"""The v1 -> v2 annotation migration moves each tag to the field holding the same content, and nothing else."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "review" / "migrate_annotations_to_v2.py"
spec = importlib.util.spec_from_file_location("migrate_annotations_to_v2", SCRIPT)
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)

CASE = "TEST-M01"
EEG = {"tool_name": "analyze_eeg", "tool_parameters": {}, "rationale": "no seizures"}
OLD = {
    "case_id": CASE,
    "followup_outputs": [{"tool_name": "analyze_csf"}],
    "ground_truth": {
        "primary_diagnosis": "Bacterial meningitis",
        "optimal_actions": [
            {"action": "Take a history", "tool_name": None},
            {"action": "Perform an LP", "tool_name": "analyze_csf"},
        ],
        "critical_actions": ["Give dexamethasone with the first antibiotic"],
        "contraindicated_actions": ["Do not delay antibiotics for imaging"],
        "key_reasoning_points": ["Fever, neck stiffness and confusion"],
        "useless_tools": [EEG],
        "harmful_tools": [],
        "sequence_constraints": [{"before": "order_ct_scan", "after": "analyze_csf", "reason": "CT first"}],
    },
}
NEW = {
    "case_id": CASE,
    "followup_outputs": [{"tool_name": "analyze_csf"}],
    "ground_truth": {
        "diagnosis": {"accepted": ["Bacterial meningitis", "meningitis"], "icd_codes": []},
        "action_criteria": [{"criterion_id": "action-2", "label": "Perform an LP"}],
        "avoided_actions": [
            {
                "severity": "waste",
                "rationale": "no seizures",
                "alternatives": [{"tool_name": "analyze_eeg", "required_arguments": {}}],
            }
        ],
        "sequence_constraints": [
            {"before_criterion_id": "action-5", "after_criterion_id": "action-2", "reason": "CT first"}
        ],
        "assessment": {
            "required_recommendations": ["Give dexamethasone with the first antibiotic"],
            "prohibited_recommendations": ["Do not delay antibiotics for imaging"],
        },
        "key_clinical_evidence": ["Fever, neck stiffness and confusion"],
    },
}


@pytest.mark.parametrize(
    ("old_path", "new_path"),
    [
        ("followup_outputs[0]", "followup_outputs[0]"),
        ("ground_truth.primary_diagnosis", "ground_truth.diagnosis"),
        ("ground_truth.optimal_actions[1]", "ground_truth.action_criteria[0]"),
        ("ground_truth.critical_actions[0]", "ground_truth.assessment.required_recommendations[0]"),
        ("ground_truth.contraindicated_actions[0]", "ground_truth.assessment.prohibited_recommendations[0]"),
        ("ground_truth.key_reasoning_points[0]", "ground_truth.key_clinical_evidence[0]"),
        ("ground_truth.useless_tools[0]", "ground_truth.avoided_actions[0]"),
        ("ground_truth.sequence_constraints[0]", "ground_truth.sequence_constraints[0]"),
        ("ground_truth.action_criteria[0]", "ground_truth.action_criteria[0]"),
    ],
)
def test_each_v1_field_resolves_to_the_v2_field_with_its_content(old_path, new_path):
    assert migration.resolve(OLD, NEW, old_path)[0] == new_path


def test_a_step_with_no_v2_counterpart_is_left_where_it_is():
    target, reason = migration.resolve(OLD, NEW, "ground_truth.optimal_actions[0]")
    assert target is None and "no unique v2 field" in reason


def _tree(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    annotations, old_cases, new_cases = tmp_path / "annotations", tmp_path / "v1", tmp_path / "v2"
    for root, case in ((old_cases, OLD), (new_cases, NEW)):
        root.mkdir()
        (root / f"{CASE}.json").write_text(json.dumps(case))
    review = annotations / "neurobench" / "NB-TEST-REVW-AAAA" / f"{CASE}.json"
    review.parent.mkdir(parents=True)
    stamp = "2026-10-01T10:00:00Z"
    review.write_text(
        json.dumps(
            {
                "case_id": CASE,
                "status": "needs_changes",
                "field_annotations": [
                    {"id": "a", "field_path": "ground_truth.critical_actions[0]", "comment": "x",
                     "severity": "error", "created_at": stamp, "updated_at": stamp, "resolved": False},
                    {"id": "b", "field_path": "ground_truth.optimal_actions[0]", "comment": "y",
                     "severity": "note", "created_at": stamp, "updated_at": stamp, "resolved": True},
                ],
                "case_comments": [{"id": "c", "comment": "z"}],
            },
            indent=2,
        )
    )
    return annotations, old_cases, new_cases, review


def test_dry_run_reports_and_writes_nothing(tmp_path):
    annotations, old_cases, new_cases, review = _tree(tmp_path)
    before = review.read_text()
    report = migration.migrate(annotations, old_cases, new_cases, apply=False)
    assert report["outcome"] == {"moved": 1, "unresolved": 1}
    assert review.read_text() == before


def test_apply_changes_only_field_path_and_is_idempotent(tmp_path):
    annotations, old_cases, new_cases, review = _tree(tmp_path)
    before = json.loads(review.read_text())
    migration.migrate(annotations, old_cases, new_cases, apply=True)
    after = json.loads(review.read_text())
    before["field_annotations"][0]["field_path"] = "ground_truth.assessment.required_recommendations[0]"
    assert after == before
    again = migration.migrate(annotations, old_cases, new_cases, apply=True)
    assert again["changes"] == [] and json.loads(review.read_text()) == before
