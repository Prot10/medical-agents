"""Per-admission fit of MedLoCoMo (MIMIC-IV v3.1 + Note v2.2 packets) to the NeuroBench format.

Reads every ``formed_packet.json`` and writes one row per admission with booleans and
lengths only: the note text never leaves this script (MIMIC-IV-Note is credentialed data,
see PhysioNet's LLM notice), so the audit can be read by anyone.

    python3 -I agent-platform/scripts/external_datasets/medlocomo_audit.py \
        data/external/medlocomo/repo/MedLoCoMo outputs/external_datasets/medlocomo.csv
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mimic_neuro import (
    HEAD_EXAM,
    NEURO_EXAM,
    STUDY_MENTIONS,
    neuro_condition,
    physical_exam,
    sections,
)

# Results already in the HPI: the discharge summary is written after the work-up.
HPI_RESULT_LEAK = re.compile(r"\b(CT|CTA|MRI|MRA|EEG|LP|CSF)\b[^.\n]{0,60}\b(show|reveal|demonstrat|notable|significant|without|negative|positive)", re.IGNORECASE)


def audit(packet: dict) -> dict:
    note = "\n".join(n["text"] for n in packet["discharge_notes"])
    sec = sections(note)
    hpi = sec.get("History of Present Illness", "")
    pe = physical_exam(note)
    neuro_lines = [ln for ln in pe.splitlines() if NEURO_EXAM.search(ln)]
    dx = sorted(packet["diagnoses"], key=lambda d: d["seq_num"])
    principal = dx[0] if dx else None
    cond = neuro_condition(principal["icd_code"], principal["icd_version"]) if principal else None
    secondary = [
        c for d in dx[1:3] if (c := neuro_condition(d["icd_code"], d["icd_version"])) is not None
    ]
    rad_titles = [r["text"].strip().split("\n")[0] for r in packet["radiology_notes"]]
    row = {
        "subject_id": packet["subject_id"],
        "hadm_id": packet["hadm_id"],
        "principal_icd": f'{principal["icd_version"]}:{principal["icd_code"]}' if principal else "",
        "principal_condition": cond or "",
        "neuro_in_top3": bool(cond or secondary),
        "has_chief_complaint": bool(sec.get("Chief Complaint")),
        "hpi_chars": len(hpi),
        "hpi_has_results": bool(HPI_RESULT_LEAK.search(hpi)),
        "pe_chars": len(pe),
        "neuro_exam_lines": len(neuro_lines),
        "has_pertinent_results": bool(sec.get("Pertinent Results")),
        "has_discharge_dx": bool(sec.get("Discharge Diagnosis")),
        "n_radiology": len(packet["radiology_notes"]),
        "n_head_spine_imaging": sum(bool(HEAD_EXAM.search(t)) for t in rad_titles)
        + sum(bool(HEAD_EXAM.search(r["text"][:300])) and not HEAD_EXAM.search(t) for r, t in zip(packet["radiology_notes"], rad_titles)),
        "n_microbiology": len(packet["microbiology"]),
    }
    for name, pat in STUDY_MENTIONS.items():
        row[f"note_mentions_{name}"] = bool(pat.search(note))
    return row


def main(src: Path, out: Path) -> None:
    rows = [audit(json.loads(p.read_text())) for p in sorted(src.glob("*/*/formed_packet.json"))]
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    neuro = [r for r in rows if r["principal_condition"]]
    bench = [r for r in neuro if not r["principal_condition"].startswith("other:")]
    print(f"admissions {len(rows)}, patients {len({r['subject_id'] for r in rows})}")
    print(f"neuro principal {len(neuro)} ({len({r['subject_id'] for r in neuro})} patients); "
          f"one of the 20 NeuroBench conditions {len(bench)}")
    print("principal conditions:", Counter(r["principal_condition"] for r in neuro).most_common())
    usable = [
        r for r in neuro
        if r["hpi_chars"] > 200 and r["neuro_exam_lines"] > 0 and r["has_pertinent_results"]
    ]
    print(f"neuro principal with HPI>200 chars + neuro exam + results: {len(usable)}")
    for k in ("hpi_has_results", "note_mentions_eeg", "note_mentions_csf", "note_mentions_ecg", "note_mentions_echo", "note_mentions_emg"):
        print(f"  {k}: {sum(r[k] for r in neuro)}/{len(neuro)}")
    print(f"  with head/spine imaging report: {sum(r['n_head_spine_imaging'] > 0 for r in neuro)}/{len(neuro)}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
