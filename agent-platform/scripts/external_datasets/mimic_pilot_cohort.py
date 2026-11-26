"""MIMIC-IV neurology: the usable cohort per condition and, for the pilot conditions, the
admissions where every step the NeuroBench policy requires has a real result.

Stage ``cohort`` (all 20 conditions): principal diagnosis mapped by ``mimic_neuro``, then, in
this order, new to the patient, not a transfer, arrived via the ED, discharge note present,
triage chief complaint present and not naming the diagnosis. Prints the waterfall (count after
each filter and its marginal drop) and each filter alone, and writes one row per admission with
its flags to ``OUT/01_cohort_flags.csv`` (IDs: OUT must be under the PhysioNet workspace).

Stage ``coverage`` (pilot conditions): reads the required action criteria of the NeuroBench cases
of each condition, turns them into steps (tool + discriminating argument), and for each cohort
admission checks the MIMIC source of every step: ``labevents`` (panels by item), CSF labs,
``microbiologyevents``, radiology reports by exam name, ICU ``chartevents`` (NIF, vital
capacity), and result detectors on the discharge note's pertinent results and hospital course
(``mimic_note_results``). Prints counts per step and condition; writes per-admission flags to
``OUT/01_pilot_coverage.csv``.

Stage ``sample``: draws a random sample of cohort notes per pilot condition and writes, for each,
the passages around every broad study keyword (to ``OUT/01_detector_sample.jsonl``) with the
detector's verdicts, for a reader to label. Stage ``score`` compares those labels
(``OUT/01_detector_labels.csv``) with the detector and prints precision and recall.

Prints counts only (PhysioNet DUA).

    nice -n 10 uv run --no-project --with duckdb --with pandas python -I mimic_pilot_cohort.py \
        --stage cohort|coverage|sample|score --physionet /eos/user/a/aprotani/physionet \
        --cases data/neurobench/cases --out $W/out --tmp $W/tmp
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from general_audit import DX_ABBREVIATIONS
from mimic_neuro import neuro_condition
from mimic_note_results import (
    BROAD,
    DETECTORS,
    STUDIES_BY_CONDITION,
    detect,
    note_scope,
    passages,
)

CONDITIONS = ["ISCH", "SYNC", "GLIO", "SAH", "MIG", "FEPI", "HEP", "MS", "SE", "PD", "ALZ", "GBS", "FND",
              "MG", "NPH", "VASC", "ALS", "BACT", "NMDAR", "FTD"]
PILOT = ["ISCH", "SAH", "SE", "BACT", "GBS"]

# --- chief complaint that names the diagnosis -------------------------------------------------
# DX_ABBREVIATIONS (general_audit) catches generic diagnosis labels and transfers. The terms below
# name the condition itself. Symptoms that define a condition (seizure for SE, syncope for SYNC,
# headache for MIG, weakness for GBS) are a presentation, not a diagnosis, and are kept; they are
# counted separately (CC_DEFINING_SYMPTOM) so the choice can be reviewed.
CC_NAMES_CONDITION = {
    "ISCH": r"stroke|\bCVA\b|infarct|\bTIA\b|\btPA\b|\bLVO\b|\bELVO\b|thrombectomy|cerebrovascular",
    "SAH": r"\bSAH\b|subarach|aneurysm|bleed|hemorrhag|haemorrhag|\bICH\b|\bIPH\b|\bIVH\b",
    "SE": r"status\s+epi|\bin\s+status\b|\bSE\b|\bNCSE\b|non-?convulsive\s+status",
    "BACT": r"mening|enceph|ventriculitis|neisseria|pneumococc|abscess",
    "GBS": r"\bGBS\b|guillain|barr[eé]|\bAIDP\b|\bCIDP\b|miller.?fisher|polyradic|demyelin",
    "SYNC": r"\bsyncope\b.*cardiac|arrhythm",
    "GLIO": r"mass|tumou?r|glio|\bGBM\b|lesion|neoplasm|\bbrain\s+ca\b|cancer|malignan|oncol",
    "MIG": r"migraine",
    "FEPI": r"epilep|focal\s+seiz|partial\s+seiz|complex\s+partial",
    "HEP": r"hepatic\s+enceph|\bHE\b|encephalopathy|cirrho|ammonia|liver",
    "MS": r"\bMS\b|multiple\s+sclerosis|demyelin|optic\s+neuritis|\bflare\b",
    "PD": r"parkinson|\bPD\b",
    "ALZ": r"alzheim|dementia",
    "FND": r"conversion|functional|psychogenic|pseudo-?seiz|\bPNES\b|non-?epileptic",
    "MG": r"myasthen|\bMG\b|crisis",
    "NPH": r"\bNPH\b|hydroceph|shunt",
    "VASC": r"dementia|vascular",
    "ALS": r"\bALS\b|amyotroph|motor\s+neuron|\bMND\b",
    "NMDAR": r"enceph|\bNMDA|teratoma|autoimmune",
    "FTD": r"dementia|frontotemporal|\bFTD\b",
}
CC_DEFINING_SYMPTOM = {
    "SE": r"seiz|convuls|\bsz\b",
    "SYNC": r"syncop|passed\s+out|\bLOC\b|loss\s+of\s+consc|faint",
    "MIG": r"headache|\bHA\b",
    "SAH": r"headache|\bHA\b",
    "FEPI": r"seiz|\bsz\b",
    "GBS": r"weak|numb|tingl|parasth|paresth",
}


def cc_class(cc: str | None, condition: str) -> str:
    """'missing', 'names_dx' (generic label or transfer), 'names_condition', or 'ok'."""
    if cc is None or not str(cc).strip() or str(cc).strip().lower() in {"nan", "none", "___"}:
        return "missing"
    cc = str(cc)
    if re.search(CC_NAMES_CONDITION.get(condition, r"(?!)"), cc, re.IGNORECASE):
        return "names_condition"
    if DX_ABBREVIATIONS.search(cc):
        return "names_dx"
    return "ok"


def connect(tmp: str):
    import duckdb
    con = duckdb.connect()
    con.execute(f"set temp_directory = '{tmp}'; set memory_limit = '16GB'; set threads = 6; "
                "set preserve_insertion_order = false")
    return con


def csv(path: Path) -> str:
    return f"read_csv_auto('{path}', sample_size=-1)"


def paths(root: str) -> dict[str, Path]:
    r = Path(root)
    return {"hosp": r / "mimiciv/3.1/hosp", "icu": r / "mimiciv/3.1/icu", "ed": r / "mimic-iv-ed/2.2/ed",
            "note": r / "mimic-iv-note/2.2/note"}


# ============================================================================================
# Stage 1: cohort
# ============================================================================================
def stage_cohort(a) -> None:
    p, con = paths(a.physionet), connect(a.tmp)
    con.execute(f"create table dx as select subject_id, hadm_id, seq_num, cast(icd_code as varchar) icd_code, "
                f"icd_version from {csv(p['hosp'] / 'diagnoses_icd.csv.gz')}")
    con.execute(f"create table adm as select * from {csv(p['hosp'] / 'admissions.csv.gz')}")
    codes = con.execute("select distinct icd_code code, icd_version from dx").df()
    codes["condition"] = [neuro_condition(c, v) for c, v in zip(codes.code, codes.icd_version)]
    con.register("icdmap", codes.dropna(subset=["condition"]))
    con.execute("""
        create table cohort as
        select d.subject_id, d.hadm_id, m.condition, a.admittime, a.dischtime, a.admission_location
        from dx d join icdmap m on d.icd_code = m.code and d.icd_version = m.icd_version
        join adm a using (hadm_id) where d.seq_num = 1
    """)
    # Same definition as mimic_cohort.py: an earlier admission carries a code of the condition.
    con.execute("""
        create table prior as select distinct c.hadm_id from cohort c
        join adm a2 on a2.subject_id = c.subject_id and a2.admittime < c.admittime
        join dx d2 on d2.hadm_id = a2.hadm_id
        join icdmap m2 on d2.icd_code = m2.code and d2.icd_version = m2.icd_version
        where m2.condition = c.condition
    """)
    con.execute(f"create table eds as select * from {csv(p['ed'] / 'edstays.csv.gz')} where hadm_id is not null")
    con.execute(f"""
        create table edcc as
        select e.hadm_id, min(e.intime) ed_intime,
               string_agg(coalesce(t.chiefcomplaint, ''), ' | ' order by e.intime) cc
        from eds e left join {csv(p['ed'] / 'triage.csv.gz')} t using (subject_id, stay_id)
        group by e.hadm_id
    """)
    con.execute(f"create table dsum as select distinct hadm_id from {csv(p['note'] / 'discharge.csv.gz')}")
    df = con.execute("""
        select c.*, c.hadm_id not in (select hadm_id from prior) as f_new,
               coalesce(c.admission_location, '') not like 'TRANSFER%' as f_not_transfer,
               e.hadm_id is not null as f_via_ed, e.ed_intime, e.cc,
               c.hadm_id in (select hadm_id from dsum) as f_note
        from cohort c left join edcc e using (hadm_id)
    """).df()
    df = df[df.condition.isin(CONDITIONS)].copy()
    # Several ED stays: the admission fails if any of their complaints names the diagnosis.
    def cls(cc, cond):
        if not isinstance(cc, str):
            return "missing"
        parts = [cc_class(x, cond) for x in cc.split(" | ")]
        for k in ("names_condition", "names_dx", "ok"):
            if k in parts:
                return k
        return "missing"
    df["cc_class"] = [cls(cc, c) for cc, c in zip(df.cc, df.condition)]
    df["cc_defining_symptom"] = [bool(isinstance(cc, str) and re.search(CC_DEFINING_SYMPTOM.get(c, r"(?!)"), cc, re.I))
                                 for cc, c in zip(df.cc, df.condition)]
    df["f_cc"] = df.cc_class == "ok"
    filters = ["f_new", "f_not_transfer", "f_via_ed", "f_note", "f_cc"]
    df["usable"] = df[filters].all(axis=1)
    out = Path(a.out)
    df.drop(columns=["cc"]).to_csv(out / "01_cohort_flags.csv", index=False)

    rows, alone = [], []
    for cond in CONDITIONS:
        g = df[df.condition == cond]
        r = {"condition": cond, "principal": len(g)}
        keep = pd.Series(True, index=g.index)
        prev = len(g)
        for f in filters:
            keep &= g[f]
            r[f] = int(keep.sum())
            r[f"drop_{f}"] = prev - r[f]
            prev = r[f]
        rows.append(r)
        alone.append({"condition": cond, "principal": len(g), **{f: int(g[f].sum()) for f in filters},
                      "new_not_transfer": int((g.f_new & g.f_not_transfer).sum())})
    wf, al = pd.DataFrame(rows), pd.DataFrame(alone)
    wf.loc[len(wf)] = ["TOTAL", *wf.drop(columns="condition").sum()]
    al.loc[len(al)] = ["TOTAL", *al.drop(columns="condition").sum()]
    # Chief-complaint classes among admissions that passed the first four filters.
    pre = df[df[filters[:-1]].all(axis=1)]
    ccx = pd.crosstab(pre.condition, pre.cc_class).reindex(CONDITIONS).fillna(0).astype(int)
    ccx["kept_with_defining_symptom"] = pre[pre.f_cc].groupby("condition").cc_defining_symptom.sum().reindex(CONDITIONS).fillna(0).astype(int)
    wf.to_csv(out / "01_waterfall.csv", index=False)
    al.to_csv(out / "01_filter_alone.csv", index=False)
    ccx.to_csv(out / "01_cc_classes.csv")
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print("Waterfall (count after each filter, in order; drop_* = marginal drop):")
        print(wf.to_string(index=False))
        print("\nEach filter alone:")
        print(al.to_string(index=False))
        print("\nChief complaint class among admissions passing the first four filters:")
        print(ccx.to_string())


# ============================================================================================
# Stage 2: policy steps and coverage
# ============================================================================================
def step_key(alt: dict) -> str:
    """One NeuroBench tool pattern -> a study step (tool + discriminating argument)."""
    t, r = alt["tool_name"], alt.get("required_arguments", {}) or {}
    if t == "order_ct_scan":
        return "cta_head_neck" if r.get("angiography") else "ct_head"
    if t == "interpret_labs":
        return "labs"
    if t == "analyze_csf":
        return "csf"
    if t == "order_microbiology":
        return f"micro:{r.get('specimen', '?')}"
    if t == "order_specialized_test":
        return f"test:{r.get('test_type', '?')}"
    if t == "order_cardiac_monitoring":
        return "cardiac_monitoring"
    if t == "order_echocardiogram":
        return "echo"
    if t == "order_advanced_imaging":
        return f"adv:{r.get('modality', '?')}"
    if t == "order_body_imaging":
        return f"body:{r.get('study', '?')}"
    if t == "analyze_brain_mri":
        return "mri_brain"
    if t == "analyze_eeg":
        return "eeg"
    if t == "analyze_ecg":
        return "ecg"
    if t == "check_drug_interactions":
        return "knowledge:check_drug_interactions"
    if t == "search_medical_literature":
        return "knowledge:search_medical_literature"
    return t


def policy_steps(cases: Path, cond: str) -> tuple[int, collections.Counter, collections.Counter, dict]:
    """Cases of a condition; per step the number of cases requiring it; lab panels and CSF
    arguments (from the smallest alternative) per case; the argument variants seen per step."""
    files = sorted(cases.glob(f"{cond}-*.json"))
    steps, panels = collections.Counter(), collections.Counter()
    variants: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for f in files:
        case_steps, case_panels = set(), set()
        for cr in json.loads(f.read_text())["ground_truth"]["action_criteria"]:
            if cr["importance"] != "required":
                continue
            keys = {step_key(alt) for alt in cr["alternatives"]}
            for k in keys:
                case_steps.add(k)
            for alt in cr["alternatives"]:
                variants[step_key(alt)][json.dumps(alt.get("required_arguments", {}), sort_keys=True)] += 1
            labs = [alt for alt in cr["alternatives"] if alt["tool_name"] == "interpret_labs"]
            if labs:
                smallest = min(labs, key=lambda x: len(x["required_arguments"].get("panels", [])))
                case_panels |= set(smallest["required_arguments"].get("panels", []))
        steps.update(case_steps)
        panels.update(case_panels)
    return len(files), steps, panels, variants


# Blood panels -> MIMIC labevents items (d_labitems label, fluid Blood). A panel is present when
# every group has at least one resulted item in the presentation window.
PANELS: dict[str, list[list[str]]] = {
    "CBC": [["White Blood Cells"], ["Hemoglobin"], ["Platelet Count"]],
    "glucose": [["Glucose"]],
    "creatinine": [["Creatinine"]],
    "coagulation": [["INR(PT)", "PT"], ["PTT"]],
    "troponin": [["Troponin T", "Troponin I"]],
    "BNP": [["NTproBNP"]],
    "BMP": [["Sodium"], ["Potassium"], ["Chloride"], ["Bicarbonate"], ["Urea Nitrogen"], ["Creatinine"], ["Glucose"]],
    "CMP": [["Sodium"], ["Potassium"], ["Chloride"], ["Bicarbonate"], ["Urea Nitrogen"], ["Creatinine"], ["Glucose"],
            ["Alanine Aminotransferase (ALT)", "Alanine Aminotransferase"],
            ["Asparate Aminotransferase (AST)", "Asparate Aminotransferase"],
            ["Alkaline Phosphatase"], ["Bilirubin, Total"]],
    "magnesium": [["Magnesium"]],
    "CK": [["Creatine Kinase (CK)"]],
    "CRP": [["C-Reactive Protein", "High-Sensitivity CRP"]],
    "HIV": [["HIV Screen", "HIV 1 Ab Confirmation", "HIV FINAL", "HIV 1 Viral Load", "Reflex HIV Confirmation"]],
    "procalcitonin": [["Procalcitonin"]],
    "lipid_panel": [["Cholesterol, Total"], ["Triglycerides"]],
    "AED_levels": [["Phenytoin", "Valproic Acid", "Carbamazepine", "Phenobarbital", "Levetiracetam", "Lamotrigine",
                    "Free Phenytoin", "Lacosamide"]],
    "tox_screen": [["Ethanol", "Acetaminophen", "Salicylate", "Benzodiazepine Screen", "Barbiturate Screen",
                    "Tricyclic Antidepressant Screen"]],
}
# CSF labs (fluid Cerebrospinal Fluid): cell count, protein, glucose.
CSF_GROUPS = {"cells": r"WBC|Total Nucleated|White Blood|Polys|Lymphs|RBC", "protein": r"Protein", "glucose": r"Glucose"}

# Radiology exam_name -> step. CT contrast: 'W/O' or 'WO' alone means non-contrast.
RAD_RULES = [
    ("cta_head_neck", r"^CTA\b.*(HEAD|NECK|BRAIN)|STROKE CTA|CTA HEAD|CT ANGIO.*(HEAD|NECK|BRAIN)"),
    ("ct_perfusion", r"PERFUSION"),
    ("ct_head", r"^CT HEAD|HEAD CT|CODE STROKE ONLY CT|^CT BRAIN"),
    ("mra", r"^MRA\b"),
    ("mri_brain", r"^MR HEAD|STROKE PROTOCOL \(BRAIN|^MR BRAIN|^MRI BRAIN"),
    ("catheter_angio", r"CAROTID/CEREBRAL|CEREBRAL ANGIO|DIAGNOSTIC ANGIO|^ANGIO|A-GRAM|EXT CAROTID"),
    ("spine_mri", r"^MR .*(SPINE|C-SPINE|T-SPINE|L-SPINE)|^MR [CTL][ -]SPINE"),
    ("lp_fluoro", r"LUMBAR (SPINAL )?PUNCTURE"),
    ("chest_xray", r"^CHEST \(|^CHEST PORT\b|CHEST \(SINGLE"),
    ("carotid_duplex", r"CAROTID SERIES|CAROTID/CERVICAL"),
]


def rad_step(exam: str) -> str | None:
    exam = (exam or "").upper()
    for step, rx in RAD_RULES:
        if re.search(rx, exam):
            if step == "ct_head":
                return "ct_head_contrast" if re.search(r"W/ ?CONT|W&W/O|W/&W/O|WITH CONT", exam) and not re.search(r"W/O CONT|WO CONT|W/O$", exam) else "ct_head"
            return step
    return None


# Where each step is served from (for the report).
SOURCE = {
    "ct_head": "radiology report, exam_name CT head without contrast (note/radiology + radiology_detail)",
    "cta_head_neck": "radiology report, exam_name CTA head/neck",
    "mri_brain": "radiology report, exam_name MR head/brain",
    "labs": "hosp/labevents, blood items per panel, first value in [ED arrival - 1 h, admission + 24 h]",
    "csf": "hosp/labevents fluid Cerebrospinal Fluid (cells, protein, glucose) + microbiologyevents CSF; opening pressure and appearance from the note",
    "micro:blood_culture": "hosp/microbiologyevents spec_type_desc BLOOD CULTURE",
    "ecg": "discharge note (pertinent results / course) - MIMIC-IV-ECG not on EOS",
    "eeg": "discharge note (pertinent results / course)",
    "test:emg_ncs": "discharge note (pertinent results / course)",
    "test:respiratory_function": "icu/chartevents NIF (224419), vital capacity (220218, 224420); else discharge note",
    "cardiac_monitoring": "discharge note (telemetry / Holter result); poe telemetry order has no result",
    "echo": "discharge note (TTE/TEE report or course)",
}


def stage_coverage(a) -> None:
    """Table sources for the pilot cohort; writes OUT/01_table_flags.csv and caches the notes."""
    p, con, out = paths(a.physionet), connect(a.tmp), Path(a.out)
    flags = pd.read_csv(out / "01_cohort_flags.csv", parse_dates=["admittime", "dischtime", "ed_intime"])
    coh = flags[flags.usable & flags.condition.isin(PILOT)].copy()
    coh["t0"] = coh[["ed_intime", "admittime"]].min(axis=1) - pd.Timedelta(hours=1)
    coh["t_lab_end"] = coh.admittime + pd.Timedelta(hours=24)
    con.register("coh_df", coh[["subject_id", "hadm_id", "condition", "t0", "t_lab_end", "admittime", "dischtime"]])
    con.execute("create table coh as select * from coh_df")
    print(f"pilot cohort admissions: {len(coh)}", file=sys.stderr)

    # --- labs: blood panels in the presentation window, CSF over the stay -----------------
    lab_labels = sorted({x for groups in PANELS.values() for g in groups for x in g})
    con.execute(f"create table items as select itemid, label, fluid from {csv(p['hosp'] / 'd_labitems.csv.gz')}")
    con.register("lab_labels", pd.DataFrame({"label": lab_labels}))
    con.execute(f"""
        create table labs as
        select c.hadm_id, i.label, i.fluid, l.charttime
        from {csv(p['hosp'] / 'labevents.csv.gz')} l
        join items i using (itemid)
        join coh c on l.subject_id = c.subject_id and l.charttime between c.t0 and c.dischtime
        where ((i.fluid = 'Blood' and i.label in (select label from lab_labels)) or i.fluid = 'Cerebrospinal Fluid')
          and (l.value is not null or l.valuenum is not null)
    """)
    blood = con.execute("""select distinct l.hadm_id, l.label from labs l join coh c using (hadm_id)
                           where l.fluid = 'Blood' and l.charttime <= c.t_lab_end""").df()
    have = blood.groupby("hadm_id").label.apply(set).to_dict()
    csf = con.execute("select hadm_id, label from labs where fluid = 'Cerebrospinal Fluid'").df()
    csf_have = csf.groupby("hadm_id").label.apply(lambda s: " ; ".join(sorted(set(s)))).to_dict()

    # --- microbiology -------------------------------------------------------------------
    micro = con.execute(f"""
        select distinct c.hadm_id, m.spec_type_desc, m.test_name
        from {csv(p['hosp'] / 'microbiologyevents.csv.gz')} m
        join coh c on m.subject_id = c.subject_id
          and coalesce(m.charttime, cast(m.chartdate as timestamp)) between c.t0 and c.dischtime
    """).df()
    micro.to_csv(Path(a.tmp) / "micro_names_tmp.csv", index=False) if a.debug else None
    m_blood = set(micro[micro.spec_type_desc.str.contains("BLOOD CULTURE", na=False, case=False)
                        & ~micro.spec_type_desc.str.contains("FLUID RECEIVED", na=False, case=False)].hadm_id)
    m_csf = set(micro[micro.spec_type_desc.str.contains("CSF", na=False)].hadm_id)
    m_hiv = set(micro[micro.test_name.str.contains("HIV", na=False, case=False)].hadm_id)

    # --- radiology by exam name; the report must have a findings section ----------------
    rad = con.execute(f"""
        select c.hadm_id, d.field_value exam, regexp_matches(r.text, '(?i)\\bFINDINGS?\\s*:') has_findings,
               r.charttime <= c.t_lab_end as first24
        from {csv(p['note'] / 'radiology.csv.gz')} r
        join {csv(p['note'] / 'radiology_detail.csv.gz')} d using (note_id)
        join coh c on r.subject_id = c.subject_id and r.charttime between c.t0 and c.dischtime
        where d.field_name = 'exam_name'
    """).df()
    rad["step"] = [rad_step(e) for e in rad.exam]
    exam_counts = (rad.assign(step=rad.step.fillna("(other)")).drop_duplicates(["hadm_id", "exam"])
                   .groupby(["step", "exam"]).size().rename("admissions").reset_index()
                   .sort_values(["step", "admissions"], ascending=[True, False]))
    exam_counts[exam_counts.admissions >= 5].to_csv(out / "01_exam_names.csv", index=False)
    rad_any = rad.dropna(subset=["step"]).groupby("hadm_id").step.apply(set).to_dict()
    rad_find = rad[rad.has_findings].dropna(subset=["step"]).groupby("hadm_id").step.apply(set).to_dict()
    # A CTA head billed "with and without contrast" holds a non-contrast acquisition.
    cta_nc = set(rad[rad.has_findings & rad.exam.str.upper().str.contains(r"^CTA HEAD W&W/O", regex=True, na=False)].hadm_id)

    # --- ICU respiratory function -------------------------------------------------------
    resp = set()
    if not a.skip_icu:
        resp = set(con.execute(f"""
            select distinct hadm_id from {csv(p['icu'] / 'chartevents.csv.gz')}
            where itemid in (224419, 220218, 224420) and valuenum is not null
              and hadm_id in (select hadm_id from coh where condition = 'GBS')
        """).df().hadm_id)

    # --- orders (poe) for context: was the study ordered at all ------------------------
    poe = con.execute(f"""
        select distinct hadm_id, order_type || ' / ' || coalesce(order_subtype, '') o
        from {csv(p['hosp'] / 'poe.csv.gz')}
        where hadm_id in (select hadm_id from coh)
          and (order_subtype in ('EEG', 'EMG', 'ECG', 'Echo', 'Telemetry') or order_type = 'Neurology')
    """).df()
    ordered = poe.groupby("hadm_id").o.apply(set).to_dict()

    # --- assemble per admission (tables) ----------------------------------------------
    rows = []
    for r in coh.itertuples():
        h = r.hadm_id
        labs_h = have.get(h, set())
        row = {"hadm_id": h, "condition": r.condition}
        for pname, groups in PANELS.items():
            row[f"panel_{pname}"] = all(any(x in labs_h for x in g) for g in groups)
        cs = csf_have.get(h, "")
        row["csf_any_lab"] = bool(cs)
        row["csf_basic"] = bool(cs) and all(re.search(rx, cs) for rx in CSF_GROUPS.values())
        row["csf_micro"] = h in m_csf
        row["micro_blood_culture"] = h in m_blood
        row["micro_hiv"] = h in m_hiv
        for st in ("ct_head", "ct_head_contrast", "cta_head_neck", "ct_perfusion", "mri_brain", "mra", "catheter_angio",
                   "spine_mri", "carotid_duplex"):
            row[f"rad_{st}"] = st in rad_any.get(h, set())
            row[f"radfind_{st}"] = st in rad_find.get(h, set())
        row["radfind_cta_head_with_noncontrast"] = h in cta_nc
        row["icu_resp_function"] = h in resp
        o = ordered.get(h, set())
        row.update({"order_eeg": "Neurology / EEG" in o, "order_emg": "Neurology / EMG" in o,
                    "order_ecg": "Cardiology / ECG" in o, "order_echo": "Cardiology / Echo" in o,
                    "order_telemetry": any(x.endswith("/ Telemetry") for x in o)})
        rows.append(row)
    tab = pd.DataFrame(rows)
    tab["panel_HIV"] = tab.panel_HIV | tab.micro_hiv
    tab.to_csv(out / "01_table_flags.csv", index=False)

    # --- the pilot notes, cached once under OUT (record content, written whole) ---------
    notes = con.execute(f"""
        select hadm_id, string_agg(text, '\n\n') text from {csv(p['note'] / 'discharge.csv.gz')}
        where hadm_id in (select hadm_id from coh) group by hadm_id
    """).df()
    notes.to_parquet(out / "01_pilot_notes.parquet", index=False)


def note_flags(notes: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for h, text in zip(notes.hadm_id, notes.text):
        scope = note_scope(text)
        r = {"hadm_id": h}
        r.update({f"note_{s}": detect(s, scope["results_course"]) for s in DETECTORS})
        r.update({f"course_{s}": detect(s, scope["course"]) for s in DETECTORS})
        r.update({f"mention_{s}": bool(BROAD[s].search(scope["results_course"])) for s in BROAD})
        rows.append(r)
    return pd.DataFrame(rows)


def stage_notes(a) -> None:
    """Note detectors on the cached pilot notes, merged with the table flags; prints the report."""
    out = Path(a.out)
    tab = pd.read_csv(out / "01_table_flags.csv")
    nf = note_flags(pd.read_parquet(out / "01_pilot_notes.parquet"))
    cov = tab.merge(nf, on="hadm_id", how="left").fillna(False)
    cov.to_csv(out / "01_pilot_coverage.csv", index=False)
    report_coverage(a, cov)


def step_served(cov: pd.DataFrame, cond: str, step: str, panels: list[str], measured: set[str]) -> tuple[pd.Series, pd.Series | None]:
    """Admissions with a real result for a step: (main rule, strict rule or None)."""
    T = lambda c: cov[c].astype(bool)
    if step == "ct_head":
        # main: a separate non-contrast head CT report; the alternative reading (non-contrast
        # phase of a CTA head W&W/O) is returned as the second series, which here is looser.
        loose = T("radfind_ct_head") | (T("radfind_cta_head_with_noncontrast") if "radfind_cta_head_with_noncontrast" in cov else False)
        return T("radfind_ct_head"), loose
    if step == "cta_head_neck":
        return T("radfind_cta_head_neck"), None
    if step == "mri_brain":
        return T("radfind_mri_brain"), None
    if step == "labs":
        strict = pd.concat([T(f"panel_{x}") for x in panels], axis=1).all(axis=1)
        main = pd.concat([T(f"panel_{x}") for x in panels if x in measured], axis=1).all(axis=1)
        return main, strict
    if step == "csf":
        return T("csf_basic"), T("csf_basic") & T("note_lp_opening_pressure")
    if step == "micro:blood_culture":
        return T("micro_blood_culture"), None
    if step == "ecg":
        return T("note_ecg"), None
    if step == "eeg":
        return T("note_eeg"), T("note_eeg") & T("note_eeg_continuous")
    if step == "test:emg_ncs":
        return T("note_emg"), None
    if step == "test:respiratory_function":
        return T("icu_resp_function") | T("note_resp_function"), None
    if step == "cardiac_monitoring":
        return T("note_telemetry"), None
    if step == "echo":
        return T("note_echo"), None
    raise KeyError(step)


def report_coverage(a, cov: pd.DataFrame) -> None:
    cases, out = Path(a.cases), Path(a.out)
    table, summary, loo = [], [], []
    for cond in PILOT:
        g = cov[cov.condition == cond].reset_index(drop=True)
        n_cases, steps, panels, _ = policy_steps(cases, cond)
        core_panels = sorted(k for k, v in panels.items() if v >= n_cases / 2)
        all_ok = pd.Series(True, index=g.index)
        all_strict = pd.Series(True, index=g.index)
        all_ct_loose = pd.Series(True, index=g.index)
        # Panels never resulted for any pilot admission are absent from MIMIC (e.g. procalcitonin).
        measured = {x for x in PANELS if f"panel_{x}" in cov and cov[f"panel_{x}"].any()}
        for step, n in steps.most_common():
            core = n >= n_cases / 2
            entry = {"condition": cond, "step": step, "cases_requiring": f"{n}/{n_cases}", "core": core,
                     "panels": ",".join(core_panels) if step == "labs" else "",
                     "source": SOURCE.get(step, "knowledge tool, no record result needed" if step.startswith("knowledge") else "not mapped")}
            if step in SOURCE and len(g):
                main, strict = step_served(g, cond, step, core_panels, measured)
                entry["admissions_with_result"] = int(main.sum())
                entry["alternative"] = int(strict.sum()) if strict is not None else ""
                if core:
                    all_ok &= main
                    all_strict &= strict if strict is not None and step != "ct_head" else main
                    all_ct_loose &= strict if step == "ct_head" else main
            table.append(entry)
        summary.append({"condition": cond, "cohort": len(g), "all_core_steps_real": int(all_ok.sum()),
                        "all_core_steps_strict": int(all_strict.sum()),
                        "all_core_ct_in_cta_counts": int(all_ct_loose.sum())})
        # Which step binds: all core steps but one.
        served = {}
        for step, n in steps.items():
            if n >= n_cases / 2 and step in SOURCE and len(g):
                served[step] = step_served(g, cond, step, core_panels, measured)[0]
        for step in served:
            others = [v for k, v in served.items() if k != step]
            loo.append({"condition": cond, "without_step": step,
                        "all_other_core_steps": int(pd.concat(others, axis=1).all(axis=1).sum()) if others else len(g)})
        # Labs reduced to the panels resulted in >= 50 % of the condition's cohort.
        common = [x for x in core_panels if f"panel_{x}" in g and g[f"panel_{x}"].mean() >= 0.5]
        if "labs" in served:
            alt = [v for k, v in served.items() if k != "labs"]
            labs_common = pd.concat([g[f"panel_{x}"].astype(bool) for x in common], axis=1).all(axis=1)
            loo.append({"condition": cond, "without_step": f"labs reduced to {','.join(common)}",
                        "all_other_core_steps": int(pd.concat(alt + [labs_common], axis=1).all(axis=1).sum())})
    t, s, lo = pd.DataFrame(table), pd.DataFrame(summary), pd.DataFrame(loo)
    lo.to_csv(out / "01_pilot_leave_one_out.csv", index=False)
    t.to_csv(out / "01_pilot_steps.csv", index=False)
    s.to_csv(out / "01_pilot_summary.csv", index=False)
    # Panel and component coverage per condition, for the report.
    comp_cols = [c for c in cov.columns if c != "hadm_id" and c != "condition"]
    comp = cov.groupby("condition")[comp_cols].sum().astype(int).T.reindex(columns=PILOT)
    comp.insert(0, "-", "")
    comp.loc["(cohort)"] = ["", *[int((cov.condition == c).sum()) for c in PILOT]]
    comp.drop(columns="-").to_csv(out / "01_pilot_components.csv")
    with pd.option_context("display.width", 250, "display.max_colwidth", 60, "display.max_rows", 200):
        print(t.drop(columns="source").to_string(index=False))
        print()
        print(s.to_string(index=False))
        print()
        print(lo.to_string(index=False))
        print()
        print(comp.drop(columns="-").to_string())


# ============================================================================================
# Stage 3: detector check sample, stage 4: score
# ============================================================================================
def stage_sample(a) -> None:
    out = Path(a.out)
    flags = pd.read_csv(out / "01_cohort_flags.csv")
    rng = random.Random(a.seed)
    pick, used = [], set()
    for prev in a.exclude_seed:  # held-out sample: notes not in an earlier sample
        used |= set(pd.read_json(out / f"01_detector_sample_seed{prev}.jsonl", lines=True).hadm_id)
    for cond in PILOT:
        ids = sorted(set(flags[flags.usable & (flags.condition == cond)].hadm_id) - used)
        pick += [(cond, h) for h in rng.sample(ids, min(a.n, len(ids)))] if ids else []
    allnotes = pd.read_parquet(out / "01_pilot_notes.parquet")
    pk = pd.DataFrame(pick, columns=["condition", "hadm_id"])
    notes = pk.merge(allnotes, on="hadm_id", how="inner")
    order = {h: i for i, (_, h) in enumerate(pick)}
    notes = notes.sort_values("hadm_id", key=lambda s: s.map(order))
    with open(out / f"01_detector_sample_seed{a.seed}.jsonl", "w") as f:
        for i, r in enumerate(notes.itertuples()):
            scope = note_scope(r.text)
            for s in STUDIES_BY_CONDITION[r.condition]:
                f.write(json.dumps({"i": i, "condition": r.condition, "hadm_id": int(r.hadm_id), "study": s,
                                    "detector": detect(s, scope["results_course"]),
                                    "passages": passages(BROAD[s], scope["results_course"])}) + "\n")
    print(f"sample written: {len(notes)} notes", file=sys.stderr)


def stage_score(a) -> None:
    out = Path(a.out)
    s = pd.read_json(out / f"01_detector_sample_seed{a.seed}.jsonl", lines=True)
    lab = pd.read_csv(out / f"01_detector_labels_seed{a.seed}.csv")  # i, study, truth (0/1)
    m = s.merge(lab, on=["i", "study"], how="inner")
    if a.rescore:  # re-run the current detector on the cached notes
        notes = pd.read_parquet(out / "01_pilot_notes.parquet").set_index("hadm_id").text
        m["detector"] = [detect(st, note_scope(notes[h])["results_course"]) for h, st in zip(m.hadm_id, m.study)]
    rows = []
    for (cond, study), g in m.groupby(["condition", "study"]):
        tp = int((g.detector & (g.truth == 1)).sum()); fp = int((g.detector & (g.truth == 0)).sum())
        fn = int((~g.detector & (g.truth == 1)).sum()); tn = int((~g.detector & (g.truth == 0)).sum())
        rows.append({"condition": cond, "study": study, "notes": len(g), "true_results": tp + fn, "tp": tp, "fp": fp,
                     "fn": fn, "tn": tn, "precision": round(tp / (tp + fp), 2) if tp + fp else None,
                     "recall": round(tp / (tp + fn), 2) if tp + fn else None})
    df = pd.DataFrame(rows)
    tag = "_rescored" if a.rescore else ""
    df.to_csv(out / f"01_detector_scores_seed{a.seed}{tag}.csv", index=False)
    print(df.to_string(index=False))
    tot = df[["tp", "fp", "fn", "tn"]].sum()
    print(f"\nall: precision {tot.tp / (tot.tp + tot.fp):.2f}, recall {tot.tp / (tot.tp + tot.fn):.2f}, "
          f"tp {tot.tp} fp {tot.fp} fn {tot.fn} tn {tot.tn}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["cohort", "coverage", "notes", "sample", "score", "steps"])
    ap.add_argument("--physionet", default="/eos/user/a/aprotani/physionet")
    ap.add_argument("--cases", default="data/neurobench/cases")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp", required=True)
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--skip-icu", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--rescore", action="store_true")
    ap.add_argument("--exclude-seed", type=int, nargs="*", default=[])
    a = ap.parse_args()
    if not str(Path(a.out).resolve()).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
        sys.exit("--out must be under the PhysioNet workspace (DUA)")
    if a.stage == "steps":
        for cond in PILOT:
            n, steps, panels, variants = policy_steps(Path(a.cases), cond)
            print(f"== {cond} ({n} cases)")
            for k, v in steps.most_common():
                print(f"  {v:>2}  {k}")
            print("  lab panels (smallest alternative):", dict(panels.most_common()))
        return
    {"cohort": stage_cohort, "coverage": stage_coverage, "notes": stage_notes, "sample": stage_sample,
     "score": stage_score}[a.stage](a)


if __name__ == "__main__":
    main()
