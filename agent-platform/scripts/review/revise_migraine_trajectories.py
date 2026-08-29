"""Rebuild migraine SFT traces around clinical diagnosis and selected red flags."""

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
    return [
        {"role": "assistant", "content": f"<think>\n{thought}\n</think>",
         "tool_calls": [{"type": "function", "function": {"name": name, "arguments": args}}]},
        {"role": "tool", "content": json.dumps(output, indent=2, ensure_ascii=False)},
    ]


def _actions(case: dict[str, Any], tool: str) -> list[dict[str, Any]]:
    return [x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == tool]


def _output(case: dict[str, Any], tool: str, discriminator: str | None = None) -> dict[str, Any]:
    key = {"perform_clinical_assessment": "clinical_assessment", "analyze_brain_mri": "mri", "analyze_eeg": "eeg",
           "interpret_labs": "labs", "order_echocardiogram": "echo", "order_cardiac_monitoring": "cardiac_monitoring",
           "order_advanced_imaging": "advanced_imaging", "order_specialized_test": "specialized_test",
           "search_medical_literature": "literature_search", "check_drug_interactions": "drug_interactions"}.get(tool)
    initial = case["initial_tool_outputs"].get(key) if key else None
    if initial is not None and (not discriminator or discriminator in json.dumps(initial)):
        return initial
    for row in case["followup_outputs"]:
        if row.get("tool_name") != tool or not row.get("output"):
            continue
        if discriminator and discriminator not in json.dumps(row["output"]):
            continue
        return row["output"]
    raise ValueError(f"{case['case_id']}: missing {tool} {discriminator or ''}")


