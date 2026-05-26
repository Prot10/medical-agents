# Gold trajectory authoring guide

**Audience:** the per-condition expert agents (and any future human reviewer)
that rewrite the `ground_truth` block of every NeuroBench v5 case.

**Purpose:** define how to populate each field of the new GroundTruth schema
so that downstream evaluation metrics, clinician validation, and the paper's
methods section all read off the same definition. **This is also a paper
artifact** — the methods section will cite it.

---

## 0. What you receive, what you produce

Each agent is invoked with:

1. The condition's **criteria pack** (`criteria_packs/{CONDITION}.md`).
2. **TOOL_PARAMETER_VOCABULARY.md** (closed allow-list for catchall tools).
3. **TOOL_REPORT_STYLE_GUIDE.md** (defines modality-faithfulness; relevant
   for case-body coherence checks).
4. ~26 case JSON files for that condition, each with the **realistic** tool
   outputs from the prior realism overhaul AND the current (legacy) ground_truth.
5. The 12-tool universe (canonical tool names).
6. The hospital rules YAMLs (read-only reference for sequence_constraints).

You produce, **for each case**, a rewritten `ground_truth` object that
validates against `neuroagent_schemas.evaluation.GroundTruth` and respects
the rules below.

---

## 1. The four buckets — required / recommended / optional / useless / harmful

The model behind every clinical-tier decision:

| Bucket | Lives in | Penalty if NOT called | Penalty if called |
| --- | --- | --- | --- |
| **required** | `optimal_actions[].category = required` | recall ↓, critical_actions_hit ↓ | — |
| **recommended** | `optimal_actions[].category = recommended` | mild (efficiency only) | — |
| **optional** | `optimal_actions[].category = optional` | none | none |
| **useless** | `useless_tools[]` | — | `useless_call_rate` ↑, cost ↑ |
| **harmful** | `harmful_tools[]` | — | `harmful_calls` ↑ (safety event) |

### How to decide between buckets

- **required** = a competent clinician would consider it negligence to skip
  this tool for this case. There must be an authoritative reason (criteria
  pack guideline) why missing it changes management.

- **recommended** = expected workup hygiene for this case, but a defensible
  workup could omit it (e.g., a clinician with high pre-test probability
  proceeding to treatment with one fewer confirmatory test).

- **optional** = a thoughtful clinician might order it, especially in
  atypical features; not ordering it is not penalized. Use sparingly —
  prefer leaving the tool out of `optimal_actions` entirely if it's
  truly neutral.

- **useless** = no clinical justification AND non-trivial cost. The cost
  threshold matters: a $0 tool (literature search) is never "useless";
  a $4000 tool (amyloid PET) with no indication absolutely is. **Per-case**,
  not per-condition — if the case has a comorbidity that justifies the
  tool, do NOT mark it useless.

- **harmful** = a competent clinician would refuse to order this for this
  case because doing so risks patient harm. Examples: LP in mass effect,
  iodinated contrast in renal failure, bubble study during acute stroke,
  high-dose magnesium IV in MG.

### What to remove from the workup entirely

Tools that are completely irrelevant to a case (`order_echocardiogram` for
a typical migraine workup) should be in `useless_tools` only if calling
them would be a meaningful resource cost or anchoring opportunity. Bare
irrelevance with low cost (e.g., literature search for an unrelated topic)
can be left silent — neither in optimal_actions nor in useless_tools.

---

## 2. Citations — strict allow-list per condition

The criteria pack lists the **only** citations the fleet may use in any
ActionStep / ToolClassification / SequenceConstraint. The validator rejects
off-list citations.

If the case genuinely requires citing something outside the pack, **flag it
in case `metadata.citation_gap`** with the proposed citation and rationale.
Do not invent. The packs will be extended after review.

Format the `citation` field as the cite-tag in square brackets exactly as
listed in the pack: `"citation": "[AAN_2009]"`. The full citation text is
in the pack — do not duplicate it here.

---

## 3. Sequence constraints — author sparingly

Only author a `SequenceConstraint` when ordering is clinically load-bearing.
Examples worth authoring:

- `order_ct_scan` → `analyze_csf` (`hard`) for suspected mass effect cases
- `analyze_brain_mri` → `analyze_csf` (`soft`) in general LP workup
- `interpret_labs` (coagulation) → invasive procedures (`hard`)
- `analyze_ecg` → IV tPA disposition (`hard`)

**Do NOT** author constraints that are merely workflow conveniences (e.g.,
"order labs before specialty consult"). The metric counts violations of
hard constraints into safety_score — over-authoring drowns out real signals.

Each constraint must cite from the allow-list and specify severity:
- `hard` = safety event when violated (LP→herniation, contrast→renal failure)
- `soft` = quality-of-care issue (efficiency)

---

## 4. Differential diagnosis — likelihood enum + ordering

`differential[]` is `list[DifferentialDx]` with structured `likelihood`
(`very_low | low | moderate | high | very_high`).

- The PRIMARY diagnosis goes in `primary_diagnosis` only, NOT in `differential`.
- The `differential` list contains the alternatives that were entertained.
- **Order by likelihood descending** (highest first; primary excluded).
- Aim for 4–6 entries. Fewer than 3 looks under-considered; more than 7 dilutes.
- Each entry needs `key_features` — one phrase that captures the
  distinguishing positive or negative feature for this case.

Likelihood semantics:
- `very_high` = primary candidate alternative if the primary diagnosis weren't true
- `high` = serious consideration, must be actively ruled out
- `moderate` = on the list, addressed in workup
- `low` = mentioned for completeness, briefly considered
- `very_low` = explicitly ruled out by a specific finding (use sparingly)

