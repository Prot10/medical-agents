# SE: condition summary, October 2026 review round

Condition auditor, 24 October 2026. Inputs: `plans/SE.md`, the 30 case logs `logs/SE-*.md`, `notes/SE.md` (24 Reviewer 2 notes on 14 cases), and scripted checks over the 30 case files.

## State at the end of the audit

- `perfect_agent.py` on all 30 cases: 30/30 pass. One warning remains, in SE-M05 (the `pelvis_abdomen_ultrasound` alternative is "answered by a fallback"). The M05 worker probed it directly and the case's ultrasound follow-up is served, so the warning comes from the simulator. It is listed under CENTRAL.
- `case_io.py check` on all 30 cases: schema OK, synonym guard OK, and no test failure names an SE case. `test_case_guards -k SE-` gives 60 passed. The baseline had leak-guard failures in 10 cases.
- Every one of the 24 note ids appears in exactly one case log, with a ruling.
- Straggler found by the audit: **SE-P05 and SE-P08 had never been worked**. There was no log, the files were unmodified against git, and the template blocks, post-treatment outputs and leaks were all still in place. The auditor applied the full plan to both and wrote their logs (`logs/SE-P05.md`, `logs/SE-P08.md`). One further straggler fix was made in SE-P01 and appended to its log.

## Error classes found and how each was fixed

