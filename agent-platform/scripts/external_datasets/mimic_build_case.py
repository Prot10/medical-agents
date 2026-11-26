"""Build NeuroBench cases (``provenance: record``) from MIMIC-IV admissions: the pilot builder.

Stages (all outputs with record content go under OUT, the PhysioNet workspace):

``select``   draws N admissions per condition at random (fixed seed) from the *strict* complete
             sets of ``mimic_pilot_cohort`` (every core policy step has a real result, conservative
             rules: SE needs a continuous/video EEG result, non-contrast CT only from a non-contrast
             exam, labs only up to admission + 24 h). Writes ``02_selection.csv`` (case id <-> hadm).
``extract``  pulls every source row a case needs into ``02_source/<case>.json``: admission,
             patient, ED stay and triage, ED medications, labs, microbiology, radiology reports with
             exam names, provider orders, discharge note, diagnoses, body size.
``draft``    writes ``02_draft/<case>.json``: the deterministic parts (note sections, admission exam
             split, home medications parsed, first lab values, radiology FINDINGS) for the reader who
             writes ``02_manual/<case>.json`` (HPI cut, note-extracted study findings, overrides).
``build``    assembles ``cases/<case>.json`` (a ``NeuroBenchCase``), validates it, and writes the
             review file ``review/<case>.md``.

The manual file is the only hand-written input: the HPI kept and every removed passage with its
reason, and the note-extracted findings of EEG / ECG / echo / telemetry. Everything else is
computed here. No record content in this file (PhysioNet DUA).

    nice -n 10 uv run --no-project --with duckdb --with pandas --with pyarrow --with pydantic \
        --with pyyaml python -I mimic_build_case.py --stage select|extract|draft|build \
        --out $W/out --tmp $W/tmp
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from mimic_pilot_cohort import PANELS, connect, csv, paths, policy_steps, step_served  # noqa: E402

SEED = 20261107
PREFIX = {"SE": "MIMIC-SE", "ISCH": "MIMIC-ISCH"}
CONDITION_ENUM = {"SE": "status_epilepticus", "ISCH": "ischemic_stroke"}
# ICD-10 category whose synonyms apply (US codes SE as G40.x01 and ICD-9 as 345.x / 433-436).
SYNONYM_CATEGORY = {"SE": "G41", "ISCH": "I63"}


def guard_out(out: str) -> Path:
    p = Path(out).resolve()
    if not str(p).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
        sys.exit("--out must be under the PhysioNet workspace (DUA)")
    return p


# ============================================================================================
# select
# ============================================================================================
def strict_set(cov: pd.DataFrame, cond: str, cases: Path) -> pd.Series:
    """Admissions where every core step is served under the conservative rules."""
    g = cov[cov.condition == cond]
    n_cases, steps, panels, _ = policy_steps(cases, cond)
    core_panels = sorted(k for k, v in panels.items() if v >= n_cases / 2)
    measured = {x for x in PANELS if f"panel_{x}" in cov and cov[f"panel_{x}"].any()}
    ok = pd.Series(True, index=g.index)
    for step, n in steps.items():
        if n < n_cases / 2 or step.startswith("knowledge"):
            continue
        main, strict = step_served(g, cond, step, core_panels, measured)
        # ct_head's second series is the looser reading (CT inside a CTA): never used here.
        ok &= strict if (strict is not None and step not in ("ct_head",)) else main
    return g[ok].hadm_id


# The reference diagnosis needs the principal ICD code *and* the discharge diagnosis to name the
# condition; when they disagree (discharge diagnosis "seizure" only, or "expired"), it is uncertain.
DISCHARGE_NAMES = {
    "SE": r"status\s+epilepticus|\bNCSE\b|\bstatus\b",
    "ISCH": r"stroke|infarct|\bCVA\b|cerebral\s+vascular\s+accident|cerebrovascular\s+accident|isch[a]?emi",
}


def eligibility(cond: str, h: int, notes: pd.Series, flags: pd.DataFrame, manual: dict[int, str],
                timing: dict[int, dict]) -> str:
    """'' when eligible, else the exclusion reason. ``manual``: exclusions found when a case was
    read (OUT/02_exclusions.csv: hadm_id, reason), e.g. a core study only outside the window."""
    from mimic_case_assemble import sections
    if h in manual:
        return manual[h]
    row = flags[flags.hadm_id == h].iloc[0]
    if (row.get("anchor_age_at_admit") or 0) > 90:
        return "age above 90 (MIMIC shifts it; the schema allows 18-90)"
    dx = sections(notes.get(h, "")).get("Discharge Diagnosis", "")
    if not re.search(DISCHARGE_NAMES[cond], dx, re.I):
        return "discharge diagnosis does not name the condition"
    t = timing.get(h, {})
    if t.get("ct") is None or t["ct"] > t["lab_end"]:
        return "no non-contrast head CT exam by admission + 24 h"
    if cond == "ISCH" and (t.get("cta") is None or t["ct"] > t["cta"] + 0.5):
        return "the non-contrast head CT exam follows the CTA (presentation CT only inside the CTA report)"
    if cond == "ISCH" and t["cta"] > t["lab_end"]:
        return "no CTA by admission + 24 h (stroke recognised later in the stay)"
    return ""


def imaging_timing(con, p, pool: pd.DataFrame) -> dict[int, dict]:
    """Hours from ED arrival of the first non-contrast head CT and the first CTA head/neck report
    with a FINDINGS section, and of admission + 24 h, per admission of the pool."""
    from mimic_case_assemble import FINDINGS
    pool = pool.assign(admittime=pd.to_datetime(pool.admittime), dischtime=pd.to_datetime(pool.dischtime))
    con.register("pool_df", pool[["hadm_id", "subject_id", "t0", "admittime", "dischtime"]])
    rad = con.execute(f"""
        select p.hadm_id, upper(d.field_value) exam, r.charttime, r.text, p.t0, p.admittime
        from {csv(p['note'] / 'radiology.csv.gz')} r join {csv(p['note'] / 'radiology_detail.csv.gz')} d using (note_id)
        join pool_df p on r.subject_id = p.subject_id and r.charttime between p.t0 and p.dischtime
        where d.field_name = 'exam_name' and regexp_matches(upper(d.field_value), '^(CT HEAD W/O|PORTABLE HEAD CT W/O|ED CODE STROKE ONLY CT|CT BRAIN W/O|CTA (HEAD|NECK)|ED STROKE CTA|CTA HEAD AND)')
    """).df()
    out: dict[int, dict] = {}
    for h, g in rad.groupby("hadm_id"):
        g = g[g.text.str.contains(FINDINGS, regex=True)]
        t_ed = g.t0.iloc[0] + pd.Timedelta(hours=1) if len(g) else None
        hrs = lambda x: (pd.Timestamp(x) - t_ed).total_seconds() / 3600
        ct = g[~g.exam.str.startswith(("CTA", "ED STROKE CTA"))]
        cta = g[g.exam.str.startswith(("CTA", "ED STROKE CTA"))]
        out[h] = {"ct": hrs(ct.charttime.min()) if len(ct) else None, "cta": hrs(cta.charttime.min()) if len(cta) else None,
                  "lab_end": hrs(pd.Timestamp(g.admittime.iloc[0]) + pd.Timedelta(hours=24)) if len(g) else None}
    return out


def stage_select(a) -> None:
    out = guard_out(a.out)
    cov = pd.read_csv(out / "01_pilot_coverage.csv")
    flags = pd.read_csv(out / "01_cohort_flags.csv")
    notes = pd.read_parquet(out / "01_pilot_notes.parquet").set_index("hadm_id").text
    # Age at admission (MIMIC: anchor_age + years since anchor_year).
    p, con = paths(a.physionet), connect(a.tmp)
    pat = con.execute(f"select subject_id, anchor_age, anchor_year from {csv(p['hosp'] / 'patients.csv.gz')}").df()
    flags = flags.merge(pat, on="subject_id", how="left")
    flags["anchor_age_at_admit"] = flags.anchor_age + pd.to_datetime(flags.admittime).dt.year - flags.anchor_year
    ex_path = out / "02_exclusions.csv"
    manual = dict(pd.read_csv(ex_path)[["hadm_id", "reason"]].itertuples(index=False)) if ex_path.exists() else {}
    pools = {cond: sorted(strict_set(cov, cond, Path(a.cases))) for cond in a.conditions}
    pool_rows = flags[flags.hadm_id.isin([h for v in pools.values() for h in v])].copy()
    pool_rows["t0"] = pd.to_datetime(pool_rows[["ed_intime", "admittime"]].min(axis=1)) - pd.Timedelta(hours=1)
    timing = imaging_timing(con, p, pool_rows)
    rng = random.Random(a.seed)
    rows, excl = [], []
    for cond in a.conditions:
        pool = pools[cond]
        picked = rng.sample(pool, len(pool))  # a full random order; the first N eligible are used
        n = 0
        for rank, h in enumerate(picked, start=1):
            reason = eligibility(cond, h, notes, flags, manual, timing)
            excl.append({"condition": cond, "reason": reason or "eligible"})
            cid = ""
            if not reason and n < a.n:
                n += 1
                cid = f"{PREFIX[cond]}-{n:03d}"
            rows.append({"case_id": cid, "condition": cond, "hadm_id": int(h),
                         "subject_id": int(flags.loc[flags.hadm_id == h, "subject_id"].iloc[0]),
                         "draw_rank": rank, "exclusion": reason})
        print(f"{cond}: strict complete set {len(pool)}, selected {n}", file=sys.stderr)
    sel = pd.DataFrame(rows)
    sel.to_csv(out / "02_selection.csv", index=False)
    counts = pd.DataFrame(excl).groupby(["condition", "reason"]).size().rename("admissions").reset_index()
    counts.to_csv(out / "02_eligibility_counts.csv", index=False)
    print(counts.to_string(index=False), file=sys.stderr)
    # Exclusions met before the fifth selected case, per condition (the draws actually skipped).
    for cond in a.conditions:
        g = sel[sel.condition == cond]
        last = g[g.case_id != ""].draw_rank.max()
        skipped = g[(g.draw_rank < last) & (g.exclusion != "")]
        print(f"{cond}: skipped before the last selected draw: {len(skipped)} "
              f"({skipped.exclusion.value_counts().to_dict()})", file=sys.stderr)


# ============================================================================================
# extract
# ============================================================================================
def stage_extract(a) -> None:
    out = guard_out(a.out)
    p, con = paths(a.physionet), connect(a.tmp)
    sel = pd.read_csv(out / a.selection)
    sel = sel[sel.case_id.notna() & (sel.case_id != "")]
    if a.cases_only:
        sel = sel[sel.case_id.isin(a.cases_only)]
    con.register("sel", sel[["case_id", "hadm_id", "subject_id"]])
    h, e, n = p["hosp"], p["ed"], p["note"]
    q = lambda sql: con.execute(sql).df()
    adm = q(f"select a.* from {csv(h / 'admissions.csv.gz')} a join sel using (hadm_id)")
    pat = q(f"select p.* from {csv(h / 'patients.csv.gz')} p where subject_id in (select subject_id from sel)")
    eds = q(f"select x.* from {csv(e / 'edstays.csv.gz')} x join sel using (hadm_id)")
    con.register("eds_df", eds[["stay_id"]])
    tri = q(f"select t.* from {csv(e / 'triage.csv.gz')} t where stay_id in (select stay_id from eds_df)")
    vit = q(f"select v.* from {csv(e / 'vitalsign.csv.gz')} v where stay_id in (select stay_id from eds_df)")
    medrec = q(f"select m.* from {csv(e / 'medrecon.csv.gz')} m where stay_id in (select stay_id from eds_df)")
    pyxis = q(f"select m.* from {csv(e / 'pyxis.csv.gz')} m where stay_id in (select stay_id from eds_df)")
    eddx = q(f"select m.* from {csv(e / 'diagnosis.csv.gz')} m where stay_id in (select stay_id from eds_df)")
    dx = q(f"""select d.*, t.long_title from {csv(h / 'diagnoses_icd.csv.gz')} d join sel using (hadm_id)
               left join {csv(h / 'd_icd_diagnoses.csv.gz')} t using (icd_code, icd_version)""")
    # Window per case: ED arrival (or admission) - 1 h to discharge.
    win = adm[["hadm_id", "subject_id", "admittime", "dischtime"]].merge(
        eds.groupby("hadm_id").intime.min().rename("ed_intime").reset_index(), on="hadm_id", how="left")
    win["t0"] = win[["ed_intime", "admittime"]].min(axis=1) - pd.Timedelta(hours=1)
    con.register("win", win)
    labs = q(f"""
        select l.*, i.label, i.fluid, i.category from {csv(h / 'labevents.csv.gz')} l
        join {csv(h / 'd_labitems.csv.gz')} i using (itemid)
        join win w on l.subject_id = w.subject_id and l.charttime between w.t0 and w.dischtime""")
    micro = q(f"""
        select m.* from {csv(h / 'microbiologyevents.csv.gz')} m join win w on m.subject_id = w.subject_id
        and coalesce(m.charttime, cast(m.chartdate as timestamp)) between w.t0 and w.dischtime""")
    rad = q(f"""
        select r.note_id, r.subject_id, r.hadm_id, r.note_type, r.charttime, r.storetime, r.text,
               d.field_value exam_name, w.hadm_id as window_hadm
        from {csv(n / 'radiology.csv.gz')} r
        join {csv(n / 'radiology_detail.csv.gz')} d using (note_id)
        join win w on r.subject_id = w.subject_id and r.charttime between w.t0 and w.dischtime
        where d.field_name = 'exam_name'""")
    poe = q(f"select o.* from {csv(h / 'poe.csv.gz')} o join sel using (hadm_id)")
    note = q(f"select d.* from {csv(n / 'discharge.csv.gz')} d join sel using (hadm_id)")
    omr = q(f"select o.* from {csv(h / 'omr.csv.gz')} o where subject_id in (select subject_id from sel)")
    # MIMIC-IV-ECG machine reads (decision 1) and ICU rhythm / heart rate / ectopy / NIF / VC (5).
    E = Path(a.physionet) / "mimic-iv-ecg/1.0"
    ecg = q(f"""select m.* from read_csv_auto('{E / 'machine_measurements.csv'}', sample_size=-1) m
                join win w on m.subject_id = w.subject_id and m.ecg_time between w.t0 and w.dischtime""")
    chart = q(f"""select x.hadm_id, x.itemid, x.charttime, x.value, x.valuenum, x.valueuom
                  from {csv(p['icu'] / 'chartevents.csv.gz')} x join sel using (hadm_id)
                  where x.itemid in (220048, 220045, 224650, 224651, 224419, 220218, 224420)""")
    (out / "02_source").mkdir(exist_ok=True)
    for r in sel.itertuples():
        bundle = {
            "case_id": r.case_id, "hadm_id": int(r.hadm_id), "subject_id": int(r.subject_id),
            "admission": adm[adm.hadm_id == r.hadm_id].to_dict("records"),
            "patient": pat[pat.subject_id == r.subject_id].to_dict("records"),
            "edstays": eds[eds.hadm_id == r.hadm_id].to_dict("records"),
            "triage": tri[tri.stay_id.isin(eds[eds.hadm_id == r.hadm_id].stay_id)].to_dict("records"),
            "ed_vitals": vit[vit.stay_id.isin(eds[eds.hadm_id == r.hadm_id].stay_id)].to_dict("records"),
            "ed_medrecon": medrec[medrec.stay_id.isin(eds[eds.hadm_id == r.hadm_id].stay_id)].to_dict("records"),
            "ed_pyxis": pyxis[pyxis.stay_id.isin(eds[eds.hadm_id == r.hadm_id].stay_id)].to_dict("records"),
            "ed_diagnosis": eddx[eddx.stay_id.isin(eds[eds.hadm_id == r.hadm_id].stay_id)].to_dict("records"),
            "window": win[win.hadm_id == r.hadm_id].to_dict("records"),
            "diagnoses": dx[dx.hadm_id == r.hadm_id].sort_values("seq_num").to_dict("records"),
            "labs": labs[labs.subject_id == r.subject_id].merge(win[win.hadm_id == r.hadm_id][["subject_id"]]).to_dict("records"),
            "micro": micro[micro.subject_id == r.subject_id].to_dict("records"),
            "radiology": rad[rad.window_hadm == r.hadm_id].sort_values("charttime").to_dict("records"),
            "poe": poe[poe.hadm_id == r.hadm_id].sort_values("ordertime").to_dict("records"),
            "discharge": note[note.hadm_id == r.hadm_id].to_dict("records"),
            "omr": omr[omr.subject_id == r.subject_id].to_dict("records"),
            "ecg_machine": ecg[ecg.subject_id == r.subject_id].sort_values("ecg_time").to_dict("records"),
            "icu_chart": chart[chart.hadm_id == r.hadm_id].sort_values("charttime").to_dict("records"),
        }
        (out / "02_source" / f"{r.case_id}.json").write_text(json.dumps(bundle, default=str, indent=0))
        print(f"{r.case_id}: labs {len(bundle['labs'])}, radiology {len(bundle['radiology'])}, poe {len(bundle['poe'])}, "
              f"notes {len(bundle['discharge'])}", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["select", "extract", "draft", "build"])
    ap.add_argument("--physionet", default="/eos/user/a/aprotani/physionet")
    ap.add_argument("--cases", default=str(ROOT / "data/neurobench/cases"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp", required=True)
    ap.add_argument("--conditions", nargs="+", default=["SE", "ISCH"])
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--cases-only", nargs="*", default=[])
    ap.add_argument("--selection", default="02_selection.csv", help="selection file under OUT")
    a = ap.parse_args()
    stages = {"select": stage_select, "extract": stage_extract}
    if a.stage in ("draft", "build"):
        from mimic_case_assemble import stage_build, stage_draft  # noqa: E402
        stages.update({"draft": stage_draft, "build": stage_build})
    stages[a.stage](a)


if __name__ == "__main__":
    main()
