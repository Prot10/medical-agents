"""Task 06: collect the readers' decisions into the selection inputs. No record content in this file.

For every candidate with a manual file (06_extract_new.csv and the task-04 cases):
- `exclude` set -> a row of 06_exclusions.csv (reason as written; decision column "06 reading");
- kept but the 06 build reports a core step without a served result / a required panel missing ->
  06_exclusions.csv with "core step without a servable result (...)";
- SE / FEPI record support read -> 06_support_review.csv (hadm_id, supported, basis, reason);
- case flags (decisions 25, 26) -> 06_case_flags.csv: the task-04 flags for task-04 cases, and for new
  cases `known_condition_in_history` from the reader's "known condition: yes" line, `dx_support`
  clinical_only when no study in the case confirms the diagnosis (reader's reason names only clinical
  evidence, or HEP, whose diagnosis is clinical by definition).

    python -I mimic_compile6.py --out $W/out
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

TEST_WORDS = re.compile(r"(?i)imaging|\bCT\b|\bMRI\b|\bEEG\b|electrograph|\bECG\b|EKG|telemetr|\becho|\bCSF\b|culture|patholog|biops|"
                        r"\bNCS\b|EMG|holter|monitor|lesion|infarct|haemorrh|hemorrh|blood on|subarachnoid blood|block|bradycard|tachycard|"
                        r"stenosis|sign|hoover|give-way|entrainment")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    cand = pd.concat([pd.read_csv(out / f) for f in ("06_extract_new.csv", "06_extract_new2.csv", "06_extract_new3.csv", "07_extract_new.csv", "07_extract_new2.csv", "07_extract_new3.csv", "07_extract_new4.csv", "07_extract_new5.csv") if (out / f).exists()])
    checks = json.loads((out / "06_build_checks.json").read_text()) if (out / "06_build_checks.json").exists() else {}
    ex = pd.read_csv(out / "06_exclusions.csv")
    keep_data = ex[(ex.decision == "06 data") & ~ex.case_id.isin(list(checks))]  # core-step rows of cases no longer rebuilt
    keep07 = ex[ex.decision.astype(str).str.startswith("07")]  # task-07 exclusions (decisions 42, 44, 49; unfixable errors)
    ex = ex[~ex.case_id.isin(cand.case_id) & ~ex.decision.astype(str).str.startswith("07")]
    ex = pd.concat([ex, keep_data[keep_data.case_id.isin(cand.case_id)], keep07], ignore_index=True)
    new_ex, sup, flags = [], [], []
    for r in cand.itertuples():
        f = out / "06_manual" / f"{r.case_id}.json"
        if not f.exists():
            continue
        m = json.loads(f.read_text())
        ds = m.get("dx_support") or {}
        if r.condition in ("SE", "FEPI"):
            sup.append({"hadm_id": int(r.hadm_id), "supported": bool(ds.get("supported")), "basis": ds.get("basis", ""), "reason": ds.get("reason", "")})
        if m.get("exclude"):
            new_ex.append({"hadm_id": int(r.hadm_id), "case_id": r.case_id, "reason": str(m["exclude"]), "decision": "06 reading"})
            continue
        errs = checks.get(r.case_id, {}).get("build_errors", [])
        core = [e for e in errs if e.startswith("core step") or e.startswith("required lab panels")]
        if core:
            new_ex.append({"hadm_id": int(r.hadm_id), "case_id": r.case_id,
                           "reason": "core step without a servable result (" + "; ".join(core) + ")", "decision": "06 data"})
            continue
        notes = " ".join(m.get("other_edits", []) + m.get("exam_notes", []))
        known = bool(re.search(r"(?i)known (?:condition|epilepsy|disease)[^.;]{0,10}:\s*yes", notes))
        reason = str(ds.get("reason", ""))
        clinical = r.condition in ("HEP", "FND") or not TEST_WORDS.search(reason)  # FND: bedside signs, no confirming test
        flags.append({"case_id": r.case_id, "known_condition_in_history": known,
                      "known_condition_detail": "condition known before this admission" if known else "",
                      "dx_support": "clinical_only" if clinical else "test_confirmed",
                      "dx_support_basis": "clinical diagnosis (no study in the case confirms it)" if clinical else "a study in the case shows the defining finding"})
    ex = pd.concat([ex, pd.DataFrame(new_ex)], ignore_index=True)
    ex.to_csv(out / "06_exclusions.csv", index=False)
    pd.DataFrame(sup).to_csv(out / "06_support_review.csv", index=False)
    cf = pd.read_csv(out / "04_case_flags.csv")
    cf = cf[~cf.case_id.isin([x["case_id"] for x in flags])]
    cf = pd.concat([cf, pd.DataFrame(flags)], ignore_index=True)
    ov = out / "06_flag_overrides.csv"  # re-read corrections (case_id, field, value, reason); workspace only
    if ov.exists():
        for o in pd.read_csv(ov, dtype=str).itertuples():
            v = {"True": True, "False": False}.get(o.value, o.value)
            cf[o.field] = cf[o.field].astype(object)
            cf.loc[cf.case_id == o.case_id, o.field] = v
            if o.field == "dx_support":
                cf.loc[cf.case_id == o.case_id, "dx_support_basis"] = str(o.reason)
        print("flag overrides applied:", len(pd.read_csv(ov)))
    cf.to_csv(out / "06_case_flags.csv", index=False)
    print("exclusions:", len(ex), "| new from reading:", pd.Series([x["reason"].split(" (")[0][:60] for x in new_ex]).value_counts().to_dict())
    print("kept new:", len(flags), "| known:", sum(x["known_condition_in_history"] for x in flags), "| clinical_only:",
          sum(x["dx_support"] == "clinical_only" for x in flags))


if __name__ == "__main__":
    main()
