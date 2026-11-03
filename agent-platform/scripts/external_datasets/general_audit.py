"""Domain-agnostic fit of MIMIC-IV (demo) and MedLoCoMo to the NeuroAgent episode format.

Same question as the neuro audits, without the neurology filter: is an admission a diagnostic
episode, i.e. an unplanned presentation whose principal diagnosis is new to the patient, with
results an agent could request and a final diagnosis to score? One row per admission, booleans
and counts only (MedLoCoMo note text never leaves the script).

    uv run --no-project --with pandas python -I \
        agent-platform/scripts/external_datasets/general_audit.py data/external outputs/external_datasets
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from medlocomo_audit import HPI_RESULT_LEAK
from mimic_neuro import dx_family, icd_chapter, physical_exam, sections

PLANNED = {"ELECTIVE", "SURGICAL SAME DAY ADMISSION"}
DIAGNOSTIC_ORDERS = {"Radiology", "Cardiology", "Neurology"}
# Chief complaints that already carry a diagnosis rather than a symptom, or come from another
# hospital whose work-up the agent would not see.
DX_ABBREVIATIONS = re.compile(
    r"\b(SDH|SAH|ICH|CVA|PNA|UTI|CHF|COPD|GIB|UGIB|LGIB|DKA|PE|DVT|MI|STEMI|NSTEMI|ESRD|CKD|AKI|"
    r"CA|CANCER|FX|FRACTURE|BLEED|HEAD BLEED|PANCREATITIS|APPENDICITIS|CHOLECYSTITIS|SEPSIS|CELLULITIS|"
    r"PNEUMONIA|OVERDOSE|OD|S/P|ETOH|TRANSFER)\b",
    re.IGNORECASE,
)
GENERIC = {"unspecified", "other", "without", "with", "mention", "acute", "chronic", "disease", "disorder", "elsewhere", "classified"}


def names_diagnosis(cc: str, title: str) -> bool:
    """Heuristic: the chief complaint states the diagnosis (abbreviation or a word of the ICD title)."""
    if not cc:
        return False
    if DX_ABBREVIATIONS.search(cc):
        return True
    words = {w for w in re.findall(r"[a-z]{5,}", title.lower()) if w not in GENERIC}
    return any(w in cc.lower() for w in words)


def mimic_demo(root: Path) -> pd.DataFrame:
    h, e = root / "mimic-iv-demo/hosp", root / "mimic-iv-ed-demo/ed"
    adm = pd.read_csv(h / "admissions.csv.gz", parse_dates=["admittime"])
    dx = pd.read_csv(h / "diagnoses_icd.csv.gz", dtype={"icd_code": str})
    titles = pd.read_csv(h / "d_icd_diagnoses.csv.gz", dtype={"icd_code": str})
    dx = dx.merge(titles, on=["icd_code", "icd_version"], how="left")
    lab = pd.read_csv(h / "labevents.csv.gz", parse_dates=["charttime"], usecols=["hadm_id", "itemid", "charttime"])
    micro = pd.read_csv(h / "microbiologyevents.csv.gz", usecols=["hadm_id"])
    poe = pd.read_csv(h / "poe.csv.gz", usecols=["hadm_id", "order_type", "order_subtype"])
    tri = pd.read_csv(e / "edstays.csv.gz").merge(pd.read_csv(e / "triage.csv.gz"), on=["subject_id", "stay_id"])
    adm = adm.sort_values("admittime")
    seen: dict[int, set[str]] = {}
    rows = []
    for a in adm.itertuples():
        d = dx[dx.hadm_id == a.hadm_id].sort_values("seq_num")
        prior = seen.setdefault(a.subject_id, set())
        if d.empty:
            continue
        p = d.iloc[0]
        t = tri[tri.hadm_id == a.hadm_id]
        cc = str(t.chiefcomplaint.iloc[0]) if not t.empty and pd.notna(t.chiefcomplaint.iloc[0]) else ""
        a_lab = lab[(lab.hadm_id == a.hadm_id) & (lab.charttime <= a.admittime + pd.Timedelta(hours=24))]
        orders = poe[(poe.hadm_id == a.hadm_id) & poe.order_type.isin(DIAGNOSTIC_ORDERS)]
        row = {
            "hadm_id": a.hadm_id,
            "chapter": icd_chapter(p.icd_code, p.icd_version),
            "principal": f"{p.icd_version}:{p.icd_code} {str(p.long_title)[:55]}",
            "unplanned": a.admission_type not in PLANNED,
            "not_transfer": not str(a.admission_location).startswith("TRANSFER"),
            "ed_chief_complaint": cc,
            "cc_names_dx": names_diagnosis(cc, str(p.long_title)),
            "new_dx": dx_family(p.icd_code) not in prior,
            "labs_24h": a_lab.itemid.nunique(),
            "diagnostic_orders": len(orders),
            "order_kinds": ";".join(sorted(set(orders.order_subtype.dropna()))),
            "micro": int((micro.hadm_id == a.hadm_id).sum()),
        }
        row["episode"] = bool(
            row["unplanned"] and row["not_transfer"] and cc and not row["cc_names_dx"] and row["new_dx"]
            and row["labs_24h"] >= 5 and (row["diagnostic_orders"] or row["micro"])
        )
        rows.append(row)
        prior.update(dx_family(c) for c in d.icd_code)
    return pd.DataFrame(rows)


def medlocomo(src: Path) -> pd.DataFrame:
    packets = [json.loads(p.read_text()) for p in sorted(src.glob("*/*/formed_packet.json"))]
    packets.sort(key=lambda d: (d["subject_id"], d["admission_start"]))
    seen: dict[str, set[str]] = {}
    rows = []
    for d in packets:
        prior = seen.setdefault(d["subject_id"], set())
        dx = sorted(d["diagnoses"], key=lambda x: x["seq_num"])
        note = "\n".join(n["text"] for n in d["discharge_notes"])
        sec = sections(note)
        hpi = sec.get("History of Present Illness", "")
        if dx:
            p = dx[0]
            row = {
                "hadm_id": d["hadm_id"],
                "chapter": icd_chapter(p["icd_code"], p["icd_version"]),
                "principal": f'{p["icd_version"]}:{p["icd_code"]} {p["long_title"][:55]}',
                "new_dx": dx_family(p["icd_code"]) not in prior,
                "cc_names_dx": names_diagnosis(sec.get("Chief Complaint", ""), p["long_title"]),
                "hpi_chars": len(hpi),
                "hpi_has_results": bool(HPI_RESULT_LEAK.search(hpi)),
                "pe_chars": len(physical_exam(note)),
                "has_results": bool(sec.get("Pertinent Results")),
                "n_radiology": len(d["radiology_notes"]),
                "n_microbiology": len(d["microbiology"]),
                "elective": bool(re.search(r"elective|scheduled|planned admission", hpi[:400], re.IGNORECASE)),
            }
            row["episode"] = bool(
                row["new_dx"] and not row["cc_names_dx"] and not row["elective"] and row["hpi_chars"] > 200
                and row["pe_chars"] > 100 and row["has_results"] and (row["n_radiology"] or row["n_microbiology"])
            )
            rows.append(row)
        prior.update(dx_family(x["icd_code"]) for x in dx)
    return pd.DataFrame(rows)


def summarise(name: str, df: pd.DataFrame) -> None:
    ep = df[df.episode]
    print(f"\n== {name}: {len(df)} admissions, {len(ep)} diagnostic episodes ({len(ep) / len(df):.1%})")
    for col in [c for c in ("unplanned", "not_transfer", "new_dx", "cc_names_dx", "hpi_has_results") if c in df]:
        print(f"  {col}: {int(df[col].sum())}")
    print("  episodes by ICD chapter:", Counter(ep.chapter).most_common())
    if "hpi_has_results" in ep:
        print(f"  episodes whose HPI already states results: {int(ep.hpi_has_results.sum())}")


def main(root: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    demo = mimic_demo(root)
    demo.to_csv(out / "mimic_demo_general.csv", index=False)
    summarise("MIMIC-IV demo", demo)
    loco = medlocomo(root / "medlocomo/repo/MedLoCoMo")
    loco.to_csv(out / "medlocomo_general.csv", index=False)
    summarise("MedLoCoMo", loco)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
