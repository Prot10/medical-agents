"""Clinical report generation from agent traces."""

from __future__ import annotations

from ..llm.client import LLMClient
from ..llm.prompts import load_prompt
from .reasoning import AgentTrace

_DEFAULT_REPORT_PROMPT = """\
You are a clinical report generator. Based on the following agent reasoning trace, \
generate a structured clinical report suitable for a neurologist.

The report should include:
1. **Patient Summary**: Demographics, chief complaint, relevant history
2. **Investigations Performed**: Tools called and key findings
3. **Clinical Reasoning**: How findings were integrated
4. **Diagnosis**: Primary diagnosis with confidence, differential diagnoses
5. **Recommendations**: Treatment plan, follow-up, safety considerations

Be concise and clinically precise. Use standard medical terminology.
"""


def generate_report(llm: LLMClient, trace: AgentTrace) -> str:
    """Generate a structured clinical report from an agent trace.

    Args:
        llm: LLM client for report generation.
        trace: Complete agent trace from a case run.

    Returns:
        Formatted clinical report string.
    """
    try:
        system_prompt = load_prompt("report_generation.txt")
    except FileNotFoundError:
        system_prompt = _DEFAULT_REPORT_PROMPT

    # Build trace summary for the LLM
    trace_text = _format_trace_for_report(trace)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": trace_text},
    ]

    response = llm.chat(messages=messages, tools=None, temperature=0.0)
    return response.content or ""


def _format_trace_for_report(trace: AgentTrace) -> str:
    """Format an agent trace into a text summary for report generation."""
    parts = []

    for turn in trace.turns:
        if turn.role == "assistant" and turn.content:
            parts.append(f"[Agent Reasoning]\n{turn.content}")
        if turn.tool_calls:
            for tc in turn.tool_calls:
                parts.append(f"[Tool Call] {tc}")
        if turn.tool_results:
            for tr in turn.tool_results:
                parts.append(f"[Tool Result] {tr}")

    if trace.final_response:
        parts.append(f"[Final Assessment]\n{trace.final_response}")

    return "\n\n".join(parts)
