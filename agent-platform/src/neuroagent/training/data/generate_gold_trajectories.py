"""Generate gold ReAct trajectories for agent distillation (teacher -> student SFT).

A teacher (Claude subagent, one per trajectory) writes an ideal [Thought, Action,
Observation] trace for a NeuroBench case. Traces that pass validation become SFT targets
for the small local student. This is offline agent distillation via rejection sampling
(FireAct, arXiv:2310.05915; Agent Distillation, arXiv:2505.17612).

Two trajectories per case, differing in shape so the student does not collapse onto one
rigid script; hospital protocols are present in ~60% of system prompts, rotated across
five hospitals, so rule-following generalises rather than being memorised.

Trajectories are generated for the TRAIN split only — run make_train_test_split first.

Usage:
    # Step 1: prepare one prompt per (train case x style)
    python -m neuroagent.training.data.generate_gold_trajectories \
        --dataset data/neurobench \
        --output training_data/gold_trajectories \
        --splits-dir data/neurobench/splits \
        --token-budget 3000 \
        --prepare-prompts

    # Step 2: subagents write raw traces to <output>/raw/{case_id}_{style}.txt
    #         (see scripts/training/generate_trajectories_workflow.js)

    # Step 3: parse, validate, reject, and emit trajectories.jsonl
    python -m neuroagent.training.data.generate_gold_trajectories \
        --dataset data/neurobench \
        --output training_data/gold_trajectories \
        --reasoning-budget 2200 \
        --assemble
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

from ...llm.prompts import load_prompt
from ...rules.rules_engine import RulesEngine
from ...tools.followup_matcher import resolve_followup

logger = logging.getLogger(__name__)

# Two trajectory styles per case. Shape diversity (FireAct) without behaviour
# collapse: one lean path, one differential-discriminating path that carries the
# hypothesis-revision episode on harder cases.
TRAJECTORY_STYLES = {
    "efficient_linear": (
        "Take the shortest defensible path to the diagnosis. Call only the tools that are "
        "strictly necessary to confirm it and to exclude the one or two dangerous "
        "alternatives. Skip anything whose result would not change management. "
        "In your <think> blocks, say briefly why the test you are ordering is essential — "
        "and, once, why you are NOT ordering an obvious but low-yield alternative. "
        "The differential narrows monotonically: no changes of direction."
    ),
    "differential_reasoned": (
        "Order tests that maximally discriminate between the competing diagnoses. In each "
        "<think> block, name the specific differential you are testing against and state "
        "what result would move you toward or away from it. After each observation, update "
        "your differential with adjusted likelihoods rather than restating it wholesale."
    ),
}

# Confidence must track difficulty, not always read as certain.
CONFIDENCE_RANGES = {
    "straightforward": "0.85-0.95",
    "moderate": "0.70-0.85",
    "diagnostic_puzzle": "0.60-0.80",
}

# Tool-call counts scale with difficulty and style (difficulty-aware distillation).
N_TOOL_CALLS = {
    ("straightforward", "efficient_linear"): "Exactly 2-3",
    ("straightforward", "differential_reasoned"): "Exactly 3-4",
    ("moderate", "efficient_linear"): "Exactly 3-4",
    ("moderate", "differential_reasoned"): "Exactly 4-5",
    ("diagnostic_puzzle", "efficient_linear"): "Exactly 3-5",
    ("diagnostic_puzzle", "differential_reasoned"): "Exactly 4-6",
}

HOSPITALS = ["us_mayo", "uk_nhs", "de_charite", "jp_todai", "br_hcfmusp"]

# Fraction of trajectories generated with NO hospital protocols in the system prompt.
# The rest rotate across the 5 hospitals so the student learns to follow whatever
# protocol block it is given rather than memorising one institution's pathways.
NO_RULES_FRACTION = 0.4

# Difficulties that receive a hypothesis-revision episode (never on straightforward:
# fabricated backtracking on easy cases teaches overthinking).
REVISION_DIFFICULTIES = {"moderate", "diagnostic_puzzle"}

_RULES_CACHE: dict[str, str] = {}

_LIKELIHOOD_ORDER = ["very_low", "low", "moderate", "high", "very_high"]


def _likelihood_rank(likelihood: Any) -> int:
    value = likelihood.value if hasattr(likelihood, "value") else str(likelihood)
    return _LIKELIHOOD_ORDER.index(value) if value in _LIKELIHOOD_ORDER else 0


def _difficulty_value(case: NeuroBenchCase) -> str:
    d = case.difficulty
    return d.value if hasattr(d, "value") else str(d)


def assign_hospital(case_id: str, style: str) -> str | None:
    """Deterministically assign a hospital (or None) to a trajectory.

    Deterministic in (case_id, style) so prompt preparation is reproducible and
    resumable across chunked generation runs.
    """
    digest = hashlib.sha256(f"{case_id}:{style}".encode()).hexdigest()
    if (int(digest[:8], 16) % 100) < int(NO_RULES_FRACTION * 100):
        return None
    return HOSPITALS[int(digest[8:16], 16) % len(HOSPITALS)]


def get_rules_context(hospital: str, rules_dir: str) -> str:
    """Cached RulesEngine.get_context() for one hospital."""
    if hospital not in _RULES_CACHE:
        _RULES_CACHE[hospital] = RulesEngine(rules_dir, hospital=hospital).get_context()
    return _RULES_CACHE[hospital]


def build_system_prompt(hospital: str | None, rules_dir: str, base: str | None = None) -> str:
    """Compose the system prompt exactly as AgentOrchestrator._build_system_prompt does."""
    if base is None:
        base = load_prompt("orchestrator.txt")
    if not hospital:
        return base
    context = get_rules_context(hospital, rules_dir)
    if not context:
        return base
    return base + f"\n\n## Hospital Protocols\n{context}"

def load_cases(dataset_path: Path, max_cases: int | None = None) -> list[NeuroBenchCase]:
    """Load NeuroBench cases from dataset directory."""
    cases_dir = dataset_path / "cases"
    if not cases_dir.exists():
        raise FileNotFoundError(f"Cases directory not found: {cases_dir}")
    case_files = sorted(cases_dir.glob("*.json"))
    if max_cases:
        case_files = case_files[:max_cases]
    cases = []
    for cf in case_files:
        data = json.loads(cf.read_text())
        cases.append(NeuroBenchCase.model_validate(data))
    return cases


def format_patient_info(case: NeuroBenchCase) -> str:
    """Format patient info — mirrors evaluation/runner.py format_patient_info."""
    p = case.patient
    v = p.vitals
    exam = p.neurological_exam

    parts = [
        f"Patient: {p.demographics.age}-year-old {p.demographics.sex}",
        f"Chief complaint: {p.chief_complaint}",
        f"History of present illness: {p.history_present_illness}",
    ]

    pmh = p.clinical_history.past_medical_history
    if pmh:
        parts.append(f"Past medical history: {'; '.join(pmh)}")

    meds = p.clinical_history.medications
    if meds:
        med_strs = [f"{m.drug} {m.dose} {m.frequency} ({m.indication})" for m in meds]
        parts.append(f"Current medications: {'; '.join(med_strs)}")

    allergies = p.clinical_history.allergies
    if allergies:
        parts.append(f"Allergies: {', '.join(allergies)}")

    fhx = p.clinical_history.family_history
    if fhx:
        parts.append(f"Family history: {'; '.join(fhx)}")

    exam_parts = []
    for field in ["mental_status", "cranial_nerves", "motor", "sensory", "reflexes", "coordination", "gait", "additional"]:
        val = getattr(exam, field, None)
        if val:
            exam_parts.append(f"{field.replace('_', ' ').title()}: {val}")
    parts.append("Neurological examination:\n" + "\n".join(f"  {e}" for e in exam_parts))

    parts.append(
        f"Vitals: BP {v.bp_systolic}/{v.bp_diastolic} mmHg, "
        f"HR {v.hr} bpm, Temp {v.temp}°C, RR {v.rr}, SpO2 {v.spo2}%"
    )

    return "\n".join(parts)


def get_available_tool_outputs(case: NeuroBenchCase) -> tuple[list[str], list[str]]:
    """Return lists of available initial and followup tool outputs."""
    ito = case.initial_tool_outputs
    initial = []
    # Map field names to tool names
    field_to_tool = {
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
    for field_name, tool_name in field_to_tool.items():
        val = getattr(ito, field_name, None)
        if val is not None:
            initial.append(tool_name)

    followup = []
    for fo in case.followup_outputs:
        followup.append(f"{fo.tool_name} (trigger: {fo.trigger_action})")

    return initial, followup


def _match_keyed_output(
    stored: dict[str, Any],
    argument: str,
    tool_name: str,
    case_id: str,
) -> dict[str, Any]:
    """Pick the stored result whose key matches the call's argument.

    `search_medical_literature` results are keyed by query and
    `check_drug_interactions` by drug. With a single stored result there is
    nothing to disambiguate. With several, match the argument against the keys
    (exact case-insensitive, then substring either way); if nothing matches,
    fall back to the first stored result — the historical behaviour — with a
    debug log so mismatched observations are traceable.
    """
    def _dump(value: Any) -> dict[str, Any]:
        return value.model_dump() if hasattr(value, "model_dump") else value

    keys = list(stored)
    if len(keys) == 1 or not argument:
        return _dump(stored[keys[0]])

    arg_norm = argument.strip().lower()
    for key in keys:
        if key.strip().lower() == arg_norm:
            return _dump(stored[key])
    for key in keys:
        key_norm = key.strip().lower()
        if key_norm and (key_norm in arg_norm or arg_norm in key_norm):
            return _dump(stored[key])

    logger.debug(
        "%s: %s argument %r matches none of the stored keys %s — falling back to first",
        case_id, tool_name, argument, keys,
    )
    return _dump(stored[keys[0]])


_TOOL_TO_FIELD = {
    "analyze_eeg": "eeg",
    "analyze_brain_mri": "mri",
    "analyze_ecg": "ecg",
    "interpret_labs": "labs",
    "analyze_csf": "csf",
    "order_ct_scan": "ct",
    "order_echocardiogram": "echo",
    "order_cardiac_monitoring": "cardiac_monitoring",
    "order_advanced_imaging": "advanced_imaging",
    "order_specialized_test": "specialized_test",
}


def _initial_output_for(case: NeuroBenchCase, tool_name: str, parameters: dict[str, Any]):
    """The case's initial output for a tool, or None. Mirrors the MockServer tiers
    for the direct-mapped and dict-keyed (literature/drug) tools."""
    ito = case.initial_tool_outputs
    field = _TOOL_TO_FIELD.get(tool_name)
    if field:
        return getattr(ito, field, None)
    if tool_name == "search_medical_literature" and ito.literature_search:
        return _match_keyed_output(
            ito.literature_search, parameters.get("query", ""), tool_name, case.case_id
        )
    if tool_name == "check_drug_interactions" and ito.drug_interactions:
        return _match_keyed_output(
            ito.drug_interactions, parameters.get("drug", ""), tool_name, case.case_id
        )
    return None


def get_tool_output_for_call(
    case: NeuroBenchCase,
    tool_name: str,
    parameters: dict[str, Any],
    served_triggers: set[str] | None = None,
    is_repeat_call: bool = False,
) -> dict[str, Any] | None:
    """Look up the pre-generated tool output for a given tool call.

    Resolution is identical to the eval MockServer (shared via
    `neuroagent.tools.followup_matcher.resolve_followup`): a matching follow-up for
    a specific re-order OVERRIDES the stale initial output; a bare first call to a
    tool returns its INITIAL output. Pass `served_triggers` (mutated in place) and
    `is_repeat_call` when replaying a trajectory so distinct re-orders escalate
    through distinct follow-ups; the stateless default (fresh call, empty served set)
    resolves a single call in isolation — used by the existence checks.

    For the dict-keyed tools (`search_medical_literature`, keyed by query;
    `check_drug_interactions`, keyed by drug), the call's argument selects among
    multiple stored initial results; see `_match_keyed_output`.
    """
    def _dump(val):
        if val is None:
            return None
        return val.model_dump() if hasattr(val, "model_dump") else val

    served = served_triggers if served_triggers is not None else set()
    initial = _initial_output_for(case, tool_name, parameters)

    followup = resolve_followup(
        tool_name, parameters, case.followup_outputs, served,
        has_initial_output=initial is not None,
        is_repeat_call=is_repeat_call,
    )
    if followup is not None:
        served.add(followup.trigger_action)
        return _dump(followup.output)

    return _dump(initial)


def compress_tool_output(output: dict[str, Any], tool_name: str) -> dict[str, Any]:
    """Compress a tool output to keep only clinically significant information.

    Removes normal/unremarkable values to reduce token count while preserving
    all diagnostically relevant findings.
    """
    if tool_name == "interpret_labs":
        # Only keep abnormal values + interpretation
        compressed = {}
        if "panels" in output:
            for panel_name, values in output["panels"].items():
                abnormal = [v for v in values if v.get("is_abnormal")]
                borderline = [v for v in values if v.get("clinical_significance")]
                kept = abnormal + [v for v in borderline if v not in abnormal]
                if kept:
                    compressed.setdefault("abnormal_results", {})[panel_name] = [
                        {"test": v["test"], "value": v["value"], "unit": v.get("unit", ""),
                         "reference_range": v.get("reference_range", ""),
                         "clinical_significance": v.get("clinical_significance")}
                        for v in kept
                    ]
            if not compressed.get("abnormal_results"):
                compressed["abnormal_results"] = "All values within normal limits"
        if "interpretation" in output:
            compressed["interpretation"] = output["interpretation"]
        if "abnormal_values_summary" in output:
            compressed["abnormal_values_summary"] = output["abnormal_values_summary"]
        return compressed

    elif tool_name == "analyze_brain_mri":
        # Keep findings + impression, drop normal observations
        compressed = {}
        if "findings" in output:
            compressed["findings"] = [
                {k: v for k, v in f.items() if v is not None and v != "None" and v != ""}
                for f in output["findings"]
            ]
        if "volumetrics" in output:
            compressed["volumetrics"] = output["volumetrics"]
        if "impression" in output:
            compressed["impression"] = output["impression"]
        # Skip additional_observations if all are "No..." / normal
        if "additional_observations" in output:
            notable = [o for o in output["additional_observations"]
                       if not o.lower().startswith("no ") and "normal" not in o.lower()
                       and "patent" not in o.lower() and "unremarkable" not in o.lower()]
            if notable:
                compressed["notable_observations"] = notable
        return compressed

    elif tool_name in ("order_specialized_test", "analyze_eeg", "analyze_ecg",
                       "order_advanced_imaging", "order_ct_scan",
                       "order_echocardiogram", "order_cardiac_monitoring"):
        # Keep findings + impression, remove null/empty fields
        return {k: v for k, v in output.items()
                if v is not None and v != "" and v != [] and v != "None"}

    elif tool_name == "analyze_csf":
        # Keep everything — CSF is usually compact and all clinically relevant
        return {k: v for k, v in output.items()
                if v is not None and v != "" and v != "None"}

    elif tool_name in ("check_drug_interactions", "search_medical_literature"):
        # Keep as-is — usually compact
        return output

    # Default: strip nulls
    return {k: v for k, v in output.items()
            if v is not None and v != "" and v != "None"}


def format_tool_outputs_section(case: NeuroBenchCase, compress: bool = True) -> str:
    """Format all available tool outputs for inclusion in the subagent prompt.

    If compress=True, strips normal/unremarkable values to reduce token count.
    """
    sections = []
    ito = case.initial_tool_outputs

    field_to_tool = {
        "mri": ("analyze_brain_mri", "Brain MRI"),
        "eeg": ("analyze_eeg", "EEG"),
        "ecg": ("analyze_ecg", "ECG"),
        "labs": ("interpret_labs", "Lab Results"),
        "csf": ("analyze_csf", "CSF Analysis"),
        "ct": ("order_ct_scan", "CT Scan"),
        "echo": ("order_echocardiogram", "Echocardiogram"),
        "cardiac_monitoring": ("order_cardiac_monitoring", "Cardiac Monitoring"),
        "advanced_imaging": ("order_advanced_imaging", "Advanced Imaging"),
        "specialized_test": ("order_specialized_test", "Specialized Test"),
    }

    for field_name, (tool_name, display_name) in field_to_tool.items():
        val = getattr(ito, field_name, None)
        if val is not None:
            raw = val.model_dump() if hasattr(val, "model_dump") else val
            output = compress_tool_output(raw, tool_name) if compress else raw
            output_json = json.dumps(output, indent=2, default=str)
            if len(output_json) > 2000:
                output_json = output_json[:2000] + "\n... (truncated)"
            sections.append(f"### {display_name} (`{tool_name}`)\n```json\n{output_json}\n```")

    # Literature search
    if ito.literature_search:
        for query_key, result in ito.literature_search.items():
            raw = result.model_dump() if hasattr(result, "model_dump") else result
            output_json = json.dumps(raw, indent=2, default=str)
            if len(output_json) > 1500:
                output_json = output_json[:1500] + "\n... (truncated)"
            sections.append(f"### Literature Search (`search_medical_literature`, query: \"{query_key}\")\n```json\n{output_json}\n```")

    # Drug interactions
    if ito.drug_interactions:
        for drug_key, result in ito.drug_interactions.items():
            raw = result.model_dump() if hasattr(result, "model_dump") else result
            output_json = json.dumps(raw, indent=2, default=str)
            if len(output_json) > 1500:
                output_json = output_json[:1500] + "\n... (truncated)"
            sections.append(f"### Drug Interactions (`check_drug_interactions`, drug: \"{drug_key}\")\n```json\n{output_json}\n```")

    # Followup outputs
    for fo in case.followup_outputs:
        raw = fo.output.model_dump() if hasattr(fo.output, "model_dump") else fo.output
        output = compress_tool_output(raw, fo.tool_name) if compress else raw
        output_json = json.dumps(output, indent=2, default=str)
        if len(output_json) > 1500:
            output_json = output_json[:1500] + "\n... (truncated)"
        sections.append(
            f"### {fo.tool_name} (followup, trigger: `{fo.trigger_action}`)\n```json\n{output_json}\n```"
        )

    return "\n\n".join(sections) if sections else "No tool outputs available."


def get_tool_schemas() -> dict[str, dict[str, Any]]:
    """The live tool schemas the agent is given at inference, keyed by tool name.

    Sourced from the running ToolRegistry rather than a hand-copied literal, so the
    arguments a golden trajectory demonstrates are exactly the arguments the student
    will be allowed to emit.
    """
    from ...tools.tool_registry import ToolRegistry

    registry = ToolRegistry.create_default_registry()
    return {d["function"]["name"]: d["function"] for d in registry.get_all_definitions()}


def format_tool_schemas(case: NeuroBenchCase) -> str:
    """Render the callable tools for this case, with exact argument names.

    Only tools that have an output for this case are listed — a call to anything else
    would return an error at inference, so it must never appear in a golden trace.
    """
    schemas = get_tool_schemas()
    lines: list[str] = []

    for name, fn in schemas.items():
        if get_tool_output_for_call(case, name, {}) is None:
            continue
        params = fn.get("parameters", {})
        props = params.get("properties", {})
        required = params.get("required", [])

        lines.append(f"- `{name}` — {fn.get('description', '').strip()}")
        for arg, spec in props.items():
            flag = "REQUIRED" if arg in required else "optional"
            enum = spec.get("enum")
            enum_str = f" one of {enum}" if enum else ""
            item = spec.get("items", {}).get("type")
            type_str = f"{spec.get('type', 'string')}" + (f"[{item}]" if item else "")
            lines.append(f"    - `{arg}` ({flag}, {type_str}){enum_str}")

    return "\n".join(lines) if lines else "(no tools available for this case)"


def optimal_tool_names(case: NeuroBenchCase) -> set[str]:
    """Tool names that appear anywhere in the case's optimal action sequence."""
    return {a.tool_name for a in case.ground_truth.optimal_actions if a.tool_name}


