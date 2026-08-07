"""A stored report must not assert a finding the case never records.

Three passes of this review authored reports for actions that had none, and twice the authoring
fabricated clinical content before an audit caught it:

  * every one of the 30 Guillain-Barré telemetry reports asserted sinus pauses of 3.2 and 3.8
    seconds "during tracheal suctioning" — identical numbers in all 30, in cases that never mention
    suctioning and are not all ventilated. The severity branch had been chosen by searching the case
    JSON *after* the new action was inserted into it, so the action's own words ("pauses beyond 3
    seconds") were read back as evidence;
  * GLIO-HG-S05's tissue report asserted TERT mutated, EGFR amplified and chromosome 7 gain with
    chromosome 10 loss, all of which that case mentions only as criteria to test.

Both are the same failure: a specific clinical assertion with no support in the case. This test
looks for the class rather than the two instances — a report claiming a distinctive finding whose
term appears nowhere else in the case — so the next one fails here instead of reaching a reviewer.

Negations are excluded: "no pause beyond 2 seconds" is a legitimate normal result and asserts
nothing. Values the report carries over from another of the case's own outputs are excluded too,
since those are derived rather than invented.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES = REPO_ROOT / "data/neurobench/cases"

pytestmark = pytest.mark.skipif(not CASES.exists(), reason="cases not present")

# Findings distinctive enough that a case describing the patient would mention them somewhere.
# Each is (label, pattern in the report, pattern that must exist elsewhere in the case).
DISTINCTIVE = [
    ("sinus pause", r"\bsinus pause|\bpause of \d|\bpause captured", r"pause|asystol|arrest"),
    ("tracheal suctioning", r"suction", r"suction"),
    ("atropine", r"atropine", r"atropine"),
    ("ileus", r"\bileus\b", r"ileus"),
    # For a molecular marker, the evidence must be the marker WITH AN OUTCOME. The bare term is not
    # enough: every glioma case quotes the WHO CNS5 definition ("...TERT promoter mutation, EGFR
    # gene amplification, or +7/-10..."), which lists the markers as criteria to test. Matching the
    # term alone let a fabricated "TERT promoter: Mutated" in GLIO-HG-S05 cite the definition of
    # glioblastoma as its own evidence — and an earlier version of this test did exactly that.
    ("TERT mutation", r"TERT[^.;]{0,30}\b(mutat|positive|present|detected)",
     r"TERT[^.;\"]{0,40}\b(present|detected|mutated|positive|c228t|c250t)"),
    ("EGFR amplification", r"EGFR[^.;]{0,30}\b(amplif|present|detected)",
     r"EGFR[^.;\"]{0,40}\b(present|detected|amplified|positive)"),
    ("1p/19q codeletion", r"1p/19q[^.;]{0,30}codelet(ed|ion)(?!\s*:?\s*(not|absent))",
     r"1p/19q[^.;\"]{0,40}\b(present|detected|codeleted|positive)"),
    ("shunt placed", r"shunt (was )?(placed|inserted)", r"shunt"),
]

# Reports whose content was MOVED into them from elsewhere in the same case, so the original source
# no longer appears "elsewhere" and the check above would read a migration as a fabrication. Each is
# verifiable in git: the 30 glioma tissue reports carry the neuropathology and molecular panel that
# the case previously stored as an `interpret_labs` follow-up, which was the defect being fixed —
# the biopsy result was obtainable by ordering bloods. Compare any of them against commit 52229f7.
#
# This list must stay short and each entry must name a real migration. It is not a place to silence
# a finding: GLIO-HG-S05 is deliberately absent, because that case stored no neuropathology at all
# and its first authored report did assert TERT, EGFR and chromosome markers with no basis. It was
# corrected rather than exempted.
MIGRATED = {
    (case_id, "tissue_diagnosis")
    for case_id in (
        "GLIO-HG-M01", "GLIO-HG-M02", "GLIO-HG-M03", "GLIO-HG-M04",
        "GLIO-HG-M05", "GLIO-HG-P01", "GLIO-HG-P02", "GLIO-HG-P03",
        "GLIO-HG-P04", "GLIO-HG-P05", "GLIO-HG-RM01", "GLIO-HG-RM02",
        "GLIO-HG-RM03", "GLIO-HG-RM04", "GLIO-HG-RP01", "GLIO-HG-RP02",
        "GLIO-HG-RP03", "GLIO-HG-RP04", "GLIO-HG-RS01", "GLIO-HG-RS02",
        "GLIO-HG-RS03", "GLIO-HG-RS04", "GLIO-HG-RS05", "GLIO-HG-RS06",
        "GLIO-HG-S01", "GLIO-HG-S02", "GLIO-HG-S03", "GLIO-HG-S04",
        "GLIO-HG-S06",
    )
}

NEGATED = re.compile(
    r"\b(no|not|without|absence of|denies|excluded?|none)\b[^.;]{0,40}$|"
    r"^\s*(no|none|not)\b", re.I
)


def _report_claims(report: dict) -> list[str]:
    """Positive assertions: findings and events, minus negations. Impression prose is excluded —
    it legitimately describes what a test looks for, which is not a claim about this patient."""
    claims: list[str] = []
    for finding in report.get("findings") or []:
        text = " ".join(str(v) for v in finding.values()) if isinstance(finding, dict) else str(finding)
        claims.append(text)
    for event in report.get("events") or []:
        claims.append(json.dumps(event))
    for key in ("integrated_diagnosis", "histological_diagnosis", "rhythm_summary"):
        if report.get(key):
            claims.append(str(report[key]))
    # Key and value together: the value alone ("Mutated") does not say which assay it belongs to,
    # and an earlier version of this test missed a fabricated TERT result for exactly that reason.
    for assay, value in (report.get("molecular_findings") or {}).items():
        claims.append(f"{assay}: {value}")
    return [c for c in claims if c and not NEGATED.search(c)]


def test_no_report_asserts_a_finding_absent_from_its_case() -> None:
    offenders: list[tuple[str, str, str]] = []
    for path in sorted(CASES.glob("*.json")):
        raw = json.loads(path.read_text())
        outputs = raw.get("initial_tool_outputs") or {}
        for field, report in outputs.items():
            if not isinstance(report, dict):
                continue
            # Evidence must come from the patient and from the case's other results — NOT from
            # ground_truth. That is the specification of what the agent should do, and its action
            # text names the findings the study looks for ("pauses beyond 3 seconds"), so including
            # it lets a fabricated report cite the instruction that asked for it as its own
            # evidence. That circularity is precisely how the GBS reports came to assert pauses in
            # all 30 cases, and an earlier version of this test reproduced it and passed.
            elsewhere = json.dumps(raw["patient"]) + json.dumps(raw.get("metadata") or {})
            elsewhere += json.dumps({k: v for k, v in outputs.items() if k != field})
            elsewhere += json.dumps(raw.get("followup_outputs") or [])
            elsewhere_low = elsewhere.lower()
            for claim in _report_claims(report):
                low = claim.lower()
                for label, in_report, in_case in DISTINCTIVE:
                    if not re.search(in_report, low, re.I):
                        continue
                    if re.search(in_case, elsewhere_low, re.I):
                        continue
                    if (raw["case_id"], field) in MIGRATED:
                        continue
                    offenders.append((raw["case_id"], f"{field}: {label}", claim[:120]))
    assert not offenders, (
        "reports asserting a finding that appears nowhere else in their case — the fabrication "
        f"class this test exists for: {offenders[:8]}"
    )


# A report that asserts something specific about *this* patient. A negative or non-contributory
# result carries no patient-specific claim and may legitimately be identical across a condition:
# 30 blood cultures with no growth in anti-NMDAR encephalitis are correct, and excluding sepsis is
# their whole purpose.
POSITIVE_CLAIM = re.compile(
    r"\b(?:mutat|amplif|codelet|methylat|positive|isolated|grew|growth of|elevated|reduced|"
    r"decreased|increased|pause|bradycard|arrhythm|stenosis|infarct|h[ae]morrhag|lesion|"
    r"atroph|hyperintens|enhanc)\w*", re.I
)


def test_identical_reports_across_a_condition_carry_no_positive_finding() -> None:
    """One report for thirty patients is a template. It is only acceptable when it asserts nothing.

    The first GBS telemetry pass produced a single report for all 30 cases *and* it asserted sinus
    pauses — a patient-specific finding, stated identically thirty times. That is the shape this
    catches. Uniform negative results are left alone: they are a legitimate and common ground truth.
    """
    whole: dict[tuple[str, str], set[str]] = {}
    counts: dict[tuple[str, str], int] = {}
    sample: dict[tuple[str, str], dict] = {}
    for path in sorted(CASES.glob("*.json")):
        raw = json.loads(path.read_text())
        outputs = raw.get("initial_tool_outputs") or {}
        for field, report in outputs.items():
            if not isinstance(report, dict):
                continue
            key = (raw["condition"], field)
            whole.setdefault(key, set()).add(json.dumps(report, sort_keys=True))
            counts[key] = counts.get(key, 0) + 1
            sample.setdefault(key, report)

    offenders: list[tuple[str, str, int, str]] = []
    for key, variants in whole.items():
        if counts[key] < 10 or len(variants) > 1:
            continue
        claims = " ".join(_report_claims(sample[key]))
        found = POSITIVE_CLAIM.findall(claims)
        if found:
            offenders.append((key[0], key[1], counts[key], ", ".join(sorted(set(found))[:4])))
    assert not offenders, (
        "an identical report across a whole condition that asserts a patient-specific positive "
        f"finding: {offenders}"
    )
