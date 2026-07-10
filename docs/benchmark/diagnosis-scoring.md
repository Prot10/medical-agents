# How a diagnosis is scored

`diagnostic_accuracy_top1` and `diagnostic_accuracy_top3` are the headline numbers of every
NeuroBench run. Both are defined in
[`evaluation/metrics.py`](../../agent-platform/src/neuroagent/evaluation/metrics.py); this
page explains what they mean and why they are shaped this way.

## The metric reads the agent's conclusion, not its essay

The orchestrator system prompt requires the final response to open with

```
### Primary Diagnosis
[Diagnosis] (Confidence: X.XX)

### Differential Diagnoses
1. [Alternative] - [Supporting/opposing features]
```

`stated_primary_diagnosis()` reads that section, and top-1 is scored against it alone.

This matters because a clinical response mentions many diseases. Before this was enforced,
the metric searched the **entire** final response, so an agent that concluded *multiple
sclerosis* while keeping *ALS* on its differential scored a correct top-1 for ALS. Measured
across the 1000 gold trajectories against all 600 ground truths, whole-response matching
accepted 1898 wrong-condition responses; 1653 of those were driven by text below the
conclusion. Scoring the stated span cuts it to 338, nearly all of which are dual diagnoses
whose stated span genuinely names both diseases (`ALS concurrent with …`).

The practical consequence of the old behaviour: **a verbose model outscored a decisive one.**

## What counts as naming the diagnosis

`_states_diagnosis()` accepts the stated span if any of these hold:

1. it contains the **core** — the ground truth up to the first ` — ` or `;`, which drops the
   trailing clinical commentary that 107 of the 600 ground truths carry;
2. it contains the **head** — the core without parenthetical abbreviations and without the
   subtype after the first comma. `Amyotrophic lateral sclerosis (ALS), bulbar-onset` →
   `amyotrophic lateral sclerosis`. Across the 600 cases no head is shared by two
   conditions, so a head match identifies the condition unambiguously, and an agent that
   names the disease without the ground truth's qualifiers is not marked wrong;
3. it contains **≥70% of the core's key terms** (words over three characters, punctuation
   stripped) — the tolerant fallback for rewordings.

Matching is deliberately tolerant *within* the stated span and strict about *where* the span
comes from. Getting this backwards is what made the metric wrong.

## Top-3 ranks the agent's differential

`diagnostic_accuracy_top3` is true when the correct diagnosis is the agent's primary or
appears in the first three entries of **its own** `### Differential Diagnoses`.

It used to return true when the response mentioned any of the *ground truth's* differential
entries — diagnoses that are wrong by construction. It credited the agent for naming the
distractors.

## If the agent states no diagnosis

A response with no recognisable diagnosis section (no heading, no `Diagnosis:` label) is
scored against the whole response, but must then contain the diagnosis **verbatim** — never
a bag-of-words near-miss. Format non-compliance should not zero a model outright, and it must
not buy it the looser standard either. `<think>` blocks are stripped before any of this;
reasoning text is not a conclusion.

## Reading old numbers

Any top-1 or top-3 figure produced before this change was measured with whole-response
matching and is not comparable to a figure produced after it. Re-run the evaluation rather
than reconciling the two.