def format_optimal_actions(case: NeuroBenchCase) -> str:
    """Format optimal actions for the subagent prompt.

    Two deliberate omissions, both to stop the teacher copying things that would make the
    trace invalid at inference:

    * `tool_parameters` are NOT rendered. The dataset's stored parameters predate the
      current tool schemas (e.g. `analyze_brain_mri.sequences`,
      `order_advanced_imaging.modality`), and the teacher copies whatever it is shown.
      The authoritative argument names come from `format_tool_schemas`.
    * Steps naming a tool outside the live registry (e.g. `consult_medical_specialist`)
      are rendered as clinical actions without a tool name, since they cannot be called.

    Repeated tools are annotated rather than repeated: the environment returns the same
    output for a second call to the same tool, so a trace may only call each tool once.
    """
    schemas = get_tool_schemas()
    lines: list[str] = []
    tool_line_index: dict[str, int] = {}

    for a in case.ground_truth.optimal_actions:
        cat = a.category.value if hasattr(a.category, "value") else a.category
        citation = f" [{a.citation}]" if (a.citation or "").strip() else ""
        callable_tool = bool(a.tool_name) and a.tool_name in schemas

        # A tool listed twice is still ONE call in this environment. Merge the later step
        # into the first line instead of printing it again — printing it twice is what
        # tempts the teacher into a duplicate call.
        if callable_tool and a.tool_name in tool_line_index:
            idx = tool_line_index[a.tool_name]
            lines[idx] += (
                f"\n    ALSO COVERS (same single call): {a.action}"
                f"\n      Expected: {a.expected_finding}"
            )
            continue

        tool = a.tool_name if callable_tool else "clinical action, no tool call"
        if callable_tool:
            tool_line_index[a.tool_name] = len(lines)

        lines.append(
            f"  Step {a.step} [{cat}] ({tool}){citation}: {a.action}\n"
            f"    Expected: {a.expected_finding}"
        )
    return "\n".join(lines)


