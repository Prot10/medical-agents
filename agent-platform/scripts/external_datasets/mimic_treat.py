"""Treatment times that change a lab analyte (workspace CLAUDE.md, decision 23), and the lab
analytes each treatment class affects. No record content in this file (PhysioNet DUA).

Sources, all restricted to the lab window of an admission (ED arrival - 1 h to admission + 24 h):
- ED ``pyxis`` (dispense time; the earliest time a drug can have been given in the ED),
- hosp ``emar`` administrations (event text says given / started / applied),
- hosp ``prescriptions`` start time, only for admissions without any emar row (older years),
- ICU ``inputevents`` start time (drugs, fluids, blood products),
- ICU ``procedureevents`` intubation / invasive ventilation, ``chartevents`` ventilator mode.

A lab value of an analyte is not served when a treatment of the class that changes it is timed at
or before the draw (``<=``: conservative, a dispense or order time precedes the administration).
"""

from __future__ import annotations

import re

import pandas as pd

CLASSES = {
    "glucose": re.compile(r"(?i)insulin|humalog|novolog|lispro|aspart|glargine|lantus|levemir|detemir|\bNPH\b|"
                          r"dextrose|\bD\s?(?:5|10|12\.5|20|25|50)\b|\bD\d+W\b|\bD5|glucose (?:gel|tab|40)"),
    "transfusion": re.compile(r"(?i)packed red|red blood cell|\bP?RBCs?\b|platelets?(?!\s+count)|whole blood|"
                              r"leukoreduced|irradiated (?:red|plat)"),
    "ventilation": re.compile(r"(?i)succinylcholine|succynlocholine|rocuronium|vecuronium|cis-?atracurium|etomidate|"
                              r"^intubation$|invasive ventilation|ventilator mode"),
    "anticoagulation": re.compile(r"(?i)^(?!.*(?:flush|lock|\bline\b|dwell|catheter|PICC)).*heparin|enoxaparin|lovenox|"
                                  r"argatroban|bivalirudin|phytonadione|vitamin k\b|prothrombin complex|kcentra|profilnine|"
                                  r"\bPCC\b|fresh frozen plasma|\bFFP\b|\bplasma\b|cryoprecipitate|protamine|idarucizumab|"
                                  r"praxbind|andexanet"),
    "antiseizure": re.compile(r"(?i)phenyto|fosphenyto|dilantin|cerebyx|valpro|depak|levetir|keppra|phenobarb|"
                              r"carbamaz|tegretol|lacosam|vimpat|lamotri|lamictal"),
}

# Lab labels (d_labitems, fluid Blood) whose value a treatment class changes.
AFFECTS = {
    "glucose": {"Glucose"},  # decision 23 (first values); repeats also withhold potassium (decision 47, mimic_case_build6)
    "transfusion": {"Hemoglobin", "Hematocrit", "Platelet Count", "Hematocrit, Calculated", "Red Blood Cells"},
    "ventilation": {"pH", "pO2", "pCO2", "Base Excess", "Calculated Total CO2", "Oxygen Saturation",
                    "Alveolar-arterial Gradient", "Required O2", "Oxygen",
                    # task 06 re-read: pH-dependent values of the same gas sample
                    "Free Calcium", "Calculated Bicarbonate, Whole Blood", "Carboxyhemoglobin", "Methemoglobin"},
    "anticoagulation": {"INR(PT)", "PT", "PTT"},
}
AED_LEVELS = {"Phenytoin": r"phenyto|dilantin|cerebyx", "Free Phenytoin": r"phenyto|dilantin|cerebyx",
              "Valproic Acid": r"valpro|depak", "Levetiracetam": r"levetir|keppra", "Phenobarbital": r"phenobarb",
              "Carbamazepine": r"carbamaz|tegretol", "Lacosamide": r"lacosam|vimpat", "Lamotrigine": r"lamotri|lamictal"}

EMAR_GIVEN = re.compile(r"(?i)administered|^started|restarted|^applied|^confirmed|bolus|rate change|^in place")


def classify(name: str) -> list[str]:
    return [k for k, rx in CLASSES.items() if rx.search(str(name or ""))]


