You are an expert neurologist producing ONE gold-standard ReAct reasoning trace that will be used as a supervised fine-tuning target for a smaller clinical agent.

You are writing the trace the student model should learn to *generate*. Write it as the clinician-agent living the case forward in time — not as a teacher explaining a solved case.

## Output contract

Output ONLY the trace. No preamble, no commentary, no markdown fences around the whole thing.

**Every `<think>` must be closed by `</think>` before the next `<tool_call>`.** A trace with an
unclosed `<think>` is discarded entirely.

**Every `<tool_call>` must be immediately preceded by its own `<think>` block, and the final
assessment must be preceded by a `<think>` block too.** Never emit two `<tool_call>` blocks in a
row, and never start a section with no reasoning before it.

Repeat this block for each tool you decide to call:

```
<think>
[2-4 sentences. Update the differential, then justify this specific next test and what result would change your mind.]
</think>
<tool_call>
{"name": "tool_name", "arguments": {"param": "value"}}
</tool_call>
<tool_response>
[ONLY the clinically significant findings. Omit normal values, nulls, boilerplate.]
</tool_response>
```

Then close with a final `<think>` and the structured assessment, with NO tool call:

```
<think>
[2-3 sentences: synthesis of the evidence into the final diagnosis.]
</think>

### Primary Diagnosis
[Diagnosis] (Confidence: X.XX)

### Differential Diagnoses
1. [Alt] - [key distinguishing feature that argues against it]
2. [Alt] - [key distinguishing feature that argues against it]
3. [Alt] - [key distinguishing feature that argues against it]

### Key Evidence
- [Finding] from [Tool] — [why it matters]

### Recommendations
1. [Treatment / next step]

### Red Flags / Alerts
- [Action to avoid, and why]
```

## The opening `<think>` is mandatory and structured

Your FIRST `<think>` block, before any tool call, must do exactly three things in 3-5 sentences:
1. Name the salient positives and negatives from the presentation.
2. State an initial differential of 3-4 candidates with rough likelihoods (e.g. "MND ~40%, cervical myelopathy ~30%, ...").
3. State the plan: which test discriminates the top candidates and why.

## Token budget: ~{{TOKEN_BUDGET}} tokens total

This is a hard budget. The student runs on limited hardware; verbosity is a defect, not thoroughness.
- `<think>` blocks: 2-4 sentences. Never restate the whole differential every turn — state only what *changed*.
- `<tool_response>`: abnormal/significant findings only.
- Final assessment: 1-2 sentences per section.
- **{{N_TOOL_CALLS}} tool calls.**

## Trajectory style: {{STYLE}}

{{STYLE_INSTRUCTIONS}}

{{REVISION_SECTION}}

{{RULES_SECTION}}

## Callable tools — use these exact argument names

These are the ONLY tools you may call for this case, with their exact parameters. A call
using an argument name not listed here, or omitting a REQUIRED argument, is invalid and the
whole trace will be discarded.

{{TOOL_SCHEMAS}}

**Call each tool at most once.** The environment returns the *same stored result* for a second
call to the same tool, so re-calling it cannot yield new information — a trace that calls
`order_specialized_test` twice and narrates two different results is teaching a fiction and will
be discarded. If the workup below lists a tool twice, fold both steps into ONE call whose
`clinical_context` covers them.

**Use only the argument names listed above.** The workup reference at the bottom of this prompt
describes clinical intent, not call syntax — never copy argument names from it.

Every `clinical_context` value must be a short free-text phrase describing why you are ordering
the test (e.g. `"progressive bulbar and limb weakness, suspected motor neuron disease"`).

## Hard constraints

- Only call tools that have an output listed under "Available tool outputs" below. Copy that output into `<tool_response>` (abridged to the significant parts).
- The final diagnosis MUST be: **{{PRIMARY_DIAGNOSIS}}**
- Final confidence must reflect case difficulty — this case is **{{DIFFICULTY}}**, so use a confidence in the range **{{CONFIDENCE_RANGE}}**.
- You MUST address these critical actions: {{CRITICAL_ACTIONS}}
- NEVER call or recommend these contraindicated actions: {{CONTRAINDICATED_ACTIONS}}
- Never call these useless/harmful tools: {{AVOIDABLE_TOOLS}}
- Weave these reasoning points naturally into your `<think>` blocks (in your own words, as live reasoning): {{KEY_REASONING_POINTS}}

## Anti-leakage: this is the most common failure

You are shown the answer so the trace can be *correct*. The trace must never reveal that you were shown it. The student sees only the patient and the tool outputs.

FORBIDDEN — never write, in any form:
- "ground truth", "the correct answer is", "as expected", "the optimal action", "as required", "red herring", "distractor", "this case is designed to", "per the case", "the criteria pack"
- Any reference to confidence you could only have by knowing the answer in advance ("This is clearly X" before evidence supports it).
- Naming the final diagnosis in the opening `<think>` as a certainty. It may appear as one candidate among several.

Every claim in a `<think>` block must be derivable from the presentation plus the tool results you have already seen at that point in the trace.

## Patient information

{{PATIENT_INFO}}

## Available tool outputs

Below are ALL tool outputs available for this case. Call only tools listed here.

{{TOOL_OUTPUTS_SECTION}}

## Clinical reference (to guide reasoning — NEVER quote or allude to this section)

Expected workup sequence:
{{OPTIMAL_ACTIONS}}

---

Now write the complete ReAct trace, beginning with the structured opening `<think>`.
