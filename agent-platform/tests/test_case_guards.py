"""Corpus guards from the October 2026 dataset review round.

Each guard is parametrized by case id, so one condition runs alone with e.g.
`pytest agent-platform/tests/test_case_guards.py -k "ALS-"`.

1. Answer-key leakage: `search_medical_literature` and `check_drug_interactions` are served for any
   query or drug, so a stored output of theirs that repeats a criterion's `expected_evidence` hands
   the scoring key to every agent that calls them.
2. Follow-up trigger hygiene: the index (first) order of a study must be answered with the index
   study, not with a repeat-study follow-up that shares a token with it.
3. Banned strings per condition: superseded drugs, criteria and phrasings the reviewers removed.
   Data-driven (`BANNED`), so later conditions add rows rather than tests.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import pytest

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "data/neurobench/cases"
CASE_IDS = sorted(path.stem for path in CASES.glob("*.json"))


def condition_of(case_id: str) -> str:
    return re.sub(r"-R?[SMP]\d+$", "", case_id)


def _raw(case_id: str) -> dict[str, Any]:
    return json.loads((CASES / f"{case_id}.json").read_text())


def _strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _normalize(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


# ---------------------------------------------------------------------------------------
# 1. Literature and drug-interaction outputs must not carry the scoring key.

_ANY_QUERY_TOOLS = {
    "search_medical_literature": "literature_search",
    "check_drug_interactions": "drug_interactions",
}
_LEAK_WINDOW = 60


def _any_query_outputs(case: dict[str, Any]) -> Iterator[tuple[str, Any]]:
    for block in ("initial_tool_outputs", "fallback_tool_outputs"):
        outputs = case.get(block) or {}
        for field in _ANY_QUERY_TOOLS.values():
            for key, output in (outputs.get(field) or {}).items():
                yield f"{block}.{field}[{key!r}]", output
    for index, followup in enumerate(case.get("followup_outputs") or []):
        if followup.get("tool_name") in _ANY_QUERY_TOOLS:
            yield f"followup_outputs[{index}] {followup.get('trigger_action')}", followup.get("output")


def leaks(case: dict[str, Any]) -> list[str]:
    found = []
    criteria = (case.get("ground_truth") or {}).get("action_criteria") or []
    outputs = [(where, _normalize(" ".join(_strings(output)))) for where, output in _any_query_outputs(case)]
    for criterion in criteria:
        evidence = _normalize(criterion.get("expected_evidence") or "")
        if len(evidence) < _LEAK_WINDOW:
            continue
        windows = {evidence[i : i + _LEAK_WINDOW] for i in range(len(evidence) - _LEAK_WINDOW + 1)}
        for where, text in outputs:
            hit = next((w for w in windows if w in text), None)
            if hit:
                found.append(f"{where} repeats expected_evidence of {criterion.get('criterion_id')}: {hit!r}")
    return found


@pytest.mark.parametrize("case_id", CASE_IDS)
def test_any_query_outputs_do_not_leak_expected_evidence(case_id):
    assert not leaks(_raw(case_id))


# ---------------------------------------------------------------------------------------
# 2. A repeat-study follow-up must not answer the index order of its study.

# Tokens that mark a follow-up as a later study or a later report of one.
_REPEAT_MARKERS = {"repeat", "repeated", "serial", "recheck", "final", "followup", "rerun"}


def _tokens(value: Any) -> set[str]:
    return set(re.sub(r"[^a-z0-9]+", " ", " ".join(_strings(value)).lower()).split())


def _is_repeat(trigger: str) -> bool:
    return bool(set(re.split(r"[^a-z0-9]+", trigger.lower())) & _REPEAT_MARKERS)


def hijacked_index_orders(case_id: str) -> list[str]:
    """Index orders answered by a repeat follow-up, through the real MockServer resolver.

    For each required/recommended criterion that is not itself a repeat order, the criterion's first
    alternative is placed as the first call to its tool in a fresh environment (the index study, as
    the perfect agent orders it). It must not be answered with a repeat-study follow-up.
    """
    from neuroagent.harness.environment import NeuroBenchEnvironment
    from neuroagent_schemas import NeuroBenchCase, ToolAction

    case = NeuroBenchCase.model_validate_json((CASES / f"{case_id}.json").read_text())
    repeats = [fu for fu in case.followup_outputs if _is_repeat(fu.trigger_action)]
    if not repeats:
        return []
    problems = []
    for criterion in case.ground_truth.action_criteria:
        if criterion.importance.value not in ("required", "recommended"):
            continue
        pattern = criterion.alternatives[0]
        if _tokens(pattern.required_arguments) & _REPEAT_MARKERS:
            continue  # the criterion is itself the repeat order
        candidates = [fu for fu in repeats if fu.tool_name == pattern.tool_name]
        if not candidates:
            continue
        environment = NeuroBenchEnvironment(case)
        schema = environment.registry.get_tool(pattern.tool_name).parameter_schema
        arguments = dict(pattern.required_arguments)
        for name in schema.get("required", []):
            # A neutral context, so only the study identity can select a follow-up.
            arguments.setdefault(name, "index order")
        result = environment.execute(ToolAction(tool_name=pattern.tool_name, arguments=arguments))
        if not result.success:
            continue  # the perfect-agent check reports rejected calls
        for followup in candidates:
            if followup.output.model_dump() == result.output:
                problems.append(
                    f"{criterion.criterion_id} {pattern.tool_name} {pattern.required_arguments} "
                    f"answered by repeat follow-up {followup.trigger_action!r}"
                )
    return problems


@pytest.mark.parametrize("case_id", CASE_IDS)
def test_index_order_is_not_answered_by_a_repeat_followup(case_id):
    assert not hijacked_index_orders(case_id)


# ---------------------------------------------------------------------------------------
# 3. Banned strings per condition.


@dataclass(frozen=True)
class Banned:
    """A phrase a condition's cases must not contain, matched per sentence of every string field.

    `pattern` must match the sentence; `unless`, when given, exempts a sentence it also matches
    (e.g. a criterion named as superseded); `tools`, when given, limits the row to the stored
    outputs of those tools (initial, follow-up and fallback); `except_cases` exempts named cases
    (a phrase that is right in one case of the condition only).
    """

    condition: str
    label: str
    pattern: str
    unless: str | None = None
    tools: tuple[str, ...] = ()
    except_cases: tuple[str, ...] = ()


BANNED: tuple[Banned, ...] = (
    Banned("ALS", "AMX0035 (withdrawn 2024)", r"\bAMX0035\b"),
    Banned("ALS", "Relyvrio (withdrawn 2024)", r"\bRelyvrio\b"),
    Banned("ALS", "grapefruit as a CYP1A2 modulator (it inhibits CYP3A4)",
           r"grapefruit.*CYP1A2|CYP1A2.*grapefruit"),
    Banned("ALS", "reference to the July 2026 review", r"July 2026 review"),
    Banned("ALS", "El Escorial presented as the current criteria (Gold Coast 2020)",
           r"El Escorial",
           unless=r"Gold Coast|supersed|replac|older|former|historic|previous|no longer|rather than|instead of"),
    Banned("BACT-MEN", "CSF/serum glucose ratio 'normal >0.6'", r"normal\s*>\s*0\.6"),
    Banned("BACT-MEN", "'age >50' as the ampicillin/Listeria criterion",
           r"(age\s*>\s*50.*(ampicillin|listeria))|((ampicillin|listeria).*age\s*>\s*50)"),
    Banned("HEP-ENC", "'2-4 soft' signs", r"\b2\s*[-–]\s*4\s+soft"),
    Banned("HEP-ENC", "'the finding the lumbar puncture is gated on'",
           r"the finding the lumbar puncture is gated on"),
    Banned("HEP-ENC", "a CT report claiming restricted diffusion", r"restricted diffusion",
           tools=("order_ct_scan",)),
    # FEPI-TEMP (24 Oct 2026 close-out): the fabricated "Glauser 2017" monotherapy review (the real
    # one is Epilepsia 2013;54:551-563), FDA letter categories (retired 2015), Glauser 2013 Level A
    # misstatements for adults, and prolactin outside the one case with a level drawn 22 minutes
    # after the event (AAN 2005).
    Banned("FEPI-TEMP", "the non-existent Glauser 2017 monotherapy review",
           r"Glauser[^.;]{0,40}2017|2017\s*;\s*58\s*:\s*1235"),
    Banned("FEPI-TEMP", "FDA pregnancy letter category", r"\bCategory X\b"),
    Banned("FEPI-TEMP", "oxcarbazepine as Level A in adults (Glauser 2013: Level A in children only)",
           r"oxcarbazepine[^.;]{0,80}\bLevel A\b|\bLevel A\b[^.;]{0,80}oxcarbazepine"),
    Banned("FEPI-TEMP", "lamotrigine as Level A outside the elderly (Glauser 2013)",
           r"lamotrigine[^.;]{0,80}\bLevel A\b|\bLevel A\b[^.;]{0,80}lamotrigine",
           unless=r"elderly|older adult|aged 60|over 60"),
    Banned("FEPI-TEMP", "prolactin outside FEPI-TEMP-P05", r"prolactin",
           unless=r"\bremoved\b|\bdeleted\b", except_cases=("FEPI-TEMP-P05",)),
)

_TOOL_FIELDS = {"order_ct_scan": "ct"}
_SENTENCE = re.compile(r"(?<=[.;!?])\s+|\n+")


def _scoped_strings(case: dict[str, Any], tools: tuple[str, ...]) -> Iterator[str]:
    if not tools:
        yield from _strings(case)
        return
    for block in ("initial_tool_outputs", "fallback_tool_outputs"):
        for tool in tools:
            yield from _strings((case.get(block) or {}).get(_TOOL_FIELDS.get(tool, tool)))
    for followup in case.get("followup_outputs") or []:
        if followup.get("tool_name") in tools:
            yield from _strings(followup.get("output"))


def banned_hits(case_id: str, case: dict[str, Any] | None = None) -> list[str]:
    case = case if case is not None else _raw(case_id)
    hits = []
    for row in BANNED:
        if condition_of(case_id) != row.condition or case_id in row.except_cases:
            continue
        for text in _scoped_strings(case, row.tools):
            for sentence in _SENTENCE.split(text):
                if re.search(row.pattern, sentence, re.IGNORECASE) and not (
                    row.unless and re.search(row.unless, sentence, re.IGNORECASE)
                ):
                    hits.append(f"{row.label}: {sentence.strip()[:200]!r}")
    return hits


@pytest.mark.parametrize("case_id", [c for c in CASE_IDS if condition_of(c) in {row.condition for row in BANNED}])
def test_condition_banned_strings(case_id):
    assert not banned_hits(case_id)


def test_banned_table_rows_fire():
    """Each row catches its own phrasing and spares the exempt one."""
    def case(text: str, field: str = "notes") -> dict[str, Any]:
        return {"metadata": {field: text}}

    assert banned_hits("ALS-S01", case("Started on AMX0035 last year."))
    assert banned_hits("ALS-S01", case("Grapefruit juice inhibits CYP1A2."))
    assert banned_hits("ALS-S01", case("Meets revised El Escorial criteria for definite ALS."))
    assert not banned_hits("ALS-S01", case("Gold Coast criteria met (El Escorial is superseded)."))
    assert banned_hits("BACT-MEN-S01", case("Add ampicillin for Listeria if age >50."))
    assert banned_hits("BACT-MEN-S01", case("CSF:serum glucose ratio 0.2 (normal >0.6)."))
    assert banned_hits("HEP-ENC-S01", case("Two to four: 2-4 soft signs present."))
    ct = {"initial_tool_outputs": {"ct": {"findings": "Hypodensity with restricted diffusion."}}}
    assert banned_hits("HEP-ENC-S01", ct)
    assert not banned_hits("HEP-ENC-S01", {"initial_tool_outputs": {"mri": {"findings": "restricted diffusion"}}})
    assert not banned_hits("ISCH-STR-S01", case("AMX0035"))
    assert banned_hits("FEPI-TEMP-S01", case("Glauser T et al., Epilepsia 2017;58:1235-1268."))
    assert banned_hits("FEPI-TEMP-S01", case("Valproate is Category X in pregnancy."))
    assert banned_hits("FEPI-TEMP-S01", case("Oxcarbazepine (Level A) is first line."))
    assert banned_hits("FEPI-TEMP-S01", case("Lamotrigine has Level A evidence in adults."))
    assert not banned_hits("FEPI-TEMP-S01", case("Lamotrigine reaches Level A only in the elderly."))
    assert banned_hits("FEPI-TEMP-S01", case("Prolactin 31 ng/mL at 6 hours."))
    assert not banned_hits("FEPI-TEMP-P05", case("Prolactin 48 ng/mL drawn 22 minutes after the event."))


# ---------------------------------------------------------------------------------------
# 4. Discriminator fields (24 Oct 2026).
#
# The MockServer routes a stored report by its discriminating field (`MockServer._DISCRIMINATOR`):
# a vocabulary value answers only its own study, while an empty or prose value is not adjudicated
# and answers every variant of the tool (a fallback "normal study" served for any test type, a
# 24-hour telemetry report for any monitor). So every stored output (initial and follow-up) and
# every case fallback of a routed tool must carry an exact vocabulary term; a fallback that cannot
# honestly name one study is null, and the library answers per study. Body imaging has no `study`
# field: its report must carry a vocabulary modality and a region that some `<region>_<modality>`
# study matches. Conditions are added to `DISCRIMINATOR_CONDITIONS` as their data is fixed.

DISCRIMINATOR_CONDITIONS = frozenset({
    "ALS", "BACT-MEN", "ISCH-STR", "HEP-ENC", "GLIO-HG", "GBS", "ALZ-EARLY", "SAH", "SE",
    "VASC-DEM", "NMDAR-ENC", "MIG-AURA", "SYNC-CARD", "FTD", "MG", "NPH", "FND", "MS-RR",
    "FEPI-TEMP", "PD",
})

# initial_tool_outputs / fallback_tool_outputs slot of each routed tool.
_ROUTED_SLOTS = {
    "order_microbiology": "microbiology",
    "order_body_imaging": "body_imaging",
    "order_advanced_imaging": "advanced_imaging",
    "order_echocardiogram": "echo",
    "order_specialized_test": "specialized_test",
    "obtain_tissue_diagnosis": "tissue_diagnosis",
    "perform_clinical_assessment": "clinical_assessment",
    "order_cardiac_monitoring": "cardiac_monitoring",
    "analyze_eeg": "eeg",  # 24 Oct 2026
}


def discriminator_defects(case: dict[str, Any]) -> list[str]:
    from neuroagent.tools.mock_server import MockServer
    from neuroagent.tools.vocabulary import DOMAIN_PACKS, body_imaging_studies

    assert set(_ROUTED_SLOTS) == set(MockServer._DISCRIMINATOR), "a routed tool has no slot here"
    packs = DOMAIN_PACKS[case.get("domain") or "neurology"]
    fold = MockServer._fold
    reports: list[tuple[str, str, Any]] = []
    for block in ("initial_tool_outputs", "fallback_tool_outputs"):
        for tool, slot in _ROUTED_SLOTS.items():
            output = (case.get(block) or {}).get(slot)
            if output:
                reports.append((f"{block}.{slot}", tool, output))
    for index, followup in enumerate(case.get("followup_outputs") or []):
        if followup.get("tool_name") in _ROUTED_SLOTS:
            reports.append((f"followup_outputs[{index}] {followup.get('trigger_action')}",
                            followup["tool_name"], followup.get("output") or {}))
    found = []
    for where, tool, output in reports:
        if tool == "order_body_imaging":
            modality = fold(output.get("modality") or "")
            region = output.get("region") or ""
            report = type("Report", (), {"modality": output.get("modality"), "region": region})()
            if not (modality and modality <= MockServer._BODY_MODALITIES and region and any(
                MockServer._body_study_matches(study, report) for study in body_imaging_studies(packs=packs)
            )):
                found.append(f"{where}: modality {output.get('modality')!r}, region {region!r}")
            continue
        key, vocabulary = MockServer._DISCRIMINATOR[tool]
        value = output.get(key)
        if not value or fold(value) not in {fold(term) for term in vocabulary(packs=packs)}:
            found.append(f"{where}: {key} {value!r} is not a {tool} term")
    # Two stored pathway reports of one study (the NPH baseline gait and its post-tap
    # reassessment) are told apart only by the secondary discriminator: each must carry a
    # distinct term of it, or the baseline order can receive the later report.
    from collections import defaultdict

    same_study: dict[tuple[str, Any], list[tuple[str, Any]]] = defaultdict(list)
    for where, tool, output in reports:
        secondary = MockServer._SECONDARY_DISCRIMINATOR.get(tool)
        if secondary is None or where.startswith("fallback_tool_outputs"):
            continue
        primary = MockServer._DISCRIMINATOR[tool][0]
        same_study[(tool, fold(output.get(primary) or ""))].append((where, output.get(secondary[0])))
    for (tool, _), stored in same_study.items():
        if len(stored) < 2:
            continue
        key, vocabulary, _default = MockServer._SECONDARY_DISCRIMINATOR[tool]
        terms = {fold(term) for term in vocabulary(packs=packs)}
        values = [fold(value or "") for _, value in stored]
        if not all(value in terms for value in values) or len(set(values)) < len(values):
            found += [f"{where}: {key} {value!r} does not tell apart two stored {tool} reports"
                      for where, value in stored]
    return found


@pytest.mark.parametrize("case_id", [c for c in CASE_IDS if condition_of(c) in DISCRIMINATOR_CONDITIONS])
def test_routed_outputs_name_their_study(case_id):
    assert not discriminator_defects(_raw(case_id))


def test_discriminator_guard_fires():
    case = {"fallback_tool_outputs": {"specialized_test": {"test_type": "", "impression": "Normal."}},
            "followup_outputs": [{"tool_name": "order_cardiac_monitoring", "trigger_action": "t",
                                  "output": {"monitor_type": "Continuous telemetry"}},
                                 {"tool_name": "order_body_imaging", "trigger_action": "u",
                                  "output": {"modality": "Doppler ultrasound", "region": "abdomen"}}]}
    assert len(discriminator_defects(case)) == 3
    case["fallback_tool_outputs"]["specialized_test"] = None
    case["followup_outputs"][0]["output"]["monitor_type"] = "telemetry"
    case["followup_outputs"][1]["output"]["modality"] = "ultrasound"
    assert not discriminator_defects(case)


def test_secondary_discriminator_guard_fires():
    gait = {"assessment_type": "gait_and_balance_timed", "impression": "TUG 18 s."}
    case = {"initial_tool_outputs": {"clinical_assessment": {**gait, "timing": "baseline"}},
            "followup_outputs": [{"tool_name": "perform_clinical_assessment", "trigger_action": "t",
                                  "output": {**gait, "timing": "baseline"}}]}
    assert len(discriminator_defects(case)) == 2
    case["followup_outputs"][0]["output"]["timing"] = ""
    assert len(discriminator_defects(case)) == 2
    case["followup_outputs"][0]["output"]["timing"] = "post_intervention"
    assert not discriminator_defects(case)


def test_leak_detector_fires():
    evidence = "Gold Coast criteria are met with upper and lower motor neuron signs in two regions and progression."
    case = {
        "ground_truth": {"action_criteria": [{"criterion_id": "c", "expected_evidence": evidence}]},
        "initial_tool_outputs": {"literature_search": {"q": {"summary": "Review: " + evidence.upper()}}},
    }
    assert leaks(case)
    case["initial_tool_outputs"]["literature_search"]["q"]["summary"] = "Unrelated guideline summary."
    assert not leaks(case)


# ---------------------------------------------------------------------------------------
# 5. A routine EEG order in a case recorded on continuous ICU EEG (25 Oct 2026).
#
# `analyze_eeg` routes by `eeg_type`, and an order without it is a routine EEG. A case whose stored
# recording is a continuous ICU EEG (SE) answered a routine order with the library's normal report,
# which contradicts a patient in status: a 30-minute recording during ongoing seizures records them.
# Such a case must also store a routine recording of its own (initial, follow-up or fallback).


def routine_eeg_defects(case: dict[str, Any]) -> list[str]:
    from neuroagent.tools.mock_server import MockServer

    fold = MockServer._fold
    stored = [(case.get("initial_tool_outputs") or {}).get("eeg"),
              (case.get("fallback_tool_outputs") or {}).get("eeg"),
              *(fu.get("output") for fu in case.get("followup_outputs") or []
                if fu.get("tool_name") == "analyze_eeg")]
    types = {fold(output.get("eeg_type") or "") for output in stored if output}
    if fold("continuous_icu") in types and fold("routine") not in types:
        return ["stores a continuous_icu EEG but no routine EEG: a routine order gets the library normal"]
    return []


@pytest.mark.parametrize("case_id", CASE_IDS)
def test_continuous_eeg_case_answers_a_routine_order(case_id):
    assert not routine_eeg_defects(_raw(case_id))


def test_routine_eeg_guard_fires():
    case = {"initial_tool_outputs": {"eeg": {"eeg_type": "continuous_icu", "impression": "Seizures."}},
            "fallback_tool_outputs": {"eeg": None}}
    assert routine_eeg_defects(case)
    case["fallback_tool_outputs"]["eeg"] = {"eeg_type": "routine", "impression": "Seizures."}
    assert not routine_eeg_defects(case)
