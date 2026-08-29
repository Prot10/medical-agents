"""Apply the remaining reviewer-2 MR-venography pathway in status epilepticus."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

def revise(case: dict) -> None:
    if case["case_id"] != "SE-S08": return
    gt = case["ground_truth"]
    gt["optimal_actions"] = [a for a in gt["optimal_actions"] if not (
        a.get("tool_name") == "order_advanced_imaging" and (a.get("tool_parameters") or {}).get("modality") == "MR_venography"
    )]
    gt["optimal_actions"].append({
        "action": "After stabilisation and brain MRI, obtain MR venography because pregnancy, severe headache/status and the PRES-like imaging differential leave cerebral venous thrombosis as a treatable alternative.",
        "tool_name": "order_advanced_imaging", "expected_finding": "Patent dural venous sinuses and cortical veins without cerebral venous sinus thrombosis.",
        "category": "optional", "tool_parameters": {"modality": "MR_venography"},
        "citation": "[LICE_NORSE_2024]", "guideline_source": "LICE 2024 NORSE/status epilepticus guidance",
    })
    for i, a in enumerate(gt["optimal_actions"], 1): a["step"] = i
    case["followup_outputs"] = [x for x in case["followup_outputs"] if x.get("trigger_action") != "request_mr_venography"]
    case["followup_outputs"].append({"trigger_action": "request_mr_venography", "tool_name": "order_advanced_imaging", "tool_parameters": {"modality": "MR_venography"}, "output": {
        "modality": "MR venography", "tracer_or_protocol": "time-of-flight and contrast-enhanced venography", "findings": [
            {"region": "superior sagittal, transverse, sigmoid and straight sinuses", "finding": "Normal flow-related enhancement; no filling defect or thrombosis."},
            {"region": "cortical veins", "finding": "No cortical venous thrombosis."}],
        "quantitative_data": None, "impression": "No cerebral venous sinus or cortical venous thrombosis.", "recommended_actions": []}})
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = "Reviewer 2 status-epilepticus audit: MR venography is optional and reachable only in the pregnancy/CVST differential case."

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--cases", type=Path, default=DEFAULT_CASES); p.add_argument("--check", action="store_true"); a=p.parse_args(); n=0
    for f in sorted(a.cases.glob("SE-*.json")):
        c=json.loads(f.read_text()); b=json.dumps(c,sort_keys=True); revise(c)
        if json.dumps(c,sort_keys=True)!=b:
            n+=1
            if not a.check: f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+"\n")
    print(f"status-epilepticus cases changed: {n}")
    if a.check and n: raise SystemExit(1)
if __name__ == "__main__": main()
