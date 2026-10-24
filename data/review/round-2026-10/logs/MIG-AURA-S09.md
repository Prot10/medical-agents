# MIG-AURA-S09
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (plan 1.3): structured ICHD-3 history required; no MRI, CSF, ECG, EEG, echo or labs in a typical case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.hpi`, `patient.pmh[1]` | The patient block gave the answer to the case's TIA question: "this was a typical left-sided 20-minute visual aura", pmh "retrospectively consistent with typical migraine aura". | FIXED: the episode is now described by its features (20-minute shimmering disturbance spreading across the left visual field, followed by headache, no limb or speech symptoms); pmh states only the query and the normal MRI. |
| B | minor | same HPI fields | "not on contraception (has an IUD)" contradicts the levonorgestrel IUS listed as contraception; the normal MRI of 4 years ago stated twice. | FIXED: "uses a levonorgestrel intrauterine system for contraception"; the duplicate MRI sentence removed; added that no long-term medication was started after the query (plan S09: no antiplatelet in `patient`). |
| D | minor | `patient.clinical_history.medications[2]` | Indication "Contraception (appropriate — progestin-only)": evaluative hint. | FIXED: drug "Levonorgestrel intrauterine system", indication "Contraception". |
| A, D | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentence copied three times, generic SNNOOP10 line, placeholder modality score. | FIXED: rewritten (10 years, 3-4 severe attacks a month, visual aura 20-25 min, the queried episode described by its features, acute-drug days about 4-6, the two failed preventives, examination, each SNNOOP10 flag); criteria_met unchanged (5 of 6, consistent). |
| C, D | major | `followup_outputs` (CGRP literature) | Empty query; patient conclusion ("Erenumab 70 mg SC monthly appropriate after 2 failed preventive medications"); eligibility stated without source. | FIXED: general evidence with query set: STRIVE (Goadsby NEJM 2017), NICE TA682/TA659/TA764 (at least 3 failed preventives, at least 4 migraine days, 12-week stopping rule), Sacco 2022, AHS 2021 (at least 2 failures). Moved last. |
| C | major | `followup_outputs` (alcohol literature) | Patient-specific ("CURRENT PATIENT: 8-10 units/week, moderately elevated"; 8-10 units is within the UK 14-unit guidance); invented "<7 units/week" target. | FIXED: deleted. |
| C, D | major | `followup_outputs` (erenumab drug check) | Summary-only, empty structured fields; conclusion voice; erenumab hypertension warning missing. | FIXED (class C): structured output for erenumab, candesartan and topiramate against sumatriptan, naproxen and the IUS (incl. NSAID with candesartan, topiramate with the IUS), pregnancy contraindications, erenumab constipation and hypertension, NICE formulary restriction, fremanezumab and galcanezumab as alternatives. |
| A, C | major | `ground_truth.action_criteria[action-2-check-drug-interactions]` | `{"context": ...}` alternative, unattainable; required with no concrete interaction; duplicate `[AAN_2000]` keys; `[Sacco_2022]` in the expected evidence. | FIXED: optional (plan 3.5), `{"drug": ...}` for erenumab, candesartan, topiramate, fremanezumab, galcanezumab; new label, rationale, expected evidence; citations emptied. |
| C | major | `ground_truth.action_criteria[action-1-search-medical-literature]` | Required literature with a fixed query (ROUND_POLICY 5). | FIXED: optional, `{}`, last, out of the stop rule. |
| A, E | minor | `ground_truth.action_criteria[action-3-perform-clinical-assessment]` | Rationale equal to the label; generic expected evidence; free-text citation. | FIXED: patient-specific; `["[ICHD_3]"]`. |
| C | major | `ground_truth.assessment.required_recommendations`, `metadata.difficulty_description` | "anti-CGRP therapy appropriate after 2 failed preventives" and "Consider CGRP mAb if conventional preventives have failed": she is in the UK, where NICE TA682/TA659/TA764 require at least 3 failed preventive drugs and at least 4 migraine days a month; "Optimise preventive therapy [Holland_2012]" vague and miscited; diagnostic must. | FIXED: musts: diagnosis with the TIA query re-attributed, no antithrombotic; a third oral class now (candesartan 8-16 mg, or topiramate under the pregnancy prevention programme with her IUS), review at 8-12 weeks; CGRP antibody if that fails [Sacco_2022]; acute plan (sumatriptan with naproxen at onset, adequate supply, under 10 triptan days). Difficulty description updated. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "Do not anticoagulate for misattributed 'TIA'" (class G); ergot boilerplate. | FIXED: class G prohibition, adapted (see Open questions); canonical combined-contraception prohibition kept (reproductive age); ergot line deleted; valproate prohibition added (class Q). |
| D, E | minor | `ground_truth.key_clinical_evidence` | "July 2026 review applied end to end..." (class D); CGRP line without the eligibility facts. | FIXED: three lines (TIA query features, prevention threshold and the NICE sequence, IUS category). |
| B | major | `ground_truth.red_herrings[1]`, `[2]` | [1] duplicates [0] with an empty field path; [2] "Small PFO on bubble echo": no echo exists in the case (class E). | FIXED: both deleted; [0] reworded with the episode's features. |
| B | minor | `ground_truth.differential` | TIA excluded by "normal vascular imaging then and now" (no vascular imaging in the case); MOH unquantified. | FIXED: TIA very low with the episode's features and the reported MRI; MOH low with her acute-drug days (G44.41); G43.009 for migraine without aura. |
| A | minor | `fallback_tool_outputs.specialized_test`, `metadata.fallback_tool_kinds` | Fallback keyed "Neurodiagnostic assessment" (class M). | FIXED: null; kind entry removed. |
| C | minor | `ground_truth.stop_rule` | Literature and drug check in the stop rule. | FIXED: clinical assessment only; max 0. |
| E | minor | `patient.chief_complaint`, `patient.pmh[0]`, HPI paragraph 2, avoided-action rationales | Pre-existing em dashes in untouched text. | FLAGGED, left unchanged (no churn). |

## Changes, in one paragraph a physician can read before re-reviewing
The patient block no longer tells the agent that the old "TIA" was aura: it describes the episode (20 minutes of shimmering spreading across the left visual field, then headache, no limb or speech symptoms, normal MRI at the time) and leaves the judgment to the agent. The IUS is recorded as her contraception. The ICHD-3 assessment is written for her (3-4 severe attacks a month, 5 of 6 C characteristics, two failed preventives). Only the assessment is required; the drug check (erenumab, candesartan, topiramate against her medicines) and a general literature search on CGRP antibodies are optional; the alcohol search and the PFO red herring, which had no data behind them, are gone. Musts: the TIA query re-attributed with no antithrombotic; a third oral preventive now (candesartan, or topiramate with her IUS under the pregnancy prevention programme); a CGRP antibody if that fails, since NICE requires three failed preventives; sumatriptan with naproxen at headache onset. Prohibitions: no antithrombotic for presumed TIA, no combined hormonal contraception, no valproate.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): drop "migraine aura" from the G43.109 group.
- Criteria pack (plan 5.3): add `[AHS_2021]`, `[MHRA_topiramate_2024]`, `[UKMEC_2016]`, and a key for NICE TA682 (CGRP antibodies) if the pack is to cite it.

## Open questions for Andrea (judgment calls you could not settle)
- None needing Andrea. Decided: (1) the class G canonical prohibition says "succession of symptoms"; her aura is visual only, so I wrote "positive symptoms spreading over minutes, followed by headache, identical to her previous attacks" and "the MRI at the time showed no infarct", to keep the sentence true for this patient. (2) The CGRP step follows NICE (three failures) rather than AHS 2021 (two), because the patient is British; both are given in the literature output.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the final case. Checked: the HPI no longer gives the answer; STRIVE figures (3.2 and 3.7 vs 1.8 days), NICE TA682/TA659/TA764 criteria (at least 4 migraine days, at least 3 failed preventives, 12-week 50% stopping rule for episodic migraine) and the erenumab hypertension and constipation warnings are correct; LNG-IUS is highly effective contraception for the topiramate programme; MOH grading consistent with the acute-drug days; no PFO or vascular-imaging residue.
Found and fixed: the TIA prohibition said the queried episode was "identical to her previous attacks", but the case places that episode in the left visual field while her usual aura starts on the right. Now "the same features as her usual attacks" (`ground_truth.assessment.prohibited_recommendations[0]`), consistent with the key evidence and red herring, which already said "same features".
Checks run after my edits: `perfect_agent.py -v` passes (the clinical assessment shows `<- ?` as in every MIG-AURA case: the initial output is served, the source lookup only fails on null fields), `case_io.py check` clean for the case, `test_case_guards.py -k` 2 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x3.
- CGRP must: NICE criteria attributed to the NICE technology appraisals, [Sacco_2022] kept for what the EHF 2022 guideline says.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.
