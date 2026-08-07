"""The panel and the cases must not disagree in silence.

`dataset-generation/config/conditions.yaml` is the generation input and it feeds the tool catalog
the clinical reviewers read. The tier the benchmark actually *measures* is
`ground_truth.optimal_actions[].category` inside each case. For a month those two disagreed for
thirteen of the reviewers' eighteen tier changes: the change had been made in the file that is read
and not in the one that is scored, which is the same class of error as the stale review catalog.

Nothing in the suite could see it. `validate_cases.py` and `check_perfect_agent.py` both check each
case *against itself* — that its actions are answerable, that a perfect agent reaches 1.0 — and
never against its condition's panel. The only tool that compared them was a report, and a report is
read when someone remembers to run it.

Two tests, for the two failure modes actually observed:

1. **A required set that costs nothing.** Fifteen migraine-with-aura cases had a required set
   consisting only of `search_medical_literature` and `check_drug_interactions`, both priced at
   zero. An agent scored 1.0 required coverage there without performing a single diagnostic act,
   and the ICHD-3 structured history that Reviewer 1 called that condition's only true required
   test was absent from all 30. This is the sharper of the two tests, because it needs no panel: a
   condition whose correct workup is genuinely nothing has no business being scored on coverage.

2. **A panel-required tool absent from a case, with no stated reason.** Legitimate exemptions
   exist — conditional requirements (CSF in subarachnoid haemorrhage is mandatory only when the CT
   is non-diagnostic) and per-case contraindications (MRI in VASC-DEM-P08, whose pacemaker is not
   MR-conditional). Those are declared in `metadata.panel_required_exemptions` as
   `{tool: reason}`, so an exemption is a documented clinical decision rather than an omission
   nobody noticed.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from neuroagent.review_api.services.tool_catalog import _CONDITION_ALIAS, _MODALITY_TO_TOOL
from neuroagent.tools.cost_tracker import CostTracker
from neuroagent_schemas import NeuroBenchCase

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES = REPO_ROOT / "data/neurobench/cases"
CONDITIONS = REPO_ROOT / "dataset-generation/config/conditions.yaml"

pytestmark = pytest.mark.skipif(not CASES.exists(), reason="cases not present")


@pytest.fixture(scope="module")
def cases() -> list[NeuroBenchCase]:
    return [NeuroBenchCase.model_validate(json.loads(p.read_text()))
            for p in sorted(CASES.glob("*.json"))]


@pytest.fixture(scope="module")
def raw_cases() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(CASES.glob("*.json"))]


@pytest.fixture(scope="module")
def panels() -> dict:
    return yaml.safe_load(CONDITIONS.read_text()) or {}


def test_no_case_has_a_free_required_set(cases: list[NeuroBenchCase]) -> None:
    """Required coverage must cost something to earn.

    A case whose entire required tool set is zero-cost hands out full required coverage for two
    calls that carry no diagnostic finding. Fifteen migraine cases were in that state until the
    ICHD-3 structured history was added; the guard keeps them out.
    """
    tracker = CostTracker()
    free: list[tuple[str, list[str]]] = []
    for case in cases:
        required = [a for a in case.ground_truth.optimal_actions
                    if a.category.value == "required" and a.tool_name]
        if not required:
            continue
        total = sum(
            tracker.compute_cost(a.tool_name, dict(a.tool_parameters or {})).cost_usd
            for a in required
        )
        if total == 0:
            free.append((case.case_id, sorted({a.tool_name for a in required})))
    assert not free, (
        "cases whose required set is entirely zero-cost — an agent scores 1.0 required coverage "
        f"without a diagnostic act: {free[:10]}"
    )


def test_panel_required_tools_are_present_or_exempted(
    raw_cases: list[dict], panels: dict
) -> None:
    """A tool the panel marks required is in the case, or the case says why not."""
    undeclared: list[tuple[str, str]] = []
    for raw in raw_cases:
        condition = raw["condition"]
        panel = panels.get(_CONDITION_ALIAS.get(condition, condition))
        if not panel:
            continue
        required = {
            _MODALITY_TO_TOOL[token]
            for token in panel.get("required_modalities") or []
            if token in _MODALITY_TO_TOOL
        }
        present = {a["tool_name"] for a in raw["ground_truth"]["optimal_actions"] if a["tool_name"]}
        exempt = (raw.get("metadata") or {}).get("panel_required_exemptions") or {}
        for tool in sorted(required - present):
            if not str(exempt.get(tool, "")).strip():
                undeclared.append((raw["case_id"], tool))
    assert not undeclared, (
        "panel marks these tools required but the case neither contains them nor documents an "
        f"exemption in metadata.panel_required_exemptions: {undeclared[:12]}"
    )


def test_exemptions_are_not_used_for_tools_the_case_does_contain(raw_cases: list[dict]) -> None:
    """A stale exemption is a lie about the case; remove it when the action is added."""
    stale: list[tuple[str, str]] = []
    for raw in raw_cases:
        exempt = (raw.get("metadata") or {}).get("panel_required_exemptions") or {}
        present = {a["tool_name"] for a in raw["ground_truth"]["optimal_actions"] if a["tool_name"]}
        for tool in exempt:
            if tool in present:
                stale.append((raw["case_id"], tool))
    assert not stale, f"exemption recorded for a tool the case does use: {stale[:12]}"
