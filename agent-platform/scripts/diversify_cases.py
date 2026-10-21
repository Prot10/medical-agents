#!/usr/bin/env python
"""
Diversify NeuroBench v1 case files: demographics, labs, vitals, allergies,
occupations, names, ICD codes, and metadata standardization.

Idempotent — running twice produces the same output (seeded RNG).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from random import Random

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = REPO_ROOT / "data" / "neurobench_v1" / "cases"
BACKUP_DIR = REPO_ROOT / "data" / "neurobench_v1" / "cases_backup"

# ---------------------------------------------------------------------------
# Skip list — these files are being rewritten by other agents
# ---------------------------------------------------------------------------
SKIP_IDS = {
    "ISCH-STR-P02", "ISCH-STR-P03",
    "ALZ-EARLY-P02", "ALZ-EARLY-P03",
    "PD-P02", "PD-P03",
    "GLIO-HG-P02",
    "SYNC-CARD-P03",
    "FEPI-TEMP-P02", "FEPI-TEMP-P03",
    "BACT-MEN-P02", "BACT-MEN-P03",
    "NMDAR-ENC-P02", "NMDAR-ENC-P03",
    "FND-P02", "FND-P03",
}

# ---------------------------------------------------------------------------
# Fix 2: Demographic targets  (case_id -> {field: value, ...})
# Only cases that need CHANGES are listed.  "Keep" cases are omitted.
# ---------------------------------------------------------------------------
DEMO_CHANGES: dict[str, dict] = {
    # ISCH-STR
    "ISCH-STR-S03": {"age": 55, "sex": "male", "ethnicity": "South Asian", "bmi": 28.7},
    "ISCH-STR-S04": {"age": 78, "sex": "female", "ethnicity": "East Asian", "bmi": 25.2},
    "ISCH-STR-M02": {"age": 58, "sex": "female", "ethnicity": "Hispanic", "bmi": 27.4},
    "ISCH-STR-M03": {"age": 73, "sex": "male", "ethnicity": "Caucasian", "bmi": 29.8},
    # ALZ-EARLY
    "ALZ-EARLY-S03": {"age": 69, "sex": "female", "ethnicity": "South Asian", "bmi": 23.1},
    "ALZ-EARLY-S04": {"age": 81, "sex": "male", "ethnicity": "East Asian", "bmi": 22.8},
    "ALZ-EARLY-M02": {"age": 73, "sex": "female", "ethnicity": "African American", "bmi": 29.4},
    "ALZ-EARLY-M03": {"age": 66, "sex": "male", "ethnicity": "Caucasian", "bmi": 26.1},
    # PD
    "PD-S02": {"age": 62, "sex": "female", "ethnicity": "African American", "bmi": 27.2},
    "PD-S03": {"age": 71, "sex": "male", "ethnicity": "East Asian", "bmi": 23.5},
    "PD-S04": {"ethnicity": "Hispanic", "bmi": 26.4},  # keep age/sex
    "PD-M02": {"age": 64, "sex": "female", "ethnicity": "South Asian", "bmi": 22.8},
    "PD-M03": {"age": 75, "sex": "male", "ethnicity": "African American", "bmi": 28.1},
    # GLIO-HG
    "GLIO-HG-S02": {"age": 64, "sex": "female", "ethnicity": "African American", "bmi": 29.4},
    "GLIO-HG-S03": {"age": 52, "sex": "male", "ethnicity": "Hispanic", "bmi": 25.8},
    "GLIO-HG-S04": {"age": 71, "sex": "male", "ethnicity": "East Asian", "bmi": 24.2},
    "GLIO-HG-M02": {"age": 47, "sex": "male", "ethnicity": "African American", "bmi": 28.8},
    "GLIO-HG-M03": {"ethnicity": "Hispanic"},  # keep rest
    # BACT-MEN
    "BACT-MEN-S02": {"age": 38, "sex": "female", "ethnicity": "South Asian", "bmi": 24.1},
    "BACT-MEN-S03": {"age": 62, "sex": "male", "ethnicity": "Hispanic", "bmi": 28.4},
    "BACT-MEN-M02": {"age": 42, "sex": "female", "ethnicity": "African American", "bmi": 26.2},
    "BACT-MEN-M03": {"age": 68, "sex": "male", "ethnicity": "East Asian", "bmi": 23.8},
    # NMDAR-ENC
    "NMDAR-ENC-S03": {"age": 19, "sex": "female", "ethnicity": "African American", "bmi": 22.1},
    "NMDAR-ENC-S04": {"age": 27, "sex": "female", "ethnicity": "Hispanic", "bmi": 24.8},
    "NMDAR-ENC-M02": {"age": 33, "sex": "female", "ethnicity": "Caucasian", "bmi": 23.4},
    "NMDAR-ENC-M03": {"age": 25, "sex": "female", "ethnicity": "East Asian", "bmi": 21.8},
    # FND
    "FND-S02": {"age": 34, "sex": "female", "ethnicity": "African American", "bmi": 26.1},
    "FND-S04": {"age": 22, "sex": "male", "ethnicity": "Hispanic", "bmi": 24.8},
    "FND-M02": {"age": 42, "sex": "female", "ethnicity": "South Asian", "bmi": 25.4},
    "FND-M03": {"age": 29, "sex": "male", "ethnicity": "African American", "bmi": 27.1},
    # SYNC-CARD
    "SYNC-CARD-S03": {"age": 66, "sex": "female", "ethnicity": "Hispanic", "bmi": 27.8},
    "SYNC-CARD-S04": {"age": 82, "sex": "male", "ethnicity": "East Asian", "bmi": 23.4},
    "SYNC-CARD-M02": {"age": 55, "sex": "female", "ethnicity": "Caucasian", "bmi": 28.4},
    "SYNC-CARD-M03": {"age": 71, "sex": "male", "ethnicity": "Hispanic", "bmi": 29.2},
    # FEPI-TEMP
    "FEPI-TEMP-S03": {"age": 42, "sex": "male", "ethnicity": "African American", "bmi": 28.1},
    "FEPI-TEMP-S04": {"age": 19, "sex": "female", "ethnicity": "East Asian", "bmi": 20.4},
    "FEPI-TEMP-M03": {"age": 35, "sex": "male", "ethnicity": "Caucasian", "bmi": 26.4},
    # MS-RR
    "MS-RR-S03": {"age": 24, "sex": "female", "ethnicity": "African American", "bmi": 25.1},
    "MS-RR-S04": {"age": 36, "sex": "male", "ethnicity": "Hispanic", "bmi": 27.4},
    "MS-RR-M02": {"age": 28, "sex": "female", "ethnicity": "South Asian", "bmi": 22.1},
    "MS-RR-M03": {"age": 38, "sex": "male", "ethnicity": "African American", "bmi": 26.8},
    "MS-RR-P02": {"age": 31, "sex": "female", "ethnicity": "African American", "bmi": 24.8},
    "MS-RR-P03": {"age": 22, "sex": "male", "ethnicity": "East Asian", "bmi": 23.2},
}

# ---------------------------------------------------------------------------
# Fix 6: Explicit patient‐name assignments
# ---------------------------------------------------------------------------
NAME_OVERRIDES: dict[str, str] = {
    # ALZ-EARLY name dedup (S03/S04 were both "Harold Jenkins")
    "ALZ-EARLY-S03": "Priya Sharma",
    "ALZ-EARLY-S04": "Takeshi Yamamoto",
    # SYNC-CARD M03 rename (M02/M03 both "Raymond Okafor")
    "SYNC-CARD-M03": "Marcus Williams",
}

# ---------------------------------------------------------------------------
# Name pools keyed by (sex, ethnicity)
# ---------------------------------------------------------------------------
_NAME_POOL: dict[tuple[str, str], list[str]] = {
    ("male", "Caucasian"): [
        "James Mitchell", "David Anderson", "Robert Thompson", "Michael Patterson",
        "William Carter", "Thomas Bennett", "Christopher Hayes", "Daniel Foster",
        "Matthew Sullivan", "Andrew Morgan",
    ],
    ("female", "Caucasian"): [
        "Sarah Lindgren", "Jennifer Walsh", "Emily Brennan", "Rebecca Morrison",
        "Katherine Sullivan", "Laura Hensley", "Amanda Pearson", "Rachel Donovan",
        "Megan Fletcher", "Stephanie Harmon",
    ],
    ("male", "African American"): [
        "Marcus Williams", "Darius Jackson", "Terrence Brooks", "Andre Washington",
        "Jerome Harris", "Malcolm Robinson", "Curtis Powell", "Darnell Henderson",
        "Kevin Morris", "Tyrone Coleman",
    ],
    ("female", "African American"): [
        "Dorothy Williams", "Keisha Johnson", "Tamara Brooks", "Shanice Washington",
        "Latoya Harris", "Monique Robinson", "Denise Powell", "Jasmine Henderson",
        "Crystal Morris", "Tiffany Coleman",
    ],
    ("male", "Hispanic"): [
        "Carlos Reyes", "Miguel Santos", "Rafael Gutierrez", "Alejandro Morales",
        "Diego Ramirez", "Fernando Castillo", "Javier Herrera", "Oscar Mendoza",
        "Ricardo Flores", "Ernesto Vargas",
    ],
    ("female", "Hispanic"): [
        "Maria Santos", "Elena Gutierrez", "Sofia Morales", "Isabella Ramirez",
        "Gabriela Castillo", "Carmen Herrera", "Lucia Mendoza", "Rosa Flores",
        "Ana Vargas", "Valentina Cruz",
    ],
    ("male", "South Asian"): [
        "Rajesh Patel", "Vikram Sharma", "Arjun Gupta", "Sunil Reddy",
        "Deepak Malhotra", "Anil Kapoor", "Pradeep Singh", "Sanjay Verma",
        "Ramesh Iyer", "Manoj Kumar",
    ],
    ("female", "South Asian"): [
        "Priya Sharma", "Ananya Patel", "Deepika Gupta", "Sunita Reddy",
        "Kavita Malhotra", "Meera Singh", "Neha Verma", "Pooja Iyer",
        "Ritu Kumar", "Shalini Nair",
    ],
    ("male", "East Asian"): [
        "Takeshi Yamamoto", "Wei Chen", "Hiroshi Tanaka", "Jianjun Liu",
        "Kenji Watanabe", "Sung-Ho Park", "Daichi Sato", "Yong Li",
        "Ryo Nakamura", "Min-Jun Kim",
    ],
    ("female", "East Asian"): [
        "Mei Chen", "Yuki Tanaka", "Soo-Jin Park", "Akiko Watanabe",
        "Ling Liu", "Haruka Sato", "Hye-Won Kim", "Sakura Nakamura",
        "Jing Li", "Miyu Yamamoto",
    ],
    ("male", "Northern European"): [
        "Erik Lindqvist", "Lars Henriksen", "Henrik Johansson", "Nils Andersen",
        "Olaf Bergstrom", "Magnus Dahl", "Sven Eriksson", "Karl Nilsson",
        "Anders Holmberg", "Bjorn Larsson",
    ],
    ("female", "Northern European"): [
        "Sarah Lindgren", "Ingrid Henriksen", "Astrid Johansson", "Freya Andersen",
        "Karin Bergstrom", "Elsa Dahl", "Sigrid Eriksson", "Greta Nilsson",
        "Maja Holmberg", "Linnea Larsson",
    ],
}

# ---------------------------------------------------------------------------
# Allergy pool
# ---------------------------------------------------------------------------
ALLERGY_POOL = [
    "Penicillin (rash)",
    "Sulfonamides (rash)",
    "Cephalosporins (hives)",
    "NSAIDs (GI upset)",
    "Contrast dye (mild reaction)",
    "Latex (contact dermatitis)",
    "Codeine (nausea)",
    "Aspirin (urticaria)",
    "ACE inhibitors (angioedema)",
    "Tetracycline (photosensitivity)",
    "No known drug allergies",
]

# ---------------------------------------------------------------------------
# Occupation pools by age
# ---------------------------------------------------------------------------
OCCUPATION_YOUNG = [
    "software engineer", "nurse", "marketing analyst", "graduate student",
    "graphic designer", "paralegal", "restaurant manager", "physical therapist",
    "data analyst", "veterinary technician",
]
OCCUPATION_MIDDLE = [
    "accountant", "high school principal", "civil engineer", "real estate agent",
    "pharmacist", "IT project manager", "social worker", "dental hygienist",
    "insurance adjuster", "librarian",
]
OCCUPATION_OLD = [
    "retired engineer", "retired nurse", "retired business owner", "retired teacher",
    "retired farmer", "retired mechanic", "retired accountant", "retired librarian",
    "retired electrician", "retired professor",
]


# ===================================================================
# Helpers
# ===================================================================

def _hash_int(s: str) -> int:
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)


def _get_condition(case_id: str) -> str:
    """ISCH-STR-S01 -> ISCH-STR"""
    parts = case_id.rsplit("-", 1)
    return parts[0]


def _parse_range(ref_range: str) -> tuple[float | None, float | None]:
    """Parse a reference range string like '4.0-11.0' or '<200' or '>40' into (lo, hi)."""
    ref = ref_range.strip()
    # "136-145"
    m = re.match(r"([\d.]+)\s*[-–]\s*([\d.]+)", ref)
    if m:
        return float(m.group(1)), float(m.group(2))
    # "<200" or "< 200"
    m = re.match(r"<\s*([\d.]+)", ref)
    if m:
        return None, float(m.group(1))
    # ">40" or "> 40"
    m = re.match(r">\s*([\d.]+)", ref)
    if m:
        return float(m.group(1)), None
    # "0.40-4.50"
    m = re.match(r"([\d.]+)\s*-\s*([\d.]+)", ref)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


def _is_outside_range(value: float, lo: float | None, hi: float | None) -> bool:
    if lo is not None and value < lo:
        return True
    if hi is not None and value > hi:
        return True
    return False


def _smart_round(original_val, new_val: float) -> int | float:
    """Round to the same precision as the original value."""
    if isinstance(original_val, int):
        return int(round(new_val))
    s = str(original_val)
    if "." in s:
        decimals = len(s.split(".")[1])
        return round(new_val, decimals)
    return int(round(new_val))


def _extract_name_from_hpi(hpi: str) -> str | None:
    """Try to extract 'Mr./Mrs./Ms./Dr. Firstname Lastname' from HPI."""
    m = re.search(r"(?:Mr\.|Mrs\.|Ms\.|Miss|Dr\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", hpi)
    if m:
        return m.group(1)
    return None


def _get_name_for_case(case_id: str, sex: str, ethnicity: str, rng: Random) -> str:
    """Get a deterministic name for a case given demographics."""
    if case_id in NAME_OVERRIDES:
        return NAME_OVERRIDES[case_id]

    key = (sex, ethnicity)
    pool = _NAME_POOL.get(key)
    if pool is None:
        # fallback to Caucasian
        pool = _NAME_POOL.get((sex, "Caucasian"), ["Pat Smith"])

    h = _hash_int(f"name-{case_id}")
    return pool[h % len(pool)]


def _get_pronoun_map(old_sex: str, new_sex: str) -> dict[str, str] | None:
    """Return a pronoun mapping if sex changed."""
    if old_sex == new_sex:
        return None
    if new_sex == "male":
        return {
            " she ": " he ", " She ": " He ",
            " her ": " his ", " Her ": " His ",
            " hers ": " his ", " Hers ": " His ",
            " herself ": " himself ", " Herself ": " Himself ",
            "Mrs. ": "Mr. ", "Ms. ": "Mr. ", "Miss ": "Mr. ",
        }
    else:
        return {
            " he ": " she ", " He ": " She ",
            " his ": " her ", " His ": " Her ",
            " himself ": " herself ", " Himself ": " Herself ",
            "Mr. ": "Ms. ",
        }


def _apply_pronoun_swap(text: str, pmap: dict[str, str]) -> str:
    """Apply pronoun replacements. Use word boundary approach."""
    for old, new in pmap.items():
        text = text.replace(old, new)
    return text


def _get_medication_drugs(data: dict) -> set[str]:
    """Get set of drug names from the patient's medication list."""
    drugs = set()
    meds = data.get("patient", {}).get("clinical_history", {}).get("medications", [])
    for m in meds:
        if isinstance(m, dict):
            drugs.add(m.get("drug", "").lower())
    return drugs