def treatment_rows(con, p: dict, win: pd.DataFrame) -> pd.DataFrame:
    """win: hadm_id, subject_id, t0, t_end. Returns hadm_id, t, source, name, classes (';'), any_ed."""
    from mimic_pilot_cohort import csv
    con.register("tw", win[["hadm_id", "subject_id", "t0", "t_end"]])
    q = lambda s: con.execute(s).df()
    ed = q(f"""select e.hadm_id, x.charttime t, 'ed_pyxis' source, x.name from {csv(p['ed'] / 'pyxis.csv.gz')} x
               join {csv(p['ed'] / 'edstays.csv.gz')} e using (subject_id, stay_id) join tw w using (hadm_id)
               where x.charttime between w.t0 and w.t_end""")
    em = q(f"""select x.hadm_id, x.charttime t, 'hosp_emar' source, x.medication name, x.event_txt
               from {csv(p['hosp'] / 'emar.csv.gz')} x join tw w using (hadm_id)
               where x.charttime between w.t0 and w.t_end""")
    em = em[em.event_txt.astype(str).str.contains(EMAR_GIVEN, na=False)].drop(columns="event_txt")
    has_emar = set(q(f"select distinct hadm_id from {csv(p['hosp'] / 'emar.csv.gz')} where hadm_id in (select hadm_id from tw)").hadm_id)
    rx = q(f"""select x.hadm_id, x.starttime t, 'hosp_prescriptions' source, x.drug name
               from {csv(p['hosp'] / 'prescriptions.csv.gz')} x join tw w using (hadm_id)
               where x.starttime between w.t0 and w.t_end""")
    rx = rx[~rx.hadm_id.isin(has_emar)]
    ie = q(f"""select x.hadm_id, x.starttime t, 'icu_inputevents' source, d.label name
               from {csv(p['icu'] / 'inputevents.csv.gz')} x join {csv(p['icu'] / 'd_items.csv.gz')} d using (itemid)
               join tw w using (hadm_id) where x.starttime between w.t0 and w.t_end""")
    pe = q(f"""select x.hadm_id, x.starttime t, 'icu_procedureevents' source, d.label name
               from {csv(p['icu'] / 'procedureevents.csv.gz')} x join {csv(p['icu'] / 'd_items.csv.gz')} d using (itemid)
               join tw w using (hadm_id) where x.itemid in (224385, 225792) and x.starttime between w.t0 and w.t_end""")
    ce = q(f"""select x.hadm_id, min(x.charttime) t, 'icu_chartevents' source, 'Ventilator Mode' name
               from {csv(p['icu'] / 'chartevents.csv.gz')} x join tw w using (hadm_id)
               where x.itemid in (223849, 229314) and x.charttime between w.t0 and w.t_end group by 1""")
    allr = pd.concat([ed, em, rx, ie, pe, ce], ignore_index=True)
    allr["t"] = pd.to_datetime(allr.t)
    names = {n: ";".join(classify(n)) for n in allr.name.dropna().unique()}
    allr["classes"] = allr.name.map(names).fillna("")
    return allr


def first_times(tr: pd.DataFrame) -> pd.DataFrame:
    """Per admission: earliest time per class, and the earliest ED medication of any kind."""
    rows = []
    for h, g in tr.groupby("hadm_id"):
        r = {"hadm_id": h, "t_first_ed_med": g[g.source == "ed_pyxis"].t.min()}
        for k in CLASSES:
            x = g[g.classes.str.contains(k, na=False)]
            r[f"t_{k}"] = x.t.min()
        rows.append(r)
    return pd.DataFrame(rows)


def blocked(label: str, t, tt: dict, aed_names: list[tuple]) -> str:
    """Class name when the value of `label` drawn at t follows a treatment that changes it; else ''.
    tt: class -> earliest time; aed_names: (time, name) of antiseizure doses."""
    for k, labels in AFFECTS.items():
        if label in labels and pd.notna(tt.get(k)) and tt[k] <= t:
            return k
    rx = AED_LEVELS.get(label)
    if rx and any(re.search(rx, str(n), re.I) and ti <= t for ti, n in aed_names):
        return "antiseizure"
    return ""


# --- decision 30 (task 06): prophylactic anticoagulation does not block ---------------------------
THERAPEUTIC_ALWAYS = re.compile(r"(?i)warfarin|coumadin|apixaban|eliquis|rivaroxaban|xarelto|dabigatran|pradaxa|edoxaban|"
                                r"argatroban|bivalirudin|alteplase|tenecteplase|\btPA\b|activase|kcentra|prothrombin complex|"
                                r"profilnine|\bPCC\b|phytonadione|vitamin k\b|protamine|idarucizumab|praxbind|andexanet|"
                                r"fresh frozen plasma|\bFFP\b|cryoprecipitate")
CLASSES["anticoagulation"] = re.compile(CLASSES["anticoagulation"].pattern + r"|" + THERAPEUTIC_ALWAYS.pattern.replace("(?i)", ""), re.I)


