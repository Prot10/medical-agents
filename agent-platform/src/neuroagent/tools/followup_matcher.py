"""Deterministic resolver for a case's conditional (follow-up) tool outputs.

A NeuroBench case stores an *initial* output per tool (what the first, bare order
returns) plus a list of ``FollowUpToolOutput`` records. Each follow-up carries a
``trigger_action`` slug (e.g. ``request_amyloid_pet``, ``request_csf_nfl``) that
names the specific *re-order* it is meant to answer. The historical MockServer
ignored the trigger entirely — it returned the initial output on every call and,
when it did reach the follow-up tier, served the FIRST follow-up for the tool
regardless of what the agent asked. That shadowed ~45% of authored follow-ups.

This module implements the single matching rule used by the executable patient
runtime so every policy profile resolves follow-ups identically.

Matching, in words:

  * Tokenize the follow-up's ``trigger_action`` slug (split on ``_``, drop a
    leading request/check/order/... verb and generic stopwords).
  * Tokenize the agent call's PARAMETER VALUES (every value stringified,
    lowercased, split on non-alphanumerics) plus the ``tool_name``.
  * A follow-up is a *specific-re-order* candidate when its trigger shares at
    least one MEANINGFUL token with the call — meaningful meaning: not a generic
    study word (``panel``, ``test``, ``level``…), not an imaging-family qualifier
    that fails to identify a specific study on its own (``pet``, ``ct``, ``mri``…),
    and not merely a token already present in the tool name.
  * Among specific candidates, pick the highest token overlap; ties broken by
    (a) preferring a trigger not yet served this session so distinct re-orders
    escalate through distinct follow-ups, then (b) declaration order.
  * The called tool's own enum terms (``continuous_icu``, ``lumbar_puncture``) are
    study identities, and their tokens count only for the term the call names
    (October 2026 review, SE CENTRAL 4):
      - a token of a term the call does NOT name never counts. Free text naming
        another study of the same tool ("routine and sleep-deprived EEGs were
        non-diagnostic" on an ambulatory order) no longer routes the call to that
        study's follow-up;
      - a token of a term the call names only through the schema default (a CSF
        order without ``source`` is a lumbar puncture) counts only when the
        trigger names the whole term, so ``request_extended_lumbar_drainage`` does
        not answer a tap test on "lumbar";
      - a token of a term the call names explicitly counts, unless the stored
        initial output already IS that study (its own discriminator field says so):
        then only a trigger naming the whole term overrides it. That is the SE
        defect, ``request_continuous_eeg_monitoring`` capturing the index
        ``continuous_icu`` order. Since 24 Oct 2026 EEG reports carry ``eeg_type``
        and EEG is routed by the MockServer's discriminator ahead of this matcher,
        which serves the index recording to the first order of its type.
  * ``accepts`` (the MockServer's "does this stored report describe the study
    ordered") filters candidates BEFORE the choice. Choosing first and checking
    after let a sibling that loses the check win a tie, and the call fell to the
    library while the right follow-up sat in the case (SE-M05).

Precedence (see ``resolve_followup``) — a specific re-order OVERRIDES the stale
initial output, but a bare first call to a tool still returns its INITIAL output.
"""

from __future__ import annotations

import re
from typing import Any, Callable, Sequence

# A follow-up's ``.output`` is a Pydantic model; we only touch ``.tool_name`` and
# ``.trigger_action`` here, so type it structurally to avoid a schema import cycle.
try:  # pragma: no cover - import convenience only
    from neuroagent_schemas.case import FollowUpToolOutput
except Exception:  # pragma: no cover
    FollowUpToolOutput = Any  # type: ignore[misc,assignment]


_SPLIT = re.compile(r"[^a-z0-9]+")

# Leading verbs stripped from a trigger slug (``request_amyloid_pet`` -> amyloid_pet).
_VERBS = {
    "request", "check", "order", "get", "search", "analyze", "perform",
    "obtain", "assess", "evaluate", "measure", "send", "run", "repeat",
}

# Dropped from every token set — connective noise.
_STOP = {"a", "an", "and", "for", "of", "or", "the", "to", "with", "in", "on", "at", "by", "per", "vs"}