def banned_tool_names(case: NeuroBenchCase) -> set[str]:
    """Tools a golden trace must never call, by name.

    `useless_tools` / `harmful_tools` entries are *parameter-scoped*: a case can flag
    `order_advanced_imaging` with `modality=MR_spectroscopy` as useless while a different
    modality of the same tool is a required action (this overlap occurs in 103/600 cases).
    Because our observation lookup is keyed by tool name only, we can neither reproduce nor
    validate that distinction — so a tool is only "banned" when it never appears among the
    case's optimal actions.
    """
    gt = case.ground_truth
    flagged = {t.tool_name for t in (getattr(gt, "useless_tools", None) or [])}
    flagged |= {t.tool_name for t in (getattr(gt, "harmful_tools", None) or [])}
    return flagged - optimal_tool_names(case)


def format_avoidable_tools(case: NeuroBenchCase) -> str:
    """Format useless_tools + harmful_tools so the subagent actively SKIPS them.

    Entries whose tool is also part of the optimal workup are omitted: telling the teacher
    "never call order_advanced_imaging" while the workup requires it produces either a
    contradiction or a wrong trace.
    """
    gt = case.ground_truth
    banned = banned_tool_names(case)
    parts: list[str] = []

    useless = [t for t in (getattr(gt, "useless_tools", None) or []) if t.tool_name in banned]
    harmful = [t for t in (getattr(gt, "harmful_tools", None) or []) if t.tool_name in banned]

    if useless:
        parts.append("Tools that would be USELESS for this case (never call them):")
        for ut in useless:
            citation = f" [{ut.citation}]" if getattr(ut, "citation", "").strip() else ""
            parts.append(f"  - {ut.tool_name}{citation}: {ut.rationale}")
    if harmful:
        parts.append("Tools that would be HARMFUL for this case (calling one = safety event):")
        for ht in harmful:
            citation = f" [{ht.citation}]" if getattr(ht, "citation", "").strip() else ""
            parts.append(f"  - {ht.tool_name}{citation}: {ht.rationale}")

    return "\n".join(parts) if parts else "(No useless or harmful tools specifically flagged.)"


