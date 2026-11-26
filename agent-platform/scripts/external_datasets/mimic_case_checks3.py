"""Timing and provenance checks of the task-03 MIMIC pilot cases (OUT/03_cases). Prints counts only.

For every served answer:
- presentation steps (labs, non-contrast CT, CTA, ECG) dated no later than admission + 24 h, labs
  and ECG no earlier than ED arrival - 1 h; the non-contrast CT never follows the CTA unless it is
  the explicit non-contrast part of the same CTA report (decision 2);
- telemetry from rhythm records covers >= 12 h (decision 5);
- the MRI / spine MRI is the first of its kind in the stay;
- the served radiology report is found in the source, and no served row belongs to another admission;
- note-extracted answers carry no time: counted as untimed.

    python -I mimic_case_checks3.py --out $W/out
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mimic_case_assemble import anchor, hours, ts  # noqa: E402
from mimic_pilot_v3 import MRI_EXAM, SPINE_MRI_EXAM  # noqa: E402


def check(out: Path, cid: str, hadm: int) -> dict:
    case = json.loads((out / f"{TAG}_cases" / f"{cid}.json").read_text())
    b = json.loads((out / "02_source" / f"{cid}.json").read_text())
    t_ed = anchor(b)
    h24 = hours(ts(b["admission"][0]["admittime"]) + pd.Timedelta(hours=24), t_ed)
    h48 = hours(ts(b["admission"][0]["admittime"]) + pd.Timedelta(hours=48), t_ed)
    served = case["metadata"]["served"]
    res = {"errors": [], "untimed_note_extracted": [], "served": {}}
    for k, v in served.items():
        t = v.get("t_h", v.get("t_first_h"))
        res["served"][k] = {"origin": v["origin"], "t_h": t}
        if v["origin"] == "note_extracted":
            res["untimed_note_extracted"].append(k)
            continue
        if k in ("labs", "ct", "followup:request_ct_angiography", "ecg") and (t is None or t > h24):
            res["errors"].append(f"{k} dated after admission + 24 h")
        if k in ("labs", "ecg") and t is not None and t < -1.0:
            res["errors"].append(f"{k} dated before ED arrival - 1 h")
        # task 06: the extra studies (follow-ups, advanced imaging, microbiology) end at the decision point
        if TAG == "06" and t is not None and (k.startswith("followup:") or k in ("advanced_imaging", "microbiology")) \
                and k not in ("followup:request_ct_angiography", "followup:request_respiratory_monitoring") and t > h48 + 0.01:
            pol = [c["alternatives"][0]["required_arguments"].get("specimen") for c in case["ground_truth"]["action_criteria"]
                   if c["alternatives"][0]["tool_name"] == "order_microbiology"]
            if not (k == "microbiology" and case["initial_tool_outputs"].get("microbiology", {}).get("specimen") in pol):
                res["errors"].append(f"{k} dated after the decision point (admission + 48 h)")
        if k == "cardiac_monitoring" and v.get("covered_h", 0) < 12:
            res["errors"].append("telemetry covers < 12 h")
    if "ct" in served and "followup:request_ct_angiography" in served:
        same = "non-contrast part" in served["ct"].get("source", "")
        if not same and served["ct"]["t_h"] > served["followup:request_ct_angiography"]["t_h"] + 0.5:
            res["errors"].append("non-contrast CT follows the CTA")
    rad = b["radiology"]
    for k in ("ct", "followup:request_ct_angiography", "mri", "body_imaging"):
        if k not in served:
            continue
        exams = served[k]["exam"].split(" + ")
        rows = [r for r in rad if r["exam_name"] in exams and abs((hours(r["charttime"], t_ed) or 0) - served[k]["t_h"]) < 0.05]
        if not rows:
            res["errors"].append(f"{k}: served report not found in the source")
        for r in rows:
            if r.get("hadm_id") not in (None, "") and pd.notna(r.get("hadm_id")) and int(float(r["hadm_id"])) != hadm:
                res["errors"].append(f"{k}: report belongs to another admission")
        if k in ("mri", "body_imaging"):
            rx = MRI_EXAM if k == "mri" else SPINE_MRI_EXAM
            earlier = [r for r in rad if re.search(rx, str(r["exam_name"]).upper()) and (hours(r["charttime"], t_ed) or 1e9) < served[k]["t_h"] - 0.05]
            if earlier:
                res["errors"].append(f"{k}: an earlier study of the kind exists")
    labs = pd.DataFrame(b["labs"])
    res["lab_rows_other_admission_in_source"] = int((labs.hadm_id.notna() & (labs.hadm_id != hadm)).sum()) if len(labs) else 0
    return res


TAG = "03"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default="03")
    a = ap.parse_args()
    global TAG
    TAG = a.tag
    out = Path(a.out)
    sel = pd.read_csv(out / f"{TAG}_selection.csv")
    sel = sel[sel.case_id.notna() & (sel.case_id != "")]
    if "exclusion" in sel:
        sel = sel[sel.exclusion.isna() | (sel.exclusion == "")]
    res = {r.case_id: check(out, r.case_id, int(r.hadm_id)) for r in sel.itertuples() if (out / f"{TAG}_cases" / f"{r.case_id}.json").exists()}
    (out / f"{TAG}_timing_checks.json").write_text(json.dumps(res, indent=1))
    by = {}
    for cid, v in res.items():
        c = cid.split("-")[1]
        d = by.setdefault(c, {"cases": 0, "errors": 0, "untimed": 0})
        d["cases"] += 1
        d["errors"] += len(v["errors"])
        d["untimed"] += len(v["untimed_note_extracted"])
    print("per condition:", by)
    for cid, v in res.items():
        if v["errors"]:
            print(f"  {cid}: {v['errors']}")


if __name__ == "__main__":
    main()
