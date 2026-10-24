# FND-M05
Reviewer status: R1 none, R2 none (no notes file for FND) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FND is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `patient.history_present_illness` | "normal complement levels and stable anti-dsDNA" 3 months ago gave the answer of the complement and anti-dsDNA panel the case now recommends. | FIXED: "found the disease quiescent". |
| B | minor | `patient.neurological_exam.motor` | "POSITIVE Hoover sign right leg" without describing the test; capitals. | FIXED: right hip extension weak on direct testing, full during left hip flexion. |
| C | major | `initial_tool_outputs.clinical_assessment` (plan H) | Meta keys; midline splitting counted as a rule-in sign; fragment findings; key leak in the impression. | FIXED: canonical shape; 3 validated signs (Hoover, distractibility, dragging gait); midline split and normal walking when unobserved listed as supportive; canonical impression. |
| B | major | `initial_tool_outputs.labs` (plan K) | "Baseline workup" rows with "Within reference range" values, no units or ranges, and the template `clinical_significance` "Ordered as part of the baseline workup..."; a clinical index (SLEDAI-2K) inside a lab report; antiphospholipid rows reported only as "Negative" with "titer" units; interpretive summary ("non-specific in SLE context"). | FIXED: CBC (arithmetic consistent), CMP, TSH and B12 with values, units and ranges; SLEDAI removed; anticardiolipin IgG/IgM, anti-beta-2 glycoprotein I IgG/IgM with values in their units and lupus anticoagulant as a dRVVT ratio; C3, C4, ESR, CRP kept; anti-dsDNA 4 IU/mL (<10); plain summary. |
| B | major | `initial_tool_outputs.mri` (plan I) | "with and without contrast", "no abnormal parenchymal or leptomeningeal enhancement". | FIXED: non-contrast report with T1, FLAIR, DWI and SWI; impression without enhancement statements. |
| C | major | `followup_outputs[1]` `hydroxychloroquine_interaction_check`, `initial_tool_outputs.drug_interactions` (plan C) | The only drug output was a follow-up recommending a baseline ECG, which this case marks as waste; no initial output. | FIXED: real content folded into a new initial output (HCQ + sertraline, minor QT effect, no PK interaction; HCQ retinal dosing warning; SSRI cautions) without the ECG recommendation; follow-up deleted. |
| C | major | `followup_outputs[0]` `rheumatology_consultation_sle` (plan B, ruling 4) | A rheumatology consult disguised as a literature search (empty summary). | FIXED: deleted; becomes the must "Inform her rheumatologist...". Canonical motor-only `initial_tool_outputs.literature_search`. |
| A | major | `ground_truth.action_criteria` (plan 3.2) | MRI and labs optional although the case raises a named stroke-mimic question in SLE; labs criterion ordered CBC, CMP, ESR, CRP rather than the assays that answer the question; literature and drug check recommended. | FIXED: exam required; antiphospholipid, complement C3/C4, anti-dsDNA recommended; non-contrast MRI recommended (`{contrast: false}`); drug check, neuropsychology and literature optional. Soft constraint exam before MRI. |
| C | major | `ground_truth.assessment` (plan D) | Template musts (duplicates, neuropsychology, "Do NOT make the diagnosis by exclusion"); template prohibitions. | FIXED: DX, COMM, PHYSIO, PSY (depression), "Inform her rheumatologist ... continue hydroxychloroquine unchanged"; prohibitions P1, P2, P3, P7 and "Start corticosteroids or escalate immunosuppression for presumed neuropsychiatric lupus". |
| C | major | `ground_truth.differential` (plan F) | MS, structural lesion and autoimmune encephalitis template rows; the case's own mimic (NPSLE or antiphospholipid-related stroke) absent although the accepted label names it. | FIXED: "Neuropsychiatric SLE or antiphospholipid-related stroke" `low` and "Acute ischemic stroke" `low`, citing the serology, the DWI MRI and the signs; template rows deleted. |
| D | major | `ground_truth.key_clinical_evidence` (plan E) | Template items with leaks. | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic data points; stressor field path; SLE itself, the case's main trap, absent. | FIXED: depression, the failed rotation (`social_history.recent_stressor`), and a new SLE red herring. |
| C | minor | `ground_truth.avoided_actions` (plan L) | `[Stone_2018]`; generic rationales. | FIXED: patient-specific rationales, `[Espay_2018]` / `[Stone_2016]`. |
| E | minor | `metadata.notes`, `difficulty_rationale`, `revision_reason` | Notes said NPSLE and APS must be excluded "rigorously before FND diagnosis" (the exclusion model the pack rejects); template rationale. | FIXED: notes and rationale restate the named question; `last_revised` 2026-10-24. |
| A | minor | `fallback_tool_outputs` (plan G) | `specialized_test` and `advanced_imaging` template fallbacks; echo without `echo_type`. | FIXED: nulled and removed from `fallback_tool_kinds`; echo `echo_type: TTE`. |

