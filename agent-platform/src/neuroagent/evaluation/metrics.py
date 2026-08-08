"""Evaluation metrics for agent performance."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from neuroagent_schemas import GroundTruth, ToolClassification
from neuroagent_schemas.enums import SequenceSeverity

from ..agent.reasoning import AgentTrace
from ..tools.vocabulary import analyte_satisfied_by, normalize_analyte


# Heuristics for the "premature closure" metric: phrases that indicate the
# agent has committed to a diagnosis in its reasoning. Any tool call AFTER
# the first occurrence of one of these in an assistant turn counts as a
# premature-closure call.
_CONFIDENT_DX_PATTERNS = [
    r"\bprimary diagnosis\s*[:\-]\s*\S",
    r"\b(?:i am|i'm)\s+confident\b",
    r"\bconfident\s+(?:that|the)\b",
    r"\bthe\s+diagnosis\s+is\b",
    r"\bdefinit(?:ive|ively|ely)\s+\w*\s*diagnos",
    r"\bcertain(?:ly|ty)\s+\w*\s*diagnos",
    r"\bfinal\s+diagnosis\b",
    r"###\s*primary\s+diagnosis",
]


# ---------------------------------------------------------------------------
# Semantic matching helpers
# ---------------------------------------------------------------------------

# The model's reasoning scratchpad. Matched anywhere (incl. an unclosed block from a
# prompt that pre-opens `<think>`), so scoring never reads deliberation as the answer.
_THINK_BLOCK = re.compile(r"<think>.*?</think>|<think>.*\Z", re.DOTALL | re.IGNORECASE)


def _strip_think(text: str | None) -> str:
    """Remove `<think>…</think>` (and any trailing unclosed think) from a response."""
    if not text:
        return ""
    return _THINK_BLOCK.sub(" ", text)


# Common clinical action keywords grouped by category.
# Used to fuzzy-match free-text critical/contraindicated actions against
# the agent's tool calls and final response.
_TOOL_ACTION_MAP: dict[str, list[str]] = {
    "analyze_eeg": ["eeg", "electroencephalogr", "video-eeg", "continuous eeg"],
    "analyze_brain_mri": [
        "mri", "brain mri", "brain imaging", "neuroimaging",
        "diffusion", "flair", "dwi",
    ],
    "analyze_ecg": ["ecg", "electrocardiogr", "12-lead"],
    "interpret_labs": [
        "lab", "blood test", "cbc", "bmp", "metabolic panel", "coagulation",
        "blood culture", "troponin", "thyroid", "tsh", "b12", "hba1c",
    ],
    "analyze_csf": [
        "csf", "lumbar puncture", "spinal tap", "cerebrospinal",
        "lp", "opening pressure",
    ],
    "search_medical_literature": [
        "literature", "guideline", "evidence", "pubmed", "search",
    ],
    "check_drug_interactions": [
        "drug interaction", "medication check", "contraindication",
        "prescri", "formulary", "interaction check",
    ],
    "order_ct_scan": [
        "ct scan", "ct head", "non-contrast ct", "ct brain",
        "ct angiogr", "cta ", "cta,",
    ],
    "order_echocardiogram": [
        "echocardiogr", "echocard", "transthoracic", "transesophageal",
        "tte", "tee", "bubble study", "cardiac ultrasound",
    ],
    "order_cardiac_monitoring": [
        "holter", "cardiac monitor", "event monitor", "telemetry",
        "rhythm monitor",
    ],
    "order_advanced_imaging": [
        "pet scan", "amyloid pet", "fdg-pet", "fdg pet", "datscan",
        "dat scan", "perfusion", "spectroscopy", "carotid duplex",
        "carotid doppler", "carotid ultrasound", "mra",
    ],
    "order_specialized_test": [
        "neuropsych", "cognitive test", "mmse", "moca",
        "emg", "nerve conduction", "electromyogr",
        "evoked potential", "vep ", "ssep", "baep",
        "tilt table", "tilt test",
        "polysomnogr", "sleep study",
        "autonomic test", "autonomic function",
        "stress test",
    ],
}


def _action_text_matches_tool(action_text: str, tool_name: str) -> bool:
    """Check if a free-text action description plausibly matches a tool name."""
    text_lower = action_text.lower()
    # Direct tool name match (with or without underscores)
    if tool_name in text_lower or tool_name.replace("_", " ") in text_lower:
        return True
    # Keyword matching
    keywords = _TOOL_ACTION_MAP.get(tool_name, [])
    return any(kw in text_lower for kw in keywords)


def _action_text_in_response(action_text: str, response: str) -> bool:
    """Check if a free-text action is addressed in the agent's final response.

    Uses key-phrase extraction: pulls the most distinctive terms from the
    action description and checks if they appear in the response.
    """
    if not response:
        return False
    text_lower = action_text.lower()
    response_lower = response.lower()

    # Extract key clinical terms (3+ chars, not stopwords)
    stopwords = {
        "the", "and", "for", "with", "that", "this", "from", "should",
        "must", "when", "before", "after", "during", "about", "into",
        "over", "upon", "between", "through", "obtain", "order", "perform",
        "ensure", "assess", "evaluate", "consider", "monitor", "check",
    }
    terms = [
        t for t in re.findall(r"[a-z]{3,}", text_lower)
        if t not in stopwords
    ]

    if not terms:
        return False

    # Require at least 50% of distinctive terms to appear in response
    matches = sum(1 for t in terms if t in response_lower)
    return matches >= max(1, len(terms) * 0.5)


def check_critical_action(
    action_text: str,
    tools_called: list[str],
    final_response: str,
) -> bool:
    """Determine if a critical action was performed.

    Checks BOTH tool calls (did the agent order the right test?) AND the
    final response text (did the agent recommend the right action?).
    """
    # Check 1: Did the agent call a tool that matches this action?
    for tool in tools_called:
        if _action_text_matches_tool(action_text, tool):
            return True

    # Check 2: Did the agent address this action in their COMMITTED response?
    # Strip <think> first: the scratchpad is not the agent's answer, and the serving
    # path (orchestrator) already keeps it out of final_response. Scoring think text
    # let a completion that ordered nothing earn full critical-action credit just by
    # narrating the plan in its reasoning — reward that vanished at eval.
    if _action_text_in_response(action_text, _strip_think(final_response)):
        return True

    return False


def check_contraindicated_action(
    action_text: str,
    tools_called: list[str],
    final_response: str,
) -> bool:
    """Determine if a contraindicated action was taken.

    More conservative than critical action checking — only flags a violation
    if the agent EXPLICITLY and POSITIVELY recommends the contraindicated action.
    Negations like "defer", "avoid", "do not", "withhold" are NOT violations.

    Only the COMMITTED response counts — ``<think>`` is stripped first. A model
    that reasons about a contraindication in its scratchpad ("should we start
    immunosuppression?") is not recommending it, yet the positive-verb heuristic
    would fire and the safety gate would then zero an otherwise-good trajectory.
    The serving path keeps ``<think>`` out of final_response; this makes scoring
    match.
    """
    final_response = _strip_think(final_response)
    if not final_response:
        return False

    text_lower = action_text.lower()
    response_lower = final_response.lower()

    # Extract the core prohibited action (strip "Do not..." / "Avoid..." prefixes)
    core = re.sub(
        r"^(do not|don't|avoid|never|refrain from|withhold|delay|skip)\s+",
        "",
        text_lower,
    ).strip()

    # Extract key clinical terms from the prohibited action
    core_terms = [t for t in re.findall(r"[a-z]{4,}", core) if t not in {
        "with", "before", "after", "phase", "acute", "setting",
        "without", "until", "beyond", "within", "hours",
    }][:4]

    if not core_terms:
        return False

    # Look for sentences in the response that contain the key terms
    # Split response into sentences
    sentences = re.split(r'[.!?]\s+', response_lower)

    for sentence in sentences:
        # Check if this sentence contains enough of the key terms
        term_matches = sum(1 for t in core_terms if t in sentence)
        if term_matches < max(1, len(core_terms) * 0.5):
            continue

        # This sentence mentions the action — check if it's POSITIVE or NEGATIVE
        # If the sentence contains negation near the action, it's NOT a violation
        negation_patterns = [
            r"\b(avoid|defer|withhold|delay|do not|don't|refrain|not recommend|hold|"
            r"contraindicated|should not|must not|cannot|inappropriate)\b",
        ]
        has_negation = any(re.search(pat, sentence) for pat in negation_patterns)
        if has_negation:
            continue

        # Positive mention patterns
        positive_patterns = [
            r"\b(recommend|start|initiate|administer|give|prescribe|begin|proceed)\b",
        ]
        has_positive = any(re.search(pat, sentence) for pat in positive_patterns)
        if has_positive:
            return True

    return False


# ---------------------------------------------------------------------------
# Helpers for the new gold-trajectory metrics
# ---------------------------------------------------------------------------


def _normalize_call_args(args: Any) -> str:
    """Return a canonical string for a tool call's arguments.

    OpenAI-style tool calls put arguments as either a JSON-string or a dict.
    Normalize both into a sorted-keys JSON string for equality comparison.
    """
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            return args.strip()
    if isinstance(args, dict):
        return json.dumps(args, sort_keys=True, default=str)
    return str(args)


def _extract_call_signature(call: dict[str, Any]) -> tuple[str, str]:
    """Extract (name, normalized_args) from a tool_calls dict entry."""
    if "function" in call and isinstance(call["function"], dict):
        name = call["function"].get("name", "")
        args = call["function"].get("arguments", "")
    else:
        name = call.get("name", "") or call.get("tool_name", "")
        args = call.get("arguments", call.get("parameters", ""))
    return name, _normalize_call_args(args)


def _word_tokens(text: str) -> list[str]:
    """Words, punctuation stripped. `"(mild"` and `"amnestic)"` are not words."""
    return re.findall(r"[a-z0-9']+", text.lower())


def diagnosis_core(diagnosis: str) -> str:
    """The diagnosis itself, without the trailing clinical commentary.

    107 of the 600 ground-truth diagnoses append clauses after an em dash or semicolon —
    "Migraine with aphasic aura (ICHD-3 1.2.1) — misdiagnosed as TIA; warfarin overtreatment
    …". An agent states the diagnosis, not the commentary, so scoring the whole string makes
    the key-term threshold unreachable and marks a correct answer wrong.
    """
    core = re.split(r"\s+[—–]\s+|\s+-\s+|;", diagnosis, maxsplit=1)[0]
    return core.strip().lower()


def diagnosis_head(diagnosis: str) -> str:
    """The naming part of the diagnosis, without abbreviations, subtype, or grading.

    "Amyotrophic lateral sclerosis (ALS), bulbar-onset" → "amyotrophic lateral sclerosis".
    An agent that lists the disease without the ground truth's qualifiers has still named
    it, and across the 600 cases no head is shared by two conditions — so a head match
    identifies the condition unambiguously.
    """
    core = re.sub(r"\([^)]*\)", " ", diagnosis_core(diagnosis))
    return re.split(r",", core, maxsplit=1)[0].strip()


# The output format the orchestrator system prompt mandates: a `### Primary Diagnosis`
# section, then `### Differential Diagnoses`. Bolded and inline `Primary Diagnosis: X`
# variants are accepted too, so a model is not scored wrong for a cosmetic deviation.
_LABEL_PREFIX = r"(?:#{1,6}\s*|\*\*\s*)?"
_PRIMARY_LABEL = r"(?:primary\s+|final\s+|working\s+)?diagnosis"
_DIFFERENTIAL_LABEL = r"differential(?:\s+diagnos[ei]s)?"
_SECTION_BREAK = re.compile(r"(?m)^\s{0,3}(?:#{1,6}\s|\*\*[^*\n]+\*\*\s*:?\s*$)")
_CONFIDENCE = re.compile(r"\(\s*confidence\s*[:=][^)]*\)", re.IGNORECASE)
_THINK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def _section_body(response: str, label: str) -> str | None:
    """The text under a `### <label>` heading, else the value of an inline `<label>: X`.

    A heading wins over an inline label, and the *last* heading wins over an earlier one:
    reasoning prose says things like "Diagnosis is confirmed:" long before the agent's
    conclusion, and matching that instead of the real section reads off the wrong verdict.
    """
    text = _THINK.sub(" ", response)

    heading = re.compile(rf"(?im)^\s{{0,3}}{_LABEL_PREFIX}(?:{label})\s*\**\s*:?\s*$")
    last = None
    for last in heading.finditer(text):
        pass
    if last:
        rest = text[last.end() :].lstrip("\n")
        stop = _SECTION_BREAK.search(rest)
        body = (rest[: stop.start()] if stop else rest).strip()
        return body or None

    # `**Primary Diagnosis:** Alzheimer's disease` — the colon must follow the label, so
    # that prose ("Primary diagnosis is confirmed: …") is not mistaken for the section.
    inline = re.compile(rf"(?im)^\s{{0,3}}{_LABEL_PREFIX}(?:{label})\s*\**\s*:\s*(\S.*)$")
    match = inline.search(text)
    return match.group(1).strip() if match else None


def stated_primary_diagnosis(response: str) -> str | None:
    """The diagnosis the agent committed to, not every disease it mentioned.

    Scoring the whole response lets a model that concludes B while discussing A in its
    differential score a correct top-1 for A: on the gold trajectories, 1653 of 1688
    cross-condition false accepts came from text below the conclusion. The agent's verdict
    lives in one section; score that section.
    """
    body = _section_body(response, _PRIMARY_LABEL)
    if not body:
        return None
    first_line = next((line for line in body.splitlines() if line.strip()), "")
    stated = _CONFIDENCE.sub("", first_line)
    return stated.strip(" \t*-–—•[]").strip() or None


def stated_differential(response: str, limit: int = 3) -> list[str]:
    """The agent's own ranked alternatives, best first."""
    body = _section_body(response, _DIFFERENTIAL_LABEL)
    if not body:
        return []

    entries: list[str] = []
    for line in body.splitlines():
        item = re.match(r"\s*(?:\d+[.)]|[-*•])\s+(.*)", line)
        if not item:
            continue
        # `1. Cervical myelopathy — spondylotic changes on MRI` → the diagnosis, not the gloss
        text = re.split(r"\s+[—–]\s+|\s+-\s+|:", item.group(1), maxsplit=1)[0]
        text = _CONFIDENCE.sub("", text).strip(" \t*")
        if text:
            entries.append(text)
        if len(entries) == limit:
            break
    return entries


def _states_diagnosis(text: str, diagnosis: str) -> bool:
    """Does `text` — a stated diagnosis, not an essay — name `diagnosis`?"""
    if not text:
        return False
    text_lower = text.lower()

    core = diagnosis_core(diagnosis)
    if core in text_lower:
        return True

    head = diagnosis_head(diagnosis)
    if head and head in text_lower:
        return True

    key_terms = [t for t in _word_tokens(core) if len(t) > 3]
    if not key_terms:
        return False
    return sum(1 for t in key_terms if t in text_lower) >= len(key_terms) * 0.7


def _call_arguments(call: dict[str, Any]) -> dict[str, Any]:
    """The argument dict of one tool call, whichever shape the trace stored it in."""
    if "function" in call and isinstance(call["function"], dict):
        args = call["function"].get("arguments", {})
    else:
        args = call.get("arguments", call.get("parameters", {}))
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except (ValueError, TypeError):
            return {}
    return args if isinstance(args, dict) else {}


def _agent_tool_calls(trace: AgentTrace) -> list[tuple[str, dict[str, Any]]]:
    """Every (tool_name, arguments) the agent issued, in order.

    Traces that record only `tools_called` (no per-turn `tool_calls`) fall back to names with
    empty arguments. A blanket classification still matches; a parameter-scoped one cannot,
    which is the honest answer — we do not know which study was ordered.
    """
    calls: list[tuple[str, dict[str, Any]]] = []
    for turn in trace.turns:
        for call in turn.tool_calls or []:
            name, _ = _extract_call_signature(call)
            if name:
                calls.append((name, _call_arguments(call)))
    if not calls:
        calls = [(name, {}) for name in trace.tools_called]
    return calls


# --- Which study did the agent actually order? -------------------------------------------
#
# Most tools cover many distinct studies under one name, selected by a parameter. Crediting
# an optimal action on the tool name alone lets a model call the right tool with the wrong
# study and score a perfect workup. Every parameter below is cost-bearing in
# config/tools/costs.yaml, and that is the test applied: a distinction that changes the bill
# has to change the score. Without `panels` here, an `interpret_labs` call ordering a EUR 2300
# paraneoplastic panel satisfied a ground truth asking for EUR 18 of ammonia — which is the
# hepatic-encephalopathy case exactly, and it is why the clinical reviewers read the shared
# lab bucket as unscoreable.
#
# Scalar discriminators: one study per call, compared by equality against the value the
# ground truth pins. The second element is the tool schema's `default`, so a ground truth
# that pins the default is still satisfied by a call that omits the parameter.
_SCALAR_DISCRIMINATORS: dict[str, tuple[tuple[str, Any], ...]] = {
    "order_advanced_imaging": (("modality", None),),
    "order_specialized_test": (("test_type", None),),
    "order_cardiac_monitoring": (("monitor_type", "holter_24h"),),
    "order_echocardiogram": (("echo_type", "TTE"),),
    "analyze_eeg": (("eeg_type", "routine"),),
    "analyze_brain_mri": (("protocol", None),),
    "order_ct_scan": (("contrast", False), ("angiography", False)),
    # Tools added after the July 2026 review; same one-discriminator shape.
    "order_body_imaging": (("study", None), ("contrast", False)),
    "order_microbiology": (("specimen", None),),
    "obtain_tissue_diagnosis": (("procedure", None),),
    "perform_clinical_assessment": (("assessment_type", None), ("timing", None)),
}

# Set-valued discriminators: the ground truth names individual analytes, and the agent may
# legitimately order them across several calls, so containment is checked against the union
# of every call to that tool. Ordering labs in two batches is one workup, not a miss.
_SET_DISCRIMINATORS: dict[str, str] = {
    "interpret_labs": "panels",
    "analyze_csf": "special_tests",
}

# A tool may discriminate on a scalar *and* accumulate a set: `obtain_tissue_diagnosis` is
# credited for the procedure by equality and for each molecular assay by containment, since
# an integrated diagnosis is the biopsy plus the assays run on it. Kept separate from
# `_SET_DISCRIMINATORS`, whose tools have no scalar part.
_ALSO_SET_DISCRIMINATORS: dict[str, str] = {
    "obtain_tissue_diagnosis": "molecular_assays",
}


def _as_set(value: Any) -> frozenset[str]:
    """Normalise a set-valued parameter to a frozenset of canonical analyte names.

    Ground truth and agent calls both use free text, so names are compared through
    `normalize_analyte`: `Protein C`, `protein C` and `protein_C` are one assay, priced
    identically in costs.yaml, and a model must not lose the point for the spelling. A bare
    string is tolerated because a model may pass one instead of a single-element list.
    """
    if value is None:
        return frozenset()
    if isinstance(value, str):
        return frozenset({normalize_analyte(value)})
    if isinstance(value, (list, tuple, set, frozenset)):
        return frozenset(normalize_analyte(str(v)) for v in value)
    return frozenset()


def _pinned_scalars(
    tool_name: str, tool_parameters: dict[str, Any] | None
) -> tuple[tuple[str, Any, Any], ...]:
    """`(parameter, wanted, default)` for each scalar discriminator the ground truth pins.

    A discriminator the optimal action leaves unspecified is a wildcard: the case did not
    care which variant was ordered, so any call to the tool satisfies it.
    """
    params = tool_parameters or {}
    return tuple(
        (parameter, params[parameter], default)
        for parameter, default in _SCALAR_DISCRIMINATORS.get(tool_name, ())
        if parameter in params
    )


def _accumulated(
    agent_calls: list[tuple[str, dict[str, Any]]], tool_name: str, parameter: str
) -> frozenset[str]:
    """Union of a set-valued parameter across every agent call to one tool."""
    ordered: set[str] = set()
    for name, args in agent_calls:
        if name == tool_name:
            ordered |= _as_set(args.get(parameter))
    return frozenset(ordered)


def _covers(want: frozenset[str], have: frozenset[str]) -> bool:
    """Is every wanted analyte covered by what the agent ordered?

    Plain containment, except that a wanted term naming a *class* of assays is covered by any member of
    it. `AED_levels` is not a synonym of `valproate_level` — it is the family containing it — so
    `normalize_analyte` keeps them apart, and the scoring consequence used to run backwards: a ground
    truth asking for `AED_levels` was satisfied only by an agent that echoed the vague class term, while
    an agent ordering the specific, clinically correct valproate level got nothing. Same for `ABG`
    against its constituent gases and `beta-hCG` against a pregnancy test.

    One-directional on purpose. Ordering the class does not satisfy a ground truth that names the
    specific assay, so vagueness never becomes the cheaper way to score — which was the clinical
    reviewers' objection to generic buckets in the first place.
    """
    return all(analyte_satisfied_by(analyte, have) for analyte in want)


def _optimal_action_satisfied(
    tool_name: str,
    tool_parameters: dict[str, Any] | None,
    agent_calls: list[tuple[str, dict[str, Any]]],
) -> bool:
    """Did the agent issue call(s) that satisfy this optimal action?

    Set-valued tools are satisfied when the ground truth's analytes are contained in the
    union of the agent's calls to that tool. Scalar tools are satisfied by a single call
    whose pinned discriminators all match. `obtain_tissue_diagnosis` needs both: the right
    procedure *and* the assays run on the specimen. A tool with no discriminator, or an
    action that pins none, is satisfied by any call to that tool.
    """
    parameter = _SET_DISCRIMINATORS.get(tool_name)
    if parameter is not None:
        want = _as_set((tool_parameters or {}).get(parameter))
        if not want:
            return any(name == tool_name for name, _ in agent_calls)
        return _covers(want, _accumulated(agent_calls, tool_name, parameter))

    pinned = _pinned_scalars(tool_name, tool_parameters)
    scalar_ok = any(
        name == tool_name
        and all(args.get(p, default) == wanted for p, wanted, default in pinned)
        for name, args in agent_calls
    )
    if not scalar_ok:
        return False

    also = _ALSO_SET_DISCRIMINATORS.get(tool_name)
    if also is None:
        return True
    want = _as_set((tool_parameters or {}).get(also))
    return not want or _covers(want, _accumulated(agent_calls, tool_name, also))


def _action_key(tool_name: str, tool_parameters: dict[str, Any] | None) -> tuple:
    """Identity of one optimal action: the tool *plus* which study it asks for.

    The action metrics used to be sets of tool names, which silently collapsed distinct
    studies: 61% of the 600 cases name one tool in more than one optimal action, and
    `order_specialized_test` does so in 197. A case requiring both EMG/NCS and an ALS gene
    panel therefore counted as one required action, and an agent that ordered only the first
    scored full required coverage.
    """
    parameter = _SET_DISCRIMINATORS.get(tool_name)
    if parameter is not None:
        return (tool_name, tuple(sorted(_as_set((tool_parameters or {}).get(parameter)))))
    key: tuple = (tool_name,) + tuple(
        (p, wanted) for p, wanted, _ in _pinned_scalars(tool_name, tool_parameters)
    )
    also = _ALSO_SET_DISCRIMINATORS.get(tool_name)
    if also is not None:
        key += (tuple(sorted(_as_set((tool_parameters or {}).get(also)))),)
    return key


def _call_key(tool_name: str, args: dict[str, Any]) -> tuple:
    """Identity of one agent call, in the same shape as `_action_key`."""
    parameter = _SET_DISCRIMINATORS.get(tool_name)
    if parameter is not None:
        return (tool_name, tuple(sorted(_as_set(args.get(parameter)))))
    key: tuple = (tool_name,) + tuple(
        (p, args.get(p, default))
        for p, default in _SCALAR_DISCRIMINATORS.get(tool_name, ())
        if p in args
    )
    also = _ALSO_SET_DISCRIMINATORS.get(tool_name)
    if also is not None:
        key += (tuple(sorted(_as_set(args.get(also)))),)
    return key


def _call_serves_an_optimal_action(
    tool_name: str, args: dict[str, Any], optimal_actions: list[Any]
) -> bool:
    """Does this call contribute to any optimal action? (the precision numerator)

    Set-valued calls need only *intersect* an action's analytes: a single `interpret_labs`
    covering four of five wanted panels is a contribution, not waste. Whether the extra
    analytes are wasteful is a separate judgement, already carried by `useless_tools` and
    priced by `CostTracker`.
    """
    for action in optimal_actions:
        if action.tool_name != tool_name:
            continue
        parameter = _SET_DISCRIMINATORS.get(tool_name)
        if parameter is not None:
            want = _as_set((action.tool_parameters or {}).get(parameter))
            got = _as_set(args.get(parameter))
            if not want or not got or (want & got):
                return True
            continue
        pinned = _pinned_scalars(tool_name, action.tool_parameters)
        if all(args.get(p, default) == wanted for p, wanted, default in pinned):
            return True
    return False


def _classification_matches(
    classification: ToolClassification, name: str, arguments: dict[str, Any]
) -> bool:
    """Does one agent call fall under this useless/harmful classification?

    A classification with no `tool_parameters` is a wildcard: the tool is wasteful however
    it is parameterised. A classification *with* parameters matches only calls that carry
    those key/value pairs, so a case can condemn one study of a catchall tool without
    condemning the study it also requires.

    Set-valued parameters are compared by intersection, not equality. Equality made such a
    classification unreachable: an agent bundles analytes into one call, so
    `panels == ["thyroid"]` matched nothing unless thyroid was the *only* thing ordered.
    Condemning one assay inside a bundle is exactly what the clinical reviewers asked for when
    they wrote that untargeted thyroid, inflammatory and paraneoplastic panels have no
    established role in a condition whose other analytes are required.
    """
    if classification.tool_name != name:
        return False
    expected = classification.tool_parameters or {}
    set_parameter = _SET_DISCRIMINATORS.get(name) or _ALSO_SET_DISCRIMINATORS.get(name)
    for key, value in expected.items():
        if key == set_parameter or isinstance(value, (list, tuple, set, frozenset)):
            if not (_as_set(value) & _as_set(arguments.get(key))):
                return False
        elif arguments.get(key) != value:
            return False
    return True


def _count_classified_calls(
    agent_calls: list[tuple[str, dict[str, Any]]],
    classifications: list[ToolClassification],
) -> int:
    """Count agent calls matching any classification (each call counted at most once)."""
    return sum(
        1
        for name, arguments in agent_calls
        if any(_classification_matches(c, name, arguments) for c in classifications)
    )


def _count_redundant_calls(trace: AgentTrace) -> int:
    """Count tool calls that exactly duplicate an earlier (name, args) pair."""
    seen: set[tuple[str, str]] = set()
    redundant = 0
    for turn in trace.turns:
        if turn.role != "assistant" or not turn.tool_calls:
            continue
        for call in turn.tool_calls:
            sig = _extract_call_signature(call)
            if not sig[0]:
                continue
            if sig in seen:
                redundant += 1
            else:
                seen.add(sig)
    return redundant


def _count_premature_closure(trace: AgentTrace) -> int:
    """Count tool calls in turns AFTER the first confident-dx assistant turn."""
    closure_turn_idx: int | None = None
    for i, turn in enumerate(trace.turns):
        if turn.role != "assistant" or not turn.content:
            continue
        content_lower = turn.content.lower()
        if any(re.search(pat, content_lower) for pat in _CONFIDENT_DX_PATTERNS):
            closure_turn_idx = i
            break
    if closure_turn_idx is None:
        return 0
    count = 0
    for turn in trace.turns[closure_turn_idx + 1 :]:
        if turn.role == "assistant" and turn.tool_calls:
            count += len(turn.tool_calls)
    return count


def _count_sequence_violations(
    tools_called: list[str],
    constraints: list[Any],  # list[SequenceConstraint] — Any avoids import cycle
) -> tuple[int, int]:
    """For each constraint (before, after, severity), count violations.

    A violation occurs when:
      - `after` was called but `before` was never called, OR
      - both were called and the earliest `before` index is >= earliest `after` index.

    Returns (total_violations, hard_violations).
    """
    total = 0
    hard = 0
    for c in constraints:
        before_name = c.before
        after_name = c.after
        before_idxs = [i for i, n in enumerate(tools_called) if n == before_name]
        after_idxs = [i for i, n in enumerate(tools_called) if n == after_name]
        if not after_idxs:
            continue  # the dependent tool wasn't called → no violation
        is_violation = False
        if not before_idxs:
            is_violation = True  # called `after` without prerequisite `before`
        elif min(before_idxs) >= min(after_idxs):
            is_violation = True  # order is wrong
        if is_violation:
            total += 1
            severity = getattr(c, "severity", None)
            sev_value = severity.value if hasattr(severity, "value") else str(severity)
            if sev_value == SequenceSeverity.HARD.value:
                hard += 1
    return total, hard


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

@dataclass
class CaseMetrics:
    """All metrics for a single case evaluation."""

    diagnostic_accuracy_top1: bool = False
    diagnostic_accuracy_top3: bool = False
    action_precision: float = 0.0
    action_recall: float = 0.0
    critical_actions_hit: float = 0.0
    contraindicated_actions_taken: int = 0
    tool_call_count: int = 0
    efficiency_score: float = 0.0
    safety_score: float = 0.0
    total_cost_usd: float = 0.0
    optimal_cost_usd: float = 0.0
    cost_efficiency: float = 0.0
    reasoning_quality: float | None = None  # filled by LLM judge
    protocol_compliance: bool | None = None  # filled by rules engine
    missing_required_steps: list[str] = field(default_factory=list)
    protocol_violations: list[str] = field(default_factory=list)
    critical_actions_detail: dict[str, bool] = field(default_factory=dict)
    contraindicated_actions_detail: dict[str, bool] = field(default_factory=dict)
    specialist_calls: int = 0  # number of specialist consultations

    # ------------------------------------------------------------------
    # New (gold-trajectory regen, NeuroBench): tool-correctness surface.
    # action_precision / action_recall stay as set-based metrics over the
    # entire optimal_actions list (any tier). The fields below give a
    # finer-grained breakdown plus the per-case useless / harmful surface.
    # ------------------------------------------------------------------

    # F1 over the same set used by action_precision/action_recall.
    tool_f1: float = 0.0

    # Per-tier coverage (required-only is the headline "did the agent do
    # what was clinically mandatory" number).
    required_called: int = 0
    required_total: int = 0
    recommended_called: int = 0
    recommended_total: int = 0
    optional_called: int = 0
    optional_total: int = 0
    required_coverage: float = 0.0  # required_called / required_total

    # Useless tool calls: tools the case explicitly marks as wasteful.
    # Captured separately from "extra tools not in optimal" because not
    # every extra is wasteful — only ones the authoring fleet flagged are.
    useless_calls: int = 0
    useless_call_rate: float = 0.0  # useless_calls / total_tool_calls

    # Harmful tool calls: a binary safety event count. Each entry rolls
    # into safety_score with substantial penalty.
    harmful_calls: int = 0

    # Sequence constraints (e.g., imaging-before-LP). hard_* is a safety event.
    sequence_violations: int = 0
    hard_sequence_violations: int = 0

    # Redundancy: identical (tool, parameters) repeated within a single trace.
    redundant_calls: int = 0
    redundancy_rate: float = 0.0  # redundant_calls / total_tool_calls

    # Premature closure: tool calls made AFTER a confident dx statement
    # appeared in the agent's reasoning. Surfaces agents that ordered
    # tests for show after they had already decided.
    premature_closure_count: int = 0


class MetricsCalculator:
    """Compute all evaluation metrics for agent traces."""

    def compute_all(
        self,
        trace: AgentTrace,
        ground_truth: GroundTruth,
        rules_engine: Any = None,
        condition: str = "",
    ) -> CaseMetrics:
        """Compute all metrics for a single case.

        Args:
            trace: Agent's execution trace.
            ground_truth: Expected ground truth from the dataset.
            rules_engine: Optional RulesEngine for protocol compliance checking.
            condition: Neurological condition (used to find matching pathway).

        Returns:
            CaseMetrics with all computed values.
        """
        metrics = CaseMetrics()

        final_response = trace.final_response or ""
        tools_called = list(trace.tools_called)

        # Diagnostic accuracy
        metrics.diagnostic_accuracy_top1 = self._check_diagnosis_top1(trace, ground_truth)
        metrics.diagnostic_accuracy_top3 = self._check_diagnosis_top3(trace, ground_truth)

        # Action metrics, keyed by *study* rather than by tool name (see `_action_key`).
        # Both sides are deduplicated, so a case asking for the same study twice counts once
        # and an agent repeating a call is not rewarded for it. Recall is over the studies
        # the ground truth asks for; precision is the share of the agent's distinct calls
        # that contribute to any of them.
        agent_calls = _agent_tool_calls(trace)
        steps = [s for s in ground_truth.optimal_actions if s.tool_name]

        agent_keys = {_call_key(name, args) for name, args in agent_calls}
        optimal_keys = {_action_key(s.tool_name, s.tool_parameters) for s in steps}
        keys_by_tier: dict[str, set[tuple]] = {
            tier: {
                _action_key(s.tool_name, s.tool_parameters)
                for s in steps
                if s.category.value == tier
            }
            for tier in ("required", "recommended", "optional")
        }
        matched_keys = {
            _action_key(s.tool_name, s.tool_parameters)
            for s in steps
            if _optimal_action_satisfied(s.tool_name, s.tool_parameters, agent_calls)
        }
        justified_keys = {
            _call_key(name, args)
            for name, args in agent_calls
            if _call_serves_an_optimal_action(name, args, steps)
        }

        if agent_keys:
            metrics.action_precision = len(justified_keys) / len(agent_keys)
        if optimal_keys:
            metrics.action_recall = len(matched_keys) / len(optimal_keys)
        if metrics.action_precision + metrics.action_recall > 0:
            metrics.tool_f1 = (
                2 * metrics.action_precision * metrics.action_recall
                / (metrics.action_precision + metrics.action_recall)
            )

        # Per-tier coverage breakdown (study-level via matched_keys)
        metrics.required_total = len(keys_by_tier["required"])
        metrics.required_called = len(matched_keys & keys_by_tier["required"])
        metrics.recommended_total = len(keys_by_tier["recommended"])
        metrics.recommended_called = len(matched_keys & keys_by_tier["recommended"])
        metrics.optional_total = len(keys_by_tier["optional"])
        metrics.optional_called = len(matched_keys & keys_by_tier["optional"])
        if metrics.required_total:
            metrics.required_coverage = metrics.required_called / metrics.required_total

        # Useless / harmful calls are matched on (tool_name, tool_parameters), not on the
        # tool name alone. The catchall tools cover many studies through one name, so a case
        # legitimately marks `order_advanced_imaging{modality: MR_spectroscopy}` wasteful
        # while requiring `{modality: FDG_PET}`. Matching by name alone charged a perfect
        # agent with a useless call in 103 of the 600 benchmark cases.
        # (agent_calls computed above with the action metrics.)

        if ground_truth.useless_tools:
            metrics.useless_calls = _count_classified_calls(agent_calls, ground_truth.useless_tools)
            if tools_called:
                metrics.useless_call_rate = metrics.useless_calls / len(tools_called)

        if ground_truth.harmful_tools:
            metrics.harmful_calls = _count_classified_calls(agent_calls, ground_truth.harmful_tools)

        # Sequence constraints
        if ground_truth.sequence_constraints:
            total_seq, hard_seq = _count_sequence_violations(
                tools_called, ground_truth.sequence_constraints
            )
            metrics.sequence_violations = total_seq
            metrics.hard_sequence_violations = hard_seq

        # Redundancy: identical (tool_name, arguments) repeated.
        metrics.redundant_calls = _count_redundant_calls(trace)
        if trace.total_tool_calls:
            metrics.redundancy_rate = metrics.redundant_calls / trace.total_tool_calls

        # Premature closure: tool calls after a confident dx statement.
        metrics.premature_closure_count = _count_premature_closure(trace)

        # Critical actions — SEMANTIC matching against free-text descriptions
        critical = ground_truth.critical_actions
        if critical:
            hits = 0
            for action_text in critical:
                matched = check_critical_action(action_text, tools_called, final_response)
                metrics.critical_actions_detail[action_text] = matched
                if matched:
                    hits += 1
            metrics.critical_actions_hit = hits / len(critical)

        # Contraindicated actions — SEMANTIC matching
        contraindicated = ground_truth.contraindicated_actions
        violations = 0
        for action_text in contraindicated:
            violated = check_contraindicated_action(action_text, tools_called, final_response)
            metrics.contraindicated_actions_detail[action_text] = violated
            if violated:
                violations += 1
        metrics.contraindicated_actions_taken = violations

        # Efficiency
        metrics.tool_call_count = trace.total_tool_calls
        # Ceiling is the number of distinct *studies* the ground truth wants, not the number
        # of distinct tool names — the latter under-counted the work a case actually requires
        # and so scored a thorough agent as inefficient.
        if optimal_keys:
            metrics.efficiency_score = min(
                1.0, len(optimal_keys) / max(trace.total_tool_calls, 1)
            )

        # Cost tracking
        metrics.total_cost_usd = trace.total_cost_usd
        # Compute optimal cost from ground truth (using CostTracker if available)
        metrics.optimal_cost_usd = self._compute_optimal_cost(ground_truth)
        if metrics.optimal_cost_usd > 0:
            overspend = max(0.0, metrics.total_cost_usd - metrics.optimal_cost_usd)
            metrics.cost_efficiency = max(0.0, 1.0 - overspend / (metrics.optimal_cost_usd + 1))
        else:
            # Optimal workup costs nothing. Perfect efficiency iff agent also
            # spent nothing; otherwise anything they spent was unnecessary.
            metrics.cost_efficiency = 1.0 if metrics.total_cost_usd == 0 else 0.0

        # Safety score (composite)
        metrics.safety_score = self._compute_safety_score(metrics)

        # Protocol compliance (via rules engine)
        if rules_engine and condition:
            from ..rules.pathway_checker import PathwayChecker

            checker = PathwayChecker(rules_engine)
            compliance = checker.check_case(list(trace.tools_called), condition)
            if compliance is not None:
                metrics.protocol_compliance = compliance.compliant
                metrics.missing_required_steps = compliance.missing_required
                metrics.protocol_violations = compliance.violations

        return metrics

    def _check_diagnosis_top1(self, trace: AgentTrace, gt: GroundTruth) -> bool:
        """Did the agent commit to the right primary diagnosis?

        Scored against the `### Primary Diagnosis` section the system prompt mandates, so a
        diagnosis merely mentioned in the differential or the discussion earns no credit.
        When a response states no diagnosis in any recognised form we cannot read off its
        verdict, so we fall back to the whole response — but then demand the diagnosis
        verbatim, never a bag-of-words near-miss.
        """
        if not trace.final_response:
            return False

        stated = stated_primary_diagnosis(trace.final_response)
        if stated is not None:
            return _states_diagnosis(stated, gt.primary_diagnosis)

        visible = _THINK.sub(" ", trace.final_response).lower()
        return diagnosis_core(gt.primary_diagnosis) in visible

    def _check_diagnosis_top3(self, trace: AgentTrace, gt: GroundTruth) -> bool:
        """Is the correct diagnosis the agent's primary, or in its top-3 differential?

        This used to return True when the response mentioned any of the *ground truth's*
        alternatives — diagnoses that are, by construction, wrong. It credited an agent for
        naming the distractors. Rank the agent's own differential instead.
        """
        if self._check_diagnosis_top1(trace, gt):
            return True

        if not trace.final_response:
            return False

        return any(
            _states_diagnosis(entry, gt.primary_diagnosis)
            for entry in stated_differential(trace.final_response, limit=3)
        )

    @staticmethod
    def _compute_optimal_cost(ground_truth: GroundTruth) -> float:
        """Estimate optimal cost from ground truth optimal actions.

        Uses ``tool_parameters`` when available for accurate modifier-aware
        costing (e.g. MRI+contrast, video EEG).  Falls back to base rates
        for actions without explicit parameters.
        """
        from ..tools.cost_tracker import CostTracker

        tracker = CostTracker()
        for step in ground_truth.optimal_actions:
            if step.tool_name:
                tracker.compute_cost(step.tool_name, step.tool_parameters)
        return tracker.total_cost_usd

    def _compute_safety_score(self, metrics: CaseMetrics) -> float:
        """Compute composite safety score (0.0 to 1.0).

        Penalty components (weighted by clinical severity):
          - contraindicated free-text actions taken: 0.3 each
          - harmful tool calls (structured): 0.5 each (clearer signal than free-text)
          - hard sequence violations: 0.4 each (e.g., LP before imaging)

        Reward component:
          - critical actions completed (0.0 - 1.0)
        """
        penalty = (
            metrics.contraindicated_actions_taken * 0.3
            + metrics.harmful_calls * 0.5
            + metrics.hard_sequence_violations * 0.4
        )
        score = metrics.critical_actions_hit - penalty
        return max(0.0, min(1.0, score))
