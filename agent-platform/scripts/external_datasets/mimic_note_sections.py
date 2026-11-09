"""Which discharge-summary sections a NeuroBench case can be built from, per condition. Counts only.

For admissions whose principal diagnosis maps to a NeuroBench condition (``mimic_neuro``), and
for all discharge summaries as a baseline: the share of notes that carry each section a case
needs, the median HPI length, how often the HPI already states a study result (leakage that the
conversion must strip), and how often the hospital course mentions an EEG, an LP or an EMG, the
studies with no structured result in MIMIC. Never prints note text (PhysioNet DUA: this output
is read by a Claude session).

    uv run --no-project --python 3.12 --with duckdb --with pandas python -I mimic_note_sections.py \
        --hosp .../mimiciv/3.1/hosp --note .../mimic-iv-note/2.2/note [--out sections.csv]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mimic_neuro import neuro_condition

SECTIONS = {
    "chief_complaint": r"Chief Complaint:",
    "hpi": r"History of Present Illness:",
    "pmh": r"Past Medical History:",
    "allergies": r"Allergies:",
    "meds_on_admission": r"Medications on Admission:",
    "social_history": r"Social History:",
    "family_history": r"Family History:",
    "physical_exam": r"Physical Exam:",
    "pertinent_results": r"Pertinent Results:",
    "hospital_course": r"Brief Hospital Course:",
    "discharge_diagnosis": r"Discharge Diagnos[ie]s:",
}
# HPI ends at the next history/exam header.
HPI = (r"(?s)History of Present Illness:(.*?)\n\s*(Past Medical History|PMH|Review of Systems|ROS|"
       r"Past Surgical History|Social History|Family History|Physical Exam|Allergies)\s*:")
COURSE = r"(?s)Brief Hospital Course:(.*?)(\n\s*(Medications on Admission|Discharge Medications)\s*:|$)"
# A study named with a finding verb: the HPI tells the agent what a tool would return.
RESULT_IN_HPI = (r"(?i)\b(CT|CTA|NCHCT|MRI|MRA|MR|LP|CSF|EEG|EMG|CXR|imaging)\b[^.\n]{0,80}"
                 r"\b(show|showed|shows|reveal|revealed|demonstrat|notable for|significant for|positive|"
                 r"c/w|consistent with|concerning for|found)")
COURSE_MENTIONS = {
    "course_eeg": r"(?i)\bv?EEG\b|electroenceph",
    "course_lp": r"(?i)\bLP\b|lumbar puncture|\bCSF\b",
    "course_emg": r"(?i)\bEMG\b|nerve conduction|\bNCS\b",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hosp", required=True)
    ap.add_argument("--note", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    con = duckdb.connect()
    con.execute("set memory_limit = '24GB'; set threads = 8")
    csv = lambda d, name: f"read_csv_auto('{Path(d) / name}', sample_size=-1)"
    codes = con.execute(
        f"select distinct icd_code code, icd_version v from {csv(a.hosp, 'diagnoses_icd.csv.gz')} where seq_num = 1"
    ).df()
    codes["condition"] = [neuro_condition(c, v) for c, v in zip(codes.code, codes.v)]
    con.register("icdmap", codes.dropna(subset=["condition"]))
    con.execute(f"""
        create table pdx as select d.hadm_id, m.condition
        from {csv(a.hosp, 'diagnoses_icd.csv.gz')} d
        join icdmap m on d.icd_code = m.code and d.icd_version = m.v where d.seq_num = 1
    """)
    has = ", ".join(f"regexp_matches(text, '(?m)^{rx}') as {k}" for k, rx in SECTIONS.items())
    course = ", ".join(f"regexp_matches(course, '{rx}') as {k}" for k, rx in COURSE_MENTIONS.items())
    con.execute(f"""
        create table notes as
        with n as (
            select hadm_id, text, regexp_extract(text, '{HPI}', 1) as hpi_text,
                   regexp_extract(text, '{COURSE}', 1) as course
            from {csv(a.note, 'discharge.csv.gz')}
        )
        select hadm_id, {has}, length(hpi_text) as hpi_len,
               regexp_matches(hpi_text, '{RESULT_IN_HPI}') as hpi_states_result,
               regexp_matches(hpi_text, '(?i)\\bin the ED\\b|\\bED course\\b|\\bat OSH\\b|outside hospital') as hpi_mentions_ed_or_osh,
               {course}
        from n
    """)
    flags = [*SECTIONS, "hpi_states_result", "hpi_mentions_ed_or_osh", *COURSE_MENTIONS]
    share = ", ".join(f"round(100 * avg({k}::int), 1) as {k}" for k in flags)
    cols = f"count(*) as notes, median(hpi_len) filter (where hpi_len > 0) as hpi_median_chars, {share}"
    df = con.execute(f"""
        select '(all notes)' as condition, {cols} from notes
        union all
        (select p.condition, {cols} from notes n join pdx p using (hadm_id)
         where p.condition not like 'other:%' group by p.condition order by notes desc)
    """).df()
    with pd.option_context("display.width", 250, "display.max_columns", 40):
        print("Shares in % of notes; hpi_median_chars over notes with an HPI.")
        print(df.to_string(index=False))
    if a.out:
        df.to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
