"""Assemble pilot NeuroBench cases from a MIMIC source bundle and a hand-written manual file.

Used by ``mimic_build_case.py`` (stages ``draft`` and ``build``). No record content here.

Sources per served answer (``metadata.served``, hidden from the agent):
  table          a structured row (labevents, microbiologyevents) or a radiology report section;
  note_extracted findings written from the discharge note by the reader (EEG, ECG, echo, ...).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

# Top-level discharge-summary sections, in document order.
TOP = ["Allergies", "Chief Complaint", "Major Surgical or Invasive Procedure", "History of Present Illness",
       "Past Medical History", "Social History", "Family History", "Physical Exam", "Pertinent Results",
       "Brief Hospital Course", "Medications on Admission", "Discharge Medications", "Discharge Disposition",
       "Discharge Diagnosis", "Discharge Condition", "Discharge Instructions", "Followup Instructions"]
_TOP = re.compile(r"(?m)^\s*(" + "|".join(re.escape(t) for t in TOP) + r"|Physical ___|___ of Present Illness|History of ___ Illness)\s*:")
DISCHARGE_EXAM = re.compile(r"(?im)^\s*[=\-* ]*(?:(?:discharge|on discharge|at discharge|upon discharge)\s*"
                            r"(?:physical\s*|neuro(?:logical|logic)?\s*)?(?:exam(?:ination)?|PE)\b"
                            r"|(?:physical\s*|neuro(?:logical|logic)?\s*)?exam(?:ination)?\s+(?:on|at|upon)\s+discharge"
                            r"|(?:on|at|upon)\s+discharge\s*:?\s*$)")


def sections(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    marks = list(_TOP.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[m.end():end].strip()
        name = {"Physical ___": "Physical Exam", "___ of Present Illness": "History of Present Illness",
                "History of ___ Illness": "History of Present Illness"}.get(m.group(1), m.group(1))  # de-identified headers
        if name in out and name in ("History of Present Illness", "Physical Exam"):
            out[name] += "\n\n" + body  # a note may carry the HPI under two headers
        else:
            out.setdefault(name, body)
    return out


def admission_exam(exam: str) -> str:
    m = DISCHARGE_EXAM.search(exam)
    return exam[: m.start()].strip() if m else exam.strip()


_MED = re.compile(r"^\s*(?:\d+\.\s*)?(?P<drug>[A-Za-z][A-Za-z0-9 \-/()]*?)\s+(?P<dose>\d[\d.,]*(?:\s*-\s*\d[\d.,]*)?\s*"
                  r"(?:mg|mcg|g|gram|units?|mL|%|meq|puffs?|tabs?|caps?|pkt|ptch|drops?|neb)\b[^ ]*(?:/\w+)?)\s*(?P<freq>.*)$", re.I)


def parse_medications(block: str) -> list[dict]:
    meds = []
    # A numbered entry may wrap onto the next line: join continuation lines first.
    lines: list[str] = []
    for line in block.splitlines():
        if lines and line.strip() and not re.match(r"^\s*\d+\.", line) and re.match(r"^\s*\d+\.", lines[-1]):
            lines[-1] = lines[-1].rstrip() + " " + line.strip()
        else:
            lines.append(line)
    for line in lines:
        line = line.strip()
        if not line or re.match(r"(?i)^(the preadmission|preadmission|none|___$)", line):
            continue
        m = _MED.match(line)
        if m:
            meds.append({"drug": m["drug"].strip(), "dose": m["dose"].strip(), "frequency": m["freq"].strip(), "indication": ""})
        else:
            meds.append({"drug": re.sub(r"^\d+\.\s*", "", line), "dose": "", "frequency": "", "indication": ""})
    return meds


def ts(x) -> pd.Timestamp | None:
    return pd.Timestamp(x) if x not in (None, "", "NaT", "None") and not (isinstance(x, float) and pd.isna(x)) else None


def hours(t, t_ed) -> float | None:
    t = ts(t)
    return None if t is None else round((t - t_ed).total_seconds() / 3600, 1)


FINDINGS = re.compile(r"(?is)\bFINDINGS?\s*:(.*?)(?=\n\s*(?:IMPRESSION|CONCLUSION|NOTIFICATION|RECOMMENDATION|"
                      r"ADDENDUM|PROVISIONAL FINDINGS IMPRESSION|DR\.)\b|\Z)")


def findings_only(report: str) -> str:
    m = FINDINGS.search(report or "")
    return re.sub(r"[ \t]+", " ", m.group(1)).strip() if m else ""


def anchor(bundle: dict) -> pd.Timestamp:
    """Time 0: ED arrival, else admission."""
    eds = [ts(e["intime"]) for e in bundle["edstays"] if ts(e["intime"])]
    adm = ts(bundle["admission"][0]["admittime"])
    return min(eds) if eds else adm


# ============================================================================================
# draft
# ============================================================================================
def draft(bundle: dict) -> dict:
    t_ed = anchor(bundle)
    adm = bundle["admission"][0]
    note = bundle["discharge"][0]["text"]
    sec = sections(note)
    rad = []
    for r in bundle["radiology"]:
        rad.append({"note_id": r["note_id"], "exam": r["exam_name"], "t_h": hours(r["charttime"], t_ed),
                    "findings": findings_only(r["text"]), "hadm_match": r.get("hadm_id")})
    return {
        "case_id": bundle["case_id"], "t_admit_h": hours(adm["admittime"], t_ed), "t_disch_h": hours(adm["dischtime"], t_ed),
        "sections": sec, "admission_exam": admission_exam(sec.get("Physical Exam", "")),
        "medications": parse_medications(sec.get("Medications on Admission", "")),
        "radiology": rad,
    }


def stage_draft(a) -> None:
    out = Path(a.out)
    (out / "02_draft").mkdir(exist_ok=True)
    sel = pd.read_csv(out / getattr(a, "selection", "02_selection.csv"))
    for cid in sel[sel.case_id.notna() & (sel.case_id != "")].case_id:
        bundle = json.loads((out / "02_source" / f"{cid}.json").read_text())
        (out / "02_draft" / f"{cid}.json").write_text(json.dumps(draft(bundle), indent=1, default=str))
        print(f"{cid}: draft written", file=sys.stderr)


def stage_build(a) -> None:  # defined below
    from mimic_case_build import build_all
    build_all(a)
