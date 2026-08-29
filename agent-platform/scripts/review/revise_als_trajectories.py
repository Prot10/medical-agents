"""Rebuild ALS SFT traces around EMG, mimic exclusion and selected optional tests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "training_data" / "gold_trajectories" / "trajectories.jsonl"
CASES = ROOT / "data" / "neurobench" / "cases"
GENETICS_TRACE_CASES = {"ALS-P02", "ALS-P03", "ALS-P05", "ALS-P08", "ALS-P09", "ALS-S07", "ALS-S10"}
RESPIRATORY_TRACE_CASES = {"ALS-M01", "ALS-M03", "ALS-RS11", "ALS-S02", "ALS-S04", "ALS-S09"}


def _pair(name: str, args: dict[str, Any], output: dict[str, Any], thought: str) -> list[dict[str, Any]]:
    return [{"role": "assistant", "content": f"<think>\n{thought}\n</think>",
             "tool_calls": [{"type": "function", "function": {"name": name, "arguments": args}}]},
            {"role": "tool", "content": json.dumps(output, indent=2, ensure_ascii=False)}]


def _actions(case: dict[str, Any], tool: str) -> list[dict[str, Any]]:
    return [x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == tool]


def _output(case: dict[str, Any], tool: str, test_type: str | None = None) -> dict[str, Any]:
    key = {"analyze_brain_mri": "mri", "order_body_imaging": "body_imaging", "interpret_labs": "labs",
           "analyze_csf": "csf", "order_specialized_test": "specialized_test",
           "search_medical_literature": "literature_search", "check_drug_interactions": "drug_interactions"}.get(tool)
    initial = case["initial_tool_outputs"].get(key) if key else None
    if initial is not None and (not test_type or initial.get("test_type") == test_type): return initial
    for row in case["followup_outputs"]:
        out = row.get("output") or {}
        if row.get("tool_name") == tool and (not test_type or out.get("test_type") == test_type): return out
    raise ValueError(f"{case['case_id']}: missing {tool} {test_type or ''}")


def _clean_final(text: str, case: dict[str, Any], called: set[str], specialty: str) -> str:
    lines = []
    for line in text.splitlines():
        low = line.lower()
        if any(x in low for x in ("eeg", "ecg", "autonomic", "tilt table", "biopsy")): continue
        if ("csf" in low or "lumbar puncture" in low) and "analyze_csf" not in called: continue
        if ("genetic" in low or "c9orf72" in low or "sod1" in low) and specialty != "genetic_panel:ALS": continue
        if ("fvc" in low or "snip" in low or "respiratory function" in low) and specialty != "respiratory_function": continue
        lines.append(line)
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    primary = case["ground_truth"]["primary_diagnosis"]
    out = re.sub(r"(### Primary Diagnosis\s*\n)[^\n]+", rf"\g<1>{primary}", out, count=1)
    return out or f"### Primary Diagnosis\n{primary}\n\nThe clinical pattern, EMG pathway and exclusion of treatable mimics support this assessment."


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "als": return False
    before = json.dumps(row, sort_keys=True); original = row["messages"]
    differential = row.get("style") == "differential_reasoned"; cid = case["case_id"]
    messages = [dict(x) for x in original if x.get("role") in {"system", "user"}][:2]
    final = next((x.get("content", "") for x in reversed(original) if x.get("role") == "assistant" and not x.get("tool_calls")), "")
    calls: list[str] = []

    mri = _actions(case, "analyze_brain_mri")[0]
    messages += _pair("analyze_brain_mri", {"clinical_context": mri["action"], **mri["tool_parameters"]}, _output(case, "analyze_brain_mri"),
                      "ALS is not confirmed by MRI, but brain imaging is required here to exclude a better structural, brainstem, inflammatory or neoplastic explanation.")
    calls.append("analyze_brain_mri")
    spine = _actions(case, "order_body_imaging")[0]
    messages += _pair("order_body_imaging", {"clinical_context": spine["action"], **spine["tool_parameters"]}, _output(case, "order_body_imaging"),
                      "Cord imaging must be a separate order. Cervical myelopathy or another compressive/inflammatory cord lesion can mimic mixed motor-neuron signs.")
    calls.append("order_body_imaging")
    labs = _actions(case, "interpret_labs")[0]; dem = case["patient"]["demographics"]
    messages += _pair("interpret_labs", {"clinical_context": labs["action"], "panels": labs["tool_parameters"]["panels"],
                                         "patient_age": dem["age"], "patient_sex": dem["sex"]}, _output(case, "interpret_labs"),
                      "Blood tests exclude treatable mimics and do not confirm ALS. I will use the baseline panel plus only the phenotype-specific additions named for this case.")
    calls.append("interpret_labs")

    specialty = "emg_ncs"
    if differential and cid in GENETICS_TRACE_CASES: specialty = "genetic_panel:ALS"
    elif differential and cid in RESPIRATORY_TRACE_CASES: specialty = "respiratory_function"
    action = next(x for x in _actions(case, "order_specialized_test") if x["tool_parameters"]["test_type"] == specialty)
    thought = {
        "emg_ncs": "EMG/NCS is the required ALS-specific study: sample multiple body regions, look for active/chronic denervation, preserved sensory responses and absence of conduction block.",
        "respiratory_function": "Bulbar or respiratory features make the recommended FVC/SNIP safety baseline immediately relevant. It stages respiratory risk but does not confirm ALS.",
        "genetic_panel:ALS": "After pre-test counselling, this familial, young-onset, ALS-FTD or gene-therapy context justifies taking up the optional ALS panel offer.",
    }[specialty]
    messages += _pair("order_specialized_test", {"clinical_context": action["action"], "test_type": specialty},
                      _output(case, "order_specialized_test", specialty), thought)
    calls.append("order_specialized_test")

    csf = _actions(case, "analyze_csf")
    if differential and csf:
        action = csf[0]
        messages += _pair("analyze_csf", {"clinical_context": action["action"], "special_tests": action["tool_parameters"]["special_tests"]},
                          _output(case, "analyze_csf"),
                          "This atypical case raises a named inflammatory, infectious or neoplastic mimic. CSF is optional and targeted; routine CSF or neurofilament testing does not diagnose ALS.")
        calls.append("analyze_csf")

    if differential:
        for tool in ("search_medical_literature", "check_drug_interactions"):
            actions = _actions(case, tool)
            if not actions: continue
            action = actions[0]
            if tool == "search_medical_literature":
                args = {"query": action.get("tool_parameters", {}).get("query", "Gold Coast ALS diagnostic criteria EAN 2024"), "max_results": 3}
                thought = "I will verify the applicable ALS criteria or management evidence."
            else:
                args = {"drug": "proposed ALS disease-modifying and symptom therapy",
                        "current_medications": [str(x.get("drug", x)) if isinstance(x, dict) else str(x) for x in case["patient"]["clinical_history"].get("medications", [])]}
                thought = "Before recommending ALS treatment, I need the patient-specific interaction and contraindication check."
            messages += _pair(tool, args, _output(case, tool), thought); calls.append(tool)

    messages.append({"role": "assistant", "content": _clean_final(final, case, set(calls), specialty)})
    row["messages"] = messages; row["tools_called"] = list(dict.fromkeys(calls)); row["num_tool_calls"] = len(calls)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", type=Path, default=DEFAULT_INPUT); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("ALS-*.json")}; rows = [json.loads(x) for x in args.input.read_text().splitlines() if x.strip()]
    changed = sum(revise(row, cases[row["case_id"]]) for row in rows if row.get("condition") == "als")
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows); print(f"ALS trajectories changed: {changed}")
    if args.check and changed: raise SystemExit(1)
    if not args.check: args.input.write_text(rendered)


if __name__ == "__main__": main()
