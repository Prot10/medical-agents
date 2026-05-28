"""Detect answer-leakage in NeuroBench tool outputs.

A tool report must read like the real modality: it describes what *that* test
shows, in real-report language. It must NOT state the integrated final clinical
diagnosis that the agent is supposed to synthesize from the whole picture.

This script flags candidate leaks — free-text interpretive fields in the
*tool-output* regions that contain the case's final diagnosis (full phrase or a
distinctive abbreviation). It deliberately SKIPS confirmatory modalities (CSF,
labs, specialized_test, drug_interactions): revealing a Gram stain organism, a
genetic mutation, or an autoantibody titer is realistic — that is the point of
ordering the confirmatory test.

It is a CANDIDATE detector: it over-flags (a finding that shares a word with the
diagnosis) and under-flags (an impression that names the diagnosis only in
finding-language). Use it to target review; the final call is clinical judgment:

  KEEP   describing a finding / hedged modality-level differential
         e.g. "hippocampal atrophy, MTA grade 1-2 ... neurodegenerative change
         cannot be excluded" ; "multi-territory embolic infarct pattern"
  FIX    stating the integrated final diagnosis on a non-confirmatory modality
         e.g. PET "most consistent with small cell lung carcinoma; paraneoplastic
         limbic encephalitis" -> "FDG-avid hilar mass, suspicious for malignancy,
         tissue diagnosis required; mesial temporal hypermetabolism, nonspecific"

Usage:
    uv run python agent-platform/scripts/detect_answer_leakage.py
    uv run python agent-platform/scripts/detect_answer_leakage.py --prefix SAH
    uv run python agent-platform/scripts/detect_answer_leakage.py --case PERI-NEURO-RP11.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

CASES_DIR = Path("data/neurobench_v5/cases")

# Free-text fields where naming the integrated diagnosis is a leak.
TEXT_FIELDS = {
    "impression", "interpretation", "clinical_correlation", "clinical_significance",
    "summary", "key_finding",
}
# Confirmatory modalities legitimately reveal their specific result — skip them.
CONFIRMATORY_SEGMENTS = {"csf", "labs", "specialized_test", "drug_interactions",
                         "literature_search"}
# Generic abbreviations that are not disease-specific.
GENERIC_ABBR = {"EEG", "MRI", "CT", "LP", "ICU", "IV", "CSF", "PET", "MRA", "MRV",
                "TTE", "TEE", "ECG", "EKG", "CTA"}


def dx_variants(dx: str) -> tuple[set[str], set[str]]:
    """Return (phrase variants, distinctive abbreviations) for a diagnosis."""
    abbrevs = {a for a in re.findall(r"\(([A-Z][A-Za-z0-9\-/]{1,12})\)", dx)
               if a not in GENERIC_ABBR}
    main = re.sub(r"\([^)]*\)", "", dx).lower().strip()
    main = re.sub(r"\s+", " ", main)
    core = re.split(r",| due to | with | from | secondary to ", main)[0].strip()
    variants = {v for v in {main, core} if len(v) >= 8}
    return variants, abbrevs


def _walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def leaks_in_case(case: dict) -> list[tuple[str, str, str]]:
    """Return [(path, matched_term, snippet)] candidate leaks for one case."""
    dx = case.get("ground_truth", {}).get("primary_diagnosis", "")
    if not dx:
        return []
    variants, abbrevs = dx_variants(dx)
    out: list[tuple[str, str, str]] = []
    for root in ("initial_tool_outputs", "followup_outputs", "fallback_tool_outputs"):
        if root not in case or case[root] is None:
            continue
        for path, s in _walk(case[root], root):
            seg = path.lower()
            if any(c in seg for c in CONFIRMATORY_SEGMENTS):
                continue
            field = path.split(".")[-1].split("[")[0]
            if field not in TEXT_FIELDS:
                continue
            sl = s.lower()
            hit = next((v for v in variants if v in sl), None)
            if not hit:
                hit = next((a for a in abbrevs
                            if re.search(rf"\b{re.escape(a)}\b", s)), None)
            if hit:
                out.append((path, hit, s[:160]))
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cases-dir", type=Path, default=CASES_DIR)
    p.add_argument("--prefix", help="Only scan cases with this condition prefix")
    p.add_argument("--case", help="Inspect a single case file in detail")
    args = p.parse_args()

    if args.case:
        case = json.loads((args.cases_dir / args.case).read_text())
        leaks = leaks_in_case(case)
        print(f"{args.case}: {len(leaks)} candidate leak(s)")
        for path, hit, sn in leaks:
            print(f'  [{path}] matched "{hit}"\n     {sn}')
        return 1 if leaks else 0

    files = sorted(args.cases_dir.glob("*.json"))
    if args.prefix:
        files = [f for f in files if f.name.startswith(args.prefix + "-")]

    by_case: dict[str, int] = {}
    by_cond: Counter[str] = Counter()
    total = 0
    for f in files:
        leaks = leaks_in_case(json.loads(f.read_text()))
        if leaks:
            by_case[f.name] = len(leaks)
            by_cond[f.name.rsplit("-", 1)[0]] += len(leaks)
            total += len(leaks)

    print(f"{len(by_case)}/{len(files)} cases with candidate leaks; {total} fields\n")
    for cond, n in sorted(by_cond.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {cond}")
    return 1 if by_case else 0


if __name__ == "__main__":
    sys.exit(main())
