"""Prototype: one MIMIC-IV admission -> a NeuroBench v2 case (draft), plus a gap report.

Serves what the structured modules hold (ED triage, home medications, labs, CSF, microbiology,
MIMIC-IV-ECG machine reads) and fills the narrative fields (HPI, neuro exam, imaging reports)
from MIMIC-IV-Note when ``--notes`` points at it. The policy is transferred from a NeuroBench
case of the same condition and kept ``draft``; the clinicians' real orders are stored next to
it as a reference trajectory. Credentialed inputs must only run on local or CERN-hosted models.

    uv run --no-project --with pandas --with pydantic python -I \
        agent-platform/scripts/external_datasets/mimic_to_neurobench.py \
        --root data/external --hadm 22484749 --template data/neurobench/cases/ISCH-STR-M01.json \
        --out outputs/external_datasets/cases
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mimic_neuro import physical_exam, sections

ORDER_TOOLS = {
    ("Radiology", "CT Scan"): "order_ct_scan",
    ("Radiology", "MRI"): "analyze_brain_mri",
    ("Radiology", "Noninvasive Vascular"): "order_advanced_imaging",
    ("Radiology", "Interventional Radiology"): "order_advanced_imaging",
    ("Radiology", "Ultrasound"): "order_body_imaging",
    ("Radiology", "General Xray"): "order_body_imaging",
    ("Cardiology", "ECG"): "analyze_ecg",
    ("Cardiology", "Echo"): "order_echocardiogram",
    ("Cardiology", "Telemetry"): "order_cardiac_monitoring",
    ("General Care", "Telemetry"): "order_cardiac_monitoring",
    ("Neurology", "EEG"): "analyze_eeg",
    ("Neurology", "EMG"): "order_specialized_test",
    ("Neurology", "TCD"): "order_advanced_imaging",
    ("Lab", None): "interpret_labs",
}
# Where each tool's result comes from in MIMIC-IV; None = no result anywhere in MIMIC-IV.
RESULT_SOURCE = {
    "interpret_labs": "hosp/labevents",
    "analyze_csf": "hosp/labevents (CSF fluid) + microbiologyevents",
    "order_microbiology": "hosp/microbiologyevents",
    "analyze_ecg": "MIMIC-IV-ECG machine_measurements (open access, machine read)",
    "order_ct_scan": "MIMIC-IV-Note radiology (credentialed)",
    "analyze_brain_mri": "MIMIC-IV-Note radiology (credentialed)",
    "order_advanced_imaging": "MIMIC-IV-Note radiology (credentialed)",
    "order_body_imaging": "MIMIC-IV-Note radiology (credentialed)",
    "order_echocardiogram": "MIMIC-IV-Echo measurements (subset) / discharge note text",
    "perform_clinical_assessment": "discharge note exam + icu/chartevents (GCS, pupils)",
    "analyze_eeg": None,
    "order_cardiac_monitoring": None,
    "order_specialized_test": None,
    "obtain_tissue_diagnosis": None,
}
OUTPUT_KEY = {
    "interpret_labs": "labs", "analyze_csf": "csf", "order_microbiology": "microbiology",
    "analyze_ecg": "ecg", "order_ct_scan": "ct", "analyze_brain_mri": "mri",
    "order_advanced_imaging": "advanced_imaging", "order_body_imaging": "body_imaging",
    "order_echocardiogram": "echo", "order_cardiac_monitoring": "cardiac_monitoring",
    "analyze_eeg": "eeg", "order_specialized_test": "specialized_test",
    "obtain_tissue_diagnosis": "tissue_diagnosis", "perform_clinical_assessment": "clinical_assessment",
}


def read(root: Path, rel: str, **kw) -> pd.DataFrame:
    return pd.read_csv(root / rel, low_memory=False, **kw)


def lab_value(r) -> dict:
    lo, hi = r.ref_range_lower, r.ref_range_upper
    value = r.valuenum if pd.notna(r.valuenum) else str(r.value)
    return {
        "test": r.label,
        "value": float(value) if isinstance(value, float) else value,
        "unit": "" if pd.isna(r.valueuom) else str(r.valueuom),
        "reference_range": f"{lo:g}-{hi:g}" if pd.notna(lo) and pd.notna(hi) else "",
        "is_abnormal": r.flag == "abnormal",
    }


def convert(args) -> tuple[dict, dict]:
    root = Path(args.root)
    h = "mimic-iv-demo/hosp/" if not args.full else "mimic-iv/hosp/"
    adm = read(root, h + "admissions.csv.gz", parse_dates=["admittime", "dischtime"])
    a = adm[adm.hadm_id == args.hadm].iloc[0]
    pat = read(root, h + "patients.csv.gz").set_index("subject_id").loc[a.subject_id]
    ed = read(root, "mimic-iv-ed-demo/ed/edstays.csv.gz", parse_dates=["intime"])
    ed = ed[ed.hadm_id == args.hadm]
    t0 = ed.intime.min() if not ed.empty else a.admittime
    window_end = a.admittime + pd.Timedelta(hours=24)
    gaps: dict[str, str] = {}

    # Presentation ------------------------------------------------------------------------
    tri = read(root, "mimic-iv-ed-demo/ed/triage.csv.gz")
    tri = tri[tri.stay_id.isin(ed.stay_id)]
    vitals = None
    if not tri.empty:
        r = tri.iloc[0]
        # A vital left blank at triage stays None: the prompt names it as not recorded.
        num = lambda v: int(v) if pd.notna(v) else None
        vitals = {
            "bp_systolic": num(r.sbp), "bp_diastolic": num(r.dbp), "hr": num(r.heartrate),
            "temp": round((float(r.temperature) - 32) * 5 / 9, 1) if pd.notna(r.temperature) else None,
            "rr": num(r.resprate), "spo2": num(r.o2sat),
        }
        missing = [k for k, v in vitals.items() if v is None]
        if missing:
            gaps["vitals"] = f"not recorded at triage: {', '.join(missing)}"
    else:
        gaps["vitals"] = "no ED triage; first ICU charted vitals would be used"
    medrec = read(root, "mimic-iv-ed-demo/ed/medrecon.csv.gz")
    meds = [
        {"drug": n, "dose": "", "frequency": "", "indication": ""}
        for n in medrec[medrec.stay_id.isin(ed.stay_id)].name.drop_duplicates().head(25)
    ]
    note = ""
    if args.notes:
        notes = read(Path(args.notes), "note/discharge.csv.gz")
        note = "\n".join(notes[notes.hadm_id == args.hadm].text)
    sec = sections(note) if note else {}
    for f in ("history_present_illness", "neurological_exam", "past_medical_history"):
        if not note:
            gaps[f] = "MIMIC-IV-Note discharge summary (credentialed) not available"

    patient = {
        "patient_id": f"MIMIC-{a.subject_id}",
        "demographics": {
            "age": int(pat.anchor_age + (a.admittime.year - pat.anchor_year)),
            "sex": "female" if pat.gender == "F" else "male",
            "handedness": "",
        },
        "clinical_history": {
            "past_medical_history": [s.strip() for s in sec.get("Past Medical History", "").splitlines() if s.strip()],
            "medications": meds,
            "allergies": [s.strip() for s in sec.get("Allergies", "").split(",") if s.strip()],
        },
        "neurological_exam": {"additional": physical_exam(note)} if note else {},
        "vitals": vitals or {},
        "chief_complaint": tri.chiefcomplaint.iloc[0] if not tri.empty else sec.get("Chief Complaint", ""),
        "history_present_illness": sec.get("History of Present Illness", ""),
    }

    # Tool outputs from structured tables ---------------------------------------------------
    labs = read(root, h + "labevents.csv.gz", parse_dates=["charttime"])
    labs = labs.merge(read(root, h + "d_labitems.csv.gz"), on="itemid")
    labs = labs[(labs.hadm_id == args.hadm) | ((labs.subject_id == a.subject_id) & labs.hadm_id.isna())]
    labs = labs[(labs.charttime >= t0 - pd.Timedelta(hours=1)) & (labs.charttime <= window_end)]
    # First instance of each test, as in MIMIC-IV-Ext-CDM: the therapy-naive value.
    first = labs.sort_values("charttime").drop_duplicates("itemid")
    blood = first[first.fluid != "Cerebrospinal Fluid"]
    outputs: dict[str, dict] = {}
    if not blood.empty:
        panels = {cat: [lab_value(r) for r in g.itertuples()] for cat, g in blood.groupby("category")}
        abnormal = [f"{v['test']} {v['value']} {v['unit']}".strip() for p in panels.values() for v in p if v["is_abnormal"]]
        outputs["labs"] = {"panels": panels, "abnormal_values_summary": abnormal,
                           "interpretation": "Values as resulted; no clinical interpretation in the source."}
    csf = labs[labs.fluid == "Cerebrospinal Fluid"].sort_values("charttime").drop_duplicates("itemid")
    micro = read(root, h + "microbiologyevents.csv.gz")
    micro = micro[micro.hadm_id == args.hadm]
    if not csf.empty:
        get = lambda pat: "; ".join(f"{r.label} {r.value} {'' if pd.isna(r.valueuom) else r.valueuom}".strip() for r in csf.itertuples() if re.search(pat, r.label, re.IGNORECASE))
        csf_micro = micro[micro.spec_type_desc.str.contains("CSF", na=False)]
        outputs["csf"] = {
            "appearance": get("color|appearance|clarity"), "opening_pressure": "not recorded in structured data",
            "cell_count": {r.label: f"{r.value} {'' if pd.isna(r.valueuom) else r.valueuom}".strip() for r in csf.itertuples() if re.search("wbc|rbc|nucleated|poly|lymph|mono|macrophage", r.label, re.IGNORECASE)},
            "protein": get("protein"), "glucose": get("glucose"),
            "special_tests": {f"{r.test_name}": str(r.org_name if pd.notna(r.org_name) else "no growth / negative") for r in csf_micro.itertuples()},
            "interpretation": "Values as resulted; no clinical interpretation in the source.",
        }
    other_micro = micro[~micro.spec_type_desc.str.contains("CSF", na=False)]
    if not other_micro.empty:
        outputs["microbiology"] = {
            "specimen": "; ".join(sorted(set(other_micro.spec_type_desc))),
            "tests": sorted(set(other_micro.test_name.dropna())),
            "organism": "; ".join(sorted(set(other_micro.org_name.dropna()))) or None,
            "impression": "Cultures as resulted.",
        }
    ecg_path = root / "mimic-iv-ecg/machine_measurements.csv"
    if ecg_path.exists():
        try:
            ecg = pd.read_csv(ecg_path, parse_dates=["ecg_time"], low_memory=False)
            ecg = ecg[(ecg.subject_id == a.subject_id) & (ecg.ecg_time >= t0 - pd.Timedelta(hours=1)) & (ecg.ecg_time <= window_end)]
        except (pd.errors.ParserError, ValueError, KeyError) as exc:  # partial download
            ecg, gaps["ecg"] = pd.DataFrame(), f"MIMIC-IV-ECG table unreadable ({exc.__class__.__name__})"
        if not ecg.empty:
            r = ecg.sort_values("ecg_time").iloc[0]
            lines = [str(r[c]) for c in ecg.columns if c.startswith("report_") and pd.notna(r[c])]
            outputs["ecg"] = {
                "rhythm": lines[0] if lines else "", "rate": int(60000 / r.rr_interval) if r.rr_interval else 0,
                # Fiducial points are ms offsets in the 10 s strip; intervals are their differences.
                "intervals": {
                    name: f"{r[b] - r[a]:.0f} ms"
                    for name, a, b in (("PR", "p_onset", "qrs_onset"), ("QRS", "qrs_onset", "qrs_end"), ("QT", "qrs_onset", "t_end"))
                    if pd.notna(r[a]) and pd.notna(r[b]) and r[a] < 29999 and r[b] < 29999
                },
                "axis": str(r.get("qrs_axis", "")), "findings": lines[1:], "interpretation": " ".join(lines),
            }
    for tool, src in RESULT_SOURCE.items():
        if OUTPUT_KEY[tool] not in outputs and tool not in ("perform_clinical_assessment",):
            if src and "credentialed" not in src and "note" not in src:
                src = f"not performed in this admission ({src})"
            gaps.setdefault(OUTPUT_KEY[tool], src or "no result for this study anywhere in MIMIC-IV")

    # Clinician trajectory (reference, not policy) ------------------------------------------
    poe = read(root, h + "poe.csv.gz", parse_dates=["ordertime"])
    poe = poe[poe.hadm_id == args.hadm].sort_values("ordertime")
    trajectory = []
    for r in poe.itertuples():
        tool = ORDER_TOOLS.get((r.order_type, r.order_subtype)) or ORDER_TOOLS.get((r.order_type, None))
        if tool and (not trajectory or trajectory[-1]["tool"] != tool):
            trajectory.append({"t_hours": round((r.ordertime - t0).total_seconds() / 3600, 1), "tool": tool, "order": f"{r.order_type}/{r.order_subtype}"})

    # Ground truth: diagnosis from ICD, policy transferred from a same-condition case ------
    dx = read(root, h + "diagnoses_icd.csv.gz", dtype={"icd_code": str})
    dx = dx[dx.hadm_id == args.hadm].sort_values("seq_num")
    template = json.loads(Path(args.template).read_text())
    gt = template["ground_truth"]
    gt["review_status"] = "draft"
    p = dx.iloc[0]
    gt["diagnosis"]["accepted"] = gt["diagnosis"]["accepted"][1:]  # drop the template's case-specific label
    if p.icd_version == 10:
        gt["diagnosis"]["icd_codes"] = sorted({f"{p.icd_code[:3]}.{p.icd_code[3:]}".rstrip("."), *gt["diagnosis"]["icd_codes"]})
    gt["key_clinical_evidence"], gt["red_herrings"] = [], []
    served = {OUTPUT_KEY.get(t) for t in RESULT_SOURCE} & set(outputs)
    coverage = []
    for c in gt["action_criteria"]:
        tool = c["alternatives"][0]["tool_name"]
        key = OUTPUT_KEY.get(tool)
        coverage.append({
            "criterion": c["criterion_id"], "importance": c["importance"], "tool": tool,
            "real_result": key in served if key else "knowledge tool",
            "clinician_ordered": any(s["tool"] == tool for s in trajectory),
        })

    case = {
        "schema_version": "2.0",
        "case_id": f"MIMIC-{template['case_id'].split('-')[0]}-{args.hadm}",
        # A real admission: orders the clinicians did not place are answered "not available".
        "provenance": "record",
        "condition": template["condition"],
        "difficulty": "moderate",
        "encounter_type": "emergency" if not ed.empty else "inpatient",
        "patient": patient,
        "initial_tool_outputs": outputs,
        "ground_truth": gt,
        "metadata": {"source": "MIMIC-IV v2.2 demo" if not args.full else "MIMIC-IV v3.1",
                     "hadm_id": int(args.hadm), "policy_template": template["case_id"],
                     "principal_icd": f"ICD-{p.icd_version} {p.icd_code}"},
    }
    report = {"gaps": gaps, "clinician_trajectory": trajectory, "policy_coverage": coverage}
    return case, report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--hadm", type=int, required=True)
    ap.add_argument("--template", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--notes", help="MIMIC-IV-Note root (credentialed)")
    ap.add_argument("--full", action="store_true", help="read the full MIMIC-IV instead of the demo")
    args = ap.parse_args()
    case, report = convert(args)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{case['case_id']}.json").write_text(json.dumps(case, indent=1, default=str))
    (out / f"{case['case_id']}.gaps.json").write_text(json.dumps(report, indent=1, default=str))
    print(json.dumps(report, indent=1, default=str))


if __name__ == "__main__":
    main()