def _get_allergy_for_case(case_id: str, condition: str, drugs: set[str], condition_cases: list[str]) -> list[str]:
    """Deterministically assign an allergy. Avoid conflicts with medications."""
    h = _hash_int(f"allergy-{case_id}")
    # Filter out conflicting allergies
    available = list(ALLERGY_POOL)
    drug_lower = {d.lower() for d in drugs}

    # Conflict rules
    if any("aspirin" in d for d in drug_lower):
        available = [a for a in available if "Aspirin" not in a]
    if any("ibuprofen" in d or "naproxen" in d or "nsaid" in d.lower() for d in drug_lower):
        available = [a for a in available if "NSAID" not in a]
    if any("penicillin" in d or "amoxicillin" in d or "ampicillin" in d for d in drug_lower):
        available = [a for a in available if "Penicillin" not in a]
    if any("cephalosporin" in d or "ceftriaxone" in d or "cefepime" in d or "cefazolin" in d for d in drug_lower):
        available = [a for a in available if "Cephalosporin" not in a]
    if any("sulfa" in d or "sulfamethoxazole" in d or "trimethoprim" in d for d in drug_lower):
        available = [a for a in available if "Sulfonamide" not in a]
    if any("lisinopril" in d or "enalapril" in d or "ramipril" in d or "captopril" in d for d in drug_lower):
        available = [a for a in available if "ACE inhibitor" not in a]
    if any("codeine" in d for d in drug_lower):
        available = [a for a in available if "Codeine" not in a]
    if any("tetracycline" in d or "doxycycline" in d or "minocycline" in d for d in drug_lower):
        available = [a for a in available if "Tetracycline" not in a]

    if not available:
        available = ["No known drug allergies"]

    idx = h % len(available)
    return [available[idx]]