# Tokens that do NOT identify a specific study on their own: generic study words
# plus imaging/assay family qualifiers (a call for ``amyloid_PET`` must not match a
# ``request_fdg_pet`` follow-up on the shared ``pet`` token alone).
_GENERIC = {
    "test", "testing", "tests", "panel", "panels", "level", "levels", "study",
    "studies", "screen", "screening", "workup", "evaluation", "assessment",
    "analysis", "profile", "status", "review", "scan", "scans", "imaging",
    "monitor", "monitoring", "function", "blood", "serum", "drug", "interaction",
    "interactions", "patient", "clinical", "pet", "ct", "mri", "mr", "ultrasound",
    "xray", "antibody", "antibodies", "biomarker", "biomarkers", "repeat", "repeated",
    "baseline", "followup", "follow",
    # `anti` is the prefix of every antibody name and identifies none of them. While it counted as
    # meaningful, MG-RS11's required myasthenia antibody order — spelled
    # `[anti_AChR, anti_MuSK, anti_LRP4, TSH]` — matched `request_anti_gq1b_miller_fisher` on that
    # token alone and was answered with the Miller-Fisher ganglioside panel, a different disease's
    # antibody. `antibody`/`antibodies` were already here for the same reason.
    "anti",
}

# Expand common abbreviations so a slug token can match a spelled-out parameter
# value (and vice versa).
_ALIAS = {
    "lp": ["lumbar", "puncture"],
    "oct": ["optical", "coherence", "tomography"],
    "dsa": ["digital", "subtraction", "angiography"],
    "tcd": ["transcranial", "doppler"],
    "cta": ["ct", "angiography"],
    "mra": ["mr", "angiography"],
    "mrv": ["mr", "venography"],
    "nfl": ["neurofilament"],
    "pft": ["pulmonary"],
    "psg": ["polysomnography"],
    "emg": ["electromyography"],
    "ncs": ["nerve", "conduction"],
    "vep": ["visual", "evoked", "potential"],
    "ssep": ["somatosensory", "evoked", "potential"],
    "baep": ["brainstem", "auditory", "evoked", "potential"],
}


def _tokenize(text: Any) -> set[str]:
    toks = [t for t in _SPLIT.split(str(text).lower()) if t and len(t) >= 2 and t not in _STOP]
    out = list(toks)
    for t in toks:
        out += _ALIAS.get(t, [])
    return set(out)


def _trigger_tokens(trigger_action: str) -> set[str]:
    parts = [t for t in _SPLIT.split(trigger_action.lower()) if t]
    if len(parts) > 1 and parts[0] in _VERBS:
        parts = parts[1:]
    return _tokenize("_".join(parts))


def _call_tokens(tool_name: str, parameters: dict[str, Any] | None) -> set[str]:
    """Tokens identifying the study a call asks for.

    Parameter *values* carry that identity for every tool but one. `order_ct_scan` names its study
    with flags — `{"contrast": True, "angiography": True}` IS the CT angiogram — and a flag's value
    stringifies to `"true"`, which identifies nothing. So a call for a CTA produced the token set
    `{"true", "ct", "order", "scan"}` while the follow-up authored to answer it carried the trigger
    `request_ct_angiography` (`{"ct", "angiography"}`), they shared no meaningful token, and the
    stored CTA report was unreachable by the only call that names it: 54 required CT-angiography
    actions across ischaemic stroke and subarachnoid haemorrhage were answered with the
    non-contrast CT, whose own `angiography_findings` is null. Both the scorer and the cost model
    treat angiography as a distinct study (`_SCALAR_DISCRIMINATORS`, +184 EUR); only the simulator
    did not.

    For a boolean flag the study identity is the parameter *key*, so a true flag contributes its
    name. A false flag contributes nothing on purpose: `angiography=False` asserts this is NOT the
    angiogram, and letting it match would hand the CTA report to a plain-CT order.
    """
    values: list[str] = []

    def walk(v: Any) -> None:
        if isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, (list, tuple, set)):
            for x in v:
                walk(x)
        elif v is not None:
            values.append(str(v))

    walk(parameters or {})
    flags = [key for key, value in (parameters or {}).items() if value is True]
    return _tokenize(" ".join([*values, *flags, tool_name]))


