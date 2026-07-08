"""Generate gold reasoning trajectories using Claude Code subagents.

Prepares NeuroBench cases into prompt-ready format for the trajectory
generation subagent, then assembles the multi-turn conversations into
training-ready JSONL.

Usage:
    # Step 1: Prepare prompts for all cases
    python -m neuroagent.training.data.generate_gold_trajectories \
        --dataset data/neurobench_v4 \
        --output training_data/gold_trajectories \
        --prepare-prompts

    # Step 2: After subagent generation, validate and format
    python -m neuroagent.training.data.generate_gold_trajectories \
        --dataset data/neurobench_v4 \
        --output training_data/gold_trajectories \
        --validate
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

from ...llm.prompts import load_prompt

logger = logging.getLogger(__name__)

# The 5 trajectory styles with instructions
TRAJECTORY_STYLES = {
    "minimal_efficient": (
        "Generate the SHORTEST possible trajectory that reaches the correct diagnosis. "
        "Only call tools that are strictly REQUIRED in the optimal actions. "
        "Skip recommended/optional tools. Prioritize the most informative tests first. "
        "In your <think> blocks, explicitly reason about why each test is essential "
        "and why you're skipping others."
    ),
    "standard_clinical": (
        "Follow a standard clinical workflow: history review → basic labs → imaging → "
        "specialized tests → final assessment. Order tests in the sequence a typical "
        "neurologist would in clinical practice. Include both required and some recommended "
        "tools where clinically justified."
    ),
    "thorough_workup": (
        "Perform a thorough diagnostic workup. Include all required tools AND most "
        "recommended tools from the optimal actions. Reason carefully about each test's "
        "contribution. This represents a careful, methodical clinician who wants to be "
        "comprehensive while still avoiding truly unnecessary tests."
    ),
    "cost_conscious": (
        "Minimize diagnostic costs while maintaining accuracy. Before EVERY tool call, "
        "explicitly reason about the cost-benefit trade-off in your <think> block. "
        "Mention approximate costs (MRI ~$320, labs vary by panel, advanced imaging $2000-5000). "
        "Order cheaper tests first. Skip expensive tests if cheaper alternatives provide "
        "sufficient diagnostic certainty. The goal is correct diagnosis at minimum cost."
    ),
    "differential_focused": (
        "Focus your tool ordering on systematically ruling out differential diagnoses. "
        "In each <think> block, explicitly state which differential you're testing against. "
        "Order tests that maximally discriminate between competing diagnoses. "
        "For each result, update your differential with specific likelihood adjustments."
    ),
}

# Tool definitions for the prompt
TOOL_DEFINITIONS_JSON = [
    {
        "type": "function",
        "function": {
            "name": "analyze_brain_mri",
            "description": "Order and analyze a brain MRI scan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "protocol": {"type": "string", "enum": ["standard", "epilepsy", "stroke", "tumor", "ms", "dementia"]},
                    "contrast": {"type": "boolean"},
                },
                "required": ["clinical_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_eeg",
            "description": "Order and interpret an EEG study.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "eeg_type": {"type": "string", "enum": ["routine", "ambulatory", "video", "continuous_icu"]},
                },
                "required": ["clinical_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_ecg",
            "description": "Order and interpret a 12-lead ECG.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                },
                "required": ["clinical_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "interpret_labs",
            "description": "Interpret laboratory results by panel.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "panels": {"type": "array", "items": {"type": "string"}},
                    "patient_age": {"type": "integer"},
                    "patient_sex": {"type": "string"},
                },
                "required": ["clinical_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_csf",
            "description": "Analyze cerebrospinal fluid results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "special_tests": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["clinical_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_ct_scan",
            "description": "Order a CT scan of the head.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "contrast": {"type": "boolean"},
                    "angiography": {"type": "boolean"},
                },
                "required": ["clinical_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_echocardiogram",
            "description": "Order an echocardiogram.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "echo_type": {"type": "string", "enum": ["TTE", "TEE", "bubble_study"]},
                },
                "required": ["clinical_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_cardiac_monitoring",
            "description": "Order cardiac rhythm monitoring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "monitor_type": {"type": "string", "enum": ["holter_24h", "holter_48h", "event_monitor_30d", "telemetry"]},
                },
                "required": ["clinical_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_advanced_imaging",
            "description": "Order advanced neuroimaging.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "imaging_type": {"type": "string", "enum": ["amyloid_PET", "FDG_PET", "DaTscan", "perfusion_MRI", "MR_spectroscopy", "carotid_duplex"]},
                },
                "required": ["clinical_context", "imaging_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_specialized_test",
            "description": "Order a specialized diagnostic test.",
            "parameters": {
                "type": "object",
                "properties": {
                    "clinical_context": {"type": "string"},
                    "test_type": {"type": "string", "enum": ["neuropsych_battery", "emg_ncs", "vep", "ssep", "baep", "tilt_table", "polysomnography", "autonomic_testing", "exercise_stress_test"]},
                },
                "required": ["clinical_context", "test_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_medical_literature",
            "description": "Search medical literature for clinical evidence.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_drug_interactions",
            "description": "Check drug interactions for a proposed medication.",
            "parameters": {
                "type": "object",
                "properties": {
                    "drug": {"type": "string"},
                    "current_medications": {"type": "array", "items": {"type": "string"}},
                    "patient_conditions": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["drug"],
            },
        },
    },
]


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


def get_tool_output_for_call(
    case: NeuroBenchCase,
    tool_name: str,
    parameters: dict[str, Any],
) -> dict[str, Any] | None:
    """Look up the pre-generated tool output for a given tool call."""
    ito = case.initial_tool_outputs
    tool_to_field = {
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

    # Check initial outputs first
    field = tool_to_field.get(tool_name)
    if field:
        val = getattr(ito, field, None)
        if val is not None:
            if hasattr(val, "model_dump"):
                return val.model_dump()
            return val

    # Check literature_search and drug_interactions (dict-based)
    if tool_name == "search_medical_literature" and ito.literature_search:
        query = parameters.get("query", "")
        # Return first match or first available
        for key, result in ito.literature_search.items():
            if hasattr(result, "model_dump"):
                return result.model_dump()
            return result

    if tool_name == "check_drug_interactions" and ito.drug_interactions:
        drug = parameters.get("drug", "")
        for key, result in ito.drug_interactions.items():
            if hasattr(result, "model_dump"):
                return result.model_dump()
            return result

    # Check followup outputs
    for fo in case.followup_outputs:
        if fo.tool_name == tool_name:
            output = fo.output
            if hasattr(output, "model_dump"):
                return output.model_dump()
            return output

    return None


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


def format_optimal_actions(case: NeuroBenchCase) -> str:
    """Format optimal actions for the subagent prompt."""
    lines = []
    for a in case.ground_truth.optimal_actions:
        cat = a.category.value if hasattr(a.category, "value") else a.category
        tool = a.tool_name or "manual"
        params = ""
        if a.tool_parameters:
            params = f" params={json.dumps(a.tool_parameters)}"
        citation = f" [{a.citation}]" if (a.citation or "").strip() else ""
        lines.append(
            f"  Step {a.step} [{cat}] ({tool}{params}){citation}: {a.action}\n"
            f"    Expected: {a.expected_finding}"
        )
    return "\n".join(lines)


def format_avoidable_tools(case: NeuroBenchCase) -> str:
    """Format useless_tools + harmful_tools for the subagent prompt.

    Used by the distractor / failure-mode trajectory styles (e.g.,
    "naive_excessive") and as input to the standard trajectories so the
    subagent knows which tools to actively SKIP, not just omit.
    """
    gt = case.ground_truth
    parts: list[str] = []
    useless = getattr(gt, "useless_tools", None) or []
    harmful = getattr(gt, "harmful_tools", None) or []
    if useless:
        parts.append("Tools that would be USELESS for this case (should NOT be called):")
        for ut in useless:
            params = ""
            tp = getattr(ut, "tool_parameters", None) or {}
            if tp:
                params = f" params={json.dumps(tp)}"
            citation = ""
            if getattr(ut, "citation", "").strip():
                citation = f" [{ut.citation}]"
            parts.append(f"  - {ut.tool_name}{params}{citation}: {ut.rationale}")
    if harmful:
        parts.append("Tools that would be HARMFUL for this case (calling = safety event):")
        for ht in harmful:
            params = ""
            tp = getattr(ht, "tool_parameters", None) or {}
            if tp:
                params = f" params={json.dumps(tp)}"
            citation = ""
            if getattr(ht, "citation", "").strip():
                citation = f" [{ht.citation}]"
            parts.append(f"  - {ht.tool_name}{params}{citation}: {ht.rationale}")
    return "\n".join(parts) if parts else "(No useless or harmful tools specifically flagged.)"


def build_subagent_prompt(
    case: NeuroBenchCase,
    style: str,
    system_prompt: str,
) -> str:
    """Build the full prompt to send to the Claude Code subagent."""
    template_path = (
        Path(__file__).resolve().parents[4]
        / "scripts"
        / "training"
        / "generate_trajectories_subagent.md"
    )
    template = template_path.read_text()

    patient_info = format_patient_info(case)
    initial_tools, followup_tools = get_available_tool_outputs(case)
    gt = case.ground_truth

    # Red herrings section
    red_herrings_section = ""
    if gt.red_herrings:
        rh_lines = []
        for rh in gt.red_herrings:
            rh_lines.append(
                f"- **{rh.data_point}** (in {rh.location}): "
                f"Intended to suggest {rh.intended_effect}. "
                f"Correct interpretation: {rh.correct_interpretation}"
            )
        red_herrings_section = (
            "- Handle these red herrings correctly in your reasoning:\n"
            + "\n".join(rh_lines)
        )

    tool_outputs_section = format_tool_outputs_section(case)

    prompt = template
    prompt = prompt.replace("{{STYLE}}", style)
    prompt = prompt.replace("{{STYLE_INSTRUCTIONS}}", TRAJECTORY_STYLES[style])
    prompt = prompt.replace("{{PRIMARY_DIAGNOSIS}}", gt.primary_diagnosis)
    prompt = prompt.replace("{{CRITICAL_ACTIONS}}", "\n".join(f"  - {ca}" for ca in gt.critical_actions))
    prompt = prompt.replace("{{CONTRAINDICATED_ACTIONS}}", "\n".join(f"  - {ci}" for ci in gt.contraindicated_actions))
    prompt = prompt.replace("{{KEY_REASONING_POINTS}}", "\n".join(f"  - {kr}" for kr in gt.key_reasoning_points))
    prompt = prompt.replace("{{RED_HERRINGS_SECTION}}", red_herrings_section)
    prompt = prompt.replace("{{PATIENT_INFO}}", patient_info)
    prompt = prompt.replace("{{TOOL_OUTPUTS_SECTION}}", tool_outputs_section)
    prompt = prompt.replace("{{OPTIMAL_ACTIONS}}", format_optimal_actions(case))

    return prompt


def parse_trajectory_from_response(
    response: str,
    case: NeuroBenchCase,
    system_prompt: str,
) -> dict[str, Any] | None:
    """Parse a subagent response into a structured trajectory.

    The subagent outputs a full trace with interleaved:
      <think>reasoning</think>
      <tool_call>{"name":..., "arguments":...}</tool_call>
      <tool_response>...</tool_response>
      ... (repeat)
      <think>final synthesis</think>
      ### Primary Diagnosis ...

    We split this into proper multi-turn messages:
      system → user → assistant (think+tool_call) → tool (response) → assistant → ...
    """
    patient_info = format_patient_info(case)

    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": patient_info},
    ]

    tools_called: list[str] = []

    # Split into blocks: <think>, <tool_call>, <tool_response>, and plain text
    pattern = r"(<think>.*?</think>|<tool_call>.*?</tool_call>|<tool_response>.*?</tool_response>)"
    segments = re.split(pattern, response, flags=re.DOTALL)

    current_assistant_content = ""

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        # Tool response → becomes a tool message
        resp_match = re.match(r"<tool_response>\s*(.*?)\s*</tool_response>", segment, re.DOTALL)
        if resp_match:
            # Flush current assistant content first (has the think + tool_call)
            if current_assistant_content.strip():
                messages.append({"role": "assistant", "content": current_assistant_content.strip()})
                current_assistant_content = ""

            tool_output = resp_match.group(1).strip()
            # Use the actual case output (compressed) instead of the subagent's copy
            if tools_called:
                last_tool = tools_called[-1]
                actual_output = get_tool_output_for_call(case, last_tool, {})
                if actual_output is not None:
                    compressed = compress_tool_output(actual_output, last_tool)
                    tool_output = json.dumps(compressed, indent=2, default=str)
                    if len(tool_output) > 2000:
                        tool_output = tool_output[:2000] + "\n... (truncated)"

            messages.append({"role": "tool", "content": tool_output})
            continue

        # Tool call → parse and accumulate in assistant content
        tc_match = re.match(r"<tool_call>\s*(.*?)\s*</tool_call>", segment, re.DOTALL)
        if tc_match:
            tc_text = tc_match.group(1).strip()
            current_assistant_content += f"\n<tool_call>\n{tc_text}\n</tool_call>"

            try:
                tc_data = json.loads(tc_text)
                tool_name = tc_data.get("name", "")
                tools_called.append(tool_name)
            except json.JSONDecodeError:
                logger.warning("Failed to parse tool call JSON: %s", tc_text[:100])
            continue

        # Think block or plain text → accumulate in assistant content
        current_assistant_content += "\n" + segment if current_assistant_content else segment

    # Flush remaining assistant content (final assessment)
    if current_assistant_content.strip():
        messages.append({"role": "assistant", "content": current_assistant_content.strip()})

    if not tools_called:
        logger.warning("No tool calls found in trajectory for %s", case.case_id)
        return None

    return {
        "case_id": case.case_id,
        "condition": case.condition.value,
        "difficulty": case.difficulty.value,
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


def validate_trajectory(
    trajectory: dict[str, Any],
    case: NeuroBenchCase,
) -> tuple[bool, list[str]]:
    """Validate a trajectory against the case ground truth.

    Returns (is_valid, list_of_issues).
    """
    issues: list[str] = []

    # Check tool names are valid
    for tool in trajectory.get("tools_called", []):
        if tool not in VALID_TOOL_NAMES:
            issues.append(f"Invalid tool name: {tool}")

    # Check final message is an assistant turn with structured assessment
    messages = trajectory.get("messages", [])
    if not messages or messages[-1]["role"] != "assistant":
        issues.append("Trajectory does not end with assistant turn")
    else:
        final = messages[-1]["content"]
        if not re.search(r"###?\s*Primary Diagnosis", final, re.IGNORECASE):
            issues.append("Missing '### Primary Diagnosis' section in final response")
        if not re.search(r"###?\s*Differential", final, re.IGNORECASE):
            issues.append("Missing '### Differential' section in final response")

        # Check diagnosis matches ground truth (fuzzy)
        gt_diag = case.ground_truth.primary_diagnosis.lower()
        # Extract the diagnosis from the final response
        diag_match = re.search(
            r"###?\s*Primary Diagnosis\s*\n+(.+?)(?:\n|$)", final, re.IGNORECASE
        )
        if diag_match:
            stated_diag = diag_match.group(1).lower()
            # Check for key terms from ground truth
            gt_terms = [t for t in gt_diag.split() if len(t) > 3]
            matches = sum(1 for t in gt_terms if t in stated_diag)
            if matches < len(gt_terms) * 0.4:
                issues.append(
                    f"Diagnosis may not match. Expected '{gt_diag}', got '{stated_diag}'"
                )

    # Check at least 1 tool was called
    if trajectory.get("num_tool_calls", 0) == 0:
        issues.append("No tool calls in trajectory")

    return len(issues) == 0, issues


def prepare_prompts(
    dataset_path: Path,
    output_dir: Path,
    system_prompt: str,
    max_cases: int | None = None,
    styles: list[str] | None = None,
) -> None:
    """Prepare all prompts and save to output directory."""
    cases = load_cases(dataset_path, max_cases=max_cases)
    styles = styles or list(TRAJECTORY_STYLES.keys())
    output_dir.mkdir(parents=True, exist_ok=True)

    prompts_dir = output_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)

    manifest = []

    for case in cases:
        for style in styles:
            prompt = build_subagent_prompt(case, style, system_prompt)
            filename = f"{case.case_id}_{style}.txt"
            (prompts_dir / filename).write_text(prompt)
            manifest.append({
                "case_id": case.case_id,
                "style": style,
                "prompt_file": f"prompts/{filename}",
                "condition": case.condition.value,
                "difficulty": case.difficulty.value,
            })

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    logger.info(
        "Prepared %d prompts for %d cases × %d styles → %s",
        len(manifest), len(cases), len(styles), output_dir,
    )


def validate_outputs(
    dataset_path: Path,
    output_dir: Path,
) -> None:
    """Validate all generated trajectories."""
    cases_by_id = {}
    for case in load_cases(dataset_path):
        cases_by_id[case.case_id] = case

    trajectories_path = output_dir / "trajectories.jsonl"
    if not trajectories_path.exists():
        logger.error("No trajectories.jsonl found in %s", output_dir)
        return

    valid = 0
    invalid = 0
    total = 0

    with open(trajectories_path) as f:
        for line in f:
            total += 1
            traj = json.loads(line)
            case_id = traj.get("case_id", "")
            case = cases_by_id.get(case_id)
            if case is None:
                logger.warning("Case %s not found in dataset", case_id)
                invalid += 1
                continue

            is_valid, issues = validate_trajectory(traj, case)
            if is_valid:
                valid += 1
            else:
                invalid += 1
                logger.warning("Invalid trajectory %s/%s: %s", case_id, traj.get("trajectory_style"), issues)

    logger.info("Validation: %d valid, %d invalid, %d total", valid, invalid, total)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate gold trajectories for SFT")
    parser.add_argument("--dataset", required=True, help="Path to NeuroBench dataset")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument(
        "--styles", nargs="+",
        choices=list(TRAJECTORY_STYLES.keys()),
        default=None,
        help="Which trajectory styles to generate (default: all 5)",
    )
    parser.add_argument("--system-prompt", default=None, help="Path to system prompt file")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare-prompts", action="store_true", help="Prepare prompts for subagent")
    group.add_argument("--validate", action="store_true", help="Validate generated trajectories")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # Load system prompt
    if args.system_prompt:
        system_prompt = Path(args.system_prompt).read_text()
    else:
        system_prompt = load_prompt("orchestrator.txt")

    if args.prepare_prompts:
        prepare_prompts(
            dataset_path=Path(args.dataset),
            output_dir=Path(args.output),
            system_prompt=system_prompt,
            max_cases=args.max_cases,
            styles=args.styles,
        )
    elif args.validate:
        validate_outputs(
            dataset_path=Path(args.dataset),
            output_dir=Path(args.output),
        )


if __name__ == "__main__":
    main()