def build_revision_section(case: NeuroBenchCase, style: str) -> str:
    """Instruct one evidence-driven hypothesis-revision episode, where warranted.

    Only for `differential_reasoned` on moderate/diagnostic_puzzle cases. Revision is
    anchored to a real red herring when the case has one, otherwise to the strongest
    competing differential. Straightforward cases stay linear on purpose: fabricated
    backtracking on easy cases trains overthinking rather than recovery.
    """
    if style != "differential_reasoned":
        return ""
    if _difficulty_value(case) not in REVISION_DIFFICULTIES:
        return ""

    gt = case.ground_truth
    lines = [
        "## Required: one hypothesis-revision episode",
        "",
        "This trace must show the agent changing its mind ONCE, driven by evidence — the "
        "single most valuable behaviour we are teaching. Structure it like this:",
        "",
        "1. In an early `<think>`, genuinely favour the misleading hypothesis below. Give it "
        "the highest likelihood. Commit to it — do not hedge or hint that it is wrong.",
        "2. Order a test whose result is inconsistent with that hypothesis.",
        "3. In the `<think>` right after that observation, do the revision explicitly: name the "
        "finding, state plainly that it does not fit the hypothesis you were favouring, say "
        "what that rules out, and re-rank the differential.",
        "4. Proceed to confirm the true diagnosis.",
        "",
        "The revision `<think>` must read as a real reappraisal — e.g. \"The normal CSF cell "
        "count does not fit meningitis; that was driven by the fever, which the urine culture "
        "now explains. Shifting to ...\" — never as \"as expected\" or \"this was a distractor\".",
        "",
    ]

    if gt.red_herrings:
        rh = gt.red_herrings[0]
        lines += [
            "**Hypothesis to favour initially, then abandon:**",
            f"- Misleading finding: {rh.data_point} (in {rh.location})",
            f"- It wrongly suggests: {rh.intended_effect}",
            f"- What you must eventually conclude: {rh.correct_interpretation}",
        ]
        if len(gt.red_herrings) > 1:
            lines.append("")
            lines.append("Also interpret these correctly, without flagging them as distractors:")
            for extra in gt.red_herrings[1:]:
                lines.append(f"- {extra.data_point}: {extra.correct_interpretation}")
    else:
        competing = [
            d for d in gt.differential
            if d.diagnosis.lower() != gt.primary_diagnosis.lower()
        ]
        if not competing:
            return ""
        # Most plausible competitor makes the most instructive wrong turn.
        target = max(competing, key=lambda d: _likelihood_rank(d.likelihood))
        detail = target.key_features or "it is not supported by the confirmatory testing"
        lines += [
            "**Hypothesis to favour initially, then abandon:**",
            f"- Initially favour: {target.diagnosis}",
            f"- Its surface-plausible features: {detail}",
            "- Abandon it at the point a tool result is inconsistent with it.",
        ]

    return "\n".join(lines) + "\n"


