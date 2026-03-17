"""Create NeuroBench v3 dataset with realistic (non-leaky) tool outputs.

Processes BOTH v1 (100 synthetic cases) and v2 (100 real-case-seeded cases)
into v3, stripping interpretive fields that give away the diagnosis and
leaving only raw descriptive data for the agent to reason over.

v3 output: 200 cases total (v1 originals + v2 originals, all stripped).

Usage:
    uv run python agent-platform/scripts/create_v3_dataset.py
    uv run python agent-platform/scripts/create_v3_dataset.py --v1-only
    uv run python agent-platform/scripts/create_v3_dataset.py --v2-only
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
V1_DIR = PROJECT_ROOT / "data" / "neurobench_v1"
V2_DIR = PROJECT_ROOT / "data" / "neurobench_v2"
V3_DIR = PROJECT_ROOT / "data" / "neurobench_v3"
V3_CASES = V3_DIR / "cases"

# ---------------------------------------------------------------------------
# Regex patterns for impression stripping
# ---------------------------------------------------------------------------
DIAGNOSIS_PATTERNS = [
    r'(?:consistent|compatible) with\b',
    r'\bsuggestive of\b',
    r'\bcharacteristic of\b',
    r'\bdiagnostic of\b',
    r'\bpathognomonic\b',
    r'\bindicative of\b',
    r'\bhighly suspicious for\b',
    r'\bmost likely\b',
    r'\bargues against\b',
    r'\brules out\b',
    r'\bexcludes\b',
    r'\bconfirms?\b',
    r'\bsupports?\s+(a |the )?diagnosis\b',
    r'\bthis (pattern|finding|profile)\b',
    r'\boverall findings\b',
]
TREATMENT_PATTERNS = [
    r'\bthrombolysis\b', r'\bthrombectomy\b', r'\bimmunotherapy\b',
    r'\bchemotherapy\b', r'\bresection\b', r'\bbiopsy\b',
    r'\banticoagulat\b', r'\bantibiotic\b', r'\bacyclovir\b',
    r'\bconsider\b', r'\brecommend(?:ed|ation)?\b',
    r'\bconsult\b', r'\breferr?al\b',
]
DISEASE_NAMES = [
    r'\bstroke\b', r'\binfarct(?:ion)?\b', r'\bglioblastoma\b', r'\bglioma\b',
    r'\blymphoma\b', r'\bmeningitis\b', r'\bencephalitis\b',
    r'\bepilepsy\b', r'\bseizure disorder\b', r'\bPNES\b',
    r'\bParkinson\b', r'\bDLB\b', r'\bLewy body\b', r'\bPSP\b', r'\bMSA\b',
    r'\bAlzheimer\b', r'\bdementia\b', r'\bFTD\b', r'\bPPA\b',
    r'\bmultiple sclerosis\b', r'\bMS\b', r'\bFND\b', r'\bfunctional\b',
    r'\bBrugada\b', r'\bARVC\b', r'\bHCM\b', r'\bmoyamoya\b',
    r'\bendocarditis\b', r'\btuberculosis\b', r'\bTB\b', r'\bcryptococc\b',
    r'\bNMDAR\b', r'\bLGI1\b', r'\bautoimmune\b',
]

_ALL_REMOVE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in
                        DIAGNOSIS_PATTERNS + TREATMENT_PATTERNS]

_DISEASE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in DISEASE_NAMES]

_STARTS_WITH_PATTERNS = [
    re.compile(r'^\s*this (pattern|finding)\b', re.IGNORECASE),
    re.compile(r'^\s*these findings\b', re.IGNORECASE),
    re.compile(r'^\s*overall findings\b', re.IGNORECASE),
]

# ---------------------------------------------------------------------------
# Counters
# ---------------------------------------------------------------------------
class Stats:
    def __init__(self):
        self.files = 0
        self.lab_clinical_significance = 0
        self.lab_interpretation = 0
        self.lab_abnormal_summary = 0
        self.mri_differential = 0
        self.mri_recommended = 0
        self.mri_confidence = 0
        self.mri_impression = 0
        self.mri_additional_obs = 0
        self.eeg_impression = 0
        self.eeg_recommended = 0
        self.eeg_confidence = 0
        self.eeg_finding_correlation = 0
        self.ecg_correlation = 0
        self.ecg_interpretation = 0
        self.csf_interpretation = 0

stats = Stats()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def split_sentences(text: str) -> list[str]:
    """Split text into sentences. Handles numbered lists and period-space."""
    # First, split on numbered list items like "1. ... 2. ... 3. ..."
    # Match pattern: number followed by period and space at start or after sentence boundary
    numbered = re.split(r'(?:^|\s+)(\d+)\.\s+', text)
    # Re-assemble numbered items: numbered[0] is before first number,
    # then alternating number, content pairs
    items = []
    if numbered[0].strip():
        items.append(numbered[0].strip())
    for i in range(1, len(numbered) - 1, 2):
        content = numbered[i + 1].strip() if i + 1 < len(numbered) else ""
        if content:
            items.append(content)

    if not items:
        items = [text]

    # Further split each item on sentence boundaries
    sentences = []
    for item in items:
        sub = re.split(r'(?<=[.!?])\s+(?=[A-Z])', item)
        sentences.extend(sub)
    return [s.strip() for s in sentences if s.strip()]


def should_remove_sentence(sentence: str) -> bool:
    """Check if a sentence should be removed from impressions."""
    for pat in _ALL_REMOVE_PATTERNS:
        if pat.search(sentence):
            return True
    for pat in _STARTS_WITH_PATTERNS:
        if pat.search(sentence):
            return True
    return False


def strip_impression(text: str) -> str:
    """Strip diagnosis names and treatment recs from an impression string."""
    if not text:
        return text
    sentences = split_sentences(text)
    kept = []
    for s in sentences:
        if should_remove_sentence(s):
            continue
        kept.append(s)
    # Re-join
    result = " ".join(kept).strip()
    # Clean up any dangling numbered list prefixes like "1. 2." or standalone numbers
    result = re.sub(r'(?:^|\s)\d+\.\s*(?=\d+\.|$)', ' ', result).strip()
    result = re.sub(r'^\d+\.\s*', '', result).strip()
    # Ensure ends with "Clinical correlation recommended."
    if not result or len(result) < 20:
        result = "See findings above. Clinical correlation recommended."
    elif "Clinical correlation recommended" not in result:
        if not result.endswith("."):
            result += "."
        result += " Clinical correlation recommended."
    return result


def strip_eeg_impression(text: str) -> str:
    """Strip disease names from EEG impressions while keeping EEG descriptions."""
    if not text:
        return text
    sentences = split_sentences(text)
    kept = []
    for s in sentences:
        if should_remove_sentence(s):
            continue
        # Also remove sentences with disease names for EEG
        if any(pat.search(s) for pat in _DISEASE_PATTERNS):
            continue
        kept.append(s)
    result = " ".join(kept).strip()
    if not result or len(result) < 20:
        result = "See findings above. Clinical correlation recommended."
    elif "Clinical correlation recommended" not in result:
        if not result.endswith("."):
            result += "."
        result += " Clinical correlation recommended."
    return result


def strip_ecg_interpretation(text: str) -> str:
    """Keep terse machine-interpretation style, remove disease/management commentary."""
    if not text:
        return text
    sentences = split_sentences(text)
    kept = []
    for s in sentences:
        # Remove sentences about stroke mechanism, disease etiology, management
        if should_remove_sentence(s):
            continue
        if any(pat.search(s) for pat in _DISEASE_PATTERNS):
            continue
        kept.append(s)
    result = " ".join(kept).strip()
    if not result or len(result) < 10:
        result = "See report details above."
    return result


def strip_additional_observations(obs_list: list) -> list:
    """Remove entries containing disease names or diagnostic conclusions."""
    if not obs_list:
        return obs_list
    kept = []
    remove_patterns = [
        re.compile(r'\bKey finding:', re.IGNORECASE),
        re.compile(r'\bargues against\b', re.IGNORECASE),
        re.compile(r'\bconsistent with\b', re.IGNORECASE),
        re.compile(r'\bcharacteristic of\b', re.IGNORECASE),
    ]
    for entry in obs_list:
        if not isinstance(entry, str):
            kept.append(entry)
            continue
        skip = False
        for pat in remove_patterns:
            if pat.search(entry):
                skip = True
                break
        if not skip:
            # Also check disease names
            for pat in _DISEASE_PATTERNS:
                if pat.search(entry):
                    skip = True
                    break
        if not skip:
            kept.append(entry)
    return kept


def build_terse_lab_interpretation(panels: dict) -> str:
    """Build terse interpretation listing only abnormal values."""
    abnormals = []
    for panel_name, tests in panels.items():
        if not isinstance(tests, list):
            continue
        for t in tests:
            if not isinstance(t, dict):
                continue
            if t.get("is_abnormal"):
                val = t.get("value", "")
                unit = t.get("unit", "")
                test_name = t.get("test", "")
                ref = t.get("reference_range", "")
                # Determine H or L
                flag = ""
                if ref and val != "" and not isinstance(val, str):
                    try:
                        numeric_val = float(val)
                        # Try to parse reference range
                        ref_match = re.match(r'[<>]?\s*([\d.]+)\s*[-–]\s*([\d.]+)', str(ref))
                        if ref_match:
                            low = float(ref_match.group(1))
                            high = float(ref_match.group(2))
                            if numeric_val > high:
                                flag = "H"
                            elif numeric_val < low:
                                flag = "L"
                            else:
                                flag = "H"  # is_abnormal but in range - default to H
                        elif str(ref).startswith("<"):
                            flag = "H"
                        elif str(ref).startswith(">"):
                            flag = "L"
                        else:
                            flag = "H"
                    except (ValueError, TypeError):
                        flag = "H"
                else:
                    flag = "H"  # Non-numeric abnormal values

                if flag:
                    abnormals.append(f"{test_name} {val} {unit} ({flag})")
                else:
                    abnormals.append(f"{test_name} {val} {unit}")

    if not abnormals:
        return "All values within normal limits."
    return "Abnormal values: " + ", ".join(abnormals) + "."


def build_terse_abnormal_summary(entry: str) -> str:
    """Strip prose from abnormal_values_summary entry, keep just test: value unit (H/L)."""
    if not isinstance(entry, str):
        return entry
    # Try to parse "Test: Value unit - <prose>" or "Test: Value unit (<prose>)"
    # Format: "{test}: {value} {unit} ({H or L})"
    # Original format is like: "WBC: 18.0 x10^9/L - Marked leukocytosis suggesting..."
    # or: "Sodium: 153 mEq/L (ref: 136-145)"

    # Split on " - " to remove prose after dash
    parts = entry.split(" - ", 1)
    base = parts[0].strip()

    # Also handle "(ref: ...)" style
    base = re.sub(r'\s*\(ref:.*?\)', '', base)

    # Now try to determine H/L from the original text
    # Parse "Test: Value Unit" pattern
    m = re.match(r'^(.+?):\s*(.+?)\s+([\w^/%.]+(?:\s+\w+)?)\s*$', base)
    if not m:
        # Fallback: try simpler parse
        m = re.match(r'^(.+?):\s*(.+)$', base)
        if m:
            test_name = m.group(1).strip()
            rest = m.group(2).strip()
            # Determine H/L from prose
            flag = "H"
            lower = entry.lower()
            if "low" in lower or "decreased" in lower or "reduced" in lower:
                flag = "L"
            elif "elevated" in lower or "high" in lower or "increased" in lower:
                flag = "H"
            return f"{test_name}: {rest} ({flag})"
        return base  # Can't parse, return as is

    test_name = m.group(1).strip()
    value = m.group(2).strip()
    unit = m.group(3).strip()

    # Determine H/L from prose in original entry
    flag = "H"
    lower = entry.lower()
    if "low" in lower or "decreased" in lower or "reduced" in lower or "hypo" in lower:
        flag = "L"
    elif "elevated" in lower or "high" in lower or "increased" in lower or "hyper" in lower or "marked" in lower:
        flag = "H"

    return f"{test_name}: {value} {unit} ({flag})"


def build_terse_csf_interpretation(csf: dict) -> str:
    """Build terse CSF interpretation with just numbers."""
    parts = []
    if csf.get("opening_pressure"):
        # Extract just the number
        op = csf["opening_pressure"]
        op_num = re.match(r'([\d.]+\s*\w+)', str(op))
        parts.append(f"Opening pressure: {op_num.group(1) if op_num else op}")

    cc = csf.get("cell_count", {})
    if cc:
        wbc = cc.get("WBC", "N/A")
        neut = cc.get("Neutrophils", "N/A")
        lymph = cc.get("Lymphocytes", "N/A")
        parts.append(f"WBC: {wbc} ({neut} PMN/{lymph} lymph)")

    if csf.get("protein"):
        parts.append(f"Protein: {csf['protein']}")

    if csf.get("glucose"):
        gl = csf["glucose"]
        ratio = csf.get("glucose_ratio", "")
        if ratio:
            parts.append(f"Glucose: {gl} (ratio {ratio})")
        else:
            parts.append(f"Glucose: {gl}")

    # Special tests
    special = csf.get("special_tests", {})
    if special:
        for test_name, test_val in special.items():
            if test_val and "pending" not in str(test_val).lower():
                # Extract just the result
                parts.append(f"{test_name}: {test_val}")

    if not parts:
        return "No CSF data available."
    return ". ".join(parts) + "."


# ---------------------------------------------------------------------------
# Transform functions
# ---------------------------------------------------------------------------

def transform_labs(labs: dict) -> None:
    """Transform lab results in-place."""
    if not labs or not isinstance(labs, dict):
        return

    panels = labs.get("panels")
    if panels and isinstance(panels, dict):
        for panel_name, tests in panels.items():
            if not isinstance(tests, list):
                continue
            for t in tests:
                if isinstance(t, dict) and "clinical_significance" in t:
                    if t["clinical_significance"] is not None:
                        stats.lab_clinical_significance += 1
                    t["clinical_significance"] = None

    # Interpretation -> terse
    if "interpretation" in labs:
        if panels and isinstance(panels, dict):
            labs["interpretation"] = build_terse_lab_interpretation(panels)
        else:
            labs["interpretation"] = "All values within normal limits."
        stats.lab_interpretation += 1

    # Abnormal values summary -> stripped
    if "abnormal_values_summary" in labs and labs["abnormal_values_summary"]:
        summary = labs["abnormal_values_summary"]
        if isinstance(summary, list):
            labs["abnormal_values_summary"] = [
                build_terse_abnormal_summary(e) for e in summary
            ]
            stats.lab_abnormal_summary += 1


def transform_mri(mri: dict) -> None:
    """Transform MRI report in-place."""
    if not mri or not isinstance(mri, dict):
        return

    # D: differential_by_imaging -> []
    if "differential_by_imaging" in mri:
        if mri["differential_by_imaging"]:
            stats.mri_differential += 1
        mri["differential_by_imaging"] = []

    # E: recommended_actions -> generic
    if "recommended_actions" in mri:
        if mri["recommended_actions"] != ["Clinical correlation recommended."]:
            stats.mri_recommended += 1
        mri["recommended_actions"] = ["Clinical correlation recommended."]

    # F: confidence -> 0.0
    if "confidence" in mri:
        if mri["confidence"] != 0.0:
            stats.mri_confidence += 1
        mri["confidence"] = 0.0

    # G: impression -> strip diagnosis names
    if "impression" in mri and mri["impression"]:
        original = mri["impression"]
        mri["impression"] = strip_impression(original)
        if mri["impression"] != original:
            stats.mri_impression += 1

    # H: additional_observations -> strip editorialized
    if "additional_observations" in mri and mri["additional_observations"]:
        original_len = len(mri["additional_observations"])
        mri["additional_observations"] = strip_additional_observations(
            mri["additional_observations"]
        )
        if len(mri["additional_observations"]) != original_len:
            stats.mri_additional_obs += 1


def transform_eeg(eeg: dict) -> None:
    """Transform EEG report in-place."""
    if not eeg or not isinstance(eeg, dict):
        return

    # I: impression -> strip disease names
    if "impression" in eeg and eeg["impression"]:
        original = eeg["impression"]
        eeg["impression"] = strip_eeg_impression(original)
        if eeg["impression"] != original:
            stats.eeg_impression += 1

    # J: recommended_actions -> generic
    if "recommended_actions" in eeg:
        if eeg["recommended_actions"] != ["Clinical correlation recommended."]:
            stats.eeg_recommended += 1
        eeg["recommended_actions"] = ["Clinical correlation recommended."]

    # K: confidence -> 0.0
    if "confidence" in eeg:
        if eeg["confidence"] != 0.0:
            stats.eeg_confidence += 1
        eeg["confidence"] = 0.0

    # L: EEGFinding.clinical_correlation -> ""
    if "findings" in eeg and isinstance(eeg["findings"], list):
        for finding in eeg["findings"]:
            if isinstance(finding, dict) and "clinical_correlation" in finding:
                if finding["clinical_correlation"] != "":
                    stats.eeg_finding_correlation += 1
                finding["clinical_correlation"] = ""


def transform_ecg(ecg: dict) -> None:
    """Transform ECG report in-place."""
    if not ecg or not isinstance(ecg, dict):
        return

    # M: clinical_correlation -> ""
    if "clinical_correlation" in ecg:
        if ecg["clinical_correlation"] != "":
            stats.ecg_correlation += 1
        ecg["clinical_correlation"] = ""

    # N: interpretation -> strip
    if "interpretation" in ecg and ecg["interpretation"]:
        original = ecg["interpretation"]
        ecg["interpretation"] = strip_ecg_interpretation(original)
        if ecg["interpretation"] != original:
            stats.ecg_interpretation += 1


def transform_csf(csf: dict) -> None:
    """Transform CSF results in-place."""
    if not csf or not isinstance(csf, dict):
        return

    # O: interpretation -> terse
    if "interpretation" in csf:
        csf["interpretation"] = build_terse_csf_interpretation(csf)
        stats.csf_interpretation += 1


def transform_tool_output(tool_name: str, output: dict) -> None:
    """Dispatch to the right transform based on tool name."""
    if not output or not isinstance(output, dict):
        return

    if tool_name in ("analyze_brain_mri",):
        transform_mri(output)
    elif tool_name in ("analyze_eeg",):
        transform_eeg(output)
    elif tool_name in ("analyze_ecg",):
        transform_ecg(output)
    elif tool_name in ("analyze_csf",):
        transform_csf(output)
    elif tool_name in ("interpret_labs",):
        # interpret_labs could be lab-like or other data; check for panels key
        if "panels" in output:
            transform_labs(output)
        # If it also has CSF-like fields, transform those too
        if "opening_pressure" in output or "cell_count" in output:
            transform_csf(output)
    elif tool_name in ("search_literature",):
        pass  # Leave as-is
    elif tool_name in ("check_drug_interactions",):
        pass  # Leave as-is


def transform_initial_outputs(initial: dict) -> None:
    """Transform all initial_tool_outputs in-place."""
    if not initial or not isinstance(initial, dict):
        return

    if initial.get("mri"):
        transform_mri(initial["mri"])
    if initial.get("eeg"):
        transform_eeg(initial["eeg"])
    if initial.get("ecg"):
        transform_ecg(initial["ecg"])
    if initial.get("labs"):
        transform_labs(initial["labs"])
    if initial.get("csf"):
        transform_csf(initial["csf"])
    # literature_search and drug_interactions left as-is


def transform_followup_outputs(followups: list) -> None:
    """Transform all followup outputs in-place."""
    if not followups or not isinstance(followups, list):
        return

    for fu in followups:
        if not isinstance(fu, dict):
            continue
        tool_name = fu.get("tool_name", "")
        output = fu.get("output")
        if output and isinstance(output, dict):
            transform_tool_output(tool_name, output)


# ---------------------------------------------------------------------------
# Impression examples for verification
# ---------------------------------------------------------------------------
impression_examples: list[tuple[str, str, str]] = []  # (case_id, before, after)


def collect_impression_example(case_id: str, field: str, before: str, after: str):
    """Collect up to 3 impression before/after examples."""
    if len(impression_examples) < 3 and before != after:
        impression_examples.append((f"{case_id} ({field})", before, after))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_source(source_dir: Path, label: str) -> int:
    """Process all cases from a source directory into v3. Returns count."""
    cases_dir = source_dir / "cases"
    if not cases_dir.exists():
        print(f"  [SKIP] {cases_dir} does not exist")
        return 0

    case_files = sorted(cases_dir.glob("*.json"))
    print(f"\n  Processing {len(case_files)} {label} case files...")

    count = 0
    for case_path in case_files:
        with open(case_path, "r") as f:
            case = json.load(f)

        case_id = case.get("case_id", case_path.stem)

        # Collect impression examples BEFORE transformation
        initial = case.get("initial_tool_outputs", {})
        mri_before = None
        eeg_before = None
        if initial and isinstance(initial, dict):
            if initial.get("mri") and initial["mri"].get("impression"):
                mri_before = initial["mri"]["impression"]
            if initial.get("eeg") and initial["eeg"].get("impression"):
                eeg_before = initial["eeg"]["impression"]

        # Transform
        transform_initial_outputs(case.get("initial_tool_outputs"))
        transform_followup_outputs(case.get("followup_outputs"))

        # Collect after examples
        if mri_before is not None:
            mri_after = case.get("initial_tool_outputs", {}).get("mri", {}).get("impression", "")
            collect_impression_example(case_id, "MRI impression", mri_before, mri_after)
        if eeg_before is not None:
            eeg_after = case.get("initial_tool_outputs", {}).get("eeg", {}).get("impression", "")
            collect_impression_example(case_id, "EEG impression", eeg_before, eeg_after)

        # Write output
        out_path = V3_CASES / case_path.name
        with open(out_path, "w") as f:
            json.dump(case, f, indent=2, ensure_ascii=False)
            f.write("\n")

        count += 1
        stats.files += 1

    return count


def main():
    # Parse args
    v1_only = "--v1-only" in sys.argv
    v2_only = "--v2-only" in sys.argv

    # Create output directory
    V3_CASES.mkdir(parents=True, exist_ok=True)

    # Copy metadata from v1 (splits, etc.)
    if not v2_only:
        for item in V1_DIR.iterdir():
            if item.name == "cases":
                continue
            dest = V3_DIR / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                print(f"Copied directory: {item.name}/ (from v1)")
            elif item.is_file():
                shutil.copy2(item, dest)
                print(f"Copied file: {item.name} (from v1)")

    # Process v1 cases
    v1_count = 0
    if not v2_only:
        print("\n" + "=" * 50)
        print("PROCESSING V1 (synthetic cases)")
        print("=" * 50)
        v1_count = process_source(V1_DIR, "v1")

    # Process v2 cases
    v2_count = 0
    if not v1_only:
        print("\n" + "=" * 50)
        print("PROCESSING V2 (real-case-seeded)")
        print("=" * 50)
        v2_count = process_source(V2_DIR, "v2")

    print(f"\n  Total: {v1_count} v1 + {v2_count} v2 = {v1_count + v2_count} cases in v3")

    # -----------------------------------------------------------------------
    # Verification
    # -----------------------------------------------------------------------
    print("=" * 70)
    print("VERIFICATION")
    print("=" * 70)

    # Check all files are valid JSON
    v3_files = sorted(V3_CASES.glob("*.json"))
    valid = 0
    for fp in v3_files:
        try:
            with open(fp) as f:
                json.load(f)
            valid += 1
        except json.JSONDecodeError as e:
            print(f"  INVALID JSON: {fp.name}: {e}")
    print(f"\nValid JSON files: {valid}/{len(v3_files)}")

    # Check no non-null clinical_significance in labs
    non_null_cs = 0
    non_empty_diff = 0
    non_zero_mri_conf = 0
    non_zero_eeg_conf = 0
    for fp in v3_files:
        with open(fp) as f:
            case = json.load(f)
        # Check initial
        initial = case.get("initial_tool_outputs", {}) or {}
        for tool_key in ["labs", "mri", "eeg", "ecg", "csf"]:
            tool_data = initial.get(tool_key)
            if not tool_data:
                continue
            if tool_key == "labs" and "panels" in tool_data:
                for pname, tests in tool_data["panels"].items():
                    if isinstance(tests, list):
                        for t in tests:
                            if isinstance(t, dict) and t.get("clinical_significance") is not None:
                                non_null_cs += 1
            if tool_key == "mri":
                if tool_data.get("differential_by_imaging"):
                    non_empty_diff += 1
                if tool_data.get("confidence", 0) != 0.0:
                    non_zero_mri_conf += 1
            if tool_key == "eeg":
                if tool_data.get("confidence", 0) != 0.0:
                    non_zero_eeg_conf += 1

        # Check followups
        for fu in case.get("followup_outputs", []) or []:
            output = fu.get("output", {})
            if not isinstance(output, dict):
                continue
            if "panels" in output:
                for pname, tests in output["panels"].items():
                    if isinstance(tests, list):
                        for t in tests:
                            if isinstance(t, dict) and t.get("clinical_significance") is not None:
                                non_null_cs += 1
            if fu.get("tool_name") == "analyze_brain_mri":
                if output.get("differential_by_imaging"):
                    non_empty_diff += 1
                if output.get("confidence", 0) != 0.0:
                    non_zero_mri_conf += 1
            if fu.get("tool_name") == "analyze_eeg":
                if output.get("confidence", 0) != 0.0:
                    non_zero_eeg_conf += 1

    print(f"Non-null clinical_significance in labs: {non_null_cs} (should be 0)")
    print(f"Non-empty differential_by_imaging: {non_empty_diff} (should be 0)")
    print(f"Non-zero MRI confidence: {non_zero_mri_conf} (should be 0)")
    print(f"Non-zero EEG confidence: {non_zero_eeg_conf} (should be 0)")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Files processed:                    {stats.files}")
    print(f"Lab clinical_significance nulled:   {stats.lab_clinical_significance}")
    print(f"Lab interpretations rewritten:      {stats.lab_interpretation}")
    print(f"Lab abnormal summaries stripped:     {stats.lab_abnormal_summary}")
    print(f"MRI differentials cleared:          {stats.mri_differential}")
    print(f"MRI recommended_actions replaced:   {stats.mri_recommended}")
    print(f"MRI confidences zeroed:             {stats.mri_confidence}")
    print(f"MRI impressions stripped:           {stats.mri_impression}")
    print(f"MRI additional_obs filtered:        {stats.mri_additional_obs}")
    print(f"EEG impressions stripped:           {stats.eeg_impression}")
    print(f"EEG recommended_actions replaced:   {stats.eeg_recommended}")
    print(f"EEG confidences zeroed:             {stats.eeg_confidence}")
    print(f"EEG finding correlations cleared:   {stats.eeg_finding_correlation}")
    print(f"ECG correlations cleared:           {stats.ecg_correlation}")
    print(f"ECG interpretations stripped:       {stats.ecg_interpretation}")
    print(f"CSF interpretations rewritten:      {stats.csf_interpretation}")

    # -----------------------------------------------------------------------
    # Impression examples
    # -----------------------------------------------------------------------
    if impression_examples:
        print("\n" + "=" * 70)
        print("IMPRESSION TRANSFORMATION EXAMPLES")
        print("=" * 70)
        for case_label, before, after in impression_examples:
            print(f"\n--- {case_label} ---")
            print(f"BEFORE: {before[:300]}{'...' if len(before) > 300 else ''}")
            print(f"AFTER:  {after[:300]}{'...' if len(after) > 300 else ''}")

    print(f"\nDone. Output written to {V3_DIR}")


if __name__ == "__main__":
    main()
