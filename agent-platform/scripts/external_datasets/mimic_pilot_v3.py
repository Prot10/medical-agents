"""MIMIC-IV neurology pilot, task 03: the cohort and strict complete counts under Andrea's decisions
of 7 Nov 2026 (workspace CLAUDE.md, "Decisions"). Counts only on stdout; IDs only under OUT.

Stages
  cohort3   cohort of the 20 conditions with the new chief-complaint rule (decisions 7, 9) and the
            hidden-transfer filter (8); waterfall per condition and the marginal effect of 7, 8, 9.
            -> OUT/03_cohort_flags.csv, 03_waterfall.csv, 03_cc_classes.csv
  tables3   per-admission sources for the candidate conditions: lab panels in the window, CSF labs,
            blood cultures, radiology (first non-contrast CT exam, first CTA, whether the CTA report
            describes its non-contrast acquisition, first brain MRI, first spine MRI, chest CT),
            MIMIC-IV-ECG (first ECG in the window), rhythm coverage (ICU chartevents heart rhythm +
            ED vitalsign rhythm), ICU NIF / vital capacity, note result detectors, discharge
            diagnosis agreement with the condition. -> OUT/03_tables.parquet, 03_notes.parquet
  strict3   strict complete counts per condition (core policy steps from the NeuroBench cases), panels
            dropped by the 50 % rule (3), and the marginal effect of decisions 1, 2, 3, 5, 10, 11.
            -> OUT/03_strict.csv, 03_strict_marginal.csv, 03_panel_rule.csv

Windows (hours from ED arrival, t0 = ED arrival - 1 h): presentation studies (labs, non-contrast
CT, CTA, ECG) to admission + 24 h; rhythm to admission + 48 h; later studies (MRI, spine MRI, CSF,
EEG, EMG) over the stay. Rhythm coverage rule (decision 5): each rhythm record covers the time to
the next record when the gap is <= 4 h, else 1 h; covered >= 12 h counts.

    nice -n 10 uv run -q --no-project --with duckdb --with pandas --with pyarrow python -I \
        mimic_pilot_v3.py --stage cohort3|tables3|strict3 --out $W/out --tmp $W/tmp
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from general_audit import DX_ABBREVIATIONS  # noqa: E402
from mimic_neuro import neuro_condition  # noqa: E402
from mimic_note_results import DETECTORS, BROAD, detect, note_scope  # noqa: E402
from mimic_pilot_cohort import CONDITIONS, PANELS, connect, csv, paths, policy_steps  # noqa: E402

CANDIDATES = ["ISCH", "SAH", "SE", "GBS", "BACT", "MS", "ALS", "FEPI", "NMDAR", "MG"]

# --- chief complaint (decisions 7 and 9) -------------------------------------------------------
# A label that needs a test to be known, or a transfer / s/p: the work-up happened before arrival.
CC_TEST_LABEL = {
    "ISCH": r"\binfarct|\bLVO\b|\bELVO\b|thrombectomy|\btPA\b|hemorrhag|\bbleed|\bICH\b|\bSAH\b",
    "SAH": r"\bSAH\b|subarach|aneurysm|bleed|hemorrhag|haemorrhag|\bICH\b|\bIPH\b|\bIVH\b",
    "SE": r"\bNCSE\b|non-?convulsive\s+status",
    "BACT": r"mening|enceph|ventriculitis|neisseria|pneumococc|abscess",
    "GBS": r"\bGBS\b|guillain|barr[eé]|\bAIDP\b|\bCIDP\b|miller.?fisher|polyradic|demyelin",
    "MS": r"\bMS\b|multiple\s+sclerosis|demyelin|optic\s+neuritis|\bflare\b",
    "ALS": r"\bALS\b|amyotroph|motor\s+neuron|\bMND\b",
    "FEPI": r"epilep",
    "NMDAR": r"enceph|\bNMDA|teratoma|autoimmune",
    "MG": r"myasthen|\bMG\b|crisis",
}
# A label that comes from the symptoms: kept, the complaint is rewritten from the kept HPI.
CC_SYMPTOM_LABEL = {
    "ISCH": r"stroke|\bCVA\b|\bTIA\b|cerebrovascular",
    "SE": r"status\s+epi|\bin\s+status\b|\bSE\b",
}
CONVULSIVE = re.compile(r"(?i)convuls|tonic|clonic|\bGTC|shaking|jerking|seizing|seizure activity|rhythmic\s+movement")
GENERIC_TEST = re.compile(DX_ABBREVIATIONS.pattern.replace("CVA|", ""), re.I)  # CVA is a symptom label
TRANSFER = re.compile(r"\btransfer|\bs/p\b|\bOSH\b", re.I)
PLACEHOLDER = re.compile(r"^\s*(unknown-cc|unknown|none|nan|___)?\s*$", re.I)


def cc_class3(cc: str, cond: str, hpi_convulsive: bool) -> str:
    """missing | transfer | test_label | symptom_label | ok (a single triage complaint)."""
    cc = "" if cc is None or (isinstance(cc, float)) else str(cc)
    if PLACEHOLDER.match(cc):
        return "missing"
    if TRANSFER.search(cc):
        return "transfer"
    if re.search(CC_TEST_LABEL.get(cond, r"(?!)"), cc, re.I):
        return "test_label"
    if re.search(CC_SYMPTOM_LABEL.get(cond, r"(?!)"), cc, re.I):
        if cond == "SE" and not hpi_convulsive:
            return "test_label"  # 'status epilepticus' without a convulsive seizure in the HPI
        return "symptom_label"
    if GENERIC_TEST.search(cc):
        return "test_label"
    return "ok"


HPI_RX = (r"(?s)History of Present Illness:(.*?)\n\s*(Past Medical History|PMH|Review of Systems|ROS|"
          r"Past Surgical History|Social History|Family History|Physical Exam|Allergies)\s*:")


def stage_cohort3(a) -> None:
    p, con, out = paths(a.physionet), connect(a.tmp), Path(a.out)
    old = pd.read_csv(out / "01_cohort_flags.csv")
    df = old[["subject_id", "hadm_id", "condition", "admittime", "dischtime", "admission_location", "f_new",
              "f_not_transfer", "f_via_ed", "ed_intime", "f_note"]].copy()
    con.register("c", df[["hadm_id"]])
    # Every triage complaint of the ED stays of the admission.
    cc = con.execute(f"""
        select e.hadm_id, string_agg(coalesce(t.chiefcomplaint, ''), ' | ' order by e.intime) cc
        from {csv(p['ed'] / 'edstays.csv.gz')} e join c using (hadm_id)
        left join {csv(p['ed'] / 'triage.csv.gz')} t using (subject_id, stay_id) group by 1""").df()
    hidden = set(con.execute(f"""
        select distinct d.hadm_id from {csv(p['hosp'] / 'diagnoses_icd.csv.gz')} d join c using (hadm_id)
        where (d.icd_version = 9 and d.icd_code = 'V4588') or (d.icd_version = 10 and d.icd_code = 'Z9282')""").df().hadm_id)
    df = df.merge(cc, on="hadm_id", how="left")
    # HPI convulsive-seizure check, only where an SE complaint says status epilepticus.
    need = df[(df.condition == "SE") & df.cc.fillna("").str.contains(CC_SYMPTOM_LABEL["SE"], case=False, regex=True)].hadm_id
    con.register("need", pd.DataFrame({"hadm_id": need}))
    hp = con.execute(f"""select hadm_id, regexp_extract(text, '{HPI_RX}', 1) hpi from {csv(p['note'] / 'discharge.csv.gz')}
                         where hadm_id in (select hadm_id from need)""").df()
    conv = {h: bool(CONVULSIVE.search(t or "")) for h, t in zip(hp.hadm_id, hp.hpi)}

    def cls(row) -> str:
        parts = [cc_class3(x, row.condition, conv.get(row.hadm_id, False)) for x in str(row.cc or "").split(" | ")] if isinstance(row.cc, str) else ["missing"]
        for k in ("transfer", "test_label", "symptom_label", "ok", "missing"):
            if k in parts:
                return k
        return "missing"

    df["cc_class3"] = [cls(r) for r in df.itertuples()]
    df["f_hidden_transfer_ok"] = ~df.hadm_id.isin(hidden)
    df["f_cc3"] = df.cc_class3.isin(["ok", "symptom_label", "missing"])
    df["cc_rewrite"] = df.cc_class3.isin(["symptom_label", "missing"])
    base = df.f_new & df.f_not_transfer & df.f_via_ed & df.f_note
    df["usable3"] = base & df.f_hidden_transfer_ok & df.f_cc3
    # Old rule (task 01) for the marginal effects; 'UNKNOWN-CC' was 'ok' there (the bug of decision 9).
    df = df.merge(old[["hadm_id", "cc_class", "usable"]], on="hadm_id")
    rows = []
    for cond in CONDITIONS:
        g = df[df.condition == cond]
        b = g[base.loc[g.index]]
        rows.append({
            "condition": cond, "principal": len(g), "new_not_transfer_ed_note": len(b),
            "hidden_transfer_dropped": int((~b.f_hidden_transfer_ok).sum()),
            "cc_dropped_transfer": int((b.f_hidden_transfer_ok & (b.cc_class3 == "transfer")).sum()),
            "cc_dropped_test_label": int((b.f_hidden_transfer_ok & (b.cc_class3 == "test_label")).sum()),
            "usable3": int(g.usable3.sum()), "usable_task01": int(g.usable.sum()),
            "kept_symptom_label_rewritten (7)": int((g.usable3 & (g.cc_class3 == "symptom_label")).sum()),
            "kept_missing_rewritten (9)": int((g.usable3 & (g.cc_class3 == "missing")).sum()),
            "task01_unknown_cc_counted_ok": int((g.usable & g.cc.fillna("").str.upper().str.contains("UNKNOWN-CC")).sum()),
            "marginal_8_hidden_transfers": int((b.f_cc3 & ~b.f_hidden_transfer_ok).sum()),
        })
    wf = pd.DataFrame(rows)
    wf.loc[len(wf)] = ["TOTAL", *wf.drop(columns="condition").sum()]
    df.drop(columns=["cc"]).to_csv(out / "03_cohort_flags.csv", index=False)
    wf.to_csv(out / "03_waterfall.csv", index=False)
    with pd.option_context("display.width", 260, "display.max_columns", 30):
        print(wf.to_string(index=False))


# --- tables -----------------------------------------------------------------------------------
EXTRA_PANELS = {
    "TSH": [["Thyroid Stimulating Hormone"]],
    "vitamin_B12": [["Vitamin B12"]],
    "B12": [["Vitamin B12"]],
    "ammonia": [["Ammonia"]],
    "ESR": [["Sedimentation Rate"]],
    "folate": [["Folate"]],
    "HbA1c": [["% Hemoglobin A1c", "Hemoglobin A1c"]],
    "beta-hCG": [["HCG, Serum, Qualitative", "HCG, Urine, Qualitative", "hCG, Serum", "Human Chorionic Gonadotropin"]],
    "type_and_screen": [["Blood Type"]],
}
ALL_PANELS = {**PANELS, **EXTRA_PANELS}
NONCONTRAST_IN_CTA = re.compile(
    r"(?im)^\s*(?:NON-?\s?CONTRAST|NONCONTRAST|UNENHANCED|NON-?ENHANCED|PRE-?CONTRAST)[^:\n]{0,40}:|"
    r"^\s*(?:HEAD\s+CT|CT\s+HEAD|CT\s+OF\s+THE\s+HEAD|HEAD)\s+(?:WITHOUT|W/O)\s+(?:IV\s+)?CONTRAST[^:\n]{0,20}:|"
    r"\b(?:on|in)\s+the\s+(?:non-?\s?contrast|noncontrast|unenhanced|non-?enhanced|pre-?contrast)\s+(?:images?|portion|scan|head\s+CT|CT|study|sequence)")
NCCT_EXAM = r"^(CT HEAD W/O|PORTABLE HEAD CT W/O|ED CODE STROKE ONLY CT|CT BRAIN W/O)"
CTA_EXAM = r"^(CTA (HEAD|NECK)|ED STROKE CTA|CTA HEAD AND)"
MRI_EXAM = r"^(MR HEAD|MRI BRAIN|MR BRAIN|STROKE PROTOCOL \(BRAIN)"
SPINE_MRI_EXAM = r"^MR .*(SPINE)|^MR [CTL][ -]SPINE|^MR (CERVICAL|THORACIC|LUMBAR)"
CHEST_CT_EXAM = r"^CT CHEST|^CTA CHEST"
SUPPORT = {  # discharge diagnosis names the condition (decision 10, first test)
    "ISCH": r"stroke|infarct|\bCVA\b|cerebral\s+vascular\s+accident|cerebrovascular\s+accident|isch[a]?emi",
    "SAH": r"subarach|\bSAH\b|aneurysm",
    "SE": r"status\s+epilepticus|\bNCSE\b|\bstatus\b",
    "GBS": r"guillain|\bGBS\b|\bAIDP\b|miller.?fisher|polyradicul|demyelinating\s+polyneuropath|___\s+syndrome",
    "BACT": r"mening|ventriculitis",
    "MS": r"multiple\s+sclerosis|\bMS\b|demyelinat",
    "ALS": r"\bALS\b|amyotrophic|motor\s+neuron",
    "FEPI": r"epilep|seizure",
    "NMDAR": r"NMDA|autoimmune\s+enceph|anti-?NMDA",
    "MG": r"myasthen|\bMG\b",
    # task 06: the other ten conditions
    # SYNC is cardiac syncope: the discharge diagnosis must name a cardiac cause (reading confirms it)
    "SYNC": r"heart block|AV block|atrioventricular block|mobitz|sick sinus|sinus node|brady(?:cardia|arrhythm)|tachy(?:cardia|arrhythm)|"
            r"ventricular tachy|\bVT\b|\bSVT\b|atrial (?:fibrillation|flutter)|\bA-?fib|aortic (?:valve )?stenosis|arrhythm|pacemaker|"
            r"\bICD\b|defibrillator|torsade|long QT|QT prolong|brugada|hypertrophic (?:obstructive )?cardiomyopathy|\bpauses?\b|asystole|"
            r"conduction (?:disease|block)|bundle branch block|bifascicular|trifascicular",
    "GLIO": r"gliom|glioblastom|\bGBM\b|astrocytom|oligodendrogliom|brain (?:tumou?r|mass|neoplasm)",
    "MIG": r"migrain",
    "HEP": r"hepatic encephalopath|\bHE\b|portosystemic encephalopath",
    "PD": r"parkinson",
    "ALZ": r"alzheimer|dementia",
    "FND": r"functional|conversion|psychogenic|non-?epileptic|\bPNES\b|somatic symptom",
    "NPH": r"hydroceph|\bNPH\b",
    "VASC": r"vascular dementia|dementia",
    "FTD": r"frontotemporal|\bFTD\b|dementia",
}
DETECT_EXTRA = {"rns": re.compile(r"(?i)repetitive\s+(?:nerve\s+)?stim\w*[^.]{0,200}(?:decrement|normal|abnormal|showed|no\s)"),
                "csf_special": re.compile(r"(?i)oligoclonal|IgG\s+index|cytology[^.]{0,40}(?:negative|positive)|HSV\s+PCR[^.]{0,30}(?:negative|positive|detected)")}


def rhythm_hours(times: list, end) -> float:
    """Decision 5 rule: a record covers the time to the next one when the gap is <= 4 h, else 1 h."""
    ts_ = sorted(t for t in times if t <= end)
    tot = 0.0
    for i, t in enumerate(ts_):
        nxt = ts_[i + 1] if i + 1 < len(ts_) else None
        gap = (nxt - t).total_seconds() / 3600 if nxt is not None else 1.0
        tot += gap if gap <= 4 else 1.0
    return tot


def stage_tables3(a) -> None:
    p, con, out = paths(a.physionet), connect(a.tmp), Path(a.out)
    flags = pd.read_csv(out / "03_cohort_flags.csv", parse_dates=["admittime", "dischtime", "ed_intime"])
    coh = flags[flags.usable3 & flags.condition.isin(CANDIDATES)].copy()
    coh["t_ed"] = coh[["ed_intime", "admittime"]].min(axis=1)
    coh["t0"] = coh.t_ed - pd.Timedelta(hours=1)
    coh["t24"] = coh.admittime + pd.Timedelta(hours=24)
    coh["t48"] = coh.admittime + pd.Timedelta(hours=48)
    con.register("coh_df", coh[["subject_id", "hadm_id", "condition", "t0", "t24", "t48", "admittime", "dischtime"]])
    con.execute("create table coh as select * from coh_df")
    print(f"candidate cohort {len(coh)}", coh.condition.value_counts().to_dict(), file=sys.stderr)
    H = lambda t, te: (t - te).total_seconds() / 3600
    T = coh.set_index("hadm_id")

    # labs
    labels = sorted({x for groups in ALL_PANELS.values() for g in groups for x in g})
    con.register("lab_labels", pd.DataFrame({"label": labels}))
    con.execute(f"create table items as select itemid, label, fluid from {csv(p['hosp'] / 'd_labitems.csv.gz')}")
    labs = con.execute(f"""
        select c.hadm_id, i.label, i.fluid, min(l.charttime) t, min(l.charttime) <= max(c.t24) in24
        from {csv(p['hosp'] / 'labevents.csv.gz')} l join items i using (itemid)
        join coh c on l.subject_id = c.subject_id and l.charttime between c.t0 and c.dischtime
        where ((i.fluid = 'Blood' and i.label in (select label from lab_labels)) or i.fluid = 'Cerebrospinal Fluid')
          and (l.value is not null or l.valuenum is not null)
        group by 1, 2, 3""").df()
    blood24 = labs[(labs.fluid == "Blood") & labs.in24].groupby("hadm_id").label.apply(set).to_dict()
    csf = labs[labs.fluid == "Cerebrospinal Fluid"].groupby("hadm_id").label.apply(lambda s: " ; ".join(sorted(s))).to_dict()
    micro = con.execute(f"""
        select distinct c.hadm_id, m.spec_type_desc from {csv(p['hosp'] / 'microbiologyevents.csv.gz')} m
        join coh c on m.subject_id = c.subject_id and coalesce(m.charttime, cast(m.chartdate as timestamp)) between c.t0 and c.dischtime""").df()
    bcx = set(micro[micro.spec_type_desc.str.upper().eq("BLOOD CULTURE")].hadm_id)
    # radiology
    from mimic_case_assemble import FINDINGS
    rad = con.execute(f"""
        select c.hadm_id, upper(d.field_value) exam, r.charttime t, r.text
        from {csv(p['note'] / 'radiology.csv.gz')} r join {csv(p['note'] / 'radiology_detail.csv.gz')} d using (note_id)
        join coh c on r.subject_id = c.subject_id and r.charttime between c.t0 and c.dischtime
        where d.field_name = 'exam_name'""").df()
    rad["has_findings"] = rad.text.str.contains(FINDINGS, regex=True)
    rad = rad[rad.has_findings]
    # ECG (MIMIC-IV-ECG): first machine-read ECG in [t0, admission + 24 h]
    E = Path(a.physionet) / "mimic-iv-ecg/1.0"
    ecg = con.execute(f"""
        select c.hadm_id, min(m.ecg_time) t from read_csv_auto('{E / 'machine_measurements.csv'}', sample_size=-1) m
        join coh c on m.subject_id = c.subject_id and m.ecg_time between c.t0 and c.t24
        where m.report_0 is not null group by 1""").df()
    ecg_t = dict(zip(ecg.hadm_id, ecg.t))
    # rhythm: ICU chartevents heart rhythm (220048) + ED vitalsign rhythm; NIF / VC
    ch = con.execute(f"""
        select c.hadm_id, x.itemid, x.charttime t from {csv(p['icu'] / 'chartevents.csv.gz')} x join coh c using (hadm_id)
        where x.itemid in (220048, 224419, 220218, 224420) and x.charttime between c.t0 and c.dischtime
          and (x.value is not null or x.valuenum is not null)""").df()
    vs = con.execute(f"""
        select e.hadm_id, v.charttime t from {csv(p['ed'] / 'vitalsign.csv.gz')} v
        join {csv(p['ed'] / 'edstays.csv.gz')} e using (subject_id, stay_id) join coh c using (hadm_id)
        where v.rhythm is not null and trim(v.rhythm) <> ''""").df()
    rhythm = pd.concat([ch[ch.itemid == 220048][["hadm_id", "t"]], vs])
    rh = {h: rhythm_hours(list(pd.to_datetime(g.t)), T.loc[h, "t48"]) for h, g in rhythm.groupby("hadm_id")}
    resp = set(ch[ch.itemid != 220048].hadm_id)
    # notes
    notes = con.execute(f"""select hadm_id, string_agg(text, '\n\n') text from {csv(p['note'] / 'discharge.csv.gz')}
                            where hadm_id in (select hadm_id from coh) group by 1""").df()
    notes.to_parquet(out / "03_notes.parquet", index=False)
    from mimic_case_assemble import sections
    rows = []
    nt = dict(zip(notes.hadm_id, notes.text))
    for r in coh.itertuples():
        h, te = r.hadm_id, r.t_ed
        g = rad[rad.hadm_id == h]
        def first(rx, end=None):
            x = g[g.exam.str.contains(rx, regex=True)]
            if end is not None:
                x = x[x.t <= end]
            return x.sort_values("t").iloc[0] if len(x) else None
        nc, cta, mri, sp, chct = first(NCCT_EXAM, r.t24), first(CTA_EXAM, r.t24), first(MRI_EXAM), first(SPINE_MRI_EXAM), first(CHEST_CT_EXAM)
        cta_nc = cta is not None and bool(NONCONTRAST_IN_CTA.search(cta.text))
        text = nt.get(h, "")
        sc = note_scope(text)["results_course"]
        dxs = sections(text).get("Discharge Diagnosis", "") if text else ""
        row = {"hadm_id": h, "condition": r.condition,
               "t_ncct": H(nc.t, te) if nc is not None else None, "t_cta": H(cta.t, te) if cta is not None else None,
               "cta_has_noncontrast": cta_nc, "t_mri": H(mri.t, te) if mri is not None else None,
               "mri_contrast": bool(mri is not None and re.search(r"W ?& ?W/O|W/ CONTRAST|WITH CONTRAST", mri.exam)),
               "t_spine_mri": H(sp.t, te) if sp is not None else None, "t_chest_ct": H(chct.t, te) if chct is not None else None,
               "t_ecg_table": H(pd.Timestamp(ecg_t[h]), te) if h in ecg_t else None,
               "rhythm_hours": rh.get(h, 0.0), "icu_resp": h in resp, "blood_culture": h in bcx,
               "csf_basic": bool(csf.get(h)) and all(re.search(x, csf.get(h, "")) for x in (r"WBC|Total Nucleated|Polys|Lymphs|RBC", "Protein", "Glucose")),
               "t_admit": H(r.admittime, te), "dx_support": bool(re.search(SUPPORT[r.condition], dxs, re.I)),
               "age_over_89": False}
        b = blood24.get(h, set())
        for pn, groups in ALL_PANELS.items():
            row[f"panel_{pn}"] = all(any(x in b for x in gg) for gg in groups)
        for s in DETECTORS:
            row[f"note_{s}"] = detect(s, sc)
        for k, rx in DETECT_EXTRA.items():
            row[f"note_{k}"] = bool(rx.search(sc))
        rows.append(row)
    tab = pd.DataFrame(rows)
    pat = con.execute(f"select subject_id, anchor_age, anchor_year from {csv(p['hosp'] / 'patients.csv.gz')}").df()
    ages = coh.merge(pat, on="subject_id")
    ages["age"] = ages.anchor_age + ages.admittime.dt.year - ages.anchor_year
    tab = tab.merge(ages[["hadm_id", "age"]], on="hadm_id")
    tab["age_over_89"] = tab.age > 89
    tab.to_parquet(out / "03_tables.parquet", index=False)
    print(f"tables written: {len(tab)} admissions", file=sys.stderr)


# --- strict counts ------------------------------------------------------------------------------
def core_steps(cond: str) -> tuple[list[str], list[str]]:
    n, steps, panels, _ = policy_steps(ROOT / "data/neurobench/cases", cond)
    return [k for k, v in steps.items() if v >= n / 2], [k for k, v in panels.items() if v >= n / 2]


def served(t: pd.DataFrame, step: str, panels: list[str], rules: dict) -> pd.Series:
    """Admissions with a real result for a step under the rules (each rule can be switched off)."""
    in24 = lambda col: t[col].notna() & (t[col] <= t.t_admit + 24)
    if step == "ct_head":
        sep = in24("t_ncct")
        if rules["timing"] and "cta_head_neck" in rules["steps"]:
            sep &= t.t_ncct.isna() | t.t_cta.isna() | (t.t_ncct <= t.t_cta + 0.5)
        split = in24("t_cta") & t.cta_has_noncontrast if rules["d2_cta_split"] else pd.Series(False, index=t.index)
        return sep | split
    if step == "cta_head_neck":
        return in24("t_cta")
    if step == "labs":
        use = [x for x in panels if f"panel_{x}" in t]
        if rules["d3_panel_rule"]:
            use = [x for x in use if x not in rules["dropped_panels"]]
        missing = [x for x in panels if f"panel_{x}" not in t]
        if missing and not rules["d3_panel_rule"]:
            return pd.Series(False, index=t.index)
        return pd.concat([t[f"panel_{x}"] for x in use], axis=1).all(axis=1) if use else pd.Series(True, index=t.index)
    if step == "ecg":
        return in24("t_ecg_table") if rules["d1_ecg_table"] else t.note_ecg
    if step == "eeg":
        return t.note_eeg & t.note_eeg_continuous if rules["se_strict_eeg"] else t.note_eeg
    if step == "csf":
        return t.csf_basic
    if step == "micro:blood_culture":
        return t.blood_culture
    if step == "test:emg_ncs":
        return t.note_emg
    if step == "test:respiratory_function":
        return t.icu_resp | t.note_resp_function
    if step == "cardiac_monitoring":
        rh = (t.rhythm_hours >= 12) if rules["d5_rhythm"] else pd.Series(False, index=t.index)
        return rh | t.note_telemetry
    if step == "mri_brain":
        return t.t_mri.notna()
    if step == "body:spine_MRI":
        return t.t_spine_mri.notna()
    if step in ("body:chest_CT", "body:mediastinum_CT"):
        return t.t_chest_ct.notna()
    if step == "test:repetitive_nerve_stimulation":
        return t.note_rns
    return pd.Series(False, index=t.index)  # no record source (clinical assessment, tissue, US, ...)


SERVABLE = {"ct_head", "cta_head_neck", "labs", "ecg", "eeg", "csf", "micro:blood_culture", "test:emg_ncs",
            "test:respiratory_function", "cardiac_monitoring", "mri_brain", "body:spine_MRI", "body:chest_CT",
            "body:mediastinum_CT", "test:repetitive_nerve_stimulation"}


DX_SECTION = re.compile(r"(?ims)^\s*(?:discharge|final)\s+diagnos[ie]s\s*:(.*?)(?=^\s*(?:discharge condition|discharge instructions|"
                        r"followup instructions|condition at discharge)\s*:|\Z)")


def dx_support(cond: str, text: str) -> str:
    """'' when the discharge diagnosis names the condition; else why not (decision 10, automatic pass)."""
    m = DX_SECTION.search(text or "")
    if not m:
        return "no discharge-diagnosis section"
    sec = m.group(1)
    if re.search(SUPPORT[cond], sec, re.I):
        return ""
    if re.search(r"(?i)expired|deceased|comfort measures|\bCMO\b", sec):
        return "patient died / comfort care: no diagnosis listed"
    return "discharge diagnosis names another condition or a masked term"


def stage_strict3(a) -> None:
    out = Path(a.out)
    tab = pd.read_parquet(out / "03_tables.parquet")
    nt = pd.read_parquet(out / "03_notes.parquet").set_index("hadm_id").text
    tab["dx_reason"] = [dx_support(c, nt.get(h, "")) for h, c in zip(tab.hadm_id, tab.condition)]
    tab["dx_support"] = tab.dx_reason == ""
    tab.to_parquet(out / "03_tables.parquet", index=False)
    panel_rows, rows, marg = [], [], []
    for cond in CANDIDATES:
        t = tab[tab.condition == cond].reset_index(drop=True)
        steps, panels = core_steps(cond)
        steps = [s for s in steps if not s.startswith("knowledge")]
        share = {x: (t[f"panel_{x}"].mean() if f"panel_{x}" in t else 0.0) for x in panels}
        dropped = [x for x, v in share.items() if v < 0.5]
        for x in panels:
            panel_rows.append({"condition": cond, "panel": x, "cohort": len(t), "resulted_share": round(100 * share[x], 1),
                               "dropped_by_rule_3": x in dropped, "has_mimic_item": f"panel_{x}" in t})
        unservable = [s for s in steps if s not in SERVABLE]
        base = {"d1_ecg_table": True, "d2_cta_split": True, "d3_panel_rule": True, "d5_rhythm": True,
                "d10_support": True, "d11_age": True, "timing": True, "se_strict_eeg": True,
                "dropped_panels": dropped, "steps": steps}

        def count(rules) -> int:
            ok = pd.Series(True, index=t.index)
            for s in steps:
                ok &= served(t, s, panels, rules)
            if rules["d11_age"]:
                ok &= ~t.age_over_89
            if rules["d10_support"]:
                ok &= t.dx_support
            return int(ok.sum())

        full = count(base)
        rows.append({"condition": cond, "cohort3": len(t), "core_steps": ";".join(steps), "unservable_steps": ";".join(unservable),
                     "panels_dropped": ";".join(dropped), "strict_complete": full,
                     "strict_without_dx_support_rule": count({**base, "d10_support": False})})
        for d in ("d1_ecg_table", "d2_cta_split", "d3_panel_rule", "d5_rhythm", "d10_support", "d11_age"):
            marg.append({"condition": cond, "decision": d, "with": full, "without": count({**base, d: False})})
    s, m, pr = pd.DataFrame(rows), pd.DataFrame(marg), pd.DataFrame(panel_rows)
    s.to_csv(out / "03_strict.csv", index=False)
    m.to_csv(out / "03_strict_marginal.csv", index=False)
    pr.to_csv(out / "03_panel_rule.csv", index=False)
    with pd.option_context("display.width", 260, "display.max_colwidth", 90):
        print(s.to_string(index=False)); print()
        print(m.pivot(index="condition", columns="decision", values="without").reindex(CANDIDATES).to_string()); print()
        print(pr.to_string(index=False))
    # Coverage of the extra checks.
    print("\nrhythm >= 12 h:", tab.groupby("condition").rhythm_hours.apply(lambda x: int((x >= 12).sum())).to_dict())
    print("CTA reports with an explicit non-contrast part:", tab.groupby("condition").cta_has_noncontrast.sum().astype(int).to_dict())
    print("discharge diagnosis disagreement, automatic pass:")
    print(tab[~tab.dx_support].groupby(["condition", "dx_reason"]).size().to_string())


PILOT3 = ["ISCH", "SAH", "SE", "GBS", "MS"]
PREFIX3 = {"ISCH": "MIMIC-ISCH", "SAH": "MIMIC-SAH", "SE": "MIMIC-SE", "GBS": "MIMIC-GBS", "MS": "MIMIC-MS"}


def strict_pool(tab: pd.DataFrame, cond: str) -> pd.DataFrame:
    """Admissions where every core step is served under all decisions; support not yet applied."""
    t = tab[tab.condition == cond].reset_index(drop=True)
    steps, panels = core_steps(cond)
    steps = [s for s in steps if not s.startswith("knowledge")]
    dropped = [x for x in panels if (t[f"panel_{x}"].mean() if f"panel_{x}" in t else 0.0) < 0.5]
    rules = {"d1_ecg_table": True, "d2_cta_split": True, "d3_panel_rule": True, "d5_rhythm": True, "d10_support": True,
             "d11_age": True, "timing": True, "se_strict_eeg": True, "dropped_panels": dropped, "steps": steps}
    ok = pd.Series(True, index=t.index)
    for st in steps:
        ok &= served(t, st, panels, rules)
    return t[ok & ~t.age_over_89]


def stage_select3(a) -> None:
    """Pilot selection: task-02 admissions still eligible keep their case id; the rest of each
    condition is filled to N in a fixed random order (seed). Support: the discharge diagnosis names
    the condition, or the reader found the defining evidence (03_se_support_review.csv); exclusions
    found while reading are in 03_exclusions.csv (hadm_id, reason)."""
    import random
    out = Path(a.out)
    tab = pd.read_parquet(out / "03_tables.parquet")
    rev = pd.read_csv(out / "03_se_support_review.csv")
    read_ok = set(rev[rev.supported].hadm_id)
    read_no = dict(zip(rev[~rev.supported].hadm_id, rev[~rev.supported].reason))
    exc_path = out / "03_exclusions.csv"
    excl = dict(pd.read_csv(exc_path)[["hadm_id", "reason"]].itertuples(index=False)) if exc_path.exists() else {}
    old = pd.read_csv(out / "02_selection.csv")
    old = old[old.case_id.notna() & (old.case_id != "")]
    old_ids = dict(zip(old.hadm_id, old.case_id))
    # Ids already given in an earlier run of this stage stay with their admission (excluded ones too).
    prev_path = out / "03_selection.csv"
    prev = pd.read_csv(prev_path) if prev_path.exists() else pd.DataFrame(columns=["hadm_id", "case_id"])
    prev = prev[prev.case_id.notna() & (prev.case_id != "")]
    prev_ids = dict(zip(prev.hadm_id, prev.case_id))
    # Ids of cases excluded after reading stay reserved for their admission: a manual file exists.
    if exc_path.exists():
        ex_df = pd.read_csv(exc_path)
        if "case_id" in ex_df:
            prev_ids.update({h: c for h, c in zip(ex_df.hadm_id, ex_df.case_id) if isinstance(c, str) and c})
    flags = pd.read_csv(out / "03_cohort_flags.csv")
    rows, counts = [], []
    rng = random.Random(a.seed)
    for cond in PILOT3:
        pool = strict_pool(tab, cond)
        order = sorted(pool.hadm_id)
        rng.shuffle(order)
        keep = []
        for rank, h in enumerate(order, start=1):
            r = pool[pool.hadm_id == h].iloc[0]
            if h in excl:
                reason = excl[h]
            elif r.dx_support or h in read_ok:
                reason = ""
            elif h in read_no:
                reason = "record does not support the code (read): " + read_no[h]
            else:
                reason = "record support not established (discharge diagnosis: " + r.dx_reason + "; not read)"
            keep.append((rank, h, reason))
        counts.append({"condition": cond, "strict_complete_before_support": len(order),
                       "eligible": sum(1 for _, _, x in keep if not x),
                       **pd.Series([x.split(" (")[0] if x else "eligible" for _, _, x in keep]).value_counts().to_dict()})
        eligible = [h for _, h, x in keep if not x]
        first = [h for h in eligible if h in old_ids]
        rest = [h for h in eligible if h not in old_ids]
        # Keep earlier picks first (same random order), then fill.
        rest = [h for h in rest if h in prev_ids] + [h for h in rest if h not in prev_ids]
        chosen = first + rest[: max(0, a.n - len(first))]
        known = {**{h: c for h, c in prev_ids.items() if c.startswith(PREFIX3[cond] + "-")}, **{h: old_ids[h] for h in first}}
        used_nums = {int(c.rsplit("-", 1)[1]) for c in known.values()}
        nums = iter(i for i in range(1, 200) if i not in used_nums)
        for rank, h, reason in keep:
            if h in known and (h in chosen or reason):
                cid = known[h] if h in chosen else ""
                prev_note = known[h]
            else:
                cid = f"{PREFIX3[cond]}-{next(nums):03d}" if h in chosen else ""
                prev_note = ""
            rows.append({"case_id": cid, "condition": cond, "hadm_id": int(h),
                         "subject_id": int(flags.loc[flags.hadm_id == h, "subject_id"].iloc[0]),
                         "draw_rank": rank, "exclusion": reason, "task02_case": h in old_ids,
                         "excluded_case_id": prev_note if (reason and prev_note) else ""})
    sel = pd.DataFrame(rows)
    sel.to_csv(out / "03_selection.csv", index=False)
    c = pd.DataFrame(counts).fillna(0)
    c.to_csv(out / "03_selection_counts.csv", index=False)
    gone = old[~old.hadm_id.isin(sel[sel.case_id != ""].hadm_id)]
    with pd.option_context("display.width", 250, "display.max_columns", 20):
        print(c.to_string(index=False))
        print("selected:", sel[sel.case_id != ""].groupby("condition").size().to_dict())
        print("task-02 cases kept:", int(sel[(sel.case_id != "") & sel.task02_case].shape[0]), "of", len(old),
              "| dropped with reason:", [sel.loc[sel.hadm_id == h, "exclusion"].iloc[0] if (sel.hadm_id == h).any() else "not in the strict pool"
                                          for h in gone.hadm_id])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["cohort3", "tables3", "strict3", "select3"])
    ap.add_argument("--seed", type=int, default=20261107)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--physionet", default="/eos/user/a/aprotani/physionet")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp", required=True)
    a = ap.parse_args()
    if not str(Path(a.out).resolve()).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
        sys.exit("--out must be under the PhysioNet workspace (DUA)")
    {"cohort3": stage_cohort3, "tables3": stage_tables3, "strict3": stage_strict3, "select3": stage_select3}[a.stage](a)


if __name__ == "__main__":
    main()