| class | where | fix |
| --- | --- | --- |
| C1 "Exclusion studies" and "Mimic exclusion" template blocks (analytes "within reference range" with no number, contradicting the real panels; notes 0aed33a9, 54e2cb28, f6c10984) | all 30 | Blocks deleted. Each analyte is reported once, in its own panel, with value, unit, range and flag, consistent with the physiology: lactic acidosis after convulsions, abnormal urinalysis in UTI cases, low thiamine in S05, low haptoglobin in S08. CSF assays placed in the serum labs (M05, M06, P06, S12) moved to the CSF report. |
| C2 beta-hCG in men, in a 68-year-old woman and in a known pregnancy (notes 64b7befa, 138b30a5) | P01, RS11, S01, S06, S10, S07, S08 | Removed from panels, labels and outputs. It is kept, with a real negative value, only in M03, M05, P02, P08, S02 and S04. |
| C3 meningitis-panel blood cultures "before antimicrobials" in afebrile or already-treated patients (notes b1f48e5f, e89c4880, 0dd7682a, e610cd86, 59001cc7, 5daa0f16, 0afbb493) | M01, M02, M07, M08, P01, P06, RS11, S01, S12 deleted; case-specific text elsewhere | Deleted where no infection is suspected. Recommended with case text in M05, M06, S03, S04, S05 and P07. Urine culture is required in M09 and S03 (S03 positive, collected on TMP-SMX day 4), and the P07 paracentesis is required. RS11's 38.1 C is explained as seizure-related hyperthermia. |
| C4 outputs that report treatment effects, and treatment disguised as labs (ruling 4) | 22 cases (`request_aed_optimization`, post-treatment cEEG, post-reversal INR, post-pyridoxine and post-pralidoxime panels) | Follow-ups deleted, and treatment criteria turned into musts. The EEG criterion hijack (the trigger token "continuous" matching `continuous_icu`) is gone in every case. The only diagnostic manoeuvres kept are P01 `benzodiazepine_trial` and P03 `sedation_wean`. |
| C5 orphan follow-ups and contradictory LP (notes aeb5068c, 7fb2fc52, fc4e7dc6) | about 20 cases | Orphan CSF, antibody, PET, troponin, intermediate-syndrome and drug-check follow-ups deleted. LP is an avoided action in S07 (contraindicated), S08 and P07 (harm). |
| C6 laterality (notes 0bc30365, 4ccf5d55, 19c53320) | S03, S09, S12, S07, M02, M03, M04, M09, P01, P03, P04, M01 | Signs moved to match the lesion and EEG side: ictal gaze away from the focus, clonus and weakness contralateral. "Contralateral activation pattern" is deleted. In P05 the EEG was rewritten so that left-sided focal runs no longer sit against left-arm twitching. |
| C7 patient-block leaks and reports doing the agent's work | P01, P02, P03, P04, P05, P07, P08 (CC/HPI EEG quotes); M04, RS11 (exam); M01, M02, S08, P02, RS11, P01, P08 (reports) | Rewritten as the presenting problem and as plain reports. Prior pre-encounter results stay as history (P06, S12, S08, M09). |
| C8 literature as a clinical step, with leaks and wrong facts (note 09924507) | all 30 | Literature criteria are optional and last, outside the stop rule. Initial literature outputs are deleted, and the remaining ones are general cited text (T-LIT). The nimodipine "teratogen" and fabricated thresholds are gone (S08). S04 now withholds valproate with L-carnitine, and the sodium limits in S03 and S06 match the musts. |
| C9 drug check mis-tiered, carrying treatment plans or wrong pharmacology | all 30 | Tiers set per plan C9, with real interactions in T-DDI format. Phenytoin and amiodarone are described through CYP2C9 and conduction, not QT (M07, P03). Dexamethasone exposure is lowered by enzyme inducers (S07). Phenytoin is prohibited after SJS (S02), and aromatic ASMs are avoided in S04. A fabricated "COMBAT-OP" trial was removed (P05). |
| C10 non-vocabulary or contradictory fallbacks | most cases | "CT chest", "MRI brain", "fetal_monitoring", "renal_function_assessment" and similar are deleted. ECG, Holter and echo fallbacks are made consistent with the patient. |
| C11 polysomnography entry carrying the DaTscan rationale; unbracketed citation keys | 23 cases | T-PSG text in every PSG entry (P08 was the last one). No unbracketed keys remain. |
| C12/C13 stop rule and sequence constraints | all 30 | `max_additional_actions` is 1 everywhere, and `required_before_assessment` equals the required criteria in all 30. CT before CSF is `hard` in every case with a CSF criterion (P08 added). Labs before drug check is `soft` only where renal, hepatic or level data decide the drug. ECG before drug check is `soft`, except `hard` in S10. |
| C14 differential not updated | all 30 | Each entry is ranked against the whole pathway, and `key_features` names the result that settles it. |
| C15 per-case clinical errors (notes adc24e17, 5ff3c70f, efb6cbfc, 35db0801, 53545e21) | M03, M04, S03, S04, S01, P01, S08, M07, M05, P02 | Applied as planned. Na 121 (S03) and Na 123 (M04) are changed together with the label numbers (CENTRAL). |
| New in the audit: presentation contradicting the label | P05 | The "cholinergic toxidrome" had mydriasis, flushed skin and 40.8 C, an anticholinergic picture. It now has miosis, sweating, bronchorrhea, fasciculations and 38.4 C. |
| New in the audit: impossible exposure and timeline | P08 | "Accidentally consumed 10-15 g of powder after a chemical spill" and fosphenytoin given "in the field" are replaced. She now takes isoniazid for latent TB, about 35 tablets are missing with the circumstances unknown, and fosphenytoin was given in the ED. CK 14200 at one hour of seizures became 1840. |
| New in the audit: guideline key cited for a dose it does not support | P01 (S05 already correct) | The canonical 500 mg tid thiamine dose was attributed to EFNS 2010, which recommends 200 mg tid. The must now cites EFNS for at least 200 mg tid and gives 500 mg tid as common practice. |

