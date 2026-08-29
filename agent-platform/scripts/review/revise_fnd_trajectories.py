"""Rebuild FND SFT traces as a diagnostic-restraint benchmark."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "training_data" / "gold_trajectories" / "trajectories.jsonl"
CASES = ROOT / "data" / "neurobench" / "cases"


def _pair(name: str, args: dict[str, Any], output: dict[str, Any], thought: str) -> list[dict[str, Any]]:
    return [{"role": "assistant", "content": f"<think>\n{thought}\n</think>",
             "tool_calls": [{"type": "function", "function": {"name": name, "arguments": args}}]},
            {"role": "tool", "content": json.dumps(output, indent=2, ensure_ascii=False)}]


def _action(case: dict[str, Any], tool: str) -> dict[str, Any] | None:
    return next((x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == tool), None)


def _output(case: dict[str, Any], tool: str) -> dict[str, Any]:
    key = {"perform_clinical_assessment": "clinical_assessment", "analyze_brain_mri": "mri", "analyze_eeg": "eeg",
           "interpret_labs": "labs", "search_medical_literature": "literature_search", "check_drug_interactions": "drug_interactions"}[tool]
    initial = case["initial_tool_outputs"].get(key)
    if initial is not None: return initial
    for row in case["followup_outputs"]:
        if row.get("tool_name") == tool and row.get("output"): return row["output"]
    raise ValueError(f"{case['case_id']}: missing {tool}")


def _clean_final(text: str, case: dict[str, Any], called: set[str]) -> str:
    markers = {"analyze_brain_mri": ("mri", "imaging"), "analyze_eeg": ("eeg", "video-eeg"), "interpret_labs": ("lab", "blood")}
    lines = []
    for line in text.splitlines():
        low = line.lower()
        if any(x in low for x in ("ecg", "csf", "lumbar puncture", "neuropsych", "echocardi", "holter")): continue
        if any(any(token in low for token in tokens) and tool not in called for tool, tokens in markers.items()): continue
        lines.append(line)
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    primary = case["ground_truth"]["primary_diagnosis"]
    out = re.sub(r"(### Primary Diagnosis\s*\n)[^\n]+", rf"\g<1>{primary}", out, count=1)
    return out or f"### Primary Diagnosis\n{primary}\n\nPositive internally inconsistent neurological signs support this rule-in diagnosis."


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "functional_neurological_disorder": return False
    before = json.dumps(row, sort_keys=True); original = row["messages"]
    differential = row.get("style") == "differential_reasoned"
    messages = [dict(x) for x in original if x.get("role") in {"system", "user"}][:2]
    final = next((x.get("content", "") for x in reversed(original) if x.get("role") == "assistant" and not x.get("tool_calls")), "")
    calls: list[str] = []
    clinical = _action(case, "perform_clinical_assessment"); assert clinical
    messages += _pair("perform_clinical_assessment", {"clinical_context": clinical["action"], "assessment_type": "functional_neuro_signs"},
                      _output(case, "perform_clinical_assessment"),
                      "FND must be ruled in through internally inconsistent or incongruent signs—not inferred from normal tests, psychiatric history or stress. I will perform the positive examination first.")
    calls.append("perform_clinical_assessment")

    if differential:
        for tool, thought in (
            ("analyze_brain_mri", "This case has an explicit acute focal deficit or competing organic neurological disease. Optional MRI addresses that named red flag; a normal scan does not diagnose FND."),
            ("analyze_eeg", "Epilepsy versus functional seizure remains genuinely ambiguous. Optional video-EEG should capture a typical event; a normal interictal EEG alone would be insufficient."),
            ("interpret_labs", "Only the case-specific metabolic, inflammatory, nutritional or treatment-related mimic justifies optional blood testing; there is no routine FND panel."),
        ):
            action = _action(case, tool)
            if not action: continue
            if tool == "analyze_brain_mri": args = {"clinical_context": action["action"], **action["tool_parameters"]}
            elif tool == "analyze_eeg": args = {"clinical_context": action["action"], "eeg_type": "video"}
            else:
                dem = case["patient"]["demographics"]
                args = {"clinical_context": action["action"], "panels": action["tool_parameters"]["panels"],
                        "patient_age": dem["age"], "patient_sex": dem["sex"]}
            messages += _pair(tool, args, _output(case, tool), thought); calls.append(tool)
        for tool in ("search_medical_literature", "check_drug_interactions"):
            action = _action(case, tool)
            if not action: continue
            if tool == "search_medical_literature":
                args = {"query": action.get("tool_parameters", {}).get("query", "positive functional neurological disorder signs treatment"), "max_results": 3}
                thought = "I will check current positive-diagnosis and treatment guidance."
            else:
                args = {"drug": "current and proposed symptom-directed therapy",
                        "current_medications": [str(x.get("drug", x)) if isinstance(x, dict) else str(x) for x in case["patient"]["clinical_history"].get("medications", [])]}
                thought = "Medication review helps avoid iatrogenic treatment escalation, especially unnecessary antiseizure therapy."
            messages += _pair(tool, args, _output(case, tool), thought); calls.append(tool)

    messages.append({"role": "assistant", "content": _clean_final(final, case, set(calls))})
    row["messages"] = messages; row["tools_called"] = list(dict.fromkeys(calls)); row["num_tool_calls"] = len(calls)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", type=Path, default=DEFAULT_INPUT); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("FND-*.json")}; rows = [json.loads(x) for x in args.input.read_text().splitlines() if x.strip()]
    changed = sum(revise(row, cases[row["case_id"]]) for row in rows if row.get("condition") == "functional_neurological_disorder")
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows); print(f"FND trajectories changed: {changed}")
    if args.check and changed: raise SystemExit(1)
    if not args.check: args.input.write_text(rendered)


if __name__ == "__main__": main()