If the case's previous differential has 7 entries with all "low/very_low",
that's a writer-quality signal — consolidate to a tighter list.

---

## 5. Critical / contraindicated actions — free-text discipline

`critical_actions: list[str]` — free-text MUST-do clinical actions. Some
of these are tool calls (already in `optimal_actions`); some are not
(e.g., "monitor FVC every 4 hours", "consult neurosurgery for craniectomy
candidacy"). Each entry should:

- Be a single coherent clinical action.
- Use active voice, present tense ("Administer dexamethasone 10 mg IV").
- Avoid hedge words ("consider", "may want to") — these belong in optional.
- Include the rationale only if essential (most are obvious from context).

`contraindicated_actions: list[str]` — free-text MUST-not-do actions. Same
rules. Examples: "Do not start tPA without ruling out hemorrhage on CT",
"Do not give haloperidol in NMDAR encephalitis".

---

## 6. Red herrings — ground them in the case body

`red_herrings: list[RedHerring]` should reference distractor elements that
ACTUALLY exist in the case body (patient_info, tool outputs). For each
entry:

- `data_point`: the specific misleading element (e.g., "Mild B12 deficiency at 240 pg/mL").
- `location`: legacy free-text label (kept for backward compat).
- `field_path`: structured dotted path to where the element lives in the
  case JSON (e.g., `initial_tool_outputs.labs.panels.metabolic[3]`).
- `intended_effect`: how a naive agent might misinterpret it.
- `correct_interpretation`: what an attentive agent should conclude.

If the case lacks an embedded distractor matching the proposed red herring,
either flag it (and we'll add the distractor to the case body in a separate
pass) or remove the red herring entry. **Never author a red herring that
doesn't correspond to actual case data** — the metric layer relies on this
correspondence.

---

## 7. Case-body coherence checks (flag-don't-fix policy)

The realism overhaul froze patient_info + tool outputs. You may edit the
case body ONLY when ALL of:

1. The inconsistency is clear and uncontroversial (vital sign outside
   plausible range for age + condition; lab reference range incorrect for
   sex; tool output references a finding not present in another tool output).
2. The fix is mechanical (correcting a typo, normalizing units).
3. The fix does not change the clinical picture or the ground-truth diagnosis.

For any deeper issue — implausible presentation, clinically inconsistent
tool outputs, diagnosis-vs-data mismatch — **flag, don't fix**. Add a
`metadata.case_body_concerns` entry describing what's wrong and how you'd
fix it. A human or a follow-up pass will decide. Cases that are too far
gone may be marked for removal.

---

## 8. Difficulty recalibration

Re-rate `difficulty` based on the rubric below, AGAINST the realistic
(non-leaky) tool outputs:

- **straightforward**: 1–3 required tools, no red herrings, single
  diagnostic chain, agent can reach confident dx with ≤3 tools and minimal
  cross-modality synthesis.
- **moderate**: 3–5 required tools, 1–3 red herrings, requires
  synthesis across ≥2 modalities, has ≥1 plausible alternative differential
  that needs active rule-out.
- **diagnostic_puzzle**: ≥5 required tools OR ≥3 red herrings OR rare
  condition presentation requiring specialized workup OR multiple
  comorbidities making the diagnosis substantively harder.

Mismatch with the old label is expected — that's why we're recalibrating.

---

## 9. Metadata fields the fleet must populate

Add (or update) these keys in `metadata`:

```json
{
  "last_revised": "2026-05-26",
  "revision_reason": "gold trajectory regen v5",
  "criteria_pack_version": "1.0",
  "authoring_agent": "condition-expert:{CONDITION}",
  "difficulty_rationale": "5 required tools, 2 red herrings, requires EMG+MRI+labs synthesis",
  "case_body_concerns": [],     // only populate if you flagged issues
  "citation_gap": [],            // only populate if you needed off-list refs
  "vocab_gap": []                // only populate if you needed off-vocab tool params
}
```

Existing metadata keys are preserved unless they conflict.

---

## 10. Output contract (per case)

Return the FULL updated case JSON (not just ground_truth). The runner does
schema validation, vocab validation, cross-field coherence checks, then
writes the file. If any check fails, the runner sends the case back to the
agent with the specific errors.

**Never** silently change fields not specified above. If you must change
patient_info or tool outputs, log it explicitly in `metadata.case_body_concerns`
and make the change minimal.

---

## 11. Quality bar (paper-grade)

When in doubt, ask: "Would I be willing to put my name on this as a
contributing clinical reviewer on a Nature Machine Intelligence paper?"
Every choice should be defensible against a sharp clinician reviewer.

Specific anti-patterns to avoid:
- Inflated required-tool counts (e.g., adding tests to look thorough)
- Citation lists that omit the canonical guideline for the condition
- "useless_tools" lists that contradict legitimate per-case comorbidities
- Sequence constraints authored for workflow preferences
- Red herrings invented without corresponding case data
- Differential entries that all have likelihood "low" (an under-considered list)

---

## 12. Failure modes — escalate

Escalate (don't fix unilaterally) when:
- The case body's diagnosis is not supported by the case findings.
- The criteria pack itself appears incomplete for this case.
- A required tool is not in the 12-tool universe.
- Multiple cases of the same subtype have systematically inconsistent
  workups in the legacy ground_truth (signals a deeper authoring issue).

Each escalation = an entry in `metadata.case_body_concerns` and a flag in
the run log. Do not block on these.
