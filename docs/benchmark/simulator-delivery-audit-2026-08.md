# Does the simulator answer the questions the gold standard asks? (August 2026)

`validate_cases.py` checks each case against itself and `check_perfect_agent.py` checks that a perfect
agent scores 1.0. Neither asks a third question: **when an optimal action is replayed through the
MockServer, does the payload that comes back contain the result the action asks for?** This audit asks
it, and the answer was no often enough to change what the benchmark measures.

Everything below is measured by replaying every optimal action through the real
`MockServer` — not by reading the case files, which is how these defects stayed invisible.

## Defect classes found and closed

### 1. A set-valued order captured by a follow-up naming one item of it

`interpret_labs`, `analyze_csf` and `obtain_tissue_diagnosis` identify their study with a *set* of
assays. `followup_matcher` scores a follow-up's `trigger_action` slug against the call's parameter
values, and a set hands it many values to match, so one shared token was enough to declare a
"specific re-order" and override the initial output.

A status epilepticus case ordering
`[CBC, CMP, magnesium, AED_levels, lactate, ABG, ESR, CRP, beta-hCG, urinalysis]` shares the token
`aed` with `request_aed_optimization`. The ten-assay first-line order was answered by a
post-dose-escalation drug level; the case's own first-line panel was then served to a later action
asking for an autoimmune panel it does not carry. The two were crossed — the same shape as the
CT/CTA crossing fixed earlier, on a set parameter instead of a boolean flag.

**The rule is a comparison, not a threshold**, and that distinction is load-bearing. The share of an
order that a trigger names does *not* separate the crossed calls from the sound ones: 35 legitimate
matches name one item of four, exactly the shape of the crossings. A share threshold would have broken
all 35. What separates them is whether another payload stored for the same tool answers *more* of the
order — which is what answering a question means. So a token-matched follow-up yields to the initial
output when the initial names more of a multi-assay order, and only then. One-assay re-orders are
untouched, so the escalation path the follow-ups exist for stays open, and a discriminator hit still
wins outright because it is not a heuristic.

`anti` was added to the non-discriminating tokens. It prefixes every antibody name and identifies
none of them.

Crossed set-valued orders, one measure at both ends: **96 in 94 cases → 2**, and the two are named
exemptions in `test_setvalued_order_not_hijacked`, not a residue hidden in a count.

### 2. Diagnosis-establishing assays no call could reach

| Cases | The assay | Why it was unreachable |
|---|---|---|
| 9 MG | acetylcholine-receptor antibody panel | trigger `request_mg_antibodies` names the *disease*; the required action orders `[anti_AChR, anti_MuSK, anti_LRP4, TSH]`, the vocabulary names of the *analytes*. No shared token. Eight were answered with an exclusion panel; MG-RS11 was answered with a Miller-Fisher ganglioside panel — a different disease's antibody — matched on the token `anti` alone. |
| 2 NMDAR-ENC | anti-NMDAR antibody (CSF) | stored under `request_repeat_lp`, whose tokens (lumbar, puncture) appear in no call an agent can make; `analyze_csf` takes assay names. The plain-re-order tier will not serve it either, because `lp` is specific. |
| 1 SE | anti-Hu, paraneoplastic panel | stored under `request_autoimmune_encephalitis_panel`; the action orders `paraneoplastic_panel`. The `expected_finding` promises "Anti-Hu positive 1:1000 — mandates urgent cancer search". |

Repaired by renaming the trigger slug to name the assay it reports. No report text, value, action or
tier changed: the stored clinical content was already correct. Myasthenia gravis is the condition no
reviewer assessed — reviewer 2's five annotations arrived filed under peripheral neuropathy — and its
diagnosis rests on the serology that was unreachable in all nine of its cases.

### 3. A study that was billed and never returned

Thirteen bacterial meningitis cases have a required `analyze_csf{special_tests: [meningitis_panel]}`
action. `meningitis_panel` is priced at 322 EUR in `costs.yaml`, next to Gram stain and culture, so it
is a distinct study — and no case returned a result for it. **In nine of the thirteen the Gram stain is
negative and the culture still pending** (partially treated meningitis), which is precisely the
scenario in which the multiplex panel is the only identification available when the decision is made.

Three cases already held the result in a payload the order could not reach; their text was reused
verbatim. Elsewhere the organism is established by the case itself (latex agglutination, Gram stain, or
preliminary culture identification). *Streptococcus suis* and *Proteus mirabilis* are not panel
targets, so their result is "no target detected" with the limitation stated — and that is not an
assumption imported from outside: RP05's authored *Klebsiella* result already reads "Escherichia coli
K1: not detected; other bacterial targets not detected". The panel's targets are named in the report
text so a clinical reviewer can check the claim rather than take it.

Required set-valued orders receiving **nothing** they name: **15 → 2**.

