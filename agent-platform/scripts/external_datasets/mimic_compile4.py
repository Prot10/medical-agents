"""Task 04: collect the readers' decisions into the selection inputs. No record content in this file.

From each manual file of the new candidates (FEPI, SE replacements):
- ``exclude`` set -> a row of 04_exclusions.csv (decision 8/21 transfer, record support, ...);
- kept but the build reports a core step without a served result -> 04_exclusions.csv with the class
  "core step without a servable result" (e.g. an EEG given only as a whole-stay summary, decision 19);
- FEPI ``dx_support`` read for admissions whose discharge diagnosis does not name a focal epilepsy
  -> 04_fepi_support_review.csv (hadm_id, supported, basis, reason).
Also adds the FEPI / new SE rows of 04_case_flags.csv (decisions 25, 26) from the reader's notes.

    python -I mimic_compile4.py --out $W/out --candidates 04_fepi_candidates.csv 04_se_candidates.csv
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--candidates", nargs="+", required=True)
    ap.add_argument("--clinical-only", nargs="*", default=[], help="case ids read as clinical_only (decision 26)")
    a = ap.parse_args()
    out = Path(a.out)
    cand = pd.concat([pd.read_csv(out / f) for f in a.candidates]).drop_duplicates("case_id")
    checks = json.loads((out / "04_build_checks.json").read_text())
    ex = pd.read_csv(out / "04_exclusions.csv")
    ex = ex[~ex.case_id.isin(cand.case_id)]
    new_ex, sup, flags = [], [], []
    for r in cand.itertuples():
        f = out / "04_manual" / f"{r.case_id}.json"
        if not f.exists():
            continue
        m = json.loads(f.read_text())
        ds = m.get("dx_support") or {}
        if r.condition == "FEPI":
            sup.append({"hadm_id": int(r.hadm_id), "supported": bool(ds.get("supported")), "basis": ds.get("basis", ""),
                        "reason": ds.get("reason", "")})
        if m.get("exclude"):
            new_ex.append({"hadm_id": int(r.hadm_id), "case_id": r.case_id, "reason": str(m["exclude"]), "decision": "04 reading"})
            continue
        errs = checks.get(r.case_id, {}).get("build_errors", [])
        core = [e for e in errs if e.startswith("core step") or e.startswith("required lab panels")]
        if core:
            new_ex.append({"hadm_id": int(r.hadm_id), "case_id": r.case_id,
                           "reason": "core step without a servable result (" + "; ".join(core) + ")", "decision": "19 / data"})
            continue
        notes = " ".join(m.get("other_edits", []))
        known = bool(re.search(r"(?i)known epilepsy:\s*yes", notes))
        flags.append({"case_id": r.case_id, "known_condition_in_history": known if r.condition == "FEPI" else False,
                      "known_condition_detail": "epilepsy known before this admission" if (known and r.condition == "FEPI") else "",
                      "dx_support": "clinical_only" if r.case_id in a.clinical_only else "test_confirmed",
                      "dx_support_basis": ("diagnosis rests on the clinical description; no study confirms it" if r.case_id in a.clinical_only
                                           else {"FEPI": "focal EEG abnormality or epileptiform discharges on the first EEG",
                                                 "SE": "electrographic seizures on the first EEG"}.get(r.condition, ""))})
    ex = pd.concat([ex, pd.DataFrame(new_ex)], ignore_index=True)
    ex.to_csv(out / "04_exclusions.csv", index=False)
    pd.DataFrame(sup).to_csv(out / "04_fepi_support_review.csv", index=False)
    cf = pd.read_csv(out / "04_case_flags.csv")
    cf = cf[~cf.case_id.isin([x["case_id"] for x in flags])]
    pd.concat([cf, pd.DataFrame(flags)], ignore_index=True).to_csv(out / "04_case_flags.csv", index=False)
    print("exclusions:", len(ex), "| new from reading:", pd.Series([x["reason"].split(" (")[0].split(":")[0] for x in new_ex]).value_counts().to_dict())
    print("FEPI support read:", pd.DataFrame(sup).groupby(["supported", "basis"]).size().to_dict() if sup else {})
    print("kept new cases:", len(flags), "| known epilepsy:", sum(x["known_condition_in_history"] for x in flags),
          "| clinical_only:", sum(x["dx_support"] == "clinical_only" for x in flags))


if __name__ == "__main__":
    main()