Uniformity check: the scripted checks over the 30 files found no surviving shared defect. That covers the template blocks, hCG, template cultures, treatment-response triggers, initial literature and drug outputs, DaTscan rationale, stop rule, CT-before-CSF, literature tier and position, and the canonical T-LABS, T-CT and T-EEG texts. The remaining differences from the plan are deliberate and logged:
- M07: SSEP deleted because she woke, so ERC-ESICM coma prognostication does not apply.
- M09: MRI optional, because the CT decides reversal and evacuation of a herniating SDH.
- P04: MRI recommended, because the cause is established.
- S04: CSF required, because she has had fever since before the seizure while on prednisone 40 mg.
- S05: a recommended CSF criterion was kept, because of fever 39.2 C in a heavy drinker.
- S08: `LDH` is a required lab argument, because it is a HELLP criterion.
- P02: prolactin is a T-LABS extra (plan C15).
- P06: a serum autoimmune encephalitis panel is in the core labs (main treatable mimic of CJD). It is accepted, but it is the only case that adds a non-canonical panel to T-LABS. A central reviewer may prefer it as its own recommended criterion.
- P05: respiratory function test deleted; the auditor's decision, below.
- T-EEG and T-CT labels were adapted with case slots in P02, P04, P06, P07, RS11 and S08.

## Counts

- Reviewer notes: 24 in total. **FIXED 24**, ALREADY-FIXED 0 as a standalone ruling (aeb5068c in S07 is FIXED; one of its parts, the MRI-before-CSF hard constraint, was already absent), DECLINED 0, BLOCKED 0.
- Own findings in the 30 log tables: 551 rows. 550 are FIXED; 1 is a check that needed no change (S12, red herrings). None is FLAGGED. On top of that, the one fix the audit made in SE-P01 is appended to that log. The adversarial verifiers also made further fixes in their verification sections of 28 logs; P05 and P08 had no verifier.
- Cases changed: **30 of 30**.
- Approved cases changed: **26 of 26**. Ten were approved with notes (M03, M04, M06, M07, P01, RS11, S01, S06, S07, S09), and sixteen had no notes and are treated as approved per the plan. Every change in an approved case is logged as a real error: template carry-over, leaks, treatment-effect outputs, impossible values or wrong facts. All four needs-changes cases (S03, S04, S08, S12) were also changed.

## DECLINED and BLOCKED notes

None. All 24 notes were applied.

## Consolidated CENTRAL requests

1. **Criteria pack `dataset-generation/criteria_packs/SE.md`** (plan CENTRAL 1):
   - Allow-list the keys the cases now cite:
     - `[ACNS_2021]` (every case)
     - `[Spasovski_2014]`, `[Verbalis_2013]`
     - `[EFNS_Wernicke_2010]`
     - `[Lheureux_2009]`
     - `[Graus_2016]`, `[Graus_2021]`
     - `[Titulaer_2013]`, `[Irani_2011]`
     - `[Tunkel_2008]`
     - `[Fugate_2015]`
     - `[Hermann_2021]`
     - `[Vilstrup_2014]`, `[AASLD_ascites_2021]`, `[EASL_decomp_2018]`
     - `[ACOG_PB222_2020]`, `[Magpie_2002]`
     - `[ERC_ESICM_2021]`
     - `[Frontera_2016]`
     - `[Eddleston_2008]`, `[Boyer_2005]`
     - `[LaFrance_2013]`
     - `[EANO_2021]` (M02)
     - `[AHA_ASA_Stroke_2026]` (P04, already in the ISCH-STR pack)
   - Add a key for the NIH/CDC/IDSA opportunistic-infection guideline (M08) and toxicology references for isoniazid (P08) and tricyclics (S10).
   - Replace "literature required" and "drug check required" with rulings 5 and 6, and add the canonical facts of plan 1.2.
   - **Correct the plan 1.2 Wernicke fact**: EFNS 2010 supports at least 200 mg tid IV. 500 mg tid is common practice but not in that key (raised by the P01 and S05 workers and the P01 verifier; fixed in both cases).
   - Remove the blood-culture template and the Exclusion-studies block from the SE generator.
2. **Vocabulary** (`costs.yaml` and the `tool_io.py` mirror):
   - lab `cholinesterase`, plasma and RBC (P05; the values now sit in the core labs)
   - CSF `toxoplasma_PCR` and `EBV_PCR`, and serum `toxoplasma_IgG` (M08)
   - lab `urine_sodium` (M04)
   - lab `NSE`: needed only if P03 is ever re-timed to 72 hours. M07 no longer needs it.
   - No `isoniazid_level` is needed (P08 is diagnosed clinically).
