# SYNC-CARD-RM02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for SYNC-CARD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | initial_tool_outputs.ecg | "Sinus bradycardia at 48 bpm" with 2:1 AV block: 48 bpm is the ventricular rate; the febrile sinus rate must be about twice that | FIXED: sinus rhythm, atrial rate 92 bpm, ventricular rate 48 bpm; Mobitz II described by non-conducted P waves without PR prolongation; em dash removed |
| A | major | followup_outputs[monitoring], ground_truth.action_criteria[monitoring] | Ambulatory 24 h Holter with "patient diary" in an admitted patient; holter_24h pinned while the label says telemetry | FIXED (plan E): inpatient telemetry 48 h, trigger `request_telemetry_holter_monitoring`, time-stamped complete-block episodes, "patient reported dizziness on waking"; alternatives telemetry, holter_24h, holter_48h; same report as `fallback_tool_outputs.cardiac_monitoring` |
| A | major | ground_truth.sequence_constraints | Hard labs before monitoring: delays Class I monitoring for blood results | FIXED (plan D): deleted; soft ECG before TTE and before monitoring |
| A | major | ground_truth.action_criteria[labs] | CBC+BMP+troponin+ESR+CRP+ASO pinned | FIXED (plan C): required `panels: [ESR, CRP, ASO]`, the assays that decide rheumatic activity |
| D | minor | initial_tool_outputs.labs | CRP filed under cardiac markers; troponin "likely represents minimal myocardial injury and warrants serial testing"; "(moderate anemia)", "(microcytic)" annotations | FIXED: CRP moved to the inflammatory panel; interpretive text removed, plain values |
| A | major | ground_truth.action_criteria[drug], followup_outputs[drug] | Required with no `drug`; the only drug output reviewed warfarin "for atrial fibrillation prophylaxis" (no AF, no stenosis, no indication) and was served to any drug query | FIXED (plan B): required `{drug: chloroquine}` with a chloroquine follow-up (QT and conduction toxicity); benzathine penicillin follow-up (the must); warfarin output deleted; neutral medication-list review as initial and fallback |
| D | major | followup_outputs[literature] | Three references that cannot be verified as given ("Heart 2021 systematic review", Epilepsia 2022, Lancet Glob Health 2023) and a patient-specific summary; literature required and in the stop rule | FIXED (plan A): optional; one follow-up citing Gewitz 2015 (Jones criteria), Glikson 2021 (ESC pacing) and Gerber 2009 (AHA prophylaxis), trigger `search_literature_rheumatic_carditis`, last; neutral initial literature answer |
| A | major | ground_truth.action_criteria[exercise test] | Recommended exercise test in symptomatic Mobitz II with paroxysmal complete block | FIXED (plan J): criterion deleted; exercise test waste; the stored report kept (so the library does not answer with a normal test), with peak HR corrected to 41% of predicted (was 46%) and the termination reason made consistent |
| C | minor | ground_truth.avoided_actions | No EEG, tilt or exercise avoidance; reasons did not name the diagnosis; CSF uncited | FIXED: brain MRI, head CT (no NG232 criterion), CSF, EEG, tilt and exercise all waste, each naming the diagnosis |
| A | minor | ground_truth.assessment.prohibited_recommendations | "Do not call `order_specialized_test` ..." engineering text; tilt prohibition (a test) | FIXED (plan H, I): deleted; tilt is an avoided action |
| C | major | ground_truth.assessment.required_recommendations | "Admit to telemetry" and "pacing" only; no chloroquine, no recurrence treatment, no reversible-cause pacing plan, no penicillin despite a sulfonamide-only allergy, no valve follow-up | FIXED (plan RM02): see Changes |
| C | major | ground_truth.differential | HCM and channelopathy moderate after normal wall thickness and a block mechanism; no rheumatic activity, chloroquine or malaria; family sudden death at 42 not addressed | FIXED (plan K): recurrent ARF with carditis high (Jones 2015), chloroquine cardiotoxicity and malaria low, familial conduction disease/laminopathy moderate, HCM and channelopathy low with the excluding results |
| D | minor | ground_truth.red_herrings | data_points paraphrased; "normal EEG" (non-criterion tool) cited; age herring not a quoted field | FIXED: five quoted herrings (queue event, jerks, clinic seizure label, anaemia, malaria history) |
| B | minor | followup_outputs[TTE] | No echo_type; no dimensions, wall thickness, MVA, TAPSE or PASP; "consistent with rheumatic involvement" diagnosis sentence | FIXED (plan G): full TTE report, same LVEF 45%, LA 48 mm, moderate MR and mild AR; morphology described without the diagnosis |
| E | minor | followup_outputs[CMR, tilt] | Em dashes and interpretive "post-inflammatory fibrosis pattern" | FIXED: plain findings |
| B | minor | patient.demographics.ethnicity | "East African" with the Akan (Ghanaian) surname Osei | FIXED: West African |
| E | minor | all criteria | rationale equal to label; section citations, [Locati_2014], [ROSE_2010] | FIXED |
| A | major | ground_truth.stop_rule | Literature and drug in, max 0 | FIXED: ECG, labs, TTE, monitoring, chloroquine review; max 3 |
| E | minor | ground_truth.key_clinical_evidence | "Class I pacing indication regardless of age" ignores the reversible cause | FIXED: rewritten (temporary pacing while carditis treated, permanent if the block persists) |

