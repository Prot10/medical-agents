# VASC-DEM-P05
Reviewer status: R1 none, R2 none (VASC-DEM has no notes file; never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (classes C1-C20) and from my own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key; no real call could match. | FIXED: `analyze_brain_mri {}`; label, rationale, evidence rewritten. |
| D | major | literature criterion `action-7-search-medical-literature`, `initial_tool_outputs.literature_search`, fallback | Plan C2 leak. | FIXED: criterion deleted, initial null, fallback deleted. |
| B | major | `action-8-check-drug-interactions`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group O: generic content while she takes sumatriptan with prior transient hemipareses and sertraline. | FIXED: criterion optional `{}` with case label, rationale and evidence; fallback deleted; initial output keyed `sumatriptan`: triptan vascular contraindications (stroke/TIA, hemiplegic migraine), ergots, sertraline-triptan serotonin toxicity (low risk), propranolol-sumatriptan none, sertraline-propranolol CYP2D6; non-vasoconstrictor acute alternatives. |
| C | major | `followup_outputs[NOTCH3]`, `ground_truth.diagnosis.accepted[0]`, `action-6` evidence | Plan C20: variant `c.475C>T p.(Arg159Cys)` replaced by the canonical `NOTCH3 c.544C>T p.(Arg182Cys)`, exon 4, EGFr 4; impression said "CADASIL is confirmed ... fits the family history ... relatives should be offered" (cross-reference to history). | FIXED: report rewritten (sequencing, ACMG 5, EGFr 1-6 group, CNV normal; impression states the genetic diagnosis as Kind 2, the EGFr 1-6 severity association and "Genetic counselling is recommended"); `quantitative_data` adds exon and zygosity. `accepted[0]` changed only in its variant string (entity unchanged); see CENTRAL. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA total and item losses. | FIXED: bedside observation (slowing, apathy, husband's quote kept), "Formal cognitive screening reported separately". |
| C | minor | `initial_tool_outputs.clinical_assessment` | "fluency 10 animals" is not the MoCA letter-fluency item; impression gave the severity ("Instrumental and occupational function are lost") and the puzzle framing ("why a 58-year-old with no vascular risk factors..."). MoCA arithmetic checked: 9 points lost = 21/30, no education correction at 17 years. | FIXED: letter fluency "10 words beginning with F"; impression lists totals, losses, AES 50, GDS 5/15, FAQ 17/30 only. |
| D | major | `initial_tool_outputs.specialized_test.impression` | "The profile is that of a small-vessel arteriopathy, not of a cortical degeneration"; "loss of instrumental function". | FIXED: profile statement per plan with percentiles and FAQ value. |
| D | major | `initial_tool_outputs.mri` | Plan C5: observations and volumetrics called anterior temporal pole involvement "the most specific imaging marker of CADASIL", the volume "far outside the sporadic range" for a patient "with normal blood pressure, normal lipids and no diabetes" (cross-modality), and the deep microbleeds "expected in CADASIL"; impression named CADASIL. | FIXED: STRIVE-2 numbered impression (Fazekas 3, 58 mL, symmetric anterior temporal pole and external capsule involvement, six lacunes with sites, two deep microbleeds, MTA 0-1); observations and volumetrics descriptive. The agent must now recognise the marker itself (the case's stated puzzle). |
| B | major | `initial_tool_outputs.labs` | Plan C6: Hct 41.6 with Hb 13.4; HDL ">40" in a woman; eGFR ">60"; interpretive `clinical_significance` on homocysteine, ESR, CRP, antiphospholipid; template values; interpretation drew the conclusion ("The absence of any acquired cause is itself the finding"). | FIXED: Hct 40.2; HDL ">50"; eGFR ">=60"; `clinical_significance` null; WBC 5.9, Plt 261, MCV 90, Na 138, K 4.0, ALT 17, albumin 4.4, folate 14.2; interpretation "No flagged values". |
| C | minor | `initial_tool_outputs.labs.panels` | Plan C15: young-SVD assays sat inside "Reversible_cause_screen"; antiphospholipid reported as one line. | FIXED: panel `Homocysteine_inflammatory_antiphospholipid` (homocysteine 9.4, ESR 8, CRP 2, lupus anticoagulant, anticardiolipin and anti-beta2-glycoprotein I negative) in the initial labs (as the plan says, so any combined order receives it) and the same panel as a follow-up (trigger `request_homocysteine_esr_crp_antiphospholipid`) so the targeted order returns exactly it. Probed: 9-panel, 4-panel, single-assay and 13-panel orders all return case data. |
| C | major | `ground_truth.action_criteria` | Plan C14, C15: no gait criterion despite a two-year gait disorder; no young-SVD criterion. | FIXED: `action-9-perform-clinical-assessment-gait` (recommended) with an authored follow-up (TUG 15.2 s, 0.79 m/s, six-step turn, tandem impossible, preserved arm swing, no freezing; consistent with the exam); `action-10-interpret-labs-young-svd` (recommended). |
| A | minor | `ground_truth.action_criteria[*]` | Plan C13: rationale equals label; duplicate keys. | FIXED: case-specific rationales and evidence; NOTCH3 cites `[Rutten_2019]`. Order per C16: screen, gait, neuropsych, labs, young-SVD labs, MRI, NOTCH3, drug check. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | Plan C16: no MRI-before-NOTCH3 constraint; `max_additional_actions` 0. | FIXED: soft MRI before NOTCH3 added; max 1; required set unchanged (screen, labs, MRI, NOTCH3). |
| B | major | `fallback_tool_outputs` | Plan C7: advanced_imaging and labs giveaways; CT "better characterised on the MRI already obtained"; echo with LV hypertrophy and aortic sclerosis in a normotensive 58-year-old, impression "No cardioembolic source". | FIXED: advanced_imaging and labs deleted; CT rewritten for this patient (confluent WM low attenuation including anterior temporal lobes and external capsules, thalamic and putaminal lacunes); echo normal LV and aortic valve, descriptive impression. Holter and EEG kept. `metadata.fallback_tool_kinds` updated. |
| C | minor | `ground_truth.avoided_actions[*].rationale` | Plan C18 generic rationales. | FIXED: case-specific (DaTscan rationale notes hypomimia and leg stiffness with preserved arm swing and pyramidal signs). |
| C | major | `ground_truth.assessment.required_recommendations` | Four musts were tool steps (look for anterior temporal poles, exclude acquired causes, send NOTCH3); no acute migraine alternative; counselling of the minor son not distinguished from adult relatives; apathy management and occupational support absent. | FIXED: six musts: diagnosis with variant [Rutten_2019]; stop sumatriptan, no triptans or ergots, non-vasoconstrictor acute treatment, continue propranolol; genetic counselling, cascade testing of adult relatives, predictive testing of the son deferred; normal BP without hypotension; apathy not treated as new depression, review sertraline; occupational and practical support. |
| C | minor | `ground_truth.assessment.prohibited_recommendations[0]`, `[1]` | "Do not continue triptans in a patient with a confirmed cerebral arteriopathy" (ergots missing); anticoagulation item claimed a haemorrhagic risk of the arteriopathy. | FIXED: triptans and ergots both named; anticoagulation item "there is no embolic source". |
| C | major | `ground_truth.differential[0]`, `[1]` | Plan C8: sporadic SVD and complicated migraine `moderate` after a positive NOTCH3 result. | FIXED: both `low`, key features cite the NOTCH3 result and the lacunes; PACNS features reworded. |
| B | minor | `ground_truth.key_clinical_evidence[2]`, `[4]`, `.red_herrings` | Dashes; empty field paths. | FIXED: KCE reworded; field paths `past_medical_history[1]` and `[2]`. |
| E | minor | `initial_tool_outputs.clinical_assessment.findings[*]` | Em dashes in untouched strings. | FLAGGED: left (plan rule). |
| - | check | plan 3.6 | perfect_agent.py ok (gait and NOTCH3 from follow-ups, young-SVD from its follow-up, others initial); `test_case_guards -k VASC-DEM-P05` 2 passed; `case_io.py check` schema and synonym guard OK, no failure names P05; `sequences` count 0. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Same case: a 58-year-old normotensive librarian with migraine with aura, two "complicated migraine" hemipareses, three years of subcortical decline with apathy and gait change, and a dominant family history; MRI shows Fazekas 3 disease with anterior temporal pole and external capsule involvement and six lacunes; NOTCH3 is positive. The variant is now the canonical exon 4, EGFr 4 cysteine variant c.544C>T p.(Arg182Cys), also in the diagnosis label. The exam no longer gives the MoCA, and the MRI, screen and neuropsychology reports no longer name CADASIL or argue the diagnosis; the agent has to read the anterior temporal pole sign itself. A timed gait assessment and a young-onset SVD screen (homocysteine, ESR, CRP, antiphospholipid antibodies, all normal) are recommended steps with their own results. The drug check returns the real triptan contraindications and the sertraline interaction. Labs use female ranges and carry no interpretive comments. Sporadic SVD and complicated migraine are low. Musts: stop sumatriptan with non-vasoconstrictor alternatives, genetic counselling with cascade testing of adults and deferred testing of the teenage son, BP without hypotension, apathy not treated as depression, occupational support.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `ground_truth.diagnosis.accepted[0]` changed in its variant string only (plan C20): "Vascular dementia due to CADASIL (...), NOTCH3 c.544C>T p.(Arg182Cys)". Synonyms and ICD codes untouched; the synonym guard passes.
- New citation key used: `[Rutten_2019]` (plan 5.4).

## Open questions for Andrea (judgment calls you could not settle)

- None. Deviation from the plan recorded: C15 says the young-SVD panel is answered by the initial labs; I kept it in the initial labs and also added the same panel as a follow-up, so that a targeted order returns only what was ordered while a combined order still receives it.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the final patient, ground truth, reports and follow-ups. Verified: canonical variant c.544C>T p.(Arg182Cys), exon 4, EGFr 4 in the report, quantitative data, criterion evidence, musts and `accepted[0]` (variant string only; logged under CENTRAL, entity unchanged); MoCA arithmetic (9 points lost = 21/30) and exam (fully oriented) agree; gait follow-up consistent with the exam (short steps, leg stiffness, no falls, tandem impossible); young-SVD panel normal and served for the targeted order; triptan and ergot prohibition matches the must and the drug output; teenage son predictive testing deferred, sister offered cascade counselling; differential alternatives all low with features drawn from the results; soft MRI before NOTCH3; no report names CADASIL except the genetic report (Kind 2).
Found and changed: eGFR 92 against creatinine 0.72 mg/dL in a 58-year-old woman (CKD-EPI 2021 about 97); set `initial_tool_outputs.labs.panels.CMP[eGFR].value` to 97 for consistency with the class fixed in P06 and P08. perfect_agent.py pass; case_io.py check: schema OK, no failure names P05; test_case_guards pass.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `initial_tool_outputs.clinical_assessment.findings[Memory].performance` | Plan C5 (screen gives scores only): "— retrieval pattern" was an interpretive label left in the screen, removed in the other cases' screens. | FIXED: "3/5 unaided, 5/5 cued" (scores only; also removes the em dash). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, executive_predominant_profile, onset_before_60, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).
- Diagnosis synonyms unchanged (I67.850 entry, shared with MIG-AURA-P06). The variant string in `accepted[0]` (`c.544C>T p.(Arg182Cys)`) is mirrored nowhere else in the repository (searched; the old `c.475C>T p.(Arg159Cys)` occurs nowhere).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