def _get_occupation(case_id: str, age: int) -> str:
    """Deterministic occupation from hash."""
    h = _hash_int(f"occupation-{case_id}")
    if age < 40:
        pool = OCCUPATION_YOUNG
    elif age <= 65:
        pool = OCCUPATION_MIDDLE
    else:
        pool = OCCUPATION_OLD
    return pool[h % len(pool)]


# ===================================================================
# Fix functions
# ===================================================================

def fix_alz_icd(data: dict, case_id: str, changes: list[str]) -> None:
    """Fix 1: ALZ-EARLY ICD codes — G30.0 -> G30.1 for all except P01."""
    if not case_id.startswith("ALZ-EARLY"):
        return
    if case_id == "ALZ-EARLY-P01":
        return
    gt = data.get("ground_truth", {})
    if gt.get("icd_code") == "G30.0":
        gt["icd_code"] = "G30.1"
        changes.append("Fix1: ICD G30.0 -> G30.1")


def fix_demographics(data: dict, case_id: str, rng: Random, changes: list[str]) -> None:
    """Fix 2: Demographics diversification + Fix 6: Name changes."""
    if case_id not in DEMO_CHANGES and case_id not in NAME_OVERRIDES:
        return

    dem = data["patient"]["demographics"]
    old_sex = dem["sex"]
    old_ethnicity = dem.get("ethnicity", "")

    # Apply demographic changes
    if case_id in DEMO_CHANGES:
        for field, value in DEMO_CHANGES[case_id].items():
            old_val = dem.get(field)
            if old_val != value:
                dem[field] = value
                changes.append(f"Fix2: demographics.{field}: {old_val} -> {value}")

    new_sex = dem["sex"]
    new_ethnicity = dem.get("ethnicity", "")

    # Handle name changes
    old_name = _extract_name_from_hpi(data["patient"].get("history_present_illness", ""))
    new_name = _get_name_for_case(case_id, new_sex, new_ethnicity, rng)

    if old_name and new_name and old_name != new_name:
        # Replace name in HPI
        hpi = data["patient"].get("history_present_illness", "")
        if old_name in hpi:
            hpi = hpi.replace(old_name, new_name)
            data["patient"]["history_present_illness"] = hpi
            changes.append(f"Fix6: name '{old_name}' -> '{new_name}' in HPI")

    # Handle pronoun changes if sex changed
    if old_sex != new_sex:
        pmap = _get_pronoun_map(old_sex, new_sex)
        if pmap:
            for field in ["history_present_illness", "chief_complaint"]:
                text = data["patient"].get(field, "")
                if text:
                    new_text = _apply_pronoun_swap(text, pmap)
                    if new_text != text:
                        data["patient"][field] = new_text
                        changes.append(f"Fix2: pronoun swap in patient.{field}")

            # Also swap in neurological_exam sub-fields
            neuro = data["patient"].get("neurological_exam", {})
            if isinstance(neuro, dict):
                for key, val in neuro.items():
                    if isinstance(val, str):
                        new_val = _apply_pronoun_swap(val, pmap)
                        if new_val != val:
                            neuro[key] = new_val

    # Fix age references in HPI (e.g., "68-year-old" -> "55-year-old")
    if case_id in DEMO_CHANGES and "age" in DEMO_CHANGES[case_id]:
        old_age = None
        hpi = data["patient"].get("history_present_illness", "")
        # Try to find old age reference
        m = re.search(r"(\d+)-year-old", hpi)
        if m:
            old_age_str = m.group(1)
            new_age = dem["age"]
            hpi = hpi.replace(f"{old_age_str}-year-old", f"{new_age}-year-old")
            data["patient"]["history_present_illness"] = hpi


