"""Add a fallback (off-pathway) tool-output tier to every NeuroBench case.

Motivation
----------
A case ships pre-computed outputs only for the tools on its diagnostic
pathway (median ~4 initial + ~6 follow-up). If the agent calls any other
of the 12 tools, the MockServer used to return a hard error -- which
breaks the simulation and tells the agent the harness simply did not
pre-generate that test.

This script fills a second tier, ``fallback_tool_outputs``: for every
tool NOT on a case's pathway it writes a clinically coherent result so
the simulation stays realistic. Outcomes follow a three-way taxonomy
grounded in the over-testing literature:

  * non-contributory NORMAL  -- a properly structured normal report
  * INCIDENTAL finding       -- abnormal but not the diagnosis; an
                                age/comorbidity-appropriate finding
                                (chronic small-vessel change, a benign
                                cyst, trace valvular regurgitation, a
                                benign EEG variant, ...). A self-inflicted
                                red herring the agent must dismiss.

Determinism: the normal-vs-incidental draw is seeded per
(case_id, tool) so a case behaves identically across runs -- a benchmark
must be a stable ruler.

Tier-1 completeness backstop: a tool is given a fallback only when it is
absent from BOTH initial_tool_outputs and followup_outputs. For a few
conditions a tool that is off-pathway would still genuinely reveal the
diagnosis (e.g. CT shows ventriculomegaly in NPH, MRI shows blood in
subarachnoid haemorrhage). DIAGNOSTIC_TOOLS_BY_CONDITION lists those
(condition, tool) pairs; they are left null rather than given a normal
fallback, so the harness errors honestly instead of returning a false
negative. Degenerative incidental findings are age-gated.

Run from repo root:
    uv run python agent-platform/scripts/add_fallback_outputs.py
    uv run python agent-platform/scripts/add_fallback_outputs.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CASES_DIR = REPO / "data" / "neurobench_v5" / "cases"

# ToolOutputSet field -> canonical tool name the agent calls.
FIELD_TO_TOOL = {
    "eeg": "analyze_eeg",
    "mri": "analyze_brain_mri",
    "ecg": "analyze_ecg",
    "labs": "interpret_labs",
    "csf": "analyze_csf",
    "ct": "order_ct_scan",
    "echo": "order_echocardiogram",
    "cardiac_monitoring": "order_cardiac_monitoring",
    "advanced_imaging": "order_advanced_imaging",
    "specialized_test": "order_specialized_test",
    "literature_search": "search_medical_literature",
    "drug_interactions": "check_drug_interactions",
}

# Per-modality probability of an incidental finding rather than a clean
# normal. Calibrated to the imaging-incidentaloma literature (~15-30% for
# imaging, lower for invasive / less incidental-prone modalities).
INCIDENTAL_PROB = {
    "mri": 0.22,
    "ct": 0.22,
    "echo": 0.20,
    "advanced_imaging": 0.18,
    "ecg": 0.15,
    "cardiac_monitoring": 0.15,
    "labs": 0.15,
    "specialized_test": 0.12,
    "eeg": 0.06,
    "csf": 0.05,
}

# Tools that would genuinely reveal the diagnosis for a given condition.
# If such a tool is off-pathway it must NOT receive a normal fallback --
# a clean result would be a false negative. It is left null so the harness
# errors honestly. This is a Tier-1-completeness backstop.
DIAGNOSTIC_TOOLS_BY_CONDITION = {
    "subarachnoid_hemorrhage": {"ct", "mri", "csf"},
    "nph": {"ct", "mri"},
    "brain_tumor_glioma": {"ct", "mri"},
    "ischemic_stroke": {"mri"},
    "bacterial_meningitis": {"csf"},
    "multiple_sclerosis": {"mri"},
    "autoimmune_encephalitis_nmdar": {"csf"},
    "status_epilepticus": {"eeg"},
}

# Age below which degenerative / atherosclerotic incidental findings are
# clinically implausible and should not be emitted.
DEGENERATIVE_MIN_AGE = 60


# ---------------------------------------------------------------------------
# Per-tool fallback generators. Each returns (output_dict, kind).
# ---------------------------------------------------------------------------

def fb_eeg(rng: random.Random, age: int, sex: str):
    normal_bg = {
        "pdr": "9-10 Hz posterior dominant rhythm, symmetric and reactive",
        "sleep_features": "normal vertex waves and sleep spindles",
        "overall": "normal organisation for age",
    }
    if rng.random() < INCIDENTAL_PROB["eeg"]:
        variant = rng.choice([
            "Wicket spikes in the temporal regions, a benign normal variant "
            "with no epileptogenic significance.",
            "Rhythmic midtemporal theta of drowsiness, a benign normal "
            "variant of no clinical significance.",
            "Small sharp spikes of sleep, a benign normal variant.",
        ])
        return ({
            "classification": "normal",
            "background": normal_bg,
            "findings": [],
            "artifacts": [],
            "activating_procedures": {},
            "impression": f"Normal awake and drowsy EEG. {variant}",
            "limitations": "",
            "recommended_actions": [],
        }, "incidental")
    return ({
        "classification": "normal",
        "background": normal_bg,
        "findings": [],
        "artifacts": [],
        "activating_procedures": {},
        "impression": ("Normal awake and drowsy EEG. No epileptiform "
                       "discharges and no focal slowing."),
        "limitations": "",
        "recommended_actions": [],
    }, "normal")


def fb_mri(rng: random.Random, age: int, sex: str):
    if rng.random() < INCIDENTAL_PROB["mri"]:
        opts = []
        if age >= 55:
            opts.append((
                [{"type": "white_matter_lesion",
                  "location": "periventricular and subcortical white matter",
                  "size": "punctate to small",
                  "signal_characteristics": {"T2": "hyperintense", "FLAIR": "hyperintense"},
                  "mass_effect": "none", "borders": "ill-defined"}],
                [],
                "Scattered chronic small-vessel ischaemic change, "
                "age-appropriate. No acute intracranial abnormality.",
            ))
        opts.append((
            [{"type": "cyst", "location": "pineal gland", "size": "4 mm",
              "signal_characteristics": {"T1": "hypointense", "T2": "hyperintense"},
              "mass_effect": "none", "borders": "well-defined"}],
            [],
            "Small benign pineal cyst, an incidental finding of no clinical "
            "significance. No acute intracranial abnormality.",
        ))
        opts.append((
            [],
            ["Incidental mild mucosal thickening of the maxillary sinuses."],
            "No acute intracranial abnormality. Incidental paranasal sinus "
            "mucosal thickening.",
        ))
        findings, obs, impression = rng.choice(opts)
        return ({
            "findings": findings,
            "volumetrics": None,
            "additional_observations": obs,
            "impression": impression,
            "differential_by_imaging": [],
            "recommended_actions": [],
        }, "incidental")
    return ({
        "findings": [],
        "volumetrics": None,
        "additional_observations": [],
        "impression": ("No acute intracranial abnormality. No mass, "
                       "haemorrhage, midline shift, or restricted diffusion. "
                       "Ventricles and sulci appropriate for age."),
        "differential_by_imaging": [],
        "recommended_actions": [],
    }, "normal")


def fb_ecg(rng: random.Random, age: int, sex: str):
    rate = rng.randint(58, 88)
    intervals = {"PR": f"{rng.randint(140, 196)} ms",
                 "QRS": f"{rng.randint(82, 100)} ms",
                 "QTc": f"{rng.randint(400, 440)} ms"}
    if rng.random() < INCIDENTAL_PROB["ecg"]:
        finding = rng.choice([
            "Occasional premature atrial complexes, a benign finding.",
            "Borderline left-axis deviation, non-specific.",
            "Incomplete right bundle branch block, a common benign variant.",
            "Sinus bradycardia, likely physiological.",
        ])
        return ({
            "rhythm": "normal sinus rhythm",
            "rate": rate,
            "intervals": intervals,
            "axis": "normal",
            "findings": [f"Normal sinus rhythm. {finding} "
                         "No acute ST-T changes."],
            "interpretation": "Largely normal ECG with a benign incidental finding",
            "clinical_correlation": "",
        }, "incidental")
    return ({
        "rhythm": "normal sinus rhythm",
        "rate": rate,
        "intervals": intervals,
        "axis": "normal",
        "findings": ["Normal sinus rhythm. Normal axis and intervals. "
                     "No acute ST-T changes."],
        "interpretation": "Normal ECG",
        "clinical_correlation": "",
    }, "normal")


def fb_labs(rng: random.Random, age: int, sex: str):
    if rng.random() < INCIDENTAL_PROB["labs"]:
        choice = rng.choice([
            {"test": "25-OH vitamin D", "value": float(rng.randint(16, 28)),
             "unit": "ng/mL", "reference_range": "30-100", "is_abnormal": True,
             "clinical_significance": "mild vitamin D insufficiency; common and non-specific"},
            {"test": "ALT", "value": float(rng.randint(57, 72)),
             "unit": "U/L", "reference_range": "7-56", "is_abnormal": True,
             "clinical_significance": "trivial transaminase elevation; non-specific"},
            {"test": "Fasting glucose", "value": float(rng.randint(101, 109)),
             "unit": "mg/dL", "reference_range": "70-99", "is_abnormal": True,
             "clinical_significance": "borderline impaired fasting glucose"},
        ])
        return ({
            "panels": {"chemistry": [choice]},
            "interpretation": ("Complete blood count and metabolic panel "
                               "otherwise within normal limits; the single "
                               "borderline value is non-specific."),
            "abnormal_values_summary": [
                f"{choice['test']} {choice['value']} {choice['unit']} "
                f"(ref {choice['reference_range']})"],
        }, "incidental")
    return ({
        "panels": {},
        "interpretation": ("Complete blood count, comprehensive metabolic "
                           "panel, and inflammatory markers within normal "
                           "limits."),
        "abnormal_values_summary": [],
    }, "normal")


def fb_csf(rng: random.Random, age: int, sex: str):
    if rng.random() < INCIDENTAL_PROB["csf"]:
        return ({
            "appearance": "clear and colourless",
            "opening_pressure": "17 cm H2O",
            "cell_count": {"wbc": "3 /uL", "rbc": "0 /uL"},
            "protein": "55 mg/dL",
            "glucose": "61 mg/dL",
            "glucose_ratio": "0.6",
            "special_tests": {},
            "interpretation": ("Mildly elevated CSF protein, a non-specific "
                               "finding. Cell count and glucose normal."),
        }, "incidental")
    return ({
        "appearance": "clear and colourless",
        "opening_pressure": "16 cm H2O",
        "cell_count": {"wbc": "2 /uL", "rbc": "0 /uL"},
        "protein": "38 mg/dL",
        "glucose": "62 mg/dL",
        "glucose_ratio": "0.6",
        "special_tests": {},
        "interpretation": ("Unremarkable CSF. Normal cell count, protein, "
                           "and glucose."),
    }, "normal")


def fb_ct(rng: random.Random, age: int, sex: str):
    if rng.random() < INCIDENTAL_PROB["ct"]:
        opts = []
        if age >= 55:
            opts.append((
                [], ["Age-related involutional change."],
                "No acute intracranial abnormality. Age-related cerebral "
                "involutional change.")
            )
        opts.append((
            [{"type": "calcification", "location": "right frontal lobe",
              "size": "3 mm", "density": "hyperdense",
              "description": "calcified focus consistent with an old, "
                             "benign granuloma"}],
            [],
            "No acute intracranial abnormality. Incidental calcified "
            "granuloma, benign.")
        )
        findings, obs, impression = rng.choice(opts)
        return ({
            "findings": findings,
            "contrast_used": False,
            "angiography_findings": None,
            "additional_observations": obs,
            "impression": impression,
            "recommended_actions": [],
        }, "incidental")
    return ({
        "findings": [],
        "contrast_used": False,
        "angiography_findings": None,
        "additional_observations": [],
        "impression": ("No acute intracranial abnormality. No haemorrhage, "
                       "mass, hydrocephalus, or large-territory infarct."),
        "recommended_actions": [],
    }, "normal")


def fb_echo(rng: random.Random, age: int, sex: str):
    ef = float(rng.randint(58, 66))
    chambers = {"LV": "normal size and systolic function",
                "RV": "normal size and function",
                "LA": "normal size", "RA": "normal size"}
    normal_valves = {"mitral": "structurally normal", "aortic": "structurally normal",
                     "tricuspid": "normal", "pulmonic": "normal"}
    if rng.random() < INCIDENTAL_PROB["echo"]:
        # Trace MR is physiological at any age; aortic sclerosis and
        # diastolic dysfunction are degenerative and age-gated.
        pool = [("Trace mitral regurgitation, physiological.", normal_valves)]
        if age >= DEGENERATIVE_MIN_AGE:
            pool.append(("Mild aortic valve sclerosis without stenosis.",
                         {**normal_valves, "aortic": "mild sclerosis"}))
            pool.append(("Grade I (mild) diastolic dysfunction, age-appropriate.",
                         normal_valves))
        finding, valves = rng.choice(pool)
        return ({
            "chambers": chambers,
            "valves": valves,
            "ejection_fraction": ef,
            "wall_motion": "no regional wall-motion abnormality",
            "findings": [f"{finding} No intracardiac thrombus or vegetation. "
                         "No pericardial effusion."],
            "impression": ("Structurally near-normal heart with a benign "
                           "incidental finding."),
            "recommended_actions": [],
        }, "incidental")
    return ({
        "chambers": chambers,
        "valves": normal_valves,
        "ejection_fraction": ef,
        "wall_motion": "no regional wall-motion abnormality",
        "findings": ["Structurally normal heart. No intracardiac thrombus "
                     "or vegetation. No pericardial effusion."],
        "impression": "Normal transthoracic echocardiogram.",
        "recommended_actions": [],
    }, "normal")


def fb_cardiac_monitoring(rng: random.Random, age: int, sex: str):
    hr = {"min": rng.randint(48, 56), "max": rng.randint(110, 132),
          "average": rng.randint(68, 82)}
    if rng.random() < INCIDENTAL_PROB["cardiac_monitoring"]:
        finding = rng.choice([
            "Rare isolated premature ventricular complexes (under 1% burden), benign.",
            "Brief runs of asymptomatic sinus tachycardia.",
            "Occasional premature atrial complexes, benign.",
        ])
        return ({
            "duration_hours": 24,
            "monitor_type": "holter_24h",
            "rhythm_summary": "Predominant sinus rhythm throughout the recording",
            "heart_rate_range": hr,
            "events": [],
            "findings": [f"{finding} No sustained arrhythmia, no pauses "
                         "greater than 2 seconds, no AV block."],
            "impression": "24-hour Holter monitor with only benign findings.",
            "recommended_actions": [],
        }, "incidental")
    return ({
        "duration_hours": 24,
        "monitor_type": "holter_24h",
        "rhythm_summary": "Sinus rhythm throughout the recording",
        "heart_rate_range": hr,
        "events": [],
        "findings": ["No sustained arrhythmia. No pauses greater than "
                     "2 seconds. No AV block."],
        "impression": "Normal 24-hour Holter monitor.",
        "recommended_actions": [],
    }, "normal")


def fb_advanced_imaging(rng: random.Random, age: int, sex: str):
    # The only incidental here (atherosclerotic plaque) is degenerative,
    # so it is age-gated; younger patients always get a clean normal.
    if age >= DEGENERATIVE_MIN_AGE and rng.random() < INCIDENTAL_PROB["advanced_imaging"]:
        return ({
            "modality": "",
            "tracer_or_protocol": None,
            "findings": [{"region": "extracranial carotid arteries",
                          "signal": "minimal plaque",
                          "interpretation": "minimal atherosclerotic plaque "
                                            "without haemodynamically "
                                            "significant stenosis"}],
            "quantitative_data": None,
            "impression": ("Minor incidental atherosclerotic change; "
                           "no abnormality relevant to the presentation."),
            "recommended_actions": [],
        }, "incidental")
    return ({
        "modality": "",
        "tracer_or_protocol": None,
        "findings": [],
        "quantitative_data": None,
        "impression": ("No abnormality identified on advanced imaging. "
                       "Findings are non-contributory; clinical correlation "
                       "recommended."),
        "recommended_actions": [],
    }, "normal")


def fb_specialized_test(rng: random.Random, age: int, sex: str):
    if rng.random() < INCIDENTAL_PROB["specialized_test"]:
        return ({
            "test_type": "",
            "findings": [{"finding": "minor non-specific abnormality",
                          "interpretation": "of uncertain and likely no "
                                            "clinical significance"}],
            "quantitative_data": None,
            "impression": ("Study with only a minor non-specific finding; "
                           "non-contributory to the presentation."),
            "recommended_actions": [],
        }, "incidental")
    return ({
        "test_type": "",
        "findings": [],
        "quantitative_data": None,
        "impression": ("Study within normal limits. No abnormality "
                       "identified; non-contributory."),
        "recommended_actions": [],
    }, "normal")


def fb_literature_search(rng: random.Random, age: int, sex: str):
    return ({"general": {
        "query": "general",
        "results": [],
        "summary": ("No directly applicable, high-quality evidence was "
                    "retrieved for this query. Recommend correlating with "
                    "current society guidelines."),
    }}, "normal")


def fb_drug_interactions(rng: random.Random, age: int, sex: str):
    return ({"general": {
        "proposed": "(agent not specified on this case's pathway)",
        "interactions": [],
        "contraindications": [],
        "warnings": ["Non-specific interaction check; verify against a "
                     "current formulary or interaction reference before "
                     "prescribing."],
        "formulary_status": "on formulary",
        "alternatives": [],
    }}, "normal")


GENERATORS = {
    "eeg": fb_eeg,
    "mri": fb_mri,
    "ecg": fb_ecg,
    "labs": fb_labs,
    "csf": fb_csf,
    "ct": fb_ct,
    "echo": fb_echo,
    "cardiac_monitoring": fb_cardiac_monitoring,
    "advanced_imaging": fb_advanced_imaging,
    "specialized_test": fb_specialized_test,
    "literature_search": fb_literature_search,
    "drug_interactions": fb_drug_interactions,
}


def covered_tools(case: dict) -> set[str]:
    """Tool fields already on this case's diagnostic pathway."""
    covered: set[str] = set()
    initial = case.get("initial_tool_outputs") or {}
    for field in FIELD_TO_TOOL:
        if initial.get(field) is not None:
            covered.add(field)
    followup_tools = {fu.get("tool_name") for fu in case.get("followup_outputs") or []}
    for field, tool in FIELD_TO_TOOL.items():
        if tool in followup_tools:
            covered.add(field)
    return covered


