# FEPI-TEMP-RS03
Reviewer status: no reviewer notes for FEPI-TEMP (R1 and R2 never reviewed this condition in a notes round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: the July 2026 tool guidance for focal_epilepsy_temporal via plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.mri` (classes E, U) | "Reduced by approximately 30%" with 2.0 vs 3.3 cm3 (39%); gadolinium lines in an HS case; teaching thresholds in volumetrics; no technique line; nothing on the venous sinuses in a postpartum patient with headaches. | FIXED: 3T epilepsy-protocol technique line, no gadolinium; size "39% smaller"; index 0.25 as (L - R)/(L + R); temporal horn enlargement added; normal dural sinus flow voids, no venous infarct or hemorrhage; numbered impression. |
| C | major | `initial_tool_outputs.labs` (class M) | Prolactin 48.2 drawn about 4 h after the event, flagged abnormal (fact 11: no value at that interval); chloride 101 with sodium 139 and bicarbonate 21 gives an anion gap of 17, unlike topiramate's normal-gap acidosis. | FIXED: prolactin row and mentions deleted; chloride 106 (anion gap 12); interpretation in panel voice. |
| C | major | `ground_truth.key_clinical_evidence` (plan RS03) | The plan says the low topiramate level points to missed doses; the HPI says no missed doses, and 3.2 mcg/mL is the expected level for 100 mg daily. | FIXED, deviating from the plan (see Open questions): KCE and labs evidence say clearance has normalized by 6 weeks and the level matches the low dose; sleep deprivation is the precipitant. |
| B | minor | `initial_tool_outputs.eeg` (class K) | Limitations recommended prolonged video-EEG; discharges "every 1-2 minutes" called frequent (ACNS borderline occasional). | FIXED: recording's own limits; frequency 1-2 per minute; numbered ABNORMAL impression. |
| D | minor | `followup_outputs` FDG-PET (class J) | FDG-PET follow-up with no criterion; text identical to RS02's. | FIXED: deleted (not moved to the fallback); FDG_PET waste avoided action added. |
| D | major | `followup_outputs` literature (classes A, O) | Meador Epilepsia 2014, Pennell Neurology 2008 with a wrong title and Harden Epilepsia 2009 (does not exist) with invented figures. | FIXED: Harden 2009 (Neurology 73:142-149, breast milk transfer), Tomson 2018 (EURAP), MHRA June 2024 topiramate pregnancy prevention programme; general summary; trigger `search_literature_asm_breastfeeding_pregnancy_risk`; last in the pathway. |
| C | minor | `followup_outputs` drug check (class B) | Interactions trivial; renal warning quoted the patient's creatinine; oxcarbazepine offered without its contraceptive interaction; nothing on contraception. | FIXED: levetiracetam-topiramate cross-titration, iron supplement, hormonal contraception; alternatives lamotrigine (ethinylestradiol lowers levels), higher topiramate (above 200 mg/day lowers contraceptive efficacy, pregnancy prevention programme), lacosamide; postpartum mood and breastfeeding warnings. |
| A | major | `ground_truth.action_criteria` (classes A, B, D, E, H) | MRI `{contrast: true, protocol: epilepsy}`; literature and drug check required with template evidence; labs optional with the template; doubled citations; rationales equal labels. | FIXED: order MRI, EEG, labs, drug check, literature. MRI `{protocol: epilepsy}` required [ILAE_MRI_2019]; routine EEG required [IFCN_ILAE_EEG_2023]; labs `{panels: [BMP, AED_levels]}` recommended [AAN_WWE_2009]; drug check recommended [MHRA_TPM_2024]; literature optional [EURAP_2018]; case-specific labels, rationales, evidence. |
| A | minor | `ground_truth.sequence_constraints`, `.stop_rule` (classes C, D) | Template constraint reason; stop rule with literature and drug check, max 0. | FIXED: MRI -> drug check soft kept with the canonical reason (drug check recommended); stop rule MRI, EEG, max 2. |
| C | major | `ground_truth.assessment` (class L) | Musts were insight or work-up steps (recognize the aura, check level, 3T MRI); "consider a second agent" before optimizing the first; no breastfeeding, contraception, topiramate pregnancy rules, infant safety, SUDEP; generic LP prohibition; "no second ASM without the level" prohibition. | FIXED: musts: switch to lamotrigine or levetiracetam or raise topiramate within its pregnancy prevention programme; contraception and folic acid; breastfeeding with infant monitoring; infant safety; sleep protection with shared night feeds; SUDEP; driving. Prohibitions: ENT referral (kept), valproate (canonical), stopping breastfeeding. |
| C | major | `ground_truth.differential` (class P) | "Breakthrough seizure from suboptimal topiramate" listed `high` with the label's own ICD code; provoked seizure entry conflated sleep deprivation; postpartum mimics (cerebral venous thrombosis, late postpartum eclampsia) absent. | FIXED: breakthrough entry removed (it is the labelled diagnosis; KCE carries it); new structural lesion, postpartum CVT (O87.3), acute symptomatic seizure `low`; late postpartum eclampsia (O15.2), PNES, convulsive syncope `very_low`; each with the excluding finding. |
| C | minor | `ground_truth.avoided_actions` (class I) | Template rationales. | FIXED: case-specific rationales for CSF, echo, Holter and CT waste (CT kept as waste: back to baseline, normal exam, MRI available); FDG_PET waste added. |
| D | minor | `ground_truth.key_clinical_evidence` (class G) | Engineering lines; "hippocampal sclerosis on prior imaging" (no prior imaging in the case). | FIXED: five case-specific statements. |
| C | minor | `ground_truth.red_herrings` | Empty. | FIXED: sibling with childhood absence epilepsy (`patient.clinical_history.family_history[3]`) as a lure toward generalized epilepsy and valproate. |
| B | minor | `patient.neurological_exam.additional` | "Small healing lateral tongue bite" 4 h after the seizure. | FIXED: "Fresh lateral tongue bite on the right side." |
| E | minor | `patient.history_present_illness` (class R) | Duplicate surname Ramirez (RM04, RS02). | FIXED: Ms. Arredondo (used nowhere else in the dataset). |
| A | minor | `fallback_tool_outputs.echo` (class I) | No `echo_type`. | FIXED: `TTE`. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | Described the low level as "a clear explanation". | FIXED: describe the management challenge. |

## Changes, in one paragraph a physician can read before re-reviewing

Ms. Arredondo (renamed), 31, with right mesial temporal epilepsy on topiramate 100 mg daily for 17 years, had a focal to bilateral convulsion six weeks after delivery while breastfeeding, after rising aura frequency since the third trimester and with no missed doses. The required epilepsy-protocol MRI shows right hippocampal sclerosis (volumes now consistent: 39% smaller) with normal venous sinuses and no gadolinium; the required routine EEG shows right anterior temporal sharp waves. Labs are recommended: topiramate 3.2 mcg/mL, which the case now reads as the expected level for a low dose once pregnancy clearance has normalized (not missed doses), and a normal-gap bicarbonate of 21; prolactin is gone. The drug review is recommended and now covers contraception interactions; literature is optional with real sources; FDG-PET is waste. Management: offer a switch to lamotrigine or levetiracetam or raise topiramate within its 2024 pregnancy prevention programme, contraception and folic acid, continue breastfeeding with infant monitoring, infant safety, protected sleep, SUDEP and driving advice; no valproate, no ENT referral, no advice to stop breastfeeding. Postpartum CVT and eclampsia are in the differential and excluded.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys not yet in the pack allow-list: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`, `[AAN_WWE_2009]`, `[MHRA_TPM_2024]`, `[EURAP_2018]` (plan request 2).
- Synonyms (plan request 6): the inherited idiopathic codes G40.009/G40.019 do not fit structural epilepsy.
- `perfect_agent.py` prints `<- ?` for the labs criterion (the `exclude_none` comparison in `_source`); the stored labs output is the one served.

## Open questions for Andrea (judgment calls you could not settle)

- Decided, deviating from the plan: the plan says the low topiramate level points to missed doses. The HPI states she denies missed doses, the drug is dosed once daily at 100 mg, and a level around 3 mcg/mL is what that dose usually gives; by six weeks postpartum the pregnancy-related rise in clearance has resolved. Writing "missed doses" would contradict the history, so the case says the level reflects her low dose, sleep deprivation is the precipitant, and the plan is to optimize treatment.
- Decided: the "breakthrough seizure" differential entry was removed because it carried the labelled diagnosis's own ICD code at `high`; postpartum cerebral venous thrombosis and late postpartum eclampsia were added because a seizure with headaches six weeks after delivery raises them (fact 16).

## Verification

Adversarial verifier, 24 Oct 2026. Checked the log against the case file and `git diff master`. Tiers (MRI, routine EEG required; labs `{panels: [BMP, AED_levels]}` and drug check recommended; literature optional), the MRI -> drug check soft constraint with the canonical reason (kept because the drug check is recommended) and the stop rule (MRI, EEG; `max_additional_actions: 2`, as plan 3.4 sets) match the plan. Volumetrics (2.0 vs 3.3 cm3: 39%, index 0.25), anion gap (139 - 106 - 21 = 12, normal-gap as with topiramate), the age arithmetic (diagnosis at 14 plus 17 years), the red-herring path `family_history[3]`, the breastfeeding and MHRA 2024 topiramate statements and the literature sources hold. The worker's departure from the plan on the topiramate level (no missed doses, as the HPI says; the level fits 100 mg daily once clearance has normalized) is consistent with the history and accepted. Guards pass.

Found and fixed:
- `initial_tool_outputs.eeg.findings[0]`: "Sharp waves" with "duration 50-80 ms" (largely spike range); now 80-140 ms. The finding and impression were also word for word the RS02 report ("Phase reversal at F8 with field extending to T4 and F4"); this report now has its own field (phase reversal at T4, field to F8 and T6), with the impression and the EEG criterion `expected_evidence` updated to match.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-4-search-medical-literature.label`: "Optional" prefix removed.

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Soft MRI -> drug check constraint: citation `[ILAE_MRI_2019]` -> `[NICE_NG217_2025]`, as in the other cases (ASM choice is what the constraint is about; auditor flag).
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.