def fix_name_dedup(data: dict, case_id: str, rng: Random, changes: list[str]) -> None:
    """Fix 6: Additional name dedup for cases without demographic changes."""
    # The SYNC-CARD-M03 case gets renamed even without demo changes struct
    if case_id == "SYNC-CARD-M03" and case_id not in DEMO_CHANGES:
        dem = data["patient"]["demographics"]
        old_name = _extract_name_from_hpi(data["patient"].get("history_present_illness", ""))
        new_name = "Marcus Williams"
        if old_name and old_name != new_name:
            hpi = data["patient"]["history_present_illness"]
            hpi = hpi.replace(old_name, new_name)
            data["patient"]["history_present_illness"] = hpi
            changes.append(f"Fix6: name '{old_name}' -> '{new_name}'")


def _apply_lab_noise(value, rng: Random) -> tuple:
    """Apply ±10% noise to a numeric value. Returns (new_value, was_numeric)."""
    if isinstance(value, (int, float)):
        factor = rng.uniform(0.90, 1.10)
        new_val = value * factor
        return _smart_round(value, new_val), True
    return value, False


def fix_lab_values(data: dict, case_id: str, rng: Random, changes: list[str]) -> None:
    """Fix 3: Lab value diversification with ±10% noise."""
    lab_change_count = 0

    def process_panels(panels: dict) -> int:
        count = 0
        if not isinstance(panels, dict):
            return 0
        for panel_name, tests in panels.items():
            if not isinstance(tests, list):
                continue
            for test_entry in tests:
                if not isinstance(test_entry, dict):
                    continue
                val = test_entry.get("value")
                if not isinstance(val, (int, float)):
                    continue
                new_val, was_numeric = _apply_lab_noise(val, rng)
                if was_numeric and new_val != val:
                    test_entry["value"] = new_val
                    count += 1
                    # Update is_abnormal
                    ref = test_entry.get("reference_range", "")
                    lo, hi = _parse_range(ref)
                    if lo is not None or hi is not None:
                        test_entry["is_abnormal"] = _is_outside_range(new_val, lo, hi)
        return count

    def rebuild_abnormal_summary(lab_output: dict) -> None:
        """Rebuild abnormal_values_summary from panel data."""
        if not isinstance(lab_output, dict):
            return
        panels = lab_output.get("panels", {})
        if not isinstance(panels, dict):
            return
        abnormals = []
        for panel_name, tests in panels.items():
            if not isinstance(tests, list):
                continue
            for t in tests:
                if isinstance(t, dict) and t.get("is_abnormal"):
                    val = t.get("value", "")
                    unit = t.get("unit", "")
                    name = t.get("test", "")
                    sig = t.get("clinical_significance", "")
                    if sig:
                        abnormals.append(f"{name}: {val} {unit} - {sig}".strip())
                    else:
                        ref = t.get("reference_range", "")
                        abnormals.append(f"{name}: {val} {unit} (ref: {ref})".strip())
        lab_output["abnormal_values_summary"] = abnormals

    # Process initial_tool_outputs.labs
    labs = data.get("initial_tool_outputs", {}).get("labs")
    if labs and isinstance(labs, dict):
        panels = labs.get("panels", {})
        lab_change_count += process_panels(panels)
        rebuild_abnormal_summary(labs)

    # Process followup_outputs
    for fo in data.get("followup_outputs", []):
        if not isinstance(fo, dict):
            continue
        output = fo.get("output", {})
        if isinstance(output, dict) and "panels" in output:
            lab_change_count += process_panels(output["panels"])
            rebuild_abnormal_summary(output)

    if lab_change_count > 0:
        changes.append(f"Fix3: noised {lab_change_count} numeric lab values")

    # CSF noise
    csf = data.get("initial_tool_outputs", {}).get("csf")
    if csf and isinstance(csf, dict):
        csf_count = 0
        # Numeric fields in CSF
        for field in ["protein", "glucose"]:
            val_str = csf.get(field, "")
            if isinstance(val_str, str):
                m = re.match(r"([\d.]+)", val_str)
                if m:
                    orig = float(m.group(1))
                    factor = rng.uniform(0.90, 1.10)
                    new_v = round(orig * factor, 1)
                    csf[field] = val_str.replace(m.group(1), str(new_v))
                    csf_count += 1
            elif isinstance(val_str, (int, float)):
                factor = rng.uniform(0.90, 1.10)
                csf[field] = _smart_round(val_str, val_str * factor)
                csf_count += 1

        # Opening pressure
        op = csf.get("opening_pressure", "")
        if isinstance(op, str):
            m = re.match(r"([\d.]+)", op)
            if m:
                orig = float(m.group(1))
                factor = rng.uniform(0.90, 1.10)
                new_v = round(orig * factor, 1)
                # Keep integer if original was int
                if orig == int(orig):
                    new_v = int(round(new_v))
                csf["opening_pressure"] = op.replace(m.group(1), str(new_v))
                csf_count += 1

        # WBC count in cell_count
        cc = csf.get("cell_count", {})
        if isinstance(cc, dict):
            for ck in ["WBC", "RBC"]:
                cv = cc.get(ck, "")
                if isinstance(cv, str):
                    m = re.match(r"([\d.]+)", cv)
                    if m:
                        orig = float(m.group(1))
                        if orig > 0:
                            factor = rng.uniform(0.90, 1.10)
                            new_v = max(0, round(orig * factor))
                            cc[ck] = cv.replace(m.group(1), str(new_v))
                            csf_count += 1

        if csf_count > 0:
            changes.append(f"Fix3: noised {csf_count} CSF values")

    # Also process CSF in followup_outputs
    for fo in data.get("followup_outputs", []):
        if not isinstance(fo, dict):
            continue
        if fo.get("tool_name") == "analyze_csf":
            csf_out = fo.get("output", {})
            if isinstance(csf_out, dict):
                csf_count = 0
                for field in ["protein", "glucose"]:
                    val_str = csf_out.get(field, "")
                    if isinstance(val_str, str):
                        m = re.match(r"([\d.]+)", val_str)
                        if m:
                            orig = float(m.group(1))
                            factor = rng.uniform(0.90, 1.10)
                            new_v = round(orig * factor, 1)
                            csf_out[field] = val_str.replace(m.group(1), str(new_v))
                            csf_count += 1
                op = csf_out.get("opening_pressure", "")
                if isinstance(op, str):
                    m = re.match(r"([\d.]+)", op)
                    if m:
                        orig = float(m.group(1))
                        factor = rng.uniform(0.90, 1.10)
                        new_v = round(orig * factor, 1)
                        if orig == int(orig):
                            new_v = int(round(new_v))
                        csf_out["opening_pressure"] = op.replace(m.group(1), str(new_v))
                        csf_count += 1
                cc = csf_out.get("cell_count", {})
                if isinstance(cc, dict):
                    for ck in ["WBC", "RBC"]:
                        cv = cc.get(ck, "")
                        if isinstance(cv, str):
                            m2 = re.match(r"([\d.]+)", cv)
                            if m2:
                                orig = float(m2.group(1))
                                if orig > 0:
                                    factor = rng.uniform(0.90, 1.10)
                                    new_v = max(0, round(orig * factor))
                                    cc[ck] = cv.replace(m2.group(1), str(new_v))
                                    csf_count += 1
                if csf_count > 0:
                    changes.append(f"Fix3: noised {csf_count} followup CSF values")