### 4. Baseline panels ordered and never reported

188 baseline-panel requests (CBC, CMP, BMP, LFTs, coagulation, TSH, B12, HIV, type and screen) were
named by an optimal action and absent from the served payload. A case implies "no abnormality that
alters the diagnosis" for such a panel, by the same reasoning as the exclusion rows, and the
convention for saying it without inventing a number already existed in these files. Qualitative
assays keep qualitative wording (`HIV: Non-reactive`); a type and screen reports the antibody screen
only, because naming a blood group would invent a fact about the patient.

**The repair is more dangerous than the defect**, so this pass is mostly a guard. A normal CBC written
into bacterial meningitis contradicts its leucocytosis; a normal metabolic panel written into hepatic
encephalopathy contradicts its ammonia. A panel is reported unremarkable only when nothing in the case
says otherwise: no lab row flagged abnormal in any payload, nothing in `abnormal_values_summary`, no
interpretation sentence, no `expected_finding` of any optimal action, and nothing in the history,
reasoning or diagnosis. A second belt — an explicit condition-to-analyte veto — runs alongside, and it
caught eleven the textual guard missed (eight GBS cases with a characteristically deranged metabolic
panel, one NMDAR, two status epilepticus). **A single guard would have written eleven contradictions.**

After applying, all 188 rows were re-checked: no case flags a constituent of a panel it now reports as
unremarkable.

## How this is measured, and a correction to the numbers

The measure is: replay each optimal action, then ask whether each analyte it names appears in the
payload served. Matching is deliberately generous, because report text is prose (`Anti-GM1 IgG` for
`anti-GM1 IgM`), so the misses it reports are the clear ones.

Two definitions inside that measure were wrong while this work was in progress, and both **overstated**
the defect:

1. `anti` counted as a distinctive token, so any report mentioning any antibody was credited with
   delivering every requested antibody. This made the measure *flatter* than the truth.
2. A bundle acronym (CBC, CMP, coagulation) was counted delivered only when several constituents were
   present — four of twelve for CMP, two of six for coagulation. These reports enumerate selectively by
   design (an interpretation reads `Abnormal values: Sodium 133, ALT 68` and nothing else), so the
   threshold penalised the file format rather than the data. It reported the coagulation panel missing
   in all 22 hepatic encephalopathy cases while **every one of them carries an INR** — the component
   that decides management in liver failure. One constituent is the honest bar.

Figures quoted in the commit messages of 2026-08-08 were computed before correction 2 and their
absolute levels are therefore too high; the before/after deltas in those messages were measured
consistently at both ends and stand. Re-measured with the final definition at both ends:

| | analytes an optimal action names and the simulator never served | cases |
|---|---|---|
| before this audit (`1918bfc`) | 742 | 274 |
| after (`427c924`) | **205** | **134** |

## What remains, and why

All 205 are accounted for. None is unexplained.

| Count | Category | Disposition |
|---|---|---|
| 93 | assays that **confirm** the diagnosis (NfH, Abeta42, cytology, chr7/chr10 status, oligoclonal bands) and therapeutic drug levels | Deliberately left. Reporting a confirmatory assay as unremarkable would deny the case its own diagnosis; a drug level is a number with treatment consequences, not an exclusion. |
| 72 | a **class name** against a delivered member: `autoimmune_panel` served LGI1 and NMDAR antibodies, which are its members | A scoring-map question, not a missing result. `analyze_csf` prices `NMDAR_antibodies` at 276 and `autoimmune_panel` at 1840, so an agent making the specific, cheaper, clinically correct order gets no credit for a gold action naming the class — the same defect `76f0937` fixed for AED levels. Extending `_ANALYTE_CLASSES` closes it and both remaining unanswered orders. Deliberately deferred: it would be a second move on published required-coverage and tool-efficiency numbers, and it costs nothing extra to land with the corpus regeneration and re-baseline that `76f0937` already made necessary. |
| 32 | a specific diagnostic antibody (21 of them `anti_LRP4` in the MG cases, whose panel reports AChR and MuSK) | Needs per-case clinical judgement, not a rule: whether an unrecorded antibody is negative depends on that case's serological story. |
| 8 | the case states an abnormality and states no value to deliver | Correctly refused. Writing a number would invent a measurement. |

## Regression cover added

- `test_setvalued_order_not_hijacked.py` — the dataset-wide invariant that no set-valued order is
  served a payload another stored payload answers better, with the two exemptions named rather than
  counted, so a *new* crossing fails the test instead of hiding.
- The comparison used by the probe is imported from `MockServer` rather than reimplemented. A
  hand-maintained second copy of a rule is what shipped the stale tool catalogue to the clinical
  reviewers.

## Gates

600/600 cases clean, perfect agent 1.0 on 600/600, 1611 tests pass (5 pre-existing failures are the
absent `trl`/`transformers` training extras).
