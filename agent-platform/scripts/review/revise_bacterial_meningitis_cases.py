"""Apply the Reviewer 2 meningitis pathway, separating LP/microbiology from carry-over tests."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"
# Imaging is retained only where the authored case has a structural/intracranial complication
# or a genuine atypical alternative, not to confirm ordinary acute bacterial meningitis.
MRI_REQUIRED = {"BACT-MEN-M04", "BACT-MEN-M05", "BACT-MEN-P02", "BACT-MEN-P03",
                "BACT-MEN-RP03", "BACT-MEN-RP04", "BACT-MEN-RS02", "BACT-MEN-RS04", "BACT-MEN-S04"}
MRI_RECOMMENDED = {"BACT-MEN-RM02"}

def cp(x: Any) -> Any: return json.loads(json.dumps(x))

def act(tool, params, text, finding, category="required"):
    return {"action": text, "tool_name": tool, "expected_finding": finding, "category": category,
            "tool_parameters": params, "citation": "[WHO_Meningitis_2025]",
            "guideline_source": "WHO meningitis guideline 2025"}

def reports(case, tool, key):
    rows = [case["initial_tool_outputs"][key]] if case["initial_tool_outputs"].get(key) else []
    rows += [x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool and x.get("output")]
    return rows

def best(case, tool, key):
    rows = reports(case, tool, key)
    if not rows: raise ValueError(f"{case['case_id']}: missing {tool}")
    return cp(max(rows, key=lambda r: len(json.dumps(r))))

def revise(case):
    cid, gt, initial = case["case_id"], case["ground_truth"], case["initial_tool_outputs"]
    # Preserve only a selected MRI report; all generic MRI follow-up is removed.
    initial["mri"] = best(case, "analyze_brain_mri", "mri") if cid in MRI_REQUIRED | MRI_RECOMMENDED else None
    initial["ecg"] = None  # reviewer: no diagnostic role in meningitis
    initial["eeg"] = best(case, "analyze_eeg", "eeg") if any(a.get("tool_name") == "analyze_eeg" for a in gt["optimal_actions"]) else None
    case["followup_outputs"] = [x for x in case["followup_outputs"] if x.get("tool_name") not in {"analyze_brain_mri", "analyze_ecg", "analyze_eeg"}]

    for row in gt["optimal_actions"]:
        if row.get("tool_name") is None and row["action"] not in gt.setdefault("critical_actions", []):
            gt["critical_actions"].append(row["action"])
    preserved = [cp(a) for a in gt["optimal_actions"] if a.get("tool_name") in {
        "order_ct_scan", "analyze_eeg", "check_drug_interactions", "search_medical_literature"
    }]
    for a in preserved:
        if a.get("tool_name") in {"check_drug_interactions", "search_medical_literature"}: a["category"] = "recommended"
    actions = [
        act("interpret_labs", {"panels": ["CBC", "CMP", "CRP", "procalcitonin", "glucose", "coagulation", "HIV"]},
            "Obtain CBC with differential, CRP (or procalcitonin), paired blood glucose, coagulation, renal/liver function and HIV testing; results must not delay LP or empirical therapy",
            "Inflammation/sepsis and LP safety context; blood values neither confirm nor exclude bacterial meningitis"),
        act("order_microbiology", {"specimen": "blood_culture", "tests": ["culture", "gram_stain", "susceptibility"], "before_antimicrobials": True},
            "Draw blood cultures with susceptibility testing as early as possible, preferably before antimicrobials, but start empirical therapy immediately if LP/imaging is delayed",
            "Pathogen and susceptibility, with collection timing recorded"),
        act("analyze_csf", {"basic": ["opening_pressure", "appearance", "cell_count_total_and_differential", "rbc_count", "protein", "glucose"],
                            "paired_serum": True, "special_tests": ["meningitis_panel"]},
            "Perform LP with opening pressure, appearance, total/differential WBC, RBC, protein, CSF-to-blood glucose ratio, Gram stain, culture/susceptibility and relevant PCR; record whether collected before antibiotics",
            "Bacterial pattern and organism/susceptibility; PCR and culture yield depend on whether antibiotics preceded sampling"),
    ]
    if cid in MRI_REQUIRED | MRI_RECOMMENDED:
        category = "required" if cid in MRI_REQUIRED else "recommended"
        actions.append(act("analyze_brain_mri", {"protocol": "standard", "contrast": True},
            "Obtain contrast brain MRI only for this case's suspected intracranial complication, structural alternative or failure to improve; it does not replace LP",
            "Abscess, empyema, ventriculitis, hydrocephalus, infarction or the stated alternative/complication", category))
    actions.extend(preserved)
    for i,a in enumerate(actions,1): a["step"] = i
    gt["optimal_actions"] = actions
    # CT can be required by a case's safety screen, but never holds treatment while it is pending.
    gt["sequence_constraints"] = [c for c in gt.get("sequence_constraints", [])
                                  if c.get("before") in {"order_ct_scan", "order_microbiology"} and c.get("after") == "analyze_csf"]
    note = "WHO 2025: obtain cultures promptly, but neither LP nor cranial imaging may delay empirical antimicrobials when the pathway requires treatment first."
    if note not in gt.setdefault("key_reasoning_points", []): gt["key_reasoning_points"].append(note)
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = "Reviewer 2 meningitis audit: complete LP/microbiology/lab pathway, no ECG, and MRI restricted to complications or non-response"

def main():
    p=argparse.ArgumentParser(); p.add_argument("--cases",type=Path,default=DEFAULT_CASES); p.add_argument("--check",action="store_true"); a=p.parse_args(); changed=0
    for path in sorted(a.cases.glob("BACT-MEN-*.json")):
        c=json.loads(path.read_text()); before=json.dumps(c,sort_keys=True); revise(c)
        if json.dumps(c,sort_keys=True)!=before:
            changed+=1
            if not a.check: path.write_text(json.dumps(c,indent=2,ensure_ascii=False)+"\n")
    print(f"bacterial-meningitis cases changed: {changed}")
    if a.check and changed: raise SystemExit(1)
if __name__ == "__main__": main()
