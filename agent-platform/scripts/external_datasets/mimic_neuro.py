"""Shared helpers for MIMIC-IV based sources: neuro ICD mapping and discharge-note sections.

The mapping covers the 20 NeuroBench conditions plus the frequent acute neurology that is
not in the benchmark (ICH, SDH, TIA, metabolic encephalopathy), so a source can be graded on
both "matches an existing condition" and "neurological at all".
"""

from __future__ import annotations

import re

# (condition, ICD-10 prefixes, ICD-9 prefixes). First match wins, so specific codes go first.
NEURO_CONDITIONS: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [
    ("SE", ("G41",), ("3453",)),
    ("FEPI", ("G40", "R56"), ("345", "78039", "7803")),
    ("ISCH", ("I63",), ("43301", "43311", "43321", "43331", "43381", "43391", "43401", "43411", "43491", "436")),
    ("SAH", ("I60",), ("430",)),
    ("MS", ("G35",), ("340",)),
    ("MIG", ("G43",), ("346",)),
    ("GBS", ("G610",), ("3570",)),
    ("MG", ("G700",), ("3580",)),
    ("ALS", ("G1221",), ("33520",)),
    ("PD", ("G20",), ("3320",)),
    ("ALZ", ("G30",), ("3310",)),
    ("FTD", ("G310",), ("3311",)),
    ("VASC", ("F01",), ("2904",)),
    ("NPH", ("G912",), ("3313", "3315")),
    ("GLIO", ("C71",), ("191",)),
    ("BACT", ("G00", "G01", "A39"), ("320", "036")),
    ("NMDAR", ("G0481",), ("32381",)),
    ("HEP", ("K7682", "K7291", "K7211", "K7041"), ("5722",)),
    ("SYNC", ("R55",), ("7802",)),
    ("FND", ("F444", "F445", "F446", "F447"), ("30011",)),
    # Neurological, but not one of the 20 NeuroBench conditions.
    ("other:ICH", ("I61", "I62"), ("431", "432")),
    ("other:TIA", ("G45",), ("435",)),
    ("other:traumatic_bleed", ("S064", "S065", "S066"), ("852", "853")),
    ("other:encephalopathy", ("G93", "G92", "E512"), ("3483", "3484", "3485", "34982", "2652")),
    ("other:cerebrovascular", ("I65", "I66", "I67", "I68", "I69"), ("433", "434", "437", "438")),
    ("other:CNS_infection", ("G02", "G03", "G04", "G05", "G06", "A8"), ("321", "322", "323", "324")),
    ("other:dementia", ("F02", "F03", "G31"), ("290", "2941", "331")),
    ("other:neuro", ("G", "R40", "R4182", "R471", "S06", "D33", "D32"), ("3", "7800", "7803", "7804", "850", "851", "854")),
]


# Nervous-system chapter codes that are not neurology for our purpose (sleep apnea, pain).
NOT_NEURO = {10: ("G473", "G89"), 9: ("32723", "338")}


def neuro_condition(code: str, version: int) -> str | None:
    """NeuroBench condition (or ``other:*``) for one ICD code, else None."""
    code = code.strip().replace(".", "")
    if code.startswith(NOT_NEURO[int(version)]):
        return None
    for name, icd10, icd9 in NEURO_CONDITIONS:
        prefixes = icd10 if int(version) == 10 else icd9
        if code.startswith(prefixes):
            # ICD-9 3xx is the nervous system only from 320 to 359.
            if name == "other:neuro" and int(version) == 9 and code[0] == "3" and not "320" <= code[:3] <= "359":
                continue
            return name
    return None


ICD10_CHAPTERS = [
    ("A", "B", "infectious"), ("C", "D4", "neoplasm"), ("D5", "D8", "blood"), ("E", "E", "endocrine"),
    ("F", "F", "mental"), ("G", "G", "nervous"), ("H", "H", "eye_ear"), ("I", "I", "circulatory"),
    ("J", "J", "respiratory"), ("K", "K", "digestive"), ("L", "L", "skin"), ("M", "M", "musculoskeletal"),
    ("N", "N", "genitourinary"), ("O", "O", "pregnancy"), ("P", "Q", "perinatal_congenital"),
    ("R", "R", "symptoms"), ("S", "T", "injury_poisoning"), ("V", "Y", "external"), ("Z", "Z", "factors"),
]
ICD9_CHAPTERS = [
    (1, 139, "infectious"), (140, 239, "neoplasm"), (240, 279, "endocrine"), (280, 289, "blood"),
    (290, 319, "mental"), (320, 389, "nervous"), (390, 459, "circulatory"), (460, 519, "respiratory"),
    (520, 579, "digestive"), (580, 629, "genitourinary"), (630, 679, "pregnancy"), (680, 709, "skin"),
    (710, 739, "musculoskeletal"), (740, 779, "perinatal_congenital"), (780, 799, "symptoms"),
    (800, 999, "injury_poisoning"),
]


def icd_chapter(code: str, version: int) -> str:
    """ICD chapter of a code, as a short name shared by ICD-9 and ICD-10."""
    code = code.strip().replace(".", "").upper()
    if int(version) == 10:
        return next((name for lo, hi, name in ICD10_CHAPTERS if lo <= code[: len(lo)] and code[: len(hi)] <= hi), "other")
    if code[0] in "VE":
        return "factors" if code[0] == "V" else "external"
    return next((name for lo, hi, name in ICD9_CHAPTERS if lo <= int(code[:3]) <= hi), "other")


def dx_family(code: str) -> str:
    """Three-character category: a diagnosis is 'new' when its family has not been coded before."""
    return code.strip().replace(".", "")[:3]


SECTION = re.compile(r"^([A-Z][A-Za-z /&]{2,40}):", re.MULTILINE)


def sections(note: str) -> dict[str, str]:
    """Split a MIMIC discharge summary into its top-level ``Header:`` sections."""
    out: dict[str, str] = {}
    marks = list(SECTION.finditer(note))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(note)
        key = m.group(1).strip()
        if key not in out:
            out[key] = note[m.end() : end].strip()
    return out


def physical_exam(note: str) -> str:
    """Admission physical exam: the text from 'Physical Exam:' to 'Pertinent Results:'."""
    m = re.search(r"Physical Exam:(.*?)(Pertinent Results:|Brief Hospital Course:|$)", note, re.DOTALL)
    return m.group(1).strip() if m else ""


NEURO_EXAM = re.compile(
    r"(neuro|mental status|cranial nerve|\bCN\b|motor|strength|reflex|sensation|gait|coordination|NIHSS)",
    re.IGNORECASE,
)
STUDY_MENTIONS = {
    "eeg": re.compile(r"\bv?EEG\b|electroenceph", re.IGNORECASE),
    "csf": re.compile(r"\bCSF\b|lumbar puncture|\bLP\b", re.IGNORECASE),
    "ecg": re.compile(r"\bEKG\b|\bECG\b", re.IGNORECASE),
    "echo": re.compile(r"\bTTE\b|\bTEE\b|echocardiog", re.IGNORECASE),
    "emg": re.compile(r"\bEMG\b|nerve conduction|\bNCS\b", re.IGNORECASE),
    "head_imaging": re.compile(r"\b(CT|CTA|MRI|MRA|MR)\b[^.\n]{0,25}\b(head|brain|neck|spine)\b|\bNCHCT\b", re.IGNORECASE),
}
HEAD_EXAM = re.compile(r"(CT|CTA|MR|MRI|MRA)[^\n]{0,30}(HEAD|BRAIN|NECK|SPINE|C-SPINE|L-SPINE|T-SPINE)", re.IGNORECASE)