def fix_allergies(data: dict, case_id: str, changes: list[str]) -> None:
    """Fix 4: Allergy diversification."""
    condition = _get_condition(case_id)
    drugs = _get_medication_drugs(data)

    hist = data.get("patient", {}).get("clinical_history", {})
    # Get all case IDs for this condition (not used directly, just for tracking)
    old_allergies = hist.get("allergies", [])
    new_allergies = _get_allergy_for_case(case_id, condition, drugs, [])

    if old_allergies != new_allergies:
        hist["allergies"] = new_allergies
        changes.append(f"Fix4: allergies {old_allergies} -> {new_allergies}")


def fix_occupation(data: dict, case_id: str, changes: list[str]) -> None:
    """Fix 5: Occupation diversification."""
    age = data["patient"]["demographics"]["age"]
    new_occ = _get_occupation(case_id, age)

    social = data.get("patient", {}).get("clinical_history", {}).get("social_history", {})
    if not isinstance(social, dict):
        return

    old_occ = social.get("occupation", "")
    if old_occ != new_occ:
        social["occupation"] = new_occ
        changes.append(f"Fix5: occupation -> '{new_occ}'")


def fix_msrr_references(data: dict, case_id: str, changes: list[str]) -> None:
    """Fix 7: MS-RR reference range standardization."""
    if not case_id.startswith("MS-RR"):
        return

    ref_fixes = {
        "Myelin basic protein": "<4.0 ng/mL",
        "IgG index": "<0.70",
    }
    # VEP P100 latency references -> "<115 ms"
    p100_ref = "<115 ms"

    fix_count = 0

    def fix_in_output(output: dict) -> int:
        count = 0
        if not isinstance(output, dict):
            return 0

        # Fix in special_tests (CSF)
        special = output.get("special_tests", {})
        if isinstance(special, dict):
            for test_name, target_ref in ref_fixes.items():
                if test_name in special:
                    val_str = special[test_name]
                    if isinstance(val_str, str):
                        # Try to find and replace the reference part
                        # Format: "value (context; reference: <old_ref)"
                        # We need to find the reference portion
                        # Patterns that capture the full reference string including optional units
                        for old_pattern in [
                            r"reference:\s*<[\d.]+\s*(?:ng/mL|ng/ml)?",
                            r"normal\s*<[\d.]+\s*(?:ng/mL|ng/ml)?",
                            r"reference\s*<[\d.]+\s*(?:ng/mL|ng/ml)?",
                            r"normal\s*<[\d.]+\s*(?:ng/mL|ng/ml)?",
                        ]:
                            m = re.search(old_pattern, val_str, re.IGNORECASE)
                            if m:
                                new_ref_str = f"reference: {target_ref}"
                                new_val = val_str[:m.start()] + new_ref_str + val_str[m.end():]
                                if new_val != val_str:
                                    special[test_name] = new_val
                                    count += 1
                                break

        # Fix in panels (lab results with VEP data)
        panels = output.get("panels", {})
        if isinstance(panels, dict):
            for panel_name, tests in panels.items():
                if not isinstance(tests, list):
                    continue
                for test_entry in tests:
                    if not isinstance(test_entry, dict):
                        continue
                    test_name = test_entry.get("test", "")
                    ref = test_entry.get("reference_range", "")

                    # Fix P100 latency references
                    if "p100 latency" in test_name.lower():
                        if ref != p100_ref and "<" in ref and "ms" in ref.lower():
                            test_entry["reference_range"] = p100_ref
                            count += 1
                            # Re-check is_abnormal
                            val_str = test_entry.get("value", "")
                            if isinstance(val_str, str):
                                vm = re.match(r"([\d.]+)", val_str)
                                if vm:
                                    val_num = float(vm.group(1))
                                    test_entry["is_abnormal"] = val_num >= 115

                    # Fix Myelin basic protein reference
                    if "myelin basic protein" in test_name.lower():
                        target = "<4.0 ng/mL"
                        if ref != target:
                            test_entry["reference_range"] = target
                            count += 1
                            # Re-check is_abnormal
                            val_str = test_entry.get("value", "")
                            if isinstance(val_str, str):
                                vm = re.match(r"([\d.]+)", val_str)
                                if vm:
                                    val_num = float(vm.group(1))
                                    test_entry["is_abnormal"] = val_num >= 4.0

                    # Fix IgG index reference
                    if "igg index" in test_name.lower():
                        target = "<0.70"
                        if ref != target:
                            test_entry["reference_range"] = target
                            count += 1

        # Also fix in abnormal_values_summary strings
        summary = output.get("abnormal_values_summary", [])
        if isinstance(summary, list):
            for i, s in enumerate(summary):
                if isinstance(s, str) and "P100 latency" in s:
                    s = re.sub(r"reference\s*<\s*\d+\s*ms", "reference <115 ms", s)
                    s = re.sub(r"normal\s*<\s*\d+\s*ms", "normal <115 ms", s)
                    summary[i] = s

        return count

    # Process initial_tool_outputs
    for tool_key in ["labs", "csf"]:
        tool_out = data.get("initial_tool_outputs", {}).get(tool_key)
        if tool_out:
            fix_count += fix_in_output(tool_out)

    # Process followup_outputs
    for fo in data.get("followup_outputs", []):
        if isinstance(fo, dict):
            output = fo.get("output", {})
            if isinstance(output, dict):
                fix_count += fix_in_output(output)

    if fix_count > 0:
        changes.append(f"Fix7: standardized {fix_count} MS-RR reference ranges")