def build_rules_section(hospital: str | None, rules_dir: str) -> str:
    """Tell the subagent that hospital protocols are in force for this trajectory."""
    if not hospital:
        return ""
    context = get_rules_context(hospital, rules_dir)
    if not context:
        return ""
    return (
        "## Hospital protocols in force\n\n"
        "The agent is operating under the protocols below. They are part of its system prompt.\n"
        "Where a protocol changes what you would otherwise do — mandating a step, dictating its "
        "timing, or forbidding an action — say so in the `<think>` block at the moment it bites "
        "(e.g. \"protocol requires CT before LP here\"). Do not recite protocols that do not apply, "
        "and do not mention the hospital by name.\n\n"
        f"```\n{context}\n```\n"
    )


def build_subagent_prompt(
    case: NeuroBenchCase,
    style: str,
    hospital: str | None,
    rules_dir: str,
    token_budget: int,
) -> str:
    """Build the full prompt to send to the trajectory-writing subagent."""
    template_path = (
        Path(__file__).resolve().parents[4]
        / "scripts"
        / "training"
        / "generate_trajectories_subagent.md"
    )
    template = template_path.read_text()

    gt = case.ground_truth
    difficulty = _difficulty_value(case)

    replacements = {
        "{{STYLE}}": style,
        "{{STYLE_INSTRUCTIONS}}": TRAJECTORY_STYLES[style],
        "{{REVISION_SECTION}}": build_revision_section(case, style),
        "{{RULES_SECTION}}": build_rules_section(hospital, rules_dir),
        "{{TOKEN_BUDGET}}": str(token_budget),
        "{{N_TOOL_CALLS}}": N_TOOL_CALLS[(difficulty, style)],
        "{{DIFFICULTY}}": difficulty.replace("_", " "),
        "{{CONFIDENCE_RANGE}}": CONFIDENCE_RANGES[difficulty],
        "{{TOOL_SCHEMAS}}": format_tool_schemas(case),
        "{{PRIMARY_DIAGNOSIS}}": gt.primary_diagnosis,
        "{{CRITICAL_ACTIONS}}": "\n".join(f"  - {ca}" for ca in gt.critical_actions) or "  (none)",
        "{{CONTRAINDICATED_ACTIONS}}": "\n".join(f"  - {ci}" for ci in gt.contraindicated_actions) or "  (none)",
        "{{AVOIDABLE_TOOLS}}": format_avoidable_tools(case),
        "{{KEY_REASONING_POINTS}}": "\n".join(f"  - {kr}" for kr in gt.key_reasoning_points) or "  (none)",
        "{{PATIENT_INFO}}": format_patient_info(case),
        "{{TOOL_OUTPUTS_SECTION}}": format_tool_outputs_section(case),
        "{{OPTIMAL_ACTIONS}}": format_optimal_actions(case),
    }

    prompt = template
    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, value)

    leftover = re.findall(r"\{\{[A-Z_]+\}\}", prompt)
    if leftover:
        raise ValueError(f"Unfilled template placeholders: {sorted(set(leftover))}")

    return prompt


def _tool_output_text(
    case: NeuroBenchCase,
    tool_name: str,
    parameters: dict[str, Any] | None = None,
    served_triggers: set[str] | None = None,
    is_repeat_call: bool = False,
) -> str | None:
    """The compressed case output for a tool, as the MockServer would return it."""
    actual = get_tool_output_for_call(
        case, tool_name, parameters or {},
        served_triggers=served_triggers, is_repeat_call=is_repeat_call,
    )
    if actual is None:
        return None
    compressed = compress_tool_output(actual, tool_name)
    text = json.dumps(compressed, indent=2, default=str)
    if len(text) > 2000:
        text = text[:2000] + "\n... (truncated)"
    return text