def _tok_match(a: str, b: str) -> bool:
    """Exact, or a length>=4 prefix relation (so ``neurofilament`` ~ ``neurofilaments``)."""
    return a == b or (len(a) >= 4 and len(b) >= 4 and (a.startswith(b) or b.startswith(a)))


def _distinctive(tokens: set[str], own: set[str]) -> set[str]:
    return {t for t in tokens if t not in _GENERIC and not any(_tok_match(t, o) for o in own)}


def _enum_sets(
    tool_name: str,
    agent_parameters: dict[str, Any] | None,
    enum_terms: Sequence[str],
    implied_terms: Sequence[str] = (),
    index_terms: Sequence[str] = (),
) -> tuple[set[str], list[tuple[set[str], bool]]]:
    """The distinctive tokens of the tool's enum terms, and the terms this call names.

    A term's distinctive tokens are the ones that are neither generic nor the tool's own name
    (`amyloid_PET` -> {amyloid}; `continuous_icu` -> {continuous, icu}). A term is *called*
    when a scalar parameter value of this call is that term, or when it is the default of a
    parameter the call leaves out (`implied_terms`). Each called term comes with whether a
    partial trigger may still count for it: only when the call names it explicitly and the
    stored initial output is not already that study (`index_terms`).
    """
    own = _tokenize(tool_name)
    values = {
        str(v).strip().lower() for v in (agent_parameters or {}).values()
        if isinstance(v, str)
    }
    implied = {t.strip().lower() for t in implied_terms}
    index = {t.strip().lower() for t in index_terms}
    every: set[str] = set()
    called: list[tuple[set[str], bool]] = []
    for term in enum_terms:
        tokens = _distinctive({t for t in _SPLIT.split(term.lower()) if t and t not in _STOP}, own)
        if not tokens:
            continue
        every |= tokens
        key = term.strip().lower()
        if key in values:
            called.append((tokens, key not in index))
        elif key in implied:
            called.append((tokens, False))
    return every, called


def _counts(
    token: str, ttoks: set[str], enum_tokens: set[str], called: list[tuple[set[str], bool]]
) -> bool:
    """Whether a matched trigger token may count (see the module docstring)."""
    if not any(_tok_match(token, e) for e in enum_tokens):
        return True
    return any(
        any(_tok_match(token, e) for e in term)
        and (partial_ok or all(any(_tok_match(e, t) for t in ttoks) for e in term))
        for term, partial_ok in called
    )


def _trigger_has_meaningful_tokens(
    trigger_action: str,
    tool_name: str,
    called_terms: Sequence[set[str]] = (),
) -> bool:
    """True when the trigger names a *specific* study (not a pure ``re-run this tool``).

    Tokens of the enum term the call names do not make the trigger specific for that call:
    `request_continuous_eeg_monitoring` is a plain re-order of an `eeg_type: continuous_icu`
    recording, so it escalates past the index study on the repeat call.
    """
    own = _tokenize(tool_name)
    ttoks = _distinctive(_trigger_tokens(trigger_action), own)
    return any(
        not any(any(_tok_match(t, e) for e in term) for term in called_terms) for t in ttoks
    )


def match_followup(
    tool_name: str,
    agent_parameters: dict[str, Any] | None,
    followups: Sequence[Any],
    served_trigger_actions: set[str] | frozenset[str] = frozenset(),
    *,
    enum_terms: Sequence[str] = (),
    implied_terms: Sequence[str] = (),
    index_terms: Sequence[str] = (),
    accepts: Callable[[Any], bool] | None = None,
) -> Any | None:
    """Return the best specific-re-order follow-up for this call, or ``None``.

    A candidate must (a) target ``tool_name`` and (b) share at least one MEANINGFUL
    token between its ``trigger_action`` and the call's parameter values + tool name.
    Among candidates, score by meaningful-overlap count, then total-overlap count,
    then Jaccard; ties prefer a not-yet-served trigger, then declaration order.

    Returns ``None`` when nothing clears the minimum-overlap bar — the caller then
    falls through to the initial / fallback tiers. This never serves the wrong
    confirmatory evidence: a call that shares only a generic/family token with a
    sibling follow-up (``amyloid_PET`` vs ``request_fdg_pet``) does not match.
    """
    ctoks = _call_tokens(tool_name, agent_parameters)
    own = _tokenize(tool_name)
    enum_tokens, called = _enum_sets(
        tool_name, agent_parameters, enum_terms, implied_terms, index_terms
    )
    best_key: tuple | None = None
    best_fu: Any | None = None

    for idx, fu in enumerate(followups):
        if fu.tool_name != tool_name:
            continue
        if accepts is not None and not accepts(fu):
            continue
        ttoks = _trigger_tokens(fu.trigger_action)
        if not ttoks:
            continue
        matched = {
            t for t in ttoks
            if any(_tok_match(t, c) for c in ctoks) and _counts(t, ttoks, enum_tokens, called)
        }
        meaningful = _distinctive(matched, own)
        if not meaningful:
            continue
        jaccard = len(matched) / len(ttoks | ctoks) if (ttoks | ctoks) else 0.0
        key = (
            len(meaningful),
            len(matched),
            jaccard,
            fu.trigger_action not in served_trigger_actions,
            -idx,
        )
        if best_key is None or key > best_key:
            best_key, best_fu = key, fu

    return best_fu


