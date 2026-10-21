"""Per-admission fit of MIMIC-IV (structured modules) to the NeuroBench format, on the open demo.

The demo (100 patients, ODbL) has the schema of the full hosp/icu/ed modules but no notes, so
this measures what the structured tables alone can serve as tool outputs, and which studies
exist only as an order whose result lives in the credentialed Note module.

    uv run --no-project --with pandas python -I \
        agent-platform/scripts/external_datasets/mimic_demo_audit.py \
        data/external outputs/external_datasets/mimic_demo.csv
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mimic_neuro import neuro_condition

# poe order subtype -> NeuroBench tool. Results for these come from notes (radiology) or
# nowhere in MIMIC-IV (EEG, ECG and echo reports are separate modules or absent).
ORDER_TOOLS = {
    "CT Scan": "order_ct_scan",
    "MRI": "analyze_brain_mri",
    "ECG": "analyze_ecg",
    "Echo": "order_echocardiogram",
    "Telemetry": "order_cardiac_monitoring",
    "Ultrasound": "order_body_imaging",
    "General Xray": "order_body_imaging",
    "Noninvasive Vascular": "order_advanced_imaging",
    "Interventional Radiology": "order_advanced_imaging",
}
GCS_ITEMS = {220739, 223900, 223901}  # GCS eye, verbal, motor (icu/chartevents)
NEURO_ITEMS_LABEL = ("GCS", "Pupil", "Strength", "Orientation", "Speech", "Sensation", "LOC")


def load(root: Path) -> dict[str, pd.DataFrame]:
    h, i, e = root / "mimic-iv-demo/hosp", root / "mimic-iv-demo/icu", root / "mimic-iv-ed-demo/ed"
    t = {
        "adm": pd.read_csv(h / "admissions.csv.gz", parse_dates=["admittime", "dischtime"]),
        "pat": pd.read_csv(h / "patients.csv.gz"),
        "dx": pd.read_csv(h / "diagnoses_icd.csv.gz", dtype={"icd_code": str}),
        "dxd": pd.read_csv(h / "d_icd_diagnoses.csv.gz", dtype={"icd_code": str}),
        "lab": pd.read_csv(h / "labevents.csv.gz", parse_dates=["charttime"]),
        "labd": pd.read_csv(h / "d_labitems.csv.gz"),
        "micro": pd.read_csv(h / "microbiologyevents.csv.gz"),
        "poe": pd.read_csv(h / "poe.csv.gz", parse_dates=["ordertime"]),
        "proc": pd.read_csv(h / "procedures_icd.csv.gz", dtype={"icd_code": str}),
        "rx": pd.read_csv(h / "prescriptions.csv.gz", low_memory=False),
        "chart": pd.read_csv(i / "chartevents.csv.gz", usecols=["hadm_id", "itemid", "value"]),
        "items": pd.read_csv(i / "d_items.csv.gz"),
        "ed": pd.read_csv(e / "edstays.csv.gz"),
        "triage": pd.read_csv(e / "triage.csv.gz"),
    }
    return t


def audit(t: dict[str, pd.DataFrame]) -> pd.DataFrame:
    titles = dict(zip(t["dxd"].icd_code + "/" + t["dxd"].icd_version.astype(str), t["dxd"].long_title))
    lab = t["lab"].merge(t["labd"][["itemid", "fluid", "label"]], on="itemid")
    neuro_items = set(
        t["items"][t["items"].label.str.contains("|".join(NEURO_ITEMS_LABEL), na=False)].itemid
    )
    ed = t["ed"].merge(t["triage"], on=["subject_id", "stay_id"])
    rows = []
    for adm in t["adm"].itertuples():
        dx = t["dx"][t["dx"].hadm_id == adm.hadm_id].sort_values("seq_num")
        if dx.empty:
            continue
        conds = [neuro_condition(r.icd_code, r.icd_version) for r in dx.itertuples()]
        if not any(conds):
            continue
        p = dx.iloc[0]
        a_lab = lab[lab.hadm_id == adm.hadm_id]
        first24 = a_lab[a_lab.charttime <= adm.admittime + pd.Timedelta(hours=24)]
        orders = t["poe"][t["poe"].hadm_id == adm.hadm_id]
        subtypes = Counter(orders.order_subtype.dropna())
        chart = t["chart"][t["chart"].hadm_id == adm.hadm_id]
        tri = ed[ed.hadm_id == adm.hadm_id]
        rows.append(
            {
                "subject_id": adm.subject_id,
                "hadm_id": adm.hadm_id,
                "admission_type": adm.admission_type,
                "principal": f"{p.icd_version}:{p.icd_code} {titles.get(f'{p.icd_code}/{p.icd_version}', '')[:60]}",
                "principal_condition": conds[0] or "",
                "neuro_rank": next(i + 1 for i, c in enumerate(conds) if c),
                "neuro_codes": ";".join(sorted({c for c in conds if c})),
                "ed_triage": not tri.empty,
                "ed_chief_complaint": tri.chiefcomplaint.iloc[0] if not tri.empty else "",
                "labs_first24h": first24.itemid.nunique(),
                "csf_labs": a_lab[a_lab.fluid == "Cerebrospinal Fluid"].itemid.nunique(),
                "micro_specimens": ";".join(sorted(set(t["micro"][t["micro"].hadm_id == adm.hadm_id].spec_type_desc))),
                "icu_gcs": bool(chart.itemid.isin(GCS_ITEMS).any()),
                "icu_neuro_items": int(chart.itemid.isin(neuro_items).sum()),
                "orders": ";".join(f"{k}:{v}" for k, v in sorted(subtypes.items()) if k in ORDER_TOOLS),
                "neurology_orders": int((orders.order_type == "Neurology").sum()),
                "consults": int((orders.order_type == "Consults").sum()),
                "n_prescriptions": int((t["rx"].hadm_id == adm.hadm_id).sum()),
            }
        )
    return pd.DataFrame(rows)


def main(root: Path, out: Path) -> None:
    t = load(root)
    df = audit(t)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    n_adm = t["adm"].hadm_id.nunique()
    print(f"admissions {n_adm}; with any neuro code {len(df)}; neuro principal {(df.neuro_rank == 1).sum()}; "
          f"neuro in top 2 {(df.neuro_rank <= 2).sum()}")
    print("principal neuro conditions:", Counter(df[df.neuro_rank == 1].principal_condition).most_common())
    top = df[df.neuro_rank <= 2]
    for k in ("ed_triage", "icu_gcs"):
        print(f"  {k}: {top[k].sum()}/{len(top)}")
    print(f"  CSF labs: {(top.csf_labs > 0).sum()}/{len(top)}; neurology orders (EEG etc.): {(top.neurology_orders > 0).sum()}/{len(top)}")
    print(f"  CT ordered: {top.orders.str.contains('CT Scan').sum()}; MRI ordered: {top.orders.str.contains('MRI').sum()}; "
          f"ECG ordered: {top.orders.str.contains('ECG').sum()}; echo ordered: {top.orders.str.contains('Echo').sum()}")
    with pd.option_context("display.width", 250, "display.max_colwidth", 70):
        print(top[["hadm_id", "principal", "neuro_codes", "ed_chief_complaint", "labs_first24h", "csf_labs", "orders", "neurology_orders"]].to_string(index=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