3. **Labels, ICD codes and synonyms** (ruling 3; not edited by workers except 3a):
   - (a) S03 "(Na 129)" became "(Na 121)", and M04 "(Na 132)" became "(Na 123)" (changed in the cases). Refresh the synonym expansion.
   - (b) `icd_codes[0]` G41.2 with NCSE synonyms in convulsive cases:
     - recode S07 and S09 to G41.0
     - recode S12 (FBDS status) and S02 to G41.8 (S02 may also take G41.0)
     - M07 (generalized NCSE) fits G41.8 better
     - prune the NCSE synonyms in S02, S07, S09 and S12
     - M01, M08 and M09 (focal NCSE) can keep G41.2
   - (c) Labels with a treatment or future clause, or a wrong mechanism:
     - P05: "nicotinic CNS seizures ... complicated by intermediate syndrome at 48 hours". Proposed: "Organophosphate poisoning with cholinergic crisis and electrographic status epilepticus".
     - P07: "resolving with ammonia correction".
     - P08: "requiring IV pyridoxine as specific antidote".
     - P03: "hypothermia confounding" (the case runs 36 C TTM).
     - M09: "INR 4.8 from ibuprofen-warfarin interaction" overstates a modest pharmacokinetic effect.
   - (d) The P04 and P07 synonym prune already pending in `CENTRAL_PENDING.md`. P04 should drop at least "lacunar" and "cardioembolic", and P07 "hepatic coma".
4. **Generator and matcher**:
   - The cEEG follow-up trigger `request_continuous_eeg_monitoring` shares the token "continuous" with `eeg_type` `continuous_icu`. Exclude the enum tokens of the core order from follow-up matching, or have the generator stop emitting such triggers. This is fixed in all 30 SE cases, but the generator will reproduce it.
   - A combined first lab order that includes a second-tier panel (`HIV`, `paraneoplastic_panel`) is answered by the initial labs (M08, P01), so the agent must re-order the panel.
5. **Tools and library**:
   - The `perfect_agent.py` warning on the M05 ultrasound alternative looks like a simulator artefact. Please check it.
   - A tumour-aware library tier is needed, so that an off-pathway `MR_spectroscopy` in a recurrent glioblastoma (M02) does not return a normal report.
6. **Review UI**: show initial outputs and follow-ups in criterion order (already requested).

## Consolidated open questions for Andrea

None needs information that only Andrea has. Judgment calls decided in the logs that a re-reviewer should know about:
- **M07:** the SSEP criterion was deleted, and prognostication became a prohibition on limiting care. She woke and was discharged, so ERC-ESICM coma prognostication does not apply.
- **P03:** the encounter is set at about 24 hours after return of circulation, so the SSEP and MRI fall inside it while prognostication stays deferred to 72 hours.
- **P05 (auditor):** the respiratory function criterion was deleted against the plan. FVC and NIF cannot be measured meaningfully at GCS 3, and the intermediate syndrome they would track comes 1 to 4 days later; the monitoring is now a must and a prohibition. Glucose was changed from 62 to 186, because organophosphate poisoning typically raises it.
- **P08 (auditor):** the intent of the ingestion is left unknown. This keeps the accidental ICD code valid under the ICD-10-CM rule for unknown intent; a psychiatric-assessment must covers self-harm.
- **P07:** NCSE was kept `moderate`, because nothing in the remaining pathway excludes it, which is why the diagnostic benzodiazepine trial is a must.
- **S03:** the 8 mmol/L in 24 hours limit applies because of potassium 3.4, a demyelination risk factor. S06 uses 10 mmol/L because he has no risk factor.
- **M06:** the equivocal Babinski moved to the left to match the left arm drift (right temporal lesion). The worker asks for a revert if the case is read otherwise.
- **S12:** the serum LGI1 panel is required and the CSF only recommended. CSF can go back to required if both specimens are wanted for a relapse.
- **P06:** the serum autoimmune panel stays inside the core labs (see Uniformity check above). It can be split into its own recommended criterion if preferred.
