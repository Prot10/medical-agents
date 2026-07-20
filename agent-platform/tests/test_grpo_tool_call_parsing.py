"""The GRPO reward must see the tool calls Qwen3.5 actually emits.

Qwen3.5 is served with `--tool-call-parser qwen3_coder` and generates an XML function block,
not a JSON object. When `extract_tool_calls` only understood the JSON form it returned [] for
every real completion, so `tools_called` was empty and the actions / cost / safety / compliance
components of CompositeReward all scored zero — GRPO would have optimised a reward that gives
no credit for ordering the right test, and nothing would have failed loudly.
"""

from __future__ import annotations

from neuroagent.training.rewards.online_reward import build_pseudo_trace, extract_tool_calls

QWEN3_CODER_XML = """<think>
UMN and LMN signs with bulbar onset.
</think>

<tool_call>
<function=analyze_brain_mri>
<parameter=clinical_context>
progressive bulbar weakness
</parameter>
<parameter=contrast>
True
</parameter>
</function>
</tool_call>
<tool_call>
<function=order_specialized_test>
<parameter=test_type>
emg_ncs
</parameter>
</function>
</tool_call>

Primary diagnosis: Amyotrophic lateral sclerosis (ALS), bulbar-onset."""


def test_parses_qwen3_coder_xml_tool_calls():
    calls = extract_tool_calls(QWEN3_CODER_XML)
    assert [c["tool_name"] for c in calls] == ["analyze_brain_mri", "order_specialized_test"]
    assert calls[0]["parameters"]["clinical_context"] == "progressive bulbar weakness"
    assert calls[1]["parameters"]["test_type"] == "emg_ncs"


def test_xml_parameter_values_are_json_typed_when_possible():
    calls = extract_tool_calls(QWEN3_CODER_XML)
    assert calls[0]["parameters"]["contrast"] is True  # "True" -> bool, not the string


def test_json_tool_call_form_still_parses():
    """Other models (and hand-written fixtures) use the JSON form — do not regress it."""
    completion = '<tool_call>\n{"name": "analyze_eeg", "arguments": {"duration_minutes": 30}}\n</tool_call>'
    calls = extract_tool_calls(completion)
    assert calls == [{"tool_name": "analyze_eeg", "parameters": {"duration_minutes": 30}}]


def test_pseudo_trace_records_the_calls_the_reward_scores():
    trace = build_pseudo_trace(QWEN3_CODER_XML, "ALS-M01")
    assert trace.tools_called == ["analyze_brain_mri", "order_specialized_test"]
    assert trace.total_tool_calls == 2
    assert trace.total_cost_usd > 0  # tools were priced, so cost/efficiency rewards are live
    assert "Amyotrophic lateral sclerosis" in trace.final_response
    assert "<tool_call>" not in trace.final_response  # tool blocks stripped from the narrative


def test_no_tool_calls_yields_empty_trace_not_a_crash():
    trace = build_pseudo_trace("I think this is ALS.", "ALS-M01")
    assert trace.tools_called == []
    assert trace.total_cost_usd == 0.0