## Changes, in one paragraph a physician can read before re-reviewing
21-year-old nursing student with prior rheumatic fever (prophylaxis stopped at 18), three abrupt collapses in two months with brief jerks, fever 38.2 C, polyarthralgia and self-prescribed weekly chloroquine. ECG: sinus rhythm 92 with Mobitz II (ventricular rate 48) and bifascicular block; telemetry 48 h: paroxysmal complete block with a 4.8 s pause; ESR 48, CRP 18.4, ASO 340, malaria tests negative; TTE: rheumatic mitral and aortic disease, LVEF 45%; CMR: non-ischaemic LGE with septal oedema. Required: ECG, ESR/CRP/ASO, TTE, monitoring, chloroquine review; recommended: CMR; optional: literature; waste: brain MRI, head CT, CSF, EEG, tilt, exercise test. Musts: monitored bed with pacing pads; stop chloroquine; treat recurrent ARF with carditis, temporary pacing while it is treated; benzathine penicillin G then secondary prophylaxis to at least age 40 (sulfonamide allergy is not a penicillin allergy); permanent pacemaker if the block persists; valve follow-up; ECG screening of relatives; driving and sport advice. Prohibitions: no antiseizure drugs, no AV-nodal blockers, no discharge without a pacing plan, no withholding of penicillin.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Neutral initial literature and drug answers kept (see P02 CENTRAL).
- Synonyms (plan C1): accepted labels include generic "cardiac syncope", "bradyarrhythmia" and "second degree av block"; the lead should decide whether a rheumatic or carditis label ("rheumatic carditis with heart block") should be added and the generic ones narrowed; ICD I01.x is not in the accepted codes.
- Library: an off-pathway TEE order returns a normal library TEE ("normal size and systolic function"), contradicting LVEF 45%.

## Open questions for Andrea (judgment calls you could not settle)
Both questions below were resolved by the verifier (see Verification); none remains open.
- Family history: father's sudden death at 42 and a brother's exertional syncope, with bifascicular block and mid-wall LGE, also fit LMNA cardiomyopathy or familial conduction disease. I made it a moderate differential and added relative screening to the musts. If the block persists and LMNA were positive, ESC 2022 favours an ICD over a pacemaker; whether the case should say so, or drop the family history, is a clinical design choice.
- Mobitz II with bifascicular block is atypical for acute rheumatic carditis (usually first-degree or Wenckebach block); the plan's "temporary pacing while carditis is treated" is applied, but a cardiologist should confirm the infranodal pattern is acceptable for this diagnosis.

## Verification
Adversarial verifier, 24 Oct 2026. Read the whole final case against the plan (RM02 bullets, sections A-O) and the log.
- Confirmed: ECG atrial 92 / ventricular 48 with intermittent 2:1 is consistent; telemetry ventricular escape 28-32 bpm, 3:1 conduction at atrial 84-104 bpm gives 28-35 bpm; CMR LVEF (168-92)/168 = 45%, LVESV index 92/1.71 = 54 mL/m2; TTE PASP 36 mmHg from TR 2.8 m/s; labs required ESR, CRP and ASO; no labs-before-monitoring constraint; chloroquine drug check required; no "Do not call" text; exercise criterion deleted and waste (peak 82 = 41% of 199); CMR recommended; chloroquine cardiotoxicity, ARF carditis (Jones 2015) and malaria in the differential; the Jones minor thresholds (fever 38.0 C, ESR 30, CRP 3.0 mg/dL) and the Gerber 2009 prophylaxis duration are stated correctly; benzathine penicillin is safe with the sulfonamide-only allergy; musts match the plan.
- Found and fixed:
  1. C/B, minor: the medication-list review (initial and fallback drug output, served for any drug the agent names other than chloroquine or penicillin) said only "no clinically significant interaction" and did not mention that chloroquine on the list prolongs QT and impairs conduction, in a patient with Mobitz II and QTc 492 ms. Added a warning in report voice (not the criterion's wording) to both blocks.
  2. C, minor (resolves the worker's first open question): the permanent-pacing must now adds that an ICD-capable device replaces a pacemaker if genetic testing shows a laminopathy (ESC 2021 pacing IIa; ESC 2022), since the case keeps the father's sudden death and the brother's syncope and screens relatives.
- Worker's second open question, resolved without a change: infranodal (Mobitz II) and complete block are uncommon in rheumatic carditis, where first-degree block is typical, but are reported, and the case is seeded from a published case (PMC10507219). Inflammatory markers, CMR oedema and the valve morphology support active carditis, so the plan's temporary-then-permanent pacing logic stands.
- Re-ran `perfect_agent.py SYNC-CARD-RM02 -v` (ok), `case_io.py check` (clean for this case) and the case guards (pass).

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: generic complete heart block and Mobitz labels no longer granted here (chloroquine toxicity and familial conduction disease are its mimics); rheumatic carditis / rheumatic heart block labels and I01.8, I01.9 added (summary C1). Residual: primary code I44.2 still credits a CHB answer coded I44.2 (code-alone scorer item, CENTRAL).
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-2-interpret-labs citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]', '[Gewitz_2015]']; action-8-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; action-5-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; avoid-waste-2-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RM02` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.
