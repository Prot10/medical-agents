"""A stored report must not deny in its impression what it asserts in its findings.

Found by the per-case audit: 21 `order_microbiology` reports carried `organism: null` and an impression
reading "No organism isolated to date", while their own `findings` named the pathogen in both aerobic
bottles and their `susceptibility` block listed its MICs. An agent reading the impression concludes the
cultures are negative and cannot narrow therapy; an agent reading the findings concludes the opposite.
The judge reads the impression, so the correct decision would have been scored as unsupported.

Nothing in the suite could see it. `validate_cases.py` checks that an action has *somewhere to land*
and `check_perfect_agent.py` checks that the gold trajectory scores 1.0 — neither reads a report
against itself.

The same shape is checked for CSF, where a "no growth" or "no organism" statement alongside a named
isolate would be the identical defect.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES = REPO_ROOT / "data/neurobench/cases"

pytestmark = pytest.mark.skipif(not CASES.exists(), reason="cases not present")

ORGANISM = re.compile(
    r"streptococc|pneumococc|neisseria\s+\w+|listeria\s+\w+|haemophilus\s+\w+|staphylococc|"
    r"klebsiella\s+\w+|proteus\s+\w+|escherichia\s+coli|e\.\s?coli|enterococc|pseudomonas\s+\w+|"
    r"cryptococc|diplococc",
    re.I,
)
DENIAL = re.compile(r"no organism|no growth|sterile|negative to date|no bacterial growth", re.I)


def _named_isolates(findings: object) -> list[str]:
    """Organisms named in a report's findings, ignoring rows that say nothing grew."""
    isolates: list[str] = []
    if not isinstance(findings, list):
        return isolates
    for row in findings:
        if not isinstance(row, dict):
            continue
        result = str(row.get("result") or row.get("value") or "")
        if DENIAL.search(result):
            continue
        match = ORGANISM.search(result)
        if match:
            isolates.append(match.group(0))
    return isolates


def _contradicts(output: dict) -> str | None:
    """The denial, if the report denies an organism its own findings name.

    The check is on the `organism` field — the report's own summary of what grew — and not on the
    impression. A first version flagged any impression containing "no growth", which is a false
    positive the moment a report correctly says the aerobic bottles grew and the anaerobic one did
    not: mixed growth is normal, and a rule that cannot express it would push authors towards
    reports that hide the negative bottle.
    """
    isolates = _named_isolates(output.get("findings"))
    if not isolates:
        return None
    organism = str(output.get("organism") or "")
    if not organism.strip():
        return f"organism field is empty but findings name {isolates[0]!r}"
    if DENIAL.search(organism):
        return f"organism field says {organism!r} but findings name {isolates[0]!r}"
    return None


def _specimen_reports(raw: dict):
    """Every stored microbiology and CSF report, with a path for the failure message."""
    for tool, key in (("order_microbiology", "microbiology"), ("analyze_csf", "csf")):
        output = raw["initial_tool_outputs"].get(key)
        if isinstance(output, dict):
            yield f"initial_tool_outputs.{key}", output
        for index, followup in enumerate(raw.get("followup_outputs") or []):
            if followup.get("tool_name") == tool and isinstance(followup.get("output"), dict):
                yield f"followup_outputs[{index}]", followup["output"]


def test_no_culture_report_denies_an_organism_it_names() -> None:
    failures: list[str] = []
    for path in sorted(CASES.glob("*.json")):
        raw = json.loads(path.read_text())
        for where, output in _specimen_reports(raw):
            problem = _contradicts(output)
            if problem:
                failures.append(f"{raw['case_id']} {where}: {problem}")

    assert not failures, (
        "these reports assert an isolate in their findings and deny it elsewhere, so the same report "
        f"supports opposite treatment decisions:\n  " + "\n  ".join(failures[:15])
    )