## Changes, in one paragraph a physician can read before re-reviewing

Sudden right-sided weakness in a woman with quiescent SLE now has one named question, an antiphospholipid-related or lupus-related stroke, answered by two recommended studies after the examination: a non-contrast brain MRI with DWI (normal 48 hours after onset) and a targeted panel of antiphospholipid antibodies, lupus anticoagulant, complement and anti-dsDNA (all normal; ESR 22 mildly high). The examination is required and counts three validated signs (right Hoover sign, distractibility, dragging gait); midline splitting and normal walking when unobserved are supportive. The HPI no longer gives the prior complement and anti-dsDNA results. The template "baseline" lab rows now have values, the SLEDAI score left the lab report, and the antiphospholipid rows have values in their own units. The rheumatology "consult" filed as a literature search became a must (inform the rheumatologist, continue hydroxychloroquine), and the interaction check no longer recommends an ECG the case marks as waste. Musts add psychological therapy with treatment of her depression; prohibitions add steroids or immunosuppression for presumed neuropsychiatric lupus. NPSLE or antiphospholipid stroke and ischemic stroke are both `low`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.2): this motor-only case accepts "psychogenic non-epileptic seizures", "PNES" and "functional seizures" and F44.5.
- The accepted label (`accepted[0]`) says "(neuropsychiatric SLE excluded)", an exclusion clause inside a positive diagnosis; not changed (rule 3), flagged for the label review.
- New citation keys used: `[Daum_2014]`, `[Stone_2016]` (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

None. Two additions beyond the plan's M05 entry, both decided for dataset quality: the M-PSY must (she has depression treated with sertraline, which plan 2D names as a qualifying comorbidity target), and a prohibition of corticosteroids or immunosuppression for presumed neuropsychiatric lupus (the case's main management trap, parallel to the plan's M09 relapse-steroid prohibition).

## Verification
Checked the log against the file (worker edits are in commit b8be2153; diffed against its parent): read the whole final case, the patient-block diff, criteria tiers and order against plan 3.2 and the case entry in plan 4, sequence constraints and stop rule, musts and prohibitions against avoided actions, differential against the returned results, lab arithmetic and ranges, laterality, leak guard. No reviewer notes exist for FND, so there is no note id to account for. perfect_agent.py -v, case_io.py check and test_case_guards pass after my changes.
The targeted panel holds the assays the recommended criterion orders (anticardiolipin, anti-beta-2 glycoprotein I, lupus anticoagulant, C3, C4, anti-dsDNA), all normal; CBC consistent (4.38 x 88.8 / 10 = 38.9, MCHC 32.9); MRI non-contrast without enhancement statements; the HPI no longer gives the prior complement and anti-dsDNA results; the drug output no longer recommends the ECG that the case marks as waste; the rheumatology consult is a must. The two additions beyond the plan (M-PSY for treated depression, the prohibition of steroids or immunosuppression for presumed NPSLE) are clinically sound.
No error found; no change.

## Condition audit

2026-10-24, FND condition auditor.

- `action-2-check-drug-interactions.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-neuropsych-battery.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `initial_tool_outputs.literature_search`: the summary still named video-EEG confirmation of functional seizures and psychological-treatment trials whose rows this motor-only output omits; set to the motor-only output of M09, P07, P08 and RM02 (Espay, Daum, Nielsen 2024, Stone 2005, motor summary).

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `ground_truth.diagnosis.accepted[0]` relabelled without the exclusion clause (was 'Functional neurological disorder — right-sided functional hemimotor syndrome, in patient with quiescent SLE (neuropsychiatric SLE excluded)'); ICD code unchanged.
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "functional movement disorder", "psychogenic non-epileptic seizures", "PNES", "functional seizures"; added "functional limb weakness", "functional motor disorder"; codes removed F44.5.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.