def parse_trajectory_from_response(
    response: str,
    case: NeuroBenchCase,
    system_prompt: str,
    style: str = "",
    hospital: str | None = None,
) -> dict[str, Any] | None:
    """Parse a subagent response into a structured multi-turn trajectory.

    The subagent writes a flat trace:
      <think>reasoning</think>
      <tool_call>{"name":..., "arguments":...}</tool_call>
      <tool_response>...</tool_response>
      ... (repeat)
      <think>final synthesis</think>
      ### Primary Diagnosis ...

    We split it into the message list the agent actually sees at inference:
      system -> user -> assistant(content + tool_calls) -> tool -> ... -> assistant(final)

    Tool calls are stored as structured `tool_calls` (not embedded text) so the Qwen
    chat template renders them in the model's native `<tool_call><function=...>` form.
    Tool responses are replaced with the real case output, so the trajectory matches
    exactly what MockServer would have returned.
    """
    # Unbalanced tags silently corrupt the split: an unclosed <think> swallows every later
    # tool call into one reasoning block, yielding a trajectory with zero tool calls.
    for tag in ("think", "tool_call", "tool_response"):
        n_open, n_close = response.count(f"<{tag}>"), response.count(f"</{tag}>")
        if n_open != n_close:
            logger.warning(
                "%s: unbalanced <%s> tags (%d open, %d close) — malformed trace",
                case.case_id, tag, n_open, n_close,
            )
            return None

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": format_patient_info(case)},
    ]

    tools_called: list[str] = []
    call_arguments: list[dict[str, Any]] = []  # parallel to tools_called
    pending_text: list[str] = []
    pending_tool_calls: list[dict[str, Any]] = []
    # Session state so re-orders resolve exactly as the MockServer would: which
    # follow-up triggers have been served, and how many times each tool was called.
    served_triggers: set[str] = set()
    tool_call_counts: dict[str, int] = {}

    def flush_assistant() -> None:
        content = "\n\n".join(t for t in pending_text if t).strip()
        if not content and not pending_tool_calls:
            return
        msg: dict[str, Any] = {"role": "assistant", "content": content}
        if pending_tool_calls:
            msg["tool_calls"] = list(pending_tool_calls)
        messages.append(msg)
        pending_text.clear()
        pending_tool_calls.clear()

    pattern = r"(<think>.*?</think>|<tool_call>.*?</tool_call>|<tool_response>.*?</tool_response>)"
    segments = re.split(pattern, response, flags=re.DOTALL)

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        resp_match = re.match(r"<tool_response>\s*(.*?)\s*</tool_response>", segment, re.DOTALL)
        if resp_match:
            if not pending_tool_calls:
                logger.warning("%s: <tool_response> with no preceding tool call", case.case_id)
                continue
            flush_assistant()
            last_tool = tools_called[-1]
            is_repeat = tool_call_counts.get(last_tool, 0) > 0
            tool_call_counts[last_tool] = tool_call_counts.get(last_tool, 0) + 1
            output = _tool_output_text(
                case, last_tool, call_arguments[-1],
                served_triggers=served_triggers, is_repeat_call=is_repeat,
            )
            if output is None:
                logger.warning("%s: no case output for tool %s", case.case_id, last_tool)
                output = resp_match.group(1).strip()
            messages.append({"role": "tool", "content": output})
            continue

        tc_match = re.match(r"<tool_call>\s*(.*?)\s*</tool_call>", segment, re.DOTALL)
        if tc_match:
            raw = tc_match.group(1).strip()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                logger.warning("%s: unparseable tool call JSON: %s", case.case_id, raw[:120])
                return None
            name = data.get("name", "")
            arguments = data.get("arguments", {})
            if not isinstance(arguments, dict):
                logger.warning("%s: tool call arguments not an object", case.case_id)
                return None
            tools_called.append(name)
            call_arguments.append(arguments)
            pending_tool_calls.append(
                {"type": "function", "function": {"name": name, "arguments": arguments}}
            )
            continue

        # <think> block or the final assessment text.
        pending_text.append(segment)

    flush_assistant()

    if not tools_called:
        logger.warning("No tool calls found in trajectory for %s", case.case_id)
        return None
    if messages[-1]["role"] != "assistant" or "tool_calls" in messages[-1]:
        logger.warning("%s: trajectory does not end with a final assistant answer", case.case_id)
        return None

    return {
        "case_id": case.case_id,
        "condition": case.condition.value,
        "difficulty": case.difficulty.value,
        "style": style,
        "hospital": hospital,
        "messages": messages,
        "tools_called": tools_called,
        "num_tool_calls": len(tools_called),
    }


# --- Validation ---

VALID_TOOL_NAMES = {
    "analyze_eeg", "analyze_brain_mri", "analyze_ecg", "interpret_labs",
    "analyze_csf", "search_medical_literature", "check_drug_interactions",
    "order_ct_scan", "order_echocardiogram", "order_cardiac_monitoring",
    "order_advanced_imaging", "order_specialized_test",
}


# Phrases that reveal the teacher was shown the answer key. Any hit rejects the
# trajectory: the student must never learn to narrate meta-knowledge it won't have.
LEAKAGE_PATTERNS = [
    r"\bground[- ]truth\b",
    r"\bred herring\b",
    r"\bdistractor\b",
    r"\boptimal action",
    r"\bthe correct answer\b",
    r"\bas (?:expected|required)\b",
    r"\bthis case (?:is|was) designed\b",
    r"\bper the case\b",
    r"\bcriteria pack\b",
    r"\bexpected finding\b",
    r"\bthe case (?:states|specifies)\b",
]

# Evidence that a genuine revision happened, rather than a linear narrowing.
REVISION_PATTERNS = [
    r"\bdoes(?:n't| not) fit\b",
    r"\bdoes(?:n't| not) support\b",
    r"\binconsistent with\b",
    r"\bargues against\b",
    r"\brevis(?:e|ing|ed)\b",
    r"\breconsider\b",
    r"\bshift(?:ing)? (?:my|the) differential\b",
    r"\bno longer\b",
    r"\brules? out\b.*\bwhich I (?:had )?favou?red\b",
    r"\bI (?:had )?favou?red\b",
    r"\bcontradicts?\b",
]


def diagnosis_core(diagnosis: str) -> str:
    """The bare diagnosis, without the trailing clinical commentary.

    107/600 ground-truth diagnoses append clauses after an em dash or semicolon, e.g.
    "Migraine with aphasic aura (ICHD-3 1.2.1) — misdiagnosed as TIA; warfarin ...".
    A trace states only the diagnosis itself, so term-overlap must be measured against the
    part before the first clause separator or the whole string would never match.
    """
    core = re.split(r"\s+[—–]\s+|\s+-\s+|;", diagnosis, maxsplit=1)[0]
    return core.strip().lower()