def fix_vitals(data: dict, case_id: str, rng: Random, changes: list[str]) -> None:
    """Fix 8: Vitals diversification with ±5-10% noise."""
    vitals = data.get("patient", {}).get("vitals", {})
    if not isinstance(vitals, dict):
        return

    count = 0
    for key in ["bp_systolic", "bp_diastolic", "hr", "temp", "rr", "spo2"]:
        val = vitals.get(key)
        if val is None:
            continue

        if key == "temp":
            # ±0.2°C
            offset = rng.uniform(-0.2, 0.2)
            new_val = round(val + offset, 1)
            # Ensure plausible: 35.5 - 39.5
            new_val = max(35.5, min(39.5, new_val))
        elif key == "rr":
            # ±2
            offset = rng.randint(-2, 2)
            new_val = val + offset
            new_val = max(10, min(30, new_val))
        elif key == "spo2":
            # Keep 95-100
            offset = rng.randint(-2, 2)
            new_val = val + offset
            new_val = max(95, min(100, new_val))
        else:
            # ±5-10% for BP and HR
            pct = rng.uniform(0.92, 1.08)
            new_val = val * pct
            if key == "bp_systolic":
                new_val = max(85, min(220, int(round(new_val))))
            elif key == "bp_diastolic":
                new_val = max(50, min(130, int(round(new_val))))
            elif key == "hr":
                new_val = max(45, min(160, int(round(new_val))))

        if isinstance(val, float) or key == "temp":
            new_val = round(float(new_val), 1)
        else:
            new_val = int(round(new_val))

        if new_val != val:
            vitals[key] = new_val
            count += 1

    # Ensure diastolic < systolic
    if vitals.get("bp_diastolic", 0) >= vitals.get("bp_systolic", 999):
        vitals["bp_diastolic"] = vitals["bp_systolic"] - 20

    if count > 0:
        changes.append(f"Fix8: noised {count} vital signs")


