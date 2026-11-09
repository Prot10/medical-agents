"""Map what MIMIC clinicians ordered for the NeuroBench conditions onto the NeuroBench tool vocabulary.

Reads the per-condition order counts of ``mimic_order_catalogue.py`` (names and counts only) and
routes every radiology exam, provider order and microbiology test to a tool call through the
RULES table below. Each rule says how the item is served:

- ``core``    a term of the NeuroBench catalogue (costs.yaml ``tools``);
- ``pack``    a term of the ``general_medicine`` pack only;
- ``approx``  served by the nearest existing term, worth a dedicated term later;
- ``missing`` a diagnostic study with no term at all;
- ``nondx``   not a diagnostic order (treatment, nursing, billing modifier, procedure step).

Labs are routed by fluid and category: the item-to-panel table is a separate job.

Prints, per source, the share of (admission, item) pairs in each class, the most frequent
missing and approximate items, and the share of cohort admissions that used each tool. Counts
only (PhysioNet DUA).

    uv run --no-project --python 3.12 --with duckdb --with pandas python -I mimic_tool_map.py orders.csv
"""

from __future__ import annotations

import re
import sys

import duckdb
import pandas as pd

# (source, regex on the item, tool, term, class). First match wins.
RULES: list[tuple[str, str, str, str, str]] = [
    # --- radiology: billing modifiers, procedure steps and admin lines are not orders
    ("radiology", (r"^-\d\d|^-X|^___$|MOD SEDATION|3D RENDERING|OUTSIDE FILMS|PRE-SURGICAL|SEL CATH|PLACE CATH|ADD'L|"
                   r"EMBO|TRANS ?CATH|THROMBECT|F/U TRANS|FLUORO GUID|US GUID|LINE PLAC|LINE/TUBE|TUBE PLAC|G TUBE|"
                   r"NASO-INTESTINAL|PARACENTESIS|STEREOTAXIS|MR SCREENING|TRANS CATH INFUS|NON-TUNNELED|PICC|PERPHERAL"),
     "-", "-", "nondx"),
    ("radiology", r"LUMBAR SPINAL PUNCTURE", "analyze_csf", "lumbar_puncture", "core"),
    ("radiology", r"MR FUNCTIONAL BRAIN", "order_advanced_imaging", "functional_MRI", "core"),
    ("radiology", r"^(L-SPINE|T-SPINE|C-SPINE|LUMBO-SACRAL)", "order_body_imaging", "spine_xray", "missing"),
    ("radiology", r"THYROID U\.?S", "order_body_imaging", "neck_ultrasound", "pack"),
    ("radiology", r"^CTA ABD", "order_body_imaging", "pelvis_abdomen_CT", "approx"),
    ("radiology", r"EXT CAROTID", "order_advanced_imaging", "cerebral_angiography", "core"),
    ("radiology", r"LUMBAR PUNCTURE", "analyze_csf", "lumbar_puncture", "core"),
    ("radiology", r"PERFUSION", "order_advanced_imaging", "CT_perfusion", "core"),
    ("radiology", r"^CTA (HEAD|NECK)|STROKE CTA|CTA HEAD AND", "order_ct_scan", "angiography", "core"),
    ("radiology", r"HEAD CT|^CT HEAD|CODE STROKE ONLY CT|^CT BRAIN", "order_ct_scan", "head", "core"),
    ("radiology", r"^MRA (BRAIN|HEAD|NECK)", "order_advanced_imaging", "MR_angiography", "core"),
    ("radiology", r"^MRV HEAD", "order_advanced_imaging", "MR_venography", "core"),
    ("radiology", r"^MR HEAD|STROKE PROTOCOL \(BRAIN|^MR BRAIN|^MRI BRAIN", "analyze_brain_mri", "brain", "core"),
    ("radiology", r"^MR .*(SPINE|C-SPINE|T-SPINE|L-SPINE)|^MR [CTL][ -]SPINE", "order_body_imaging", "spine_MRI", "core"),
    ("radiology", r"^CT .*SPINE", "order_body_imaging", "spine_CT", "core"),
    ("radiology", r"^CHEST \(|^CHEST PORT\b|CHEST \(SINGLE", "order_body_imaging", "chest_xray", "core"),
    ("radiology", r"^CTA CHEST", "order_body_imaging", "chest_CTA", "core"),
    ("radiology", r"^CT CHEST", "order_body_imaging", "chest_CT", "core"),
    ("radiology", r"^CT (ABD|PELVIS)", "order_body_imaging", "pelvis_abdomen_CT", "core"),
    ("radiology", r"^MR(I)? (ABD|PELVIS)|^MRV PELVIS|MRCP", "order_body_imaging", "pelvis_abdomen_MRI", "core"),
    ("radiology", r"LIVER OR GALLBLADDER US", "order_body_imaging", "hepatobiliary_ultrasound", "pack"),
    ("radiology", r"^US ABD|ABDOMEN U\.?S|PELVIS U\.?S|^PELVIS, NON-OB", "order_body_imaging", "pelvis_abdomen_ultrasound", "core"),
    ("radiology", r"RENAL U\.?S", "order_body_imaging", "renal_ultrasound", "pack"),
    ("radiology", r"PORTABLE ABDOMEN|^ABDOMEN \(", "order_body_imaging", "abdomen_xray", "pack"),
    ("radiology", r"LOWER EXT VEINS|VEN DUP", "order_body_imaging", "lower_extremity_venous_duplex", "core"),
    ("radiology", r"UP EXT VEINS", "order_body_imaging", "upper_extremity_venous_duplex", "missing"),
    ("radiology", r"CAROTID SERIES|CAROTID/CERVICAL", "order_advanced_imaging", "carotid_duplex", "core"),
    ("radiology", r"CAROTID/CEREBRAL|A-GRAM|ANGIO", "order_advanced_imaging", "cerebral_angiography", "core"),
    ("radiology", r"DUPLEX DOP+ ABD", "order_body_imaging", "abdominal_doppler", "missing"),
    ("radiology", r"VIDEO OROPHARYNGEAL SWALLOW", "order_specialized_test", "speech_language_evaluation", "approx"),
    ("radiology", r"KNEE|ANKLE|WRIST|HAND|FOOT|SHOULDER|HIP|ELBOW|FEMUR|TIB|HUMERUS|^PELVIS \(", "order_body_imaging",
     "extremity_xray", "pack"),
    ("radiology", r"CT SINUS|MAXILLOFACIAL|CT ORBIT|CT TEMPORAL", "order_ct_scan", "face_or_orbits", "approx"),
    ("radiology", r"^CT NECK|SOFT TISSUE NECK", "order_ct_scan", "neck_soft_tissue", "approx"),
    ("radiology", r"NUC|PET|SPECT|BONE SCAN|V/Q|VQ", "order_advanced_imaging", "nuclear", "approx"),
    ("radiology", r"ECHO", "order_echocardiogram", "TTE", "core"),
    # --- provider orders: only the diagnostic ones get a tool; radiology and labs have their own tables
    ("poe", r"^(Radiology|Lab|Blood Bank / Blood tests)\b", "-", "-", "dup"),
    ("poe", r"Cardiology / Echo", "order_echocardiogram", "TTE", "core"),
    ("poe", r"Cardiology / ECG", "analyze_ecg", "-", "core"),
    ("poe", r"Neurology / EEG", "analyze_eeg", "-", "core"),
    ("poe", r"Neurology / TCD", "order_advanced_imaging", "transcranial_doppler", "core"),
    ("poe", r"Neurology / EMG", "order_specialized_test", "emg_ncs", "core"),
    ("poe", r"Cardiology / Holter", "order_cardiac_monitoring", "holter_24h", "core"),
    ("poe", r"General Care / Telemetry", "order_cardiac_monitoring", "telemetry", "core"),
    ("poe", r"Cardiology / ETT", "order_specialized_test", "exercise_stress_test", "core"),
    ("poe", r"Consults / Speech", "order_specialized_test", "speech_language_evaluation", "approx"),
    ("poe", r"Consults / (Neurology|Cardiology|Infectious|Psychiatry|Hematology|Medicine|Acute Care Surgery)",
     "consult", "-", "missing"),
    ("poe", r".", "-", "-", "nondx"),
    # --- microbiology
    ("micro", r"MRSA SCREEN|VANCOMYCIN RESISTANT", "-", "-", "nondx"),
    ("micro", r"^CSF", "analyze_csf", "culture/special tests", "core"),
    ("micro", r"^BLOOD CULTURE|Blood Culture", "order_microbiology", "blood_culture", "core"),
    ("micro", r"^URINE", "order_microbiology", "urine", "core"),
    ("micro", r"^SPUTUM", "order_microbiology", "sputum", "core"),
    ("micro", r"^STOOL", "order_microbiology", "stool", "core"),
    ("micro", r"BRONCHOALVEOLAR|Mini-BAL", "order_microbiology", "bronchoalveolar_lavage", "pack"),
    ("micro", r"RAPID PLASMA REAGIN|TREPONEM", "interpret_labs", "RPR", "core"),
    ("micro", r"SEROLOGY/BLOOD \| CRYPTOCOCCAL", "interpret_labs", "serum_cryptococcal_antigen", "core"),
    ("micro", r"\(Toxo\)", "interpret_labs", "toxoplasma_IgG", "core"),
    ("micro", r"HCV VIRAL LOAD", "interpret_labs", "hepatitis_C_antibody", "approx"),
    ("micro", r"LYME", "interpret_labs", "Lyme_serology", "core"),
    ("micro", r"\(EBV\)|\(CMV|VARICELLA|HSV|HEPATITIS|HIV", "interpret_labs", "viral_serology", "approx"),
    ("micro", r"^SWAB|WOUND|CATHETER TIP|TISSUE", "order_microbiology", "wound_swab", "core"),
    ("micro", r"PERITONEAL|ASCIT", "order_microbiology", "ascitic_fluid", "core"),
    ("micro", r"PLEURAL", "order_microbiology", "pleural_fluid", "pack"),
    ("micro", r"JOINT|SYNOVIAL", "order_microbiology", "synovial_fluid", "pack"),
    ("micro", r"Respiratory Viral|Influenza|SARS|COVID", "order_microbiology", "nasopharyngeal_swab", "pack"),
    ("micro", r"Legionella", "order_microbiology", "urine", "approx"),
    ("micro", r"FLUID RECEIVED IN BLOOD CULTURE", "order_microbiology", "blood_culture", "approx"),
]