def _assistant_text(trajectory: dict[str, Any]) -> str:
    return "\n".join(
        m["content"] for m in trajectory.get("messages", []) if m["role"] == "assistant"
    )


def validate_trajectory(
    trajectory: dict[str, Any],
    case: NeuroBenchCase,
    token_budget: int | None = None,
) -> tuple[bool, list[str]]:
    """Validate a trajectory against the case ground truth.

    This is the rejection-sampling gate: only trajectories that pass become SFT targets.

    Returns (is_valid, list_of_issues).
    """
    issues: list[str] = []
    tools_called = trajectory.get("tools_called", [])

    for tool in tools_called:
        if tool not in VALID_TOOL_NAMES:
            issues.append(f"Invalid tool name: {tool}")

    # Each tool at most once: the observation lookup is keyed by tool name, so a second
    # call returns the identical output. A trace that narrates a *different* result from
    # a repeated call is teaching the student a fiction.
    repeated = sorted({t for t in tools_called if tools_called.count(t) > 1})
    if repeated:
        issues.append(f"Tool called more than once: {repeated}")

    # Tool arguments must match the live schemas the student sees at inference.
    schemas = get_tool_schemas()
    for message in trajectory.get("messages", []):
        for call in message.get("tool_calls", []) or []:
            fn = call.get("function", {})
            name, arguments = fn.get("name", ""), fn.get("arguments", {})
            schema = schemas.get(name)
            if schema is None:
                continue
            params = schema.get("parameters", {})
            props, required = params.get("properties", {}), params.get("required", [])
            for arg in arguments:
                if arg not in props:
                    issues.append(f"{name}: unknown argument '{arg}'")
            for arg in required:
                if arg not in arguments:
                    issues.append(f"{name}: missing required argument '{arg}'")
            for arg, value in arguments.items():
                allowed = props.get(arg, {}).get("enum")
                if allowed and value not in allowed:
                    issues.append(f"{name}.{arg}: '{value}' not in {allowed}")

    # Never demonstrate a tool the case cannot answer, or one flagged unsafe/useless.
    # `banned_tool_names` excludes tools that are also part of the optimal workup, since
    # the useless/harmful flags are parameter-scoped and we cannot check parameters here.
    gt = case.ground_truth
    banned = banned_tool_names(case)
    for tool in set(tools_called):
        if tool in banned:
            issues.append(f"Called useless/harmful tool: {tool}")
        if tool in VALID_TOOL_NAMES and get_tool_output_for_call(case, tool, {}) is None:
            issues.append(f"Called tool with no case output: {tool}")

    messages = trajectory.get("messages", [])
    if not messages or messages[-1]["role"] != "assistant":
        issues.append("Trajectory does not end with assistant turn")
    else:
        final = messages[-1]["content"]
        if messages[-1].get("tool_calls"):
            issues.append("Final assistant turn contains a tool call")
        for heading in ("Primary Diagnosis", "Differential", "Key Evidence", "Recommendations"):
            if not re.search(rf"###?\s*{heading}", final, re.IGNORECASE):
                issues.append(f"Missing '### {heading}' section in final response")

        gt_diag = diagnosis_core(gt.primary_diagnosis)
        diag_match = re.search(
            r"###?\s*Primary Diagnosis\s*\n+(.+?)(?:\n|$)", final, re.IGNORECASE
        )
        if diag_match:
            stated_diag = diag_match.group(1).lower()
            gt_terms = [t for t in gt_diag.split() if len(t) > 3]
            matches = sum(1 for t in gt_terms if t in stated_diag)
            if gt_terms and matches < len(gt_terms) * 0.4:
                issues.append(
                    f"Diagnosis may not match. Expected '{gt_diag}', got '{stated_diag}'"
                )
            if not re.search(r"confidence:\s*0?\.\d+", stated_diag, re.IGNORECASE):
                issues.append("Primary diagnosis line missing '(Confidence: X.XX)'")

    if trajectory.get("num_tool_calls", 0) == 0:
        issues.append("No tool calls in trajectory")

    assistant_text = _assistant_text(trajectory)

    # Every assistant turn must reason before it acts. Qwen's chat template renders an
    # empty `<think></think>` for a turn without one, which would train the student to
    # emit an empty reasoning block and jump straight to the tool call.
    for i, message in enumerate(messages):
        if message["role"] != "assistant":
            continue
        if not message["content"].strip():
            issues.append(f"Assistant turn {i} has empty content")
        elif "<think>" not in message["content"]:
            issues.append(f"Assistant turn {i} has no <think> block")

    for pattern in LEAKAGE_PATTERNS:
        hit = re.search(pattern, assistant_text, re.IGNORECASE)
        if hit:
            issues.append(f"Answer-key leakage: matched {pattern!r} ({hit.group(0)!r})")

    # Calibrated backtracking: revision required exactly where we asked for it.
    style = trajectory.get("style", "")
    difficulty = trajectory.get("difficulty", "")
    if style == "differential_reasoned" and difficulty in REVISION_DIFFICULTIES:
        if not any(re.search(p, assistant_text, re.IGNORECASE) for p in REVISION_PATTERNS):
            issues.append("Expected a hypothesis-revision episode but found no revision language")

    if token_budget:
        # ~4 chars/token is close enough for a budget guard; the exact check happens
        # at tokenisation time in the dataset audit.
        approx_tokens = len(assistant_text) // 4
        if approx_tokens > token_budget:
            issues.append(f"Trajectory too long: ~{approx_tokens} tokens > budget {token_budget}")

    return len(issues) == 0, issues


def load_train_case_ids(splits_dir: Path) -> set[str]:
    """Read the train split. Trajectories are never generated for test cases."""
    train_file = splits_dir / "train_cases.txt"
    if not train_file.exists():
        raise FileNotFoundError(
            f"{train_file} not found — run `python -m neuroagent.training.data."
            "make_train_test_split` first so no test case leaks into training."
        )
    return {line.strip() for line in train_file.read_text().splitlines() if line.strip()}


