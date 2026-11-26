"""Task 06, check C4: per-case reading files for the independent field-by-field re-read.
Each file holds the case as built (the review file: presentation as the agent sees it, every tool
output, policy, served-origin metadata) and the source the reader checks it against (triage, the
discharge note, the radiology reports in the window and every served report, the machine ECG reads,
ED medication times). Labs are rechecked by mimic_reread3.py (table values). Output only under the
PhysioNet workspace: the files hold record content. No record content in this file.

    python -I mimic_reread6_files.py --out $W/out --to $W/tmp/reread6
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mimic_case_assemble import anchor, hours, ts  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--to", required=True)
    ap.add_argument("--selection", default="06_selection.csv")
    a = ap.parse_args()
    out, to = Path(a.out), Path(a.to)
    if not str(to.resolve()).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
        sys.exit("--to must be under the PhysioNet workspace")
    to.mkdir(parents=True, exist_ok=True)
    sel = pd.read_csv(out / a.selection)
    live = sel[sel.case_id.notna() & (sel.case_id != "") & (sel.exclusion.isna() | (sel.exclusion == ""))]
    for cid in live.case_id:
        case = json.loads((out / "06_cases" / f"{cid}.json").read_text())
        b = json.loads((out / "02_source" / f"{cid}.json").read_text())
        t_ed = anchor(b)
        t_adm = ts(b["admission"][0]["admittime"])
        h48 = hours(t_adm + pd.Timedelta(hours=48), t_ed)
        served_exams = set()
        for v in case["metadata"]["served"].values():
            for x in str(v.get("exam", "")).split(" + "):
                served_exams.add(x.strip())
        parts = [f"# {cid}: re-read file\n\nTimes are hours from ED arrival (t=0). Admission at t={hours(t_adm, t_ed):.1f} h; "
                 f"decision point for extra studies t={h48:.1f} h (admission + 48 h).\n",
                 "## PART 1. The case as built\n", (out / "06_review" / f"{cid}.md").read_text(),
                 "\n## PART 1b. Served-origin metadata\n```json\n" + json.dumps(case["metadata"].get("served", {}), indent=1) + "\n```\n",
                 "\n## PART 1c. Every follow-up output exactly as served (the review file above may omit some), and the hidden case flags\n```json\n"
                 + json.dumps({"followup_outputs": case["followup_outputs"],
                               "hidden_flags": {k: case["metadata"].get(k) for k in ("dx_support", "dx_support_basis", "known_condition_in_history",
                                                                                     "known_condition_detail", "eeg_source", "decision_point",
                                                                                     "sah_aneurysm_status", "csf_not_served", "policy_study_hours",
                                                                                     "rejected_labels_rule", "diagnosis_code_note")},
                               "policy_adaptations": case["metadata"].get("policy", {}).get("adapted", []),
                               "diagnosis": case["ground_truth"]["diagnosis"]}, indent=1) + "\n```\n",
                 "\n## PART 2. Source\n### Triage\n```json\n" + json.dumps(b.get("triage", []), indent=1, default=str) + "\n```\n",
                 "### ED medications (pyxis), hours from ED arrival\n" + "\n".join(
                     f"- t={hours(m['charttime'], t_ed):.1f} h: {m.get('name')}" for m in b.get("ed_pyxis", []) if hours(m.get("charttime"), t_ed) is not None),
                 "\n### Discharge note\n```\n" + b["discharge"][0]["text"] + "\n```\n", "### Radiology reports (window up to admission + 48 h, and every served report)\n"]
        for r in sorted(b["radiology"], key=lambda r: r["charttime"]):
            h = hours(r["charttime"], t_ed)
            if h is None or not (h <= h48 or r["exam_name"] in served_exams):
                continue
            parts.append(f"#### {r['exam_name']} (t={h:.1f} h)\n```\n{r['text']}\n```\n")
        parts.append("### Machine ECG reads (window)\n")
        for e in sorted(b.get("ecg_machine", []), key=lambda e: e["ecg_time"]):
            h = hours(e["ecg_time"], t_ed)
            if h is not None and -1 <= h <= h48:
                parts.append(f"- t={h:.1f} h: " + json.dumps({k: v for k, v in e.items() if k not in ("subject_id", "study_id", "file_name", "cart_id")}, default=str))
        (to / f"{cid}.md").write_text("\n".join(parts) + "\n")
    print(len(live), "re-read files written to", to)


if __name__ == "__main__":
    main()