def resolve_followup(
    tool_name: str,
    agent_parameters: dict[str, Any] | None,
    followups: Sequence[Any],
    served_trigger_actions: set[str] | frozenset[str] = frozenset(),
    *,
    has_initial_output: bool,
    is_repeat_call: bool,
    enum_terms: Sequence[str] = (),
    implied_terms: Sequence[str] = (),
    index_terms: Sequence[str] = (),
    accepts: Callable[[Any], bool] | None = None,
) -> Any | None:
    """Resolve which follow-up (if any) to serve, honouring the precedence rule.

    Precedence:
      1. A *specific re-order* (``match_followup`` above) always wins — it OVERRIDES
         a stale initial output. This fires even on the first call to a tool when
         the parameters carry a meaningful token (an explicit escalation order).
      2. Tool has NO initial output: the follow-up(s) ARE the only data for this
         tool (a fresh order like echo / cardiac monitoring, or a CSF study on a
         pathway with no baseline CSF). Serve the first not-yet-served follow-up
         for the tool — meaningful-trigger or not — matching the historical
         behaviour that a bare order returns the case's stored result.
      3. Tool HAS an initial output and this is a repeat call (call number >= 2):
         a *plain re-order* follow-up (trigger with no meaningful token, e.g.
         ``request_echocardiogram``, ``request_repeat_mri``) escalates past the
         already-seen initial. Among plain candidates, an unserved trigger is
         preferred, then declaration order.
      4. Otherwise return ``None`` — the caller serves the initial output (a bare
         first call to a tool that has one) or falls through to the off-pathway
         fallback tier.

    Tiers 1 and 3 consider only the follow-ups ``accepts`` (when given), so a candidate
    that does not describe the study ordered never shadows one that does. Tier 2 does
    not: its pick is not evidence that the follow-up answers this call, and skipping a
    refused report there would hand the call the next stored report of any study (an
    audiometry order receiving the case's autonomic testing), so a refused tier-2 pick
    is left for the caller to refuse.

    Pure: never mutates ``served_trigger_actions``; the caller records the served
    trigger after this returns.
    """
    specific = match_followup(
        tool_name, agent_parameters, followups, served_trigger_actions,
        enum_terms=enum_terms, implied_terms=implied_terms, index_terms=index_terms,
        accepts=accepts,
    )
    if specific is not None:
        return specific

    candidates = [fu for fu in followups if fu.tool_name == tool_name]
    if not candidates:
        return None

    if not has_initial_output:
        # The follow-up is the only stored data for this tool — serve first unserved.
        unserved = [fu for fu in candidates if fu.trigger_action not in served_trigger_actions]
        return (unserved or candidates)[0]

    if is_repeat_call:
        _, called = _enum_sets(tool_name, agent_parameters, enum_terms, implied_terms)
        plain = [
            fu for fu in candidates
            if (accepts is None or accepts(fu))
            and not _trigger_has_meaningful_tokens(
                fu.trigger_action, tool_name, [term for term, _ in called]
            )
        ]
        if plain:
            unserved = [fu for fu in plain if fu.trigger_action not in served_trigger_actions]
            return (unserved or plain)[0]

    return None