def _clean_final(text: str, case: dict[str, Any], called: set[str]) -> str:
    lines = []
    markers = {"analyze_brain_mri": ("mri", "imaging"), "analyze_eeg": ("eeg",), "interpret_labs": ("lab",),
               "order_echocardiogram": ("echocardi", "bubble"), "order_cardiac_monitoring": ("holter", "loop recorder", "cardiac monitor"),
               "order_advanced_imaging": ("spectroscopy",), "order_specialized_test": ("notch3", "neuropsych")}
    for line in text.splitlines():
        low = line.lower()
        if "ecg" in low or "lumbar puncture" in low or "csf" in low:
            continue
        if any(any(token in low for token in tokens) and tool not in called for tool, tokens in markers.items()):
            continue
        lines.append(line)
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    primary = case["ground_truth"]["primary_diagnosis"]
    out = re.sub(r"(### Primary Diagnosis\s*\n)[^\n]+", rf"\g<1>{primary}", out, count=1)
    return out or f"### Primary Diagnosis\n{primary}\n\nThe structured ICHD-3 assessment and targeted red-flag work-up support this conclusion."


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "migraine_with_aura": return False
    before = json.dumps(row, sort_keys=True); original = row["messages"]
    differential = row.get("style") == "differential_reasoned"
    messages = [dict(x) for x in original if x.get("role") in {"system", "user"}][:2]
    final = next((x.get("content", "") for x in reversed(original) if x.get("role") == "assistant" and not x.get("tool_calls")), "")
    calls: list[str] = []

    clinical = _actions(case, "perform_clinical_assessment")[0]
    messages += _pair("perform_clinical_assessment",
                      {"clinical_context": clinical["action"], "assessment_type": "structured_headache_history_ichd3"},
                      _output(case, "perform_clinical_assessment"),
                      "Migraine with aura is diagnosed clinically. I must first document reversibility, the six ICHD-3 temporal/phenomenological characteristics, neurological examination and red flags before deciding whether any test is justified.")
    calls.append("perform_clinical_assessment")

    mri = _actions(case, "analyze_brain_mri")
    if mri:
        action = mri[0]
        if action["category"] in {"required", "recommended"} or differential:
            messages += _pair("analyze_brain_mri", {"clinical_context": action["action"], **action["tool_parameters"]},
                              _output(case, "analyze_brain_mri"),
                              "The history contains a documented atypical feature or secondary diagnosis. MRI answers that red-flag question; it is not being ordered to confirm migraine or provide reassurance.")
            calls.append("analyze_brain_mri")

    eeg = _actions(case, "analyze_eeg")
    if eeg:
        messages += _pair("analyze_eeg", {"clinical_context": eeg[0]["action"], "eeg_type": "video"},
                          _output(case, "analyze_eeg"),
                          "A convulsive event was witnessed, so video-EEG evaluates the seizure component. This is the sole seizure exception and not routine headache testing.")
        calls.append("analyze_eeg")

    labs = _actions(case, "interpret_labs")
    if labs and (labs[0]["category"] == "recommended" or differential):
        dem = case["patient"]["demographics"]
        messages += _pair("interpret_labs", {"clinical_context": labs[0]["action"], "panels": labs[0]["tool_parameters"]["panels"],
                                             "patient_age": dem["age"], "patient_sex": dem["sex"]},
                          _output(case, "interpret_labs"),
                          "These tests target a specific arteritic, vascular, mitochondrial or seizure mimic. No fixed blood panel diagnoses migraine.")
        calls.append("interpret_labs")

    monitor = _actions(case, "order_cardiac_monitoring")
    if monitor:
        kind = monitor[0].get("tool_parameters", {}).get("monitor_type", "event_monitor_30d")
        messages += _pair("order_cardiac_monitoring", {"clinical_context": monitor[0]["action"], "monitor_type": kind},
                          _output(case, "order_cardiac_monitoring"),
                          "This is an infarct/atrial-fibrillation mechanism question, not a migraine test. Rhythm correlation can distinguish an embolic stroke or independent AF from aura.")
        calls.append("order_cardiac_monitoring")

    echo = _actions(case, "order_echocardiogram")
    if echo:
        old = echo[0].get("tool_parameters", {}); kind = old.get("echo_type", "TTE")
        messages += _pair("order_echocardiogram", {"clinical_context": echo[0]["action"], "echo_type": kind},
                          _output(case, "order_echocardiogram"),
                          "The retained echocardiogram addresses an embolic-source or MELAS cardiomyopathy question. Routine migraine cases have no echo action or result.")
        calls.append("order_echocardiogram")

    advanced = _actions(case, "order_advanced_imaging")
    if advanced and differential:
        action = advanced[0]
        messages += _pair("order_advanced_imaging", {"clinical_context": action["action"], "modality": action["tool_parameters"]["modality"]},
                          _output(case, "order_advanced_imaging"),
                          "MR spectroscopy is a targeted mitochondrial-disease study here; it has no routine role in migraine with aura.")
        calls.append("order_advanced_imaging")

    specialized = _actions(case, "order_specialized_test")
    if specialized:
        # One call per trace: always cover required CADASIL genetics; the second style
        # can instead demonstrate the recommended cognitive baseline when present.
        action = next((x for x in specialized if x["category"] == "required"), specialized[0])
        if differential:
            action = next((x for x in specialized if x["category"] == "recommended"), action)
        test_type = action["tool_parameters"]["test_type"]
        output_type = ("genetic_panel" if test_type.startswith("genetic_panel") else
                       "neuropsychological_assessment" if test_type == "neuropsych_battery" else test_type)
        messages += _pair("order_specialized_test", {"clinical_context": action["action"], "test_type": test_type},
                          _output(case, "order_specialized_test", output_type),
                          "This family-history/secondary-diagnosis question justifies targeted CADASIL genetics or a cognitive baseline; it is not a routine migraine panel.")
        calls.append("order_specialized_test")

    for tool in ("search_medical_literature", "check_drug_interactions"):
        actions = _actions(case, tool)
        if not actions: continue
        action = actions[0]
        if action.get("category") not in {"required", "recommended"}: continue
        if tool == "search_medical_literature":
            args = {"query": action.get("tool_parameters", {}).get("query", "ICHD-3 migraine with aura criteria"), "max_results": 3}
            thought = "I will verify the exact current classification or management question."
        else:
            args = {"drug": "proposed migraine treatment", "current_medications": [str(x.get("drug", x)) if isinstance(x, dict) else str(x) for x in case["patient"]["clinical_history"].get("medications", [])]}
            thought = "Before recommending acute or preventive therapy, I need patient-specific contraindications and interactions."
        messages += _pair(tool, args, _output(case, tool), thought); calls.append(tool)

    messages.append({"role": "assistant", "content": _clean_final(final, case, set(calls))})
    row["messages"] = messages; row["tools_called"] = list(dict.fromkeys(calls)); row["num_tool_calls"] = len(calls)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", type=Path, default=DEFAULT_INPUT); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("MIG-AURA-*.json")}; rows = [json.loads(x) for x in args.input.read_text().splitlines() if x.strip()]
    changed = sum(revise(row, cases[row["case_id"]]) for row in rows if row.get("condition") == "migraine_with_aura")
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows); print(f"Migraine trajectories changed: {changed}")
    if args.check and changed: raise SystemExit(1)
    if not args.check: args.input.write_text(rendered)


if __name__ == "__main__": main()