def build_fallback(case: dict) -> tuple[dict, dict]:
    """Return (fallback_tool_outputs dict, {field: kind} map)."""
    case_id = case["case_id"]
    condition = case.get("condition", "")
    demo = (case.get("patient") or {}).get("demographics") or {}
    age = int(demo.get("age") or 50)
    sex = str(demo.get("sex") or "unknown")

    covered = covered_tools(case)
    diagnostic = DIAGNOSTIC_TOOLS_BY_CONDITION.get(condition, set())
    fallback = {field: None for field in FIELD_TO_TOOL}
    kinds: dict[str, str] = {}

    for field in FIELD_TO_TOOL:
        if field in covered:
            continue
        if field in diagnostic:
            # Off-pathway but genuinely diagnostic for this disease:
            # a normal fallback would be a false negative. Leave null.
            continue
        rng = random.Random(f"{case_id}::{field}")
        output, kind = GENERATORS[field](rng, age, sex)
        fallback[field] = output
        kinds[field] = kind

    return fallback, kinds


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="Report stats without writing files.")
    ap.add_argument("--cases-dir", type=Path, default=CASES_DIR)
    args = ap.parse_args()

    files = sorted(args.cases_dir.glob("*.json"))
    if not files:
        raise SystemExit(f"No case files found in {args.cases_dir}")

    field_counts: Counter = Counter()
    kind_counts: Counter = Counter()
    n_fallbacks = 0

    for path in files:
        case = json.loads(path.read_text())
        fallback, kinds = build_fallback(case)

        for field, kind in kinds.items():
            field_counts[field] += 1
            kind_counts[kind] += 1
            n_fallbacks += 1

        if not args.dry_run:
            # Rebuild dict so fallback_tool_outputs sits next to followup_outputs.
            rebuilt: dict = {}
            for key, value in case.items():
                if key in ("fallback_tool_outputs",):
                    continue
                rebuilt[key] = value
                if key == "followup_outputs":
                    rebuilt["fallback_tool_outputs"] = fallback
            if "fallback_tool_outputs" not in rebuilt:
                rebuilt["fallback_tool_outputs"] = fallback

            meta = rebuilt.setdefault("metadata", {})
            meta["fallback_tool_kinds"] = kinds

            path.write_text(json.dumps(rebuilt, indent=2, ensure_ascii=False) + "\n")

    print(f"cases processed:        {len(files)}")
    print(f"fallback outputs added: {n_fallbacks} "
          f"(avg {n_fallbacks / len(files):.1f} per case)")
    print(f"  normal:     {kind_counts['normal']}")
    print(f"  incidental: {kind_counts['incidental']}")
    print("per-tool fallback coverage (cases needing a fallback for that tool):")
    for field in FIELD_TO_TOOL:
        print(f"  {field:<20} {field_counts[field]}")
    if args.dry_run:
        print("\n[dry run] no files written")
    else:
        print(f"\nwrote fallback_tool_outputs into {len(files)} case files")


if __name__ == "__main__":
    main()