def fix_metadata(data: dict, case_id: str, changes: list[str]) -> None:
    """Fix 9: Metadata standardization."""
    meta = data.get("metadata", {})
    if not isinstance(meta, dict):
        data["metadata"] = {"created_by": "neurobench_generator"}
        changes.append("Fix9: created metadata with created_by")
        return

    # Standardize field: remove "generated_by", "author"; set "created_by"
    changed = False
    for old_key in ["generated_by", "author"]:
        if old_key in meta:
            del meta[old_key]
            changed = True

    if meta.get("created_by") != "neurobench_generator":
        meta["created_by"] = "neurobench_generator"
        changed = True

    if changed:
        changes.append("Fix9: metadata.created_by = 'neurobench_generator'")


# ===================================================================
# Main
# ===================================================================

def main() -> None:
    if not CASES_DIR.exists():
        print(f"ERROR: Cases directory not found: {CASES_DIR}")
        sys.exit(1)

    case_files = sorted(CASES_DIR.glob("*.json"))
    print(f"Found {len(case_files)} case files in {CASES_DIR}")

    # Back up
    if not BACKUP_DIR.exists():
        print(f"Creating backup at {BACKUP_DIR}")
        shutil.copytree(CASES_DIR, BACKUP_DIR)
    else:
        print(f"Backup already exists at {BACKUP_DIR}, skipping backup")

    total_changes = 0
    files_modified = 0

    for case_file in case_files:
        case_id = case_file.stem
        if case_id in SKIP_IDS:
            print(f"  SKIP {case_id} (in skip list)")
            continue

        # Each case gets its own seeded RNG for idempotency
        rng = Random(42 + _hash_int(case_id) % (2**31))

        # Always load from backup (original) to ensure idempotency
        backup_file = BACKUP_DIR / case_file.name
        source_file = backup_file if backup_file.exists() else case_file
        with open(source_file, "r") as f:
            data = json.load(f)

        changes: list[str] = []

        # Apply all fixes in order
        fix_alz_icd(data, case_id, changes)
        fix_demographics(data, case_id, rng, changes)
        fix_name_dedup(data, case_id, rng, changes)
        fix_lab_values(data, case_id, rng, changes)
        fix_allergies(data, case_id, changes)
        fix_occupation(data, case_id, changes)
        fix_msrr_references(data, case_id, changes)
        fix_vitals(data, case_id, rng, changes)
        fix_metadata(data, case_id, changes)

        if changes:
            with open(case_file, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")  # trailing newline
            files_modified += 1
            total_changes += len(changes)
            print(f"  {case_id}: {len(changes)} changes")
            for c in changes:
                print(f"    - {c}")
        else:
            print(f"  {case_id}: no changes needed")

    print(f"\n{'='*60}")
    print(f"Summary: {files_modified}/{len(case_files)} files modified, {total_changes} total changes")
    print(f"Backup at: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
