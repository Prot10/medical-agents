"""Rebuild acute-stroke traces so optional imaging never precedes reperfusion imaging."""

from __future__ import annotations

import argparse
import json
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
    if tool == "order_ct_scan":
        if discriminator == "cta":
            return next(x["output"] for x in case["followup_outputs"] if x.get("trigger_action") == "request_ct_angiography")
        return case["initial_tool_outputs"]["ct"]
    if tool == "order_advanced_imaging":
        return next(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool)
    key = {
        "interpret_labs": "labs", "analyze_ecg": "ecg", "analyze_brain_mri": "mri",
        "analyze_eeg": "eeg", "order_echocardiogram": "echo",
        "order_cardiac_monitoring": "cardiac_monitoring",
        "search_medical_literature": "literature_search", "check_drug_interactions": "drug_interactions",
    }[tool]
    initial = case["initial_tool_outputs"].get(key)
    if initial:
        if tool in {"search_medical_literature", "check_drug_interactions"} and "query" not in initial and "proposed" not in initial:
            return next(iter(initial.values()))
        return initial
    return next(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool)


def _has_output(case: dict[str, Any], tool: str) -> bool:
    try: _output(case, tool)
    except (StopIteration, KeyError, TypeError): return False
    return True


def _call(messages: list[dict[str, Any]], calls: list[str], case: dict[str, Any], tool: str,
          args: dict[str, Any], thought: str, discriminator: str | None = None) -> None:
    messages.extend(_pair(tool, args, _output(case, tool, discriminator), thought)); calls.append(tool)


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "ischemic_stroke": return False
    before = json.dumps(row, sort_keys=True); differential = row.get("style") == "differential_reasoned"
    messages = [dict(x) for x in row["messages"] if x.get("role") in {"system", "user"}][:2]; calls: list[str] = []
    ct = _actions(case, "order_ct_scan")
    if differential:
        action = next(x for x in ct if x["tool_parameters"]["angiography"])
        _call(messages, calls, case, "order_ct_scan",
              {"clinical_context": action["action"], "contrast": True, "angiography": True},
              "NCCT has already excluded hemorrhage in this branch. CTA is the separate rapid LVO study and must not wait for creatinine.", "cta")
    else:
        action = next(x for x in ct if not x["tool_parameters"]["angiography"])
        _call(messages, calls, case, "order_ct_scan",
              {"clinical_context": action["action"], "contrast": False, "angiography": False},
              "I will start with mandatory NCCT. It excludes hemorrhage and is sufficient for most thrombolysis decisions; optional MRI must not delay it.")
    labs = _actions(case, "interpret_labs")[0]; dem = case["patient"]["demographics"]
    _call(messages, calls, case, "interpret_labs",
          {"clinical_context": labs["action"], "panels": labs["tool_parameters"]["panels"],
           "patient_age": dem["age"], "patient_sex": dem["sex"]},
          "Glucose is checked before thrombolysis; CBC/coagulation are obtained but not routinely awaited, and troponin does not delay reperfusion.")
    ecg = _actions(case, "analyze_ecg")
    if ecg:
        _call(messages, calls, case, "analyze_ecg", {"clinical_context": ecg[0]["action"]},
              "Baseline ECG supports cardiac assessment but cannot delay thrombolysis or thrombectomy.")
    if differential:
        perf = _actions(case, "order_advanced_imaging")
        if perf:
            _call(messages, calls, case, "order_advanced_imaging",
                  {"clinical_context": perf[0]["action"], "modality": "CT_perfusion"},
                  "This is a selected wake-up/extended-window case, so immediately available automated CTP can quantify core and penumbra without delaying treatment.")
        else:
            mri = _actions(case, "analyze_brain_mri")[0]
            _call(messages, calls, case, "analyze_brain_mri",
                  {"clinical_context": mri["action"], "protocol": "stroke", "contrast": False},
                  "MRI is optional and used only after the emergent pathway when it answers an onset, posterior-circulation or mimic question.")
        eeg = _actions(case, "analyze_eeg")
        if eeg:
            _call(messages, calls, case, "analyze_eeg",
                  {"clinical_context": eeg[0]["action"], "eeg_type": "routine"},
                  "The witnessed tonic hand event creates a genuine seizure-mimic question; EEG remains optional and cannot delay reperfusion.")
        for tool, default_args, thought in (
            ("order_echocardiogram", {"echo_type": "TTE"}, "Echocardiography is downstream mechanism work-up."),
            ("order_cardiac_monitoring", {"monitor_type": "holter_24h"}, "Rhythm monitoring is downstream mechanism work-up."),
        ):
            acts = _actions(case, tool)
            if acts and _has_output(case, tool):
                params = {k: v for k, v in acts[0].get("tool_parameters", {}).items() if k in default_args}
                _call(messages, calls, case, tool, {"clinical_context": acts[0]["action"], **default_args, **params}, thought)
        drug = _actions(case, "check_drug_interactions")
        if drug and _has_output(case, "check_drug_interactions"):
            meds = case["patient"]["clinical_history"].get("medications", [])
            current = [str(x.get("drug", x)) if isinstance(x, dict) else str(x) for x in meds]
            _call(messages, calls, case, "check_drug_interactions",
                  {"drug": drug[0].get("tool_parameters", {}).get("drug", "alteplase"), "current_medications": current},
                  "I will check treatment contraindications after obtaining the hemorrhage-excluding scan, in parallel with—not after waiting for—routine tests.")
    primary = case["ground_truth"]["primary_diagnosis"]
    messages.append({"role": "assistant", "content": f"### Primary Diagnosis\n{primary}\n\nNCCT and CTA are distinct urgent studies. Glucose is checked before thrombolysis, but routine laboratories, ECG, MRI and advanced imaging do not delay reperfusion. Tissue perfusion imaging is reserved for selected extended-window cases."})
    row["messages"] = messages; row["tools_called"] = calls; row["num_tool_calls"] = len(calls)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", type=Path, default=DEFAULT_INPUT); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("ISCH-STR-*.json")}
    rows = [json.loads(x) for x in args.input.read_text().splitlines() if x.strip()]
    changed = sum(revise(row, cases[row["case_id"]]) for row in rows if row.get("condition") == "ischemic_stroke")
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows); print(f"ischemic-stroke trajectories changed: {changed}")
    if args.check and changed: raise SystemExit(1)
    if not args.check: args.input.write_text(rendered)


if __name__ == "__main__": main()