def route(source: str, item: str) -> tuple[str, str, str]:
    if source == "lab":
        _, fluid, cat = (item.split(" | ") + ["", ""])[:3]
        if fluid == "Cerebrospinal Fluid":
            return "analyze_csf", "labs", "core"
        if fluid == "Blood" and cat == "Blood Gas":
            return "interpret_labs", "ABG", "core"
        if fluid in ("Blood", "Urine"):
            return "interpret_labs", f"{fluid.lower()} panels", "core"
        if fluid in ("Pleural", "Joint Fluid"):
            return "order_microbiology", f"{fluid.lower()} studies", "pack"
        if fluid == "Ascites":
            return "order_microbiology", "ascitic_fluid", "core"
        return "interpret_labs", f"{fluid.lower()} studies", "approx"
    for src, rx, tool, term, cls in RULES:
        if src == source and re.search(rx, item, re.IGNORECASE):
            return tool, term, cls
    return "?", "?", "unmatched"


def main() -> None:
    df = duckdb.sql(f"select * from read_csv_auto('{sys.argv[1]}')").df()
    df[["tool", "term", "cls"]] = [route(s, i) for s, i in zip(df.source, df.item)]
    df = df[df.cls != "dup"]
    cohort = df.groupby("condition").condition_admissions.first().sum()
    pd.set_option("display.width", 200)
    print(f"cohort admissions: {cohort:,}\n")
    print("Share of (admission, item) pairs by class, per source:")
    tab = df.groupby(["source", "cls"]).admissions.sum().unstack(fill_value=0)
    print((100 * tab.div(tab.sum(axis=1), axis=0)).round(1).to_string(), "\n")
    for cls in ("missing", "approx", "unmatched", "pack"):
        top = df[df.cls == cls].groupby(["source", "item", "tool", "term"]).admissions.sum().sort_values(ascending=False)
        print(f"Top {cls} items (admissions):")
        print(top.head(15).to_string() if len(top) else "  none", "\n")
    dx = df[df.cls.isin(["core", "pack", "approx", "missing"])]
    use = dx.groupby(["tool", "condition"]).admissions.max().unstack(fill_value=0)
    share = (100 * use / df.groupby("condition").condition_admissions.first()).round(0)
    print("Upper bound of admissions using each tool, % per condition (max over the tool's items):")
    print(share.T.to_string())


if __name__ == "__main__":
    main()
