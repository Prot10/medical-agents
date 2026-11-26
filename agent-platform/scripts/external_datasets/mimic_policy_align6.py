"""Task 06, check C5: policy alignment of the selected cases. For every case: the transferred
criteria (step, importance, tool, arguments), whether each required criterion has a served result
(an initial output of that tool or a follow-up the criterion's trigger reaches), the lab panels
dropped by decision 3, and how the case's required set differs from its condition's modal set
(an adaptation). Writes $W/out/06_policy_alignment.csv (case ids: workspace only); prints
aggregates per condition (no ids). No record content in this file.

    python -I mimic_policy_align6.py --out $W/out
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import pandas as pd

TOOL_KEY = {"interpret_labs": "labs", "analyze_eeg": "eeg", "analyze_brain_mri": "mri", "analyze_ecg": "ecg", "analyze_csf": "csf",
            "order_ct_scan": "ct", "order_echocardiogram": "echo", "order_cardiac_monitoring": "cardiac_monitoring",
            "order_advanced_imaging": "advanced_imaging", "order_specialized_test": "specialized_test", "order_body_imaging": "body_imaging",
            "order_microbiology": "microbiology", "obtain_tissue_diagnosis": "tissue_diagnosis", "perform_clinical_assessment": "clinical_assessment"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    sel = pd.read_csv(out / "06_selection.csv")
    live = sel[sel.case_id.notna() & (sel.case_id != "") & (sel.exclusion.isna() | (sel.exclusion == ""))]
    perfect = json.loads((out / "06_perfect_agent.json").read_text()) if (out / "06_perfect_agent.json").exists() else {}
    rows = []
    for r in live.itertuples():
        c = json.loads((out / "06_cases" / f"{r.case_id}.json").read_text())
        pol = c["metadata"].get("policy", {})
        io, fu = c["initial_tool_outputs"], c["followup_outputs"]
        req, rec, unserved = [], [], []
        for cr in c["ground_truth"]["action_criteria"]:
            alt = cr["alternatives"][0]
            tool = alt["tool_name"]
            step = pol.get("criteria", {}).get(cr.get("id", ""), {}).get("step") or tool
            (req if cr["importance"] == "required" else rec).append(step)
            if cr["importance"] != "required" or tool.startswith(("check_", "search_")):
                continue
            has = bool(io.get(TOOL_KEY.get(tool, ""))) or any(x["tool_name"] == tool for x in fu)
            if not has:
                unserved.append(step)
        rows.append({"case_id": r.case_id, "condition": r.condition, "required": "|".join(sorted(req)), "recommended": "|".join(sorted(rec)),
                     "n_required": len(req), "required_unserved": "|".join(unserved),
                     "lab_panels_dropped_rule_3": "|".join(pol.get("lab_panels_dropped_rule_3", []) or []),
                     "perfect_agent_ok": not (perfect.get(r.case_id, {}) or {}).get("errors") if perfect else None})
    df = pd.DataFrame(rows)
    modal = df.groupby("condition").required.agg(lambda s: s.value_counts().index[0])
    df["adapted_vs_modal"] = [x != modal[c] for x, c in zip(df.required, df.condition)]
    df.to_csv(out / "06_policy_alignment.csv", index=False)
    print("== required sets per condition (cases per distinct set)")
    for cond, g in df.groupby("condition"):
        print(f"{cond}: modal = {modal[cond]} | sets: {g.required.value_counts().to_dict()}")
    print("\n== required criteria without a served result:", int((df.required_unserved != "").sum()), "cases")
    print("== lab panels dropped by decision 3 per condition:",
          {c: dict(collections.Counter(p for x in g.lab_panels_dropped_rule_3 for p in x.split("|") if p)) for c, g in df.groupby("condition")})
    print("== cases whose required set differs from the condition's modal set:", df.groupby("condition").adapted_vs_modal.sum().to_dict())


if __name__ == "__main__":
    main()
