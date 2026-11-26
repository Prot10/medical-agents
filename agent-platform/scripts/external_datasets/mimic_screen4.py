"""Reading aid for decisions 21, 25, 26 (task 04): per case, the HPI / PMH sentences that a reader
must judge (outside-facility treatment or intubation before arrival; the condition already known
in the history; whether a test confirms the diagnosis). Prints to the reader's terminal only: the
output holds record text and must never go into a report. No record content in this file.

    python -I mimic_screen4.py --out $W/out --cases MIMIC-SE-001 ... [--what transfer|known|confirm]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

OUTSIDE = re.compile(r"(?i)\bOSH\b|outside (?:hospital|facility|ED|institution)|transferr|transfer\b|\bsent (?:here|to)|"
                     r"referr|other hospital|community hospital|nursing (?:home|facility)|rehab|urgent care|"
                     r"\bat ___\b|presented to ___|taken to ___|brought to ___|initially (?:presented|seen|taken)|"
                     r"intubat|loaded|was given|received|administered|\bgiven\b|tPA|alteplase|thromboly|\bEMS\b|ambulance|medic")
KNOWN = {
    "ISCH": r"(?i)stroke|\bCVA\b|infarct|\bTIA\b",
    "SAH": r"(?i)\bSAH\b|subarach|aneurysm",
    "SE": r"(?i)status epilepticus|\bstatus\b|\bSE\b",
    "GBS": r"(?i)guillain|\bGBS\b|\bAIDP\b|\bCIDP\b",
    "MS": r"(?i)multiple sclerosis|\bMS\b|demyelinat|\bRIS\b|optic neuritis|transverse myelitis|\bCIS\b",
    "FEPI": r"(?i)epilep|seizure|\bsz\b|\bAED\b|keppra|levetir|lamotri|lacosam|carbamaz|oxcarb|phenyto|valpro|topira",
}


def sentences(t: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.;!?])\s+|\n", t or "") if s.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cases", nargs="+", required=True)
    ap.add_argument("--what", default="transfer", choices=["transfer", "known", "confirm"])
    ap.add_argument("--tag", default="03")
    a = ap.parse_args()
    out = Path(a.out)
    for cid in a.cases:
        cond = cid.split("-")[1]
        au = json.loads((out / f"{a.tag}_hpi_audit" / f"{cid}.json").read_text())
        c = json.loads((out / f"{a.tag}_cases" / f"{cid}.json").read_text())
        print(f"##### {cid}")
        if a.what == "transfer":
            for s in sentences(au["hpi_original"]):
                if OUTSIDE.search(s):
                    print("  -", s[:400])
        elif a.what == "known":
            for s in c["patient"]["clinical_history"]["past_medical_history"]:
                if re.search(KNOWN[cond], s):
                    print("  PMH:", s[:300])
            for s in sentences(au["hpi_kept"]):
                if re.search(KNOWN[cond], s):
                    print("  HPI:", s[:300])
            meds = " ; ".join(m["drug"] for m in c["patient"]["clinical_history"]["medications"])
            if cond in ("FEPI", "SE", "MS"):
                print("  MEDS:", meds[:400])
        else:
            io = c["initial_tool_outputs"]
            for k in ("ct", "mri", "body_imaging", "csf", "eeg", "specialized_test"):
                v = io.get(k)
                if v:
                    imp = v.get("impression") or v.get("interpretation") or ""
                    print(f"  {k}: {str(imp)[:500]}")
            for f in c["followup_outputs"]:
                print(f"  followup {f['trigger_action']}: {str(f['output'].get('impression', ''))[:300]}")
            print("  dx_support:", json.dumps(au.get("dx_support", {}))[:300])
            print("  discharge dx:", c["metadata"]["diagnosis_source"].get("discharge_diagnosis", "")[:300])


if __name__ == "__main__":
    main()