def prepare_prompts(
    dataset_path: Path,
    output_dir: Path,
    splits_dir: Path,
    rules_dir: str,
    token_budget: int,
    max_cases: int | None = None,
    styles: list[str] | None = None,
) -> None:
    """Prepare one prompt per (train case × style) and save to output directory."""
    train_ids = load_train_case_ids(splits_dir)
    cases = [c for c in load_cases(dataset_path) if c.case_id in train_ids]
    if max_cases:
        cases = cases[:max_cases]

    styles = styles or list(TRAJECTORY_STYLES.keys())
    output_dir.mkdir(parents=True, exist_ok=True)

    prompts_dir = output_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    # Subagents write their traces here; create it up front so a subagent's Write
    # never fails on a missing parent directory.
    (output_dir / "raw").mkdir(exist_ok=True)

    manifest = []
    hospital_counts: dict[str, int] = {}

    for case in cases:
        for style in styles:
            hospital = assign_hospital(case.case_id, style)
            prompt = build_subagent_prompt(case, style, hospital, rules_dir, token_budget)
            filename = f"{case.case_id}_{style}.txt"
            (prompts_dir / filename).write_text(prompt)

            key = hospital or "none"
            hospital_counts[key] = hospital_counts.get(key, 0) + 1

            manifest.append({
                "case_id": case.case_id,
                "style": style,
                "hospital": hospital,
                "prompt_file": f"prompts/{filename}",
                "condition": case.condition.value,
                "difficulty": case.difficulty.value,
                "has_revision": bool(build_revision_section(case, style)),
                "token_budget": token_budget,
            })

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    n_revision = sum(1 for m in manifest if m["has_revision"])
    logger.info(
        "Prepared %d prompts for %d train cases × %d styles → %s",
        len(manifest), len(cases), len(styles), output_dir,
    )
    logger.info("Revision episodes: %d/%d trajectories", n_revision, len(manifest))
    logger.info("Hospital mix: %s", dict(sorted(hospital_counts.items())))


def assemble_trajectories(
    dataset_path: Path,
    output_dir: Path,
    rules_dir: str,
    token_budget: int,
) -> None:
    """Parse raw subagent traces into the SFT dataset, rejecting whatever fails validation.

    This is the rejection-sampling step of agent distillation: a teacher trace only
    becomes a training target if it reaches the right diagnosis, keeps to the safety
    constraints, shows the revision behaviour we asked for, and never leaks the answer key.
    """
    cases_by_id = {c.case_id: c for c in load_cases(dataset_path)}

    manifest_path = output_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No manifest.json in {output_dir} — run --prepare-prompts first")
    manifest = json.loads(manifest_path.read_text())

    raw_dir = output_dir / "raw"
    rejected_dir = output_dir / "rejected"
    rejected_dir.mkdir(parents=True, exist_ok=True)
    # Clear stale rejects: a trajectory repaired since the last run must not keep an old
    # rejection file, or the repair list will keep re-repairing what already passed.
    for stale in rejected_dir.glob("*.json"):
        stale.unlink()

    trajectories_path = output_dir / "trajectories.jsonl"
    base_prompt = load_prompt("orchestrator.txt")

    n_valid = n_invalid = n_missing = n_unparsed = 0
    issue_counts: dict[str, int] = {}

    with open(trajectories_path, "w") as out:
        for entry in manifest:
            case_id, style = entry["case_id"], entry["style"]
            stem = f"{case_id}_{style}"
            raw_path = raw_dir / f"{stem}.txt"
            if not raw_path.exists():
                n_missing += 1
                continue

            case = cases_by_id[case_id]
            hospital = entry.get("hospital")
            system_prompt = build_system_prompt(hospital, rules_dir, base_prompt)

            traj = parse_trajectory_from_response(
                raw_path.read_text(), case, system_prompt, style=style, hospital=hospital
            )
            if traj is None:
                n_unparsed += 1
                (rejected_dir / f"{stem}.json").write_text(
                    json.dumps({"reason": "unparseable", "raw": raw_path.read_text()}, indent=2)
                )
                continue

            is_valid, issues = validate_trajectory(traj, case, token_budget=token_budget)
            if is_valid:
                out.write(json.dumps(traj) + "\n")
                n_valid += 1
            else:
                n_invalid += 1
                for issue in issues:
                    key = issue.split(":")[0]
                    issue_counts[key] = issue_counts.get(key, 0) + 1
                (rejected_dir / f"{stem}.json").write_text(
                    json.dumps({"issues": issues, "trajectory": traj}, indent=2)
                )

    total = len(manifest)
    logger.info(
        "Assembled %d valid / %d invalid / %d unparseable / %d not yet generated (of %d)",
        n_valid, n_invalid, n_unparsed, n_missing, total,
    )
    if issue_counts:
        logger.info("Rejection reasons: %s", dict(sorted(issue_counts.items(), key=lambda kv: -kv[1])))
    logger.info("Wrote %s", trajectories_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate gold trajectories for SFT")
    parser.add_argument("--dataset", required=True, help="Path to NeuroBench dataset")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument(
        "--styles", nargs="+",
        choices=list(TRAJECTORY_STYLES.keys()),
        default=None,
        help="Which trajectory styles to generate (default: both)",
    )
    parser.add_argument(
        "--splits-dir", default="data/neurobench/splits",
        help="Directory holding train_cases.txt (trajectories are train-split only)",
    )
    parser.add_argument("--rules-dir", default="agent-platform/config/hospital_rules")
    parser.add_argument(
        "--token-budget", type=int, default=3000,
        help="Total trace length the subagent is told to target, in tokens",
    )
    parser.add_argument(
        "--reasoning-budget", type=int, default=2200,
        help="Max supervised (assistant) tokens per trajectory, enforced at assembly",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare-prompts", action="store_true", help="Prepare prompts for subagent")
    group.add_argument(
        "--assemble", action="store_true",
        help="Parse raw subagent traces, validate, and write trajectories.jsonl",
    )

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.prepare_prompts:
        prepare_prompts(
            dataset_path=Path(args.dataset),
            output_dir=Path(args.output),
            splits_dir=Path(args.splits_dir),
            rules_dir=args.rules_dir,
            token_budget=args.token_budget,
            max_cases=args.max_cases,
            styles=args.styles,
        )
    elif args.assemble:
        assemble_trajectories(
            dataset_path=Path(args.dataset),
            output_dir=Path(args.output),
            rules_dir=args.rules_dir,
            token_budget=args.reasoning_budget,
        )


if __name__ == "__main__":
    main()
