# MIG-AURA-M02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (structured ICHD-3 history required, MRI for red flags only, echo removed from routine use), applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness`, `patient.hpi` | "She has ... no family history of stroke" contradicted "her father had a stroke at age 45" in the same HPI and in `family_history[0]`. | FIXED: "She has no cardiac disease and no hypertension." in both copies. |
| D | major | `patient.clinical_history.medications[0].indication` | "Contraception, REQUIRES URGENT REVIEW" pointed at the management. | FIXED: "Contraception". |
| B | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentences copied, generic red-flag line, placeholder modality score. | FIXED: structured assessment of her two attacks (A two attacks; B visual then sensory; C1-C6 with her data, C5 met by the visual scintillation while the numbness is negative), examination today, SNNOOP10 line naming the flag present (recent new headache type), medicines and vascular risk; criteria all true plus `all_criteria_for_migraine_with_aura_1_2_met`; impression supports 1.2.1.1. |
| D | major | `initial_tool_outputs.mri.impression` | "No venous sinus filling defect on MRV" and "Normal MRA" inside a brain MRI report (class K); `findings` empty while the impression named WMH. | FIXED: vessel text removed; structured `white_matter_lesion` finding (two punctate frontal subcortical foci); pertinent negatives including normal anterior temporal white matter and external capsules (relevant to the CADASIL question the family history raises). No vessel study added (plan: none for M02). |
| C | major | `ground_truth.red_herrings`, `assessment`, `key_clinical_evidence[1]`, `differential[0]` | A "small PFO seen on bubble echocardiogram" that exists nowhere in the case (no echo output; echo is not routinely indicated); "Full thrombophilia screen negative" and "normal ... Holter" with no labs or monitoring in the case (class E). PFO must cited `[Charles_2017]` (class N). | FIXED: PFO red herrings (two), PFO must, PFO closure prohibition, PFO key-evidence line and PFO differential wording deleted; thrombophilia and Holter claims deleted. No echo added (plan). New red herrings point at real data: father's stroke (`family_history[0]`), numbness without tingling (HPI), travel to Nigeria (`social_history.note`), punctate WMH (`initial_tool_outputs.mri.findings[0]`). |
| C | minor | `ground_truth.avoided_actions` | Nothing discouraged the bubble echo the father's stroke invites. | FIXED: new `avoid-waste-3-order-echocardiogram` (PFO screening and closure not indicated for migraine with aura; PREMIUM, PRIMA, MIST named in the rationale). |
| A | major | `action-2-check-drug-interactions` | `{"context": ...}` criterion not sendable; output a free-text essay with empty `contraindications` and `alternatives`. | FIXED (class C): ten `{"drug": ...}` alternatives (Yasmin as written, ethinylestradiol spellings, drospirenone, combined oral contraceptive / hormonal contraception); follow-up `followup_outputs[0]` with those trigger tokens; output gives her paracetamol and triptans (no interaction), UKMEC 4 / WHO MEC 4 at any age, drospirenone VTE warning, switch without a gap, alternatives with categories. Required (concrete contraindication). |
| A | major | `action-1-search-medical-literature`, literature follow-ups | Required literature step in the stop rule; `query` = slugs; second block on ethnicity, sickle cell and thrombophilia screening with no source and claims not relevant to this case. | FIXED: criterion optional, `{}`, last; ethnicity block deleted; one follow-up (`followup_outputs[1]`, last) with Russell and Olesen, Brain 1996 and ICHD-3, general findings only. |
| C | minor | `assessment` | Ergot prohibition with no ergot (class I); "Initiate sumatriptan" without timing; nothing on vomiting or frequency. | FIXED: ergot line deleted; canonical combined pill prohibition; musts: stop Yasmin with named alternatives, sumatriptan at headache onset with an NSAID and metoclopramide 10 mg (she vomits), triptans under 10 days a month (NICE CG150), diary with no preventive at two attacks in six weeks (AHS 2021). |
| C | minor | `ground_truth.differential` | TIA entry built on PFO and Holter; AVM "normal vascular imaging expected" with no vascular imaging; CADASIL, raised by migraine with aura and a parent's stroke at 45, absent. | FIXED: TIA low with the clinical features; CADASIL added very low with the MRI regions that exclude it; seizure and AVM/cavernoma very low with case-specific features. |
| D/E | minor | `key_clinical_evidence` | Engineering sentence "July 2026 review applied end to end..." (class D). | FIXED: deleted; four lines from this case. |
| A | minor | `fallback_tool_outputs.advanced_imaging`, `.specialized_test`, `metadata.fallback_tool_kinds` | "MRA head and neck" and "Neurodiagnostic assessment" junk fallbacks (class M). | FIXED: null, kinds removed. The CT fallback (incidental calcified granuloma) is a correct normal-variant report and stays. |
| C | minor | `action-3`, `action-4` | Template labels and rationales; MRI arguments `{"contrast": false, "protocol": "standard"}`; duplicate and free-text citations. | FIXED: case-specific text; MRI `{}`, optional; `[ICHD_3]`, `[AAN_2000]` one key each; drug check citations empty, UKMEC/WHO MEC named in the rationale. |
| C | major | `sequence_constraints`, `stop_rule` | None; literature in the stop rule, max 0. | FIXED: soft history-before-MRI; stop rule = action-3 and action-2, max 1. Criteria order history, MRI, drug check, literature. |
| B | minor | `metadata.condition_name`, `difficulty_description`, `difficulty_rationale` | Described a PFO and an MRV the case does not contain. | FIXED: rewritten to the case as it is. |
| E | minor | `avoided_actions[1].rationale` | Em dash. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 29-year-old woman on Yasmin has had two stereotyped attacks in six weeks of left visual scintillation followed by left hand and cheek numbness and a right-sided migrainous headache; her father had a stroke at 45. The HPI no longer says she has no family history of stroke. The structured history output applies ICHD-3 to her attacks (criteria met, 6 of 6 C characteristics; numbness is a negative sensory aura symptom). The PFO that the label, red herrings, must and prohibition referred to did not exist anywhere in the case, so all PFO text is gone and a routine echo is now a waste action; the thrombophilia and Holter claims are gone too. MRI stays optional and reports only two punctate non-specific WMH (MRV and MRA text removed). The drug check (required) is orderable by drug name and states UKMEC/WHO MEC category 4. Musts: stop Yasmin and switch without a gap; sumatriptan at headache onset with an NSAID and an antiemetic; diary, no preventive at this frequency. CADASIL is added to the differential as very low, with the MRI regions that argue against it.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `ground_truth.diagnosis.accepted[0]` still ends "small PFO, no closure indicated": the case contains no PFO (no echo output, and the plan rules out adding one). Recommend relabelling to "Migraine with combined visual and sensory aura (ICHD-3 1.2.1); combined OCP contraindicated (WHO Category 4)". Left unchanged per the plan's default (section 4, M02; section 5.4) because ROUND_POLICY 3 reserves label edits; the clause is a management note, not the entity, and does not affect token scoring.
- `diagnosis_synonyms.yaml` G43.109: drop "migraine aura" (plan 5.1).
- Criteria pack allow-list: `[UKMEC_2016]`, `[WHO_MEC_2015]`, `[AHS_neuroimaging_2020]`, `[NICE_CG150]`, `[AHS_2021]`, `[PREMIUM_2017]`, `[PRIMA_2016]`, `[MIST_2008]`.

## Open questions for Andrea (judgment calls you could not settle)

None beyond the CENTRAL label clause above, which needs the central synonym and label owner rather than a clinical decision.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the HPI fix (father's stroke now consistent), structured-history criteria versus the HPI (C3 and C5 reasoning), timeline of the Nigeria travel red herring (8 weeks ago, 2 weeks before the first attack: consistent with `social_history`), MRI report, removal of every PFO, thrombophilia and Holter claim (only the label clause remains, correctly left to CENTRAL), drug-check alternatives and trigger, literature sources (Russell and Olesen, Brain 1996; ICHD-3 comment on numbness), musts, differential, red-herring paths, sequence direction, stop rule. Every log claim holds. No reviewer notes exist for this case.

Found and fixed:
- `followup_outputs[0].output.interactions[1]`: same triptan statement as M01 ("no pharmacokinetic interaction" is wrong for zolmitriptan and frovatriptan). Now "no clinically relevant interaction; no dose change needed".

`perfect_agent.py -v` ok, `case_io.py check` clean for the case, guard tests pass.
