#!/usr/bin/env python3
"""Integration test: simulate a complete agent run on v4 cases using mock tool outputs.

Tests the full pipeline: case loading → tool registry → mock server → cost tracking
→ metrics computation → evaluation. Runs across all 10 conditions with representative
tool call sequences that a real model would produce.

Usage:
    uv run python agent-platform/scripts/test_v4_integration.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from neuroagent_schemas import NeuroBenchCase
from neuroagent.tools.base import ToolCall
from neuroagent.tools.cost_tracker import CostTracker
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry
from neuroagent.agent.reasoning import AgentTrace
from neuroagent.evaluation.metrics import MetricsCalculator

V4_DIR = Path("data/neurobench_v4/cases")

# Simulated agent behavior per condition — realistic tool call sequences
# Each entry: (tool_name, params_dict)
WORKUPS: dict[str, list[tuple[str, dict]]] = {
    "ALZ-EARLY": [
        ("interpret_labs", {"clinical_context": "Dementia screen", "panels": ["CBC", "BMP", "thyroid", "B12", "folate", "RPR", "HIV"]}),
        ("analyze_brain_mri", {"clinical_context": "Evaluate atrophy", "protocol": "dementia", "contrast": False}),
        ("order_specialized_test", {"clinical_context": "Cognitive profiling", "test_type": "neuropsych_battery"}),
        ("check_drug_interactions", {"drug": "donepezil"}),
    ],
    "FEPI-TEMP": [
        ("interpret_labs", {"clinical_context": "Seizure workup", "panels": ["CBC", "BMP", "drug_screen", "prolactin"]}),
        ("analyze_ecg", {"clinical_context": "Cardiac screen"}),
        ("analyze_eeg", {"clinical_context": "Seizure localization", "eeg_type": "routine"}),
        ("analyze_brain_mri", {"clinical_context": "Structural etiology", "protocol": "epilepsy", "contrast": True}),
        ("check_drug_interactions", {"drug": "levetiracetam"}),
    ],
    "ISCH-STR": [
        ("order_ct_scan", {"clinical_context": "Acute stroke, hemorrhage exclusion", "angiography": True}),
        ("analyze_brain_mri", {"clinical_context": "Ischemic stroke", "protocol": "stroke", "contrast": False}),
        ("interpret_labs", {"clinical_context": "Stroke workup", "panels": ["CBC", "BMP", "coagulation", "troponin", "lipid", "HbA1c"]}),
        ("analyze_ecg", {"clinical_context": "Cardioembolic source"}),
        ("order_echocardiogram", {"clinical_context": "Stroke - cardioembolic", "echo_type": "TTE"}),
        ("order_cardiac_monitoring", {"clinical_context": "AFib screening", "monitor_type": "holter_24h"}),
    ],
    "MS-RR": [
        ("interpret_labs", {"clinical_context": "MS workup", "panels": ["CBC", "BMP", "inflammatory_markers", "B12"]}),
        ("analyze_brain_mri", {"clinical_context": "Demyelination", "protocol": "ms", "contrast": True}),
        ("analyze_csf", {"clinical_context": "Intrathecal synthesis", "special_tests": ["oligoclonal_bands", "IgG_index"]}),
        ("order_specialized_test", {"clinical_context": "Visual pathway", "test_type": "vep"}),
        ("check_drug_interactions", {"drug": "dimethyl_fumarate"}),
    ],
    "PD": [
        ("interpret_labs", {"clinical_context": "PD screen", "panels": ["CBC", "BMP", "thyroid", "ceruloplasmin"]}),
        ("analyze_brain_mri", {"clinical_context": "Rule out atypical PD", "protocol": "standard", "contrast": False}),
        ("order_advanced_imaging", {"clinical_context": "Confirm dopaminergic deficit", "imaging_type": "DaTscan"}),
        ("check_drug_interactions", {"drug": "carbidopa-levodopa"}),
    ],
    "SYNC-CARD": [
        ("analyze_ecg", {"clinical_context": "Syncope - arrhythmia"}),
        ("interpret_labs", {"clinical_context": "Syncope workup", "panels": ["CBC", "BMP", "troponin"]}),
        ("order_echocardiogram", {"clinical_context": "Structural cardiac disease", "echo_type": "TTE"}),
        ("order_cardiac_monitoring", {"clinical_context": "Arrhythmia capture", "monitor_type": "holter_24h"}),
    ],
    "GLIO-HG": [
        ("order_ct_scan", {"clinical_context": "Acute presentation, mass effect", "contrast": True}),
        ("analyze_brain_mri", {"clinical_context": "Tumor characterization", "protocol": "tumor", "contrast": True}),
        ("interpret_labs", {"clinical_context": "Pre-surgical", "panels": ["CBC", "BMP", "coagulation"]}),
        ("order_advanced_imaging", {"clinical_context": "Tumor grading", "imaging_type": "perfusion_MRI"}),
    ],
    "FND": [
        ("interpret_labs", {"clinical_context": "Rule out organic", "panels": ["CBC", "BMP", "thyroid", "inflammatory_markers"]}),
        ("analyze_brain_mri", {"clinical_context": "Rule out structural", "protocol": "standard", "contrast": False}),
        ("analyze_eeg", {"clinical_context": "Rule out epilepsy", "eeg_type": "routine"}),
    ],
    "NMDAR-ENC": [
        ("analyze_eeg", {"clinical_context": "Encephalitis pattern", "eeg_type": "continuous_icu"}),
        ("analyze_brain_mri", {"clinical_context": "Limbic involvement", "protocol": "standard", "contrast": True}),
        ("interpret_labs", {"clinical_context": "Autoimmune workup", "panels": ["CBC", "BMP", "inflammatory_markers", "autoimmune_encephalitis"]}),
        ("analyze_csf", {"clinical_context": "Intrathecal antibodies", "special_tests": ["autoimmune_panel", "HSV_PCR"]}),
    ],
    "MENING": [
        ("order_ct_scan", {"clinical_context": "Rule out mass before LP"}),
        ("interpret_labs", {"clinical_context": "Sepsis screen", "panels": ["CBC", "BMP", "coagulation", "CRP"]}),
        ("analyze_csf", {"clinical_context": "Meningitis", "special_tests": ["meningitis_panel"]}),
        ("analyze_brain_mri", {"clinical_context": "Complications", "protocol": "standard", "contrast": True}),
    ],
}


def find_case(prefix: str) -> NeuroBenchCase | None:
    """Find first v4 case matching a condition prefix."""
    for path in sorted(V4_DIR.glob(f"{prefix}*.json")):
        return NeuroBenchCase(**json.loads(path.read_text()))
    return None


def simulate_run(case: NeuroBenchCase, workup: list[tuple[str, dict]]) -> dict:
    """Simulate an agent run on a case with a predetermined tool sequence."""
    mock = MockServer(case)
    registry = ToolRegistry.create_default_registry(mock_server=mock)
    tracker = CostTracker()

    trace = AgentTrace(case_id=case.case_id)
    trace.start_timer()

    results = []
    for tool_name, params in workup:
        tc = ToolCall(tool_name=tool_name, parameters=params)
        result = registry.execute(tc)
        cost_entry = tracker.compute_cost(tool_name, params)
        result.cost_usd = cost_entry.cost_usd

        trace.add_tool_turn(
            turn_number=len(trace.turns) + 1,
            tool_name=tool_name,
            tool_result=result.model_dump(),
        )

        results.append({
            "tool": tool_name,
            "success": result.success,
            "cost": cost_entry.cost_usd,
            "breakdown": cost_entry.cost_breakdown,
        })

    # Set fake final response
    trace.set_final_response(
        f"### Primary Diagnosis\n{case.ground_truth.primary_diagnosis} (Confidence: 0.85)\n\n"
        "### Differential Diagnoses\n1. Alternative\n\n"
        "### Key Evidence\n- Finding from tool\n\n"
        "### Recommendations\n1. Treatment\n\n"
        "### Red Flags\n- None"
    )
    trace.total_cost_usd = tracker.total_cost_usd
    trace.cost_entries = [e.model_dump() for e in tracker.entries]

    # Compute metrics
    calc = MetricsCalculator()
    metrics = calc.compute_all(trace, case.ground_truth)

    return {
        "case_id": case.case_id,
        "condition": case.condition.value,
        "tool_calls": results,
        "total_cost": tracker.total_cost_usd,
        "optimal_cost": metrics.optimal_cost_usd,
        "cost_efficiency": metrics.cost_efficiency,
        "top1_accuracy": metrics.diagnostic_accuracy_top1,
        "action_recall": metrics.action_recall,
        "action_precision": metrics.action_precision,
        "critical_hit": metrics.critical_actions_hit,
        "safety": metrics.safety_score,
        "all_tools_returned_data": all(r["success"] for r in results),
    }


def main():
    if not V4_DIR.exists():
        print(f"ERROR: v4 dataset not found at {V4_DIR}", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print("V4 INTEGRATION TEST — Simulated Agent Runs Across Conditions")
    print("=" * 80)
    print()

    all_ok = True
    total_tests = 0
    passed = 0

    for condition_prefix, workup in WORKUPS.items():
        case = find_case(condition_prefix)
        if case is None:
            print(f"  SKIP: No v4 case found for {condition_prefix}")
            continue

        result = simulate_run(case, workup)
        total_tests += 1

        # Determine pass/fail
        issues = []
        if not result["all_tools_returned_data"]:
            failed_tools = [r["tool"] for r in result["tool_calls"] if not r["success"]]
            issues.append(f"tools failed: {failed_tools}")
        if result["total_cost"] <= 0:
            issues.append("total cost is zero")
        if result["optimal_cost"] <= 0:
            issues.append("optimal cost is zero")

        status = "PASS" if not issues else "FAIL"
        if issues:
            all_ok = False
        else:
            passed += 1

        # Print result
        print(f"[{status}] {result['case_id']} ({result['condition']})")
        print(f"       Tools: {len(result['tool_calls'])} calls, "
              f"all returned data: {result['all_tools_returned_data']}")
        print(f"       Cost:  ${result['total_cost']:,.0f} actual / "
              f"${result['optimal_cost']:,.0f} optimal → "
              f"efficiency={result['cost_efficiency']:.2f}")
        print(f"       Diagnosis: top1={result['top1_accuracy']}, "
              f"recall={result['action_recall']:.2f}, "
              f"precision={result['action_precision']:.2f}, "
              f"critical={result['critical_hit']:.2f}")

        # Show per-tool breakdown
        for tc in result["tool_calls"]:
            status_char = "✓" if tc["success"] else "✗"
            print(f"         {status_char} {tc['tool']:30s}  ${tc['cost']:>8,.0f}  {tc['breakdown']}")

        if issues:
            for issue in issues:
                print(f"       ⚠ {issue}")
        print()

    print("=" * 80)
    print(f"RESULTS: {passed}/{total_tests} conditions passed")
    if all_ok:
        print("All integration tests PASSED")
    else:
        print("Some tests FAILED — check output above")
        sys.exit(1)


if __name__ == "__main__":
    main()