def anticoag_level(name: str, dose, unit, route, itemid=None, source: str = "") -> str:
    """'therapeutic' (blocks INR/aPTT), 'prophylactic' (does not), or 'unknown' (blocks: conservative)."""
    n, u, rt = str(name or ""), str(unit or "").lower(), str(route or "").upper()
    if THERAPEUTIC_ALWAYS.search(n):
        return "therapeutic"
    if itemid is not None and not pd.isna(itemid):
        return "prophylactic" if int(itemid) == 225975 else "therapeutic"  # ICU: 225975 Heparin Sodium (Prophylaxis)
    try:
        d = float(str(dose).split("-")[0])
    except (TypeError, ValueError):
        d = None
    if re.search(r"(?i)heparin", n):
        if re.search(r"(?i)infusion|drip|premix|in d5w|in 0\.45|25,?000|/250|bolus", n) or rt in ("IV", "IV DRIP", "IV BOLUS", "IVPB"):
            return "therapeutic"
        if rt in ("SC", "SUBCUT", "SUBQ", "SQ") or re.search(r"(?i)\bsc\b|subcut|5,?000 ?unit", n):
            if d is None:
                return "prophylactic" if re.search(r"(?i)5,?000", n) else "unknown"
            return "prophylactic" if d <= 5000 and "unit" in (u or "unit") else "therapeutic"
        return "unknown"
    if re.search(r"(?i)enoxaparin|lovenox", n):
        if d is None:
            return "unknown"
        return "prophylactic" if d <= 40 else "therapeutic"
    if re.search(r"(?i)dalteparin|fragmin", n):
        if d is None:
            return "unknown"
        return "prophylactic" if d <= 5000 else "therapeutic"
    return "unknown"


def anticoag_rows(con, p: dict, win: pd.DataFrame) -> pd.DataFrame:
    """Anticoagulant administrations in the window with dose and route (decision 30)."""
    from mimic_pilot_cohort import csv
    con.register("aw", win[["hadm_id", "subject_id", "t0", "t_end"]])
    rx = r"(?i)heparin|enoxaparin|lovenox|dalteparin|fragmin|warfarin|coumadin|apixaban|rivaroxaban|dabigatran|edoxaban|argatroban|bivalirudin|alteplase|tenecteplase"
    q = lambda s: con.execute(s).df()
    em = q(f"""select x.hadm_id, x.charttime t, 'hosp_emar' source, x.medication name, d.dose_given dose, d.dose_given_unit unit, d.route, null itemid
               from {csv(p['hosp'] / 'emar.csv.gz')} x join aw w using (hadm_id)
               left join (select emar_id, max(dose_given) dose_given, max(dose_given_unit) dose_given_unit, max(route) route
                          from {csv(p['hosp'] / 'emar_detail.csv.gz')} group by 1) d using (emar_id)
               where x.charttime between w.t0 and w.t_end and regexp_matches(x.medication, '{rx}')""")
    pr = q(f"""select x.hadm_id, x.starttime t, 'hosp_prescriptions' source, x.drug name, x.dose_val_rx dose, x.dose_unit_rx unit, x.route, null itemid
               from {csv(p['hosp'] / 'prescriptions.csv.gz')} x join aw w using (hadm_id)
               where x.starttime between w.t0 and w.t_end and regexp_matches(x.drug, '{rx}')""")
    ie = q(f"""select x.hadm_id, x.starttime t, 'icu_inputevents' source, d.label name, x.amount dose, x.amountuom unit, null route, x.itemid
               from {csv(p['icu'] / 'inputevents.csv.gz')} x join {csv(p['icu'] / 'd_items.csv.gz')} d using (itemid)
               join aw w using (hadm_id) where x.starttime between w.t0 and w.t_end and regexp_matches(d.label, '{rx}')""")
    ed = q(f"""select e.hadm_id, x.charttime t, 'ed_pyxis' source, x.name, null dose, null unit, null route, null itemid
               from {csv(p['ed'] / 'pyxis.csv.gz')} x join {csv(p['ed'] / 'edstays.csv.gz')} e using (subject_id, stay_id)
               join aw w using (hadm_id) where x.charttime between w.t0 and w.t_end and regexp_matches(x.name, '{rx}')""")
    a = pd.concat([em, pr, ie, ed], ignore_index=True)
    a["t"] = pd.to_datetime(a.t)
    a = a[~a.name.astype(str).str.contains(r"(?i)flush|lock|dwell|catheter|PICC", na=False)]
    a["level"] = [anticoag_level(n, d, u, r, i, s) for n, d, u, r, i, s in zip(a.name, a.dose, a.unit, a.route, a.itemid, a.source)]
    return a
